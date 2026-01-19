# Session 1258: Zero to Production: Shipping an AI-Ready APS CLI in 30 Min

## Session Details

| Field | Value |
|-------|-------|
| **Session ID** | 1258 |
| **Title** | Zero to Production: Shipping an AI-Ready APS CLI in 30 Min |
| **Speaker(s)** | Dmytro Yemelianov |
| **Session Type** | 30-minute deep dive |
| **Status** | Complete |

## AI Pillars

- [x] **Automate** - Speed repetitive tasks, shrink cycle times, reduce errors
- [x] **Assist** - Improve decisions with insights, copilots, and intelligent guidance
- [ ] Augment

## Themes

- [ ] Sustainability
- [x] **Digital Transformation**
- [x] **System Integration**

## Target Audience

- [ ] Business Decision Makers
- [x] **Developers/Architects** - How it's built, APIs, patterns, lessons learned

## Learning Objectives

1. Install and configure raps CLI for APS operations in under 5 minutes
2. Execute common APS workflows (auth, buckets, translations) from the command line
3. Connect raps CLI to AI assistants via MCP for intelligent automation

![Zero to Production Hero](/devcon/images/1258-zero-to-production-hero.png)

## Abstract

Every APS project starts the same way. You create an app in the developer portal. You copy the client ID and secret. Then you open your favorite HTTP client and start crafting requests. Base64-encode the credentials. POST to the token endpoint. Copy the access token. Remember to add "Bearer" prefix. Paste it into the next request. Repeat when the token expires in an hour.

It's 2026. We can do better.

This session is a speedrun. In 30 minutes, we'll go from zero tooling to a production-ready workflow that handles authentication, file management, model translation, and—here's the twist—AI assistant integration. Everything live, everything real.

**Part 1: Installation & Setup (5 min)**
Four ways to install, because developers are opinionated about package managers. OAuth configuration that actually makes sense. Profile management for when you're juggling dev, staging, and production environments.

**Part 2: Core Operations (15 min)**
The operations you do every day, but faster. Create buckets with one command. Upload files with automatic chunking for large models. Start translations and actually *wait* for them to complete instead of polling manually. Navigate BIM 360/ACC project hierarchies without losing your mind.

**Part 3: AI Integration (10 min)**
The part that makes people's eyes light up. Connect the CLI to Claude, Cursor, or any MCP-compatible AI assistant. Ask questions in English, get operations executed. "What buckets do I have?" becomes a conversation, not a curl command.

## The Problem This Solves

Let me tell you about a Tuesday afternoon that changed how I think about developer tooling.

I was helping a client debug a translation issue. They had a Revit file that kept failing with a cryptic error. To diagnose it, I needed to:

1. Authenticate (find credentials, encode them, POST, copy token)
2. Check if the file was uploaded correctly (GET object details)
3. Look at the translation manifest (decode URN, GET manifest)
4. Parse the nested JSON to find the actual error message
5. Re-upload with different settings
6. Repeat steps 2-4

Each step required switching between Postman tabs, copying values, remembering endpoint URLs. By step 4, I'd forgotten what I was originally trying to debug.

That Tuesday, I started building raps.

The idea was simple: what if every APS operation was a single command? What if the CLI handled authentication automatically, remembered my tokens, and let me focus on the actual problem?

18 months later, we have **150+ commands covering 15 APS APIs**, plus bulk account administration, Python bindings, and AI assistant integration. And it's open source, because the APS community deserves better tooling.

## APS Components Used

- Authentication API (2-legged, 3-legged, device code flow, token inspection)
- OSS API (Buckets, Objects, Signed S3 URLs)
- Model Derivative API (Translations, Manifests, Downloads, Presets)
- Data Management API (Hubs, Projects, Folders, Items)
- Webhooks API
- Design Automation API (Engines, Activities, Work Items)
- ACC Issues API
- ACC RFIs API
- ACC Assets API
- ACC Submittals API
- ACC Checklists API
- ACC Account Admin API (Bulk User Management)

## Autodesk Products

Works with everything APS touches:
- Autodesk Construction Cloud (ACC)
- BIM 360
- Autodesk Fusion
- Autodesk Forma
- AutoCAD Web

If it has an APS API, raps can talk to it.

## Part 1: Installation (Choose Your Adventure)

![Multi-Platform Install](/devcon/images/1258-zero-to-production-installation.png)

I respect that developers have strong opinions about package managers. Here are **six ways** to install—pick the one that doesn't make you twitch.

### Option 1: Quick Install Scripts (Recommended)

The fastest path for most developers:

**Linux/macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/dmytro-yemelianov/raps/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/dmytro-yemelianov/raps/main/install.ps1 | iex
```

### Option 2: npm (Node.js)

For the JavaScript ecosystem folks:

```bash
npm install -g @dmytro-yemelianov/raps-cli

# Or run without installing
npx @dmytro-yemelianov/raps-cli --version
```

### Option 3: pip (Python)

For Python developers:

```bash
pip install raps
```

### Option 4: Homebrew (macOS/Linux)

For the Unix folks who live in the terminal:

```bash
brew install dmytro-yemelianov/tap/raps
```

Homebrew handles updates, man pages, and shell completions automatically.

### Option 5: Scoop (Windows)

Because Windows developers deserve nice things too:

```powershell
scoop bucket add raps https://github.com/dmytro-yemelianov/scoop-bucket
scoop install raps
```

### Option 6: Cargo (The Rust Way)

If you have Rust installed:

```bash
cargo install raps
```

### Verify It Works

```bash
raps --version
# raps 4.3.0
```

If you see a version number, we're in business.

## Configuration: Making It Yours

Here's where raps starts earning its keep. Instead of managing credentials in environment variables, Postman environments, and random .env files, you get profiles.

### Create Your First Profile

```bash
# Interactive setup walks you through it
raps config profile create dev

# Or set values directly
raps config set client_id "your_client_id"
raps config set client_secret "your_client_secret"
```

### Multiple Environments, No Confusion

Real projects have multiple environments. raps handles this gracefully:

```bash
# Create profiles for each environment
raps config profile create dev
raps config profile create staging  
raps config profile create production

# Switch between them
raps config profile use staging

# Check which profile is active
raps config profile current
# → staging
```

No more "wait, which credentials did I just use?" moments.

### Test Your Setup

```bash
# Test 2-legged authentication
raps auth test
# ✓ Authentication successful
#   Token expires in: 59 minutes
#   Scopes: data:read data:write bucket:create ...

# Check detailed status
raps auth status
```

If this works, you're ready for the fun part.

## Part 2: Core Operations (The Daily Workflow)

![CLI Workflow](/devcon/images/1258-zero-to-production-workflow.png)

### Buckets: Your Cloud Storage

OSS buckets are the foundation of everything. Let's create one:

```bash
# Interactive mode asks the right questions
raps bucket create
# ? Bucket key: hospital-project-2026
# ? Retention policy: persistent
# ? Region: us
# ✓ Bucket created successfully!

# Or one-liner for scripts
raps bucket create --key hospital-project-2026 --policy persistent --region us
```

**Why start with the derivative service?** Honestly, because it has the best immediate payoff. You run one command, wait a few minutes, and you can see your model in a browser. It's satisfying. And once people see that work, they're hooked—they want to automate the rest of their workflow.

```bash
# List your buckets
raps bucket list
# ┌─────────────────────────┬────────────┬────────┐
# │ Bucket Key              │ Policy     │ Region │
# ├─────────────────────────┼────────────┼────────┤
# │ hospital-project-2026   │ persistent │ US     │
# │ temp-uploads            │ transient  │ US     │
# │ archive-2025            │ persistent │ US     │
# └─────────────────────────┴────────────┴────────┘

# Get detailed info
raps bucket info hospital-project-2026
```

### Uploads: Handling Real Files

This is where I wasted the most time before building raps. Uploading large files to OSS is annoying—you need to chunk files over 100MB, manage upload sessions, handle resumable uploads when your VPN decides to reconnect mid-transfer.

```bash
# Upload a file (auto-chunks large files)
raps object upload hospital-project-2026 model.rvt
# Uploading model.rvt to hospital-project-2026/model.rvt
# [████████████████████████████████] 100% | 245 MB
# ✓ Upload complete!
#   Object ID: urn:adsk.objects:os.object:hospital-project-2026/model.rvt
#   Size: 245.32 MB
#   SHA1: a3f2b1c4d5e6...
#
#   URN (for translation): dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z...
```

See that URN at the end? That's what you need for translation. No manual Base64 encoding required.

**For the serious workflows:** batch upload multiple files in parallel:

```bash
# Upload all DWG files, 4 at a time
raps object upload-batch hospital-project-2026 *.dwg --parallel 4
# Uploading 12 files to bucket 'hospital-project-2026' with 4 parallel uploads
# ✓ floor-plan-L1.dwg (2.3 MB)
# ✓ floor-plan-L2.dwg (2.1 MB)
# ✓ floor-plan-L3.dwg (2.4 MB)
# ...
# Total: 12 uploaded, 0 failed
# Size: 28.4 MB
```

### Translation: The Moment of Truth

Model Derivative translation is where APS earns its keep. You upload a Revit file, APS extracts geometry, properties, metadata, and produces viewable formats.

```bash
# Start a translation
raps translate start dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z... --format svf2
# ✓ Translation job started
#   URN: dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z...
#   Output: svf2
#   Status: pending

# Check status (and actually wait for it)
raps translate status dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z... --wait
# Translation progress: 15%... 42%... 78%... 100%
# ✓ Translation complete!
#   Status: success
#   Derivatives: svf2, thumbnail
```

That `--wait` flag is deceptively powerful. Instead of writing yet another while loop with time.sleep(5), the CLI handles the polling. Go get coffee. Come back. It'll be done.

```bash
# View the manifest (what derivatives are available)
raps translate manifest dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z...

# Download derivatives
raps translate download dXJuOmFkc2sub2JqZWN0czpvcy5vYmplY3Q6aG9z... \
  --format obj --output ./exports/
```

### Data Management: Navigating the Hierarchy

BIM 360 and ACC organize data in a hierarchy: Hubs → Projects → Folders → Items → Versions. If you've ever tried to navigate this via raw API calls, you know it's... not fun. Each level requires a different endpoint, different ID format, and the documentation is scattered across three different sites.

```bash
# List your hubs (requires 3-legged auth)
raps auth login  # Opens browser for OAuth flow
raps hub list
# ┌───────────────────────────────────────────────┬─────────┐
# │ Hub Name                                       │ Type    │
# ├───────────────────────────────────────────────┼─────────┤
# │ ACME Construction                              │ ACC     │
# │ Legacy BIM 360 Account                         │ BIM 360 │
# └───────────────────────────────────────────────┴─────────┘

# Drill down into projects
raps project list b.abc123-hub-id

# Navigate folders
raps folder list b.xyz789-project-id urn:folder:root

# View item versions
raps item versions b.xyz789-project-id urn:item:12345
```

## Part 3: AI Integration (The Part Where Things Get Weird)

![Speedrun Timer](/devcon/images/1258-zero-to-production-speedrun.png)

I'll be honest—when I first added MCP support, I thought it was a gimmick. "Oh cool, AI can call my CLI. Whatever."

Then I actually used it. Now I can't go back.

### Start the MCP Server

```bash
raps serve
```

That's it. The CLI is now an MCP server, exposing **35 tools** for AI assistants to use.

### Connect Claude Desktop

Create or edit your Claude configuration:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`  
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"],
      "env": {
        "APS_CLIENT_ID": "your_client_id",
        "APS_CLIENT_SECRET": "your_client_secret"
      }
    }
  }
}
```

Restart Claude Desktop, and you'll see "raps" in the available tools.

### Connect Cursor IDE

For the developers who live in Cursor, add `.cursor/mcp.json` to your project:

```json
{
  "mcpServers": {
    "raps": {
      "command": "raps",
      "args": ["serve"]
    }
  }
}
```

### 35 MCP Tools Available

The MCP server exposes comprehensive APS operations:

**Authentication & Buckets:**
- `auth_test`, `auth_status`
- `bucket_list`, `bucket_create`, `bucket_get`, `bucket_delete`

**Objects & Translation:**
- `object_list`, `object_delete`, `object_signed_url`, `object_urn`
- `translate_start`, `translate_status`

**Data Management:**
- `hub_list`, `project_list`, `folder_list`, `folder_create`
- `item_info`, `item_versions`

**ACC Issues & RFIs:**
- `issue_list`, `issue_get`, `issue_create`, `issue_update`
- `rfi_list`, `rfi_get`

**ACC Extended:**
- `acc_assets_list`, `acc_submittals_list`, `acc_checklists_list`

**Account Admin (Bulk Operations):**
- `admin_project_list`, `admin_user_add`, `admin_user_remove`
- `admin_user_update_role`, `admin_operation_list`, `admin_operation_status`

### What Can You Do With This?

Once connected, natural language becomes API operations:

- "List all my OSS buckets" → AI calls `bucket_list`
- "Create a bucket named 'new-project' with transient policy" → AI calls `bucket_create`
- "What's the status of my translation job?" → AI calls `translate_status`
- "Show me all projects in my BIM 360 hub" → AI calls `hub_list`, then `project_list`
- "Add user@company.com to all active projects as project admin" → AI calls `admin_user_add`
- "List all open issues in project XYZ" → AI calls `issue_list`

The AI doesn't hallucinate endpoints. It uses the tools we've defined, with the parameters we've specified, against your actual APS environment.

## The Bigger Picture

Look, this 30-minute walkthrough isn't about the CLI. Not really.

APS is powerful. The APIs are comprehensive. But there's a gap—a big one—between reading the documentation and actually shipping production code. That gap is filled with friction: OAuth dance, Base64 encoding URNs, polling loops with magic sleep timers, error messages that could mean five different things.

Good tooling shrinks that gap. It lets you focus on what you're actually building instead of fighting the mechanics.

raps is one answer. It's the answer I wish existed when I spent three hours debugging why my translation kept returning "complete" with zero derivatives. Maybe it's the answer you need too.

## Key Takeaways

1. **CLI beats clicking** for anything you do more than twice
2. **raps has 150+ commands** across 15 APIs—probably covers what you need
3. **Pick your poison for install**: npm, pip, brew, scoop, cargo, or curl-bash
4. **Profiles save your sanity** when juggling staging vs prod (you will forget which one you're on otherwise)
5. **MCP is real**—35 tools, works today, not a demo
6. **Python bindings** exist if you prefer scripting over shell commands
7. **Open source** means you can fix bugs without waiting on a vendor ticket

## Resources

- **GitHub**: https://github.com/dmytro-yemelianov/raps
- **Documentation**: https://rapscli.xyz/docs
- **Installation Guide**: https://rapscli.xyz/docs/installation
- **MCP Server Guide**: https://rapscli.xyz/docs/mcp-server
- **Python Bindings**: https://rapscli.xyz/docs/python-bindings
- **Command Reference**: https://rapscli.xyz/docs/commands
