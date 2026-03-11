# Effective Engineering for CAD/PLM — Slide Content for Verification

> **Purpose:** This document contains ALL claims made in the C-level pitch deck.
> Claude Code should verify each claim marked with `[VERIFY]` against actual RAPS source code, website, and available data.
> 
> **Verification approach:**
> 
> - Check RAPS codebase for command counts, MCP tools, API coverage, bindings, paid tiers
> - Check rapscli.xyz and mcp.rapscli.xyz for live services
> - Check raps-marketing repo for research documents
> - Cross-reference numbers with actual data, not memory

-----

## SLIDE 1: Title

**Title:** Effective Engineering for CAD/PLM

**Subtitle:** Where manufacturing expertise meets modern software engineering

**Tagline:** The industry is 10 years behind. We lead the shift.

**Author:** Dmytro Yemelianov | March 2026

**Claims to verify:** None (framing only)

-----

## SLIDE 2: The Industry’s Inflection Point

### Left block: “$80B industry, zero modern engineering”

- `[VERIFY]` AI is rewriting every workflow — AEC hasn’t started
- `[VERIFY]` Global instability demands efficiency at scale
- `[VERIFY]` The gap: engineers don’t code, coders don’t engineer
- `[VERIFY]` Companies that move first define the standard

### Right block: “Meanwhile, Autodesk is going backwards”

- `[VERIFY]` Layoffs gutted developer support teams
  - Source: Autodesk layoff announcements 2023-2024
- `[VERIFY]` BIM360 → ACC forced migration, no tooling
  - Check: does Autodesk provide bulk migration tools? CLI support for migration?
- `[VERIFY]` Bulk operations: total failure (1,700+ projects, zero automation)
  - Source: Blake Pettus engagement, QuikTrip project count
  - Check: does ACC Admin API support bulk user add across all projects?
- `[VERIFY]` Customer requests ignored 4+ years. Archived their own CLI.
  - Check: Viewer measurement diameter request (97 votes, years unresolved)
  - Check: forge-cli archived on GitHub (https://github.com/Autodesk-Forge/forge-cli)

### Center bar:

“This is not about selling tools. It’s about leading the paradigm shift to effective engineering.”

### Bottom section: “Our window to become the evangelist”

- `[VERIFY]` Autodesk May demo confirmed — Dir. Platform Services
  - Source: confirm with Dmytro
- `[VERIFY]` DevCon Virtual — visibility to entire developer community
  - Source: DevCon invitation from Cyrille
- `[VERIFY]` Team Intl already investing in AEC hiring
  - Source: confirm with Dmytro
- `[VERIFY]` Sitecore contract ends April → zero ramp-up
  - Source: confirm with Dmytro

### Bottom tagline:

“Think multiple steps ahead. The companies that define AEC engineering practices now will own the decade.”

-----

## SLIDE 3: What We Already Have

### Left column: READY ASSETS

#### Card 1: RAPS Platform

- `[VERIFY]` CLI + MCP server + Cloud (Cloudflare containers)
  - Check: MCP server exists at mcp.rapscli.xyz
  - Check: Cloud version uses Cloudflare containers
  - Check: fire-and-forget mode exists
- `[VERIFY]` Python & Node bindings
  - Check: PyO3 bindings exist in repo
  - Check: Node bindings/delivery exists
- `[VERIFY]` Runs in CI/CD, GitHub Actions
  - Check: GitHub Actions integration exists or is documented
  - Check: container/Docker support exists
- `[VERIFY]` Paid plugin tiers
  - Check: paid tier structure exists (what tiers? what pricing?)
- `[VERIFY]` Rust-optimized
  - Check: main codebase is Rust
- `[VERIFY]` Devs don’t write clients from scratch
  - Check: bindings allow direct integration without custom HTTP client code

#### Card 2: Engineering + Software

- `[VERIFY]` 10+ yrs in manufacturing (Vault, Inventor, AutoCAD)
  - Source: confirm with Dmytro
- `[VERIFY]` AND software dev (Rust, Python, APIs)
  - Check: RAPS codebase
- `[VERIFY]` Expert Elite status
  - Check: current Autodesk Expert Elite status
- `[VERIFY]` ADN member
  - Check: current ADN membership

#### Card 3: Novel market research

- `[VERIFY]` 200+ forum threads analyzed
  - Source: research documents
  - Check: Cross-platform_CAD_PLM_Developer_Experience.md
  - Check: Developer_Pain_Points_Are_Universal.md
- `[VERIFY]` Cross-platform pain points documented
- `[VERIFY]` No public research like this exists
  - Source: gap analysis document confirms this

### Right column: LIVE TRACTION

#### QuikTrip — Status: In Progress

- `[VERIFY]` $14B company
  - Source: QuikTrip revenue data (FY2024)
- `[VERIFY]` 1,700+ ACC projects
  - Source: confirm with Dmytro
  - Check: confirm exact project count with Dmytro
- `[VERIFY]` Actively onboarding
  - Check: has Blake executed RAPS commands on QT infrastructure?
- `[VERIFY]` First reference case
  - Check: is QuikTrip aware they’re being positioned as reference?

#### Autodesk May Demo — Status: Confirmed

- `[VERIFY]` With Dir. Platform Services (Cyrille Fauvel)
  - Check: Cyrille’s exact title — is it “Director of Platform Services”?
- `[VERIFY]` His personal invitation
  - Source: confirm with Dmytro

#### DevCon Virtual — Status: Invited

- `[VERIFY]` 3 sessions submitted
  - Check: how many DevCon session proposals actually submitted?
  - Check: session titles and topics
- `[VERIFY]` Personal invite
  - Source: confirm with Dmytro

#### Michael Beale (Autodesk) — Status: Active

- `[VERIFY]` Sr. Engineer title
  - Check: is Michael Beale “Senior Software Engineer” at Autodesk?
- `[VERIFY]` Collaboration + consulting referrals already offered
  - Source: confirm with Dmytro
  - Check: SSA support offered?
  - Check: ACC Admin API contributions offered?
  - Check: RCW migration consulting leads — exactly 2 leads?

### Bottom tagline:

“This is not a pitch for an idea. Everything above is live and in motion.”

-----

## SLIDE 4: Evangelism Creates Revenue Naturally

### Three revenue columns:

#### Column 1: Solve Their Problems (Consulting)

- Custom APS/ACC builds
- Cross-platform migrations
- Design Automation

Tag: “Consulting — high margin”

#### Column 2: RAPS Platform (Product)

- `[VERIFY]` CLI + MCP + Cloud tiers
- `[VERIFY]` Python & Node bindings
- `[VERIFY]` Paid plugins, enterprise

Tag: “Product — recurring”

- `[VERIFY]` What is the actual paid tier structure?
- `[VERIFY]` What plugins are paid vs free?
- `[VERIFY]` Is there enterprise pricing?

#### Column 3: Embed Our People (Staff Aug)

- Specialized developers
- Long-term embedding
- Our core competency

Tag: “Staff aug — steady base”

### Phased timeline:

#### Q2 2026 — PROVE IT

- QuikTrip as working illustration
- Autodesk demo. DevCon talks.

#### Q3 2026 — SCALE IT

- Team + convert inbound demand
- Referrals from DevCon wave

#### Q4 2026 — OWN IT

- Cross-platform expansion
- Recognized industry voice

-----

## SLIDE 5: The Ask — 60-Day Proof Period

### Left: WHAT I PUT ON THE TABLE

1. **QuikTrip LOI secured**
- `[VERIFY]` Has LOI been requested from Blake yet?
- `[VERIFY]` Status: “in progress” or “secured”?
- Note: pitch says “secured” — should only say this if Blake has confirmed
1. **RAPS platform IP — ready to discuss terms**
- `[VERIFY]` CLI + MCP server + Cloud + paid tiers — all components exist?
- Note: offering exclusive license or contribution
1. **60 days, just me — zero additional cost**
- `[VERIFY]` Sitecore contract ends April 2026 — confirmed?
- Logic: reallocation of existing salary, not new hire
1. **Compensation tied to milestones**
- Note: commitment from Dmytro — no verification needed

### Right: PIPELINE: CLIENT + PARTNER + LEADS

1. **QuikTrip** — $14B company
- `[VERIFY]` 1,700+ ACC projects (exact number from Blake)
- `[VERIFY]` LOI in progress
- `[VERIFY]` Actively onboarding — what commands has Blake run?
1. **Autodesk (Cyrille Fauvel)** — Strategic partner
- `[VERIFY]` May demo confirmed — exact date?
- `[VERIFY]` Written interest in progress — confirm status with Dmytro
1. **RCW Migrations (x2)** — via Michael Beale
- `[VERIFY]` Exactly 2 RCW migration leads?
- `[VERIFY]` Are these referrals from Michael, or potential referrals?
- `[VERIFY]` RCW = Revit Cloud Worksharing — correct terminology?
1. **DevCon Inbound** — Post-May 2026
- Logic: DevCon + marketing materials drive organic leads
- `[VERIFY]` Are DevCon sessions confirmed or just submitted?

### Bottom bar:

“I’m not asking you to bet on an idea. I’m asking for 60 days to prove it — at zero additional cost.”

### 60-DAY SUCCESS CRITERIA:

1. QuikTrip signed engagement
1. Autodesk May demo delivered
1. RCW migration scoped
1. DevCon materials published
1. Then → hire discussion

-----

## SLIDE 6: Next Steps

1. **Approve 60-day proof period — just me, zero cost**
- April-May 2026. Engineering + software expertise. Ready now.
1. **Close QuikTrip as paid engagement**
- LOI secured. First revenue under Team International.
1. **Deliver Autodesk May demo as Team International**
- Establish our voice with the team that shapes the platform.
1. **Day 60: review results, decide on team buildout**
- Pipeline proven → hire. Not proven → zero loss.

### Closing:

“60 days. Zero cost. All the upside. Let’s go.”

-----

## ANALYTICS PDF — Key Claims to Verify

### ROI Numbers:

- `[VERIFY]` $150-250K Year 1 revenue target — based on what?
- `[VERIFY]` Break-even Month 4-5 — assumptions?
- `[VERIFY]` 3-5x ROI by Month 12

### Cost Estimates:

- `[VERIFY]` Senior Dev salary range: $8-12K/mo — realistic for Ukraine market?
- `[VERIFY]` Mid Dev salary range: $5-8K/mo — realistic?
- `[VERIFY]` Sales/BD: $3-5K/mo — realistic?
- `[VERIFY]` PM: $4-6K/mo — realistic?

### Pain Point Matrix:

- `[VERIFY]` OAuth/Auth: HIGH across all 4 vendors
  - Source: Developer_Pain_Points doc
- `[VERIFY]` Bulk operations: NONE for Autodesk — truly zero CLI/API support?
  - Check: ACC Admin API capabilities for bulk user operations
- `[VERIFY]` AI/MCP integration: NONE across all vendors
  - Check: Petr Broz aps-mcp-server exists — should this be “BASIC” for Autodesk?

### Research Sources:

- `[VERIFY]` 80+ Autodesk Forums threads
- `[VERIFY]` 40+ GitHub Issues
- `[VERIFY]` 25+ Onshape Forums threads
- `[VERIFY]` 30+ SOLIDWORKS/3DX Forums
- `[VERIFY]` 20+ Siemens Community posts
- `[VERIFY]` 15+ Stack Overflow posts
- `[VERIFY]` 10+ Industry Analyst Reports
- Note: do these numbers add up to 200+? (80+40+25+30+20+15+10 = 220+) ✓

### Autodesk App Store Gap:

- `[VERIFY]` 4,078 apps analyzed
  - Source: autodesk_apps_complete.csv in project files (shows 4,078 rows) ✓
- `[VERIFY]` Zero competition in: DA CLI tools, auth helpers, translation debuggers, ACC admin automation, cross-platform CLI, MCP/AI tools
  - Check: search app store data for competing apps in these categories

### Competitive Landscape:

- `[VERIFY]` Petr Broz aps-mcp-server — how many MCP tools does it have vs RAPS 51?
- `[VERIFY]` Frederic Python SDK — 373 endpoints claim
  - Source: Kiota-generated SDK, check actual endpoint count
- `[VERIFY]` forge-cli archived — confirm on GitHub
- `[VERIFY]` AMC Bridge — confirm they do CAD integrations consulting

### RAPS Platform Specifics:

- `[VERIFY]` 100+ commands — exact count from `raps --help` or command index
- `[VERIFY]` 51 MCP tools — exact count from MCP server tool list
- `[VERIFY]` 15+ APIs covered — list which APIs
- `[VERIFY]` Current version number (v4.13.0+ per memory, may be higher now)
- `[VERIFY]` MCP server URL: mcp.rapscli.xyz — is it live?
- `[VERIFY]` Cloud version on Cloudflare containers — deployed?
- `[VERIFY]` Fire-and-forget mode — what exactly is this?
- `[VERIFY]` Python bindings via PyO3 — exist in repo?
- `[VERIFY]` Node bindings — exist? via what mechanism (NAPI, WASM)?
- `[VERIFY]` Paid plugin tiers — what tiers exist? pricing?
- `[VERIFY]` GitHub Actions support — documented?
- `[VERIFY]` Container/Docker support — Dockerfile exists?

-----

## Speaker Script — Additional Claims

- `[VERIFY]` “Autodesk archived their own CLI (forge-cli)”
  - Check: https://github.com/Autodesk-Forge/forge-cli status
- `[VERIFY]` “Viewer measurement gaps (97 votes, 4+ years unresolved)”
  - Source: Autodesk Ideas forum — find exact vote count and age
- `[VERIFY]` “Guilherme Pombeiro — Dir. Strategic Talent Management”
  - Check: exact title at Team International
- `[VERIFY]` “Blake Pettus — Manager, Prototyping & Systems at QuikTrip”
  - Check: exact current title
- `[VERIFY]` “Michael Beale — Senior Software Engineer at Autodesk”
  - Check: exact current title

-----

## Verification Priority

**Critical (pitch fails if wrong):**

1. RAPS command count (100+)
1. MCP tool count (51)
1. API count (15+)
1. MCP server at mcp.rapscli.xyz is live
1. Cloud version exists on Cloudflare
1. Paid tiers exist
1. Python & Node bindings exist
1. QuikTrip project count (1,700+)
1. Cyrille’s title and May demo confirmation
1. Michael Beale’s title and RCW referral count

**Important (weakens pitch if wrong):**
11. 200+ forum threads count
12. 4,078 app store count
13. forge-cli archived status
14. Viewer measurement vote count
15. Salary estimates for Ukraine market

**Nice to have:**
16. Exact RAPS version number
17. DevCon session count submitted
18. Frederic SDK endpoint count