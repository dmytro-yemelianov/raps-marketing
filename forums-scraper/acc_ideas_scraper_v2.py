#!/usr/bin/env python3
"""
ACC Ideas Forum Scraper - Enhanced Version
==========================================
Scrapes ideas from https://forums.autodesk.com/t5/acc-ideas/idb-p/acc-ideas-en
using the Khoros Community API v2 (LiQL).

Features:
- Order by kudos (votes)
- Full message body content
- Fetch first N replies per idea
- Filter by reply count (min/max)
- Export to JSON/CSV

Author: For RAPS Marketing research
"""

import requests
import json
import time
import csv
import argparse
import html
from datetime import datetime
from pathlib import Path
from typing import Optional, Iterator, List, Dict, Any, Callable
from urllib.parse import quote

from bs4 import BeautifulSoup

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configuration
BASE_URL = "https://forums.autodesk.com/api/2.0/search"
BOARD_ID = "acc-ideas-en"
OUTPUT_DIR = Path("acc_ideas_data")
BATCH_SIZE = 100  # Max 100 per request
DELAY_BETWEEN_REQUESTS = 0.5  # seconds


class KhorosApiError(RuntimeError):
    """Raised when the Khoros API returns a non-success status payload."""


def create_session() -> requests.Session:
    """Create a requests Session with retries/backoff for common transient errors."""
    session = requests.Session()
    session.headers.update(
        {
            "Accept": "application/json",
            # Keep a stable UA (also helps Autodesk/Khoros ops if they investigate traffic)
            "User-Agent": "ACC-Ideas-Scraper/2.0 (Research purposes)",
        }
    )

    retry = Retry(
        total=6,
        connect=6,
        read=6,
        status=6,
        backoff_factor=0.8,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
        respect_retry_after_header=True,
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


SESSION = create_session()


def liql_query(query: str) -> dict:
    """Execute a LiQL query against the Khoros API."""
    url = f"{BASE_URL}?q={quote(query)}"

    response = SESSION.get(url, timeout=30)
    response.raise_for_status()

    data = response.json()
    if data.get("status") != "success":
        raise KhorosApiError(
            f"API error: {data.get('message', 'Unknown error')} (query={query[:200]!r})"
        )

    return data


def strip_html(html_content: str) -> str:
    """Convert Khoros HTML content to readable plain text.

    Uses BeautifulSoup for correctness (nested tags, lists, links, etc.).
    """
    if not html_content:
        return ""

    # Khoros content is HTML; unescape first so soup sees real characters.
    decoded = html.unescape(html_content)
    soup = BeautifulSoup(decoded, "lxml")

    # Remove non-content elements
    for tag in soup(["script", "style"]):
        tag.decompose()

    # Improve line breaks for common block elements
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for p in soup.find_all("p"):
        # Ensure paragraphs separate
        if p.contents:
            p.append("\n")

    text = soup.get_text(separator=" ")
    # Normalize whitespace a bit (keep it readable, not perfect)
    text = " ".join(text.split())
    return text.strip()


def get_total_count() -> int:
    """Get total count of ideas in the board."""
    query = f"SELECT count(*) FROM messages WHERE board.id = '{BOARD_ID}' AND depth = 0"
    result = liql_query(query)
    return result["data"]["count"]


def fetch_replies(message_id: Optional[str], limit: int = 10) -> List[dict]:
    """Fetch replies for a specific idea using parent.id."""
    if not message_id:
        return []
    query = f"""
        SELECT id, body, post_time, author.login, author.id, kudos.sum(weight)
        FROM messages 
        WHERE parent.id = '{message_id}'
        LIMIT {limit}
    """
    
    result = liql_query(query.strip())
    replies = []
    
    for item in result["data"].get("items", []):
        replies.append({
            "id": item.get("id"),
            "author": item.get("author", {}).get("login"),
            "author_id": item.get("author", {}).get("id"),
            "body_html": item.get("body", ""),
            "body_text": strip_html(item.get("body", "")),
            "post_time": item.get("post_time"),
            "kudos": item.get("kudos", {}).get("sum", {}).get("weight", 0),
        })
    
    return replies


def fetch_ideas_batch(
    cursor: Optional[str] = None,
    limit: int = BATCH_SIZE,
) -> tuple[list[dict], Optional[str]]:
    """Fetch a batch of ideas ordered by kudos."""
    
    fields = [
        "id",
        "subject",
        "body",
        "view_href",
        "post_time",
        "author.login",
        "author.id",
        "kudos.sum(weight)",
        "metrics.views",
        "conversation.messages_count",
        "conversation.id",
        "status.key",
        "status.name",
        "labels",
    ]
    
    query = f"""
        SELECT {', '.join(fields)} 
        FROM messages 
        WHERE board.id = '{BOARD_ID}' AND depth = 0
        ORDER BY kudos.sum(weight) DESC
        LIMIT {limit}
    """
    
    if cursor:
        query += f" CURSOR '{cursor}'"
    
    result = liql_query(query.strip())
    
    items = result["data"].get("items", [])
    next_cursor = result["data"].get("next_cursor")
    
    return items, next_cursor


def fetch_all_ideas(
    max_ideas: Optional[int] = None,
    min_replies: Optional[int] = None,
    max_replies: Optional[int] = None,
    include_replies: int = 0,
    progress_callback: Optional[Callable[[int, int], None]] = None
) -> Iterator[dict]:
    """
    Generator that yields all ideas ordered by kudos (most voted first).
    
    Args:
        max_ideas: Optional limit on total ideas
        min_replies: Minimum number of replies required (client-side filter)
        max_replies: Maximum number of replies allowed (client-side filter)
        include_replies: Number of replies to fetch per idea (0 = none)
        progress_callback: Optional callback(fetched, total) for progress
    
    Note: Reply filtering is done client-side since LiQL doesn't support
    filtering by conversation.messages_count in WHERE clauses.
    """
    total = get_total_count()
    
    cursor = None
    fetched = 0
    yielded = 0
    
    while True:
        if max_ideas and yielded >= max_ideas:
            break
        
        items, cursor = fetch_ideas_batch(cursor=cursor, limit=BATCH_SIZE)
        
        for item in items:
            if max_ideas and yielded >= max_ideas:
                break
            
            # Client-side filtering by reply count
            reply_count = item.get("conversation", {}).get("messages_count", 1) - 1
            
            if min_replies is not None and reply_count < min_replies:
                continue
            if max_replies is not None and reply_count > max_replies:
                continue
            
            # Normalize the idea
            idea = normalize_idea(item)
            
            # Fetch replies if requested
            if include_replies > 0:
                time.sleep(DELAY_BETWEEN_REQUESTS)
                idea["replies"] = fetch_replies(item.get("id"), limit=include_replies)
            
            yield idea
            yielded += 1
            
        fetched += len(items)
        
        if progress_callback:
            # Show progress based on total fetched (not yielded, since we filter)
            progress_callback(fetched, total)
            
        if not cursor or not items:
            break
            
        time.sleep(DELAY_BETWEEN_REQUESTS)


def normalize_idea(raw: dict) -> dict:
    """Convert raw API response to clean data structure."""
    messages_count = raw.get("conversation", {}).get("messages_count", 1) or 1
    reply_count = max(messages_count - 1, 0)
    
    return {
        "id": raw.get("id"),
        "title": raw.get("subject"),
        "body_html": raw.get("body", ""),
        "body_text": strip_html(raw.get("body", "")),
        "url": raw.get("view_href"),
        "post_date": raw.get("post_time"),
        "author_username": raw.get("author", {}).get("login"),
        "author_id": raw.get("author", {}).get("id"),
        "kudos": raw.get("kudos", {}).get("sum", {}).get("weight", 0),
        "views": raw.get("metrics", {}).get("views", 0),
        "reply_count": reply_count,
        "status_key": raw.get("status", {}).get("key"),
        "status_name": raw.get("status", {}).get("name"),
        "conversation_id": raw.get("conversation", {}).get("id"),
    }


def save_to_json(ideas: list[dict], filename: str):
    """Save ideas to JSON file."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(ideas, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(ideas)} ideas to {filepath}")
    return filepath


def save_to_csv(ideas: list[dict], filename: str):
    """Save ideas to CSV file (flattened, no nested replies)."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    filepath = OUTPUT_DIR / filename
    
    if not ideas:
        return filepath
    
    # Flatten for CSV - exclude replies array
    flat_ideas = []
    for idea in ideas:
        flat = {k: v for k, v in idea.items() if k != "replies"}
        # Truncate body for CSV readability
        flat["body_text"] = flat.get("body_text", "")[:500]
        flat.pop("body_html", None)  # Remove HTML from CSV
        flat_ideas.append(flat)
    
    fieldnames = list(flat_ideas[0].keys())
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_ideas)
    
    print(f"Saved {len(flat_ideas)} ideas to {filepath}")
    return filepath


def print_progress(fetched: int, total: int):
    """Print progress bar."""
    pct = (fetched / total) * 100 if total > 0 else 0
    bar_len = 40
    filled = int(bar_len * fetched / total) if total > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"\r[{bar}] {fetched}/{total} ({pct:.1f}%)", end="", flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Scrape ACC Ideas forum - ordered by kudos (votes)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Top 100 most voted ideas
  python acc_ideas_scraper.py -n 100
  
  # Top 50 with 5 replies each
  python acc_ideas_scraper.py -n 50 --replies 5
  
  # Ideas with at least 10 replies
  python acc_ideas_scraper.py --min-replies 10
  
  # Ideas with 5-20 replies, get top 200
  python acc_ideas_scraper.py -n 200 --min-replies 5 --max-replies 20
  
  # All ideas (will take a while for 4000+)
  python acc_ideas_scraper.py --all
        """
    )
    
    parser.add_argument("-n", "--limit", type=int, default=100,
                        help="Number of ideas to fetch (default: 100)")
    parser.add_argument("--all", action="store_true",
                        help="Fetch ALL ideas (ignores -n)")
    parser.add_argument("--replies", type=int, default=0,
                        help="Number of replies to fetch per idea (default: 0)")
    parser.add_argument("--min-replies", type=int, default=None,
                        help="Only ideas with at least N replies")
    parser.add_argument("--max-replies", type=int, default=None,
                        help="Only ideas with at most N replies")
    parser.add_argument("--output", "-o", type=str, default=None,
                        help="Output filename prefix (default: auto-generated)")
    parser.add_argument("--json-only", action="store_true",
                        help="Only output JSON (skip CSV)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Minimal output")
    
    args = parser.parse_args()
    
    # Determine max ideas
    max_ideas = None if args.all else args.limit
    
    if not args.quiet:
        print("=" * 60)
        print("ACC Ideas Forum Scraper - Enhanced")
        print("=" * 60)
        print(f"Ordering: By kudos (most voted first)")
        print(f"Limit: {'ALL' if max_ideas is None else max_ideas}")
        print(f"Replies per idea: {args.replies}")
        if args.min_replies:
            print(f"Min replies filter: {args.min_replies}")
        if args.max_replies:
            print(f"Max replies filter: {args.max_replies}")
        print()
    
    # Get count
    total = get_total_count()
    
    if not args.quiet:
        print(f"Total ideas in board: {total}")
        if args.min_replies or args.max_replies:
            print(f"Note: Reply filtering is done client-side during fetch")
        print()
        print("Fetching ideas...")
        print()
    
    # Fetch ideas
    ideas = []
    progress_cb = None if args.quiet else print_progress
    
    for idea in fetch_all_ideas(
        max_ideas=max_ideas,
        min_replies=args.min_replies,
        max_replies=args.max_replies,
        include_replies=args.replies,
        progress_callback=progress_cb,
    ):
        ideas.append(idea)
    
    if not args.quiet:
        print()
        print()
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output:
        prefix = args.output
    else:
        parts = ["acc_ideas", f"top{len(ideas)}"]
        if args.min_replies:
            parts.append(f"minrep{args.min_replies}")
        if args.max_replies:
            parts.append(f"maxrep{args.max_replies}")
        if args.replies:
            parts.append(f"with{args.replies}replies")
        prefix = "_".join(parts) + f"_{timestamp}"
    
    # Save
    json_path = save_to_json(ideas, f"{prefix}.json")
    if not args.json_only:
        save_to_csv(ideas, f"{prefix}.csv")
    
    # Summary
    if not args.quiet:
        print()
        print("=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total ideas fetched: {len(ideas)}")
        
        if ideas:
            total_replies_fetched = sum(len(i.get("replies", [])) for i in ideas)
            if total_replies_fetched:
                print(f"Total replies fetched: {total_replies_fetched}")
            
            print()
            print("Top 10 by votes:")
            for i, idea in enumerate(ideas[:10], 1):
                print(f"  {i:2}. [{idea['kudos']:4} votes, {idea['reply_count']:3} replies] {idea['title'][:50]}...")
                print(f"      Status: {idea['status_name'] or 'Unknown'}")
                if idea.get("replies"):
                    print(f"      First reply by: {idea['replies'][0]['author']}")
            
            # Status distribution
            print()
            print("Status distribution:")
            statuses = {}
            for idea in ideas:
                status = idea["status_name"] or "Unknown"
                statuses[status] = statuses.get(status, 0) + 1
            
            for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
                print(f"  {status}: {count}")
    
    return ideas


if __name__ == "__main__":
    main()
