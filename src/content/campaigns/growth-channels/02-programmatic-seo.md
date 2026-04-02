# Programmatic SEO — Pain-Point Landing Pages

> Capture search intent from AEC teams Googling their exact problems.
> Each page = one ACC pain point + how RAPS solves it + terminal demo.
> Target: 30 pages → long-tail organic traffic within 60-90 days.

---

## Strategy

**Pattern**: `rapscli.xyz/solutions/{slug}`

Each page follows the same template:
1. **The Problem** — what hurts, who it affects, how much time it wastes
2. **The Manual Way** — screenshots/description of the painful web UI workflow
3. **The RAPS Way** — terminal command + output, time comparison
4. **Try It** — install command, quick start

**SEO targeting**: Long-tail keywords that AEC teams actually type:
- "how to bulk add users to autodesk ACC"
- "export ACC project permissions CSV"
- "automate BIM model translation"
- "autodesk forge webhook not working"

---

## Page Templates

### Template Structure (Astro/MDX)

```yaml
---
title: "{Problem Statement} — RAPS"
description: "{One-sentence solution}"
keywords: ["{keyword1}", "{keyword2}", "{keyword3}"]
pain_point: "{pain_point_id from painpoints.json}"
raps_commands: ["command1", "command2"]
time_saved: "{X hours → Y seconds}"
persona: "{BIM Manager | IT Admin | APS Developer}"
---
```

```mdx
## The Problem

{2-3 sentences describing the pain. Use specific numbers.}

## The Manual Way

{Step-by-step of how you'd do this in ACC web UI. Include click counts.}

## The RAPS Way

```bash
{exact raps command}
```

{Expected output}

**Time**: {manual time} → {raps time}

## Get Started

```bash
npm install -g @nicedmytro/raps
raps auth login --device
{the command from above}
```
```

---

## 30 Target Pages

### Wave 1 — Blake's Pain Points (highest search volume, proven demand)

| # | Slug | Target Keyword | Pain Point | RAPS Command |
|---|------|---------------|------------|--------------|
| 1 | `bulk-add-users-acc` | "add users to multiple ACC projects" | Adding one user to 1,700 projects takes days in web UI | `raps admin user add --all-projects` |
| 2 | `export-permissions-csv` | "export ACC permissions to CSV" | No built-in ACC export for who-has-what-access | `raps project users list --format csv` |
| 3 | `export-users-companies-csv` | "export ACC users companies CSV" | Member/company directory locked in web UI | `raps admin user list --format csv` |
| 4 | `clone-user-permissions` | "copy user permissions ACC project" | No way to duplicate one user's access to another | `raps project users list → raps project user add` |
| 5 | `copy-project-with-permissions` | "duplicate ACC project setup" | Project templates don't copy member roles | `raps project create --from-template` |
| 6 | `change-user-email-keep-permissions` | "update user email Autodesk ACC" | Changing email/name means re-adding everywhere | Pipeline: export → update → re-apply |
| 7 | `archive-project-backup` | "backup ACC project locally" | No full project export/download in ACC | `raps pipeline run backup-project` |
| 8 | `delete-acc-projects` | "permanently delete Autodesk project" | Archive-only, no permanent delete via UI | `raps project archive` (API limitation noted) |

### Wave 2 — Developer Pain Points (Stack Overflow top unanswered)

| # | Slug | Target Keyword | Pain Point | RAPS Command |
|---|------|---------------|------------|--------------|
| 9 | `autodesk-3-legged-auth` | "autodesk 3 legged oauth setup" | Auth flow is confusing, 55% questions unanswered | `raps auth login --device` |
| 10 | `forge-webhook-not-working` | "autodesk forge webhook 401 error" | 67% webhook questions unanswered on SO | `raps webhook create/list/delete` |
| 11 | `translate-revit-model-api` | "translate revit model forge API" | Multi-step process with polling, easy to get wrong | `raps translate start --wait` |
| 12 | `upload-large-file-forge` | "upload large file autodesk forge resumable" | Resumable uploads are complex to implement | `raps object upload --resume` |
| 13 | `design-automation-revit` | "design automation revit workitem" | DA setup has 50% unanswered rate on SO | `raps da workitem create` |
| 14 | `forge-bucket-403` | "autodesk forge bucket permission denied" | Bucket auth scope confusion | `raps bucket create / raps auth test` |
| 15 | `acc-api-get-project-users` | "ACC API list project members" | API docs are scattered across multiple endpoints | `raps project users list` |
| 16 | `forge-token-expired` | "autodesk forge token refresh" | Token lifecycle management is manual | `raps auth status` (auto-refresh) |

### Wave 3 — Enterprise Workflow Pain Points (ACC Ideas top-voted)

| # | Slug | Target Keyword | Pain Point | RAPS Command |
|---|------|---------------|------------|--------------|
| 17 | `bulk-folder-permissions` | "set folder permissions ACC bulk" | Manual per-folder permission assignment | `raps admin folder set-permissions` |
| 18 | `automate-acc-project-setup` | "automate ACC project creation" | Manual project provisioning at scale | `raps project create` + pipeline |
| 19 | `acc-issue-export-csv` | "export ACC issues to CSV Excel" | No bulk issue export from ACC web UI | `raps issue list --format csv` |
| 20 | `acc-rfi-export` | "export RFIs from ACC" | RFI data locked in web UI | `raps rfi list --format csv` |
| 21 | `model-coordination-clash` | "automate clash detection ACC" | Manual clash management in MC | Pipeline: translate → coordinate |
| 22 | `acc-cost-management-api` | "ACC cost management API automation" | Cost data entry is manual and error-prone | `raps api request` (Cost API) |
| 23 | `acc-submittal-tracking` | "automate ACC submittals" | Manual submittal lifecycle tracking | `raps acc submittals list` |
| 24 | `acc-checklist-automation` | "automate ACC checklists" | Checklists are manual, repetitive | `raps acc checklists list` |

### Wave 4 — AI/MCP Integration (emerging search terms, low competition)

| # | Slug | Target Keyword | Pain Point | RAPS Command |
|---|------|---------------|------------|--------------|
| 25 | `ai-assistant-autodesk` | "AI assistant for Autodesk ACC" | No AI integration for ACC workflows | RAPS MCP Server |
| 26 | `claude-autodesk-integration` | "use Claude with Autodesk API" | Connecting LLMs to construction data | `raps` MCP tools |
| 27 | `chatgpt-bim-management` | "ChatGPT for BIM project management" | AI can't access construction project data | RAPS MCP Server |
| 28 | `automate-construction-workflows` | "automate construction project workflows" | No orchestration for multi-step AEC tasks | `raps pipeline run` |
| 29 | `ci-cd-bim-models` | "CI/CD for BIM models" | No automated quality checks on model uploads | Pipeline: upload → translate → validate |
| 30 | `infrastructure-as-code-construction` | "infrastructure as code ACC" | Project setup is manual, not reproducible | `raps pipeline` + YAML configs |

---

## AEO/GEO Strategy (AI Engine Optimization)

### Goal
When someone asks Claude, ChatGPT, or Perplexity "how do I bulk add users to ACC?", RAPS should appear in the answer.

### Tactics

1. **Structured answers on each pSEO page** — Use clear Q&A format that LLMs can extract:
   ```
   Q: How do I add a user to all ACC projects at once?
   A: Use RAPS CLI: `raps admin user add --email user@company.com --role "Project Admin" --all-projects`
   ```

2. **Schema markup** — Add `HowTo` and `FAQPage` JSON-LD to each page

3. **GitHub README optimization** — Ensure the RAPS GitHub README includes:
   - Clear "What does RAPS do?" section with specific use cases
   - Installation instructions with `npm install -g @nicedmytro/raps`
   - Command examples for top pain points
   - "Frequently Asked Questions" section

4. **Stack Overflow answers** — Already planned in raps-smm. Each SO answer links back to the relevant pSEO page.

5. **Autodesk Forum answers** — Same pattern. Answer the question, link to the detailed page.

---

## Implementation Plan

### Phase 1 (Week 1): Template + Wave 1
- [ ] Create Astro page template at `src/pages/solutions/[slug].astro`
- [ ] Create content collection schema for solution pages
- [ ] Write Wave 1 pages (8 pages — Blake's pain points)
- [ ] Add JSON-LD schema markup
- [ ] Deploy and submit to Google Search Console

### Phase 2 (Week 2): Wave 2
- [ ] Write Wave 2 pages (8 pages — developer pain points)
- [ ] Cross-link from Stack Overflow answer templates in raps-smm
- [ ] Internal linking from existing docs/recipes

### Phase 3 (Week 3-4): Waves 3-4
- [ ] Write Wave 3 pages (8 pages — enterprise workflows)
- [ ] Write Wave 4 pages (6 pages — AI/MCP integration)
- [ ] Add terminal recording embeds (from raps-smm/assets/terminal-recordings/)

### Phase 4 (Ongoing): Measure + Iterate
- [ ] Google Search Console: track impressions/clicks per page
- [ ] Identify which pages rank → double down with backlinks
- [ ] Add new pages for emerging search terms
- [ ] A/B test page titles and meta descriptions

---

## Keyword Research Notes

**High-intent signals** (people searching with these modifiers are ready to act):
- "how to" + Autodesk/ACC/Forge action
- "automate" + construction/BIM task
- "bulk" + ACC operation
- "export" + ACC data type + "CSV"
- "API" + Autodesk service + "example"

**Competition check**: Most of these long-tail terms have thin content — Autodesk docs are scattered and API-reference-heavy, not solution-oriented. Forum answers are fragmented. There's a clear content gap.

**Volume estimate**: Individual terms are low volume (50-500/mo) but collectively 30 pages × 100-300 visits/mo = 3,000-9,000 monthly organic visits from high-intent users.
