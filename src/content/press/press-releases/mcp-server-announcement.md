---
title: "RAPS CLI Launches MCP Server with 101 Tools for AI-Powered APS Automation"
description: "Open-source RAPS CLI adds Model Context Protocol server, enabling AI assistants to interact with Autodesk Platform Services"
type: "release"
publishDate: 2026-06-10
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS CLI Launches MCP Server with 101 Tools for AI-Powered APS Automation

*Open-source CLI tool adds Model Context Protocol support, enabling AI assistants to perform Autodesk Platform Services operations*

---

**Version Information**
- **RAPS Version**: 4.14.0
- **APS API Coverage**: Data Management v1, Model Derivative v2, OSS v2, Authentication v2, Construction Cloud v1, Design Automation v3
- **MCP Tools**: 101 tools across all APS services
- **License**: Apache-2.0 (open source)

---

RAPS, the open-source Rust-based CLI for Autodesk Platform Services, has added a Model Context Protocol (MCP) server with 101 tools, allowing AI assistants like Claude to interact with APS APIs through natural language.

### What the MCP Server Does

The MCP server exposes RAPS CLI capabilities as structured tools that AI assistants can call. This means developers can describe APS operations in plain language and have an AI assistant execute the corresponding API calls.

**Example interactions:**
- "List all buckets in my account" - calls bucket listing tools
- "Upload model.rvt to my-bucket" - executes object upload
- "Start an SVF2 translation for this URN" - initiates Model Derivative job
- "Show my current auth status" - checks token validity

### 101 Tools Across APS Services

The MCP server provides tools for:

- **Authentication**: Login, status, token inspection
- **Object Storage**: Bucket and object CRUD operations, batch uploads
- **Data Management**: Hub, project, folder, and item navigation
- **Model Derivative**: Translation, status, metadata, property extraction
- **Design Automation**: Engine listing, app bundle and activity management, work item execution
- **Webhooks**: Create, list, delete, test webhook subscriptions
- **Construction Cloud**: Asset, submittal, and checklist management
- **Account Admin**: User and project administration
- **Configuration**: Profile and context management
- **Pipelines**: YAML pipeline validation and execution

### Technical Details

- Built with `rmcp` 0.12 (Rust MCP SDK)
- Runs as a stdio-based MCP server (`raps mcp`)
- Compatible with any MCP-compliant AI client
- Inherits RAPS CLI's built-in retry logic, rate limiting, and error handling
- Uses the same authentication and configuration as the CLI

### Getting Started

```bash
# Install RAPS
cargo install raps-cli

# Configure credentials
raps config profile create default
raps config set client_id YOUR_CLIENT_ID
raps config set client_secret YOUR_SECRET

# Start the MCP server
raps mcp
```

Configure your AI assistant to connect to the MCP server via stdio transport.

### About RAPS

RAPS is an open-source CLI tool for Autodesk Platform Services, written in Rust. It provides 60+ commands covering authentication, data management, object storage, model translation, design automation, webhooks, and more. RAPS is developed by Dmytro Yemelianov and released under the Apache-2.0 license.

- **Website**: [rapscli.xyz](https://rapscli.xyz)
- **Source Code**: [github.com/dmytro-yemelianov/raps](https://github.com/dmytro-yemelianov/raps)
- **Author**: Dmytro Yemelianov (dmytroyemelianov@icloud.com)

---

*RAPS is an independent open-source project. Autodesk, APS, and related marks are trademarks of Autodesk, Inc. Model Context Protocol is developed by Anthropic.*
