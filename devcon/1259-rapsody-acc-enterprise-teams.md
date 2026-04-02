# Session 1259: ACC at Enterprise Scale: Automation for Teams, Not Just Developers

## Session Details

| Field | Value |
|-------|-------|
| **Session ID** | 1259 |
| **Title** | ACC at Enterprise Scale: Automation for Teams, Not Just Developers |
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

- [x] **Business Decision Makers** - Strategy, ROI, operational outcomes
- [x] **Developers/Architects** - How it's built, APIs, patterns, lessons learned

## Learning Objectives

1. Identify enterprise ACC workflows that benefit from a web-based automation platform vs CLI scripts
2. Implement self-service user management, scheduled audits, and compliance dashboards accessible to non-developers
3. Design operation safety layers with preflight validation, before/after diffs, and rollback capability

![ACC Enterprise Teams Hero](/devcon/images/1259-rapsody-hero.png)

## Abstract

The RAPS session showed how CLI automation cuts enterprise ACC admin overhead from $600K/year to $60K/year. But the person running those scripts was always a developer. The project coordinator who onboards 50 subcontractors can't open a terminal. The compliance officer who needs a weekly permission audit doesn't write YAML pipelines.

Rapsody brings the same automation to the browser. Same resilience, same idempotency, same APS API patterns — but wrapped in a web platform that project managers, compliance teams, and account administrators use directly. No scripts. No terminal. No "can you run that command for me?"

This session walks through the same three enterprise problems from the RAPS session — bulk project creation, cross-hub data sync, and permission audits — but shows how each is solved when the tool is a platform, not a CLI.

## How This Differs from the RAPS Session

The RAPS session taught **developers how to automate ACC** with CLI commands and shell scripts. Every example was `raps admin ...` in a terminal.

This session shows **how teams use the same automation** through a web UI, scheduled operations, and compliance dashboards — without touching a terminal.

| RAPS (OSS Session) | Rapsody (This Session) |
|--------------------|------------------------|
| `raps admin user add ...` | Web UI: drag users into cart, click Execute |
| `raps pipeline run matrix.yaml` | Scheduled operation: runs every Monday at 6 AM |
| `comm -23 <(cut -d, -f2 ...)` | Comparison page: visual side-by-side diff |
| `raps admin export-permissions > audit.csv` | Compliance dashboard: score, violations, trends |
| Shell script with `while read -r` | Import page: paste CSV, preview, preflight, execute |
| Manual `--dry-run` before every command | Automatic preflight on every operation |
| `git blame` to find who changed what | Operation history with full audit trail |
| Developer runs it | Anyone on the team runs it |

The architecture underneath is identical. The Rust crates don't know the difference. The audience changes.

## The Enterprise ACC Reality (Unchanged)

The same picture from the RAPS session. A large general contractor. 200+ active projects. 8 coordinators. 160 admin hours/week. $600,000/year in overhead.

The math hasn't changed. What changed is who can use the solution.

**With RAPS (OSS):** One developer writes scripts. Five coordinators ask them to "run that command" every time something needs to change. The developer becomes a bottleneck.

**With Rapsody:** Five coordinators manage users themselves through the web UI. The developer sets up the platform once and moves on to actual development work.

## APS Components Used

- ACC Account Admin API v2 (Projects, Users, Companies, Permissions)
- BIM 360 HQ v1 API (legacy accounts)
- Data Management API (Hubs, Projects, Folders, Items)
- ACC Issues API, Submittals API, Checklists API, RFIs API, Assets API
- OSS API (Bulk uploads)
- Model Derivative API (Batch translations)

## Autodesk Products

- Autodesk Construction Cloud (ACC)
- BIM 360 (legacy migration and mixed-account scenarios)

## Strategy 1: Bulk User Management — Self-Service

### The Problem (Same as RAPS)

You've onboarded a mechanical subcontractor with 50 engineers. Each needs access to 12 projects with the role "Project Member." In the ACC UI, that's 600 individual operations — each requiring navigating to a project, clicking Members, clicking Add, searching for the email, selecting the role, clicking Add.

### The RAPS Solution (CLI)

```bash
raps admin user add "$ACCOUNT_ID" "engineer@mech-sub.com" \
  --role "Project Member" --filter "^Hospital" --dry-run
```

Powerful. Fast. Requires a developer.

### The Rapsody Solution (Web UI)

The project coordinator opens the Bulk User Manager at `tools.rapscli.xyz/app/bulk-user-manager/`.

**Step 1: Import**

Paste a CSV or upload a spreadsheet:

```
email,role
john.doe@mech-sub.com,Project Member
jane.smith@mech-sub.com,Project Member
...48 more rows...
```

The import page validates emails, normalizes role names, and flags issues:
- 2 duplicate emails → deduplicated
- 1 email fails format validation → highlighted in red
- Role "project member" → auto-corrected to "Project Member"

**Step 2: Select Projects**

The project picker shows all 200+ projects. Filter by name: "Hospital". Select 12 projects. The UI shows: "50 users × 12 projects = 600 operations."

**Step 3: Preflight**

Before anything executes, the platform runs a preflight check:

```
Preflight Results:
├─ 47 users: new access (will be added)
├─ 3 users: already have access to some projects (will be skipped)
├─ 0 conflicts detected
├─ Role resolution: "Project Member" → confirmed for all 12 projects
├─ Estimated time: ~6 minutes
└─ Status: ✓ Ready to execute
```

The coordinator reviews the preflight. No surprises. Click "Execute."

**Step 4: Real-Time Progress**

The operation runs on a Cloudflare Worker. The coordinator watches progress in the browser:

```
Operation: user-add-batch
├─ Hospital Phase 1:    ████████████████████ 50/50 ✓
├─ Hospital Phase 2:    ████████████████░░░░ 38/50
├─ Hospital Phase 3:    ████████░░░░░░░░░░░░ 20/50
├─ ...
└─ ETA: 4 minutes remaining
```

The coordinator doesn't need to stay on the page. They can close the browser, go to lunch, come back, and check the result in the History page.

**Step 5: Before/After Diff**

After completion, the operation detail page shows exactly what changed:

```
john.doe@mech-sub.com
├─ Hospital Phase 1: (new) Project Member
├─ Hospital Phase 2: (new) Project Member
├─ Hospital Phase 3: (new) Project Member ← added
└─ Hospital Phase 4: already Project Member ← skipped

jane.smith@mech-sub.com
├─ Hospital Phase 1: (new) Project Member
├─ Hospital Phase 2: (failed) 403 Forbidden ← flagged
└─ ...
```

The coordinator sees the failure. Jane's email isn't in the ACC account yet — she needs to be invited first. The error is clear, actionable, and visible to the person who needs to fix it.

### Why This Matters

The RAPS CLI handles the same 600 operations. The difference: the coordinator doesn't file a ticket asking a developer to run a script. They do it themselves, in a browser, with validation, progress, and audit trail.

### Time Saved

| Method | Time | Who Does It |
|--------|------|-------------|
| ACC UI | 10 hours | Coordinator (clicking) |
| RAPS CLI | 6 minutes | Developer (scripting) |
| Rapsody Web | 8 minutes | Coordinator (self-service) |

The 2-minute difference between CLI and web is the preflight review. The 10-hour difference is the point.

## Strategy 2: Cross-Hub Data Sync — Visual Reconciliation

### The Problem (Same as RAPS)

BIM 360 account with 500 users. New ACC account. You need to reconcile users, roles, and permissions across hubs during the multi-year migration.

### The RAPS Solution (CLI)

```bash
raps admin user list "$BIM360_ACCOUNT_ID" --output csv > bim360-users.csv
raps admin user list "$ACC_ACCOUNT_ID" --output csv > acc-users.csv
comm -23 <(cut -d, -f2 bim360-users.csv | sort) <(cut -d, -f2 acc-users.csv | sort) > delta.txt
```

Effective. Requires understanding `comm`, `cut`, `sort`, and CSV column offsets.

### The Rapsody Solution (Web UI)

**The Compare Page** at `/app/bulk-user-manager/compare`:

Select two projects (or two accounts). The platform loads both user lists and shows a visual side-by-side comparison:

```
┌─────────────────────────────────────────────────────┐
│ BIM 360 Account           →    ACC Account          │
├─────────────────────────────────────────────────────┤
│ ✓ john.doe@co.com         =    john.doe@co.com      │ same role
│ ⚠ jane.smith@co.com (PM)  ≠    jane.smith@co.com (V)│ role mismatch
│ ✗ bob.wilson@co.com       →    (missing)            │ needs adding
│ ← (missing)               ✗    temp@contractor.com  │ only in ACC
└─────────────────────────────────────────────────────┘
```

**One-click reconciliation:**
- "Add missing users to ACC" → adds 200 users to cart
- "Fix role mismatches" → adds 150 role updates to cart
- "Remove departed users" → adds 50 removals to cart

Each goes through preflight before execution. The coordinator reviews the delta, picks what to sync, and executes — no shell scripting.

**The Transfer Page** at `/app/bulk-user-manager/transfer`:

For project-level transfers, select a source project and target project. See which users exist in both, which are missing. Select the users to transfer, pick a role strategy (keep same role or override), and add to cart.

### The BIM 360 Compatibility Layer

Same as RAPS — the platform auto-detects ACC vs BIM 360 and adjusts API calls transparently. The web UI doesn't even show which API version is being used. The coordinator doesn't need to know.

### Time Saved

| Method | Time | Who Does It |
|--------|------|-------------|
| Manual | 3-4 weeks | IT team + coordinators |
| RAPS CLI | 2-3 days | Developer |
| Rapsody Web | 2-3 days (same) | Developer + coordinators together |

The time is similar because reconciliation review is the bottleneck — not the tooling. But the coordinator participates directly instead of reviewing spreadsheets a developer produced.

## Strategy 3: Permission Audits — Compliance Dashboard

### The Problem (Same as RAPS)

"Who has access to what?" 3,000 users across 200 projects. 600,000 potential access combinations. Compliance needs an answer by Friday.

### The RAPS Solution (CLI)

```bash
raps admin export-permissions --account "$ACCOUNT_ID" --output csv > permissions.csv
# Diff against approved-access.csv using shell commands
# Schedule via cron
```

### The Rapsody Solution (Web Platform)

**The Compliance Page** at `/app/bulk-user-manager/compliance`:

Not a CSV export. A live compliance dashboard with rules, scores, and violations.

**Built-in compliance rules:**

| Rule | Severity | Check |
|------|----------|-------|
| Missing Company Name | warning | Users without company field set |
| High Admin Ratio | error | Projects where >30% of users are admins |
| Inactive Users With Access | warning | Users marked inactive but still in projects |
| Users Without Roles | warning | Project members with no role assigned |
| External Email Domains | info | Users outside the primary organization domain |
| Single-Project Users | info | Users in only one project (potential orphans) |

**Compliance score:**

```
Compliance Score: 72/100
├─ 3 errors (high admin ratio in 3 projects)
├─ 12 warnings (8 inactive users, 4 missing company)
├─ 47 info items (external domains, single-project users)
└─ Rules: 6 active, 0 disabled
```

**Configurable:** Disable rules that don't apply. Adjust thresholds. The settings persist.

**The Hygiene Page** at `/app/bulk-user-manager/hygiene`:

Complementary to compliance. Focuses on data quality:
- Users with no email domain
- Duplicate name detection (same person, different emails)
- Inconsistent company names across projects
- Stale users (no activity in 90+ days)

**The Duplicates Page** at `/app/bulk-user-manager/duplicates`:

Detects potential duplicate accounts:
- Same name, different emails (John Doe = john.doe@old-domain.com + jdoe@new-domain.com)
- Email variants (john.doe vs johndoe vs john.doe+work)
- Metadata mismatches (same email, different company names across projects)

Each cluster can be reviewed and dismissed or acted on.

### Scheduled Audits

The compliance check runs automatically on a schedule:

```
Schedule: Every Monday at 6:00 AM UTC
Operation: permission-export + compliance-check
Notify: Slack #acc-compliance
Last run: 2026-03-24 06:00:12 — Score: 72/100 (3 new violations)
```

No cron job to maintain. No laptop to keep running. The Cloudflare Worker fires on schedule, runs the audit, and posts the result to Slack.

### Audit History

Every operation is recorded. The **History Page** shows:

```
2026-03-25 14:30  user-add    50 items   completed   coordinator@company.com
2026-03-24 06:00  compliance  scheduled  completed   system
2026-03-23 11:15  role-update 12 items   completed   admin@company.com
2026-03-22 16:45  user-remove 8 items    completed   coordinator@company.com
```

Click any operation to see the full before/after diff, who initiated it, and the preflight results.

### Time Saved

| Method | Time | Who Does It |
|--------|------|-------------|
| Manual audit | 2 weeks | 2 compliance staff |
| RAPS CLI | 2 hours | Developer |
| Rapsody scheduled | 0 hours (automated) | Nobody (platform runs it) |

## Strategy 4: Roles and Companies — Organizational Views

### The Roles Page

Not just "who has what role" — an operational view of role distribution:

```
┌─────────────────┬───────┬──────────┬─────────────┐
│ Role            │ Users │ Projects │ Distribution │
├─────────────────┼───────┼──────────┼─────────────┤
│ Project Admin   │   47  │    23    │ ████░░░░░░  │
│ Project Manager │  123  │    45    │ ████████░░  │
│ Project Member  │  890  │   127    │ ██████████  │
│ Project Viewer  │  234  │    89    │ ██████░░░░  │
│ VDC Manager     │   31  │    12    │ ██░░░░░░░░  │
└─────────────────┴───────┴──────────┴─────────────┘
```

Click a role card to see all users with that role. Select users. **Bulk change role** — adds to cart. **Remove from projects** — adds to cart.

A project coordinator notices too many Project Admins (compliance rule flagged it). They click "Project Admin," select the users who should be downgraded, pick "Project Member" as the new role, and the cart handles the rest.

### The Companies Page

Group users by company with full CRUD actions:

- **Expand** any company to see all members
- **Select members** → Change Role, Remove from projects
- **Company metrics**: user count, project count, role distribution

The compliance team uses this to verify that all contractor users from "MechSub LLC" have been removed after contract completion. Select all, Remove, Preflight, Execute.

### The Groups Page

**Computed groups**: View users grouped by company, role, project set, or status.
**Custom groups**: Create named groups for organizational needs:

- "Electrical Team — Hospital Phase 2"
- "Temp Contractors — Q2 2026"
- "Offboarding Queue"

Add/remove members. Bulk actions on the entire group. The groups persist in localStorage (no backend needed for personal organization).

## The Offboarding Workflow

When someone leaves the company, the coordinator:

1. Opens **Offboarding** at `/app/bulk-user-manager/offboard`
2. Searches for the user
3. Selects "Remove from all projects" or picks specific projects
4. Reviews the preflight (which shows exactly which projects they'll lose access to)
5. Executes

Total time: 30 seconds. No ticket. No developer. No "did we get all 127 projects?"

## Strategy 5: The Changelog — What Changed?

For enterprise accounts with multiple administrators, the **Changelog** page shows a timeline of all completed operations:

```
Mar 25, Tue
├─ john@company.com → Hospital Phase 1    +Project Member    2h ago
├─ jane@company.com → Harbor Bridge       Project Viewer → Admin   3h ago
└─ bob@company.com  → Downtown Tower      -Removed          5h ago

Mar 24, Mon
├─ (scheduled) Permission audit completed — score 72/100
└─ 50 users added to Hospital Phase 2 by coordinator@company.com
```

Filter by time range, change type (added/removed/role change), or search by email. Every change is traceable to who made it and when.

## Under the Hood

Every strategy uses the same infrastructure:

- **raps-admin** (Rust): `AdminOperation` trait with `execute()`, `is_retryable_error()`, idempotent upserts
- **Cloudflare Workers** (WASM): Same Rust logic compiled to WASM, processing jobs from the queue
- **D1 database**: Operation state, user/project cache, preflight results
- **KV store**: Session management, preferences, subscription cache
- **Queues**: Durable job delivery between web UI and Workers

The architectural patterns are covered in depth in **Session 1258: "From CLI to Platform"**, which dissects how each layer transforms from a local CLI to a distributed cloud platform.

## Key Takeaways

1. **Automation is only valuable if the right people can use it** — a CLI that only developers run creates a developer bottleneck
2. **Self-service user management** saves the 10-hour gap between "click 600 times" and "run a script"
3. **Preflight validation** catches "wrong spreadsheet" errors before they become "wrong 400 users in wrong account" incidents
4. **Visual reconciliation** lets coordinators participate in cross-hub sync decisions instead of reviewing developer-produced spreadsheets
5. **Compliance dashboards** replace quarterly audit sprints with continuous monitoring
6. **Scheduled operations** remove the "someone needs to run this" bottleneck entirely
7. **Before/after diffs** provide the audit trail compliance teams need
8. **Offboarding workflows** ensure complete access removal in 30 seconds, not 30 minutes
9. **Custom groups** let teams organize users for their specific operational needs
10. **The ROI doubles** — same $540K/year savings, but without creating a developer bottleneck

## What's Next?

| Effort | RAPS (OSS) | Rapsody |
|--------|------------|---------|
| **Quick win** | Export permissions via CLI | Compliance dashboard — already running |
| **Medium** | Script project provisioning | Web-based project provisioning with templates |
| **High impact** | Automate BIM 360 → ACC sync | Visual Compare + one-click reconciliation |
| **Recurring** | Cron-based permission audit | Scheduled operations with Slack notifications |
| **Safety** | `--dry-run` flag | Automatic preflight on every operation |

Start with the compliance dashboard. It requires zero configuration and immediately shows your hygiene score. Everything else builds from there.

## Resources

- **Rapsody**: https://rapsody.dev
- **RAPS (OSS)**: https://github.com/dmytro-yemelianov/raps
- **Web Tools**: https://tools.rapscli.xyz
- **Documentation**: https://rapscli.xyz/docs
- **Account Admin Guide**: https://rapscli.xyz/docs/account-admin
- **Permission Audit Guide**: https://rapscli.xyz/docs/permission-audit
- **ACC Cookbook**: https://rapscli.xyz/docs/cookbook-construction
- **BIM 360 Migration**: https://rapscli.xyz/docs/bim360-migration
