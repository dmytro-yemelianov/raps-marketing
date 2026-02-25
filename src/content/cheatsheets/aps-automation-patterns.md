---
title: "APS Automation Patterns Cheat Sheet"
description: "Common automation workflows and patterns for Autodesk Platform Services with RAPS CLI"
category: "workflows"
order: 2
downloadUrl: "/pdfs/aps-automation-patterns.pdf"
---

# APS Automation Patterns Cheat Sheet

---

**RAPS Version**: 4.14.0
**APS API Coverage**: Data Management v1, Model Derivative v2, OSS v2, Authentication v2, Construction Cloud v1, Design Automation v3

---

## Common Automation Workflows

### File Processing Pipeline
```bash
# Pattern: Upload → Translate → Download derivatives
# 1. Upload a model to OSS
raps object upload mybucket model.rvt

# 2. Start translation (the URN is base64-encoded)
raps translate start <base64-urn> --format svf2 --wait

# 3. Check available derivatives
raps translate derivatives <base64-urn>

# 4. Download translated output
raps translate download <base64-urn> --out-dir ./output
```

### Batch File Upload
```bash
# Upload multiple files in parallel
raps object upload-batch mybucket *.dwg --parallel 4

# Upload with resume support for large files
raps object upload mybucket large-model.rvt --resume
```

### Design Automation Workflow
```bash
# 1. List available engines
raps da engines

# 2. Create an app bundle with your custom plugin
raps da appbundle-create --id MyPlugin --engine Autodesk.Revit+2024 --description "Extract parameters"

# 3. Upload the plugin archive
raps da appbundle-upload --id MyPlugin --archive ./plugin.zip --engine Autodesk.Revit+2024

# 4. Create an activity that uses your bundle
raps da activity-create --file activity-definition.json

# 5. Run a work item
raps da run --activity MyPlugin.ExtractParams+prod --file workitem.json
```

---

## CI/CD Integration Patterns

### GitHub Actions
```yaml
name: APS Model Processing
on:
  push:
    branches: [main]
    paths: ['models/**']
jobs:
  process:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install RAPS
        run: cargo install raps-cli

      - name: Authenticate
        run: raps auth login --token ${{ secrets.APS_ACCESS_TOKEN }}

      - name: Upload models
        run: |
          for file in models/*.rvt; do
            raps object upload production-bucket "$file"
          done

      - name: Start translations
        run: |
          for file in models/*.rvt; do
            filename=$(basename "$file")
            urn=$(echo -n "urn:adsk.objects:os.object:production-bucket:$filename" | base64 | tr '+/' '-_' | tr -d '=')
            raps translate start "$urn" --format svf2 --wait
          done
```

### Docker Integration
```dockerfile
FROM rust:1.88-slim AS builder
RUN cargo install raps-cli

FROM debian:bookworm-slim
COPY --from=builder /usr/local/cargo/bin/raps /usr/local/bin/raps

# Set credentials via environment
ENV APS_CLIENT_ID=""
ENV APS_CLIENT_SECRET=""

ENTRYPOINT ["raps"]
```

```bash
# Run RAPS in Docker
docker run -e APS_CLIENT_ID=$CLIENT_ID -e APS_CLIENT_SECRET=$SECRET \
  raps-cli auth test
```

### Shell Script Automation
```bash
#!/usr/bin/env bash
set -euo pipefail

# Authenticate (2-legged for server-to-server)
raps auth test

# Upload and translate all .dwg files in a directory
for file in ./input/*.dwg; do
  filename=$(basename "$file")
  echo "Processing: $filename"

  # Upload
  raps object upload my-bucket "$file"

  # Build URN and translate
  urn=$(echo -n "urn:adsk.objects:os.object:my-bucket:$filename" | base64 | tr '+/' '-_' | tr -d '=')
  raps translate start "$urn" --format svf2 --wait

  # Download derivatives
  raps translate download "$urn" --out-dir "./output/$filename/"
done
```

---

## Pipeline Automation

### RAPS Pipeline Files
RAPS supports YAML pipeline definitions for multi-step automation.

```yaml
# pipeline.yml
name: model-processing
steps:
  - name: authenticate
    command: "raps auth test"

  - name: upload-model
    command: "raps object upload ${BUCKET} ${INPUT_FILE}"

  - name: translate
    command: "raps translate start ${URN} --format svf2 --wait"
    continue_on_error: false

  - name: download-output
    command: "raps translate download ${URN} --out-dir ${OUTPUT_DIR}"
```

```bash
# Validate pipeline syntax
raps pipeline validate pipeline.yml

# Run with variable substitution
raps pipeline run pipeline.yml \
  --var BUCKET=my-bucket \
  --var INPUT_FILE=model.rvt \
  --var URN=dXJuOmFkc2... \
  --var OUTPUT_DIR=./output

# Dry run to see what would execute
raps pipeline run pipeline.yml --dry-run
```

---

## Webhook-Driven Automation

### Event-Driven Processing
```bash
# List available webhook event types
raps webhook events

# Set up webhook for file uploads
raps webhook create --event dm.version.added --url https://myserver.com/hooks/new-version

# Set up webhook for translation completion
raps webhook create --event extraction.finished --url https://myserver.com/hooks/translation-done

# List active webhooks
raps webhook list

# Test webhook endpoint connectivity
raps webhook test https://myserver.com/hooks/new-version --timeout 10

# Verify webhook signature authenticity
raps webhook verify-signature '{"payload":"..."}' --signature "abc123..."
```

---

## Object Management Patterns

### Bucket Lifecycle
```bash
# Create buckets with different retention policies
raps bucket create --key temp-processing --policy transient --region US
raps bucket create --key project-archive --policy persistent --region US

# List all buckets
raps bucket list

# Check bucket details
raps bucket info my-bucket

# Clean up temporary bucket
raps bucket delete temp-processing --yes
```

### Object Operations
```bash
# Copy objects between buckets
raps object copy --source-bucket staging --source-key model.rvt \
  --dest-bucket production --dest-key model.rvt

# Batch copy all objects
raps object batch-copy --source-bucket staging --dest-bucket production

# Rename objects within a bucket
raps object rename --bucket my-bucket --old-key draft.rvt --new-key final.rvt

# Get pre-signed download URL
raps object signed-url my-bucket model.rvt

# Get object details
raps object info my-bucket model.rvt
```

---

## Profile and Configuration Management

### Multi-Environment Setup
```bash
# Create separate profiles for dev/staging/production
raps config profile create development
raps config set client_id DEV_CLIENT_ID
raps config set client_secret DEV_SECRET

raps config profile create production
raps config set client_id PROD_CLIENT_ID
raps config set client_secret PROD_SECRET

# Switch between environments
raps config profile use development
raps auth test

raps config profile use production
raps auth test

# List all profiles
raps config profile list
```

### Working Context
```bash
# Set default hub/project context to avoid repeating IDs
raps config context set hub_id b.12345678-abcd-1234-5678-abcdef123456
raps config context set project_id b.87654321-dcba-4321-8765-fedcba654321

# Show current context
raps config context show

# Clear context
raps config context set hub_id clear
```

---

## Model Derivative Patterns

### Translation with Metadata Extraction
```bash
# Start translation
raps translate start <urn> --format svf2 --wait

# Get model metadata (views/viewables)
raps translate metadata <urn>

# Get object tree for a specific view
raps translate tree <urn> <view-guid>

# Extract properties from a view
raps translate properties <urn> <view-guid>

# Query specific object properties
raps translate query-properties <urn> <view-guid> --filter "1,2,3" --fields "name,value"
```

### Translation Presets
```bash
# List available presets
raps translate preset list

# Use presets for consistent translation settings
raps translate start <urn> --format svf2 --wait
```

---

## Authentication Patterns

### Token Management for CI/CD
```bash
# Direct token injection (CI/CD)
raps auth login --token $APS_ACCESS_TOKEN

# With refresh token for long-running jobs
raps auth login --token $APS_ACCESS_TOKEN --refresh-token $APS_REFRESH_TOKEN

# Device code flow for headless environments
raps auth login --device

# Check token health before operations
raps auth inspect --warn-expiry-seconds 300

# View current auth status
raps auth status

# See authenticated user info (3-legged only)
raps auth whoami
```

### Keychain Security
```bash
# Migrate plaintext tokens to OS keychain
raps config migrate-tokens

# Check current auth configuration
raps config get client_id
```

---

## Best Practices

### Do's
- Use `raps config profile` to separate dev/staging/production credentials
- Use `--wait` flag on translations to block until completion in scripts
- Use `raps auth inspect --warn-expiry-seconds 300` in CI to catch expiring tokens
- Use `raps object upload-batch` for multiple files instead of sequential uploads
- Use `raps pipeline validate` before running pipelines
- Store credentials in environment variables or CI secrets, never in scripts

### Don'ts
- Don't hardcode client IDs or secrets in automation scripts
- Don't poll translation status in tight loops (use `--wait` flag instead)
- Don't skip error checking in shell scripts (use `set -euo pipefail`)
- Don't use transient buckets for data you need to keep long-term
- Don't ignore the `--resume` flag for large file uploads

---

*APS Automation Patterns | RAPS v4.14.0 | APS APIs: DM v1, MD v2, OSS v2, Auth v2, CC v1, DA v3 | Updated: February 2026*
