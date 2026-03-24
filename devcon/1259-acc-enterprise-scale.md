# Session 1259: ACC at Enterprise Scale: Automating the Impossible

## Session Details

| Field | Value |
|-------|-------|
| **Session ID** | 1259 |
| **Title** | ACC at Enterprise Scale: Automating the Impossible |
| **Speaker(s)** | Dmytro Yemelianov |
| **Session Type** | 30-minute deep dive |
| **Status** | Complete |

## AI Pillars

- [x] **Automate** - Speed repetitive tasks, shrink cycle times, reduce errors
- [ ] Assist
- [ ] Augment

## Themes

- [ ] Sustainability
- [x] **Digital Transformation**
- [x] **System Integration**

## Target Audience

- [x] **Business Decision Makers** - Strategy, ROI, operational outcomes
- [x] **Developers/Architects** - How it's built, APIs, patterns, lessons learned

## Learning Objectives

1. Identify which ACC operations outgrow the UI at enterprise scale and benefit from programmatic automation
2. Implement strategies for bulk project creation, cross-hub data sync, and permission audits across thousands of users
3. Design resumable, idempotent automation that survives network failures and API rate limits

![ACC Enterprise Scale Hero](/devcon/images/1259-acc-enterprise-scale-hero.png)

## Abstract

Enterprise delivery teams face challenges that outgrow the UI: bulk project creation, cross-hub data sync, and permission audits across thousands of users. This session dissects real-world strategies for high-scale ACC integrations.

Not theory. Not "here's the API endpoint." Real strategies from automating accounts with 200+ projects and 10,000+ users — including the failures that shaped the approach.

We'll cover three problems that define enterprise ACC:

**Problem 1: Bulk Project Creation.** You've won a program of 40 projects. Each needs the same folder structure, the same issue types, the same checklist templates, the same user matrix. The ACC UI gives you a "Create Project" button that handles one at a time. We'll show how project templates, scripted provisioning, and idempotent upserts turn a two-week setup into a two-hour pipeline.

**Problem 2: Cross-Hub Data Sync.** Your organization has a BIM 360 account with 5 years of history and a new ACC account. Moving 500 users, their roles, and their permissions across hubs isn't a migration — it's a reconciliation. We'll walk through the strategy: export from one, transform, import to the other, handle conflicts, and verify.

**Problem 3: Permission Audits at Scale.** "Who has access to what?" sounds simple until you have 3,000 users across 200 projects, each with different folder-level permissions. Compliance needs an answer by Friday. We'll show how to export the entire permission matrix to CSV, diff it against your approved access list, and remediate discrepancies automatically.

## The Enterprise ACC Reality

Let me paint a picture that might feel familiar.

**The Setup:** A large general contractor with 200+ active construction projects. ACC is their platform of choice — they've bet big on the Autodesk ecosystem. Documents flow through ACC. Issues get tracked in ACC. Submittals, RFIs, checklists — all ACC.

**The Problem:** At this scale, manual processes can't keep up.

- 8 coordinators spend 20 hours/week on ACC administration
- New project setup takes 2-3 days of manual configuration
- User onboarding across 127 projects takes 6-10 hours per person
- The compliance team's quarterly permission audit takes two full weeks
- Nobody knows for sure which BIM 360 projects have been migrated to ACC and which haven't

**The Math:**
- 160 admin hours/week x 50 weeks = 8,000 hours/year
- At fully-loaded cost of $75/hour = **$600,000/year in administrative overhead**

**After automation:** Same work done in 10% of the time. **$540,000/year saved.** The tooling is free (open source). The implementation is measured in days, not months.

## APS Components Used

- ACC Account Admin API v2 (Projects, Users, Companies, Permissions)
- BIM 360 HQ v1 API (legacy accounts)
- Data Management API (Hubs, Projects, Folders, Items)
- ACC Issues API
- ACC Submittals API
- ACC Checklists API
- ACC RFIs API
- ACC Assets API
- OSS API (Bulk uploads)
- Model Derivative API (Batch translations)

## Autodesk Products

- Autodesk Construction Cloud (ACC)
- BIM 360 (legacy migration and mixed-account scenarios)

## Strategy 1: Bulk Project Creation from Templates

### The Problem

You've won a program of work: 40 healthcare facilities, each with the same delivery methodology, same folder structure, same issue categories, same quality checklists. The ACC UI offers "Create from Template" — one project at a time, each taking 5-10 minutes of clicking through configuration screens.

40 projects x 10 minutes = 6.5 hours. Plus another day to add users to each project with the right roles. Plus another day to deploy checklists. That's a week before anyone does actual construction management.

### The Strategy

**Step 1: Define the template once**

```bash
# List available project templates
raps template list "$ACCOUNT_ID"

# Inspect a template's configuration
raps template info "$ACCOUNT_ID" "$TEMPLATE_ID"
```

**Step 2: Script the provisioning**

```yaml
# project-matrix.yaml — defines 40 projects
name: "Healthcare Program 2026"
version: 2

variables:
  account_id: "01fb1602-2ec0-4b05-bf6e-39dc70b3ae05"
  template_id: "healthcare-standard-v3"

steps:
  - name: create-projects
    command: project create
    for_each:
      items_from: projects.csv  # facility_name, city, state, start_date
    args:
      account_id: ${account_id}
      name: "${item.facility_name} - ${item.city}"
      template_id: ${template_id}
      start_date: ${item.start_date}
    retry:
      max_attempts: 3
      backoff: exponential

  - name: add-users
    command: admin user add
    for_each:
      items_from: user-matrix.csv  # email, role
    args:
      account_id: ${account_id}
      email: ${item.email}
      role: ${item.role}
      filter: "^Healthcare Program"
    if: steps.create-projects.status == 'success'
```

```bash
# Dry-run first — always
raps pipeline run project-matrix.yaml --dry-run

# Execute
raps pipeline run project-matrix.yaml
```

**Step 3: Verify**

```bash
# List projects matching the program
raps admin project list "$ACCOUNT_ID" --filter "^Healthcare Program"

# Verify user counts per project
raps admin project list "$ACCOUNT_ID" --filter "^Healthcare Program" --output json | \
  jq '.[] | {name: .name, members: .member_count}'
```

### Why This Works at Scale

**Idempotent upserts:** If a project already exists with the same name, the operation skips it. You can re-run the pipeline after a failure without creating duplicates.

**Resumable state:** RAPS persists operation state to disk. If your laptop loses WiFi at project 23 of 40, `raps admin operation resume` picks up at project 24.

**Template drift protection:** By scripting from a template ID, every project gets the same configuration. No manual deviation. No "I forgot to add the quality checklist template to this one."

### Time Saved

Manual: 5 days (project creation + user assignment + verification)
Automated: 2 hours (write the matrix, dry-run, execute, verify)

## Strategy 2: Cross-Hub Data Sync (BIM 360 → ACC Migration)

### The Problem

Your organization adopted BIM 360 in 2019. You have 5 years of projects, 500 users, and a complex permission matrix. Now you're migrating to ACC. Autodesk's built-in migration handles projects and documents, but user provisioning and permissions? That's on you.

The challenge isn't moving data. It's **reconciliation**:
- 200 users exist in BIM 360 but haven't been invited to ACC yet
- 150 users have different roles in BIM 360 vs ACC
- 50 users left the company but are still active in BIM 360
- Company assignments don't match between platforms

### The Strategy

**Step 1: Export the source of truth**

```bash
# Export BIM 360 user list (auto-detects BIM 360 vs ACC)
raps admin user list "$BIM360_ACCOUNT_ID" --output csv > bim360-users.csv

# Export ACC user list
raps admin user list "$ACC_ACCOUNT_ID" --output csv > acc-users.csv

# Export BIM 360 permissions
raps admin export-permissions --account "$BIM360_ACCOUNT_ID" --output bim360-perms.csv

# Export ACC permissions
raps admin export-permissions --account "$ACC_ACCOUNT_ID" --output acc-perms.csv
```

**Step 2: Compute the delta**

This is where a script (or an AI assistant) shines. Compare the two exports:

```bash
# Humans in BIM 360 but not ACC → need inviting
comm -23 <(cut -d, -f2 bim360-users.csv | sort) \
         <(cut -d, -f2 acc-users.csv | sort) > users-to-invite.txt

# Humans in both but with different roles → need reconciliation
# (this is where you involve project leads for decisions)
```

**Step 3: Execute the sync**

```bash
# Invite missing users to ACC
while read -r email; do
  raps admin user create "$ACC_ACCOUNT_ID" "$email"
done < users-to-invite.txt

# Add users to projects with correct roles
raps admin user add "$ACC_ACCOUNT_ID" "user@company.com" \
  --role project_admin \
  --dry-run  # ALWAYS dry-run first
```

**Step 4: Clone permissions for complex cases**

```bash
# Clone one user's exact project memberships and folder permissions to another
raps admin clone-permissions \
  --from "senior.pm@company.com" \
  --to "new.pm@company.com"
```

### The BIM 360 Compatibility Layer

RAPS auto-detects whether an account is ACC or BIM 360 and adjusts the API calls transparently. ACC uses Admin API v2 endpoints. BIM 360 uses HQ v1 endpoints. The response formats, pagination patterns, and role naming conventions are different. RAPS normalizes all of it:

```bash
# Same command, different platforms — RAPS handles the difference
raps admin user list "$ACC_ACCOUNT_ID"        # → ACC Admin v2
raps admin user list "$BIM360_ACCOUNT_ID"     # → HQ v1 (auto-detected)

# Role names normalized: "Project Admin" works on both
raps admin user add "$ACCOUNT_ID" "user@co.com" --role "Project Admin"
```

This matters because most enterprise accounts have **both** ACC and BIM 360 projects during the multi-year migration window. You can't write separate scripts for each platform.

### Why This Is Hard

**Email matching isn't enough.** Users may have different email addresses across platforms (personal vs corporate, old domain vs new domain). You need fuzzy matching and manual review for edge cases.

**Role semantics differ.** BIM 360's "Document Management" role maps to ACC's "Project Admin" for some operations but not others. Document the mapping decisions.

**Timing matters.** Don't sync on Friday afternoon. Do it Monday morning when IT is available to handle the "I can't access my project" tickets.

### Time Saved

Manual migration of 500 users across 200 projects: 3-4 weeks
Scripted with validation and dry-run: 2-3 days (mostly the reconciliation review)

## Strategy 3: Permission Audits at Scale

### The Problem

Compliance asks: "Who has access to the Downtown Tower project?" You open ACC, navigate to the project, click Members, and start scrolling. 47 members. You copy names into a spreadsheet. Then they ask about the 199 other projects.

Or worse: "Prove that former employees no longer have access to any project." You have 3,000 users and 200 projects. That's 600,000 potential access combinations to verify.

### The Strategy

**Step 1: Export the entire permission matrix**

```bash
# Export every user's project memberships and folder permissions
raps admin export-permissions \
  --account "$ACCOUNT_ID" \
  --output permissions-$(date +%Y%m%d).csv
```

This produces a CSV with columns: `user_email, project_name, project_role, folder_name, folder_permission`. One row per user-project-folder combination. For an account with 3,000 users and 200 projects, expect ~50,000 rows.

**Step 2: Diff against the approved access list**

Every enterprise should have an approved access matrix — which roles are authorized for which projects. Compare:

```bash
# Find users with access who shouldn't have it
comm -23 \
  <(cut -d, -f1,2 permissions-20260415.csv | sort) \
  <(cut -d, -f1,2 approved-access.csv | sort) > unauthorized-access.csv

# Find users who should have access but don't
comm -13 \
  <(cut -d, -f1,2 permissions-20260415.csv | sort) \
  <(cut -d, -f1,2 approved-access.csv | sort) > missing-access.csv
```

**Step 3: Remediate automatically**

```bash
# Remove unauthorized access (dry-run first!)
while IFS=, read -r email project; do
  raps admin user remove "$ACCOUNT_ID" "$email" --filter "$project" --dry-run
done < unauthorized-access.csv

# Grant missing access
while IFS=, read -r email project role; do
  raps admin user add "$ACCOUNT_ID" "$email" --role "$role" --filter "$project" --dry-run
done < missing-access.csv
```

**Step 4: Generate the audit report**

```bash
# Before/after comparison
raps admin export-permissions --account "$ACCOUNT_ID" --output permissions-after.csv

diff permissions-$(date +%Y%m%d).csv permissions-after.csv > audit-changes.diff
```

### Scheduling Recurring Audits

The real power is running this automatically:

```yaml
# weekly-audit.yaml
name: permission-audit
version: 2

steps:
  - name: export
    command: admin export-permissions --account ${ACCOUNT_ID}
    timeout: 30m

  - name: notify
    command: "!curl -X POST $SLACK_WEBHOOK -d '{\"text\": \"Permission audit complete. Review: permissions.csv\"}'"
    if: steps.export.status == 'success'
```

```bash
# Run weekly via CI/CD or cron
raps pipeline run weekly-audit.yaml
```

### The Safeguard Layer

Permission changes are irreversible in the APS API. There's no "undo" for removing a user from 200 projects. Before any destructive operation:

```bash
# Generate a rollback script before bulk removal
raps safeguard backup "admin user remove $ACCOUNT_ID former@company.com"
# Creates: rollback-20260415-143022.sh
# Contains: exact commands to re-add the user with original roles

# Now execute with confidence
raps admin user remove "$ACCOUNT_ID" "former@company.com"

# If something goes wrong:
bash rollback-20260415-143022.sh
```

32 destructive operations are covered. Every generated script includes `set -euo pipefail`, inline comments, and the original command as documentation.

### Time Saved

Manual quarterly audit: 2 weeks (2 people x 5 days)
Automated with export-permissions: 2 hours (export, diff, review, remediate)

## Strategy 4: Bulk Issue and RFI Management

At enterprise scale, issues and RFIs aren't just project-level concerns — they're portfolio-level metrics.

### Cross-Project Reporting

```bash
# Generate portfolio-wide issue summary
raps report issues-summary "$ACCOUNT_ID"
# ┌─────────────────────┬──────┬──────┬────────┬─────────┐
# │ Project             │ Open │ Closed│ Overdue │ Avg Days│
# ├─────────────────────┼──────┼──────┼────────┼─────────┤
# │ Downtown Tower      │  47  │  203 │    8   │   12.3  │
# │ Harbor Bridge       │  23  │  156 │    2   │    8.7  │
# │ Hospital Phase 2    │  89  │   67 │   31   │   18.2  │
# └─────────────────────┴──────┴──────┴────────┴─────────┘

# RFI summary across all projects
raps report rfi-summary "$ACCOUNT_ID"
```

### Bulk Issue Creation from Clash Reports

```bash
# Import clashes as issues from a structured CSV
while IFS=, read -r title description location priority; do
  raps issue create "$PROJECT_ID" \
    --title "$title" \
    --description "$description"
done < clash-report.csv

echo "Created $(wc -l < clash-report.csv) issues"
```

47 issues x 2 minutes each = 94 minutes manually. 10 seconds with automation.

### Standardized Checklists at Scale

```bash
# Deploy inspection checklists for a 50-story building
for floor in {1..50}; do
  for zone in "North" "South" "East" "West"; do
    raps acc checklist create "$PROJECT_ID" \
      --title "MEP Rough-In - Level $floor $zone" \
      --template-id "$TEMPLATE_ID" \
      --location "Level $floor, $zone Zone"
  done
done
# Created 200 checklists in under 5 minutes
```

## Under the Hood: Resilience & Output

Every strategy above relies on infrastructure patterns — rate-limit-aware concurrency, resumable operations, dry-run previews, and structured output (JSON, CSV, NDJSON) for integration with ERP, BI, and notification systems. These architectural decisions are covered in depth in **Session 1258: "Zero to Production"**, which dissects the five layers that make bulk APS automation survive at enterprise scale.

## Key Takeaways

1. **UI doesn't scale** — at 200+ projects, clicking is not a strategy
2. **Bulk project creation from templates** turns weeks of setup into hours with idempotent, resumable pipelines
3. **Cross-hub data sync** between BIM 360 and ACC requires reconciliation, not just migration — export, diff, transform, import
4. **Permission audits** at scale are solvable: export the matrix, diff against approved access, remediate automatically
5. **The BIM 360 compatibility layer** means one set of scripts works across mixed accounts during the multi-year migration
6. **Safeguard rollback scripts** provide an undo for APIs that don't have one
7. **The ROI is 10x** — $600K/year in admin overhead becomes $60K/year with automation

## What's Next?

Start with the highest-impact automation:

- **Quick win:** Export permissions to CSV for your next compliance review
- **Medium effort:** Script new project provisioning from templates
- **High impact:** Automate the BIM 360 → ACC user migration
- **Recurring value:** Schedule weekly permission audits via CI/CD
- **Safety net:** Add safeguard backup scripts before any bulk operation

Start small. Prove value. Scale up.

## Resources

- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **Documentation**: https://rapscli.xyz/docs
- **Account Admin Guide**: https://rapscli.xyz/docs/account-admin
- **Permission Audit Guide**: https://rapscli.xyz/docs/permission-audit
- **Pipeline Guide**: https://rapscli.xyz/docs/pipelines
- **ACC Cookbook**: https://rapscli.xyz/docs/cookbook-construction
- **BIM 360 Migration**: https://rapscli.xyz/docs/bim360-migration
