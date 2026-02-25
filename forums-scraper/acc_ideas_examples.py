#!/usr/bin/env python3
"""
Quick examples - ACC Ideas API queries
Run these to test specific features.
"""

import requests
from urllib.parse import quote
import json

API_URL = "https://forums.autodesk.com/api/2.0/search"
BOARD_ID = "acc-ideas-en"

def liql(query: str) -> dict:
    """Execute LiQL query."""
    url = f"{API_URL}?q={quote(query)}"
    return requests.get(url, timeout=30).json()

def pp(data):
    """Pretty print JSON."""
    print(json.dumps(data, indent=2))

# ============================================================
# EXAMPLE 1: Top 5 most voted ideas with full body content
# ============================================================
print("=" * 60)
print("TOP 5 MOST VOTED IDEAS (with body content)")
print("=" * 60)

result = liql(f"""
    SELECT id, subject, body, view_href, kudos.sum(weight), metrics.views, 
           conversation.messages_count, status.name, author.login
    FROM messages 
    WHERE board.id = '{BOARD_ID}' AND depth = 0 
    ORDER BY kudos.sum(weight) DESC 
    LIMIT 5
""")

for i, idea in enumerate(result['data']['items'], 1):
    kudos = idea.get('kudos', {}).get('sum', {}).get('weight', 0)
    views = idea.get('metrics', {}).get('views', 0)
    replies = idea.get('conversation', {}).get('messages_count', 1) - 1
    status = idea.get('status', {}).get('name', 'Unknown')
    author = idea.get('author', {}).get('login', 'Unknown')
    
    print(f"\n{i}. {idea['subject']}")
    print(f"   Kudos: {kudos} | Views: {views} | Replies: {replies}")
    print(f"   Status: {status} | Author: {author}")
    print(f"   URL: {idea['view_href']}")
    
    # Show first 200 chars of body (strip HTML for readability)
    import re, html
    body = html.unescape(re.sub(r'<[^>]+>', '', idea.get('body', '')))[:200]
    print(f"   Body: {body}...")


# ============================================================
# EXAMPLE 2: Get replies for a specific idea
# ============================================================
print("\n" + "=" * 60)
print("REPLIES FOR TOP IDEA")
print("=" * 60)

top_idea_id = result['data']['items'][0]['id']
print(f"Fetching replies for idea #{top_idea_id}...")

# Use parent.id to get direct replies
replies_result = liql(f"""
    SELECT id, body, post_time, author.login, kudos.sum(weight)
    FROM messages 
    WHERE parent.id = '{top_idea_id}'
    LIMIT 5
""")

for reply in replies_result['data']['items']:
    author = reply.get('author', {}).get('login', 'Unknown')
    kudos = reply.get('kudos', {}).get('sum', {}).get('weight', 0)
    body = html.unescape(re.sub(r'<[^>]+>', '', reply.get('body', '')))[:150]
    print(f"\n  [{author}] (+{kudos} kudos)")
    print(f"  {body}...")


# ============================================================
# EXAMPLE 3: Get ideas sorted by reply count
# Note: LiQL doesn't support filtering by messages_count,
# so we fetch all and filter client-side
# ============================================================
print("\n" + "=" * 60)
print("IDEAS WITH MOST REPLIES (top 10)")
print("=" * 60)

# Fetch more ideas and sort by reply count client-side
result = liql(f"""
    SELECT id, subject, kudos.sum(weight), conversation.messages_count, status.name
    FROM messages 
    WHERE board.id = '{BOARD_ID}' AND depth = 0
    ORDER BY kudos.sum(weight) DESC 
    LIMIT 200
""")

# Sort by reply count
items = result['data']['items']
items_sorted = sorted(items, key=lambda x: x.get('conversation', {}).get('messages_count', 1), reverse=True)

print(f"From top 200 by votes, sorted by replies:\n")
for i, idea in enumerate(items_sorted[:10], 1):
    kudos = idea.get('kudos', {}).get('sum', {}).get('weight', 0)
    replies = idea.get('conversation', {}).get('messages_count', 1) - 1
    status = idea.get('status', {}).get('name', 'Unknown')
    print(f"  {i:2}. [{kudos:4} kudos, {replies:3} replies] {idea['subject'][:50]}...")


# ============================================================
# EXAMPLE 4: Status distribution  
# ============================================================
print("\n" + "=" * 60)
print("STATUS DISTRIBUTION (from top 500)")
print("=" * 60)

result = liql(f"""
    SELECT id, status.name
    FROM messages 
    WHERE board.id = '{BOARD_ID}' AND depth = 0 
    ORDER BY kudos.sum(weight) DESC
    LIMIT 500
""")

statuses = {}
for item in result['data']['items']:
    status = item.get('status', {}).get('name', 'Unknown')
    statuses[status] = statuses.get(status, 0) + 1

for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
    print(f"  {status}: {count}")


# ============================================================
# EXAMPLE 5: Ideas with specific status
# ============================================================
print("\n" + "=" * 60)
print("TOP DELIVERED IDEAS (implemented)")
print("=" * 60)

result = liql(f"""
    SELECT id, subject, kudos.sum(weight), conversation.messages_count
    FROM messages 
    WHERE board.id = '{BOARD_ID}' AND depth = 0 
          AND status.key = 'delivered'
    ORDER BY kudos.sum(weight) DESC 
    LIMIT 5
""")

for i, idea in enumerate(result['data']['items'], 1):
    kudos = idea.get('kudos', {}).get('sum', {}).get('weight', 0)
    replies = idea.get('conversation', {}).get('messages_count', 1) - 1
    print(f"  {i}. [{kudos} kudos] {idea['subject'][:55]}...")


print("\n" + "=" * 60)
print("✅ All examples completed!")
print("=" * 60)
