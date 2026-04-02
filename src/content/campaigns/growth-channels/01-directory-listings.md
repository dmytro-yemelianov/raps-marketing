# Software Directory Listings — RAPS

> Passive discovery channel. List once, get traffic indefinitely.
> Goal: Be findable when AEC teams search "Autodesk automation" / "ACC CLI" / "BIM integration tools"

---

## Priority Tier 1 — Submit This Week

### 1. OpenAlternative (openalternative.co)

**Why first**: Open-source focused, fast approval, strong SEO, developer audience.

- **Submission**: GitHub repo link + description
- **Category**: Developer Tools / Construction Tech / Automation
- **Alternative to**: Manual Autodesk Platform Services workflows, ACC web UI for bulk operations

**Listing copy:**

> **Name**: RAPS — Rapid APS Shell
> **Tagline**: CLI toolkit and MCP server for Autodesk Platform Services
> **Description**: Command-line interface with 195+ operations across 51 command families across 15+ Autodesk APIs. Automates bulk user management, model translation, project provisioning, design automation, and ACC administration. Includes pipeline engine for multi-step workflows, MCP server for AI assistant integration, and distributed job orchestration. Built for AEC teams managing hundreds or thousands of ACC projects.
> **License**: Proprietary (free tier available)
> **GitHub**: https://github.com/rapscli/raps
> **Website**: https://rapscli.xyz
> **Categories**: Developer Tools, Construction, Automation, CLI
> **Tech Stack**: Rust, TypeScript, Python

---

### 2. G2 (g2.com)

**Why**: #1 B2B software review site. AEC decision-makers check G2 before buying.

- **Category**: Construction Management Software → subcategory "BIM Tools" or "Construction Collaboration"
- **Also list under**: API Management Tools, DevOps Tools (for the pipeline/automation angle)

**Product Profile:**

> **Product Name**: RAPS
> **Company**: RAPS CLI
> **Website**: https://rapscli.xyz
> **What is RAPS?**
> RAPS is a command-line toolkit for Autodesk Platform Services (formerly Forge) that automates repetitive construction technology workflows. It provides 195+ operations across 51 command families covering 15+ Autodesk APIs — from bulk user provisioning across thousands of ACC projects to automated model translation, webhook management, and design automation.
>
> **Who uses RAPS?**
> - BIM managers at large AEC firms (500+ ACC projects)
> - Construction technology teams automating ACC administration
> - APS developers building integrations and CI/CD pipelines
> - IT administrators managing enterprise Autodesk deployments
>
> **Key differentiator:**
> Zero CLI tools exist in the 259-app ACC marketplace. RAPS is the only command-line interface for Autodesk's construction platform.
>
> **Top features:**
> - Bulk add/remove users across all projects in one command
> - Pipeline engine for multi-step automated workflows (DAG scheduling, retry, checkpoints)
> - MCP server enabling AI assistants (Claude, GPT) to operate Autodesk APIs directly
> - Export permissions, users, and project data to CSV
> - Model translation with progress tracking
> - Webhook lifecycle management
>
> **Deployment**: Cross-platform CLI (Windows, macOS, Linux). npm, pip, or direct binary install.
> **Pricing**: Free tier + paid plans for teams/enterprise.

**Review seed strategy**: Ask Blake (QuikTrip) for a G2 review once onboarding stabilizes. One genuine enterprise review outweighs fifty generic ones.

---

### 3. Capterra (capterra.com)

**Why**: Owned by Gartner. Strong purchase-intent traffic. AEC buyers use it.

- **Category**: Construction Management Software
- **Also**: Project Management, BIM Software

**Use same product profile as G2** (adapt to Capterra's form fields). Key differences:
- Capterra allows "free trial" badge — enable this
- Screenshot slots: Use terminal recordings from `raps-smm/assets/terminal-recordings/`
- Pricing: Mark as "Free Version Available" + "Pricing Model: Per User"

---

### 4. Product Hunt (producthunt.com)

**Dedicated launch plan in file 03.** List the product profile now, launch later (timed with DevCon).

---

## Priority Tier 2 — Submit Within 2 Weeks

### 5. AlternativeTo (alternativeto.net)

- **Alternative to**: Autodesk Construction Cloud web UI, BIM 360 manual admin, custom Forge apps
- **Tags**: CLI, Automation, Construction, Autodesk, BIM, API
- **Platforms**: Windows, macOS, Linux
- Use same description as OpenAlternative

### 6. StackShare (stackshare.io)

- **Category**: DevOps Tools / Build Tools
- **Stack decisions**: "We use RAPS to automate our Autodesk ACC administration instead of building custom Forge apps"
- **Pairs well with**: GitHub Actions, GitLab CI, Jenkins (CI/CD integration angle)

### 7. Awesome Lists (GitHub)

Submit PRs to relevant awesome lists:
- `awesome-construction` — if it exists
- `awesome-cli-apps` — established list, good traffic
- `awesome-rust` — if RAPS source is public
- `awesome-bim` — niche but targeted
- `awesome-mcp-servers` — for the MCP server angle (high activity in 2026)

### 8. Slant (slant.co)

- Answer: "What are the best tools for managing Autodesk ACC projects?"
- Add RAPS as an option with pros/cons

---

## Priority Tier 3 — Submit Within 1 Month

### 9. SaaSHub (saashub.com)
- **Alternative to**: Manual ACC administration
- Free listing, good SEO

### 10. There's An AI For That (theresanaiforthat.com)
- **Angle**: MCP server that gives AI assistants control of Autodesk APIs
- **Category**: AI Tools for Construction / Developer Tools
- Growing rapidly, good for the AI angle

### 11. ToolJet / DevHunt / Uneed.best
- Smaller indie directories, fast approval, cumulative SEO value

### 12. AEC-Specific Directories
- **BIMobject** (bimobject.com) — if they list tools (not just BIM objects)
- **BuiltWorlds** (builtworlds.com) — AEC tech directory
- **ConTech community directories** — submit to any that accept listings

---

## Listing Maintenance

**Monthly check (15 min):**
- Update version numbers (currently v5.7.0)
- Update command count if it changes significantly
- Respond to any reviews or questions
- Check traffic/referral analytics

**After major releases:**
- Update feature list across all directories
- Post "What's New" updates where supported (G2, Capterra allow this)
- Request updated reviews from active users

---

## Tracking

| Directory | Submitted | Approved | Profile URL | Notes |
|-----------|-----------|----------|-------------|-------|
| OpenAlternative | | | | Submit first — fastest approval |
| G2 | | | | Need company verification |
| Capterra | | | | Free listing, paid boost optional |
| Product Hunt | | | | See launch plan (file 03) |
| AlternativeTo | | | | Community-driven |
| StackShare | | | | Developer audience |
| Awesome Lists | | | | PR-based, may take time |
| Slant | | | | Answer-based |
| SaaSHub | | | | Auto-import from GitHub |
| TAAIFT | | | | AI angle |
