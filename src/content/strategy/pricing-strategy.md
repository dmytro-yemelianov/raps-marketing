# RAPS Platform Pricing Strategy

> **Last updated**: 2026-03-15
> **Target segment**: AEC firm IT/BIM teams (500+ ACC projects)
> **Positioning**: Premium — the only CLI toolkit in a 259-app marketplace
> **Billing**: Monthly + Annual (20% annual discount)

---

## Table of Contents

1. [Pricing Philosophy](#1-pricing-philosophy)
2. [Tier Structure](#2-tier-structure)
3. [CLI Feature Gating](#3-cli-feature-gating)
4. [MCP Gateway Pricing](#4-mcp-gateway-pricing)
5. [Consulting & Services](#5-consulting--services)
6. [Competitive Positioning](#6-competitive-positioning)
7. [Revenue Projections](#7-revenue-projections)
8. [Pricing Page Copy](#8-pricing-page-copy)
9. [Implementation Notes](#9-implementation-notes)
10. [Pricing Evolution Roadmap](#10-pricing-evolution-roadmap)

---

## 1. Pricing Philosophy

### Value Anchor

RAPS doesn't compete on features against other AEC tools. It competes against **manual labor**. The pricing is anchored to time saved, not to competing products.

**Blake's math** (1,700 ACC projects):
- Adding one user to all projects manually: ~3-4 full workdays (1,700 clicks, page loads, confirmations)
- With RAPS: one command, 4 minutes
- At $75/hr BIM manager rate: **$2,400 saved per user onboarding event**
- A firm doing 10 onboardings/offboardings per month saves **$24,000/month**

RAPS at $499/month is a **48x ROI** on this one workflow alone.

### Principles

1. **Free tier is generous enough to prove value** — basic CLI commands let teams evaluate without a sales call
2. **Professional tier is the wedge** — bulk operations and cross-project dashboards solve the #1 ACC pain point (344 kudos, 6+ years unresolved)
3. **Enterprise tier is the expansion** — automation, provisioning, and analytics for portfolio-scale operations
4. **Per-seat pricing with a floor** — minimum 3 seats for Professional, 5 for Enterprise. Prevents single-user arbitrage at enterprise firms
5. **Annual commits get meaningful discount** — 20% off, because AEC firms budget annually and longer commitments reduce churn
6. **MCP Gateway available standalone** — captures the "AI for construction" buyer who doesn't need the full platform

---

## 2. Tier Structure

### Free (Starter)

**Price**: $0 forever

**CLI**:
- Authentication (login, logout, status, test)
- OSS Buckets (list, create, get, delete)
- OSS Objects (list, upload, download, info — single files only)
- Model Derivative (translate start, translate status — 5/month limit)
- Data Management reads (hub list, hub info, project list, project info, folder contents)
- Webhooks (list, create, delete — 3 active webhooks max)

**Web Tools** (3):
- Bucket Manager
- Model Translator
- Webhook Console

**MCP Server**: Not included

**Limits**:
- 1 user
- 100 API calls/day via CLI
- No bulk operations
- No pipeline engine
- No job queue
- Community support only (GitHub Issues)

**Purpose**: Evaluation, individual developers, students, hobbyists. Enough to experience the CLI and see the value of automation.

---

### Professional

**Price**: $49/user/month ($39/user/month billed annually)

**Minimum**: 3 seats ($147/month or $1,404/year)

**Everything in Free, plus:**

**CLI**:
- All read/write commands across all 12 API domains
- Bulk operations: `admin user add/remove/update`, `admin user list`, `admin folder set-permissions`
- CSV import/export for all entities
- Report generation (issues summary, RFI summary)
- `workflow` compound commands (prepare-for-viewing, batch-translate, compare-versions, analyze-model, setup-project)
- Pipeline engine: run, validate, dry-run (up to 10 pipeline executions/day)
- 5,000 API calls/day per seat

**Web Tools** (3 + 4 = 7):
- Bulk User Manager
- Issue Tracker Pro
- RFI Dashboard
- Folder Permissions Manager

**MCP Server**: Included (50 requests/hour per seat)

**Support**: Email support, 48-hour response SLA

**Purpose**: BIM teams managing 100-1,000 ACC projects. Day-to-day bulk operations, cross-project visibility, user management.

---

### Enterprise

**Price**: $99/user/month ($79/user/month billed annually)

**Minimum**: 5 seats ($495/month or $4,740/year)

**Everything in Professional, plus:**

**CLI**:
- Pipeline engine: unlimited executions, scheduled pipelines (cron), serverless dispatch
- Job queue: background job submission and management
- Swarm orchestration: distributed multi-worker execution
- Safeguard: data protection, compliance checks, rollback scripts
- Snapshot: point-in-time data captures
- Sync: file synchronization across environments
- Dashboard commands: visual resource dashboards
- Unlimited API calls

**Web Tools** (7 + 4 = 11):
- Project Provisioner
- Portfolio Reporter
- Design Automation Studio
- Reality Capture Manager

**MCP Server**: Included (200 requests/hour per seat)

**Support**: Priority email, 24-hour response SLA, onboarding call, quarterly review

**Additional**:
- Custom pipeline templates
- Audit log export
- SSO/SAML (when implemented)
- Dedicated Slack channel (10+ seats)
- Early access to new features

**Purpose**: Enterprise AEC firms managing 1,000+ ACC projects. Full automation, provisioning, portfolio analytics, CI/CD for construction workflows.

---

### Enterprise Custom

**Price**: Custom quote (starting at $20,000/year)

**For firms that need**:
- Unlimited seats
- Self-hosted MCP Gateway
- Custom integrations
- Dedicated infrastructure (isolated Workers)
- On-premise deployment option
- SLA with uptime guarantees
- Custom training and onboarding
- Direct engineering support

**Purpose**: Large GCs, ENR Top 100 firms, firms with compliance/security requirements that need custom deployment.

---

## 3. CLI Feature Gating

### How It Works

The CLI already has license key validation infrastructure. Feature gating maps CLI command groups to tiers:

| Command Group | Free | Professional | Enterprise |
|---------------|------|--------------|------------|
| `auth` | Yes | Yes | Yes |
| `bucket` | Yes | Yes | Yes |
| `object` (single file) | Yes | Yes | Yes |
| `object` (batch/resume/parallel) | — | Yes | Yes |
| `hub`, `project` (read) | Yes | Yes | Yes |
| `project` (write/create) | — | Yes | Yes |
| `folder`, `item` | Yes | Yes | Yes |
| `translate` | 5/mo | Yes | Yes |
| `webhook` | 3 active | Yes | Yes |
| `issue`, `rfi` (read) | Yes | Yes | Yes |
| `issue`, `rfi` (write) | — | Yes | Yes |
| `acc` (checklists, assets, submittals) | — | Yes | Yes |
| `admin` (bulk user/folder ops) | — | Yes | Yes |
| `report` | — | Yes | Yes |
| `workflow` | — | Yes | Yes |
| `da` (Design Automation) | — | — | Yes |
| `reality` | — | — | Yes |
| `pipeline` (basic) | — | 10/day | Unlimited |
| `pipeline` (cron, serverless) | — | — | Yes |
| `job` | — | — | Yes |
| `swarm` | — | — | Yes |
| `safeguard` | — | — | Yes |
| `snapshot`, `sync` | — | — | Yes |
| `template` | — | Yes | Yes |
| MCP Server | — | 50 req/hr | 200 req/hr |

### License Key Flow

```
User installs CLI (free)
  → raps auth login (works immediately)
  → raps bucket list (works immediately)
  → raps admin user add (blocked: "This command requires a Professional license. Upgrade at rapscli.xyz/pricing")
  → raps activate <license-key> (unlocks Professional commands)
```

The infrastructure for this already exists in the subscription middleware and license key tables.

---

## 4. MCP Gateway Pricing

### Bundled (included in Professional/Enterprise)

As described in tier structure above. Rate limits per seat.

### Standalone — "RAPS AI Connect"

For teams that want AI assistants (Claude, GPT, Copilot) to operate Autodesk APIs without adopting the full CLI platform.

**Pricing**:

| Plan | Price | Rate Limit | Seats |
|------|-------|------------|-------|
| AI Starter | $29/month ($23/mo annual) | 100 req/hr | 1 |
| AI Team | $99/month ($79/mo annual) | 500 req/hr | 5 |
| AI Enterprise | $249/month ($199/mo annual) | 2,000 req/hr | Unlimited |

**What's included**:
- 114 MCP tools across 12 Autodesk API domains
- Hosted MCP Gateway (no infrastructure to manage)
- Works with Claude Code, Claude Desktop, Cursor, Windsurf, any MCP-compatible client
- APS credential injection (user provides their own APS client credentials)

**What's NOT included**:
- CLI commands
- Web tools
- Pipeline engine
- Support beyond documentation

**Upgrade path**: AI Connect customers can upgrade to Professional/Enterprise at any time. AI Connect subscription is credited toward the first month of the platform tier.

---

## 5. Consulting & Services

### Integration Consulting

For firms that need custom workflows, pipeline development, or integration with existing systems.

| Service | Rate | Typical Engagement |
|---------|------|--------------------|
| Pipeline Development | $200/hr | 10-40 hours. Custom YAML pipelines for client-specific workflows (onboarding, reporting, compliance) |
| ACC Integration | $200/hr | 20-80 hours. Connect RAPS with client's ERP, HR, or project management systems |
| Migration Support | $175/hr | 10-30 hours. Migrate from manual processes or legacy scripts to RAPS pipelines |
| Architecture Review | $250/hr | 4-8 hours. Review client's APS integration strategy, recommend RAPS-based solutions |

**Packaged offerings**:

| Package | Price | What's Included |
|---------|-------|-----------------|
| Quick Start | $2,500 | 4-hour onboarding call + 3 custom pipelines + documentation. For teams with 100-500 projects. |
| Professional Onboarding | $7,500 | 2-day on-site/remote workshop + 10 custom pipelines + CI/CD integration + 30 days email support |
| Enterprise Deployment | $15,000-$30,000 | Full deployment plan + custom pipelines + SSO setup + training for 10+ users + 90 days priority support |

### Staff Augmentation

For firms that need ongoing APS/ACC automation expertise embedded in their team.

| Engagement | Rate | Duration |
|------------|------|----------|
| Part-time (20 hrs/week) | $8,000/month | 3-month minimum |
| Full-time (40 hrs/week) | $14,000/month | 6-month minimum |

**Scope**: Build and maintain RAPS pipelines, custom integrations, Design Automation appbundles, webhook-driven workflows, reporting dashboards.

### Training

| Format | Price | Duration |
|--------|-------|----------|
| Self-paced online course | Included with Pro/Enterprise | N/A |
| Live virtual workshop (group) | $1,500 per session | 3 hours, up to 15 attendees |
| On-site training | $3,500/day + travel | Full day, up to 20 attendees |

---

## 6. Competitive Positioning

### Why RAPS is premium-priced

| Factor | RAPS | Alternatives |
|--------|------|--------------|
| CLI for ACC | Only one (zero competitors in 259-app marketplace) | None |
| MCP/AI integration | First and only for Autodesk APIs | None |
| Bulk user management | One command, 4 minutes for 1,700 projects | 1,700 manual clicks, 3-4 days |
| Pipeline orchestration | Built-in DAG engine with retry, cron, serverless | Build custom with Zapier/Make ($200-6,000/mo for comparable volume) |
| Cross-project visibility | Issues, RFIs, permissions across all projects | ACC only shows one project at a time |

### Price positioning vs. market

```
                        ┌─────────────────────────────────────────┐
                        │        Enterprise / Platform            │
  $100K+/yr             │  Procore ($25-100K/yr)                  │
                        │  Oracle Aconex (custom)                 │
                        │  OpenSpace ($10K+/project)              │
                        ├─────────────────────────────────────────┤
                        │        Mid-Market / Team                │
  $5-20K/yr             │  RAPS Enterprise ($4,740-$9,480/yr) ◄── │
                        │  Assemble ($7,500/yr)                   │
                        │  BIM Track Enterprise ($79/user/mo)     │
                        ├─────────────────────────────────────────┤
                        │        Entry / Individual               │
  $500-5K/yr            │  RAPS Professional ($1,404-$1,764/yr) ◄─│
                        │  Fieldwire Pro ($39/user/mo)            │
                        │  Bluebeam ($260-440/user/yr)            │
                        │  BIM Track Pro ($49/user/mo)            │
                        ├─────────────────────────────────────────┤
                        │        Free / Freemium                  │
  $0                    │  RAPS Free ◄────────────────────────────│
                        │  Fieldwire Basic (free)                 │
                        │  BIM Track Free (50 issues)             │
                        └─────────────────────────────────────────┘
```

### Key insight

ACC users already pay $1,625+/user/year for the base platform. RAPS Professional at $468/user/year (annual) is a **29% add-on** that multiplies the value of their existing ACC investment. This is easy to justify in any budget conversation.

---

## 7. Revenue Projections

### Assumptions

- Launch: Q2 2026 (aligned with DevCon April 15-16)
- Growth model: bottoms-up, driven by Product Hunt launch + pSEO + directory listings
- Average seats per customer: 5 (Professional), 8 (Enterprise)
- Monthly churn: 3% (Professional), 1.5% (Enterprise)
- Mix: 70% annual / 30% monthly billing

### Year 1 Scenarios

#### Conservative (5 paying customers by end of Year 1)

| Quarter | New Customers | Cumulative | Mix | Quarterly Revenue |
|---------|--------------|------------|-----|-------------------|
| Q2 2026 | 1 Pro (3 seats) | 1 | Pro only | $441 |
| Q3 2026 | 1 Pro (5 seats), 1 Ent (5 seats) | 3 | 2 Pro, 1 Ent | $3,615 |
| Q4 2026 | 1 Ent (8 seats) | 4 | 2 Pro, 2 Ent | $6,636 |
| Q1 2027 | 1 Ent (10 seats) | 5 | 2 Pro, 3 Ent | $10,446 |
| **Year 1 Total** | | | | **$21,138** |

Plus consulting: 2 Quick Starts ($5,000) + 1 Professional Onboarding ($7,500) = **$12,500**

**Year 1 Total (Conservative): ~$33,600**

#### Base Case (12 paying customers by end of Year 1)

| Quarter | New Customers | Cumulative | Mix | Quarterly Revenue |
|---------|--------------|------------|-----|-------------------|
| Q2 2026 | 2 (1 Pro, 1 Ent) | 2 | 1 Pro, 1 Ent | $2,361 |
| Q3 2026 | 3 (2 Pro, 1 Ent) | 5 | 3 Pro, 2 Ent | $7,839 |
| Q4 2026 | 4 (2 Pro, 2 Ent) | 9 | 5 Pro, 4 Ent | $17,016 |
| Q1 2027 | 3 (1 Pro, 2 Ent) | 12 | 6 Pro, 6 Ent | $24,948 |
| **Year 1 Total** | | | | **$52,164** |

Plus consulting: 4 Quick Starts ($10,000) + 2 Professional Onboardings ($15,000) + 1 Enterprise Deployment ($20,000) = **$45,000**

**Year 1 Total (Base Case): ~$97,000**

#### Optimistic (25 paying customers by end of Year 1)

Includes 1 Enterprise Custom deal at $25,000/year.

**Year 1 Total (Optimistic): ~$180,000-$220,000**

### MCP Gateway Standalone (Additional)

| Quarter | AI Connect Subscribers | Quarterly Revenue |
|---------|----------------------|-------------------|
| Q2 2026 | 3 | $261 |
| Q3 2026 | 8 | $696 |
| Q4 2026 | 15 | $1,305 |
| Q1 2027 | 25 | $2,175 |
| **Year 1 Total** | | **$4,437** |

MCP Gateway standalone is a small revenue line initially but serves as a lead-gen funnel for platform upgrades.

---

## 8. Pricing Page Copy

### Headline

> **Automate Autodesk Construction Cloud at any scale**

### Subheadline

> From single-file uploads to managing 1,700 projects with one command. Choose the plan that matches your operation.

### Tier Cards

#### Free
> **$0** / forever
>
> For individual developers evaluating the platform.
>
> - 3 web tools (Bucket Manager, Model Translator, Webhook Console)
> - Basic CLI commands (auth, buckets, objects, translate)
> - 100 API calls/day
> - Community support

#### Professional
> **$49** /user/month
> $39/user/month billed annually — save 20%
> Minimum 3 seats
>
> For BIM teams managing projects at scale.
>
> - **Everything in Free, plus:**
> - 7 web tools including Bulk User Manager, Issue Tracker Pro
> - All CLI commands including bulk admin operations
> - Pipeline engine (10 runs/day)
> - MCP Server for AI assistants (50 req/hr)
> - CSV import/export for all entities
> - Cross-project reporting
> - 5,000 API calls/day per seat
> - Email support (48hr SLA)

#### Enterprise
> **$99** /user/month
> $79/user/month billed annually — save 20%
> Minimum 5 seats
>
> For enterprise firms with portfolio-scale automation needs.
>
> - **Everything in Professional, plus:**
> - 11 web tools including Project Provisioner, Portfolio Reporter
> - Unlimited pipeline executions with cron scheduling
> - Serverless dispatch and swarm orchestration
> - MCP Server (200 req/hr)
> - Design Automation Studio
> - Reality Capture Manager
> - Audit log export
> - Priority support (24hr SLA)
> - Onboarding call + quarterly reviews
> - Dedicated Slack channel (10+ seats)

#### Enterprise Custom
> **Custom pricing**
>
> For organizations requiring dedicated infrastructure, SLAs, or custom integrations.
>
> - Unlimited seats
> - Self-hosted options
> - Custom SLA with uptime guarantees
> - Dedicated engineering support
> - Custom training program
>
> [Contact Sales →]

### FAQ Section

**Q: Do I need an Autodesk subscription to use RAPS?**
A: Yes. RAPS automates your existing Autodesk Construction Cloud (ACC) and APS workflows. You need your own APS client credentials (Client ID and Secret) or an active ACC account.

**Q: What's the difference between CLI and web tools?**
A: The CLI is a terminal-based interface for power users and automation scripts. Web tools provide visual dashboards for the same operations — no terminal required. Both are included in your plan.

**Q: Can I try Professional features before committing?**
A: Yes. Contact us for a 14-day Professional trial with full access to all features.

**Q: What counts as a "seat"?**
A: Each person who uses RAPS (CLI or web tools) needs a seat. Service accounts for CI/CD pipelines also count as a seat.

**Q: Is there a per-project or per-API-call pricing?**
A: No. All plans include generous API call limits. We don't charge per project — whether you manage 10 or 10,000 projects, the price per seat stays the same.

**Q: What happens if I exceed the API call limit?**
A: We'll notify you. For short-term spikes, we don't enforce hard limits. For sustained overages, we'll work with you to find the right plan.

**Q: Do you offer discounts for nonprofits or educational institutions?**
A: Yes. Contact us for 50% off any plan.

---

## 9. Implementation Notes

### What's Already Built

The subscription infrastructure is production-ready:

- **3-tier model** in `apps/shell/src/routes/tools.ts` (entry/professional/enterprise)
- **D1 schema** with subscriptions, customers, usage_events, licenses tables
- **Subscription middleware** in `src/middleware/subscription.ts` — validates tier + entitled_tools
- **License key system** — generate, validate, revoke
- **Stripe integration** — checkout sessions, webhooks, refunds, balance queries
- **Admin console** — subscriptions, customers, payments, licenses, usage analytics
- **MCP Gateway** — per-license rate limiting, credential injection, Durable Objects isolation

### What Needs To Be Built

| Component | Priority | Effort | Notes |
|-----------|----------|--------|-------|
| CLI license key activation (`raps activate`) | High | 2-3 days | Add `activate` command, store key in `~/.config/raps/license.json`, validate on gated commands |
| CLI feature gate checks | High | 3-5 days | Middleware in command dispatch that checks license tier before executing gated commands |
| Stripe price IDs for new tiers | High | 1 day | Create Products + Prices in Stripe Dashboard matching the tier structure |
| Pricing page on rapscli.xyz | High | 2-3 days | Astro page with tier cards, FAQ, checkout flow |
| Trial flow (14-day Professional) | Medium | 2 days | Auto-create trial subscription on signup, send reminder emails at day 7, 12, 14 |
| Usage metering (API calls/day) | Medium | 3 days | Count calls per seat per day, enforce limits at middleware level |
| Seat management UI | Medium | 2 days | Admin can add/remove seats, view who's using what |
| MCP Gateway standalone checkout | Medium | 1-2 days | Separate Stripe product for AI Connect plans |
| Invoice / receipt emails | Low | 1 day | Stripe handles this natively with Stripe Billing |
| SSO/SAML for Enterprise | Low | 5-7 days | Future — implement when first Enterprise customer requests it |

### Stripe Product Structure

```
Products:
├── RAPS Professional
│   ├── Price: $49/mo (monthly)
│   ├── Price: $39/mo ($468/yr billed annually)
│   └── Quantity: per-seat, minimum 3
├── RAPS Enterprise
│   ├── Price: $99/mo (monthly)
│   ├── Price: $79/mo ($948/yr billed annually)
│   └── Quantity: per-seat, minimum 5
├── RAPS AI Connect Starter
│   ├── Price: $29/mo (monthly)
│   └── Price: $23/mo ($276/yr billed annually)
├── RAPS AI Connect Team
│   ├── Price: $99/mo (monthly)
│   └── Price: $79/mo ($948/yr billed annually)
└── RAPS AI Connect Enterprise
    ├── Price: $249/mo (monthly)
    └── Price: $199/mo ($2,388/yr billed annually)
```

---

## 10. Pricing Evolution Roadmap

### Phase 1: Launch (Q2 2026)

- Free + Professional + Enterprise tiers
- CLI feature gating
- Web tool access control (already built)
- Stripe checkout for Professional and Enterprise
- MCP Gateway bundled only (standalone comes later)

### Phase 2: Expand (Q3 2026)

- MCP Gateway standalone ("AI Connect") launch
- 14-day trial flow
- Usage analytics dashboard for customers (see your own API calls, active users)
- Referral program: give $50 credit, get $50 credit

### Phase 3: Enterprise (Q4 2026)

- Enterprise Custom tier with custom quotes
- SSO/SAML
- Audit log export
- Volume discounts (20+ seats: 15% off, 50+ seats: 25% off)
- Annual prepay for consulting hours (buy 100 hours at $175/hr instead of $200)

### Phase 4: Ecosystem (2027)

- Usage-based pricing option (for firms that prefer pay-per-call over per-seat)
- Marketplace plugin revenue share (if third-party publishers emerge)
- Partner program: system integrators get wholesale pricing (30% off) for reselling to their clients
- Multi-year contracts with locked pricing

### Price Increase Strategy

- Grandfather existing customers for 12 months on any price increase
- Give 90 days written notice before price changes take effect
- Annual increases capped at 10% unless major new features are added
- Enterprise Custom contracts lock pricing for contract duration

---

## Appendix A: Competitive Pricing Reference

| Tool | Model | Entry | Mid | Enterprise |
|------|-------|-------|-----|------------|
| Procore | ACV-based | $4,500/yr | $20-80K/yr | $100K+/yr |
| ACC/Autodesk Build | Per-seat | $1,625/user/yr | — | Custom |
| BIM Track | Per-seat | Free (50 issues) | $49/user/mo | $79/user/mo |
| Bluebeam | Per-seat | $260/user/yr | $330/user/yr | $440/user/yr |
| Fieldwire | Per-seat | Free | $39/user/mo | $89/user/mo |
| Assemble | Annual | $7,500/yr | — | Custom |
| OpenSpace | ACV-based | ~$10K/project | — | Custom |
| Zapier | Per-task | Free | $20-69/mo | $6K/mo |
| Make | Per-operation | Free | $11-34/mo | Custom |
| n8n | Per-execution | Free (self-host) | EUR 60/mo | EUR 800/mo |
| Vercel | Per-seat + usage | Free | $20/seat/mo | ~$20K/yr |
| Supabase | Base + usage | Free | $25/mo | $599/mo |

## Appendix B: Price Sensitivity Analysis

### Will $49/user/month feel expensive?

**No.** Context:
- These users already pay $135/user/month for ACC/Build
- $49 is a 36% add-on to their existing Autodesk spend
- The ROI on bulk operations alone justifies the cost within days
- Fieldwire charges $39-89/user/month for field management — RAPS is in the same range for admin automation
- BIM Track charges $49-79/user/month for issue tracking alone — RAPS includes this plus 10 other tools

### Will $99/user/month feel expensive?

**Possibly, for smaller firms.** Mitigation:
- Enterprise features (DA Studio, Reality Capture, Portfolio Reporter) are clearly differentiated
- Pipeline engine with cron/serverless is a genuine enterprise capability
- The minimum 5-seat floor ($495/month) is within most IT budget approval ranges without VP sign-off
- Position against the cost of building custom Forge apps ($50-200K+ for equivalent functionality)

### What if a firm only needs one feature?

This is the biggest pricing risk. A firm that only needs Bulk User Manager doesn't want to pay for 10 other tools.

**Mitigation**: Don't offer single-tool pricing. The value proposition is the platform, not individual tools. If a firm only needs bulk user management, the Professional tier at $147/month minimum is still a fraction of the manual labor cost. Frame it as "you get 7 tools for the price of one."

## Appendix C: Discounts & Promotions

| Discount | Amount | Conditions |
|----------|--------|------------|
| Annual billing | 20% off | Pay annually instead of monthly |
| DevCon 2026 launch promo | 30% off Year 1 | Sign up during April 15-30, 2026 |
| Nonprofit / education | 50% off | Verified 501(c)(3) or .edu domain |
| Startup (<50 employees) | 25% off Year 1 | Self-reported, verified via LinkedIn |
| Volume (20+ seats) | 15% off | Applied automatically |
| Volume (50+ seats) | 25% off | Applied automatically |
| Referral credit | $50 per referral | Both referrer and referee get $50 credit |
| Annual consulting prepay | $175/hr (vs $200) | Buy 100+ hours upfront |
