# Autodesk Marketplace Analysis — ACC & BIM 360 App Store

**Generated**: 2026-02-25
**Data Sources**: apps.autodesk.com BIM360/ACC listings, integration category, construction management category, web search
**Previous Report**: competition_revit.json (Jan 31, 2026 — Revit marketplace only, 1,437 apps)

## Executive Summary

The ACC & BIM 360 App Store contains **259 apps** across 22 categories. The marketplace is dominated by free/freemium apps (64%), has extremely low user engagement (most apps have 0 ratings), and has **zero CLI tools**, **zero MCP/AI integration tools**, and **near-zero developer/admin tooling**. RAPS occupies a completely uncontested niche.

## App Store Statistics

| Metric | Value |
|--------|-------|
| Total apps (ACC/BIM360) | 259 |
| Total apps (Revit) | 1,437 |
| Categories | 22 |
| Pages of listings | 11 (24 apps/page) |
| Free apps | ~64% |
| Trial apps | ~27% |
| Paid apps | ~4% |
| Subscription apps | ~2% |

## Apps by Category

| Category | Count | Notes |
|----------|-------|-------|
| Integration | 115 | Largest — dominated by Data Exchange connectors |
| Construction Management | 124 | Second largest, heavy overlap with Integration |
| Data Exchange | ~20 | Autodesk-published connectors (Revit, Civil 3D, etc.) |
| Reality Capture / AR/VR | ~8 | OpenSpace, Evercam, Matterport, FARO |
| BIM Data Analysis / Reporting | ~5 | Power BI connector, Vcad |
| Task Automation | ~5 | IMAGINiT Clarity family (4 variants) |
| AI Platforms | ~3 | Trunk Tools, Gryps, LevelApp |
| File Management / Bulk Ops | ~3 | Bulk File Uploader, eT.ools, Cloudsfer |
| Project Setup / Admin | ~2 | BIM load, IMAGINiT ACCelerate |
| Construction 4D / Scheduling | ~3 | cmBuilder, Fuzor, Project Atom |

## Most Relevant Apps to RAPS

### Tier 1 — Direct Competitors

| App | Pricing | Overlap with RAPS |
|-----|---------|-------------------|
| **BIM load** | Unknown | **Most direct.** Automates project setup, bulk user/role assignment, custom folder structures. Web app only, likely limited scope vs RAPS's 60+ tools. |
| **IMAGINiT ACCelerate** | Trial | Automate administrative tasks in ACC. Web UI, no CLI/scripting. |
| **Bulk File Uploader for ACC** | Subscription | Batch upload/download files. Windows-only desktop app. |
| **eT.ools DM UD** | $100/year | Batch update file description attributes. Very narrow, Windows-only. |

### Tier 2 — Partial Competitors

| App | Pricing | Overlap Area |
|-----|---------|-------------|
| IMAGINiT Clarity (3 versions) | Free | Revit/AutoCAD task automation, not APS API admin |
| Connect for ACC | Trial | No-code integration platform, different audience |
| Cloudsfer | Free | Data transfer/backup across ACC + 20 cloud services |
| ProjectReady WorkBridge | Free | Sync/migrate across Autodesk, Procore, SharePoint |
| Two Way Sync (Build & SharePoint) | Free | Bi-directional sync with SharePoint/Teams/OneDrive |
| CDE Sync | Free | Automate data sync between ACC and other CDEs |

## RAPS Capabilities vs Marketplace — Gap Analysis

| RAPS Capability | Marketplace Coverage | Gap |
|-----------------|---------------------|-----|
| **CLI-based APS API access** | **NONE** — every app is web or Windows desktop | CRITICAL |
| **MCP/AI integration (60+ tools)** | **NONE** — no LLM-integrated APS tooling | CRITICAL |
| **Scriptable/automatable workflows** | **NONE** — no piping, shell, or CI/CD support | CRITICAL |
| **Cross-platform (macOS/Linux/Windows)** | **~0** — 95%+ are Web or Windows-only | MAJOR |
| **OSS bucket management** | **NONE** | TOTAL |
| **APS auth management** | **NONE** — no OAuth flow/token management tools | TOTAL |
| **Webhook management** | **NONE** | TOTAL |
| **Data Management API operations** | **NONE** — no hubs/projects/folders API access | TOTAL |
| **Model Derivative / translation ops** | **NONE** — no translation job management tools | TOTAL |
| **API health monitoring** | **NONE** | TOTAL |
| **Developer tooling / debugging** | **NONE** | TOTAL |
| **Bulk user management at scale** | 1 app (BIM load) | MAJOR |
| **Project template/scaffolding** | 1 app (BIM load) | MAJOR |
| **ACC admin operations via API** | 1 app (IMAGINiT ACCelerate, trial) | MAJOR |
| **Batch operations across projects** | ~2 apps (BIM load, Cloudsfer) | MAJOR |

**RAPS has ZERO competition in 11 of 15 assessed capability areas.**

## Notable Apps (Full Details)

### BIM load (Closest Competitor)
- Automate project setup in ACC
- Quickly assign users and roles in bulk
- Apply custom folder structure templates
- **Limitations vs RAPS**: Web-only, no CLI, no scripting, no CI/CD, no auth management, no Model Derivative, no webhooks, no OSS, no Design Automation, no Reality Capture

### IMAGINiT (Most Prolific Vendor)
- **Clarity** — Automate Revit/AutoCAD tasks in ACC (Free)
- **Clarity Cloud** — Cloud-based version (Free)
- **Clarity w/Secure Service Accounts** — SSA-compatible version (Free)
- **ACCelerate** — ACC admin task automation (Trial)
- 4 marketplace entries from one vendor = dominant in automation space
- **Limitations vs RAPS**: Focused on Revit/AutoCAD design tasks, not APS API platform admin

### Autodesk Data Exchange Connectors (~10 apps)
- Autodesk publishes official connectors for: Revit, Civil 3D, Dynamo, Navisworks, Rhino, Inventor, Tekla, Grasshopper
- These are format/model exchange tools, not admin/automation tools
- No overlap with RAPS

## Pricing Landscape

| Tier | % | Implication |
|------|---|-------------|
| Free | 64% | Marketplace norm is free; RAPS being open-source aligns well |
| Trial | 27% | Likely convert to paid but pricing hidden behind trial wall |
| Paid | 4% | Only 2 apps with visible pricing ($100/year, subscription) |
| Subscription | 2% | SaaS model emerging but rare |

**Key insight**: The marketplace has zero "premium developer tooling" category. The concept of paying for APS developer tools is unexplored territory.

## Rating/Review Data

| Rating | Count |
|--------|-------|
| 9 (Vcad) | 1 app |
| 3 | 2 apps |
| 2 | 2 apps |
| 1 | 5+ apps |
| **0 (no ratings)** | **~85% of apps** |

**Key insight**: Marketplace engagement is extremely low. Most apps have zero ratings. Discovery happens outside the marketplace.

## Strategic Takeaways

1. **The "developer/admin tooling" category doesn't exist** in Autodesk's marketplace taxonomy — RAPS would need to create the category
2. **No CLI tool in the entire 259-app marketplace** — RAPS is unique across the entire ecosystem
3. **AI/LLM integration is nascent** — only 3 apps mention AI (none for APS API operations)
4. **BIM load is the only direct competitor** but covers ~5% of RAPS's functionality
5. **IMAGINiT dominates the automation niche** with 4 apps but focuses on design, not platform admin
6. **64% free pricing norm** validates RAPS's open-source model
7. **Low engagement** suggests the marketplace is not the primary discovery channel — forums, SO, and GitHub are more important
