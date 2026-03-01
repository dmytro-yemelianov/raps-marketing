---
title: "RAPS 4.x: Open-Source CLI for Autodesk Platform Services Reaches 95+ Commands"
description: "Rust-based APS CLI tool covers authentication, data management, model translation, design automation, and more"
type: "release"
publishDate: 2026-03-15
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 4.x: Open-Source CLI for Autodesk Platform Services Reaches 95+ Commands

*Rust-based CLI tool provides comprehensive APS API coverage with 10 workspace crates and MCP server integration*

---

**Version Information**
- **Current Version**: 4.16.0
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates
- **License**: Apache-2.0 (open source)

---

RAPS (Rust-based APS CLI) has reached version 4.16.0, providing comprehensive command-line coverage for Autodesk Platform Services APIs. The tool is written in Rust for performance and reliability, and is available as open source under the Apache-2.0 license.

### What RAPS Does

RAPS replaces manual APS API calls with simple CLI commands:

```bash
# Instead of writing OAuth token exchange code
raps auth login

# Instead of multi-step upload API calls
raps object upload my-bucket model.rvt

# Instead of building translation job requests
raps translate start <urn> --format svf2 --wait

# Instead of polling for status
raps translate status <urn>
```

### Coverage

RAPS provides 55 top-level commands (95+ total operations) organized into command groups:

| Command Group | Operations | APS API |
|---------------|-----------|---------|
| `raps auth` | login, test, status, inspect, whoami, logout | Authentication v2 |
| `raps hub/project/folder/item` | list, create, navigate | Data Management v1 |
| `raps bucket` | create, list, info, delete | OSS v2 |
| `raps object` | upload, download, list, delete, copy, batch ops | OSS v2 |
| `raps translate` | start, status, manifest, download, metadata, properties | Model Derivative v2 |
| `raps da` | engines, appbundle-create, activity-create, run | Design Automation v3 |
| `raps webhook` | create, list, delete, test, verify-signature | Webhooks |
| `raps acc` | asset, submittal, checklist management | Construction Cloud v1 |
| `raps admin` | user, project, folder bulk operations | Account Admin |
| `raps pipeline` | run, validate, sample | Pipeline v2 engine |
| `raps config` | profile, get, set, context management | Local config |
| GitHub Actions | setup, pipeline, upload, translate | CI/CD (GitHub) |
| GitLab CI | .raps-setup, .raps-pipeline, .raps-upload, .raps-translate | CI/CD (GitLab) |

### Architecture

RAPS is built as a Rust workspace with 10 crates:

- **raps-cli**: Command-line interface and output formatting
- **raps-kernel**: Authentication, token management, HTTP client
- **raps-oss**: Object Storage Service operations
- **raps-dm**: Data Management API client
- **raps-derivative**: Model Derivative API client
- **raps-da**: Design Automation API client
- **raps-webhooks**: Webhooks API client
- **raps-acc**: Construction Cloud API client
- **raps-admin**: Account Admin API client
- **raps-reality**: Reality Capture API client

### Key Features in 4.14.0

- **API Health Tracking**: Real-time monitoring of APS endpoint health
- **Streaming Bucket Listing**: Per-region bucket listing with `tokio::select!`
- **Headless Auth Detection**: Auto-switches to device code flow in headless environments
- **PKCE Support**: Proof Key for Code Exchange for enhanced OAuth security
- **Unix Pipe Support**: Read from stdin, write to stdout for shell integration
- **MCP Server**: 101 tools for AI assistant integration
- **TUI Dashboard**: 7 tabs with 33 views for interactive monitoring

### What's New in v4.16

- **Pipeline v2 Engine**: A completely revamped pipeline engine with retry policies, configurable timeouts, `if`/`unless` conditionals, parallel step execution, `for-each` loops, and a built-in expression evaluator. Pipelines are defined in YAML and can orchestrate complex multi-step APS workflows with error handling and recovery.
- **Official CI/CD Integrations**: RAPS now ships with first-party CI/CD support:
  - **GitHub Actions** (v1.0.0): Four composite actions (`setup`, `pipeline`, `upload`, `translate`) for integrating RAPS into GitHub Actions workflows.
  - **GitLab CI Templates**: Four include templates (`.raps-setup`, `.raps-pipeline`, `.raps-upload`, `.raps-translate`) for GitLab CI/CD pipelines.
- **ASVS L2 Security Hardening**: Comprehensive security improvements aligned with OWASP ASVS Level 2 requirements, achieving 82% compliance. Includes enhanced token handling, input validation, secure credential storage, and audit logging.

### Installation

```bash
# Via Cargo
cargo install raps-cli

# Via Homebrew (macOS)
brew install dmytro-yemelianov/tap/raps

# Via Scoop (Windows)
scoop install raps
```

### About RAPS

RAPS is an open-source project developed by Dmytro Yemelianov. It is free to use under the Apache-2.0 license.

- **Website**: [rapscli.xyz](https://rapscli.xyz)
- **Source Code**: [github.com/dmytro-yemelianov/raps](https://github.com/dmytro-yemelianov/raps)
- **Author**: Dmytro Yemelianov (dmytroyemelianov@icloud.com)

---

*RAPS is an independent open-source project. Autodesk, APS, Forge, and related marks are trademarks of Autodesk, Inc.*
