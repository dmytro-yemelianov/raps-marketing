---
title: "APS OAuth Scopes Reference"
description: "Complete guide to Autodesk Platform Services OAuth scopes and permissions"
category: "scopes"
lastUpdated: 2026-01-08
completeness: "complete"
keywords: ["APS", "OAuth", "scopes", "permissions", "authentication", "Forge API"]
raps_commands: ["raps auth login", "raps auth status", "raps auth inspect"]
raps_version: ">=4.14.0"
aps_apis:
  authentication: "v2"
last_verified: "February 2026"
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

## How Scopes Work with RAPS

RAPS handles scope selection in several ways:

```bash
# Interactive scope selection (default - opens checklist)
raps auth login

# Use common scopes without prompting
raps auth login --default

# Use all available scopes
raps auth login --preset all

# For CI/CD: inject a pre-obtained token
raps auth login --token $APS_ACCESS_TOKEN
```

---

## Data Management Scopes

### `data:read`
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
```

**RAPS Usage:**
```bash
raps hub list
raps project list
raps folder list
raps item list
```

### `data:write`
**What it enables:**
- Update file metadata and custom attributes
- Modify folder properties
- Update version descriptions
- Change file relationships and references

**API Endpoints:**
```
PATCH /data/v1/projects/{project_id}/items/{item_id}
PATCH /data/v1/projects/{project_id}/folders/{folder_id}
```

### `data:create`
**What it enables:**
- Upload new files to projects
- Create new folders and project structure
- Create new versions of existing items

**API Endpoints:**
```
POST /data/v1/projects/{project_id}/storage
POST /data/v1/projects/{project_id}/folders
POST /data/v1/projects/{project_id}/items
POST /data/v1/projects/{project_id}/versions
```

**RAPS Usage:**
```bash
raps folder create
raps object upload <bucket> <file>
```

---

## Object Storage Service (OSS) Scopes

### `bucket:read`
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
raps bucket list
raps bucket info <bucket>
raps object list <bucket>
raps object download <bucket> <object>
```

### `bucket:create`
**What it enables:**
- Create new storage buckets
- Set bucket policies and retention

**API Endpoints:**
```
POST /oss/v2/buckets
```

**RAPS Usage:**
```bash
raps bucket create --key my-bucket --policy transient --region US
```

### `bucket:delete`
**What it enables:**
- Delete empty buckets
- Clean up unused storage containers

**API Endpoints:**
```
DELETE /oss/v2/buckets/{bucketKey}
```

**RAPS Usage:**
```bash
raps bucket delete <bucket> --yes
```

---

## Model Derivative & Viewer Scopes

### `viewables:read`
**What it enables:**
- Access translated model derivatives (SVF/SVF2)
- Download viewable geometry and metadata
- Initialize Viewer with models
- Extract model properties and metadata

**API Endpoints:**
```
GET /modelderivative/v2/designdata/{urn}/manifest
GET /modelderivative/v2/designdata/{urn}/metadata/{guid}
GET /modelderivative/v2/designdata/{urn}/metadata/{guid}/properties
```

**RAPS Usage:**
```bash
raps translate start <urn> --format svf2 --wait
raps translate status <urn>
raps translate metadata <urn>
raps translate properties <urn> <guid>
raps translate download <urn>
```

---

## Design Automation Scopes

### `code:all`
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
raps da engines
raps da appbundle-create --id MyPlugin --engine Autodesk.AutoCAD+24
raps da activity-create --file activity.json
raps da run --activity MyPlugin.MyActivity+prod --file workitem.json
```

---

## Account & Construction Cloud Scopes

### `account:read`
**What it enables:**
- List account information and users
- Read project settings and permissions
- Access account-level reporting data

**API Endpoints:**
```
GET /hq/v1/accounts
GET /hq/v1/accounts/{account_id}/projects
GET /hq/v1/accounts/{account_id}/users
```

**RAPS Usage:**
```bash
raps hub list
raps project list
raps acc asset list --project-id <id>
raps acc checklist list --project-id <id>
```

### `account:write`
**What it enables:**
- Modify account settings and permissions
- Create and configure projects
- Manage user access and roles

**API Endpoints:**
```
POST /hq/v1/accounts/{account_id}/projects
PATCH /hq/v1/accounts/{account_id}/projects/{project_id}
POST /hq/v1/accounts/{account_id}/users
```

**RAPS Usage:**
```bash
raps admin user list --account-id <id>
raps admin project list --account-id <id>
```

---

## Common Scope Combinations

### Basic File Operations
```bash
# Read-only access to files and projects
raps auth login --default
# Selects: data:read, bucket:read, viewables:read

# Full access for all operations
raps auth login --preset all
```

### Typical Workflows

| Workflow | Required Scopes |
|----------|----------------|
| **List projects and files** | `data:read` |
| **Upload files to OSS** | `data:read`, `data:create`, `bucket:read`, `bucket:create` |
| **Translate models** | `data:read`, `viewables:read` |
| **Design Automation** | `code:all`, `data:read`, `data:create`, `bucket:read`, `bucket:create` |
| **BIM360/ACC access** | `data:read`, `account:read` |
| **Full file management** | `data:read`, `data:write`, `data:create` |

---

## Scope Troubleshooting

### Checking Current Authentication
```bash
# View current authentication status
raps auth status

# Inspect token details including scopes and expiry
raps auth inspect

# Check expiry with warning threshold (useful in CI)
raps auth inspect --warn-expiry-seconds 300

# See authenticated user profile
raps auth whoami
```

### Common Scope Issues

#### Error: "Insufficient privileges to access this resource"
**Cause:** Missing required scope for the operation
**Solution:**
```bash
# Check current auth status
raps auth status

# Re-authenticate with all scopes
raps auth login --preset all
```

#### Error: "Access denied to BIM360 project"
**Cause:** User not added to project or app not provisioned
**Solution:**
```bash
# Verify accessible hubs and projects
raps hub list
raps project list

# Ensure app is provisioned in ACC admin console
# (see ACC Provisioning Checklist guide)
```

#### Error: "Cannot create bucket"
**Cause:** Missing `bucket:create` scope
**Solution:**
```bash
# Re-login with all scopes
raps auth login --preset all

# Then create bucket
raps bucket create --key my-bucket --policy transient --region US
```

---

## 2-Legged vs 3-Legged Authentication

### 2-Legged OAuth (Server-to-Server)
**When to use:** Background processing, server applications, automation
**Available scopes:** Limited subset, no user context
**RAPS command:**
```bash
raps auth test
```

### 3-Legged OAuth (User Authorization)
**When to use:** User-facing applications, accessing user's BIM360/ACC projects
**Available scopes:** Full set, user context preserved
**RAPS command:**
```bash
raps auth login
# Use --device flag for headless/CI environments
raps auth login --device
```

### Scope Differences

| Scope | 2-Legged | 3-Legged | Notes |
|-------|----------|----------|-------|
| `data:read` | Limited | Full | 2-legged can't access user's BIM360/ACC |
| `data:write` | Limited | Full | 2-legged can't modify user's projects |
| `bucket:*` | Full | Full | Both have same OSS access |
| `code:all` | Full | Full | Design Automation works with both |
| `account:*` | None | Full | Account management requires 3-legged |

---

## Best Practices

### 1. Principle of Least Privilege
Request only the scopes your application actually needs. During `raps auth login`, select only the scopes required for your workflow.

### 2. Use Profiles for Different Environments
```bash
# Create separate profiles for dev/prod
raps config profile create development
raps config set client_id DEV_CLIENT_ID
raps config set client_secret DEV_SECRET

raps config profile create production
raps config set client_id PROD_CLIENT_ID
raps config set client_secret PROD_SECRET

# Switch between them
raps config profile use development
raps auth login --default
```

### 3. Token Management for CI/CD
```bash
# Inject pre-obtained token for CI environments
raps auth login --token $APS_ACCESS_TOKEN

# Or use device flow for headless servers
raps auth login --device
```

---

## Migration from Forge

OAuth scopes are identical between Forge and APS. No scope changes needed.

| Forge Scope | APS Equivalent | Notes |
|-------------|----------------|-------|
| `data:read` | `data:read` | No change |
| `data:write` | `data:write` | No change |
| `data:create` | `data:create` | No change |
| `bucket:*` | `bucket:*` | No change |
| `code:all` | `code:all` | No change |
| `viewables:read` | `viewables:read` | No change |
| `account:*` | `account:*` | No change |

The main migration change is authentication endpoint: `/authentication/v1/` to `/authentication/v2/`. RAPS uses v2 by default.

---

## Getting Help

### Scope-Related Issues
1. **Check [APS Authentication Guide](https://aps.autodesk.com/en/docs/oauth/v2/overview/)**
2. **Test with [APS Postman Collection](https://github.com/Autodesk-Forge/forge-api-postman-collection)**

### RAPS Auth Commands
```bash
raps auth --help       # See all auth subcommands
raps auth status       # Check current auth state
raps auth inspect      # Detailed token info
raps auth whoami       # Authenticated user profile
raps auth login --help # Login options
```

---

*Last verified: February 2026 against APS Authentication API v2 and RAPS v4.14.0*
*OAuth scopes may evolve. Check the [official documentation](https://aps.autodesk.com/en/docs/oauth/v2/overview/scopes) for the latest information.*
