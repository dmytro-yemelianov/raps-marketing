# Claude Code Task: RAPS Marketing Content Generation — Part 2

## Context
This is a continuation of the first task file. These deliverables are based on deep research into Autodesk forums, Stack Overflow, and GitHub issues — real pain points developers face daily.

**Do not duplicate content from Part 1.** This file covers NEW gaps discovered through community research.

---

## High-Priority Tools (Developers Desperately Need These)

### 1. Coordinate Transformation Calculator (`/tools/coord-transform.html`)

**Why:** Official Autodesk blog admits developers face *"frustration with translation/rotation matrices, matrix inverses, quaternions"* — this is one of the most complex topics in forums.

**Features:**
- Fragment proxy → World position converter
- Matrix multiplication visualizer
- Quaternion ↔ Euler angles converter
- Global offset calculator for 2D sheets → 3D views
- Unit conversion (model units to display units)

```javascript
// Example calculation this tool should handle:
// Input: Fragment proxy local position + model matrix
// Output: World position coordinates
```

**Raps integration:** "For batch transformations, use `raps viewer transform --input coords.json`"

---

### 2. Chunk Size Calculator (`/tools/chunk-calculator.html`)

**Why:** Developers get `416 Range Not Satisfiable` errors constantly due to incorrect chunk sizing. The 2MB minimum, 5MB recommended, 100MB maximum constraints aren't intuitive.

**Features:**
- Input: file size
- Output: 
  - Recommended chunk size
  - Number of chunks
  - Estimated upload time
  - Session ID format helper
- Handles edge cases (files < 2MB, files > 5GB)

**Include formulas:**
```
Optimal chunks = ceil(fileSize / 5MB)
If fileSize < 100MB → single upload recommended
If fileSize > 5GB → requires multipart with specific session format
```

**Raps integration:** "`raps upload` handles chunking automatically — no manual calculation needed"

---

### 3. Token Cost Estimator (`/tools/token-estimator.html`)

**Why:** No self-service calculator exists. Developers must contact sales or guess. Prices changed from $1 to $3/token in 2022, catching many off guard.

**Build a calculator for:**

| Operation | Token Cost |
|-----------|-----------|
| Model Derivative (Revit/Navisworks) | 1.5 tokens |
| Model Derivative (other formats) | 0.5 tokens |
| Design Automation (per hour) | 6 tokens |
| Viewer sessions | Free |
| Data Management | Free |
| OSS Storage | Free (with limits) |

**Features:**
- Input: expected monthly translations by file type
- Input: expected DA processing hours
- Output: monthly token cost estimate
- Compare: Free tier limits vs Paid tier needs

**Raps integration:** "`raps usage estimate --translations 100 --da-hours 10`"

---

### 4. Region Mismatch Debugger (`/tools/region-checker.html`)

**Why:** Files uploaded to EMEA bucket cannot generate derivatives in US region — causes mysterious failures. Developers waste hours on this.

**Features:**
- Input: URN or bucket key
- Detect: which region (US/EMEA) the file is in
- Check: which region your app is configured for
- Output: "Mismatch detected! File in EMEA, app configured for US"
- Solution: step-by-step fix or re-upload guidance

**Include decision tree:**
```
Is your ACC account EMEA-based?
├── Yes → Use developer.api.autodesk.com with x-ads-region: EMEA
└── No → Use developer.api.autodesk.com (default US)

Did you upload via OSS?
├── Yes → Check bucket region in creation call
└── No (BIM360/ACC) → Region follows account location
```

---

### 5. SDK Compatibility Matrix (`/references/sdk-compatibility.md`)

**Why:** Revit 2025 embeds `Autodesk.Forge.dll v1.9.3` internally, causing conflicts. Developers discover this through crashes, not documentation.

| Host App | Embedded SDK | Compatible External SDK | Workaround |
|----------|--------------|------------------------|------------|
| Revit 2025 | Forge 1.9.3 | aps-sdk-net only | Use binding redirects or custom impl |
| Revit 2026 | Forge 1.9.3 | aps-sdk-net only | Same |
| Revit 2024 | Forge 1.9.1 | Forge ≤1.9.1 | Match versions |
| AutoCAD 2025 | None | Any | Full compatibility |
| Inventor 2025 | None | Any | Full compatibility |

**Include:**
- NuGet package version history
- Binding redirect examples
- "Roll your own HTTP client" pattern for conflict-free integration

---

### 6. IFC Translation Guide (`/guides/ifc-translation-deep-dive.md`)

**Why:** Three different IFC conversion methods exist (legacy, modern, v3) with different default units and behaviors. Forum questions about this are endless.

| Method | Trigger | Default Units | IFC4x3 Support | Notes |
|--------|---------|---------------|----------------|-------|
| Legacy | `generateMasterViews: false` | Native file | No | Deprecated |
| Modern | `generateMasterViews: true` | Feet | No | Current default |
| V3 | `"conversionMethod": "v3"` | Feet | Yes (basic) | March 2023+ |

**Cover:**
- When to use each method
- Unit handling gotchas
- Large coordinate issues ("exploded geometry")
- Property set extraction differences
- MVD support matrix

**Raps integration:** "`raps translate model.ifc --method v3 --units meters`"

---

### 7. BIM360/ACC Provisioning Checklist (`/guides/acc-provisioning-checklist.md`)

**Why:** The #1 cause of 403 errors. Developers don't realize they must manually enable custom integrations from ACC admin console.

**Step-by-step checklist:**

```markdown
## Before You Code

- [ ] Created APS app at aps.autodesk.com
- [ ] Noted Client ID and Client Secret
- [ ] Set correct Callback URL

## ACC Admin Console (REQUIRED)

- [ ] Logged into ACC as Account Admin
- [ ] Navigated to Account Admin → Settings → Custom Integrations
- [ ] Clicked "Add Custom Integration"
- [ ] Entered your Client ID
- [ ] Selected required access (BIM 360 Account Admin + Docs)
- [ ] Completed wizard

## Per-Project Setup

- [ ] Added app to specific project (if using 2-legged)
- [ ] Verified user has project access (if using 3-legged)
- [ ] Waited 5-10 minutes for propagation

## Common Errors After Setup

- "client_id does not have access" → Integration not added
- "User not authorized" → User lacks project permissions
- "Project not found" → 3-legged token from wrong user
```

**Raps integration:** "`raps acc check-provisioning` validates your setup"

---

### 8. Translation Failure Diagnosis Tool (`/tools/translation-debugger.html`)

**Why:** Error messages like `TranslationWorker-InternalFailure` provide zero actionable info. Developers are blind.

**Interactive debugger:**
1. Input: URN
2. Fetch: manifest via API
3. Analyze: status, messages, derivatives
4. Output: 
   - Human-readable diagnosis
   - Specific failure reason
   - Recommended fix

**Common failure patterns to detect:**

| Manifest Status | Messages Content | Likely Cause | Fix |
|-----------------|------------------|--------------|-----|
| `failed` | "Tr worker fail to download" | File deleted or moved | Re-upload |
| `failed` | "TranslationWorker-InternalFailure" | Corrupted file | Check source |
| `success` | No viewable in derivatives | Wrong output format | Specify SVF2 |
| `inprogress` stuck | - | Large file timeout | Wait or split file |
| `failed` | Region mismatch hint | US/EMEA mismatch | Delete manifest, re-translate in correct region |

**Raps integration:** "`raps translate status <urn> --diagnose`"

---

### 9. Design Automation Debugging Guide (`/guides/da-debugging-guide.md`)

**Why:** Local testing requires complex setup. The official debug tool doesn't support multiple addins or multiple input files locally.

**Cover:**

1. **Local setup checklist:**
   - Install DesignAutomationHandler
   - Configure Revit Addins folder
   - Use `DBApplication` type (RevitAPIUI detection issue)
   - Single input file limitation locally

2. **AppBundle configuration validator:**
   ```
   ZIP structure:
   └── MyApp.bundle/           ← Must have .bundle suffix
       ├── PackageContents.xml ← ModuleName must match
       └── Contents/
           └── MyPlugin.dll
   ```

3. **Common errors:**
   - "ActivityId not found" → Check nickname format: `{owner}.{activity}+{alias}`
   - "Engine mismatch" → SeriesMin/SeriesMax must match engine version
   - "FailedDownload" → Signed URL expired or inaccessible

4. **Cloud vs local behavior differences:**
   - Cloud supports multiple inputs, local doesn't
   - Cloud has 1-hour timeout, local unlimited
   - Cloud logs available via Report URL

**Raps integration:** "`raps da debug --bundle ./MyApp.bundle --activity MyActivity`"

---

### 10. Viewer Measurement Workarounds (`/guides/viewer-measurement-hacks.md`)

**Why:** The measurement tool can't measure diameter, radius, or distance between holes — a 4+ year unresolved feature request with 97 votes. Developers need workarounds.

**Document workarounds:**

1. **Custom measurement extension:**
   ```javascript
   // Diameter measurement using cylinder detection
   viewer.addEventListener(
     Autodesk.Viewing.SELECTION_CHANGED_EVENT,
     detectCylindricalFaces
   );
   ```

2. **Property extraction approach:**
   - Extract geometry via `model.getGeometry()`
   - Calculate measurements programmatically
   - Display via custom overlay

3. **External tools integration:**
   - Export to STEP/SAT
   - Measure in CAD application
   - Return to Viewer for visualization

4. **Precision issues:**
   - Unit calibration: `ext.sharedMeasureConfig.units = "in"`
   - Scale calibration: `ext.calibrateByScale('in', 0.0254)`
   - STL files have no units — always calibrate

**Note:** "These are workarounds for limitations Autodesk hasn't addressed in 4+ years"

---

### 11. Webhook Testing Setup Guide (`/guides/webhook-testing-local.md`)

**Why:** No official test infrastructure. Developers must use ngrok or similar tunneling tools — official samples explicitly require this.

**Complete setup:**

1. **Local tunnel setup:**
   ```bash
   # Install ngrok
   brew install ngrok
   
   # Start tunnel
   ngrok http 3000
   
   # Copy HTTPS URL → set as APS_WEBHOOK_URL
   ```

2. **Webhook registration:**
   ```javascript
   // Required scopes: data:read, data:write
   POST /webhooks/v1/systems/data/events/dm.version.added/hooks
   {
     "callbackUrl": "https://abc123.ngrok.io/webhook",
     "scope": { "folder": "urn:..." }
   }
   ```

3. **Testing workflow:**
   - Register webhook with ngrok URL
   - Upload file to trigger event
   - Inspect ngrok dashboard for payload
   - Validate signature in your handler

4. **Common issues:**
   - Webhook not firing → Check scope matches folder URN
   - 403 on registration → Need 3-legged token for BIM360
   - Duplicate events → Implement idempotency via eventId

**Raps integration:** "`raps webhook test --event dm.version.added --target http://localhost:3000`"

---

### 12. 3-Legged Auth Visual Walkthrough (`/guides/3legged-auth-visual.md`)

**Why:** The flow is confusing, especially the difference between getting auth code vs exchanging for token. Developers get lost in the redirects.

**Create with diagrams:**

```
┌──────────────┐     1. User clicks "Login"      ┌──────────────┐
│   Your App   │ ─────────────────────────────→  │   Autodesk   │
│              │                                  │   OAuth      │
│              │ ←───────────────────────────── │   Server     │
│              │     2. Redirect to /authorize   │              │
└──────────────┘                                  └──────────────┘
       │                                                 │
       │        3. User enters credentials               │
       │        4. User grants permissions               │
       ↓                                                 ↓
┌──────────────┐     5. Redirect with ?code=...  ┌──────────────┐
│   Callback   │ ←────────────────────────────── │   Autodesk   │
│   Endpoint   │                                  │              │
│              │ ─────────────────────────────→  │              │
│              │     6. Exchange code for token   │              │
└──────────────┘                                  └──────────────┘
       │
       │     7. Store tokens, redirect to app
       ↓
┌──────────────┐
│   App Home   │  Now authenticated!
└──────────────┘
```

**Step-by-step with code:**

| Step | Endpoint | What You Send | What You Get |
|------|----------|---------------|--------------|
| 1 | /authorize | client_id, redirect_uri, scope, response_type=code | Redirect to Autodesk login |
| 2 | (user action) | - | User logs in |
| 3 | /callback | (receive code param) | Authorization code |
| 4 | /token | code, client_id, client_secret, grant_type=authorization_code | access_token, refresh_token |

**Raps integration:** "`raps auth login --3legged` handles this entire flow"

---

### 13. Token Refresh Race Condition Guide (`/guides/token-refresh-patterns.md`)

**Why:** Refresh tokens are one-time-use. Multiple concurrent requests trying to refresh simultaneously cause race conditions and token invalidation.

**The problem:**
```javascript
// BAD: Multiple requests might all try to refresh
async function callApi() {
  if (tokenExpired()) {
    await refreshToken();  // Race condition!
  }
  return fetch(endpoint);
}
```

**The solution (Singleton Promise pattern):**
```javascript
let refreshPromise = null;

async function getValidToken() {
  if (!tokenExpired()) return currentToken;
  
  // Reuse existing refresh if in progress
  if (!refreshPromise) {
    refreshPromise = refreshToken().finally(() => {
      refreshPromise = null;
    });
  }
  
  return refreshPromise;
}
```

**Additional patterns:**
- Proactive refresh (refresh 5 min before expiry)
- Token bucket (pre-fetch multiple tokens)
- Queue pending requests during refresh

**Note:** "The official SDKs don't handle this — you must implement it yourself"

**Raps integration:** "`raps` handles token refresh automatically with proper locking"

---

### 14. Viewer Extension Catalog (`/references/viewer-extensions.md`)

**Why:** Developers build the same extensions repeatedly. Many essential features aren't in core Viewer and require undocumented `viewer.impl` access.

**Catalog community + official extensions:**

| Extension | Purpose | Official? | Notes |
|-----------|---------|-----------|-------|
| Autodesk.Measure | Measurement tool | Yes | Limited (no diameter) |
| Autodesk.Section | Section planes | Yes | Built-in |
| Autodesk.Explode | Explode assemblies | Yes | Built-in |
| TransformTool | Move/rotate objects | Community | Uses `viewer.impl` |
| Markup3D | 3D annotations | Community | forge-viewer-utils |
| StateManager | Save/restore states | Community | forge-viewer-utils |
| BoundingBox | Show bounding boxes | Community | Custom impl |
| PropertySearch | Search properties | Community | Custom impl |

**Link to resources:**
- [library-javascript-viewer-extensions](https://github.com/Autodesk-Forge/library-javascript-viewer-extensions) — 25+ extensions
- [forge-viewer-utils](https://github.com/petrbroz/forge-viewer-utils) — utility wrapper

**Raps integration:** "For server-side property extraction without Viewer, use `raps props extract <urn>`"

---

### 15. Offline Viewing Guide (`/guides/offline-viewing.md`)

**Why:** Enterprise requirement. Multiple community tools exist because there's no official offline solution.

**Options:**

1. **SVF/SVF2 extraction:**
   - Use [forge-convert-utils](https://github.com/petrbroz/forge-convert-utils)
   - Extract to local file system
   - Serve via local HTTP server

2. **Direct SVF loading:**
   ```javascript
   viewer.loadModel('/path/to/output.svf', {
     isAEC: true
   });
   ```

3. **Service worker approach:**
   - Cache viewer JS/CSS
   - Cache model files
   - Works offline after initial load

4. **Limitations:**
   - No live collaboration
   - Manual sync for updates
   - Larger initial download

**Tools:**
- [svf-viewer](https://github.com/NovaShang/svf-viewer) — direct SVF opening
- [viewer-javascript-offline.sample](https://github.com/Autodesk-Forge/viewer-javascript-offline.sample)
- extract.autodesk.io — Autodesk's extraction tool

---

## File Structure (Part 2 additions)

```
raps-marketing/
├── tools/
│   ├── coord-transform.html      ← NEW
│   ├── chunk-calculator.html     ← NEW
│   ├── token-estimator.html      ← NEW
│   ├── region-checker.html       ← NEW
│   └── translation-debugger.html ← NEW
│
├── guides/
│   ├── ifc-translation-deep-dive.md     ← NEW
│   ├── acc-provisioning-checklist.md    ← NEW
│   ├── da-debugging-guide.md            ← NEW
│   ├── viewer-measurement-hacks.md      ← NEW
│   ├── webhook-testing-local.md         ← NEW
│   ├── 3legged-auth-visual.md           ← NEW
│   ├── token-refresh-patterns.md        ← NEW
│   └── offline-viewing.md               ← NEW
│
└── references/
    ├── sdk-compatibility.md        ← NEW
    └── viewer-extensions.md        ← NEW
```

---

## Site Structure Mapping (Part 2)

These additions map to raps-website sections:

```
/tools/
├── coord-transform/      ← Coordinate calculator
├── chunk-calculator/     ← Upload chunking
├── token-estimator/      ← Cost estimation
├── region-checker/       ← US/EMEA debugging
└── translation-debugger/ ← Manifest analysis

/learn/guides/
├── ifc-translation/      ← IFC deep dive
├── acc-provisioning/     ← BIM360/ACC setup
├── da-debugging/         ← Design Automation
├── measurement-hacks/    ← Viewer workarounds
├── webhook-testing/      ← Local webhook setup
├── 3legged-visual/       ← Auth walkthrough
├── token-refresh/        ← Concurrency patterns
└── offline-viewing/      ← Disconnected mode

/references/
├── sdk-compatibility/    ← Version matrix
└── viewer-extensions/    ← Extension catalog
```

---

## Execution Priority

**Highest impact (build first):**
1. Token Cost Estimator — no official calculator exists
2. BIM360/ACC Provisioning Checklist — #1 cause of 403 errors
3. Translation Failure Diagnosis Tool — saves hours of debugging
4. 3-Legged Auth Visual Walkthrough — constant source of confusion

**High impact:**
5. SDK Compatibility Matrix — prevents Revit plugin crashes
6. Region Mismatch Debugger — mysterious failure explainer
7. Chunk Size Calculator — prevents upload failures

**Medium impact:**
8. IFC Translation Guide — complex topic, high search volume
9. Design Automation Debugging Guide — complex setup
10. Token Refresh Patterns — prevents production bugs

**Nice to have:**
11. Coordinate Transformation Calculator — complex, niche
12. Viewer Measurement Workarounds — workarounds for platform limits
13. Webhook Testing Setup — useful but narrower audience
14. Viewer Extension Catalog — reference material
15. Offline Viewing Guide — enterprise niche

---

## SEO Target Keywords (Part 2)

Primary:
- "APS token cost calculator"
- "BIM360 API 403 error"
- "Forge translation failed"
- "APS 3-legged authentication tutorial"
- "Design Automation debugging"

Long-tail:
- "Autodesk Forge TranslationWorker-InternalFailure"
- "Revit plugin Autodesk.Forge.dll conflict"
- "APS webhook ngrok setup"
- "IFC translation units feet meters"
- "BIM360 custom integration setup"
- "Forge Viewer measure diameter"
- "APS EMEA region mismatch"

---

## Quality Notes

- All tools should work standalone (no server required)
- Include "Last verified" dates
- Link to official docs where they exist
- Acknowledge platform limitations honestly
- Position raps as the "easy mode" alternative
