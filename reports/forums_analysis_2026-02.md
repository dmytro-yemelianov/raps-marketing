# Autodesk Developer Forums Analysis

**Generated**: 2026-02-25
**Data Sources**: forums.autodesk.com (Data Exchange, Forma Developer, Revit API), Reddit r/bim, web search
**Previous Report**: ACC Ideas Forum analysis (Jan 16, 2026 — 4,295 feature requests)

## Executive Summary

Autodesk developer forums lack a dedicated APS forum — developer questions are fragmented across Revit API, Data Exchange, Forma Developer, and external platforms (StackOverflow, Reddit). The Forma Developer Forum is the most active with 72 unique topic tags. Key pain points mirror StackOverflow: authentication, Model Derivative, and DWG conversion workflows. A Reddit thread directly asking about Model Derivative/Design Automation real-world usage represents an ideal RAPS outreach opportunity.

## Forum Landscape

| Forum | Activity | APS Relevance | Notes |
|-------|----------|--------------|-------|
| **Forma Developer Forum** | Active | Medium | 72 topic tags, regular events, monthly updates |
| **Revit API Forum** | Active | Medium | De facto overflow for APS questions |
| **Data Exchange Forum** | Low | Low | Mostly test posts, minimal real content |
| **APS/Forge dedicated forum** | **Does not exist** | — | Critical gap in Autodesk's support |
| **Reddit r/bim** | Active | High | Real-world workflow questions |
| **StackOverflow** | Active | High | Primary Q&A channel (see separate report) |

## Key Finding: No Dedicated APS Forum

There is no `forums.autodesk.com` board specifically for APS Platform Services developers. Questions are scattered across:
- Revit API Forum (Forge/APS plugin questions)
- Data Exchange Forum (file conversion questions)
- Forma Developer Forum (auth API, APS viewer questions)
- StackOverflow (primary for technical Q&A)
- Reddit r/bim (real-world workflow discussions)

**This fragmentation is itself a pain point** — developers post "Not sure if this is the correct spot to post APS questions."

## Identified Forum Threads

| Thread | Forum | Status | Topic |
|--------|-------|--------|-------|
| "AutoDesk Platform services" — DWG to 3D conversion | Data Exchange | **Unsolved** | Automated workflow for .dwg containing 3D models |
| "Autodesk User Profile using Auth Api?" | Forma Developer | **Solved** | SDK Auth API for user profile retrieval |
| "APS Tutorial Trouble" | Revit API | **Solved** | Getting started with APS tutorials |
| "Plugin for Revit 2025 could not load Autodesk.Forge" | Revit API | **Unsolved** | Forge-to-APS migration in .NET Core |
| "Do anyone use Model Derivative or Design Automation?" | Reddit r/bim | Active | Real workflow questions about MD/DA usage |

## Forma Developer Forum — Topic Taxonomy (72 Tags)

### Most Active Topics

| Theme | Tags (count) | Est. Threads |
|-------|-------------|-------------|
| Forma Platform Core | Forma (31), AutodeskForma (7), Autodesk Forma (4), Forma Design (2) | ~44 |
| Community & Events | community (4), hackathon (3), devcon (2), AU (2), discussion (2) | ~15 |
| API & Integration | API (4), APS (2), REST API (1), invokeEndpoint (1), APSViewer (1) | ~11 |
| Analysis & Simulation | Analysis (3), Analysis Tools (1), Noise/Sun/Wind analysis | ~10 |
| Geometry & 3D | Geometry (4), 3D Import (1), Mesh (1), Terrain (1) | ~9 |
| Interop / Export | "Forma to Revit" (2), Revit (1), SketchUp (1), GeoJSON (1) | ~8 |
| Data & Units | area (1), floor plan (1), batch-create (1), Library (1) | ~8 |
| Extensions | extension (2), custom extension (1), Floating Panel (1) | ~6 |
| Auth & Access | auth (2), access (1), user (1), view-only (1) | ~5 |

### Emerging Interests
- **batch-create** tag indicates demand for bulk operations in Forma
- **invokeEndpoint** suggests developers pushing beyond documented APIs
- **hackathon** (3 threads) shows community engagement opportunities

## Data Exchange Forum — Topic Taxonomy (27 Tags)

Dominated by test/sandbox content. Limited real developer activity.

| Theme | Tags (count) |
|-------|-------------|
| Testing | test (6), Test Only (2) |
| BIM / Construction | BIM (1), BIM 360 Docs (1), VDC (1) |
| CAD / Design | AutoCAD (1), Convert Mesh (1), 3D Printing (1) |
| Account Issues | accounts (1), Login (1), sessions (1), cookies (1) |

## Reddit r/bim — Direct RAPS Opportunity

Thread: *"Do anyone use Autodesk's Model Derivative or Design Automation?"*
- URL: `reddit.com/r/bim/comments/1jqkryk/`
- Asks about real workflows, geometry vs. properties extraction, practical integration patterns
- **This is exactly what RAPS solves** — ideal outreach target
- Represents organic demand for Model Derivative/Design Automation tooling

## Developer Pain Points Where RAPS Helps

### High Relevance
1. **File conversion & Model Derivative** — "Reliable automated workflow to convert .dwg files containing 3D models" → `raps translate start --wait`
2. **Authentication & token management** — OAuth flows, token issues, SSA migration → `raps auth login/test/inspect`
3. **Forge-to-APS migration** — NuGet package loading failures, API changes → RAPS uses current APS endpoints natively
4. **Design Automation CLI** — Autodesk's own blog recognizes developers want CLI access → RAPS provides this

### Medium Relevance
5. **Data Exchange & interop** — Forma-to-Revit, GeoJSON, batch creation → `raps object upload/download`
6. **Construction Cloud integration** — ACC file operations, project management → `raps admin/folder/issue/rfi`
7. **Analysis automation** — Sun/wind/noise analysis pipelines → orchestratable via RAPS

## Content Opportunities

### Forum Engagement Targets
1. **Data Exchange Forum** — Answer DWG conversion questions with `raps translate` examples
2. **Revit API Forum** — Help Forge-to-APS migration questions, demonstrate RAPS as modern alternative
3. **Forma Developer Forum** — Engage on API/auth topics, show `raps auth` simplicity
4. **Reddit r/bim** — Answer Model Derivative/Design Automation workflow questions with real RAPS demos

### Content to Create
1. Forum answer template: "Automating DWG-to-SVF2 conversion with RAPS CLI"
2. Reddit response: "Real-world Model Derivative workflow with RAPS"
3. Forum tutorial: "3-legged OAuth without code — using raps auth login"
4. Blog cross-post: "Why there's no APS developer forum (and what we do instead)"

## Comparison: Forum Activity vs Data Sources

| Source | Content Type | Volume | RAPS Relevance |
|--------|-------------|--------|---------------|
| ACC Ideas Forum | Feature requests | 4,295 ideas | HIGH — shows unmet needs |
| StackOverflow | Technical Q&A | 4,582+ questions | HIGH — shows developer pain |
| Forma Dev Forum | Discussion + API | ~132 threads | MEDIUM — emerging platform |
| Reddit r/bim | Workflow questions | Active | HIGH — real-world use cases |
| Data Exchange Forum | Mixed/test | ~34 threads | LOW — minimal real content |
| APS official forum | **Does not exist** | — | — |
