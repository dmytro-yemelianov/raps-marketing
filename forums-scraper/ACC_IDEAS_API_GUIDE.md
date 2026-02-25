# Autodesk Forums Khoros API - Complete Guide

## Discovery Summary

The Autodesk Community Forums run on **Khoros (formerly Lithium) Community Platform**.
This platform exposes a public REST API v2 that uses **LiQL (Lithium Query Language)**.

**No authentication required** for public data!

## API Endpoint

```
https://forums.autodesk.com/api/2.0/search?q={LiQL_QUERY}
```

## Board IDs for Ideas Forums

| Forum | Board ID |
|-------|----------|
| ACC Ideas | `acc-ideas-en` |
| Revit Ideas | `revit-ideas` |
| AutoCAD Ideas | `autocad-ideas` |
| Inventor Ideas | `inventor-ideas` |
| Fusion 360 Ideas | `fusion-360-ideas-idb` |
| Civil 3D Ideas | `civil-3d-ideas` |
| Vault Ideas | `vault-ideas` |
| APS/Forge Ideas | `aps-ideas-idb` |

## Quick Start Examples

### 1. Get Total Count of Ideas

```bash
curl "https://forums.autodesk.com/api/2.0/search?q=SELECT%20count(*)%20FROM%20messages%20WHERE%20board.id%20=%20'acc-ideas-en'%20AND%20depth%20=%200"
```

Response:
```json
{"status":"success","data":{"count":4295}}
```

### 2. Get Top 10 Most Voted Ideas

```bash
curl "https://forums.autodesk.com/api/2.0/search?q=SELECT%20id,%20subject,%20view_href,%20kudos.sum(weight),%20metrics.views,%20status.key%20FROM%20messages%20WHERE%20board.id%20=%20'acc-ideas-en'%20AND%20depth%20=%200%20ORDER%20BY%20kudos.sum(weight)%20DESC%20LIMIT%2010"
```

### 3. Get Recent Ideas (Last 30 Days)

```bash
# Replace DATE with ISO format date
curl "https://forums.autodesk.com/api/2.0/search?q=SELECT%20*%20FROM%20messages%20WHERE%20board.id%20=%20'acc-ideas-en'%20AND%20depth%20=%200%20AND%20post_time%20%3E%20'2025-12-15'%20LIMIT%20100"
```

### 4. Filter by Status

```bash
# Status values: accepted, delivered, needs_info, already_offered, archived, implemented
curl "https://forums.autodesk.com/api/2.0/search?q=SELECT%20*%20FROM%20messages%20WHERE%20board.id%20=%20'acc-ideas-en'%20AND%20depth%20=%200%20AND%20status.key%20=%20'delivered'%20LIMIT%2050"
```

## Available Fields

### Message Fields
| Field | Description |
|-------|-------------|
| `id` | Unique message ID |
| `subject` | Title of the idea |
| `body` | Full HTML content |
| `view_href` | URL to the idea page |
| `post_time` | ISO 8601 timestamp |
| `author.login` | Username |
| `author.id` | User ID |
| `kudos.sum(weight)` | Vote count |
| `metrics.views` | View count |
| `conversation.messages_count` | Total messages including replies |
| `status.key` | Status code (e.g., "accepted", "delivered") |
| `status.name` | Status display name |
| `labels` | Category labels |
| `depth` | 0 = top-level post, 1+ = replies |

### Status Values
| Key | Name | Description |
|-----|------|-------------|
| `accepted` | Gathering Support | New idea collecting votes |
| `delivered` | Delivered | Implemented |
| `needs_info` | Needs More Info | Autodesk needs clarification |
| `already_offered` | Already Offered | Functionality exists |
| `archived` | Archived | Closed/deprecated |
| `implemented` | Implemented | Same as delivered |

## Pagination with Cursors

The API returns a `next_cursor` in the response for pagination:

```python
import requests
from urllib.parse import quote

def fetch_all_ideas():
    cursor = None
    while True:
        query = f"SELECT * FROM messages WHERE board.id = 'acc-ideas-en' AND depth = 0 LIMIT 100"
        if cursor:
            query += f" CURSOR '{cursor}'"
        
        url = f"https://forums.autodesk.com/api/2.0/search?q={quote(query)}"
        data = requests.get(url).json()
        
        for item in data['data']['items']:
            yield item
        
        cursor = data['data'].get('next_cursor')
        if not cursor:
            break
```

## Fetching Replies for an Idea

Use `parent.id` to get direct replies to an idea:

```bash
# Get first 10 replies for idea ID 12714729
curl "https://forums.autodesk.com/api/2.0/search?q=SELECT%20id,%20body,%20author.login,%20kudos.sum(weight)%20FROM%20messages%20WHERE%20parent.id%20=%20'12714729'%20LIMIT%2010"
```

## Filtering by Reply Count

**Note:** LiQL doesn't support filtering by `conversation.messages_count` in WHERE clauses.
Fetch ideas with messages_count included, then filter client-side:

```python
# Fetch top ideas and filter by reply count client-side
result = liql("SELECT id, subject, kudos.sum(weight), conversation.messages_count FROM messages WHERE board.id = 'acc-ideas-en' AND depth = 0 ORDER BY kudos.sum(weight) DESC LIMIT 500")

# Filter for ideas with 10+ replies
ideas_with_replies = [
    item for item in result['data']['items']
    if item.get('conversation', {}).get('messages_count', 1) >= 11  # 11 = 10 replies + 1 original
]
```

## Rate Limits

- No official rate limit documented
- Recommended: 1 request per second
- Max LIMIT: 100 items per request

## Python Quick Script

```python
import requests
from urllib.parse import quote
import json

def get_top_ideas(board_id: str, limit: int = 100) -> list:
    """Get top-voted ideas from any Autodesk Ideas forum."""
    query = f"""
        SELECT id, subject, body, view_href, kudos.sum(weight), metrics.views, 
               conversation.messages_count, status.name, author.login
        FROM messages 
        WHERE board.id = '{board_id}' AND depth = 0 
        ORDER BY kudos.sum(weight) DESC 
        LIMIT {limit}
    """
    url = f"https://forums.autodesk.com/api/2.0/search?q={quote(query)}"
    response = requests.get(url)
    return response.json()['data']['items']

def get_replies(idea_id: str, limit: int = 10) -> list:
    """Get replies for a specific idea using parent.id."""
    query = f"""
        SELECT id, body, post_time, author.login, kudos.sum(weight)
        FROM messages 
        WHERE parent.id = '{idea_id}'
        LIMIT {limit}
    """
    url = f"https://forums.autodesk.com/api/2.0/search?q={quote(query)}"
    response = requests.get(url)
    return response.json()['data']['items']

def get_ideas_with_replies(min_replies: int, limit: int = 500) -> list:
    """Get ideas filtered by reply count (client-side filtering)."""
    query = f"""
        SELECT id, subject, kudos.sum(weight), conversation.messages_count
        FROM messages 
        WHERE board.id = 'acc-ideas-en' AND depth = 0 
        ORDER BY kudos.sum(weight) DESC
        LIMIT {limit}
    """
    url = f"https://forums.autodesk.com/api/2.0/search?q={quote(query)}"
    response = requests.get(url)
    items = response.json()['data']['items']
    
    # Filter client-side (LiQL doesn't support messages_count in WHERE)
    return [
        item for item in items
        if item.get('conversation', {}).get('messages_count', 1) >= min_replies + 1
    ]

# Usage examples
ideas = get_top_ideas('acc-ideas-en', limit=50)
for idea in ideas[:5]:
    votes = idea.get('kudos', {}).get('sum', {}).get('weight', 0)
    replies = idea.get('conversation', {}).get('messages_count', 1) - 1
    print(f"[{votes} votes, {replies} replies] {idea['subject']}")

# Get replies for top idea
top_idea = ideas[0]
replies = get_replies(top_idea['id'], limit=5)
print(f"\nReplies for '{top_idea['subject'][:40]}...':")
for reply in replies:
    author = reply.get('author', {}).get('login')
    print(f"  - {author}: {reply.get('body', '')[:80]}...")

# Get ideas with 10+ replies
popular = get_ideas_with_replies(min_replies=10, limit=200)
print(f"\nIdeas with 10+ replies: {len(popular)}")
```

## Node.js Example

```javascript
const fetch = require('node-fetch');

async function getTopIdeas(boardId, limit = 100) {
    const query = `SELECT id, subject, view_href, kudos.sum(weight), metrics.views 
                   FROM messages 
                   WHERE board.id = '${boardId}' AND depth = 0 
                   ORDER BY kudos.sum(weight) DESC 
                   LIMIT ${limit}`;
    
    const url = `https://forums.autodesk.com/api/2.0/search?q=${encodeURIComponent(query)}`;
    const response = await fetch(url);
    const data = await response.json();
    return data.data.items;
}

// Usage
getTopIdeas('acc-ideas-en', 50).then(ideas => {
    ideas.forEach(idea => {
        const votes = idea.kudos?.sum?.weight || 0;
        console.log(`[${votes} votes] ${idea.subject}`);
    });
});
```

## cURL One-Liner for All Data

```bash
# Save top 100 most-voted ACC ideas to JSON
curl -s "https://forums.autodesk.com/api/2.0/search?q=$(python3 -c "from urllib.parse import quote; print(quote(\"SELECT id, subject, view_href, body, post_time, kudos.sum(weight), metrics.views, status.name FROM messages WHERE board.id = 'acc-ideas-en' AND depth = 0 ORDER BY kudos.sum(weight) DESC LIMIT 100\"))")" | python3 -c "import sys, json; print(json.dumps(json.loads(sys.stdin.read())['data']['items'], indent=2))" > acc_top100.json
```

## Alternative Methods (Less Reliable)

### 1. RSS Feed
```
https://forums.autodesk.com/t5/acc-ideas/tkb-p/acc-ideas-en/rss-board
```
Limited to recent items only, no vote counts.

### 2. Web Scraping
Use Playwright/Selenium, but:
- Slower (requires rendering)
- More fragile (HTML changes)
- May trigger bot detection
- Limited pagination support

### 3. Autodesk Internal API
Some forums have internal APIs for voting, but these require authentication
and are not publicly documented.

## Why This Method is Most Reliable

1. **Official API** - Part of Khoros platform, not reverse-engineered
2. **No Auth Required** - Public data, no login needed
3. **Full Data Access** - All fields including votes, views, body content
4. **Pagination** - Cursor-based, can fetch all 4000+ ideas
5. **Stable** - LiQL syntax is documented by Khoros
6. **Fast** - Direct JSON responses, no HTML parsing
7. **No Bot Detection** - API endpoint expects programmatic access

## Khoros LiQL Documentation

For advanced queries, see Khoros documentation:
- https://developer.khoros.com/khoroscommunitydevdocs/docs/liql-overview

Note: Autodesk's implementation may have slight variations.
