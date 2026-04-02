---
title: "RAPS 5.7: Safeguard — Rollback and Backup Script Generators for APS Operations"
description: "RAPS 5.7 introduces raps safeguard, generating executable rollback and backup shell scripts for 32 destructive APS operations — providing recovery paths for bucket deletions, bulk user changes, webhook modifications, and more."
type: "release"
publishDate: 2026-03-14
status: "draft"
---

# FOR IMMEDIATE RELEASE

## RAPS 5.7: Safeguard — Rollback and Backup Script Generators for APS Operations

*Open-source APS CLI adds automated recovery script generation for 32 destructive operations, covering buckets, objects, webhooks, projects, admin users, issues, RFIs, templates, and folder permissions*

---

**Version Information**
- **Current Version**: 5.7.0
- **APS API Coverage**: Authentication v2, Data Management v1, Model Derivative v2, OSS v2, Design Automation v3, Construction Cloud v1, Webhooks, Account Admin
- **Architecture**: 10 Rust workspace crates
- **License**: Apache-2.0

---

The Autodesk Platform Services API provides no built-in undo mechanism. Bucket deletions are permanent. User removals from projects are immediate. Folder permission overwrites discard the previous configuration without backup. For enterprise teams automating operations across hundreds of projects, a single mistake can cascade through an entire account with no recovery path.

RAPS 5.7 solves this with `raps safeguard` — a command that generates executable shell scripts to either capture current state before a destructive operation (backup) or reverse an operation after it executes (rollback).

### What's New in 5.7.0

**Backup Script Generation**

Before running any destructive operation, generate a backup script that captures the current state:

```bash
raps safeguard backup "bucket delete my-models"
```

The generated script downloads all objects, saves bucket metadata as JSON, and takes a snapshot manifest with SHA1 hashes — a complete recovery package that can restore the bucket to its pre-deletion state.

**Rollback Script Generation**

After executing an operation, generate a script containing the inverse commands:

```bash
raps safeguard rollback "admin user add --email jane@co.com --project-id wrong-project"
```

This produces a script that removes the erroneously added user, using the same email and project ID from the original command.

**32 Operations Covered**

Safeguard covers every major APS domain:

- **Storage**: Bucket create/delete, object upload/delete/copy, directory sync
- **Construction**: Project create/update/archive, admin user add/remove/update/import, folder permission management
- **Collaboration**: Issue create/update, RFI create/update, template create/update/archive
- **Compute**: Webhook create/delete/update, Design Automation workitem create, Reality Capture photoscene delete, model translation
- **System**: Config set, pipeline run

**Production-Grade Scripts**

Every generated script follows engineering standards:

- `set -euo pipefail` — fails on any error instead of continuing silently
- Inline comments explaining each step and its purpose
- Original command preserved as documentation
- Timestamped filenames for audit traceability
- Executable permissions set automatically (`chmod +x`)
- Only `raps` commands used — no external dependencies beyond a standard shell

**CI/CD Integration**

Safeguard fits into automated pipelines as a pre-step before destructive operations:

```yaml
- name: Backup before sync
  run: |
    raps safeguard backup "sync ./dist my-bucket" --out-file backup.sh
    bash backup.sh
- name: Sync to bucket
  run: raps sync ./dist my-bucket
```

If the pipeline fails mid-execution, the backup script provides a one-command recovery path.

### Availability

RAPS 5.7.0 is available immediately:

```bash
cargo install raps
raps safeguard list
```

Full documentation: [rapscli.xyz/docs/safeguard](https://rapscli.xyz/docs/safeguard)
GitHub: [github.com/dmytro-yemelianov/raps](https://github.com/dmytro-yemelianov/raps)

### Technical Specifications

- **32** reversible operations with backup and rollback strategies
- **Zero runtime dependencies** — generated scripts use only `raps` and standard shell utilities
- **Longest-prefix matching** — correctly dispatches `admin user add` vs `admin user update` vs `admin user import`
- **11 unit tests** covering command parsing, operation matching, and script generation
- **Machine-readable output** — `--output json` for integration with external tooling

---

**About RAPS**

RAPS (Rust Autodesk Platform Services) is the open-source CLI and automation toolkit for the Autodesk Platform Services API ecosystem. Built in Rust with 10 workspace crates, it provides 195+ CLI operations across 51 command families, 114 MCP tools for AI assistant integration, pipeline orchestration, and enterprise-grade account administration. Used by AEC teams worldwide for bulk user management, model translation workflows, and CI/CD automation.

**Contact**: Dmytro Yemelianov — [rapscli.xyz](https://rapscli.xyz)
