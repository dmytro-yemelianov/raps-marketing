---
title: "Upload, Translate, and View Workflow Recipe"
description: "Complete step-by-step recipe for uploading CAD files, translating them, and viewing derivatives"
difficulty: "beginner"
estimatedTime: "10 minutes"
prerequisites: ["CAD file (any format)", "Valid APS access token", "Basic command line knowledge"]
apis: ["OSS v2", "Model Derivative v2", "Authentication v2"]
keywords: ["APS", "workflow", "recipe", "upload", "translate", "viewer", "3D", "SVF2"]
raps_commands: ["raps object upload", "raps translate start", "raps translate download"]
raps_version: ">=4.14.0"
aps_apis:
  authentication: "v2"
  oss: "v2"
  model_derivative: "v2"
last_verified: "February 2026"
---

# Upload, Translate, and View Workflow Recipe

**Complete recipe for the most common APS workflow: upload a CAD file, translate it to a viewable format, and download derivatives**

---

## Goal

Transform a CAD file (`.dwg`, `.rvt`, `.ipt`, etc.) into web-viewable SVF2 format and download the output.

**What you'll achieve:**
- Upload CAD files to cloud storage
- Convert files to web-optimized format (SVF2)
- Download translated derivatives
- Extract model metadata and properties

---

## Prerequisites

### Required Tools
- **RAPS CLI** v4.14.0+ installed
- **Autodesk Developer Account** with app credentials
- **CAD file** to test with (`.dwg`, `.rvt`, `.ipt`, `.f3d`, etc.)

### Required OAuth Scopes
```
data:read data:create bucket:read bucket:create viewables:read
```

### Files Used in This Recipe
- `model.rvt` - Sample Revit file (replace with your CAD file)
- `my-bucket` - Bucket name (replace with your unique bucket name)

---

## The Manual Way (100+ Lines of Code)

To appreciate what RAPS does, here's the manual approach:

<details>
<summary>Click to see manual implementation (JavaScript example)</summary>

```javascript
const axios = require('axios');
const fs = require('fs');

// Step 1: Get access token
async function getToken() {
  const response = await axios.post(
    'https://developer.api.autodesk.com/authentication/v2/token',
    new URLSearchParams({
      client_id: process.env.APS_CLIENT_ID,
      client_secret: process.env.APS_CLIENT_SECRET,
      grant_type: 'client_credentials',
      scope: 'bucket:read bucket:create data:read viewables:read'
    }),
    { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
  );
  return response.data.access_token;
}

// Step 2: Create bucket
async function createBucket(token, bucketKey) {
  try {
    await axios.post(
      'https://developer.api.autodesk.com/oss/v2/buckets',
      { bucketKey: bucketKey, policyKey: 'transient' },
      { headers: { Authorization: `Bearer ${token}` }}
    );
  } catch (error) {
    if (error.response?.status !== 409) throw error;
  }
}

// Step 3: Upload file
async function uploadFile(token, bucketKey, fileName, fileData) {
  const response = await axios.put(
    `https://developer.api.autodesk.com/oss/v2/buckets/${bucketKey}/objects/${fileName}`,
    fileData,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/octet-stream'
      }
    }
  );
  return response.data.objectId;
}

// Step 4: Start translation
async function startTranslation(token, urn) {
  await axios.post(
    'https://developer.api.autodesk.com/modelderivative/v2/designdata/job',
    {
      input: { urn: urn },
      output: { formats: [{ type: 'svf2', views: ['2d', '3d'] }] }
    },
    { headers: { Authorization: `Bearer ${token}` }}
  );
}

// Step 5: Poll for completion
async function waitForTranslation(token, urn) {
  while (true) {
    const response = await axios.get(
      `https://developer.api.autodesk.com/modelderivative/v2/designdata/${urn}/manifest`,
      { headers: { Authorization: `Bearer ${token}` }}
    );
    if (response.data.status === 'success') return true;
    if (response.data.status === 'failed') throw new Error('Translation failed');
    await new Promise(resolve => setTimeout(resolve, 5000));
  }
}

// Main workflow
async function main() {
  const token = await getToken();
  const bucketKey = 'my-bucket-' + Date.now();
  await createBucket(token, bucketKey);
  const fileData = fs.readFileSync('./model.rvt');
  await uploadFile(token, bucketKey, 'model.rvt', fileData);
  const urn = Buffer.from(`urn:adsk.objects:os.object:${bucketKey}:model.rvt`)
    .toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
  await startTranslation(token, urn);
  await waitForTranslation(token, urn);
  console.log('Done! URN:', urn);
}

main();
```

**That's 80+ lines of code with incomplete error handling!**

</details>

---

## The RAPS Way

### Step 1: Authenticate

```bash
# 2-legged (server-to-server, client credentials)
raps auth test

# Or 3-legged (user-facing, opens browser)
raps auth login
# Use --default for common scopes, or --preset all for every scope
```

**What happens:**
- 2-legged: validates client credentials and gets an access token
- 3-legged: opens browser for OAuth flow, saves token securely to system keychain
- Token refresh is automatic for subsequent commands

### Step 2: Create a Storage Bucket

```bash
# Interactive (prompts for name, policy, region)
raps bucket create

# Or fully specified
raps bucket create --key my-project-bucket --policy transient --region US
```

**What happens:**
- Creates a new Object Storage Service (OSS) bucket
- Policy options: `transient` (24h), `temporary` (30 days), `persistent` (permanent)
- Region options: `US`, `EMEA`

### Step 3: Upload Your CAD File

```bash
# Upload file to bucket
raps object upload my-project-bucket model.rvt
```

**What happens:**
- Uploads the file with progress indicator
- For large files, use `--resume` to resume interrupted uploads
- Returns the object key for building the URN

### Step 4: Translate to Web Format

```bash
# Build base64 URN and start translation
URN=$(echo -n "urn:adsk.objects:os.object:my-project-bucket:model.rvt" | base64 | tr '+/' '-_' | tr -d '=')

# Start translation and wait for completion
raps translate start "$URN" --format svf2 --wait
```

**What happens:**
- Submits translation job to Model Derivative service
- `--wait` polls for completion automatically
- Shows progress updates during translation
- `--force` can be added to re-translate even if a manifest already exists

### Step 5: Download Derivatives

```bash
# List available derivatives
raps translate derivatives "$URN"

# Download all derivatives
raps translate download "$URN" --all --out-dir ./output

# Or download specific format
raps translate download "$URN" --format obj --out-dir ./output
```

**What happens:**
- Lists or downloads translated output files
- `--all` downloads everything available
- `--format` filters to a specific output format

---

## Batch Upload Workflow

For processing multiple files at once:

```bash
# Upload multiple files in parallel
raps object upload-batch my-project-bucket *.dwg --parallel 4

# Then translate each one
for file in *.dwg; do
  urn=$(echo -n "urn:adsk.objects:os.object:my-project-bucket:$file" | base64 | tr '+/' '-_' | tr -d '=')
  raps translate start "$urn" --format svf2 --wait
done
```

---

## Translation Format Options

You can translate to different output formats:

```bash
# SVF2 (recommended for web viewing)
raps translate start "$URN" --format svf2 --wait

# OBJ (3D meshes)
raps translate start "$URN" --format obj --wait

# STL (3D printing)
raps translate start "$URN" --format stl --wait

# IFC (industry standard exchange)
raps translate start "$URN" --format ifc --wait
```

---

## Webhook Notifications

Instead of polling, set up webhooks to be notified when translation completes:

```bash
# Create webhook for translation completion
raps webhook create --event extraction.finished --url https://your-app.com/hooks/done

# List all webhooks
raps webhook list

# Test webhook endpoint
raps webhook test https://your-app.com/hooks/done
```

---

## Troubleshooting Common Issues

### Issue 1: "Bucket already exists" Error

**Problem:** Bucket name conflicts (names are globally unique)
**Solution:** Use a more unique bucket name
```bash
BUCKET_NAME="my-project-$(date +%s)"
raps bucket create --key "$BUCKET_NAME" --policy transient --region US
```

### Issue 2: Translation Fails

**Problem:** Unsupported file format or corrupted file
**Solution:** Check translation status for error details
```bash
# Check status
raps translate status "$URN"

# Check full manifest for error details
raps translate manifest "$URN"
```

### Issue 3: Authentication Errors

**Problem:** Token expired or wrong scopes
**Solution:** Re-authenticate
```bash
# Check current auth status
raps auth status

# Inspect token details
raps auth inspect

# Re-login
raps auth login --default
```

### Issue 4: Large File Upload Fails

**Problem:** Network interruption during upload
**Solution:** Use resume flag
```bash
# Resume interrupted upload
raps object upload my-bucket large-model.rvt --resume
```

---

## CI/CD Integration

```yaml
# GitHub Actions example
name: Process CAD Models
on:
  push:
    paths: ['models/**']

jobs:
  translate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install RAPS
        run: cargo install raps-cli

      - name: Authenticate
        run: raps auth login --token ${{ secrets.APS_ACCESS_TOKEN }}

      - name: Upload and translate
        run: |
          raps object upload production-bucket models/building.rvt
          URN=$(echo -n "urn:adsk.objects:os.object:production-bucket:building.rvt" | base64 | tr '+/' '-_' | tr -d '=')
          raps translate start "$URN" --format svf2 --wait
```

---

## Performance Tips

1. **Use SVF2 format** - loads faster than legacy SVF
2. **Batch uploads** - `raps object upload-batch` processes files in parallel
3. **Reuse buckets** - create once, upload many files
4. **Use `--wait`** - avoids manual polling in scripts
5. **Resume large uploads** - `--resume` flag handles network interruptions

---

*Last verified: February 2026 | RAPS v4.14.0 | APS APIs: OSS v2, Model Derivative v2*
*This recipe works with all major CAD formats supported by APS Model Derivative service.*
