# Session 1258: From CLI to Platform: Shipping a Cloud-Native APS Automation Stack

## Session Details

| Field | Value |
|-------|-------|
| **Session ID** | 1258 |
| **Title** | From CLI to Platform: Shipping a Cloud-Native APS Automation Stack |
| **Speaker(s)** | Dmytro Yemelianov |
| **Session Type** | 30-minute deep dive |
| **Status** | Draft |
| **Product** | Rapsody |

## AI Pillars

- [x] **Automate** - Speed repetitive tasks, shrink cycle times, reduce errors
- [x] **Assist** - Improve decisions with insights, copilots, and intelligent guidance
- [ ] Augment

## Themes

- [ ] Sustainability
- [x] **Digital Transformation**
- [x] **System Integration**

## Target Audience

- [ ] Business Decision Makers
- [x] **Developers/Architects** - How it's built, APIs, patterns, lessons learned

## Learning Objectives

1. Identify the architectural layers that evolve a CLI into a cloud-native APS automation platform
2. Implement distributed execution patterns with circuit breakers, checkpoint stores, and rate budgets
3. Design a web-accessible automation layer that serves developers, project managers, and AI agents from the same backend

![From CLI to Platform Hero](/devcon/images/1258-rapsody-hero.png)

## Abstract

The open-source RAPS CLI proved that 195+ APS operations could live behind a single binary with resilient auth, resumable bulk operations, and AI-ready output. But enterprise teams asked: what about the project manager who doesn't use a terminal? What about operations that run on a schedule at 2 AM? What about progress visibility when someone else kicked off a 10,000-user sync?

This session dissects the architecture of Rapsody — the commercial evolution of RAPS — showing how the same five layers (resilience, scale, output, discoverability, MCP) transform when you move from a local CLI to a distributed cloud platform. Rust workspace. Cloudflare Workers. PostgreSQL job queues. WebSocket progress. A web UI that non-developers can use. Same domain logic, fundamentally different deployment model.

## How This Differs from the RAPS Session

The RAPS session (OSS) focused on **patterns any developer can implement in any language** — auth caching, adaptive retry, structured output. The five layers were portable, language-agnostic principles.

This session focuses on **what changes when those patterns must serve a team, not a person**. Specifically:

| RAPS (OSS CLI) | Rapsody (Commercial Platform) |
|-----------------|-------------------------------|
| Runs on your laptop | Runs on Cloudflare Workers + SaaS gateway |
| State on disk (`~/.cache/raps/`) | State in PostgreSQL + Redis + Cloudflare D1 |
| Single user sees progress | Multiple users see progress via WebSocket |
| CLI output (table/JSON/CSV) | CLI + Web UI + REST API |
| Resume after laptop crash | Resume after anything — state is server-side |
| MCP tools from CLI binary | MCP tools from cloud API + WASM workers |
| `cron` for scheduling | Built-in scheduled operations with preflight checks |
| One binary, 195 commands | 12 Rust crates + Cloudflare Workers + React web tools |

The principles are identical. The deployment model changes everything.

## The Reality

Enterprise teams loved RAPS — but they hit three walls:

**Wall 1: "My project manager can't use a terminal."** The CLI is powerful, but half the team that needs automation doesn't write scripts. They need a browser.

**Wall 2: "I can't leave my laptop running overnight."** A bulk operation across 200 projects takes 45 minutes. Laptop sleeps. VPN disconnects. The operation dies at project 87.

**Wall 3: "Who ran what, and when?"** When five people have CLI access, nobody knows who added 400 users to the wrong projects last Tuesday.

Rapsody solves all three without abandoning the CLI. The same Rust domain logic serves the terminal, the web browser, and the AI agent.

## APS Components Used

- Authentication API (2-legged, 3-legged, device code flow)
- OSS API (Buckets, Objects, Signed S3 URLs, resumable uploads)
- Model Derivative API (Translations, Manifests, Metadata)
- Data Management API (Hubs, Projects, Folders, Items)
- ACC Issues API, RFIs API, Assets API, Submittals API, Checklists API
- ACC Account Admin API (Bulk User Management, Companies, Permissions)
- Webhooks API
- Design Automation API

## Autodesk Products

- Autodesk Construction Cloud (ACC)
- BIM 360

## Layer 1: Resilience — Now Distributed (7 min)

The RAPS session showed auth as infrastructure, adaptive retry, and resumable state. Those patterns survive unchanged in Rapsody. What changes is where they run and what watches them.

### Pattern 1: Circuit Breakers per API Family

A CLI retries and moves on. A platform needs to protect itself — and its neighbors.

Each APS API family (ACC Admin, OSS, Model Derivative, Issues) has its own circuit breaker. When ACC Admin starts returning 503s, the circuit opens for that API — but OSS operations keep running.

```
ACC Admin:  ██████████ OPEN (503 rate: 40%, cooldown 30s)
OSS:        ██████████ CLOSED (healthy, 0% error rate)
Issues API: ██████████ HALF-OPEN (testing recovery...)
```

The TUI dashboard (F8) shows this in real time. The web UI shows it to every team member. The CLI user who kicked off a bulk operation sees which API is causing the slowdown — not just "retrying..."

### Pattern 2: Checkpoint Store — Server-Side State

In RAPS, operation state lives in `~/.cache/raps/operation-state.json`. Laptop dies, state dies.

In Rapsody, every operation step is checkpointed to PostgreSQL. The Cloudflare Worker that processes the job reads from the checkpoint store. If the Worker restarts, the job restarts from the last checkpoint — not from the beginning.

```
Operation: user-add-batch-2026-03-25
├─ Step 1/200: ✓ completed (2ms)
├─ Step 2/200: ✓ completed (3ms)
├─ ...
├─ Step 47/200: ⚠ failed (503 — circuit breaker open)
├─ Step 48-200: ⏸ pending (auto-resume when circuit closes)
└─ Checkpoint: step=47, resumable=true, estimated_eta=12min
```

Nobody babysits the operation. It resumes on its own when the API recovers.

### Pattern 3: Rate Budgets Across Workers

A CLI manages its own rate limit. A platform has multiple workers hitting the same API simultaneously.

Rapsody uses Redis to coordinate rate budgets across all Workers processing jobs for the same account. Worker A consumed 40 of 100 requests this minute. Worker B sees 60 remaining and adjusts its concurrency.

```
Account: acme-construction
├─ Worker A: 40 requests used (bulk user add)
├─ Worker B: 30 requests used (permission export)
└─ Budget: 100/min, 30 remaining, throttling Worker B
```

No single Worker can starve the others. The total never exceeds the API's limit.

## Layer 2: Scale — Multi-Tenant Execution (6 min)

### Pattern 1: Job Queue Architecture

Every operation goes through the same pipeline:

```
Cart → Preflight → Queue → Worker → Checkpoint → Complete
```

**Cart**: The web UI collects operations (add users, remove users, change roles). A project manager drags users into a cart without writing a single command.

**Preflight**: Before execution, the system validates: Do these users exist? Are the project IDs valid? Will any operations conflict? This catches "I pasted the wrong spreadsheet" before it becomes "I added 400 contractors to the wrong account."

**Queue**: Cloudflare Queue distributes work to Workers. The queue survives deployments, restarts, and Worker recycling.

**Worker**: A Cloudflare Worker processes each job item with the same `raps-admin` Rust logic that powers the CLI — compiled to WASM. Same retry, same idempotency, same error classification.

**Checkpoint**: Every item result (success/skip/fail) is written to D1. The web UI shows real-time progress via Server-Sent Events.

### Pattern 2: Preflight Role Resolution

The #1 support issue with bulk user operations: "I specified `project_admin` but the API wanted `b6ea8f0f-0b3e-4da3-b1c9-0a82e3e8cb8d`."

ACC role names map to role IDs that differ per project and platform (ACC vs BIM 360). Rapsody's preflight step resolves role names to IDs before any API call is made:

```
Preflight: "Project Admin" for project X
├─ Platform: ACC
├─ Resolved roleId: b6ea8f0f-0b3e-4da3-b1c9-0a82e3e8cb8d
├─ Strategy: exact_match (confidence: 100%)
└─ Status: ✓ resolved
```

If resolution fails — wrong role name, unsupported platform, conflicting roles — the preflight catches it. The operation never starts.

### Pattern 3: The Same Concurrency, Distributed

The CLI uses a semaphore for concurrent requests. Rapsody uses the same semaphore per Worker, but coordinates across Workers via Redis:

```rust
// Same AdminOperation trait — CLI and Worker both implement it
#[async_trait]
impl AdminOperation for AddUser {
    async fn execute(&self, client: &AccountAdminClient, account_id: &str, project_id: &str)
        -> Result<OperationResult> { ... }
    fn is_retryable_error(&self, err: &Error) -> bool { ... }
}
```

The `execute_bulk_operation()` function in `raps-admin` doesn't know whether it's running in a terminal or a Worker. The concurrency layer adapts to the runtime.

## Layer 3: Output — Multiplexed Consumers (6 min)

### Pattern 1: The Web UI as an Output Layer

The RAPS session showed auto-detecting TTY vs pipe. Rapsody adds a third consumer: the browser.

The same operation produces:
- **CLI**: Table with progress bar on stderr, JSON result on stdout
- **Web UI**: Real-time progress cards, before/after diff views, operation history
- **REST API**: JSON responses for automation and integrations

All three read from the same PostgreSQL/D1 state. There's no separate "web backend" — the web UI calls the same API that the CLI calls.

### Pattern 2: Before/After Diff Views

When you change 200 users' roles, the web UI shows what changed:

```
john.doe@company.com
├─ Downtown Tower:    Project Viewer → Project Admin
├─ Harbor Bridge:     Project Viewer → Project Admin
└─ Hospital Phase 2:  (no change — already Project Admin)

jane.smith@company.com
├─ Downtown Tower:    (new — added as Project Admin)
└─ Harbor Bridge:     (new — added as Project Admin)
```

The CLI gets the same information as `--diff` output. The web UI renders it as expandable cards. Same data, different presentation — because the output types are shared.

### Pattern 3: Operation Audit Log

Every operation is recorded with: who initiated it, when, what changed, and the before/after state.

```bash
# CLI: query the operation history
raps admin operation list --limit 10

# Web UI: browse the same history with filtering
# /app/bulk-user-manager/history
```

Compliance asks "who changed permissions on the Hospital project?" The answer is a filter away — not a forensic investigation.

## Layer 4: Discoverability — Platform-Wide (5 min)

### Pattern 1: Compound MCP Tools

RAPS exposed 114 individual MCP tools. Rapsody adds compound tools that combine multiple operations:

```
bulk_upload          → upload N files with progress
bulk_download        → download N objects in parallel
upload_and_translate → upload + start translation + poll
search_and_download  → search by name + download matches
```

An AI agent no longer needs to orchestrate multi-step workflows. It calls one tool and the platform handles the steps.

### Pattern 2: Web-Based Tool Discovery

The web UI isn't just for operations. Each tool has documentation, parameter descriptions, and example payloads — generated from the same schema system that powers MCP:

```
/app/admin-console → System overview, MCP server status, tool catalog
/app/bulk-user-manager → User management, roles, companies, compliance
```

A project manager doesn't need to know CLI syntax. They navigate to the right tool, fill in the fields, review the preflight, and execute.

### Pattern 3: Scheduled Operations

Operations can run on a cron schedule — no CI/CD pipeline required:

```yaml
# Weekly permission audit — runs every Monday at 6 AM
schedule: "0 6 * * 1"
operation:
  action: export-permissions
  account_id: "01fb1602-..."
  notify: slack://webhook-url
```

The Cloudflare Worker fires on schedule, runs the operation, and notifies the team. No laptop needs to be open. No VPN needs to be connected.

## Layer 5: MCP — From Binary to Service (4 min)

### The Key Insight

RAPS proved that AI integration is a consequence of good architecture — same types, same auth, different transport. Rapsody takes this further: the MCP server runs as a cloud service, not a local binary.

**RAPS MCP**: Agent connects to a local process. Agent's laptop must be running.
**Rapsody MCP**: Agent connects to a cloud endpoint. Operations survive disconnection.

### What This Enables

```
User: "Add the entire electrical team to the new hospital project"

AI: [Calls admin_user_add — routes to cloud Worker]
    Preflight check: 47 users, 1 project, role: Project Member
    3 users already have access (will be skipped)
    Proceed?

User: "Yes"

AI: [Operation queued — Worker processes in background]
    44 added, 3 skipped. Operation ID: op-2026-03-25-001
    View details: https://tools.rapscli.xyz/app/bulk-user-manager/history/op-2026-03-25-001
```

The AI agent doesn't need to stay connected. The operation runs server-side with checkpoints, retries, and audit logging.

### Swarm Orchestration

Multiple AI agents — or multiple automation scripts — can coordinate through the same platform:

```
Agent A: Processing bulk uploads (OSS API, rate budget: 40/100)
Agent B: Running permission audit (ACC Admin, rate budget: 30/100)
Agent C: Translating models (Model Derivative, rate budget: 20/100)
Platform: Coordinating rate budgets, circuit breakers, checkpoints
```

The swarm dashboard shows all active operations across all agents, with circuit breaker states and rate budget utilization.

## The Bigger Picture

RAPS showed that resilience, scale, structured output, self-documentation, and AI integration are consequences of good architecture — not features you bolt on.

Rapsody shows what happens when those same principles serve a team instead of a person. The domain logic is identical — the same `AdminOperation` trait, the same retry classification, the same output types. What changes is where it runs (cloud, not laptop), who can use it (anyone with a browser, not just CLI users), and how it's observed (dashboards, not terminal output).

The patterns are portable. The architecture is Rust. The deployment is Cloudflare. But the principles work in any language, on any cloud, for any API platform.

## Key Takeaways

1. **Same domain logic, different deployment** — the `AdminOperation` trait runs identically in a CLI binary and a Cloudflare Worker
2. **Circuit breakers per API family** protect a platform from cascading failures across 15+ APIs
3. **Server-side checkpoints** mean operations survive Worker restarts, deployments, and network failures
4. **Rate budgets via Redis** coordinate multiple Workers hitting the same API without exceeding limits
5. **Preflight validation** catches errors before execution — wrong role names, invalid projects, conflicting operations
6. **The web UI is an output layer**, not a separate product — it reads the same state as the CLI and REST API
7. **Before/after diff views** show exactly what changed, for compliance and debugging
8. **Scheduled operations** remove the "someone needs to run this" bottleneck
9. **Cloud MCP** means AI agents don't need a running local binary — operations survive disconnection
10. **Swarm orchestration** coordinates multiple agents and scripts through shared rate budgets and circuit breakers

## RAPS vs Rapsody: When to Use Which

| Need | Use |
|------|-----|
| Personal automation, scripting, CI/CD | RAPS (OSS) |
| Team-wide operations with audit trail | Rapsody |
| Operations that must run unattended | Rapsody |
| Non-developer users need access | Rapsody |
| AI agent integration (local) | RAPS MCP |
| AI agent integration (cloud, multi-user) | Rapsody MCP |
| Learning APS automation patterns | RAPS (OSS, read the source) |
| Production enterprise deployment | Rapsody |

RAPS is free, open source, and frozen at v5.7.0. Rapsody is the actively developed commercial evolution. Both share the same architectural DNA.

## Resources

- **Rapsody**: https://rapsody.dev
- **RAPS (OSS)**: https://github.com/dmytro-yemelianov/raps
- **Documentation**: https://rapscli.xyz/docs
- **Web Tools**: https://tools.rapscli.xyz
- **MCP Server Guide**: https://rapscli.xyz/docs/mcp-server
- **Account Admin Guide**: https://rapscli.xyz/docs/account-admin
