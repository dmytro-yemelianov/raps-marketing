# Session 1258: Zero to Production: Shipping an AI-Ready APS CLI in 30 Min

## Session Details

| Field | Value |
|-------|-------|
| **Session ID** | 1258 |
| **Title** | Zero to Production: Shipping an AI-Ready APS CLI in 30 Min |
| **Speaker(s)** | Dmytro Yemelianov |
| **Session Type** | 30-minute deep dive |
| **Status** | Complete |

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

1. Identify the five architectural layers that make an APS client robust at enterprise scale
2. Implement resilient patterns for authentication, rate limits, and bulk operations in any language
3. Design output layers that serve humans, scripts, and AI agents from a single code path

![Zero to Production Hero](/devcon/images/1258-zero-to-production-hero.png)

## Abstract

Many teams want to automate their APS workflows but get stuck on the same problems: authentication flows that require careful handling across environments, translations with complex failure modes, and bulk operations that push against API rate limits. These aren't flaws — they're the reality of building on a platform that spans 15+ APIs and serves millions of users.

This session dissects the architecture of a production CLI that covers 195+ APS operations, showing the five layers that let it survive platform instability at enterprise scale. You'll learn patterns for resilient auth, bulk operations that resume after failures, output that feeds humans, scripts, and AI agents without adaptation, and how structured design made 114 AI-agent tools almost free. Language-agnostic. Battle-tested. Open source.

## The Reality

APS covers an enormous surface area — 15+ API families, from object storage to construction management to design automation. That breadth is its strength, but it also means complexity compounds fast. Authentication spans multiple OAuth flows. Translations handle dozens of CAD formats with different failure modes. Bulk operations at enterprise scale — hundreds of projects, thousands of users — push every API's rate limits and pagination boundaries.

The community feels this complexity. On Stack Overflow, the hardest topics to get answers on are webhooks, ACC API, and authentication — not because they're poorly designed, but because they involve the most moving parts. The most-requested feature on ACC Ideas, bulk user assignment across projects, has 344 kudos — a clear signal that enterprise teams need programmatic access to operations the UI handles one at a time.

Good tooling bridges this gap. We built RAPS to handle the complexity so developers can focus on their actual workflows: 195+ operations across 15+ APIs, bulk operations that resume after network failures, output that serves humans, scripts, and AI agents from a single code path.

Here's how — layer by layer.

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

## Layer 1: Resilience (7 min)

APS authentication is evolving — SSA migration, Developer Hub consolidation, new scope requirements. These are good changes that improve security, but they mean your automation needs to absorb platform evolution gracefully. A client that hardcodes auth assumptions will break; one that abstracts the auth layer adapts.

### Pattern 1: Auth as Infrastructure

Authentication is table stakes, but most teams get it wrong the first time. Three decisions that save weeks of debugging:

**Token caching with pre-expiry refresh.** Don't wait for a 401. Refresh 5 minutes before expiry so no request ever fails mid-flight. The 300-second margin sounds paranoid until your first large upload fails at 98% because the token expired during transfer.

**2-legged / 3-legged auto-selection.** The client knows which OAuth flow to use based on what the operation needs. Bucket operations → 2-legged. Project navigation → 3-legged. The caller doesn't think about it.

**Credential storage abstraction.** Keyring on desktop, environment variables in CI, file fallback in Docker. One interface, three backends. Developers and CI pipelines use the same CLI with zero configuration changes.

### Pattern 2: Adaptive Per-Endpoint Retry

Model Derivative returns "TranslationWorker-InternalFailure." Do you retry? Is it permanent?

The answer: it depends on the endpoint. Translation failures are often transient (server overload). A 404 on a bucket is permanent. A 429 on any endpoint means "slow down, try again."

The pattern: track failure rates per endpoint. Adjust backoff multipliers (1x → 2x → 4x). Parse `Retry-After` headers when the API provides them. Exponential backoff with jitter so parallel clients don't all retry at the same instant.

```
Attempt 1: failed (500)  → wait 1s + jitter
Attempt 2: failed (500)  → wait 2s + jitter
Attempt 3: success       → reset counter for this endpoint
```

Not all 500s are equal. A translation failure at 3 AM is different from a rate limit at peak hours. Your retry logic should know the difference.

### Pattern 3: Resumable State for Bulk Operations

You're adding a user to 200 projects. Network fails at project 47. Without resumable state, you start over. With it:

```bash
# Resume from where you left off
raps admin operation resume

# Check what happened
raps admin operation status
# ┌────────────┬───────┬──────┬────────┬────────┐
# │ Operation  │ Total │ Done │ Failed │ Status │
# ├────────────┼───────┼──────┼────────┼────────┤
# │ user-add   │  200  │  47  │   0    │ paused │
# └────────────┴───────┴──────┴────────┴────────┘
```

Operation progress is checkpointed to disk. Every operation is idempotent — re-running doesn't create duplicates. User already exists? Skip. Role already correct? Skip. And every destructive operation supports `--dry-run`: preview exactly what will happen before executing.

**The principle:** Your automation will fail. The question is whether it fails gracefully — with state you can inspect, resume, and audit — or catastrophically.

## Layer 2: Scale (6 min)

The most-requested feature on ACC Ideas — bulk user assignment across projects — has 344 kudos. The ACC UI is designed for project-level management, which makes sense for most users. But when you have 200 projects and need to onboard someone across all of them, you need a different approach.

### Pattern 1: Semaphore-Based Concurrency with Rate-Limit Awareness

Naive parallelism: spawn 200 requests, get 429'd after 20, crash.

Smart parallelism: a semaphore limits concurrent requests. Default 5, configurable up to 50. But the real trick is proactive throttling — parse `X-RateLimit-Remaining` headers and slow down *before* hitting the limit.

```
Request 1-20:   remaining = 80   → full speed
Request 21-40:  remaining = 30   → slow to 10 concurrent
Request 41+:    remaining = 8    → slow to 3 concurrent
```

The API tells you when it's about to reject you. Most clients ignore this signal and react to 429s after the fact. Proactive throttling avoids the penalty entirely.

### Pattern 2: Adaptive Throughput for Uploads

Not all uploads are equal. A 2MB DWG file on fast datacenter internet is different from a 500MB NWD file on office WiFi.

- Small files (<5MB): single PUT, no chunking overhead
- Medium files (5-100MB): 5MB chunks, reasonable parallelism
- Large files (>100MB): 25MB chunks, fewer round trips

RAPS goes further: it measures actual upload speed and adjusts dynamically. Slow connection → smaller chunks (less wasted on retry). Fast connection → larger chunks (fewer round trips).

```bash
# Upload 47 files, 8 parallel streams
raps object upload-batch my-bucket *.rvt --parallel 8
# Sequential: ~45 minutes
# Parallel with adaptive chunking: ~4 minutes
```

### Pattern 3: The Bulk Operation Contract

Every result in a bulk operation is one of three things:

- **Success** — operation completed
- **Skipped** — already done (user already has access, file already uploaded)
- **Failed** — unexpected error

**Skipped** is the key insight. Idempotent operations mean re-running is always safe. The operation detects existing state and moves on. This is what makes resumable operations work — you don't need to track exactly which items succeeded; you just re-run and let the idempotency handle it.

```bash
# Preview with dry-run
raps admin user add "$ACCOUNT_ID" "user@company.com" \
  --role project_admin --dry-run
# Would add to 127 projects
# 73 projects: already has access (skipped)

# Execute — completes in under 2 minutes
raps admin user add "$ACCOUNT_ID" "user@company.com" \
  --role project_admin
# ✓ 127 added, 73 skipped, 0 failed
```

Real progress tracking with ETA — not a spinner. "Project 127/200 — 3 min remaining." Numbers your team can plan around.

**The principle:** Bulk operations aren't loops. They're state machines — with concurrency control, progress tracking, and a clear contract for success, skip, and failure.

## Layer 3: Output (6 min)

![CLI Workflow](/devcon/images/1258-zero-to-production-workflow.png)

You automate an APS workflow. It works. Then your manager asks for a weekly report in Excel. Your DevOps team wants it in their CI pipeline. The data team wants it in Power BI. An AI agent needs it in JSON. You now maintain four output formats — or you grep your way through table output and pray nobody changes a column.

### Pattern 1: Context Auto-Detection

Is stdout a terminal? → colored table with auto-sized columns.
Is stdout piped? → JSON, no flags needed.
Is `RAPS_OUTPUT_FORMAT` set? → whatever the environment demands.

The same command serves three consumers without configuration:

```bash
# Human at a terminal — sees a table
raps bucket list
# ┌─────────────────────────┬────────────┬────────┐
# │ Bucket Key              │ Policy     │ Region │
# ├─────────────────────────┼────────────┼────────┤
# │ hospital-project-2026   │ persistent │ US     │
# │ temp-uploads            │ transient  │ US     │
# └─────────────────────────┴────────────┴────────┘

# Script piping to jq — gets JSON automatically
raps bucket list | jq '.[0].bucketKey'
# "hospital-project-2026"

# CI environment variable — gets whatever it needs
RAPS_OUTPUT_FORMAT=csv raps bucket list > buckets.csv
```

Zero flags in the common cases. The right thing happens automatically.

### Pattern 2: The stderr/stdout Contract

This is the single most important design decision for an AI-ready CLI.

**stdout** = structured data only. The payload. What a machine parses.
**stderr** = everything else. Progress bars, "Uploading..." messages, warnings, prompts.

Why it matters: `raps translate start --wait` shows a progress bar updating in real time on stderr while the final manifest comes out clean on stdout. A human sees both. A script captures only the result. An AI agent gets parseable JSON without stripping spinner characters.

```bash
# Human sees progress AND result
raps translate start $URN --format svf2 --wait
# Translation: pending 15%... 42%... 78%... 100%    ← stderr
# {"status": "success", "derivatives": ["svf2"]}     ← stdout

# Script captures only the result
result=$(raps translate start $URN --format svf2 --wait)
# $result = clean JSON, no progress noise
```

If you put a single human-friendly message on stdout, you've broken every downstream consumer. Every progress indicator, every warning, every "Uploading file 3 of 47..." — all stderr.

### Pattern 3: NDJSON for Streaming

Not a JSON array. One JSON object per line. No closing bracket to wait for.

An AI agent processing 10,000 issues starts working after the first line, not after the last. A monitoring pipeline can tail the output like a log stream.

```bash
# Stream-process one record at a time
raps admin user list "$ACCOUNT_ID" --output ndjson | \
  while read -r user; do
    echo "$user" | jq '{email: .email, status: .status}'
  done
```

For large result sets, NDJSON is the difference between "wait 30 seconds for the full response" and "start processing immediately."

### Pattern 4: CSV as a First-Class Citizen

The person asking for the data is often a project manager, not a developer.

```bash
# Compliance asks "who has access to what?"
raps admin export-permissions --account "$ACCOUNT_ID" --output csv > permissions.csv
# Open in Excel. Filter. Email to compliance. Done.
```

No transformation script. No "let me write a quick Python thing to convert that JSON." The answer is a CSV they can open, filter, and forward — not a JSON blob that needs a developer to interpret.

**The principle:** Your CLI's output format is a contract with every consumer you'll ever have — humans today, scripts tomorrow, AI agents next year. Design it once. Get it right.

## Layer 4: Discoverability (5 min)

APS spans a massive API surface — 15+ API families, each with its own documentation site, versioning scheme, and community forum. For developers, finding the right endpoint, understanding its parameters, and knowing the response shape takes real effort. ACC APIs are the newest and fastest-growing, which means the docs and community knowledge are still catching up to the platform's capabilities.

What if your tool could answer "what can you do?" programmatically?

### Pattern 1: Runtime JSON Schema

Every output type in your client has a schema. Not a docs page — a queryable schema at runtime.

```bash
# What types are available?
raps schema list
# bucket-info, object-info, translation-manifest, issue, rfi, ...

# What does a bucket look like?
raps schema generate bucket-info
# {
#   "type": "object",
#   "properties": {
#     "bucketKey": { "type": "string", "description": "Unique bucket identifier" },
#     "policyKey": { "type": "string", "enum": ["transient", "temporary", "persistent"] },
#     "region": { "type": "string", "enum": ["US", "EMEA"] }
#   }
# }
```

An AI agent discovering your tool for the first time calls `schema list`, picks what it needs, and knows the exact shape of every response before making a single call. No documentation scraping. No hallucinated field names.

No platform team can document every edge case across 15+ API families. Your client can fill the gap by documenting itself.

### Pattern 2: Structured Exit Codes

Not 0 and 1. Semantic codes that machines can branch on:

| Code | Meaning | Automated response |
|------|---------|-------------------|
| 0 | Success | Continue |
| 1 | Auth failure | Re-authenticate |
| 2 | Not found | Skip or report |
| 3 | Rate limited | Wait and retry |
| 4 | Network error | Retry with backoff |
| 5 | Invalid input | Fail fast, fix input |
| 6 | Server error | Retry or escalate |

A CI pipeline branches: exit 3 → retry with backoff. Exit 5 → fail fast, bad input. Exit 1 → re-authenticate. An AI agent interprets: "rate limited, I should wait" — without parsing an error string.

### Pattern 3: Auto-Generated Tool Documentation

```bash
# Generate AGENTS.md from live code
raps docs mcp --write
# 114 tools documented: descriptions, parameters, auth requirements, examples

# CI check: fail if code changed but docs didn't regenerate
raps docs mcp --check
```

Any documentation maintained separately from code eventually drifts — that's true for every platform, not just APS. Machine-generated docs from live code can't go stale. If the code changes, the docs change.

**The principle:** The best documentation is the kind that can't be wrong — because it's generated from the code that runs.

## Layer 5: MCP — AI Integration as a Consequence (4 min)

The ACC marketplace has 259 apps — rich UI tools for specific workflows. But there's an untapped category: CLI tools and AI-agent integrations. No one has built them yet, which means there's a wide-open opportunity for developers who think in terms of pipelines, automation, and programmatic access.

### The Key Insight

We built 195 CLI commands. We needed 114 AI tools. We didn't rewrite anything.

- **Same auth layer** — MCP tools use the same token cache, same pre-expiry refresh, same 2-leg/3-leg selection.
- **Same resilience** — retries, rate-limit handling, error classification come for free.
- **Same output types** — MCP tool responses are the same serializable types that produce JSON, CSV, and tables.
- **Same domain logic** — the MCP handler for `bucket_list` calls the same function as `raps bucket list`. It's a transport adapter, not a reimplementation.

114 tools. Each one is a thin wrapper over existing domain logic. The MCP server and the CLI share everything except the transport.

### What This Enables

```
User: "What buckets do I have?"

AI: [Calls bucket_list tool — same code path as CLI]
    You have 4 buckets:
    1. hospital-central-2026 (persistent, US)
    2. temp-processing (transient, US) - 3 objects
    3. archive-2025 (persistent, US) - 147 objects
    4. eu-client-data (persistent, EMEA) - 52 objects

User: "Add new.engineer@company.com to all active projects"

AI: [Calls admin_user_add — same resilience, same dry-run]
    Adding to 127 active projects...
    125 added, 2 already had access (skipped).
```

The AI doesn't hallucinate endpoints. It uses the same tools, the same auth, the same error handling as the CLI.

### The Punchline

AI integration isn't a feature you bolt on. It's what happens when your resilience layer handles failures, your output layer speaks JSON, and your schema layer describes itself. MCP was a weekend of wiring, not a quarter of rewriting.

## The Bigger Picture

APS is powerful — and like any platform spanning 15+ API families, it rewards developers who design for its complexity rather than fighting it.

The patterns we showed today — resilience, scale, structured output, self-documentation, and AI as a consequence — aren't specific to RAPS or to Rust. They're how you build automation that survives production. Apply them in Python, C#, Node, Go — the architecture is the same.

The code is open source. The patterns are yours. Go build.

## Key Takeaways

1. **Auth is infrastructure, not application logic** — cache tokens, refresh before expiry, abstract credential storage
2. **Retry per endpoint, not globally** — translation failures and rate limits need different strategies
3. **Resumable bulk operations** survive network failures without restarting from item 1
4. **Proactive rate-limit throttling** reads API headers and slows down before getting 429'd
5. **Auto-detect output format** — TTY gets tables, pipes get JSON, no flags required
6. **The stderr/stdout contract** — progress to stderr, data to stdout, one command serves all consumers
7. **Runtime JSON Schema** lets machines discover your tool's capabilities programmatically
8. **Structured exit codes** give machines semantics to branch on, not strings to parse
9. **Auto-generated docs from live code** can't go stale
10. **AI integration is a consequence** of getting the other layers right — same types, same auth, different transport

## Resources

- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **Documentation**: https://rapscli.xyz/docs
- **MCP Server Guide**: https://rapscli.xyz/docs/mcp-server
- **Account Admin Guide**: https://rapscli.xyz/docs/account-admin
- **Output Formats**: https://rapscli.xyz/docs/output-formats
- **Command Reference**: https://rapscli.xyz/docs/commands
- **CI/CD Integrations**: https://rapscli.xyz/docs/ci-cd
