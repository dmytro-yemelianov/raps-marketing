#!/usr/bin/env python3
"""
Autodesk Forums API Toolkit v3

Uses the Khoros/Lithium REST API v2 with LiQL (Lithium Query Language)
for efficient, structured data extraction - NO HTML SCRAPING REQUIRED!

API Endpoint: https://forums.autodesk.com/api/2.0/search?q={LiQL_QUERY}

Part of raps-research: https://github.com/dmytro-yemelianov/raps-research

Usage:
    # Discover all forums
    python autodesk_forum_api.py discover
    
    # Export all ideas from a board
    python autodesk_forum_api.py export --board acc-ideas-en --output data/acc_ideas.csv
    
    # Export discussion board
    python autodesk_forum_api.py export --board revit-api-forum-en --output data/revit_api.csv
    
    # Get board statistics
    python autodesk_forum_api.py stats --board acc-ideas-en

Requirements:
    pip install requests pandas tqdm
"""

import argparse
import json
import time
import csv
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any, Iterator
from urllib.parse import quote
import requests
import pandas as pd
from tqdm import tqdm


BASE_URL = "https://forums.autodesk.com"
API_URL = f"{BASE_URL}/api/2.0"


# =============================================================================
# LiQL Query Builder
# =============================================================================

class LiQLQuery:
    """Build LiQL (Lithium Query Language) queries."""
    
    @staticmethod
    def url_encode(query: str) -> str:
        """URL encode a LiQL query."""
        return quote(query, safe='')
    
    @staticmethod
    def search_url(query: str) -> str:
        """Build full search URL."""
        return f"{API_URL}/search?q={LiQLQuery.url_encode(query)}"
    
    # Predefined queries
    @staticmethod
    def all_categories() -> str:
        return "SELECT id,title,node_type FROM nodes WHERE node_type = 'category' LIMIT 500"
    
    @staticmethod
    def all_boards() -> str:
        return "SELECT id,title,conversation_style,parent.id FROM nodes WHERE node_type = 'board' LIMIT 500"
    
    @staticmethod
    def ideas_boards() -> str:
        return "SELECT id,title,conversation_style,parent.id FROM nodes WHERE conversation_style = 'idea' LIMIT 200"
    
    @staticmethod
    def forum_boards() -> str:
        return "SELECT id,title,conversation_style,parent.id FROM nodes WHERE conversation_style = 'forum' LIMIT 200"
    
    @staticmethod
    def messages_by_board(board_id: str, limit: int = 100, cursor: str = None) -> str:
        """Get messages from a board. depth=0 means only topic starters (not replies)."""
        query = f"SELECT id,subject,view_href,kudos.sum(weight),metrics.views,post_time,author.login,conversation.messages_count FROM messages WHERE board.id = '{board_id}' AND depth = 0 ORDER BY kudos.sum(weight) DESC LIMIT {limit}"
        if cursor:
            query += f" CURSOR '{cursor}'"
        return query
    
    @staticmethod
    def message_count(board_id: str) -> str:
        return f"SELECT count(*) FROM messages WHERE board.id = '{board_id}' AND depth = 0"


# =============================================================================
# API Client
# =============================================================================

class AutodeskForumAPI:
    """Client for Autodesk Community Forum API."""
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'RAPS-Research/3.0 (+https://rapscli.xyz)',
            'Accept': 'application/json',
        })
    
    def query(self, liql: str) -> Dict[str, Any]:
        """Execute a LiQL query."""
        url = LiQLQuery.search_url(liql)
        time.sleep(self.delay)
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data.get('status') == 'error':
                print(f"API Error: {data.get('message')}")
                return {'data': {'items': []}}
            
            return data
        except Exception as e:
            print(f"Request failed: {e}")
            return {'data': {'items': []}}
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """Get full details of a single message."""
        url = f"{API_URL}/messages/{message_id}"
        time.sleep(self.delay)
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json().get('data', {})
        except Exception as e:
            print(f"Failed to get message {message_id}: {e}")
            return {}
    
    # High-level methods
    def discover_boards(self) -> Dict[str, List[Dict]]:
        """Discover all forum boards organized by type."""
        result = {
            'categories': [],
            'ideas_boards': [],
            'discussion_boards': [],
        }
        
        # Categories
        data = self.query(LiQLQuery.all_categories())
        result['categories'] = data.get('data', {}).get('items', [])
        
        # Ideas boards
        data = self.query(LiQLQuery.ideas_boards())
        result['ideas_boards'] = data.get('data', {}).get('items', [])
        
        # Forum/discussion boards
        data = self.query(LiQLQuery.forum_boards())
        result['discussion_boards'] = data.get('data', {}).get('items', [])
        
        return result
    
    def get_board_messages(self, board_id: str, max_messages: int = 10000) -> Iterator[Dict]:
        """
        Get all messages from a board with pagination.
        Uses cursor-based pagination for efficiency.
        """
        cursor = None
        total_fetched = 0
        batch_size = 100  # Max per request
        
        while total_fetched < max_messages:
            query = LiQLQuery.messages_by_board(board_id, batch_size, cursor)
            data = self.query(query)
            
            items = data.get('data', {}).get('items', [])
            if not items:
                break
            
            for item in items:
                yield item
                total_fetched += 1
                if total_fetched >= max_messages:
                    break
            
            # Get next cursor
            cursor = data.get('data', {}).get('next_cursor')
            if not cursor:
                break
    
    def enrich_message(self, message: Dict) -> Dict:
        """Fetch full message details including status."""
        message_id = message.get('id')
        if not message_id:
            return message
        
        full_data = self.get_message(message_id)
        if full_data:
            # Extract status
            status = full_data.get('status', {})
            message['status_name'] = status.get('name', '')
            message['status_key'] = status.get('key', '')
            
            # Body text (strip HTML for analysis)
            body_html = full_data.get('body', '')
            # Simple HTML strip - for proper handling use BeautifulSoup
            import re
            message['body_text'] = re.sub(r'<[^>]+>', ' ', body_html).strip()
            
            # Additional fields
            message['replies_count'] = full_data.get('conversation', {}).get('messages_count', 0)
            message['solved'] = full_data.get('conversation', {}).get('solved', False)
        
        return message


# =============================================================================
# Data Export
# =============================================================================

@dataclass
class ForumMessage:
    """Structured forum message data."""
    id: str
    subject: str
    url: str
    kudos: int = 0
    views: int = 0
    replies: int = 0
    status: str = ""
    post_date: str = ""
    author: str = ""
    body_text: str = ""
    solved: bool = False
    board_id: str = ""
    scraped_at: str = ""
    
    def __post_init__(self):
        if not self.scraped_at:
            self.scraped_at = datetime.now().isoformat()


def export_board(api: AutodeskForumAPI, board_id: str, output_path: str, 
                 enrich: bool = False, max_messages: int = 10000):
    """Export all messages from a board to CSV."""
    
    print(f"Exporting board: {board_id}")
    messages = []
    
    for msg in tqdm(api.get_board_messages(board_id, max_messages), 
                    desc="Fetching messages"):
        
        if enrich:
            msg = api.enrich_message(msg)
        
        # Transform to standard format
        record = ForumMessage(
            id=msg.get('id', ''),
            subject=msg.get('subject', ''),
            url=msg.get('view_href', ''),
            kudos=msg.get('kudos', {}).get('sum', {}).get('weight', 0) if isinstance(msg.get('kudos'), dict) else 0,
            views=msg.get('metrics', {}).get('views', 0) if isinstance(msg.get('metrics'), dict) else 0,
            replies=msg.get('conversation', {}).get('messages_count', 0) if isinstance(msg.get('conversation'), dict) else msg.get('replies_count', 0),
            status=msg.get('status_name', ''),
            post_date=msg.get('post_time', ''),
            author=msg.get('author', {}).get('login', '') if isinstance(msg.get('author'), dict) else '',
            body_text=msg.get('body_text', ''),
            solved=msg.get('solved', False),
            board_id=board_id,
        )
        messages.append(asdict(record))
    
    # Save to CSV
    if messages:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        df = pd.DataFrame(messages)
        df.to_csv(output, index=False)
        print(f"Exported {len(messages)} messages to {output}")
    else:
        print("No messages found")
    
    return messages


# =============================================================================
# CLI Commands
# =============================================================================

def cmd_discover(args):
    """Discover all available forums."""
    api = AutodeskForumAPI()
    boards = api.discover_boards()
    
    print("\n" + "="*70)
    print("AUTODESK FORUM DISCOVERY (via API)")
    print("="*70)
    
    print(f"\n📁 CATEGORIES ({len(boards['categories'])})")
    for cat in sorted(boards['categories'], key=lambda x: x.get('title', '')):
        cat_id = cat.get('id', '').replace('category:', '')
        print(f"  {cat_id:40} {cat.get('title', '')}")
    
    print(f"\n💡 IDEAS BOARDS ({len(boards['ideas_boards'])})")
    for board in sorted(boards['ideas_boards'], key=lambda x: x.get('title', '')):
        board_id = board.get('id', '').replace('board:', '')
        parent = board.get('parent', {}).get('id', '').replace('category:', '')
        if 'Read Only' not in board.get('title', ''):
            print(f"  {board_id:40} {board.get('title', '')[:40]}")
    
    print(f"\n💬 DISCUSSION BOARDS ({len(boards['discussion_boards'])})")
    for board in sorted(boards['discussion_boards'], key=lambda x: x.get('title', '')):
        board_id = board.get('id', '').replace('board:', '')
        if 'Read Only' not in board.get('title', ''):
            print(f"  {board_id:40} {board.get('title', '')[:40]}")
    
    # Save full data
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(boards, f, indent=2)
        print(f"\nFull data saved to {args.output}")


def cmd_export(args):
    """Export messages from a board."""
    api = AutodeskForumAPI()
    export_board(
        api, 
        args.board, 
        args.output, 
        enrich=args.enrich,
        max_messages=args.max
    )


def cmd_stats(args):
    """Get board statistics."""
    api = AutodeskForumAPI()
    
    print(f"\nFetching stats for: {args.board}")
    
    # Get sample messages
    messages = list(api.get_board_messages(args.board, max_messages=100))
    
    if not messages:
        print("No messages found")
        return
    
    # Enrich first 20 to get status distribution
    print("Enriching sample messages for status analysis...")
    statuses = []
    for msg in tqdm(messages[:20]):
        enriched = api.enrich_message(msg)
        if enriched.get('status_name'):
            statuses.append(enriched['status_name'])
    
    # Calculate stats
    total_kudos = sum(
        m.get('kudos', {}).get('sum', {}).get('weight', 0) 
        if isinstance(m.get('kudos'), dict) else 0
        for m in messages
    )
    total_views = sum(
        m.get('metrics', {}).get('views', 0)
        if isinstance(m.get('metrics'), dict) else 0
        for m in messages
    )
    
    print(f"\n📊 BOARD STATISTICS: {args.board}")
    print(f"  Sample size: {len(messages)} messages")
    print(f"  Total kudos (sample): {total_kudos:,}")
    print(f"  Total views (sample): {total_views:,}")
    
    if statuses:
        from collections import Counter
        status_counts = Counter(statuses)
        print(f"\n  Status distribution (sample of {len(statuses)}):")
        for status, count in status_counts.most_common():
            pct = count / len(statuses) * 100
            print(f"    {status:30} {count:4} ({pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser(
        description='Autodesk Forums API Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover all forums
  python autodesk_forum_api.py discover --output forums.json
  
  # Export ACC Ideas (fast, no enrichment)
  python autodesk_forum_api.py export --board acc-ideas-en --output data/acc_ideas.csv
  
  # Export with full details (slower, includes status)
  python autodesk_forum_api.py export --board acc-ideas-en --output data/acc_ideas_full.csv --enrich
  
  # Get board statistics
  python autodesk_forum_api.py stats --board revit-ideas-en

Key Board IDs:
  Ideas Boards:
    acc-ideas-en          ACC Ideas
    revit-ideas-en        Revit Ideas  
    inventor-ideas-en     Inventor Ideas
    fusion-ideas-en       Fusion Ideas (check actual ID)
    civil-3d-ideas-en     Civil 3D Ideas
    
  Discussion Boards:
    revit-api-forum-en    Revit API Forum
    inventor-programming-forum-en  Inventor Programming
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # Discover
    discover_parser = subparsers.add_parser('discover', help='Discover all forums')
    discover_parser.add_argument('--output', '-o', help='Output JSON file')
    discover_parser.set_defaults(func=cmd_discover)
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export board messages')
    export_parser.add_argument('--board', '-b', required=True, help='Board ID')
    export_parser.add_argument('--output', '-o', required=True, help='Output CSV file')
    export_parser.add_argument('--enrich', action='store_true', help='Fetch full message details (slower)')
    export_parser.add_argument('--max', '-m', type=int, default=10000, help='Max messages')
    export_parser.set_defaults(func=cmd_export)
    
    # Stats
    stats_parser = subparsers.add_parser('stats', help='Get board statistics')
    stats_parser.add_argument('--board', '-b', required=True, help='Board ID')
    stats_parser.set_defaults(func=cmd_stats)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    args.func(args)


if __name__ == '__main__':
    main()
