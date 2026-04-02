---
title: "RAPS 5.2: Interactive Init Wizard, Status Dashboard, and rapscli-api Worker"
description: "RAPS 5.2 ships a guided init wizard for first-time setup, raps status context dashboard, account context banners across admin commands, and a Cloudflare Worker API powering install scripts and shields.io version badges."
type: "release"
publishDate: 2026-03-06
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.2: Interactive Init Wizard, Status Dashboard, and rapscli-api Worker

*Open-source APS CLI gets guided onboarding, a live context dashboard, and a Cloudflare Worker powering install scripts and shields.io version badges*

---

**Version Information**
- **Current Version**: 5.2.0
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates
- **License**: Apache-2.0

---

The biggest friction point for new APS developers has always been the first fifteen minutes: locating credentials, understanding 2-legged vs 3-legged auth, figuring out which hub you're even talking to. RAPS 5.2 collapses that gap with a guided init wizard that walks through every step, a status dashboard that shows exactly where you stand at any moment, and a Cloudflare Worker backend that keeps the install experience fast and the README badges live.

### What's New in 5.2.0

**`raps init` — Guided Onboarding Wizard**

Running `raps init` on a fresh install launches a 6-step interactive wizard:

1. **Credentials** — enter Client ID and Client Secret; stored securely in the RAPS config
2. **2-legged auth test** — immediately verifies the credentials work against APS before proceeding
3. **Login** — walks through 3-legged OAuth (browser or device code) to capture a user token
4. **Hub discovery** — lists available hubs and prompts you to select the one you want as your default
5. **Enterprise context setup** — detects hub tier (personal, enterprise, BIM360, ACC) and configures account context accordingly
6. **Summary** — prints a confirmation screen showing account, hub, tier, and auth state

The whole flow takes under two minutes. At the end, `raps hub list` and every admin command work without additional flags.

**`raps status` — Context Dashboard**

`raps status` prints a full-context dashboard: current account identity, hub name and tier, connected projects count, and auth state (token validity, expiry). It is the single command to run when you need to confirm "am I pointing at the right thing?" before a destructive operation or a CI run.

**Account Context Banners**

`raps hub list` and all admin commands now render an inline context box at the top of their output showing hub name, tier classification, and account. The HubTier enum covers four cases — personal, enterprise, BIM360, and ACC — so the banner reflects the actual environment rather than a generic label. This is especially useful when managing multiple APS accounts or switching between personal and enterprise hubs.

**Admin Improvements**

A new `add-to-all-projects` command bulk-adds a user to every project under an account in one invocation. Commands that previously required `--account` now auto-resolve it via hub list when the flag is omitted, removing a common source of "missing required flag" errors in scripts.

**rapscli-api Cloudflare Worker**

A new Cloudflare Worker at `rapscli.xyz` backs several pieces of infrastructure that previously required hardcoded values or manual maintenance:

- **Install script API** — `curl -fsSL https://rapscli.xyz/install.sh | sh` resolves the latest release version dynamically rather than pinning a tag in the script
- **Version API** — JSON endpoint consumed by shields.io for live version badges in the README and documentation
- **URN decoder** — utility endpoint that decodes APS Base64-encoded URNs to human-readable form
- **APS status endpoint** — proxies Autodesk's API health data for CLI diagnostics
- **URL shortener** — short links at `rapscli.xyz` for use in documentation and community posts

**Device Auth Polish**

The device auth flow now passes the user code as a `?code=` query parameter in the verification URL, so navigating to `rapscli.xyz/device?code=ABCD-1234` pre-fills the code field. A plain fallback URL is shown when the terminal cannot render the query string.

**Standardized Exit Codes**

All CLI commands and SDK crates now return consistent exit codes: `0` for success, `1` for general error, `2` for auth failure, `3` for not found, `4` for rate limited. Scripts and CI pipelines can now branch on exit codes without parsing output text.

### Availability

RAPS 5.2.0 is available now:

```bash
curl -fsSL https://rapscli.xyz/install.sh | sh
```

Or via package managers:

```bash
cargo install raps-cli
npm install -g @dmytro-yemelianov/raps-cli
pip install raps
brew install dmytro-yemelianov/tap/raps
```

### About RAPS

RAPS (Rust Autodesk Platform Services) is an open-source CLI and SDK for Autodesk Platform Services, written in Rust. It provides 195+ operations across 51 command families and 10 workspace crates, covering 15+ APS APIs including authentication, data management, model translation, design automation, construction administration, and more. The current release is v5.7.0 with 114 MCP tools for AI assistant integration. Available at github.com/dmytro-yemelianov/raps under Apache-2.0.

**Website:** https://rapscli.xyz
**Repository:** https://github.com/dmytro-yemelianov/raps
**Documentation:** https://rapscli.xyz/docs
