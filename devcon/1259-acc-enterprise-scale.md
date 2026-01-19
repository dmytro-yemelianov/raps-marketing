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

1. Understand the challenges of managing ACC at enterprise scale (100+ projects, 10,000+ files)
2. Learn automation patterns for bulk operations: issues, submittals, checklists, and file management
3. Discover how to integrate ACC workflows with enterprise systems using scriptable CLI tools

![ACC Enterprise Scale Hero](/devcon/images/1259-acc-enterprise-scale-hero.png)

## Abstract

There's a moment in every enterprise ACC deployment when someone realizes the math doesn't work.

You have 200 active projects. Each project needs issues tracked, submittals managed, checklists completed, RFIs answered. The project management team has 8 people. Even if each person spends just 15 minutes per project per week on administrative tasks, that's 500 hours of clicking—every week.

This session is about breaking that math.

We'll demonstrate automation patterns that transform hours of manual work into seconds of scripted operations. Not theoretical patterns—real commands you can run today. Creating 50 issues across 10 projects? One script. Exporting all open RFIs to a CSV for your Monday meeting? One command. Deploying standardized checklists from templates? Done before your coffee gets cold.

The tools are open source. The patterns are proven. The only question is: how much time are you willing to save?

## The Enterprise ACC Reality

Let me paint a picture that might feel familiar.

**The Setup:** A large general contractor with 200+ active construction projects. ACC is their platform of choice—they've bet big on the Autodesk ecosystem. Documents flow through ACC. Issues get tracked in ACC. Submittals, RFIs, checklists—all ACC.

**The Problem:** Scale breaks everything.

- The BIM team uploads 500 models per month. Each needs translation for viewing.
- The quality team creates 2,000 checklists per month from standardized templates.
- The project controls group tracks 10,000+ open issues across all projects.
- Leadership wants weekly reports aggregating data across the entire portfolio.

**The Current State:** A small army of coordinators clicking through the ACC UI, copying data into spreadsheets, manually creating issues one at a time. It's unsustainable. People burn out. Data gets stale. Reports are always "as of last Tuesday."

**The Question:** What if we could automate 80% of this?

## APS Components Used

- Data Management API (Hubs, Projects, Folders, Items)
- ACC Issues API (Issues, Comments, Attachments, Transitions)
- ACC Submittals API
- ACC Checklists API
- ACC RFIs API
- ACC Assets API
- **ACC Account Admin API (v4.0+)** - Bulk user management, folder permissions
- OSS API (Bulk uploads)
- Model Derivative API (Batch translations)

## Autodesk Products

- Autodesk Construction Cloud (ACC)
- BIM 360 (legacy migration scenarios)

## Pattern 1: Issue Management at Scale

Issues are the heartbeat of construction project management. Clashes identified, RFIs needed, defects logged—they all become issues. At enterprise scale, you might have tens of thousands of open issues across your portfolio.

### The Commands

```bash
# List all issues in a project
raps issue list abc123-project-id
# Returns: ID, title, status, assignee, due date, created date

# Filter to just open issues
raps issue list abc123-project-id --status open

# Create an issue programmatically
raps issue create abc123-project-id \
  --title "Structural clash at Level 3 - Grid C7" \
  --description "HVAC duct conflicts with beam B-12. Coordination required."
```

### The Real-World Use Case

**Scenario:** Your clash detection software identifies 47 clashes in the latest model coordination. Instead of manually creating 47 issues in the ACC UI (click, type, click, type, repeat), you export the clash report to CSV and run a script:

```bash
#!/bin/bash
PROJECT_ID="abc123-project-id"

while IFS=, read -r title description location; do
  raps issue create "$PROJECT_ID" \
    --title "$title" \
    --description "$description"
done < clash-report.csv

echo "Created $(wc -l < clash-report.csv) issues"
```

**Time saved:** 47 issues × 2 minutes each = 94 minutes → 10 seconds.

### Issue Lifecycle Management

Issues aren't just created—they move through a lifecycle:

```bash
# View available issue types (categories) in the project
raps issue types abc123-project-id
# Shows: Clash, Defect, RFI Needed, Safety, etc.

# Update an issue
raps issue update abc123-project-id issue-id-123 \
  --status "in_review"

# Add a comment
raps issue comment add abc123-project-id issue-id-123 \
  --body "Design team has proposed a solution. See attached sketch."

# Transition to a new status
raps issue transition abc123-project-id issue-id-123 \
  --to answered
```

## Pattern 2: Submittals Workflow

Submittals are the formal dance between contractors and design teams. Shop drawings submitted, reviewed, approved or rejected, resubmitted. At scale, this process generates enormous administrative overhead.

### The Commands

```bash
# List all submittals in a project
raps acc submittal list abc123-project-id

# Get details on a specific submittal
raps acc submittal get abc123-project-id submittal-id-456

# Create a new submittal
raps acc submittal create abc123-project-id \
  --title "Curtain Wall Shop Drawings - Revision 2" \
  --spec-section "08 44 00" \
  --due-date "2026-05-15"

# Update status after review
raps acc submittal update abc123-project-id submittal-id-456 \
  --status approved
```

### The Real-World Use Case

**Scenario:** At project kickoff, you need to create the standard set of 120 submittals from your company's master list. This is typically a week of data entry.

With automation:
```bash
#!/bin/bash
PROJECT_ID="new-project-id"

# Read from your master submittal list
while IFS=, read -r title spec_section days_until_due; do
  due_date=$(date -d "+${days_until_due} days" +%Y-%m-%d)
  raps acc submittal create "$PROJECT_ID" \
    --title "$title" \
    --spec-section "$spec_section" \
    --due-date "$due_date"
done < master-submittal-list.csv
```

**Time saved:** One week → 30 minutes (including review).

## Pattern 3: Checklists at Scale

Quality checklists are the backbone of construction quality assurance. Inspection checklists, safety checklists, commissioning checklists—each needs to be created, assigned, completed, and documented.

### The Commands

```bash
# List available checklist templates
raps acc checklist templates abc123-project-id
# Returns: Template ID, name, description, item count

# Create a checklist from a template
raps acc checklist create abc123-project-id \
  --title "Level 5 MEP Rough-In Inspection" \
  --template-id template-789 \
  --location "Building A, Level 5, Zones 1-4" \
  --due-date "2026-04-20" \
  --assignee-id user-id-inspector

# List all checklists
raps acc checklist list abc123-project-id

# Get checklist details
raps acc checklist get abc123-project-id checklist-id-101

# Update status
raps acc checklist update abc123-project-id checklist-id-101 \
  --status completed
```

### The Real-World Use Case

**Scenario:** Your 50-story tower project requires MEP rough-in inspections for every floor, every zone. That's 200 checklists just for this one inspection type. The quality team was going to spend two days creating them manually.

```bash
#!/bin/bash
PROJECT_ID="tower-project-id"
TEMPLATE_ID="mep-roughin-template"

for floor in {1..50}; do
  for zone in "North" "South" "East" "West"; do
    raps acc checklist create "$PROJECT_ID" \
      --title "MEP Rough-In - Level $floor $zone" \
      --template-id "$TEMPLATE_ID" \
      --location "Level $floor, $zone Zone"
  done
done

echo "Created 200 checklists"
```

**Time saved:** 2 days → 5 minutes.

## Pattern 4: RFI Automation

RFIs (Requests for Information) are the formal questions that get asked when drawings are unclear. They're also a major source of project delays—every day an RFI sits unanswered is potentially a day of construction delay.

### The Commands

```bash
# List RFIs in a project
raps rfi list abc123-project-id

# Get RFI details
raps rfi get abc123-project-id rfi-id-202

# Create a new RFI
raps rfi create abc123-project-id \
  --title "Clarification needed: Foundation depth at Grid C-7"

# Answer an RFI
raps rfi update abc123-project-id rfi-id-202 \
  --status answered
```

### The Real-World Use Case

**Scenario:** Monday morning portfolio review. Leadership wants to know: how many RFIs are overdue across all 200 projects?

```bash
#!/bin/bash

echo "Overdue RFIs by Project" > rfi-report.csv

for project_id in $(cat project-ids.txt); do
  overdue=$(raps rfi list "$project_id" --output json | \
    jq '[.[] | select(.status != "answered" and .due_date < now)] | length')
  echo "$project_id,$overdue" >> rfi-report.csv
done
```

The report that used to take someone all morning? Runs automatically at 6 AM, emailed to leadership before they finish their coffee.

## Pattern 5: Asset Management

Assets are the physical things that get installed and need to be tracked: equipment, fixtures, systems. ACC's Asset module lets you track them from specification through installation to operations.

### The Commands

```bash
# List assets in a project
raps acc asset list abc123-project-id

# Get asset details
raps acc asset get abc123-project-id asset-id-303

# Create an asset
raps acc asset create abc123-project-id \
  --description "AHU-01 Air Handling Unit - Mechanical Penthouse" \
  --barcode "AHU-001-2026" \
  --category-id hvac-equipment-category

# Update asset status
raps acc asset update abc123-project-id asset-id-303 \
  --status-id installed
```

### The Real-World Use Case

**Scenario:** The equipment schedule shows 450 pieces of mechanical equipment arriving over the next 6 months. Each needs an asset record in ACC.

You could have someone type 450 records. Or:

```bash
#!/bin/bash
PROJECT_ID="hospital-project-id"

while IFS=, read -r description barcode category; do
  raps acc asset create "$PROJECT_ID" \
    --description "$description" \
    --barcode "$barcode" \
    --category-id "$category"
done < equipment-schedule.csv
```

## Pattern 6: Bulk File Operations

At enterprise scale, file operations compound quickly. 500 models per month means 500 uploads, 500 translations, 500 quality checks.

### Parallel Uploads

```bash
# Upload multiple files in parallel (8 concurrent uploads)
raps object upload-batch my-bucket *.rvt *.nwd --parallel 8
# Uploading 47 files to bucket 'my-bucket' with 8 parallel uploads
# ✓ hospital-L1.rvt (145 MB)
# ✓ hospital-L2.rvt (152 MB)
# ...
# Total: 47 uploaded, 0 failed
# Total size: 6.2 GB
# Time: 4 minutes 32 seconds
```

Sequential uploads: ~45 minutes. Parallel uploads: ~5 minutes.

### Output Formats for Integration

Every command supports multiple output formats, making integration with other systems trivial:

```bash
# JSON for processing with jq or Python
raps issue list abc123-project-id --output json

# CSV for Excel or database import
raps issue list abc123-project-id --output csv > issues.csv

# YAML for configuration management
raps acc checklist list abc123-project-id --output yaml
```

## Pattern 7: Pipeline Automation

For complex multi-step workflows, individual commands aren't enough. raps supports YAML-based pipelines that orchestrate multiple operations with error handling and conditional logic.

```bash
# Run a pipeline
raps pipeline run weekly-report.yaml

# Validate without executing (dry run)
raps pipeline run weekly-report.yaml --dry-run

# Generate sample pipeline templates
raps pipeline sample
```

### What Pipelines Enable

- **Sequential dependencies:** Step 2 only runs if Step 1 succeeds
- **Variable substitution:** `${PROJECT_ID}` gets replaced at runtime
- **Continue-on-error:** One failure doesn't stop the whole pipeline
- **Conditional execution:** Skip steps based on previous results

This is how you build reliable automation that runs unattended—overnight batch jobs, scheduled reports, triggered workflows.

## Pattern 8: Bulk User Management (NEW in v4.0)

![Bulk Operations](/devcon/images/1259-acc-enterprise-scale-bulk-ops.png)

This one came from real pain. A client called me because they'd spent two full days adding a new hire to their 180 projects. Click, search, assign, repeat. Their IT guy was ready to quit.

### The Problem

> "We just hired a new BIM manager who needs project admin access to all 127 active projects."

With the ACC web interface, you'd need to:
1. Navigate to each project
2. Open the Members panel
3. Search for the user
4. Assign the role
5. **Repeat 127 times**

I timed it once: 3-5 minutes per project if you're fast. That's 6-10 hours of your life you're not getting back.

### The Solution

```bash
# Add user to ALL projects as project admin
raps admin user add "$ACCOUNT_ID" "new.bim.manager@company.com" \
  --role project_admin

# Preview first with dry-run (learned this the hard way)
raps admin user add "$ACCOUNT_ID" "new.bim.manager@company.com" \
  --role project_admin \
  --dry-run

# Filter to only active projects matching a pattern
raps admin user add "$ACCOUNT_ID" "new.bim.manager@company.com" \
  --role project_admin \
  --filter "^2026-"
```

**Result:** 127 projects updated in under 2 minutes. The IT guy didn't quit.

### User Offboarding

When someone leaves the company:

```bash
# Remove user from ALL projects
raps admin user remove "$ACCOUNT_ID" "former.employee@company.com"
```

No more discovering six months later that a departed employee still has access to sensitive project data.

### Role Updates

Promoting someone from viewer to admin?

```bash
# Update role across all projects
raps admin user update-role "$ACCOUNT_ID" "promoted.user@company.com" \
  --role project_admin
```

### Folder Permissions at Scale

Need to update permissions on Project Files folders across your entire portfolio?

```bash
# Update folder permissions for user across all projects
raps admin folder rights "$ACCOUNT_ID" "user@company.com" \
  --folder-type "Project Files" \
  --permission edit
```

### Resumable Operations

Network hiccup? Rate limited? No problem. RAPS saves operation state automatically:

```bash
# Resume from where you left off
raps admin operation resume

# Check operation status
raps admin operation status

# List all operations
raps admin operation list
```

### Built for Enterprise

- **Parallel processing:** Up to 50 concurrent API requests
- **Smart retry:** Exponential backoff handles rate limits automatically
- **Resumable state:** Operations can be interrupted and resumed
- **Dry-run mode:** Preview exactly what will happen before executing
- **Progress tracking:** Real-time progress bars with ETA

## The Integration Story

Everything we've shown today produces structured output. That means integration with enterprise systems is straightforward:

**ERP Integration:** Export issue counts and submittal status to SAP or Oracle for cost tracking.

**BI Dashboards:** Feed issue trends into Power BI or Tableau for executive dashboards.

**Custom Applications:** Use JSON output as input to your internal tools.

**Notification Systems:** Pipe results to Slack, Teams, or email via simple scripts.

The CLI becomes a bridge between ACC and everything else in your enterprise.

## The ROI Conversation

![Time Savings](/devcon/images/1259-acc-enterprise-scale-time-savings.png)

Let's talk numbers that matter to decision makers.

**Before automation:**
- 8 coordinators spending 20 hours/week on ACC administration
- 160 hours/week × 50 weeks = 8,000 hours/year
- At fully-loaded cost of $75/hour = **$600,000/year in administrative overhead**

**After automation:**
- Same work done in 10% of the time
- 800 hours/year instead of 8,000
- Savings: **$540,000/year**
- Plus: data is always current, reports are always fresh, humans focus on judgment calls

The tooling is free (open source). The implementation is measured in days, not months. The ROI is measured in multiples, not percentages.

## Key Takeaways

![ACC Module Coverage](/devcon/images/1259-acc-enterprise-scale-acc-modules.png)

1. **Manual doesn't scale**—at enterprise volume, clicking is not a strategy
2. **raps CLI provides comprehensive ACC API coverage**: Issues, Submittals, Checklists, RFIs, Assets, **and Account Admin**
3. **Bulk user management (v4.0+)** transforms 6-10 hours of clicking into 2 minutes
4. **Multiple output formats (JSON, CSV, YAML)** enable integration with any system
5. **Parallel operations** (batch uploads, bulk user management) dramatically reduce processing time
6. **Resumable operations** mean network issues don't restart your 200-project operation
7. **Pipeline automation** enables complex, reliable workflows that run unattended
8. **The patterns are reusable**—what works on one project works on 200 projects

## What's Next?

This session showed you the tools. The next step is identifying your highest-impact automation opportunities:

- **Quick win:** Export all open issues to CSV for your next project review
- **Medium effort:** Automate weekly reporting across your portfolio
- **High impact:** Use bulk user management for onboarding/offboarding
- **Strategic investment:** Build pipelines that create standardized project setups

Start small. Prove value. Scale up.

## Resources

- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **Documentation**: https://rapscli.xyz/docs
- **Account Admin Guide**: https://rapscli.xyz/docs/account-admin
- **ACC Cookbook**: https://rapscli.xyz/docs/cookbook-construction
- **Pipeline Guide**: https://rapscli.xyz/docs/pipelines
- **Issue Commands**: https://rapscli.xyz/docs/cookbook-acc-issues
- **Checklist Guide**: https://rapscli.xyz/docs/cookbook-acc-checklists
