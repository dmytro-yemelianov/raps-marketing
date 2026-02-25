# Portfolio Project: MCP Server for APS

## Project Title
**MCP Server - AI-Powered Autodesk Platform Services Automation**

---

## Project Overview

### One-Liner
Model Context Protocol server enabling AI assistants (Claude, Cursor) to directly interact with Autodesk Platform Services through natural language.

### Description (For Portfolio)

```
Built an MCP (Model Context Protocol) server that bridges AI assistants with Autodesk Platform Services, enabling natural language control of APS operations.

🤖 THE PROBLEM
Developers spend hours writing code to interact with APS APIs. Even experienced engineers need to constantly reference documentation for authentication, URN encoding, and API quirks.

💡 THE SOLUTION
An MCP server that exposes APS functionality as tools that AI assistants can call directly. Instead of writing code, users simply describe what they want in natural language.

🔧 AVAILABLE TOOLS (14 MCP Tools)

Authentication:
• auth_test - Validate credentials
• auth_status - Check token status

Bucket Operations:
• bucket_list - List all OSS buckets
• bucket_create - Create new buckets
• bucket_get - Get bucket details
• bucket_delete - Remove buckets

Object Operations:
• object_list - List bucket contents
• object_delete - Remove objects
• object_signed_url - Generate download URLs
• object_urn - Get object URN for translation

Translation:
• translate_start - Initiate CAD translation
• translate_status - Check translation progress

Data Management:
• hub_list - List BIM 360/ACC hubs
• project_list - List projects in a hub

🎯 EXAMPLE INTERACTIONS

User: "List all my buckets"
Claude: *calls bucket_list* → Returns formatted bucket list

User: "Create a bucket called 'project-models' with persistent policy"
Claude: *calls bucket_create* → Creates bucket, confirms success

User: "Start translating the CAD file I just uploaded to SVF2"
Claude: *calls object_urn, then translate_start* → Initiates translation

User: "Is my translation done yet?"
Claude: *calls translate_status* → Reports progress/completion

🏗️ ARCHITECTURE

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI Assistant  │────▶│   MCP Server    │────▶│   APS APIs      │
│  (Claude, etc.) │     │   (RAPS serve)  │     │   (Autodesk)    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       ▲                        │
       │                        ▼
       │                 ┌─────────────────┐
       └─────────────────│ Human-readable  │
                         │    responses    │
                         └─────────────────┘

✨ KEY FEATURES
• Zero configuration - uses existing RAPS profile
• Automatic authentication handling
• Error messages formatted for AI understanding
• Streaming responses for long operations
• Works with any MCP-compatible AI assistant
```

---

## Technical Details

### Technologies Used
- **Protocol**: Model Context Protocol (MCP) v0.1.0
- **Language**: Rust
- **Transport**: stdio (for local), HTTP (for remote)
- **Authentication**: OAuth 2.0 via RAPS token store
- **Compatible Clients**: Claude Desktop, Cursor, any MCP client

### Architecture Decisions
1. **Stateless tools**: Each tool call is independent
2. **Human-readable responses**: Formatted for AI to relay to users
3. **Error wrapping**: API errors converted to helpful messages
4. **Lazy authentication**: Only authenticates when tools are called

### Integration Examples

**Claude Desktop Configuration:**
```json
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"],
      "env": {
        "APS_CLIENT_ID": "your_client_id",
        "APS_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

**Cursor Configuration:**
```json
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"]
    }
  }
}
```

---

## Challenges & Solutions

### Challenge 1: Tool Design for AI Understanding
**Problem**: AI assistants need tools with clear semantics - ambiguous responses cause hallucinations.

**Solution**: 
- Designed each tool with specific, single-purpose functionality
- Return structured data with clear field names
- Include context in responses (e.g., "Bucket 'x' created successfully in US region")
- Error messages include actionable suggestions

### Challenge 2: Authentication Flow in MCP Context
**Problem**: 3-legged OAuth requires browser interaction, but MCP runs headlessly.

**Solution**:
- Primary: Use 2-legged auth for most operations
- Fallback: Pre-authenticate via CLI, server uses stored tokens
- Device code: Alternative for user-context operations

### Challenge 3: Rate Limiting and Long Operations
**Problem**: Translations can take minutes; AI shouldn't wait in blocking call.

**Solution**:
- translate_start returns immediately with job ID
- translate_status can be polled by AI
- Responses include estimated time remaining
- AI can suggest user check back later

---

## Impact & Results

- **Productivity Gain**: 10x faster APS exploration and testing
- **Learning Curve**: New developers can interact with APS immediately
- **Documentation Access**: AI provides context from RAPS docs
- **Error Recovery**: AI suggests fixes for common mistakes

---

## Screenshots/Demos

*Include:*
1. Screenshot of Claude Desktop using MCP to list buckets
2. Cursor IDE with MCP integration active
3. Terminal showing MCP server startup
4. Example conversation transcript

---

## Links

- **Documentation**: https://rapscli.xyz/docs/mcp
- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **MCP Protocol**: https://modelcontextprotocol.io

---

## Client Relevance

This project demonstrates:
- ✅ Cutting-edge AI integration expertise
- ✅ Protocol design and implementation
- ✅ Developer experience optimization
- ✅ Understanding of modern AI tooling ecosystem
- ✅ Production-ready server implementation
