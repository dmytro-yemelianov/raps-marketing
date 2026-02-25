# Portfolio Project: RAPS CLI

## Project Title
**RAPS - Production-Grade CLI for Autodesk Platform Services**

---

## Project Overview

### One-Liner
A comprehensive command-line interface for Autodesk Platform Services (APS), written in Rust with support for all major APS API domains.

### Description (For Portfolio)

```
RAPS (Rust Autodesk Platform Services) is a production-grade CLI tool I created to streamline automation of Autodesk Platform Services workflows. It's the most comprehensive open-source CLI for APS, featuring:

🔐 Authentication
• 2-legged OAuth for server-to-server operations
• 3-legged OAuth with browser-based login
• Device-code authentication for headless environments
• Secure token storage with automatic refresh

📦 Object Storage Service (OSS)
• Full bucket management across US & EMEA regions
• Resumable multipart uploads for large files (auto-chunking > 5MB)
• Batch uploads with parallel processing
• Signed S3 URLs for direct downloads

🔄 Model Derivative
• CAD translation to SVF2, OBJ, STL, STEP, and more
• Translation status monitoring with polling
• Manifest viewing and derivative downloads
• Reusable translation presets

📂 Data Management
• Browse hubs, projects, folders, and items
• Create folders and manage item versions
• Bind OSS objects to ACC folders

🪝 Webhooks
• Create and manage event subscriptions
• Support for all data management and model derivative events
• Endpoint testing with sample payloads

⚙️ Design Automation
• Manage engines (AutoCAD, Revit, Inventor, 3ds Max)
• Create and configure activities
• Submit and monitor work items

🏗️ Construction Cloud (ACC)
• Issues management with comments and attachments
• RFIs (Requests for Information)
• Assets, Submittals, and Checklists
• State transitions and workflow automation

📸 Reality Capture
• Photoscene creation for photogrammetry
• Photo upload and processing
• Result downloads (OBJ, FBX, RCS)

🤖 MCP Server (AI Integration)
• 14 MCP tools for AI assistant integration
• Natural language APS operations via Claude, Cursor, etc.
• Direct access to all major API functions
```

---

## Technical Details

### Technologies Used
- **Primary Language**: Rust 1.88+
- **Dependencies**: tokio (async runtime), reqwest (HTTP), serde (JSON)
- **Authentication**: OAuth 2.0 (all grant types)
- **Distribution**: crates.io, npm, pip, Homebrew, Scoop
- **CI/CD**: GitHub Actions
- **Documentation**: MkDocs

### Key Features
- Zero runtime dependencies (single binary)
- Cross-platform: Windows, macOS, Linux (x64 & ARM64)
- Multiple output formats: JSON, YAML, CSV, table, plain
- Shell completions: bash, zsh, fish, PowerShell, elvish
- Profile management for multiple environments
- Plugin system for extensibility
- Standardized exit codes for scripting

### Metrics
- 100% API coverage for core APS endpoints
- Validated against official Autodesk OpenAPI specs
- Active open-source community
- Regular releases with semantic versioning

---

## Challenges & Solutions

### Challenge 1: OAuth Token Management
**Problem**: Managing OAuth tokens across different authentication flows (2-leg, 3-leg, device code) with secure storage and automatic refresh.

**Solution**: Implemented a unified token manager with:
- Platform-specific secure storage
- Automatic refresh before expiry
- Grace period handling
- Multi-profile support

### Challenge 2: Large File Uploads
**Problem**: OSS API has limitations on single-request uploads for large files.

**Solution**: Built automatic chunking for files > 5MB with:
- Resumable multipart uploads
- Progress tracking with ETA
- Automatic retry on failure
- Parallel chunk processing

### Challenge 3: Cross-Platform Distribution
**Problem**: Making a Rust CLI accessible to developers who don't use cargo.

**Solution**: Multi-channel distribution:
- npm package with platform-specific binaries
- PyPI package for Python users
- Homebrew tap for macOS
- Scoop bucket for Windows
- Direct binary downloads

---

## Screenshots/Images

*Include screenshots of:*
1. CLI in action (bucket list, translation status)
2. MCP server working with Claude
3. Terminal output showing various commands
4. GitHub repository overview

---

## Links

- **Documentation**: https://rapscli.xyz
- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **crates.io**: https://crates.io/crates/raps
- **npm**: https://www.npmjs.com/package/@dmytro-yemelianov/raps-cli

---

## Client Relevance

This project demonstrates:
- ✅ Deep expertise in all Autodesk Platform Services APIs
- ✅ Production-quality Rust development
- ✅ Comprehensive documentation and user experience focus
- ✅ Enterprise-ready architecture with security considerations
- ✅ Open-source project management and community engagement
