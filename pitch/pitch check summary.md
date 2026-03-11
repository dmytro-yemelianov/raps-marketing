# Pitch Check — Verification Summary

> Generated 2026-03-11 against RAPS v5.6.0 codebase

---

## Critical Issues

| # | Claim | Actual | Action |
|---|-------|--------|--------|
| 1 | 51 MCP tools | **114 tools** (`raps-cli/src/mcp/definitions.rs`) | Update to **110+** everywhere |
| 2 | 100+ commands | **~238** (49 top-level + 189 subcommands) | Update to **230+** everywhere |
| 3 | Python & Node bindings | Python (PyO3) exists; **Node bindings do not exist** | Remove Node or mark as planned |
| 4 | 15+ APIs covered | **11 confirmed** (OSS, DM, Model Derivative, Issues, RFI, Assets, Submittals, Checklists, Admin, DA, Reality Capture, Webhooks) | Change to **12 APIs** or list explicitly |
| 5 | Version v4.13.0+ | **v5.6.0** | Update |

## Important Issues

| # | Claim | Actual | Action |
|---|-------|--------|--------|
| 6 | 200+ forum threads analyzed | 4,295 ACC ideas scraped + scattered forum analysis; no consolidated "200+ threads" methodology | Reframe — actual data is stronger (4,295 ideas alone) |
| 7 | Petr Broz comparison "vs RAPS 51" | RAPS has 114 tools, not 51; competitor tool count undocumented | Fix both numbers |
| 8 | Frederic Python SDK "373 endpoints" | No source found in marketing docs | Needs verification |
| 9 | forge-cli archived | Referenced but not verified against live GitHub | Verify at github.com/Autodesk-Forge/forge-cli |
| 10 | AI/MCP integration: NONE across all vendors | Petr Broz's aps-mcp-server exists for Autodesk | Change to "minimal" or "basic" for Autodesk |

## Confirmed Correct

| # | Claim | Status |
|---|-------|--------|
| 11 | CLI + MCP server + Cloud | All three exist |
| 12 | Python bindings via PyO3 | `python-bindings/` with maturin, Python 3.8–3.13 |
| 13 | Paid plugin tiers | Free and Pro tiers with monthly/yearly pricing |
| 14 | Rust-optimized | Rust 2024 edition, v1.88+ |
| 15 | Cloudflare deployment | 4 Workers (device-auth, rapscli-api, url-shortener, webhook-gateway) |
| 16 | Docker/Container support | 7 Dockerfiles, docker-compose, Kubernetes Helm charts |
| 17 | GitHub Actions CI/CD | 14+ workflows |
| 18 | mcp.rapscli.xyz | Configured in `.mcp.json` with Bearer auth |
| 19 | Fire-and-forget mode | `tokio::spawn` in device code auth flow |
| 20 | 4,078 apps analyzed | Confirmed in `opportunity_report.md` and `gaps.json` |
| 21 | 3 DevCon sessions submitted | Sessions 1257, 1258, 1259 — all marked Complete |

## Needs Dmytro Confirmation

- QuikTrip: $14B revenue, 1,700+ projects, LOI status, Blake's engagement
- Cyrille Fauvel: exact title, May demo date
- Michael Beale: exact title, 2 RCW migration leads
- Expert Elite / ADN membership current status
- Sitecore contract end date (April 2026)
- Guilherme Pombeiro title

## Recommended Changes

1. **"51 MCP tools" → "110+ MCP tools"** — everywhere in deck + analytics PDF
2. **"100+ commands" → "230+ commands"** — everywhere
3. **Remove "Node bindings"** — or mark as roadmap item
4. **"15+ APIs" → "12 APIs"** — or enumerate them
5. **Update version** — v4.13.0 → v5.6.0
6. **Fix competitive comparison** — RAPS 114 tools vs competitor, not 51
7. **"AI/MCP: NONE across all vendors"** → "minimal" for Autodesk (Petr Broz's server exists)
8. **"200+ forum threads"** → reframe around 4,295 ACC ideas + multi-platform analysis

## Suggested Additions

### Stronger numbers already available but unused

- **4,295 ACC feature requests analyzed** — far more impressive than "200+ forum threads". Lead with this number.
- **10-crate Rust workspace** — signals serious engineering architecture, not a side project.
- **14+ CI/CD workflows** — CodeQL, Semgrep, fuzzing, SBOM generation. Shows enterprise-grade software practice.

### Enterprise readiness story (not mentioned in pitch)

- **3 deployment tiers** documented: Docker Compose (dev/small), Fly.io (serverless), Kubernetes (enterprise). A C-level audience cares about scalability options — "Cloud (Cloudflare containers)" undersells this.
- **Kubernetes Helm charts** with HPA auto-scaling and multi-tenant isolation — enterprise-ready out of the box.
- **Multi-format output** (JSON, table, CSV) — matters for enterprise integration and CI/CD pipelines.
- **Offline-capable CLI** — runs without cloud dependency, cloud is optional. Reduces buyer objection about vendor lock-in.

### Concrete pricing makes "paid tiers" tangible

- Pro plugins have actual prices: TUI Dashboard at $10/mo, ACC Bulk Manager at $15/mo. Naming even one example is more convincing than "paid tiers exist".

### Competitive landscape targets wrong audience

- Petr Broz and Frederic's SDK are developer tools — a C-level audience won't know them. The marketplace analysis found **BIM load** and **IMAGINiT ACCelerate** as actual commercial competitors. These are recognizable AEC names and make the competitive moat clearer.

### Reframing suggestions

- "Python & Node bindings" → **"Python bindings (PyO3), WASM planned"** — honest and still forward-looking.
- "15+ APIs" → **enumerate the 12 in a compact grid** — explicit list is more convincing than a rounded number when the real count is lower.
- "$80B industry" → **source this claim**. AEC software, construction tech, and PLM markets have different numbers. A C-level will ask.

### Housekeeping

- **Python bindings version mismatch** — workspace is v5.6.0 but `python-bindings/` is at v5.0.0. Sync before demo.
- **raps-actions repo** — if pre-built GitHub Actions composites and GitLab CI templates exist, add them to "What We Already Have". Concrete CI/CD integration story.
