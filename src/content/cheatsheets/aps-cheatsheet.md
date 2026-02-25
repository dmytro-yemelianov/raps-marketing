---
title: "APS Developer Cheat Sheet"
description: "Single-page reference for Autodesk Platform Services APIs with RAPS shortcuts"
category: "api"
order: 1
downloadUrl: "/pdfs/aps-cheatsheet.pdf"
keywords: ["APS", "cheat sheet", "reference", "API", "endpoints", "Forge"]
raps_commands: ["raps auth login", "raps project list", "raps translate start", "raps object upload"]
raps_version: ">=4.14.0"
aps_apis:
  authentication: "v2"
  data_management: "v1"
  model_derivative: "v2"
  design_automation: "v3"
  oss: "v2"
last_verified: "February 2026"
---

# APS Developer Cheat Sheet

**Single-page reference for Autodesk Platform Services (APS) with RAPS CLI shortcuts**

---

## Authentication

### OAuth Flow Comparison

| **2-Legged OAuth** | **3-Legged OAuth** | **RAPS Command** |
|-------------------|-------------------|------------------|
| **Use Case:** Server-to-server | **Use Case:** User-facing apps | |
| **Context:** App identity only | **Context:** User + app identity | |
| **BIM360/ACC:** Limited access | **BIM360/ACC:** Full project access | |
| **Grant Type:** `client_credentials` | **Grant Type:** `authorization_code` | |
| **Endpoint:** `/authentication/v2/token` | **Endpoint:** `/authentication/v2/authorize` + `/token` | |
| | | `raps auth test` (2-legged) |
| | | `raps auth login` (3-legged, opens browser) |

### OAuth Scopes

| **Scope** | **Purpose** | **Required For** |
|-----------|-------------|------------------|
| `data:read` | Read files/projects | Download, list contents |
| `data:write` | Modify metadata | Update file properties |
| `data:create` | Upload files | File uploads, folder creation |
| `bucket:read` | List buckets | OSS bucket operations |
| `bucket:create` | Create buckets | New storage containers |
| `viewables:read` | View models | Viewer SDK, derivatives |
| `code:all` | Design Automation | All DA operations |
| `account:read` | BIM360/ACC info | Account/project listing |

> Scopes are selected interactively during `raps auth login`, or use `--default` for common scopes or `--preset all` for every scope.

### Token Lifecycle

| **Manual Process** | **RAPS Equivalent** |
|-------------------|-------------------|
| POST to `/authentication/v2/token` | `raps auth test` (2-legged) or `raps auth login` (3-legged) |
| Store token + refresh logic | Automatic token management |
| Check expiry (1 hour default) | `raps auth status` |
| Refresh when needed | Automatic (built-in refresh) |
| Inspect token details | `raps auth inspect` |

---

## Data Management API

### Project Hierarchy

```
Hub (Company/Account)
├── Project 1
│   ├── Folder A
│   │   ├── Item 1
│   │   │   ├── Version 1
│   │   │   └── Version 2 (latest)
│   │   └── Item 2
│   └── Folder B
└── Project 2
```

### Common Endpoints

| **Operation** | **Manual API Call** | **RAPS Command** |
|---------------|-------------------|------------------|
| **List Hubs** | `GET /project/v1/hubs` | `raps hub list` |
| **List Projects** | `GET /project/v1/hubs/{hub_id}/projects` | `raps project list` |
| **List Folders** | `GET /data/v1/projects/{project_id}/folders/{folder_id}/contents` | `raps folder list` |
| **Upload File** | Multi-step: Create storage → Upload → Create item → Create version | `raps object upload <bucket> <file>` |
| **Download File** | `GET /oss/v2/buckets/{bucket}/objects/{object}` | `raps object download <bucket> <object>` |
| **Create Folder** | `POST /data/v1/projects/{project_id}/folders` | `raps folder create` |

### URN Formats

| **Context** | **URN Format** | **Example** |
|-------------|----------------|-------------|
| **OSS Object** | `urn:adsk.objects:os.object:{bucket}:{object}` | `urn:adsk.objects:os.object:mybucket:model.rvt` |
| **Data Management** | `urn:adsk.wipprod:dm.lineage:{item_id}` | `urn:adsk.wipprod:dm.lineage:abc123...` |
| **Encoded URN** | Base64 URL-safe encoding | `dXJuOmFkc2sub2JqZWN0cy...` |

**URN Encoding:**
```bash
# Manual (error-prone)
echo -n "urn:adsk.objects:os.object:bucket/file.dwg" | base64 | tr '+/' '-_' | tr -d '='
```

---

## Object Storage Service (OSS)

### Bucket Operations

| **Operation** | **Manual API Call** | **RAPS Command** |
|---------------|-------------------|------------------|
| **List Buckets** | `GET /oss/v2/buckets` | `raps bucket list` |
| **Create Bucket** | `POST /oss/v2/buckets` | `raps bucket create --key <name> --policy transient --region US` |
| **Bucket Details** | `GET /oss/v2/buckets/{bucketKey}/details` | `raps bucket info <name>` |
| **Delete Bucket** | `DELETE /oss/v2/buckets/{bucketKey}` | `raps bucket delete <name>` |

### Object Operations

| **Operation** | **Manual API Call** | **RAPS Command** |
|---------------|-------------------|------------------|
| **List Objects** | `GET /oss/v2/buckets/{bucketKey}/objects` | `raps object list <bucket>` |
| **Upload Object** | `PUT /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps object upload <bucket> <file>` |
| **Upload Batch** | Multiple PUTs | `raps object upload-batch <bucket> <files...> --parallel 4` |
| **Download Object** | `GET /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps object download <bucket> <object>` |
| **Delete Object** | `DELETE /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps object delete <bucket> <object>` |

### Bucket Naming Rules

- 3-128 characters
- Lowercase letters, numbers, hyphens
- Must start/end with letter or number
- No spaces, underscores, or special chars
- Cannot look like IP address

---

## Model Derivative API

### Translation Workflow

```
1. Upload to OSS or Data Management
2. Start Translation Job → GET Job Status (polling)
3. Translation Complete → Download Manifest
4. Extract Viewables/Properties
```

### Translation Operations

| **Operation** | **Manual Process** | **RAPS Command** |
|---------------|-------------------|------------------|
| **Start Translation** | `POST /modelderivative/v2/designdata/job` | `raps translate start <urn> --format svf2` |
| **Start + Wait** | POST + manual polling | `raps translate start <urn> --format svf2 --wait` |
| **Check Status** | `GET /modelderivative/v2/designdata/{urn}/manifest` | `raps translate status <urn>` |
| **Get Manifest** | `GET .../manifest` | `raps translate manifest <urn>` |
| **List Derivatives** | Parse manifest | `raps translate derivatives <urn>` |
| **Get Properties** | `GET /modelderivative/v2/designdata/{urn}/metadata/{guid}/properties` | `raps translate properties <urn> <guid>` |
| **Download Derivatives** | Multiple API calls + file handling | `raps translate download <urn>` |

### Output Formats

| **Format** | **Use Case** | **File Extension** | **RAPS Format Code** |
|------------|--------------|-------------------|-------------------|
| **SVF2** | Web viewer (modern) | `.svf2` | `svf2` |
| **SVF** | Web viewer (legacy) | `.svf` | `svf` |
| **OBJ** | 3D meshes | `.obj` | `obj` |
| **STL** | 3D printing | `.stl` | `stl` |
| **PDF** | 2D drawings | `.pdf` | `pdf` |
| **DWG** | AutoCAD format | `.dwg` | `dwg` |
| **IFC** | Industry standard | `.ifc` | `ifc` |
| **Thumbnail** | Preview images | `.png` | `thumbnail` |

### Translation Status Codes

| **Status** | **Meaning** | **RAPS Action** |
|------------|-------------|-----------------|
| `pending` | Job queued | Continue polling |
| `inprogress` | Processing | Continue polling |
| `success` | Completed successfully | Download derivatives |
| `failed` | Processing failed | Check manifest for errors |
| `timeout` | Took too long | Retry with different settings |

---

## Design Automation API

### Engine Support

| **Engine** | **File Types** | **Version** | **RAPS Command** |
|------------|----------------|-------------|------------------|
| **AutoCAD** | DWG, DXF | 2024 | `raps da engines` |
| **Revit** | RVT, RFA | 2024 | `raps da engines` |
| **Inventor** | IPT, IAM | 2024 | `raps da engines` |
| **3ds Max** | MAX | 2024 | `raps da engines` |

### DA Workflow Components

```
AppBundle (your code) + Activity (defines process) + WorkItem (execution instance)
```

| **Component** | **Purpose** | **RAPS Management** |
|---------------|-------------|-------------------|
| **AppBundle** | Custom code/plugins | `raps da appbundle-create` |
| **Activity** | Processing definition | `raps da activity-create` |
| **WorkItem** | Execution request | `raps da run` |

---

## Webhooks

### Event Types

| **Service** | **Event** | **Trigger** | **RAPS Setup** |
|-------------|-----------|-------------|----------------|
| **Data Management** | `dm.folder.added` | New folder created | `raps webhook create --event dm.folder.added --url <callback>` |
| **Data Management** | `dm.version.added` | File uploaded/versioned | `raps webhook create --event dm.version.added --url <callback>` |
| **Model Derivative** | `extraction.finished` | Translation complete | `raps webhook create --event extraction.finished --url <callback>` |
| **Model Derivative** | `extraction.updated` | Translation progress | `raps webhook create --event extraction.updated --url <callback>` |

### Webhook Payload Structure

```json
{
  "version": "1.0",
  "resourceUrn": "urn:adsk.wipprod:dm.lineage:...",
  "eventType": "dm.version.added",
  "timestamp": "2026-01-07T10:30:00.000Z",
  "payload": {
    "userId": "...",
    "projectId": "...",
    "versionId": "..."
  }
}
```

---

## Common Error Codes

| **Code** | **API** | **Cause** | **Manual Fix** | **RAPS Prevention** |
|----------|---------|-----------|----------------|-------------------|
| **400** | All | Invalid request format | Check JSON syntax | Built-in validation |
| **401** | All | Authentication failed | Refresh token | `raps auth login` (auto-refresh) |
| **403** | All | Insufficient permissions | Check scopes | `raps auth status` |
| **404** | Model Derivative | URN not found | Verify URN encoding | Check base64 encoding |
| **409** | OSS | Bucket name conflict | Use different name | `raps bucket list` first |
| **429** | All | Rate limit exceeded | Implement backoff | Built-in rate limiting |

---

## Rate Limits

| **API** | **Limit** | **Window** | **RAPS Handling** |
|---------|-----------|------------|------------------|
| **Authentication** | 500 requests/min | 1 minute | Automatic token reuse |
| **Data Management** | 100 requests/min | 1 minute | Intelligent batching |
| **Model Derivative** | 20 concurrent jobs | - | Queue management |
| **OSS** | 500 requests/min | 1 minute | Parallel optimization |
| **Design Automation** | 50 concurrent WorkItems | - | WorkItem queuing |

---

## Quick Setup Commands

### First-Time Setup
```bash
# Install RAPS
# Windows: scoop install raps
# macOS: brew install dmytro-yemelianov/tap/raps
# Linux: cargo install raps-cli

# Initial authentication (2-legged test)
raps auth test

# 3-legged login (opens browser)
raps auth login

# Check auth status
raps auth status
```

### Common Workflows
```bash
# Upload file to a bucket
raps object upload mybucket model.rvt

# Translate uploaded file
raps translate start <base64-urn> --format svf2 --wait

# List available derivatives
raps translate derivatives <base64-urn>

# Download derivatives
raps translate download <base64-urn>

# Batch upload multiple files
raps object upload-batch mybucket *.dwg --parallel 4
```

### Configuration
```bash
# Set profile values
raps config set client_id YOUR_CLIENT_ID
raps config set client_secret YOUR_SECRET
raps config set base_url https://developer.api.autodesk.com

# Get a config value
raps config get client_id

# Manage profiles
raps config profile create myprofile
raps config profile list
raps config profile use myprofile
```

---

## Regional Endpoints

| **Region** | **Base URL** | **Use Case** | **RAPS Setting** |
|------------|--------------|--------------|------------------|
| **US** | `developer.api.autodesk.com` | North America | `raps config set base_url https://developer.api.autodesk.com` |
| **EMEA** | `developer.api.autodesk.com` | Europe/Middle East | `raps config set base_url https://developer.api.autodesk.com` |

---

## Help & Documentation
```bash
raps --help                          # General help
raps auth --help                     # Command-specific help
raps translate --help                # Translate subcommands
raps --version                       # Check version
```

---

**Pro Tips:**
- Use `--default` with `raps auth login` to skip scope selection
- Use `--device` with `raps auth login` for headless/CI environments
- Use `--format json` on most commands for machine-readable output
- Use `raps auth inspect` to check token details and expiry

---

*Last verified: February 2026 | RAPS v4.14.0 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3*
*Print-friendly format - Save for quick reference - Share with your team*
