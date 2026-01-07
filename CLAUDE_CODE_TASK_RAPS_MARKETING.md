# Claude Code Task: RAPS Marketing Content Generation

## Repository Context
- **Working repo:** https://github.com/dmytro-yemelianov/raps-marketing
- **Target repo:** https://github.com/dmytro-yemelianov/raps-website (after review)

## Mission
Generate comprehensive APS (Autodesk Platform Services) developer resources that:
1. Fill documentation gaps Autodesk doesn't prioritize
2. Capture SEO traffic for APS-related searches
3. Naturally introduce raps CLI as the practical solution
4. Position rapscli.xyz as the go-to APS developer companion

---

## Content Strategy: "Value First, Tool Second"

### Raps Mention Guidelines
When referencing raps in content, use these patterns:

**Pattern 1: Manual vs Easy**
```
To get a token manually, you need to base64-encode credentials, POST to /authentication/v2/token...

Or with raps: `raps auth login`
```

**Pattern 2: Inline Tip**
```
Make sure your URN is base64-encoded (raps handles this automatically with `raps urn encode`).
```

**Pattern 3: Callout Box**
```
💡 **Tip:** This entire workflow can be scripted with `raps translate watch <urn>`
```

**Pattern 4: Comparison Tables**
Show manual steps vs raps one-liners

**Pattern 5: Footer Reference**
```
*For a streamlined workflow, check out [raps CLI](https://rapscli.xyz).*
```

**Placement Rules:**
- Top of article: NO raps mention (build trust first)
- Middle (pain point): Show manual complexity, then raps shortcut
- Bottom: "Tools that help" section

---

## Deliverables

### 1. APS Cheat Sheet (`/cheatsheets/aps-cheatsheet.md`)
Single-page reference covering:
- Authentication (2-legged vs 3-legged flow diagrams)
- OAuth scopes quick reference
- Common endpoints by API
- URN encoding/decoding rules
- Status codes and meanings
- Rate limits per API
- Token lifetimes

**Format:** Markdown optimized for printing/PDF export
**Raps integration:** Show `raps` equivalents in a sidebar column

---

### 2. APS Mindmap (`/mindmaps/aps-ecosystem.md`)
Mermaid diagram showing:
```
APS Ecosystem
├── Authentication
│   ├── 2-legged (client credentials)
│   └── 3-legged (authorization code)
├── Data Management API
│   ├── Hubs
│   ├── Projects
│   ├── Folders
│   ├── Items & Versions
│   └── OSS (Object Storage)
├── Model Derivative API
│   ├── Translation jobs
│   ├── Manifest & metadata
│   ├── Properties extraction
│   └── Thumbnails
├── Viewer SDK
│   ├── Initialization
│   ├── Extensions
│   └── Events
├── Automation API (Design Automation)
│   ├── Engines (AutoCAD, Revit, Inventor, 3ds Max, Fusion)
│   ├── AppBundles
│   ├── Activities
│   └── WorkItems
├── Webhooks
│   ├── Event types
│   └── Payload structure
└── ACC/BIM360 APIs
    ├── Account Admin
    ├── Project Admin
    ├── Issues, RFIs, Submittals
    ├── Sheets, Cost, Assets
    └── Model Coordination
```

**Format:** Mermaid + exportable SVG/PNG
**Also create:** Interactive HTML version if feasible

---

### 3. Decision Tree (`/guides/which-api-do-i-need.md`)
Flowchart answering "Which APS API should I use?"

```
START: What do you want to do?
│
├─► View 3D models in browser? → Viewer SDK + Model Derivative
├─► Store files in cloud? → Data Management (OSS)
├─► Access BIM360/ACC projects? → Data Management (Hubs/Projects)
├─► Convert file formats? → Model Derivative
├─► Extract model properties? → Model Derivative
├─► Automate CAD operations? → Automation API (Design Automation)
├─► Get notified of changes? → Webhooks
└─► Manage ACC/BIM360 settings? → ACC Admin APIs
```

**Format:** Mermaid flowchart + written guide
**Raps integration:** Each endpoint shows `raps` command equivalent

---

### 4. Error Code Reference (`/troubleshooting/error-codes.md`)
Comprehensive error lookup:

| Code | API Context | Likely Cause | Solution | Raps helps? |
|------|-------------|--------------|----------|-------------|
| 400 | All | Malformed request | Check JSON syntax | `raps` validates input |
| 401 | All | Invalid/expired token | Refresh token | `raps auth refresh` |
| 403 | Data Mgmt | Wrong scopes or no access | Check app permissions | `raps auth status` shows scopes |
| 404 | Model Deriv | URN not found or not encoded | Base64 encode URN | `raps urn encode` |
| 409 | OSS | Bucket exists | Use different name or check existing | `raps bucket list` |
| 429 | All | Rate limited | Implement backoff | `raps` has built-in retry |
| 500 | All | Server error | Retry with backoff | - |

**Include for each error:**
- Actual error message examples
- Step-by-step diagnosis
- Code snippets for fix
- `raps` command that avoids this issue

---

### 5. Forge → APS Migration Guide (`/guides/forge-to-aps-migration.md`)
For developers with legacy Forge code:

| Old (Forge) | New (APS) | Notes |
|-------------|-----------|-------|
| forge.autodesk.com | aps.autodesk.com | Domain change |
| learnforge.autodesk.io | tutorials.autodesk.io | Tutorials moved |
| Forge Viewer | APS Viewer | Same SDK, new name |
| /authentication/v1/ | /authentication/v2/ | Scope format changed |

**Include:**
- Endpoint mapping table
- SDK package name changes
- Breaking changes list
- Migration checklist
- "raps works with both" note

---

### 6. Workflow Recipes (`/recipes/`)
Copy-paste workflow guides:

#### `/recipes/upload-translate-view.md`
```bash
# Manual: 6 API calls, ~50 lines of code
# With raps:
raps auth login
raps bucket create my-bucket
raps upload model.rvt --bucket my-bucket
raps translate <urn> --wait
raps view <urn>
```

#### `/recipes/extract-properties.md`
#### `/recipes/batch-translate.md`
#### `/recipes/webhook-setup.md`
#### `/recipes/design-automation-basic.md`

**Format for each:**
1. Goal (what you'll achieve)
2. Prerequisites
3. Manual approach (show the complexity)
4. Raps approach (show the simplicity)
5. Common issues & fixes

---

### 7. OAuth Scopes Matrix (`/references/oauth-scopes.md`)

| Scope | Used for | Required by |
|-------|----------|-------------|
| `data:read` | Read files, projects | Data Mgmt GET endpoints |
| `data:write` | Upload, modify files | Data Mgmt POST/PUT/DELETE |
| `data:create` | Create new resources | Bucket creation, uploads |
| `bucket:read` | List buckets | OSS bucket listing |
| `bucket:create` | Create buckets | OSS bucket creation |
| `code:all` | Design Automation | All DA endpoints |
| `viewables:read` | View translated models | Viewer initialization |
| `account:read` | BIM360/ACC account info | Account Admin API |
| `account:write` | Modify account settings | Account Admin API |

**Raps integration:** Show how `raps auth login --scopes` works

---

### 8. Rate Limits Reference (`/references/rate-limits.md`)

| API | Limit | Window | Backoff Strategy |
|-----|-------|--------|------------------|
| Authentication | 500/min | 1 minute | Exponential |
| Data Management | 100/min | 1 minute | Exponential |
| Model Derivative | 20/min (translate) | 1 minute | Queue locally |
| OSS | 500/min | 1 minute | Exponential |
| Design Automation | 50 concurrent | - | Queue workitems |

**Include:** `raps` built-in rate limiting explanation

---

### 9. Troubleshooting Flowcharts (`/troubleshooting/`)

#### `/troubleshooting/translation-failed.md`
```
Translation failed?
├─► Check manifest: GET /modelderivative/v2/designdata/{urn}/manifest
│   ├─► Status: failed → Check messages array for details
│   ├─► Status: timeout → File too large, retry or split
│   └─► Status: success but no viewable → Wrong output format specified
├─► Common causes:
│   ├─► Corrupted source file
│   ├─► Unsupported file version
│   ├─► Missing linked files (assemblies)
│   └─► Region mismatch (US vs EMEA)
└─► With raps: `raps translate status <urn> --verbose`
```

#### `/troubleshooting/auth-issues.md`
#### `/troubleshooting/viewer-not-loading.md`
#### `/troubleshooting/webhook-not-firing.md`

---

### 10. Interactive Tools (HTML/JS) (`/tools/`)

#### `/tools/urn-encoder.html`
- Input: raw URN or file path
- Output: base64 URL-safe encoded URN
- Note: "Or use `raps urn encode <input>`"

#### `/tools/token-decoder.html`
- Input: JWT token
- Output: decoded payload (scopes, expiry, etc.)
- Note: "Or use `raps auth status`"

#### `/tools/scope-builder.html`
- Checkboxes for each scope
- Output: space-separated scope string
- Note: "Or use `raps auth login --scopes data:read,data:write`"

---

### 11. Comparison Tables (`/comparisons/`)

#### `/comparisons/2legged-vs-3legged.md`
| Aspect | 2-Legged | 3-Legged |
|--------|----------|----------|
| User context | App only | User's identity |
| Use case | Server-to-server | User-facing apps |
| Token endpoint | /authentication/v2/token | /authentication/v2/authorize |
| Scopes | Limited | Full |
| BIM360/ACC | Limited access | Full project access |
| raps command | `raps auth login` | `raps auth login --3legged` |

#### `/comparisons/oss-vs-bim360-storage.md`
#### `/comparisons/svf-vs-svf2.md`

---

### 12. Quick Start Templates (`/templates/`)

#### `/templates/node-starter/`
#### `/templates/python-starter/`
#### `/templates/dotnet-starter/`

Minimal working examples with:
- Environment setup
- Authentication
- One useful operation
- "Alternatively, use `raps` for quick prototyping"

---

## File Structure

```
raps-marketing/
├── README.md
├── cheatsheets/
│   └── aps-cheatsheet.md
├── mindmaps/
│   ├── aps-ecosystem.md (Mermaid source)
│   └── aps-ecosystem.svg (exported)
├── guides/
│   ├── which-api-do-i-need.md
│   └── forge-to-aps-migration.md
├── recipes/
│   ├── upload-translate-view.md
│   ├── extract-properties.md
│   ├── batch-translate.md
│   ├── webhook-setup.md
│   └── design-automation-basic.md
├── references/
│   ├── oauth-scopes.md
│   └── rate-limits.md
├── troubleshooting/
│   ├── error-codes.md
│   ├── translation-failed.md
│   ├── auth-issues.md
│   ├── viewer-not-loading.md
│   └── webhook-not-firing.md
├── comparisons/
│   ├── 2legged-vs-3legged.md
│   ├── oss-vs-bim360-storage.md
│   └── svf-vs-svf2.md
├── tools/
│   ├── urn-encoder.html
│   ├── token-decoder.html
│   └── scope-builder.html
└── templates/
    ├── node-starter/
    ├── python-starter/
    └── dotnet-starter/
```

---

## Quality Checklist

For each piece of content, verify:

- [ ] Technically accurate (test against actual APS APIs)
- [ ] Value-first structure (useful even without raps)
- [ ] Raps mentions feel natural, not forced
- [ ] SEO-friendly title and headings
- [ ] Includes practical examples
- [ ] Links to official docs where appropriate
- [ ] Disclaimer: "Unofficial community resource"
- [ ] Mobile-friendly formatting
- [ ] No Autodesk trademarks misuse

---

## SEO Target Keywords

Primary:
- "APS cheat sheet"
- "Autodesk Platform Services tutorial"
- "Forge API guide"
- "APS error 403"
- "APS URN encoder"
- "BIM360 API tutorial"

Long-tail:
- "Autodesk Forge to APS migration"
- "Design Automation API example"
- "APS Viewer not loading fix"
- "2-legged vs 3-legged authentication APS"

---

## Execution Order

1. **High impact, low effort first:**
   - Error codes reference
   - OAuth scopes matrix
   - Forge → APS migration table

2. **Visual assets:**
   - Mindmap
   - Decision tree flowchart

3. **Workflow content:**
   - Recipes (start with upload-translate-view)
   - Troubleshooting flowcharts

4. **Interactive tools:**
   - URN encoder
   - Token decoder

5. **Templates last** (most maintenance burden)

---

## Notes for Claude Code

- Clone raps-marketing repo first
- Check existing raps CLI documentation for accurate command syntax
- Use Mermaid for all diagrams (renders on GitHub)
- Keep files self-contained (no complex build process)
- Commit logical chunks, not everything at once
- Add frontmatter for future static site generation:

```yaml
---
title: "APS Error Codes Reference"
description: "Complete guide to APS/Forge API error codes with solutions"
keywords: ["APS", "error codes", "troubleshooting", "403", "401"]
raps_commands: ["raps auth status", "raps urn encode"]
---
```

---

---

## Site Structure Mapping (raps-website)

When content moves from `raps-marketing` → `raps-website`, place in these sections:

```
rapscli.xyz/
├── /docs/                      ← Main documentation
│   ├── /docs/getting-started/  ← Quick start templates
│   ├── /docs/commands/         ← Existing raps CLI reference
│   └── /docs/recipes/          ← Workflow recipes
│
├── /learn/                     ← Educational content (NEW SECTION)
│   ├── /learn/aps-cheatsheet/  ← Cheat sheet
│   ├── /learn/aps-overview/    ← Mindmap, decision tree
│   ├── /learn/guides/          ← Migration guide, comparisons
│   └── /learn/troubleshooting/ ← Error codes, flowcharts
│
├── /tools/                     ← Interactive utilities (NEW SECTION)
│   ├── /tools/urn-encoder/
│   ├── /tools/token-decoder/
│   └── /tools/scope-builder/
│
└── /references/                ← Quick lookups (NEW SECTION)
    ├── /references/scopes/
    ├── /references/rate-limits/
    └── /references/error-codes/
```

**Navigation structure:**
```
Docs | Learn | Tools | References | GitHub
```

**Cross-linking rules:**
- Every `/learn/` page links to relevant `/docs/commands/`
- Every `/tools/` page shows equivalent `raps` command
- Every `/references/` page is reachable from `/learn/troubleshooting/`

---

## Version Tracking

### Raps CLI Versions

Each document must specify compatible raps version:

```yaml
---
raps_version: ">=0.5.0"
raps_commands_tested: "0.5.2"
last_verified: "2025-01-07"
---
```

**In content, show version notes:**
```markdown
> ⚠️ `raps translate --wait` requires raps v0.5.0+
```

**Maintain compatibility matrix:**

| Feature | raps version | Notes |
|---------|--------------|-------|
| `raps auth login` | 0.1.0+ | - |
| `raps translate --wait` | 0.5.0+ | Polling added |
| `raps acc projects` | 0.6.0+ | ACC support |

Create `/references/raps-changelog.md` tracking breaking changes.

---

### APS API Versions

APS APIs have versions that drift. Track in frontmatter:

```yaml
---
aps_apis:
  authentication: "v2"
  data_management: "v2" 
  model_derivative: "v2"
  design_automation: "v3"
  acc_admin: "v1"
aps_spec_date: "2025-01"
---
```

**In content, be explicit:**
```markdown
## Authentication (API v2)

POST `https://developer.api.autodesk.com/authentication/v2/token`
```

**Track APS changes:**
- Subscribe to [APS changelog](https://aps.autodesk.com/blog)
- Create `/references/aps-api-versions.md`:

| API | Current Version | Deprecated | Sunset Date |
|-----|-----------------|------------|-------------|
| Authentication | v2 | v1 | 2024-01-01 |
| Model Derivative | v2 | - | - |
| Design Automation | v3 | v2 | TBD |
| Data Management | v2 | v1 | 2023-06-01 |

---

### Version Drift Handling

**Quarterly review process:**
1. Check APS blog for API updates
2. Verify all documented endpoints still work
3. Update `last_verified` dates
4. Add deprecation warnings if needed

**Automation idea (future):**
- CI job that hits documented endpoints
- Fails build if responses change
- Alerts maintainer to update docs

**Content warnings:**
```markdown
> 📅 **Last verified:** January 2025 against APS API v2 and raps v0.5.2
> 
> APIs evolve. If something doesn't work, [open an issue](https://github.com/dmytro-yemelianov/raps-marketing/issues).
```

---

## Success Metrics

After deployment to raps-website:
- Organic traffic to APS-related pages
- GitHub stars on raps-marketing
- Mentions/backlinks from APS community
- raps CLI downloads from documentation referrals
