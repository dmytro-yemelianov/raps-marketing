---
title: "RAPS 5.1: Device Code Authentication for Headless Environments"
description: "RAPS adds GitHub-style device code auth flow via Cloudflare Worker proxy, enabling OAuth login from SSH sessions, containers, and MCP servers."
type: "release"
publishDate: 2026-03-02
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.1: Device Code Authentication for Headless Environments

*Open-source APS CLI introduces "go to URL, enter code" OAuth flow for SSH, containers, and AI assistants*

---

**Version Information**
- **Current Version**: 5.1.0
- **Previous Version**: 5.0.0
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates + 2 Cloudflare Workers
- **License**: Apache-2.0

---

3-legged OAuth in headless environments has always been painful. Copy a long URL, paste it somewhere, authorize, copy the callback URL back. RAPS 5.1 replaces this with a familiar experience: a short code you enter on any device.

### What's New

**Device Code Auth Flow**

Run `raps auth login --device` and you get a short code like `ABCD-1234`. Open `rapscli.xyz/device` on your phone, laptop, or any browser. Enter the code, authorize with your Autodesk account, and the CLI completes login automatically. No local browser required.

**Cloudflare Worker Proxy**

A new Cloudflare Worker at `rapscli.xyz/device` bridges the gap between APS (which doesn't support RFC 8628 natively) and the CLI. The proxy manages session state via Durable Objects with automatic 5-minute TTL cleanup. PKCE security is preserved end-to-end — the proxy never sees the client_secret or code_verifier.

**Automatic Headless Detection**

RAPS detects headless environments (SSH, Docker, CI runners) and automatically switches to the device code flow with clear instructions.

### Security

- `code_verifier` never leaves the CLI
- `client_secret` never reaches the proxy
- Authorization codes wiped on consumption, alarm-cleaned at 300 seconds
- CSRF protection via session ID as OAuth state parameter

### Availability

RAPS 5.1.0 is available now:

```bash
cargo install raps
npm install -g @dmytro-yemelianov/raps-cli
pip install raps
brew install dmytro-yemelianov/tap/raps
```

### About RAPS

RAPS (Rust Autodesk Platform Services) is an open-source CLI and MCP server for Autodesk Platform Services. It provides 195+ operations across 51 command families and 114 MCP tools covering 15+ APS APIs, with 10 workspace crates and enterprise features including swarm orchestration, distributed job processing, and pipeline automation. The current release is v5.7.0.

**Website:** https://rapscli.xyz
**Repository:** https://github.com/dmytro-yemelianov/raps
**Documentation:** https://rapscli.xyz/docs
