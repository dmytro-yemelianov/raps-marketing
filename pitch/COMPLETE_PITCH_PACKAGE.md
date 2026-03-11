# Effective Engineering for CAD/PLM — Complete Pitch Package

> **For:** CTO, COO — Team International
> **By:** Dmytro Yemelianov | March 2026
> **Format:** 6-slide live pitch (3-5 min) + Analytics handout + Speaker script
> **Internal sponsor:** Guilherme Pombeiro (Dir. Strategic Talent Management)

---

# PART 1: SLIDE DECK CONTENT

---

## Slide 1 — Title

**Effective Engineering for CAD/PLM**

Where manufacturing expertise meets modern software engineering

*The industry is 10 years behind. We lead the shift.*

Dmytro Yemelianov | March 2026

---

## Slide 2 — The Industry's Inflection Point

### Left: $80B industry, zero modern engineering

- AI is rewriting every workflow — AEC hasn't started
- Global instability demands efficiency at scale
- The gap: engineers don't code, coders don't engineer
- Companies that move first define the standard

### Right: Autodesk is creating a vacuum — and they know it

- 7% layoffs reduced developer support capacity
- BIM360 → ACC forced migration with no tooling for customers
- Bulk operations across 1,700+ projects? No automation exists
- Customer feature requests ignored 4+ years. Archived their own CLI.
- **That's why their Director of Platform Services invited us in.**

### Center banner:

**This is not about selling tools. It's about leading the paradigm shift to effective engineering.**

### Bottom: Our window

- ✅ Autodesk May demo confirmed — Dir. Platform Services & Ecosystem
- ✅ DevCon Virtual — visibility to entire developer community
- ✅ Team Intl already investing in AEC hiring
- ✅ My current project (Sitecore) ends April — ready to transition immediately

*The companies that define AEC engineering practices now will own the decade.*

---

## Slide 3 — What We Already Have

### Left: READY ASSETS

**RAPS Platform**
230+ commands, 114 MCP tools, 16 APIs. CLI + MCP server + SaaS cloud + marketplace. Python bindings. Docker, Helm, CI/CD. Paid tiers with Stripe. Rust v5.6. 579 commits in 2 months.

```
┌─────────────────── Autodesk Platform Services (16 APIs) ───────────────────┐
│                                                                            │
│  ┌──────────────────────── raps-kernel ──────────────────────────┐         │
│  │  Auth · HTTP · Rate Limiting · Circuit Breaker · Token Cache  │         │
│  └──────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────────┘         │
│         │      │      │      │      │      │      │                        │
│       OSS    DM   Derivative DA   ACC  Webhooks Reality  ← 7 API crates   │
│         │      │      │      │      │      │      │                        │
│         │      │      │      │    Admin (bulk ops)│                        │
│  ┌──────┴──────┴──────┴──────┴──────┴──────┴──────┴─────────────┐         │
│  │                    Consumed by 3 apps:                        │         │
│  │                                                               │         │
│  │  CLI (230+ cmd)    SaaS Cloud (Axum)    Python (PyO3)        │         │
│  │  MCP (114 tools)   Jobs + WebSocket     Bindings for         │         │
│  │  TUI (7 tabs)      Multi-tenant + RLS   data science         │         │
│  │  Plugins + Skills  AES-256 + JWT                             │         │
│  └───────────────────────────────────────────────────────────────┘         │
│                                                                            │
│  Ships via: npm · PyPI · crates.io · Homebrew · Scoop · Docker · Helm     │
│  Edge: 4 Cloudflare Workers · Marketplace (Stripe) · MCP Gateway          │
│  Content: rapscli.xyz — 6 tools, 35 blog posts, 73 recipes, 72 docs      │
└────────────────────────────────────────────────────────────────────────────┘
```

**Engineering + Software**
10+ yrs in manufacturing (Vault, Inventor, AutoCAD) AND software dev (Rust, Python, APIs). Expert Elite. ADN. This combination barely exists.

**Novel market research**
4,295 ACC feature requests + multi-platform analysis across 4 vendors. No public cross-vendor research exists.

### Right: LIVE TRACTION

| Item | Status |
|------|--------|
| **QuikTrip** — $14B company, 1,700+ ACC projects. Actively onboarding. 8-item wish list received. Permission clone/export already built for their scale. | In Progress |
| **Autodesk May Demo** — With Cyrille Fauvel, Dir. Platform Services & Ecosystem (PSET). Personal invitation. | Confirmed |
| **DevCon Virtual** — 3 sessions submitted. Personal invite. Brand visibility to entire APS community. | Invited |
| **Michael Beale (Autodesk)** — Collaboration offered + RCW migration pipeline (up to 5 enterprise clients). | Active |

*This is not a pitch for an idea. Everything above is live and in motion.*

---

## Slide 4 — Evangelism Creates Revenue Naturally

### Three revenue columns:

| Solve Their Problems | RAPS Platform | Embed Our People |
|---------------------|---------------|-----------------|
| Custom APS/ACC builds | CLI + MCP + Cloud tiers | Specialized developers |
| Cross-platform migrations | Python bindings (PyO3) | Long-term embedding |
| Design Automation | Paid plugins, enterprise | Our core competency |
| *Consulting — high margin* | *Product — recurring* | *Staff aug — steady base* |

### Phased timeline:

| Q2 2026 — PROVE IT | Q3 2026 — SCALE IT | Q4 2026 — OWN IT |
|---------------------|--------------------|--------------------|
| Close QuikTrip. Autodesk demo. DevCon talks. | Team + convert inbound demand. Referrals from DevCon wave. | Cross-platform expansion. Recognized industry voice. |

---

## Slide 5 — The Opportunity for Team International

### Left: WHAT I BRING

| Asset | Detail |
|-------|--------|
| **RAPS platform — production-ready** | CLI + MCP server + SaaS cloud + marketplace. 230+ commands, 114 MCP tools, 16 APIs. Stripe billing live. |
| **QuikTrip — active enterprise engagement** | $14B company. 8-item wish list received. Calls scheduled. Closing in progress. |
| **Autodesk access at director level** | Cyrille Fauvel (Dir. Platform Services & Ecosystem). May demo scheduled. |
| **Ukrainian BIM network** | 50+ specialists — architects, engineers, Revit/Inventor developers in my professional network. |

### Right: WHAT TI GETS

| Benefit | Timeline |
|---------|----------|
| **New revenue stream** — QuikTrip + RCW migrations + DevCon inbound | from April |
| **Autodesk Partner Programs** — APS Certified Partner, ACC Integration Partner, App Store. Eligible to apply from day one. | Q2 |
| **RCW Migration Pipeline** — Autodesk contact with enterprise clients for Revit Cloud Worksharing | up to 5 clients |
| **New practice / vertical** — Differentiation from generic staff aug. Higher margins, recurring product revenue. | CAD/PLM |

### Center banner:

**This is happening. The question is whether Team International is part of the story.**

### Bottom: IMMEDIATE ACTIONS

1. Close QuikTrip engagement
2. Deliver Autodesk May demo
3. Apply for Partner Programs
4. Scope RCW migrations
5. Present at DevCon Virtual

---

## Slide 6 — Next Steps

1. **Form the practice. I lead it from April.** — Current project ends — I'm ready. Product, clients, and contacts come with me.
2. **QuikTrip and RCW migrations under TI** — Revenue pipeline active from day one. Enterprise reference case.
3. **Autodesk May demo + Partner Programs** — APS Certified Partner, ACC Integration Partner — TI on the Autodesk map.
4. **DevCon Virtual — TI as the industry voice** — Thousands of developers. New inbound pipeline.

**The plan is in motion. Let's do it together.**

---

### Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| QuikTrip deal delays to Q3 | RCW migration pipeline (up to 5 clients) fills the gap. DevCon inbound starts Q3. Conservative scenario still net positive Y1. |
| Autodesk rebuilds their own CLI | RAPS has 2+ years head start, 230+ commands, 114 MCP tools, SaaS cloud, marketplace. 579 commits in 2 months — we ship faster. Symbiotic positioning — they're more likely to partner than compete. |
| Key-person dependency (me) | First Sr. Dev hire starts knowledge transfer Q2-Q3. RAPS codebase documented and tested (14 CI/CD workflows, 12-crate workspace, 13 bundled skills, diagnostic doctor command). Ukrainian BIM network is the hiring pipeline. |

---
---

# PART 2: SPEAKER SCRIPT

**6 slides. 3-5 minutes. Then Q&A.**
**Guilherme opens with 30-second endorsement.**

---

### GUILHERME — Opening (30 sec)

> *(Guilherme introduces context: he facilitated the QuikTrip connection, has seen the traction firsthand, and believes the timing is right for TI to move on this.)*

---

### SLIDE 1 — Title (10 sec)

> I want to talk about a paradigm shift. I've spent 10+ years on both sides — manufacturing engineering and software development. That combination is rare, and it's exactly what this industry needs right now.

---

### SLIDE 2 — Inflection Point (60 sec)

> **[Left]** $80 billion industry, zero modern engineering practices. AI is rewriting workflows everywhere — AEC hasn't started. Global instability demands efficiency. The core problem: engineers don't code, coders don't understand engineering.
>
> **[Right]** Autodesk is creating a vacuum. 7% layoffs. Forced BIM360 to ACC migration with no tooling. Customer requests ignored for years. They archived their own CLI. But here's the thing — they know it. That's why their Director of Platform Services reached out personally and invited us to present.
>
> **[Center]** This is not about selling tools. It's about leading the paradigm shift to effective engineering.
>
> **[Bottom]** The companies that define AEC engineering practices now own the decade.

---

### SLIDE 3 — What We Have (60 sec)

> RAPS Platform — 230+ commands, 114 MCP tools, 16 APIs. CLI, hosted MCP server, SaaS cloud on Cloudflare, marketplace with Stripe billing. Python bindings. Docker, Kubernetes. 579 commits in the last two months. Rust v5.6. This is not a prototype — it's production software with a commercial backend.
>
> 10+ years in manufacturing AND software. Expert Elite, ADN. This combination barely exists.
>
> 4,295 ACC feature requests analyzed across 4 vendors. No public research like this exists.
>
> **Right:** QuikTrip — Blake Pettus, Design Project Manager at a $14B company, sent a detailed 8-item wish list and is actively scheduling calls. Cyrille Fauvel — Director of Platform Services & Ecosystem at Autodesk — personally invited me and scheduled a demo in May. DevCon Virtual — 3 sessions. Michael Beale at Autodesk — collaboration, Slack, and a pipeline of up to 5 enterprise RCW migration clients.

---

### SLIDE 4 — Revenue + Timeline (45 sec)

> Evangelism creates revenue. Solve their problems — consulting. RAPS Platform — paid tiers. Embed our people — staff aug. All three need someone who bridges engineering and code.
>
> The plan: Q2 — close QuikTrip, deliver Autodesk demo, DevCon. Q3 — scale with a team, convert inbound. Q4 — expand cross-platform.

---

### SLIDE 5 — The Opportunity (45 sec)

> **[Left]** Here's what I bring. A production platform — not just a CLI, but a SaaS cloud backend, a marketplace with Stripe billing, 114 MCP tools, 16 APIs. An enterprise client in active discussions — $14B company with a documented wish list, not a cold lead. Director-level Autodesk access with a May demo scheduled. And a network of 50+ specialists in the Ukrainian BIM community — architects, engineers, developers — that becomes our hiring pipeline.
>
> **[Right]** Here's what TI gets. A new revenue stream from month one. Eligibility for Autodesk Partner Programs — APS Certified Partner, ACC Integration Partner, App Store — all require a company entity. An RCW migration pipeline with up to 5 enterprise clients. And a differentiated practice — not generic staff aug, but domain expertise with product revenue.
>
> **[Bottom]** This is happening. The question is whether Team International is part of the story.

---

### SLIDE 6 — Close (20 sec)

> Four steps. One — form the practice, I lead it from April. Two — QuikTrip and RCW migrations under TI. Three — Autodesk May demo plus Partner Programs. Four — DevCon Virtual, TI as the industry voice.
>
> The plan is in motion. Let's do it together.

**[Stop. Wait.]**

---

### Q&A CHEAT SHEET

| Question | Answer |
|----------|--------|
| **Is RAPS a real product?** | Full platform. 230+ commands, 114 MCP tools, 16 APIs. Hosted MCP server. SaaS cloud on Cloudflare (Workers, D1, R2). Marketplace with Stripe billing at buy.rapscli.xyz. Python bindings. Docker, Kubernetes Helm charts. 14 CI/CD workflows. Plugin signing (Ed25519). 579 commits in 2 months. Rust v5.6. |
| **What makes you uniquely qualified?** | 10+ years on both sides. Manufacturing (Vault, Inventor, AutoCAD) AND software (Rust, Python, APIs). Autodesk's Director of Platform Services personally invited me. QuikTrip came to us. |
| **How real is QuikTrip?** | Blake Pettus, Design Project Manager, sent a detailed 8-item wish list on March 3. Scheduled multiple calls. Last email March 9 asking to meet. Active engagement — not a signed contract yet, but a client with documented needs who is investing time. We're in closing discussions. |
| **How real is the Autodesk connection?** | Cyrille Fauvel — Director, Platform Services & Ecosystem, PSET. Emailed me personally, invited to DevCon Virtual, immediately shared a Zoom link. His team member sent Speaker Workshop materials. Working relationship, not a LinkedIn connection. |
| **RCW migration pipeline?** | An Autodesk engineer has identified up to 5 enterprise clients needing RCW migration tooling and offered to connect us once we ship the feature. The migration command fits naturally into RAPS. |
| **What does TI get that I can't do alone?** | Three things. **First:** Autodesk Partner Programs — APS Certified Partner, ACC Integration Partner, App Store. All require a company entity — eligible to apply from day one with TI. **Second:** enterprise credibility — legal, contracts, a name that a $14B company can sign with. **Third:** my 50+ person Ukrainian BIM network plus TI's hiring infrastructure = specialized AEC team fast. |
| **What if it doesn't work out?** | Worst case, we've built AEC domain expertise into TI's bench — that's valuable regardless. Best case — and I believe this is where we are — we've built a practice. There's a product, active client discussions, Autodesk access, and a pipeline. |
| **What if QuikTrip delays?** | RCW migration pipeline fills the gap. DevCon inbound starts Q3. RAPS licensing generates recurring revenue independently. The practice isn't single-client dependent. |
| **Key-person risk?** | First Sr. Dev hire starts knowledge transfer from Q2. RAPS codebase is documented — 14 CI/CD workflows, 12-crate workspace, 13 bundled skills, diagnostic doctor command. Ukrainian BIM network is the hiring pipeline for AEC-specialized talent. |
| **Investment?** | Fully loaded including me: $143-187K Year 1 against $165-250K revenue. Hires phased with engagements. Even if QuikTrip slips to Q3, we break even by year end. |
| **How does AI fit?** | RAPS has 114 MCP tools at mcp.rapscli.xyz. Autodesk insiders are converging on the same conclusion — AI-assisted engineering is the norm. We're already there. |
| **BIM 360 legacy customers?** | RAPS supports both ACC and BIM 360 with automatic fallback. Customers don't need to have migrated yet — we handle both. |
| **What shipped recently?** | 579 commits in 2 months. SaaS cloud backend (multi-tenant, encrypted, WebSocket job progress). Marketplace with Stripe at buy.rapscli.xyz. Permission clone/export for bulk audits. TUI dashboard expanded to 7 tabs, 33 views. Skill system with 13 bundled skills. Diagnostic doctor command. BIM 360 backward compatibility. |
| **How big is the Ukrainian BIM network?** | 50+ specialists — architects, mechanical engineers, structural engineers, Revit/Inventor developers, APS developers. Active in Ukrainian Autodesk community. Professional network built over 10+ years, not a formal organization. |
| **Guilherme?** | *(Guilherme: "I facilitated the QuikTrip introduction. The opportunity is real and timely.")* |

---
---

# PART 3: ANALYTICS DATA

---

## ROI Projections — Phased Investment Model

### Revenue Breakdown

| Revenue Stream | Q2 2026 | Q3 2026 | Q4 2026 | Year 1 Total | Type |
|---------------|---------|---------|---------|-------------|------|
| Integration Consulting | $15-25K | $40-60K | $60-80K | $115-165K | Project-based |
| RAPS Platform Licensing | — | $5-10K | $15-25K | $20-35K | Recurring (MRR) |
| AEC Staff Augmentation | — | $10-20K | $20-30K | $30-50K | Steady baseline |
| **TOTAL** | **$15-25K** | **$55-90K** | **$95-135K** | **$165-250K** | |

### Conservative Scenario (QuikTrip closes Q3)

| Revenue Stream | Q2 2026 | Q3 2026 | Q4 2026 | Year 1 Total |
|---------------|---------|---------|---------|-------------|
| Integration Consulting | $0 | $25-40K | $60-80K | $85-120K |
| RAPS Platform Licensing | — | $5-10K | $15-25K | $20-35K |
| AEC Staff Augmentation | — | $10-20K | $20-30K | $30-50K |
| **TOTAL** | **$0** | **$40-70K** | **$95-135K** | **$135-205K** |

*Even in conservative scenario, practice breaks even to net positive by Year 1 end.*

### Cost Breakdown (fully loaded)

| Cost Item | Q2 2026 | Q3 2026 | Q4 2026 | Year 1 Total | Notes |
|-----------|---------|---------|---------|-------------|-------|
| Practice Lead (me) | $7K/mo | $7K/mo | $7K/mo | $63K | Reallocation from current project |
| Senior Dev | — | $8-12K/mo | $8-12K/mo | $48-72K | Hire Q2-Q3 |
| Mid Dev | — | $5-8K/mo | $5-8K/mo | $20-32K | Hire Q3, phased with revenue |
| Sales / BD | — | $3-5K/mo | $3-5K/mo | $12-20K | Hire Q3 |
| **TOTAL (fully loaded)** | **$7K/mo** | **$23-32K/mo** | **$23-32K/mo** | **$143-187K** | |

*My salary is not a new expense — I'm reallocated from a project ending April. Shown for full transparency.*

### Summary

| Scenario | Year 1 Revenue | Year 1 Cost (fully loaded) | Net |
|----------|---------------|---------------------------|-----|
| **Base case** | $165-250K | $143-187K | +$22-63K |
| **Conservative** | $135-205K | $143-187K | -$8K to +$62K (break-even to positive) |
| **Upside (strong DevCon)** | $250-350K | $143-187K | +$107-163K |

---

## Cross-Platform Pain Point Matrix

| Pain Point | Autodesk | PTC Onshape | Dassault 3DX | Siemens TC/NX | Opportunity |
|------------|----------|-------------|--------------|---------------|-------------|
| Auth / permissions | **HIGH** | **HIGH** | **HIGH** | **HIGH** | Auth CLI helper |
| Translation failures | **HIGH** | **HIGH** | **HIGH** | MEDIUM | Translation manager |
| SDK version conflicts | **HIGH** | MEDIUM | **CRITICAL** | **HIGH** | Compatibility checker |
| Documentation gaps | MEDIUM | MEDIUM | **HIGH** | **HIGH** | Resource hub |
| Webhook reliability | MEDIUM | **HIGH** | NEW (2025) | MEDIUM | Test toolkit |
| Bulk admin tooling | **NO TOOLING** | LIMITED | **NO TOOLING** | LIMITED | RAPS bulk ops |
| AI/MCP integration | BASIC* | NONE | NONE | NONE | 114 MCP tools |

*\*One community-built basic MCP server (Petr Broz). RAPS: 110+ production tools.*

---

## Research Methodology

| Metric | Value |
|--------|-------|
| ACC feature requests scraped | **4,295** |
| App Store apps audited | **4,078** |
| Requests still "gathering support" | **96.6%** |
| Autodesk implementation rate | **1.4%** |

| Source | Volume | Method | Key Findings |
|--------|--------|--------|-------------|
| ACC Ideas Forum | 4,295 ideas | Full scrape + analysis | Permission errors #1 (3,628 votes). 96.6% unresolved. |
| Autodesk App Store | 4,078 apps | Full scrape + gap analysis | Zero CLI tools, zero auth helpers, zero MCP tools. |
| Stack Overflow (APS) | 4,582+ questions | Tag-based analysis | No CAD/PLM segment in Developer Survey. |
| Cross-platform | PTC, Dassault, Siemens | Forum + docs review | Same pain patterns across all vendors. |
| Analyst reports | CIMdata, ABI, Forrester | Report review | Zero developer experience coverage across vendors. |

---

## Competitive Landscape

| Player | What They Do | Gap We Fill |
|--------|-------------|-------------|
| **Autodesk (internal)** | Creating vacuum — archived CLI, reduced dev support. | We fill the vacuum. Symbiotic — they invited us in. |
| **IMAGINiT ACCelerate** | ACC admin via web UI only. | RAPS: CLI + MCP + Cloud. Scriptable. 230+ cmds. |
| **BIM load** | Project setup. ~5% of RAPS scope. | Full platform: 16 APIs, bulk ops, DA, AI. |
| **Petr Broz** | Community expert. Basic MCP. | RAPS: 114 MCP tools. Hosted. Paid tiers. |
| **Generic consultancies** | No domain expertise. | Dual expertise = moat. |

---

## Autodesk App Store Gap (4,078 Apps Analyzed)

| Category | Existing Apps | RAPS Opportunity | Competition |
|----------|:------------:|-----------------|:-----------:|
| Design Automation CLI tools | 0 | First mover | **ZERO** |
| APS authentication helpers | 0 | First mover | **ZERO** |
| Translation debugging utilities | 0 | First mover | **ZERO** |
| ACC admin automation | 1 (web UI only) | CLI + MCP + Cloud (scriptable) | MINIMAL |
| Cross-platform CLI (any vendor) | 0 | Category creator | **ZERO** |
| MCP/AI integration tools | 0 | Category creator (110+ tools) | **ZERO** |

---

## SEO — Developer Search Demand

| Category | Example Searches | Current Answer | Our Play |
|----------|-----------------|----------------|----------|
| Auth errors | "APS 403", "onshape 401" | Forum posts | rapscli.xyz guide + RAPS |
| Translation failures | "TranslationWorker-InternalFailure" | Nothing | Debugger tool + guide |
| Bulk operations | "ACC bulk add users" | Nothing | RAPS CLI (built) |
| AI + CAD/PLM | "MCP server APS" | Basic community tool | RAPS 114 MCP tools |
| CLI tooling | "Autodesk CLI", "forge cli" | Archived forge-cli | RAPS (replacement) |

**Flywheel: rapscli.xyz (6 live tools, 35 blog posts, 73 cookbook recipes, 72 docs pages) captures traffic → RAPS users → consulting clients.**

---

## Appendix: RAPS Domain Logic (Technical Detail)

*For technical stakeholders if asked "what makes RAPS hard to replicate?"*

| Capability | RAPS Implementation | Why It Matters |
|-----------|-------------------|----------------|
| **Chunked uploads** | Adaptive sizing, 5 concurrent, 3 retries/chunk, resumable | Auto-gen SDKs do single POST. Large files (>100MB) fail. |
| **OAuth race conditions** | Mutex + Notify pattern. Singleton promise in Rust. | Concurrent requests cause token invalidation. Official SDKs ignore this. |
| **Failure classification** | 13 failure types, 3 backoff strategies, circuit breaker | Generic retries waste hours. Smart retries save hours. |
| **Bulk admin operations** | 4 ops, 10 concurrent workers, resumable state | QuikTrip: 1,700 projects. No other tool does this. |
| **Permission clone/export** | Clone across projects, bulk CSV export/import, audit trails | Customers need to replicate permission structures at scale. No other tool does this. |
| **SaaS cloud backend** | Multi-tenant with RLS, AES-256-GCM encryption, JWT + Argon2, WebSocket job progress | Not just a CLI — a full cloud platform with job orchestration. |
| **Plugin marketplace** | Stripe billing, Ed25519 signing, license validation, per-seat subscriptions | Commercial infrastructure ready for enterprise distribution. |

---

## Bottom Line

**4,295 feature requests analyzed. 4,078 apps audited. 96.6% unresolved by Autodesk. Zero competition in 5 of 6 categories. A production platform (230+ commands, 114 MCP tools, 16 APIs, SaaS cloud, marketplace with Stripe), an active enterprise engagement (QuikTrip), confirmed Autodesk access, and rare dual expertise. 579 commits in 2 months. The question is not IF — it is WHO captures it first.**

---

*Prepared by Dmytro Yemelianov | Primary: ACC Ideas (4,295), App Store (4,078), Stack Overflow (4,582+). Supplementary: cross-platform community observation (PTC, Dassault, Siemens) | Dec 2025 — Mar 2026*
