---
title: "APS Developer Cheat Sheet"
description: "Single-page reference for Autodesk Platform Services APIs with RAPS shortcuts"
category: "api"
order: 1
downloadUrl: "/pdfs/aps-cheatsheet.pdf"
keywords: ["APS", "cheat sheet", "reference", "API", "endpoints", "Forge"]
raps_commands: ["raps auth login", "raps dm projects", "raps translate", "raps oss upload"]
raps_version: ">=4.2.0"
aps_apis:
  authentication: "v2"
  data_management: "v1" 
  model_derivative: "v2"
  design_automation: "v3"
  oss: "v2"
last_verified: "January 2026"
---

# APS Developer Cheat Sheet

**Single-page reference for Autodesk Platform Services (APS) with RAPS CLI shortcuts**

---

## 🔐 Authentication

### OAuth Flow Comparison

| **2-Legged OAuth** | **3-Legged OAuth** | **RAPS Command** |
|-------------------|-------------------|------------------|
| **Use Case:** Server-to-server | **Use Case:** User-facing apps | |
| **Context:** App identity only | **Context:** User + app identity | |
| **BIM360/ACC:** Limited access | **BIM360/ACC:** Full project access | |
| **Grant Type:** `client_credentials` | **Grant Type:** `authorization_code` | |
| **Endpoint:** `/authentication/v2/token` | **Endpoint:** `/authentication/v2/authorize` + `/token` | |
| | | `raps auth login` (2-legged default) |
| | | `raps auth login --3legged` |

### Essential OAuth Scopes

| **Scope** | **Purpose** | **Required For** | **RAPS Usage** |
|-----------|-------------|------------------|----------------|
| `data:read` | Read files/projects | Download, list contents | `--scopes data:read` |
| `data:write` | Modify metadata | Update file properties | `--scopes data:read,data:write` |
| `data:create` | Upload files | File uploads, folder creation | `--scopes data:read,data:write,data:create` |
| `bucket:read` | List buckets | OSS bucket operations | `--scopes bucket:read` |
| `bucket:create` | Create buckets | New storage containers | `--scopes bucket:read,bucket:create` |
| `viewables:read` | View models | Viewer SDK, derivatives | `--scopes viewables:read` |
| `code:all` | Design Automation | All DA operations | `--scopes code:all` |
| `account:read` | BIM360/ACC info | Account/project listing | `--scopes account:read` |

### Token Lifecycle

| **Manual Process** | **RAPS Equivalent** |
|-------------------|-------------------|
| POST to `/authentication/v2/token` | `raps auth login` |
| Store token + refresh logic | Automatic token management |
| Check expiry (1 hour default) | `raps auth status` |
| Refresh when needed | `raps auth refresh` |
| Handle auth errors manually | Built-in retry with refresh |

---

## 📁 Data Management API

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
| **List Hubs** | `GET /project/v1/hubs` | `raps dm hubs` |
| **List Projects** | `GET /project/v1/hubs/{hub_id}/projects` | `raps dm projects` |
| **List Folders** | `GET /data/v1/projects/{project_id}/folders/{folder_id}/contents` | `raps dm folders <project_id>` |
| **Upload File** | Multi-step: Create storage → Upload → Create item → Create version | `raps dm upload <file> --project <id>` |
| **Download File** | `GET /data/v1/projects/{project_id}/downloads` + download URL | `raps dm download <item_id>` |
| **Create Folder** | `POST /data/v1/projects/{project_id}/folders` | `raps dm create-folder <name>` |

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

# With RAPS
raps urn encode "urn:adsk.objects:os.object:bucket/file.dwg"
```

---

## 🗄️ Object Storage Service (OSS)

### Bucket Operations

| **Operation** | **Manual API Call** | **RAPS Command** |
|---------------|-------------------|------------------|
| **List Buckets** | `GET /oss/v2/buckets` | `raps bucket list` |
| **Create Bucket** | `POST /oss/v2/buckets` | `raps bucket create <name>` |
| **Bucket Details** | `GET /oss/v2/buckets/{bucketKey}/details` | `raps bucket info <name>` |
| **Delete Bucket** | `DELETE /oss/v2/buckets/{bucketKey}` | `raps bucket delete <name>` |

### Object Operations

| **Operation** | **Manual API Call** | **RAPS Command** |
|---------------|-------------------|------------------|
| **List Objects** | `GET /oss/v2/buckets/{bucketKey}/objects` | `raps oss list <bucket>` |
| **Upload Object** | `PUT /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps oss upload <file> <bucket>` |
| **Download Object** | `GET /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps oss download <bucket> <object>` |
| **Delete Object** | `DELETE /oss/v2/buckets/{bucketKey}/objects/{objectName}` | `raps oss delete <bucket> <object>` |

### Bucket Naming Rules

- ✅ 3-128 characters
- ✅ Lowercase letters, numbers, hyphens
- ✅ Must start/end with letter or number
- ❌ No spaces, underscores, or special chars
- ❌ Cannot look like IP address

---

## 🔄 Model Derivative API

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
| **Start Translation** | `POST /modelderivative/v2/designdata/job` | `raps translate <urn> --formats svf2` |
| **Check Status** | `GET /modelderivative/v2/designdata/{urn}/manifest` | `raps translate status <urn>` |
| **Wait for Completion** | Manual polling with delays | `raps translate <urn> --wait` |
| **Get Properties** | `GET /modelderivative/v2/designdata/{urn}/metadata/{guid}/properties` | `raps translate properties <urn>` |
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

## 🤖 Design Automation API

### Engine Support

| **Engine** | **File Types** | **Version** | **RAPS Command** |
|------------|----------------|-------------|------------------|
| **AutoCAD** | DWG, DXF | 2024 | `raps da engines --filter autocad` |
| **Revit** | RVT, RFA | 2024 | `raps da engines --filter revit` |
| **Inventor** | IPT, IAM | 2024 | `raps da engines --filter inventor` |
| **3ds Max** | MAX | 2024 | `raps da engines --filter max` |
| **Fusion 360** | F3D | Current | `raps da engines --filter fusion` |

### DA Workflow Components

```
AppBundle (your code) + Activity (defines process) + WorkItem (execution instance)
```

| **Component** | **Purpose** | **RAPS Management** |
|---------------|-------------|-------------------|
| **AppBundle** | Custom code/plugins | `raps da appbundle create` |
| **Activity** | Processing definition | `raps da activity create` |
| **WorkItem** | Execution request | `raps da workitem submit` |

---

## 🕸️ Webhooks

### Event Types

| **Service** | **Event** | **Trigger** | **RAPS Setup** |
|-------------|-----------|-------------|----------------|
| **Data Management** | `dm.folder.added` | New folder created | `raps webhook create --event dm.folder.added` |
| **Data Management** | `dm.version.added` | File uploaded/versioned | `raps webhook create --event dm.version.added` |
| **Model Derivative** | `extraction.finished` | Translation complete | `raps webhook create --event extraction.finished` |
| **Model Derivative** | `extraction.updated` | Translation progress | `raps webhook create --event extraction.updated` |

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

## ⚠️ Common Error Codes

| **Code** | **API** | **Cause** | **Manual Fix** | **RAPS Prevention** |
|----------|---------|-----------|----------------|-------------------|
| **400** | All | Invalid request format | Check JSON syntax | Built-in validation |
| **401** | All | Authentication failed | Refresh token | `raps auth refresh` |
| **403** | All | Insufficient permissions | Check scopes | `raps auth status --scopes` |
| **404** | Model Derivative | URN not found | Verify URN encoding | `raps urn encode` |
| **409** | OSS | Bucket name conflict | Use different name | `raps bucket list` first |
| **429** | All | Rate limit exceeded | Implement backoff | Built-in rate limiting |

---

## 📊 Rate Limits

| **API** | **Limit** | **Window** | **RAPS Handling** |
|---------|-----------|------------|------------------|
| **Authentication** | 500 requests/min | 1 minute | Automatic token reuse |
| **Data Management** | 100 requests/min | 1 minute | Intelligent batching |
| **Model Derivative** | 20 concurrent jobs | - | Queue management |
| **OSS** | 500 requests/min | 1 minute | Parallel optimization |
| **Design Automation** | 50 concurrent WorkItems | - | WorkItem queuing |

---

## 🔧 Quick Setup Commands

### First-Time Setup
```bash
# Install RAPS
# Windows: scoop install raps
# macOS: brew install raps
# Linux: cargo install raps-cli

# Initial authentication
raps auth login

# Test connectivity
raps auth status
raps dm projects --limit 1
```

### Common Workflows
```bash
# File Upload → Translation → View
raps oss upload model.rvt mybucket
raps translate $(raps urn encode "urn:adsk.objects:os.object:mybucket:model.rvt") --wait
raps view $(raps urn encode "urn:adsk.objects:os.object:mybucket:model.rvt")

# Batch Operations
raps oss upload-batch *.dwg --bucket mybucket --parallel 5
raps translate-batch --bucket mybucket --formats svf2,pdf

# Data Management Upload
raps dm upload model.rvt --project b.12345678-1234-5678-9abc-123456789012 --folder fol123
```

### Configuration
```bash
# Set preferences
raps config set output.format table
raps config set parallel.max-workers 10
raps config set retry.enabled true

# View current config
raps config list
```

---

## 🌐 Regional Endpoints

| **Region** | **Base URL** | **Use Case** | **RAPS Setting** |
|------------|--------------|--------------|------------------|
| **US** | `developer.api.autodesk.com` | North America | `raps config set region us` |
| **EMEA** | `developer.api.autodesk.com` | Europe/Middle East | `raps config set region emea` |

---

## 📚 Quick References

### URN Quick Commands
```bash
raps urn encode "urn:adsk.objects:os.object:bucket:file.dwg"    # Encode for API
raps urn decode "dXJuOmFkc2sub2JqZWN0cy..."                     # Decode URN
raps urn validate "urn:adsk.objects:os.object:bucket:file.dwg"  # Validate format
```

### Health & Diagnostics
```bash
raps health check                    # Full system check
raps health check --aps-endpoints    # Test APS connectivity
raps auth diagnose                   # Auth troubleshooting
raps debug report                    # Generate support report
```

### Help & Documentation
```bash
raps help                           # General help
raps help auth                      # Command-specific help
raps --version                      # Check version
raps examples                       # Show usage examples
```

---

## 🚨 Emergency Commands

```bash
# Authentication issues
raps auth refresh                   # Refresh expired token
raps auth login --force             # Force re-authentication
raps auth status --verbose         # Detailed auth info

# Operation failures
raps config set retry.max-attempts 5    # Increase retries
raps health check --comprehensive       # Full diagnostic
raps logs --level error --last 1h      # Check recent errors
```

---

**💡 Pro Tips:**
- Use `raps examples` to see common workflow patterns
- Set up multiple profiles with `raps auth login --profile <name>` for different environments
- Enable verbose output with `--verbose` flag for debugging
- Check `raps health check` if anything isn't working

---

*Last verified: January 2026 | RAPS v4.2.1 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3*  
*Print-friendly format • Save for quick reference • Share with your team*