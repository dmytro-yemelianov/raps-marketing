---
title: "RAPS 5.3: Comprehensive Test Coverage Suite and Interactive Coverage Dashboard"
description: "RAPS 5.3 brings 25+ new scenario tests across RFI, DA, admin operations, and object commands using raps-mock, plus an interactive HTML coverage dashboard with animated gauges and per-module drill-down."
type: "release"
publishDate: 2026-03-06
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.3: Comprehensive Test Coverage Suite and Interactive Coverage Dashboard

*Open-source APS CLI adds 25+ mock scenario tests for RFI CRUD, Design Automation, admin operations, and object storage — plus an animated HTML dashboard for visualizing test coverage*

---

**Version Information**
- **Current Version**: 5.3.0
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates
- **License**: Apache-2.0

---

Software teams building on the Autodesk Platform Services API face a recurring challenge: testing CLI tools that require live credentials. RAPS 5.3 solves this with a major expansion of the raps-mock scenario test suite — 25+ new tests covering RFI CRUD operations, Design Automation activities, appbundles and work items, admin bulk operations, object copy/rename, and config context management. No real APS credentials needed.

### What's New in 5.3.0

**RFI Scenario Tests — 81% Line Coverage**

The construction RFI module now has comprehensive scenario coverage across all five CRUD operations. Tests exercise JSON and table output, status filtering, since-date filtering, CSV bulk import with validation, and error paths for nonexistent resources — all against the raps-mock server using `RAPS_FORCE_TOKEN` to bypass 3-legged OAuth.

```bash
rfi list <project> --output json
rfi get <project> <rfi-id> --output table
rfi create <project> --title "My RFI" --output json
rfi create <project> --from-csv rfis.csv
rfi update <project> <rfi-id> --status open --output table
rfi delete <project> <rfi-id>
```

**Admin Operations Scenario Tests — 53% Line Coverage**

The `admin operation` subcommands (list, status, resume, cancel) are tested with an isolated HOME tempdir approach — no APS credentials required because the StateManager is purely file-based. Tests cover empty state, filter flags, YAML output, and graceful failure for unknown operation IDs.

**Design Automation Coverage**

DA activities (65%), appbundles (50%), and work items (44%) now have scenario tests covering list/create/delete round-trips, JSON file inputs, missing-field validation, and qualified/unqualified alias resolution. Wait/polling paths that require a live DA compute cluster are documented as requiring live API and excluded from mock tests.

**Object Copy/Rename Scenario Tests — 40% Line Coverage**

Batch-copy and batch-rename operations are tested against error paths: copying from an empty bucket, renaming with no pattern matches, argument validation failures, and nonexistent source objects. Full upload round-trips are excluded due to a known clap positional arg assertion in debug mode.

**Interactive Coverage Dashboard**

A new HTML dashboard at `docs/coverage-report.html` visualizes test coverage across all 40+ source files:

- SVG arc gauges with animated count-up for overall line (25.4%) and function (35.9%) coverage
- Tier filter cards (≥80%, 60-79%, 40-59%, etc.) with live filtering
- Search by filename or module
- Collapsible module sections with mini progress bars
- Per-file animated line and function coverage bars
- Dark terminal aesthetic with amber accents and JetBrains Mono

**WORKFLOW.md Coverage Policy**

A new `WORKFLOW.md` at the repository root documents the 10-file priority list, 40% coverage threshold, and 5-step agent workflow for systematically expanding test coverage in future sessions.

### Coverage Impact

| Module | Before | After | Method |
|--------|--------|-------|--------|
| `commands/rfi/crud.rs` | 0% | 81% | raps-mock scenario tests |
| `commands/admin/operations.rs` | 0% | 53% | isolated HOME tempdir |
| `commands/da/activities.rs` | 0% | 65% | raps-mock scenario tests |
| `commands/da/appbundles.rs` | 0% | 50% | raps-mock scenario tests |
| `commands/da/workitems.rs` | 0% | 44% | raps-mock scenario tests |
| `commands/object/copy.rs` | 0% | 40% | error path scenario tests |
| `commands/config/context.rs` | 0% | 75% | round-trip scenario tests |

### Availability

Install or upgrade via npm:

```bash
npm install -g @rapscli/raps
```

Or via the install script:

```bash
curl -fsSL https://rapscli.xyz/install.sh | bash
```

Source and binaries available at github.com/dmytro-yemelianov/raps.

### About RAPS

RAPS (Rust Autodesk Platform Services CLI) is an open-source command-line interface for the Autodesk Platform Services API, built in Rust. It covers authentication, object storage, model translation, design automation, construction management, and MCP server integration in a single binary. RAPS is licensed under Apache-2.0 and available on macOS, Linux, and Windows.
