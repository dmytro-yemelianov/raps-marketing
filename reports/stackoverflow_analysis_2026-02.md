# StackOverflow APS Developer Pain Points Analysis

**Generated**: 2026-02-25
**Data Sources**: autodesk-forge tag (4,582 Qs), autodesk-model-derivative tag (777 Qs), web search results
**Previous Report**: Jan 31, 2026 (7,424 SO questions referenced in plugin_ideas.json)

## Executive Summary

StackOverflow remains the primary Q&A channel for APS developers, with 4,582 questions tagged `autodesk-forge` and 777 tagged `autodesk-model-derivative`. The **13% unanswered rate** (597 questions with zero answers) signals an underserved developer community. Authentication, Model Derivative failures, and ACC API gaps are the top three pain point areas.

## Tag Statistics

| Tag | Total Questions | Unanswered | Rate |
|-----|----------------|------------|------|
| `autodesk-forge` | 4,582 | 597 | 13.0% |
| `autodesk-model-derivative` | 777 | ~100+ | ~13% |
| `autodesk-viewer` | ~400 | ~50+ | ~12% |

## Pain Points by Theme (Ranked by Frequency)

### 1. Authentication & Authorization (Very High)

The single most recurring frustration area. Migration from 2LO/3LO to SSA (Secure Service Accounts) is causing immediate friction.

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| SSA (2LO) cannot access ACC file contents, 3LO works | 0 | 92 | Answered | Jan 2025 |
| APS Authentication (OAuth) error (3-legged) | 0 | 54 | **Unanswered** | Dec 2025 |
| APS Scoped Tokens results into 401 | 1 | 115 | **Unanswered** | Nov 2025 |
| 403 error after migration to developer hubs | 0 | 47 | **Unanswered** | Dec 2025 |
| Automate Authentication 3-legged with Zapier | 0 | 67 | Answered | Nov 2025 |
| 403 Forbidden using CEO's APS credentials | 0 | — | **Unanswered** | 2025 |
| APS OAuth invalid_scope for issues:read | 0 | 58 | **Unanswered** | Sep 2025 |
| ACC Forms access with two-legged OAuth token | 0 | 90 | Answered | Oct 2025 |
| Unable to Access Forma APIs Using Service Account | 0 | 48 | **Unanswered** | Jul 2025 |

**Key patterns**: SSA migration confusion, scope configuration errors, 401/403 after config changes, automating 3-legged tokens, developer hub migration breaking access.

**RAPS opportunity**: CLI auth management (`raps auth login/test/inspect`) directly addresses every one of these pain points.

### 2. Model Derivative / Translation (High)

The most technically complex area with diverse failure modes.

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| TranslationWorker-Internal Failure: failed to unzip | 0 | — | **Unanswered** | 2025 |
| Model Derivative API ignores conversionMethod v3 for IFC | 0 | 57 | Answered | Jul 2025 |
| New failures to translate NWD files | 0 | 91 | Answered | Jun 2025 |
| Error ATF-1024: SAT to SVF Conversion Failure | 0 | 28 | **Unanswered** | Apr 2025 |
| Bounding box mismatch SVF vs STL | 0 | 38 | **Unanswered** | Apr 2025 |
| MD Fetch Properties stuck on 'success' | 1 | 71 | Answered | Nov 2025 |
| Model Derivative returns outdated properties JSON | 1 | 25 | **Unanswered** | Jun 2025 |
| SVF2 storage/cache duration | 1 | 193 | Answered | Apr 2025 |
| Forge Viewer support for IFC v4 files | 0 | 97 | **Unanswered** | Sep 2025 |

**Key patterns**: Translation failures (NWD, IFC, SAT formats), SVF vs SVF2 migration issues, properties endpoint returning stale data, IFC v4 not supported.

**RAPS opportunity**: `raps translate start --wait` with error reporting, `raps translate manifest/status` for tracking.

### 3. Viewer SDK (High)

Runtime issues and developer experience problems.

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| APS Viewer - hide UI (AggregatedView) | -7 | 173 | Answered | Nov 2025 |
| setThemingColor not working without Object Tree | 0 | 167 | Answered | Nov 2025 |
| Very slow load on APS viewer (600-700mb Revit) | -1 | 60 | Answered | Nov 2025 |
| fitToView() returns same bounds in linked models | 0 | 110 | Answered | Jan 2026 |
| Minimap extension globalOffset for multi-model | 1 | 104 | **Unanswered** | Dec 2025 |
| Forge Viewer offline in Vue/Vite (iOS WebView) | 0 | 108 | **Unanswered** | Sep 2025 |

**Key patterns**: Large model performance, multi-model alignment, offline/local SVF loading, mobile 2D crashes.

### 4. ACC / Construction Cloud API (High, Rising)

Newer API area with highest unanswered rate. Growing rapidly.

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| ACC API empty results for custom attributes | 2 | 50 | **Unanswered** | Oct 2025 |
| Read/update custom tabular data in ACC forms | 0 | 37 | **Unanswered** | Feb 2026 |
| Issue image URL for snapshots in ACC Issues | 0 | 26 | Answered | Feb 2026 |
| Place push pins when creating Issues | 1 | 110 | Answered | Jan 2026 |
| Get list of all available roles for ACC project | 0 | 58 | **Unanswered** | Nov 2025 |
| Issue rootcauses parameter not returning data | 0 | 58 | **Unanswered** | Nov 2025 |
| Programmatically downloading an ACC model (403) | 1 | 60 | **Unanswered** | Sep 2025 |
| APS entities search endpoint (undocumented) | 3 | 113 | **Unanswered** | Aug 2025 |

**Key patterns**: Push pin/issue placement coordinates, custom attributes returning empty, forms API auth, undocumented endpoints needed, roles/permissions management.

**RAPS opportunity**: `raps issue create/list`, `raps acc asset/submittal/checklist` commands directly fill these gaps.

### 5. Webhooks (Medium)

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| Fusion Lifecycle webhooks not firing | 0 | 26 | **Unanswered** | Feb 2026 |
| ACC Webhooks: c4r:model.sync not triggered | -1 | 115 | **Unanswered** | Dec 2025 |
| APS Webhook not triggering callback (GET challenge) | 0 | 93 | **Unanswered** | Dec 2025 |

**Key pattern**: Webhooks silently failing. No debugging tools available.

**RAPS opportunity**: `raps webhook create/test/list` with endpoint verification.

### 6. Design Automation (Medium, Emerging)

| Question | Votes | Views | Status | Date |
|----------|-------|-------|--------|------|
| DA 2026 .NET Core update failure | -1 | 60 | Answered | Nov 2025 |
| DA AutoCAD failedUpload 404 | 0 | — | **Unanswered** | 2025 |
| DA Inventor: DWG conversion with titleblock | 0 | 21 | **Unanswered** | Feb 2026 |
| Register app bundle in EMEA region | 0 | 39 | **Unanswered** | Sep 2025 |

**Key patterns**: .NET Framework to .NET Core migration for 2026, regional deployment (EMEA), upload URL expiration.

## Emerging Trends (Late 2025 - Early 2026)

1. **SSA migration friction** — Multiple questions from developers struggling with 2LO-to-SSA transition
2. **Developer Hub migration causing 403 errors** — Autodesk infrastructure changes breaking apps (Dec 2025)
3. **APS Business Model Evolution** — Paid API tier changes raising pricing questions
4. **.NET Core transition for DA 2026** — Breaking change for Inventor/AutoCAD plugins
5. **ACC API adoption growing** — More questions, higher unanswered rate, immature community
6. **IFC v4 support gap** — Multiple questions about IFC v4 failing in Model Derivative
7. **Webhook reliability issues** — Systemic delivery problems, not just config errors

## Most Viewed Questions

| # | Question | Views | Answers |
|---|----------|-------|---------|
| 1 | SVF2 storage created by Model Derivative API | 193 | 1 |
| 2 | Unable to convert BIM360 Derivative | 187 | 1 |
| 3 | APS Viewer - hide UI | 173 | 2 |
| 4 | setThemingColor not working without Object Tree | 167 | 1 |
| 5 | Forge Viewer setThemingColor for large models | 157 | 1 |
| 6 | Explode Block Reference in viewer | 129 | 0 |
| 7 | APS Scoped Tokens 401 | 115 | — |
| 8 | ACC Webhooks c4r:model.sync not triggered | 115 | 0 |
| 9 | APS entities search endpoint (undocumented) | 113 | 0 |
| 10 | Place push pins in Issues API | 110 | 1 |

## Key Takeaways for RAPS Positioning

1. **Auth is #1 pain** — CLI tools simplifying OAuth/token management directly address the most frequent frustration
2. **Translation is complex and error-prone** — Better error reporting and status tracking has a large audience
3. **ACC API is the growth area** — Newer, less documented, highest unanswered rate = opportunity
4. **Community is small and underserved** — Low vote counts + 13% unanswered rate = developers feel alone
5. **Platform changes cause immediate friction** — SSA, developer hubs, .NET Core create demand for stable tooling
