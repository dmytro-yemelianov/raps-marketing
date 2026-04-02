# Product Hunt Launch Plan — RAPS

> Concentrated visibility burst. One shot — make it count.
> Target: Top 5 Product of the Day → 500+ upvotes, 2,000+ website visits, 50+ installs.

---

## Timing

### Recommended Launch Date: **April 16, 2026 (Wednesday)**

**Why this date:**
- Day 2 of Autodesk DevCon Amsterdam (April 15-16) — RAPS has 3 live sessions
- Wednesday is historically the best PH launch day (less competition than Tue, more traffic than Thu)
- DevCon attendees provide an engaged audience to upvote and comment
- Creates a "two-front" visibility event: PH + DevCon simultaneously
- "As seen at Autodesk DevCon" adds credibility to the PH listing

**Fallback**: If DevCon timing is too hectic, launch the following Wednesday (April 22). The DevCon buzz is still fresh but you have bandwidth to manage the launch.

**Time**: Schedule for 12:01 AM PT (PH resets at midnight Pacific).

---

## Pre-Launch Checklist (2 weeks before)

### Product Hunt Profile Setup

- [ ] Create Maker profile (Dmytro) — complete bio, photo, links
- [ ] Claim product page and set as "Coming Soon"
- [ ] Collect early followers on the "Coming Soon" page (share link in LinkedIn posts)
- [ ] Prepare Hunter — ideally someone with PH following who's in the AEC/dev-tool space
  - Options: Ask an Autodesk Developer Advocate, a known AEC tech influencer, or a PH-active dev-tool reviewer
  - If no external hunter: self-hunt (works fine for dev tools)

### Assets to Prepare

**Tagline (60 chars max):**
> CLI toolkit that automates Autodesk construction workflows

**Description (260 chars max):**
> 195+ operations across 15+ Autodesk APIs. Bulk-manage users across 1,700 projects, automate model translation, orchestrate workflows with pipelines, and give AI assistants direct access to construction data via MCP. Built in Rust. Zero GUI required.

**Gallery images (5 slots, 1270×760px):**

1. **Hero**: Terminal split-screen showing `raps admin user add --all-projects` processing 1,700 projects with a progress bar. Clean dark terminal aesthetic.
2. **MCP Demo**: AI assistant conversation using RAPS MCP tools to query project data. Shows the "AI meets construction" angle.
3. **Pipeline**: YAML pipeline definition → execution output showing multi-step workflow (upload → translate → validate → notify).
4. **Web Tools**: Screenshot grid of the 12 raps-tools web apps (bulk user manager, issue tracker, webhook console, etc.).
5. **Architecture**: Clean diagram showing RAPS connecting CLI/MCP/Pipeline/Workers to Autodesk API domains.

**Maker comment (first comment, posted at launch):**

```
Hey PH! I'm Dmytro, the developer behind RAPS.

I've spent 2 years building command-line tools for Autodesk's construction platform (ACC/APS).
The problem is simple: AEC firms managing hundreds or thousands of construction projects
have to do everything through a web UI — one click at a time.

Adding a new team member to 1,700 projects? That's 1,700 clicks.
Exporting permissions for an audit? Copy-paste from each project.
Translating 50 Revit models? Upload, click, wait, repeat.

RAPS automates all of this:

  raps admin user add --email new-hire@company.com --role "Project Admin" --all-projects
  ✓ Added to 1,700 projects in 4 minutes

It's built in Rust (fast), works on all platforms (npm/pip/binary), and includes:
- 195+ operations across 15+ Autodesk APIs
- Pipeline engine for multi-step workflows (DAG scheduling, retry, checkpoints)
- MCP server so AI assistants like Claude can operate Autodesk APIs directly
- 12 web tools for common tasks (no terminal required)

Zero CLI tools exist in the 259-app Autodesk marketplace. This is the first.

Currently presenting 3 sessions at Autodesk DevCon in Amsterdam 🇳🇱

Happy to answer any questions about AEC automation, the Autodesk platform, or building
developer tools for industries that haven't had them.
```

**Embed/video**:
- Option A: 60-second terminal recording (VHS/asciinema) showing bulk user add
- Option B: 90-second Loom walkthrough showing problem → solution
- Recommendation: **Option A** — dev tools do better with terminal demos on PH

---

## Launch Day Playbook

### T-0 (12:01 AM PT / 9:01 AM CET)

- [ ] Product goes live on Product Hunt
- [ ] Post Maker comment immediately
- [ ] Share PH link on personal LinkedIn with context (NOT just "we launched on PH")

### Morning (CET — you're in Europe at DevCon)

- [ ] LinkedIn post #1: "We just launched RAPS on Product Hunt — while presenting at Autodesk DevCon in Amsterdam" (leverage the simultaneity)
- [ ] Tweet/X post with PH link
- [ ] DM 10-15 supporters who said they'd upvote (prepare this list in advance)
- [ ] Post in relevant Slack/Discord communities:
  - APS developer community
  - Indie Hackers
  - Dev-tool communities
  - Rust communities (if RAPS has open-source components)

### Midday

- [ ] Respond to EVERY PH comment within 1 hour
- [ ] LinkedIn post #2 (if momentum is good): Share a specific upvote milestone
- [ ] DevCon session mentions: "By the way, we launched on Product Hunt today" (if natural)
- [ ] Ask DevCon attendees who liked the sessions to check out the PH page

### Evening

- [ ] Respond to remaining PH comments
- [ ] Thank supporters
- [ ] Post final LinkedIn update with day's results

---

## Post-Launch (Week After)

- [ ] Write "RAPS Product Hunt Launch Retrospective" for the blog
- [ ] Update all directory listings with "Featured on Product Hunt" badge
- [ ] Follow up with everyone who commented on PH (potential users/advocates)
- [ ] Analyze traffic: PH → website → installs conversion funnel
- [ ] Add PH badge to website hero section and GitHub README

---

## Audience Mobilization

### Who to notify before launch

**Tier 1 — Direct ask to upvote + comment (10-20 people):**
- Blake / QuikTrip team (if relationship allows)
- Autodesk developer relations contacts
- Fellow Expert Elite / ADN members
- DevCon co-presenters or attendees you've connected with
- Close professional network on LinkedIn

**Tier 2 — Soft notification (50-100 people):**
- LinkedIn connections in AEC tech
- Autodesk forum contacts (don't ask them to upvote — just share the link)
- raps-smm existing audience

**Tier 3 — Community posts (reach):**
- Indie Hackers "Launch" section
- Hacker News "Show HN" (separate from PH, can do same day or day after)
- Reddit: r/AutodeskConstructionCloud, r/BIM, r/commandline, r/rust (if appropriate)
- Dev.to or Hashnode post: "Why I Built a CLI for Construction"

### Rules
- **Never ask for upvotes explicitly on PH** (against ToS)
- **Do** share the link with context: "We launched RAPS on Product Hunt — it automates X, Y, Z"
- **Don't** send bulk emails asking people to upvote
- **Do** prep supporters 3-5 days in advance: "We're launching Wednesday, I'd love your support"

---

## Show HN (Hacker News) — Companion Launch

### Timing: April 17, 2026 (day after PH launch)

**Why separate day**: HN audience is different from PH. Stagger for maximum reach.

**Title**: `Show HN: RAPS – CLI toolkit for automating Autodesk construction workflows (Rust)`

**Post body (HN Show guidelines — short, technical, honest):**

```
RAPS is a CLI with 195+ operations for Autodesk's construction platform (ACC/APS).

The construction industry manages everything through web UIs. Adding a user to 1,700
projects means 1,700 clicks. RAPS does it in one command.

Built in Rust. Includes a pipeline engine (DAG scheduling, retry, checkpoints) and an
MCP server so AI assistants can operate Autodesk APIs directly.

Tech stack: Rust (CLI), TypeScript (web tools on Cloudflare Workers), Python (test suite).

There are 259 apps in Autodesk's marketplace. Zero of them are CLI tools. This is the first.

Install: npm install -g @nicedmytro/raps
Docs: https://rapscli.xyz
```

**HN tips**:
- Don't ask friends to upvote (HN detects and penalizes vote rings)
- Respond to every comment, especially critical ones — HN rewards transparency
- Technical depth wins. If asked "why Rust?", have a real answer (not "because it's fast")
- Be honest about limitations (e.g., API rate limits, Autodesk API gaps)

---

## Metrics & Goals

| Metric | Target | Stretch |
|--------|--------|---------|
| PH upvotes | 300+ | 500+ |
| PH ranking | Top 10 of day | Top 5 of day |
| PH comments | 30+ | 50+ |
| Website visits (launch day) | 1,000 | 2,000+ |
| npm installs (launch week) | 50 | 100+ |
| GitHub stars (launch week) | +100 | +200 |
| HN points | 50+ | 100+ |
| New LinkedIn followers | +50 | +100 |
| Direct inquiries/emails | 5 | 10+ |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Low upvotes | Pre-seed supporters (Tier 1 list). Focus on comment quality over vote count. |
| Negative PH comments | Respond quickly, honestly, graciously. Acknowledge limitations. |
| DevCon distracts from launch management | Pre-schedule LinkedIn posts. Have phone ready for PH comment responses. |
| HN skepticism ("why not just use the API?") | Acknowledge the question, explain: "You can. RAPS saves you from writing 10K lines of auth/pagination/error-handling boilerplate." |
| Install problems on launch day | Test install paths (npm, pip, binary) the week before. Have troubleshooting guide ready. |
| Autodesk API goes down on launch day | Unlikely but: Have recorded demos as fallback. "Live demo" isn't required for PH. |

---

## Content Calendar Integration

| Date | Channel | Content |
|------|---------|---------|
| April 1 | LinkedIn | "Coming Soon" PH page link + DevCon preview |
| April 8 | LinkedIn | Technical deep-dive post (pipeline engine or MCP) |
| April 14 | LinkedIn | "Tomorrow: DevCon Amsterdam. Wednesday: Product Hunt." |
| April 15 | DevCon | Sessions 1257, 1258, 1259 |
| April 16 | PH + LinkedIn + Communities | **LAUNCH DAY** |
| April 17 | Hacker News | Show HN post |
| April 18 | LinkedIn | Launch results + thank you |
| April 22 | Blog | Launch retrospective |
| April 29 | LinkedIn | "1 week since launch — here's what happened" |
