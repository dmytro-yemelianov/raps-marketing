# Autodesk Forum API Discovery

**Major Finding:** Autodesk Community Forums expose a public REST API v2 using **LiQL (Lithium Query Language)** - no authentication required for read operations!

## API Endpoint

```
https://forums.autodesk.com/api/2.0/search?q={LiQL_QUERY}
```

## LiQL Query Examples

### Discover All Categories
```sql
SELECT id,title,node_type FROM nodes WHERE node_type = 'category' LIMIT 500
```

### Discover All Boards
```sql
SELECT id,title,conversation_style,parent.id FROM nodes WHERE node_type = 'board' LIMIT 500
```

### Get Ideas Boards Only
```sql
SELECT id,title,conversation_style,parent.id FROM nodes WHERE conversation_style = 'idea' LIMIT 200
```

### Get Discussion Boards Only
```sql
SELECT id,title,conversation_style,parent.id FROM nodes WHERE conversation_style = 'forum' LIMIT 200
```

### Get Messages from a Board (sorted by kudos)
```sql
SELECT id,subject,view_href,kudos.sum(weight),metrics.views,post_time,author.login 
FROM messages 
WHERE board.id = 'acc-ideas-en' AND depth = 0 
ORDER BY kudos.sum(weight) DESC 
LIMIT 100
```

### Get Single Message with Full Details
```
GET https://forums.autodesk.com/api/2.0/messages/{message_id}
```

Returns full data including:
- `status.name` - Idea status (e.g., "Gathering Support", "Future Consideration", "Implemented")
- `body` - Full HTML content
- `kudos.sum.weight` - Vote count
- `metrics.views` - View count
- `conversation.messages_count` - Reply count
- `conversation.solved` - Has accepted solution (for discussions)

## Key Board IDs Discovered

### Ideas Boards (conversation_style = 'idea')

| Board ID | Title | Parent Category |
|----------|-------|-----------------|
| `acc-ideas-en` | ACC Ideas | autodesk-construction-cloud-en |
| `revit-ideas-en` | Revit Ideas | revit-products-en |
| `inventor-ideas-en` | Inventor Ideas | inventor-en |
| `fusion-ideas-en` | Fusion Ideas | (check actual) |
| `civil-3d-ideas-en` | Civil 3D Ideas | civil-3d-en |
| `bim-360-ideas-en` | BIM 360 Ideas | bim-360-en |
| `vault-ideas-en` | Vault Ideas | vault-en |
| `3ds-max-ideas-en` | 3ds Max Ideas | 3ds-max-en |
| `maya-ideas-en` | Maya Ideas | maya-en |
| `autocad-electrical-ideas-en` | AutoCAD Electrical Ideas | autocad-electrical-en |
| `infraworks-ideas-en` | InfraWorks Ideas | infraworks-en |
| `recap-ideas-en` | ReCap Ideas | recap-en |

### Discussion Boards (conversation_style = 'forum')

Check API response for full list - includes:
- Product forums (Revit, AutoCAD, Inventor, etc.)
- API/Programming forums
- Support forums

## Sample API Response

### Messages Query Response
```json
{
  "status": "success",
  "http_code": 200,
  "data": {
    "type": "messages",
    "size": 10,
    "items": [
      {
        "type": "message",
        "id": "12714729",
        "view_href": "https://forums.autodesk.com/t5/acc-ideas/allow-adding-a-user-s-to-multiple-projects/idi-p/12714729",
        "author": {"type": "user", "login": "adbryson"},
        "subject": "Allow adding a user(s) to MULTIPLE PROJECTS",
        "post_time": "2024-04-17T06:49:50.140-07:00",
        "metrics": {"views": 7334},
        "kudos": {"sum": {"weight": 344}}
      }
    ],
    "next_cursor": "MjUuMTJ8Mi4wfG98MTB8NzI6MHwxMA"
  }
}
```

### Single Message Response (includes status!)
```json
{
  "status": "success",
  "data": {
    "id": "12714729",
    "subject": "Allow adding a user(s) to MULTIPLE PROJECTS",
    "body": "<P>There is a major need...</P>",
    "status": {
      "type": "message_status",
      "key": "delivered",
      "name": "Future Consideration",
      "completed": false
    },
    "metrics": {"views": 7334},
    "kudos": {"query": "SELECT * FROM kudos WHERE message.id = '12714729'"},
    "conversation": {
      "style": "idea",
      "messages_count": 59,
      "solved": false
    }
  }
}
```

## Pagination

Use cursor-based pagination:
```sql
SELECT ... FROM messages WHERE board.id = 'xxx' LIMIT 100 CURSOR 'next_cursor_value'
```

The `next_cursor` is returned in the response when more results exist.

## Rate Limiting

No explicit rate limit documented, but:
- Add 0.5-1 second delay between requests
- Use batch queries (LIMIT 100) to minimize calls
- Cache board/category discovery results

## Advantages Over HTML Scraping

1. **Structured Data** - Clean JSON, no HTML parsing needed
2. **Faster** - Get 100 messages per request vs crawling pages
3. **Reliable** - API won't break with UI changes
4. **Complete** - Access to fields not visible in UI (status key, metrics)
5. **Efficient** - Cursor pagination, no duplicate handling needed

## Usage with Toolkit

```bash
# Discover all forums
python autodesk_forum_api.py discover --output forums.json

# Export ACC Ideas (fast)
python autodesk_forum_api.py export --board acc-ideas-en --output acc_ideas.csv

# Export with full details including status (slower - 1 API call per message)
python autodesk_forum_api.py export --board acc-ideas-en --output acc_ideas_full.csv --enrich

# Get statistics
python autodesk_forum_api.py stats --board revit-ideas-en
```

## RAPS Research Applications

1. **Pain Point Analysis** - Export ideas boards, analyze by status
2. **Trend Detection** - Track kudos over time  
3. **Cross-Product Comparison** - Compare implementation rates across products
4. **Developer Sentiment** - Analyze API forum discussions
5. **Content Generation** - Find top unmet needs for blog content

---

*Discovered 2025-01-16 as part of raps-research project*
*API powered by Khoros/Lithium Community Platform*
