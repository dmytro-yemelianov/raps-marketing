---
title: "Upload → Translate → View Workflow Recipe"
description: "Complete step-by-step recipe for uploading CAD files, translating them, and viewing in browser"
keywords: ["APS", "workflow", "recipe", "upload", "translate", "viewer", "3D", "SVF2"]
raps_commands: ["raps oss upload", "raps translate", "raps view", "raps urn encode"]
raps_version: ">=4.2.0"
aps_apis:
  authentication: "v2"
  oss: "v2"
  model_derivative: "v2"
  viewer: "v7"
last_verified: "January 2026"
---

# Upload → Translate → View Workflow Recipe

**Complete recipe for the most common APS workflow: upload a CAD file, translate it to web-viewable format, and display in browser**

---

## Goal

Transform a CAD file (`.dwg`, `.rvt`, `.ipt`, etc.) into a 3D model viewable in any web browser.

**What you'll achieve:**
- Upload CAD files to cloud storage
- Convert files to web-optimized 3D format (SVF2)
- Display interactive 3D models in browser
- Extract model properties and metadata

---

## Prerequisites

### Required Tools
- ✅ **RAPS CLI** v4.2.0+ installed
- ✅ **Autodesk Developer Account** with app credentials
- ✅ **CAD file** to test with (`.dwg`, `.rvt`, `.ipt`, `.f3d`, etc.)
- ✅ **Modern web browser** (Chrome, Firefox, Safari, Edge)

### Required Scopes
```bash
# Authentication scopes needed for this workflow
data:read bucket:read bucket:create viewables:read
```

### Files Used in This Recipe
- `model.rvt` - Sample Revit file (replace with your CAD file)
- `my-bucket` - Bucket name (replace with your unique bucket name)

---

## The Manual Way (50+ Lines of Code)

To appreciate what RAPS does, here's the manual approach:

<details>
<summary>🔍 Click to see manual implementation (JavaScript example)</summary>

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
      {
        bucketKey: bucketKey,
        policyKey: 'transient'
      },
      { headers: { Authorization: `Bearer ${token}` }}
    );
  } catch (error) {
    if (error.response?.status !== 409) throw error; // Ignore if exists
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
  const response = await axios.post(
    'https://developer.api.autodesk.com/modelderivative/v2/designdata/job',
    {
      input: { urn: urn },
      output: {
        formats: [{
          type: 'svf2',
          views: ['2d', '3d']
        }]
      }
    },
    { headers: { Authorization: `Bearer ${token}` }}
  );
  return response.data.urn;
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
    
    await new Promise(resolve => setTimeout(resolve, 5000)); // Wait 5 seconds
  }
}

// Step 6: Generate viewer HTML
function generateViewerHTML(urn, token) {
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <script src="https://developer.api.autodesk.com/modelderivative/v2/viewers/7.*/viewer3D.min.js"></script>
    </head>
    <body>
      <div id="forgeViewer" style="width: 100%; height: 500px;"></div>
      <script>
        const options = {
          env: 'AutodeskProduction',
          api: 'derivativeV2',
          getAccessToken: function(onTokenReady) {
            onTokenReady('${token}', 3600);
          }
        };
        
        Autodesk.Viewing.Initializer(options, function() {
          const viewer = new Autodesk.Viewing.GuiViewer3D(
            document.getElementById('forgeViewer')
          );
          viewer.start();
          viewer.loadDocumentNode(viewer, '${urn}');
        });
      </script>
    </body>
    </html>
  `;
}

// Main workflow (6 steps, error handling, base64 encoding...)
async function main() {
  try {
    console.log('1. Getting access token...');
    const token = await getToken();
    
    console.log('2. Creating bucket...');
    const bucketKey = 'my-bucket-' + Date.now();
    await createBucket(token, bucketKey);
    
    console.log('3. Uploading file...');
    const fileData = fs.readFileSync('./model.rvt');
    const objectId = await uploadFile(token, bucketKey, 'model.rvt', fileData);
    
    console.log('4. Starting translation...');
    const urn = Buffer.from(`urn:adsk.objects:os.object:${bucketKey}:model.rvt`)
                     .toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    await startTranslation(token, urn);
    
    console.log('5. Waiting for translation...');
    await waitForTranslation(token, urn);
    
    console.log('6. Generating viewer...');
    const html = generateViewerHTML(urn, token);
    fs.writeFileSync('./viewer.html', html);
    
    console.log('✅ Complete! Open viewer.html in browser');
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

main();
```

**That's 120+ lines of code with incomplete error handling!**

</details>

---

## The RAPS Way (5 Commands)

### Step 1: Authenticate

```bash
# One-time setup: login with required scopes
raps auth login --scopes bucket:read,bucket:create,data:read,viewables:read
```

**What happens:**
- Opens browser for OAuth flow
- Saves credentials securely to system keyring
- Validates scopes work correctly

### Step 2: Create Storage Bucket

```bash
# Create a bucket for your files (bucket names must be globally unique)
raps bucket create my-bucket-$(date +%s)
```

**What happens:**
- Creates a new Object Storage Service (OSS) bucket
- Handles naming conflicts automatically
- Sets appropriate retention policies

### Step 3: Upload Your CAD File

```bash
# Upload file to bucket
raps oss upload model.rvt my-bucket-$(date +%s)
```

**What happens:**
- Uploads file with progress indicator
- Validates file integrity
- Returns the file's URN for translation

### Step 4: Translate to Web Format

```bash
# Start translation job (using SVF2 for best performance)
raps translate $(raps urn encode "urn:adsk.objects:os.object:my-bucket-1234567890:model.rvt") --formats svf2 --wait
```

**What happens:**
- Encodes URN correctly (handles base64 URL-safe encoding)
- Submits translation job to Model Derivative service
- Polls for completion automatically with `--wait` flag
- Shows progress updates during translation

### Step 5: View in Browser

```bash
# Generate and open viewer
raps view $(raps urn encode "urn:adsk.objects:os.object:my-bucket-1234567890:model.rvt")
```

**What happens:**
- Generates HTML viewer with embedded 3D model
- Handles authentication token injection
- Opens browser automatically
- Provides interactive 3D navigation

---

## Complete One-Liner Workflow

Once authenticated, the entire workflow can be done in one command:

```bash
# Upload, translate, and view in one command
raps workflow upload-translate-view model.rvt --bucket my-project-bucket
```

**What this does:**
1. Creates bucket if needed
2. Uploads the file
3. Starts translation to SVF2
4. Waits for completion
5. Opens browser viewer

---

## Workflow Variations

### Batch Processing Multiple Files

```bash
# Upload and translate multiple files
raps workflow batch-translate *.dwg --bucket cad-drawings --formats svf2,pdf --parallel 3
```

### Extract Properties Only

```bash
# Get model metadata without viewing
raps translate <urn> --formats properties --output metadata.json
```

### Custom Translation Formats

```bash
# Translate to multiple formats for different uses
raps translate <urn> --formats svf2,stl,obj,pdf --wait
```

### Webhook Integration

```bash
# Set up webhook to get notified when translations complete
raps webhook create --event extraction.finished --callback https://your-app.com/webhook
```

---

## Troubleshooting Common Issues

### Issue 1: "Bucket already exists" Error

**Problem:** Bucket name conflicts  
**Solution:** Use timestamps or UUIDs in bucket names
```bash
# Add timestamp to ensure uniqueness
BUCKET_NAME="my-project-$(date +%s)"
raps bucket create $BUCKET_NAME
```

### Issue 2: Translation Fails

**Problem:** Unsupported file format or corrupted file  
**Solution:** Check file and format support
```bash
# Check translation status with details
raps translate status <urn> --verbose

# Retry with different format
raps translate <urn> --formats svf --retry
```

### Issue 3: Viewer Shows "Loading..." Forever

**Problem:** Translation not complete or token expired  
**Solution:** Check translation status and refresh auth
```bash
# Verify translation completed successfully
raps translate status <urn>

# Refresh authentication if needed
raps auth refresh
```

### Issue 4: File Upload Fails

**Problem:** File too large or network issues  
**Solution:** Check file size and use resumable upload
```bash
# Check file size (max 100MB for standard upload)
ls -lh model.rvt

# Use chunked upload for large files
raps oss upload model.rvt my-bucket --chunked --chunk-size 10MB
```

### Issue 5: Permission Denied

**Problem:** Missing required scopes  
**Solution:** Re-authenticate with correct scopes
```bash
# Check current scopes
raps auth status --scopes

# Re-login with required scopes
raps auth login --scopes bucket:read,bucket:create,data:read,viewables:read
```

---

## Performance Tips

### 1. Use SVF2 Format

SVF2 loads 50% faster than legacy SVF format:
```bash
# Always prefer SVF2 for new projects
raps translate <urn> --formats svf2
```

### 2. Pre-create Buckets

Create buckets once, reuse many times:
```bash
# Create project bucket
raps bucket create my-project-models

# Upload multiple files to same bucket
raps oss upload model1.rvt my-project-models
raps oss upload model2.dwg my-project-models
```

### 3. Batch Operations

Process multiple files efficiently:
```bash
# Parallel uploads (faster than sequential)
raps oss upload-batch *.rvt --bucket my-models --parallel 5

# Batch translation with progress
raps translate-batch --bucket my-models --formats svf2 --parallel 3
```

### 4. Monitor Translation Queue

Large files can take time to translate:
```bash
# Start translation without waiting
raps translate <urn> --formats svf2

# Check status later
raps translate status <urn>

# Get notified when done (if webhooks set up)
raps translate <urn> --notify-webhook https://your-app.com/done
```

---

## Advanced Scenarios

### Scenario 1: Assembly Files with Dependencies

For CAD assemblies with multiple linked files:

```bash
# Upload all related files to same bucket
raps oss upload main-assembly.iam my-project
raps oss upload part1.ipt my-project  
raps oss upload part2.ipt my-project

# Translate main assembly (will find dependencies automatically)
raps translate $(raps urn encode "urn:adsk.objects:os.object:my-project:main-assembly.iam") --formats svf2
```

### Scenario 2: Password-Protected Files

For encrypted/password-protected CAD files:

```bash
# Include password in translation request
raps translate <urn> --formats svf2 --password "your-file-password"
```

### Scenario 3: Custom Viewer Integration

Generate embeddable viewer code for your website:

```bash
# Generate viewer HTML with custom options
raps view <urn> --generate-embed --width 800 --height 600 --toolbar minimal > embed.html
```

### Scenario 4: Region-Specific Deployment

For EMEA data residency requirements:

```bash
# Configure for European data centers
raps config set region emea

# All subsequent operations use EMEA endpoints
raps bucket create eu-project-models --region emea
```

---

## Cost Optimization

### Understanding APS Pricing

| Operation | Cost Factor | RAPS Optimization |
|-----------|-------------|-------------------|
| **OSS Storage** | Per GB per month | Auto-cleanup old files |
| **Translation** | Per job | Batch processing |
| **Viewer** | Per view session | Token reuse |
| **API Calls** | Per request | Request batching |

### Cost-Saving Tips

```bash
# Enable automatic cleanup of old translations
raps config set cleanup.auto-delete-derivatives true
raps config set cleanup.retention-days 30

# Use transient buckets for temporary files
raps bucket create temp-bucket --policy transient

# Monitor usage
raps usage report --period last-month
```

---

## Integration Examples

### Web Application Integration

```javascript
// In your Node.js app
const { exec } = require('child_process');

// Upload and translate via RAPS
function processCADFile(filePath, bucketName) {
  return new Promise((resolve, reject) => {
    const cmd = `raps workflow upload-translate-view "${filePath}" --bucket ${bucketName} --output-urn`;
    
    exec(cmd, (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve(stdout.trim()); // Returns URN for viewer
    });
  });
}

// Use in your route
app.post('/upload-model', async (req, res) => {
  try {
    const urn = await processCADFile(req.file.path, 'user-models');
    res.json({ urn, viewerUrl: `/viewer?urn=${urn}` });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});
```

### CI/CD Pipeline Integration

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
      - uses: actions/checkout@v3
      
      - name: Install RAPS
        run: curl -sSL https://rapscli.xyz/install.sh | sh
        
      - name: Authenticate
        run: raps auth login --client-id ${{ secrets.APS_CLIENT_ID }} --client-secret ${{ secrets.APS_CLIENT_SECRET }}
        
      - name: Process changed models
        run: |
          for file in $(git diff --name-only HEAD~1 | grep '\.rvt$'); do
            echo "Processing $file..."
            raps workflow upload-translate-view "$file" --bucket ci-models
          done
```

---

## Next Steps

### Once you've mastered this workflow:

1. **🎯 Try other recipes:**
   - [Extract Properties Recipe](./extract-properties.md)
   - [Batch Processing Recipe](./batch-translate.md)
   - [Webhook Integration Recipe](./webhook-setup.md)

2. **📚 Learn advanced features:**
   - Custom viewer extensions
   - Property filtering and search
   - Real-time collaboration

3. **🚀 Scale your application:**
   - Load balancing translation jobs
   - Caching strategies
   - Error recovery patterns

### Resources

- **RAPS Documentation:** [rapscli.xyz/docs](https://rapscli.xyz/docs/)
- **APS Viewer SDK:** [aps.autodesk.com/developer/documentation](https://aps.autodesk.com/developer/documentation)
- **Community Support:** [discord.gg/raps-community](https://discord.gg/raps-community)

---

**💡 Pro Tip:** Save time by creating aliases for common workflows:
```bash
# Add to your .bashrc or .zshrc
alias translate-view='raps workflow upload-translate-view'
alias quick-upload='raps oss upload'

# Then use like:
translate-view my-model.rvt --bucket project-alpha
```

---

*Last verified: January 2026 | RAPS v4.2.1 | APS APIs: OSS v2, Model Derivative v2, Viewer v7*  
*This recipe works with all major CAD formats. For format-specific notes, see the [APS Format Support Guide](../references/supported-formats.md).*