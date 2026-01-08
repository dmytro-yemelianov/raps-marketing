---
title: "APS OAuth Scopes Reference"
description: "Complete guide to Autodesk Platform Services OAuth scopes and permissions"
category: "scopes"
lastUpdated: 2026-01-08
completeness: "complete"
keywords: ["APS", "OAuth", "scopes", "permissions", "authentication", "Forge API"]
raps_commands: ["raps auth login", "raps auth status"]
raps_version: ">=4.2.0"
aps_apis:
  authentication: "v2"
last_verified: "January 2026"
---

# APS OAuth Scopes Reference

**Complete guide to Autodesk Platform Services OAuth scopes and when to use them**

---

## Quick Reference

| Scope | Purpose | APIs Enabled | Example Use Case |
|-------|---------|--------------|------------------|
| `data:read` | Read files, folders, projects | Data Management GET operations | Download files, list projects |
| `data:write` | Modify files and metadata | Data Management PUT/PATCH operations | Update file metadata, rename files |
| `data:create` | Create new resources | Data Management POST operations | Upload files, create folders |
| `bucket:read` | List and access buckets | OSS read operations | List available storage buckets |
| `bucket:create` | Create new buckets | OSS bucket creation | Setup new storage containers |
| `bucket:delete` | Remove buckets | OSS bucket deletion | Clean up unused storage |
| `viewables:read` | Access translated models | Model Derivative, Viewer SDK | Display 3D models in browser |
| `code:all` | Design Automation access | All Design Automation operations | Automate CAD operations |
| `account:read` | BIM360/ACC account info | Account Admin API reads | List account details |
| `account:write` | Modify BIM360/ACC settings | Account Admin API writes | Manage account settings |

---

## Data Management Scopes

### Core Data Operations

#### `data:read`
**What it enables:**
- Download files from projects and folders
- List project contents and folder hierarchy  
- Read file metadata and version history
- Access item thumbnails and previews

**API Endpoints:**
```
GET /data/v1/projects/{project_id}
GET /data/v1/projects/{project_id}/folders/{folder_id}/contents
GET /data/v1/projects/{project_id}/items/{item_id}/versions
GET /data/v1/projects/{project_id}/downloads
```

**RAPS Usage:**
```bash
# Login with read-only access
raps auth login --scopes data:read

# List projects (requires data:read)
raps dm projects

# Download file (requires data:read)
raps dm download <item_id> ./local-file.dwg
```

#### `data:write`
**What it enables:**
- Update file metadata and custom attributes
- Modify folder properties
- Update version descriptions
- Change file relationships and references

**API Endpoints:**
```
PATCH /data/v1/projects/{project_id}/items/{item_id}
PATCH /data/v1/projects/{project_id}/folders/{folder_id}
PATCH /data/v1/projects/{project_id}/versions/{version_id}
```

**RAPS Usage:**
```bash
# Login with write permissions
raps auth login --scopes data:read,data:write

# Update file metadata
raps dm update-item <item_id> --name "Updated Model.rvt"
```

#### `data:create`
**What it enables:**
- Upload new files to projects
- Create new folders and project structure
- Create new versions of existing items
- Establish file relationships

**API Endpoints:**
```
POST /data/v1/projects/{project_id}/storage
POST /data/v1/projects/{project_id}/folders
POST /data/v1/projects/{project_id}/items
POST /data/v1/projects/{project_id}/versions
```

**RAPS Usage:**
```bash
# Login with full data permissions
raps auth login --scopes data:read,data:write,data:create

# Upload new file
raps dm upload model.rvt --project <project_id> --folder <folder_id>

# Create new folder
raps dm create-folder "CAD Models" --parent <folder_id>
```

---

## Object Storage Service (OSS) Scopes

### Bucket Management

#### `bucket:read`
**What it enables:**
- List available buckets
- Read bucket details and settings
- Access bucket contents (object listing)
- Download objects from buckets

**API Endpoints:**
```
GET /oss/v2/buckets
GET /oss/v2/buckets/{bucketKey}/details
GET /oss/v2/buckets/{bucketKey}/objects
GET /oss/v2/buckets/{bucketKey}/objects/{objectName}
```

**RAPS Usage:**
```bash
# Login with bucket read access
raps auth login --scopes bucket:read

# List all accessible buckets
raps bucket list

# List objects in bucket
raps oss list mybucket
```

#### `bucket:create`
**What it enables:**
- Create new storage buckets
- Set bucket policies and retention
- Configure bucket permissions

**API Endpoints:**
```
POST /oss/v2/buckets
```

**RAPS Usage:**
```bash
# Login with bucket creation rights
raps auth login --scopes bucket:read,bucket:create

# Create new bucket
raps bucket create my-new-bucket --region us-west
```

#### `bucket:delete`
**What it enables:**
- Delete empty buckets
- Remove bucket policies
- Clean up unused storage containers

**API Endpoints:**
```
DELETE /oss/v2/buckets/{bucketKey}
```

**RAPS Usage:**
```bash
# Login with full bucket permissions
raps auth login --scopes bucket:read,bucket:create,bucket:delete

# Delete unused bucket
raps bucket delete old-bucket --confirm
```

---

## Model Derivative & Viewer Scopes

#### `viewables:read`
**What it enables:**
- Access translated model derivatives (SVF/SVF2)
- Download viewable geometry and metadata
- Initialize Forge Viewer with models
- Extract model properties and metadata

**API Endpoints:**
```
GET /modelderivative/v2/designdata/{urn}/manifest
GET /modelderivative/v2/designdata/{urn}/metadata/{guid}
GET /modelderivative/v2/designdata/{urn}/metadata/{guid}/properties
```

**RAPS Usage:**
```bash
# Login for model viewing
raps auth login --scopes data:read,viewables:read

# Start translation for viewing
raps translate <urn> --formats svf2

# View model in browser
raps view <urn>
```

---

## Design Automation Scopes

#### `code:all`
**What it enables:**
- Create and manage Activities
- Upload and manage AppBundles
- Submit and monitor WorkItems
- Access all Design Automation engines (AutoCAD, Revit, Inventor, 3ds Max)

**API Endpoints:**
```
GET /da/us-east/v3/engines
POST /da/us-east/v3/appbundles
POST /da/us-east/v3/activities
POST /da/us-east/v3/workitems
```

**RAPS Usage:**
```bash
# Login for Design Automation
raps auth login --scopes code:all

# List available engines
raps da engines

# Create activity
raps da create-activity MyActivity --engine Autodesk.AutoCAD+24

# Submit workitem
raps da submit-workitem MyActivity --input input.dwg --output output.pdf
```

---

## Account & Construction Cloud Scopes

### BIM360/ACC Account Management

#### `account:read`
**What it enables:**
- List account information and users
- Read project settings and permissions
- Access account-level reporting data
- View company and project structure

**API Endpoints:**
```
GET /hq/v1/accounts
GET /hq/v1/accounts/{account_id}/projects
GET /hq/v1/accounts/{account_id}/users
```

**RAPS Usage:**
```bash
# Login for account reading
raps auth login --scopes account:read

# List accessible accounts
raps acc accounts

# List projects in account
raps acc projects --account <account_id>
```

#### `account:write`
**What it enables:**
- Modify account settings and permissions
- Create and configure projects
- Manage user access and roles
- Update company information

**API Endpoints:**
```
POST /hq/v1/accounts/{account_id}/projects
PATCH /hq/v1/accounts/{account_id}/projects/{project_id}
POST /hq/v1/accounts/{account_id}/users
```

**RAPS Usage:**
```bash
# Login for account management
raps auth login --scopes account:read,account:write

# Create new project
raps acc create-project "New Building Project" --account <account_id>

# Add user to project
raps acc add-user user@company.com --project <project_id> --role admin
```

---

## Common Scope Combinations

### Basic File Operations
```bash
# Read-only access to files and projects
raps auth login --scopes data:read

# Full file management (most common)
raps auth login --scopes data:read,data:write,data:create
```

### 3D Model Workflow
```bash
# Upload, translate, and view models
raps auth login --scopes data:read,data:write,data:create,viewables:read

# Include bucket access for direct storage
raps auth login --scopes data:read,data:write,data:create,bucket:read,bucket:create,viewables:read
```

### Design Automation
```bash
# Full Design Automation access
raps auth login --scopes code:all,data:read,data:write,data:create,bucket:read,bucket:create

# DA with BIM360 integration
raps auth login --scopes code:all,data:read,data:write,data:create,account:read
```

### BIM360/ACC Administration
```bash
# Read-only account access
raps auth login --scopes account:read,data:read

# Full account management
raps auth login --scopes account:read,account:write,data:read,data:write,data:create
```

### Maximum Permissions (Development/Testing)
```bash
# All available scopes (use carefully)
raps auth login --scopes data:read,data:write,data:create,bucket:read,bucket:create,bucket:delete,viewables:read,code:all,account:read,account:write
```

---

## Scope Troubleshooting

### Checking Current Scopes
```bash
# View current authentication details
raps auth status

# Show detailed scope information
raps auth status --scopes

# Test specific scope permissions
raps auth test-scope data:read
```

### Common Scope Issues

#### Error: "Insufficient privileges to access this resource"
**Cause:** Missing required scope for the operation
**Solution:**
```bash
# Check what scopes you have
raps auth status --scopes

# Re-authenticate with additional scopes
raps auth login --scopes data:read,data:write,data:create
```

#### Error: "Access denied to BIM360 project"
**Cause:** User not added to project or missing account scope
**Solution:**
```bash
# Login with account scope
raps auth login --scopes account:read,data:read

# Verify project access
raps acc projects
```

#### Error: "Cannot create bucket"
**Cause:** Missing `bucket:create` scope
**Solution:**
```bash
# Add bucket creation scope
raps auth login --scopes bucket:read,bucket:create

# Verify bucket permissions
raps auth test-scope bucket:create
```

---

## 2-Legged vs 3-Legged Authentication

### 2-Legged OAuth (Server-to-Server)
**When to use:** Background processing, server applications, automation
**Available scopes:** Limited subset, no user context
**RAPS command:**
```bash
raps auth login --2legged --scopes data:read,bucket:read,code:all
```

### 3-Legged OAuth (User Authorization)
**When to use:** User-facing applications, accessing user's BIM360/ACC projects
**Available scopes:** Full set, user context preserved
**RAPS command:**
```bash
raps auth login --3legged --scopes data:read,data:write,account:read
```

### Scope Differences

| Scope | 2-Legged | 3-Legged | Notes |
|-------|----------|----------|-------|
| `data:read` | ✅ Limited | ✅ Full | 2-legged can't access user's BIM360/ACC |
| `data:write` | ✅ Limited | ✅ Full | 2-legged can't modify user's projects |
| `bucket:*` | ✅ Full | ✅ Full | Both have same OSS access |
| `code:all` | ✅ Full | ✅ Full | Design Automation works with both |
| `account:*` | ❌ None | ✅ Full | Account management requires 3-legged |

---

## Best Practices

### 1. Principle of Least Privilege
Request only the scopes your application actually needs:
```bash
# Good: Only what's needed for file download
raps auth login --scopes data:read

# Avoid: Requesting unnecessary permissions
raps auth login --scopes data:read,data:write,data:create,bucket:delete,account:write
```

### 2. Scope Validation
Always verify your scopes match your intended operations:
```bash
# Test specific functionality
raps auth test-scope data:write
raps auth test-scope bucket:create
```

### 3. Environment-Specific Scopes
Use different scopes for different environments:
```bash
# Development: Full access for testing
raps auth login --profile dev --scopes data:read,data:write,data:create,viewables:read,code:all

# Production: Minimal required scopes
raps auth login --profile prod --scopes data:read,viewables:read
```

### 4. Regular Scope Auditing
Periodically review and update your scope requirements:
```bash
# Review current permissions
raps auth status --scopes --verbose

# Check actual API usage
raps logs --scope-usage --last 30d
```

---

## Advanced Scope Management

### Dynamic Scope Requests
For applications with varying requirements:
```bash
# Base authentication
raps auth login --scopes data:read,bucket:read

# Request additional scopes when needed
raps auth extend-scopes --add data:write,data:create

# Remove unnecessary scopes
raps auth reduce-scopes --remove bucket:delete
```

### Scope Monitoring
Track scope usage for optimization:
```bash
# Enable scope usage tracking
raps config set auth.track-scope-usage true

# Generate scope usage report
raps auth scope-report --period 30d
```

---

## Migration from Forge

### Legacy Forge Scopes
If migrating from Forge APIs, map old scopes to new ones:

| Forge Scope | APS Equivalent | Notes |
|-------------|----------------|-------|
| `data:read` | `data:read` | No change |
| `data:write` | `data:write` | No change |
| `data:create` | `data:create` | No change |
| `bucket:read` | `bucket:read` | No change |
| `bucket:create` | `bucket:create` | No change |
| `bucket:delete` | `bucket:delete` | No change |
| `viewables:read` | `viewables:read` | No change |
| `code:all` | `code:all` | No change |

**Migration command:**
```bash
# Most Forge scopes work unchanged in APS
raps auth migrate-from-forge --verify-scopes
```

---

## Getting Help

### Scope-Related Issues
1. **Check [APS Authentication Guide](https://aps.autodesk.com/en/docs/oauth/v2/overview/)**
2. **Test with [APS Postman Collection](https://github.com/Autodesk-Forge/forge-api-postman-collection)**
3. **Ask in [RAPS Discord](https://discord.gg/raps-community)**

### Debugging Commands
```bash
# Comprehensive auth diagnosis
raps auth diagnose

# Test specific scope combination
raps auth test-scopes --scopes data:read,bucket:create --endpoint /oss/v2/buckets

# Generate auth report for support
raps auth support-report --sanitize
```

---

**💡 Pro Tip:** Use `raps auth status` regularly to verify your current scopes match your intended operations. RAPS will warn you if you're attempting operations without proper permissions.

---

*Last verified: January 2026 against APS Authentication API v2 and RAPS v4.2.1*  
*OAuth scopes may evolve. Check the [official documentation](https://aps.autodesk.com/en/docs/oauth/v2/overview/scopes) for the latest information.*