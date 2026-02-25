---
title: "APS/Forge API Error Codes Reference"
description: "Complete guide to Autodesk Platform Services error codes with solutions"
category: "error-codes"
lastUpdated: 2026-01-08
completeness: "complete"
keywords: ["APS", "error codes", "troubleshooting", "403", "401", "Forge API"]
raps_commands: ["raps auth status", "raps auth inspect", "raps auth login"]
raps_version: ">=4.14.0"
aps_apis:
  authentication: "v2"
  data_management: "v1"
  model_derivative: "v2"
  design_automation: "v3"
  oss: "v2"
last_verified: "February 2026"
---

# APS/Forge API Error Codes Reference

**Quick lookup for Autodesk Platform Services (APS) and Forge API errors with practical solutions**

---

## Authentication Errors (401/403)

### 401 Unauthorized

| Context | Likely Cause | Manual Solution | RAPS Solution |
|---------|--------------|-----------------|---------------|
| **All APIs** | Token missing/invalid | Check Authorization header format | `raps auth status` to verify |
| **All APIs** | Token expired | Get new token via auth flow | Re-run `raps auth login` (auto-refresh handles most cases) |
| **All APIs** | Malformed token | Verify Bearer prefix and token format | `raps auth inspect` to check token details |

**Example Error:**
```json
{
  "developerMessage": "The request requires user authentication",
  "errorCode": "AUTH-001",
  "more info": "https://aps.autodesk.com/en/docs/oauth/v2/overview/"
}
```

**Quick Fix with RAPS:**
```bash
# Check current auth status
raps auth status

# Inspect token details and expiry
raps auth inspect

# Re-authenticate if needed
raps auth login
```

### 403 Forbidden

| Context | Likely Cause | Manual Solution | RAPS Solution |
|---------|--------------|-----------------|---------------|
| **Data Management** | Insufficient scopes | Add `data:read` or `data:write` to app | Re-login with `raps auth login --preset all` |
| **BIM360/ACC** | No project access | User must be added to project | Check with `raps hub list` and `raps project list` |
| **OSS** | Wrong bucket permissions | Check bucket policy and ownership | `raps bucket list` shows accessible buckets |
| **Model Derivative** | Source file access denied | Verify file permissions | `raps translate status <urn>` shows detailed errors |

**Example Error:**
```json
{
  "developerMessage": "Insufficient privileges to access this resource",
  "errorCode": "FORBIDDEN",
  "more info": "https://aps.autodesk.com/en/docs/data/v1/overview/scopes"
}
```

---

## Request Format Errors (400)

### 400 Bad Request

| API Context | Common Causes | Manual Diagnosis | RAPS Prevention |
|-------------|---------------|------------------|-----------------|
| **All APIs** | Invalid JSON syntax | Validate JSON with linter | RAPS validates all payloads |
| **Model Derivative** | URN not base64-encoded | Use base64url encoding | Encode manually: `echo -n "urn:..." \| base64 \| tr '+/' '-_' \| tr -d '='` |
| **Model Derivative** | Invalid output format | Check supported format list | `raps translate start --help` shows options |
| **Data Management** | Invalid folder/item hierarchy | Verify parent relationships | `raps folder list` shows structure |
| **OSS** | Invalid bucket name | Check naming conventions | `raps bucket create` validates interactively |

**URN Encoding:**
```bash
# Base64 URL-safe encode a URN
echo -n "urn:adsk.objects:os.object:bucket/file.dwg" | base64 | tr '+/' '-_' | tr -d '='
```

---

## Resource Not Found (404)

### 404 Not Found

| API Context | Likely Cause | Investigation Steps | RAPS Debugging |
|-------------|--------------|-------------------|----------------|
| **Model Derivative** | URN doesn't exist or wrong encoding | Check OSS bucket contents first | `raps object list <bucket>` to verify file exists |
| **Data Management** | Project/folder/item deleted | Verify in web interface | `raps project list` and `raps folder list` |
| **OSS** | Bucket or object deleted | List bucket contents | `raps bucket list` and `raps object list <bucket>` |
| **Design Automation** | Activity/AppBundle not found | Check DA console | `raps da engines` to verify setup |

**Debugging Workflow:**
```bash
# 1. Check if file exists in OSS
raps object list mybucket

# 2. Encode URN manually
echo -n "urn:adsk.objects:os.object:mybucket:model.rvt" | base64 | tr '+/' '-_' | tr -d '='

# 3. Check translation status
raps translate status <encoded_urn>
```

---

## Conflict Errors (409)

### 409 Conflict

| API Context | Specific Issue | Manual Resolution | RAPS Resolution |
|-------------|----------------|-------------------|-----------------|
| **OSS** | Bucket already exists | Choose different name or use existing | `raps bucket list` first, then create |
| **Design Automation** | Activity/AppBundle name conflict | Use versioning or different name | Use `raps da activity-create` with new ID |

---

## Rate Limiting (429)

### 429 Too Many Requests

| API | Standard Limits | Backoff Strategy | RAPS Handling |
|-----|-----------------|------------------|---------------|
| **Authentication** | 500/min | Exponential backoff (2^n seconds) | Built-in rate limiting |
| **Data Management** | 100/min | Linear backoff (1s increments) | Automatic queuing |
| **Model Derivative** | 20 concurrent translations | Queue locally | Submit sequentially with `--wait` |
| **OSS** | 500/min | Exponential backoff | Smart batching |
| **Design Automation** | 50 concurrent WorkItems | Queue and monitor | Automatic WorkItem management |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

RAPS handles rate limiting automatically with built-in exponential backoff and retry logic.

---

## Server Errors (500/503)

### 500 Internal Server Error

| When It Happens | Likely Cause | Action Required | RAPS Response |
|-----------------|--------------|-----------------|---------------|
| **Translation jobs** | Service overload or file corruption | Retry after delay | Automatic retry with exponential backoff |
| **File uploads** | Network interruption or service issue | Retry with same URN | `raps object upload <bucket> <file> --resume` |
| **Any API** | Autodesk infrastructure issue | Check [status.autodesk.com](https://status.autodesk.com) | Built-in retry logic |

### 503 Service Unavailable

Usually indicates planned maintenance or unplanned service disruption.

**RAPS Resilience:**
RAPS includes built-in retry logic with exponential backoff for transient errors (429, 500, 503).

---

## Model Derivative Specific Errors

### Translation Failed

**Common Manifest Error Messages:**

| Error Message | Cause | Solution |
|---------------|-------|----------|
| "Unsupported file format" | File extension not recognized | Check [supported formats](https://aps.autodesk.com/en/docs/model-derivative/v2/developers_guide/supported-translations/) |
| "File is empty or corrupted" | Upload corrupted or incomplete | Re-upload source file |
| "Missing dependencies" | Assembly references missing | Upload all dependency files |
| "Invalid password" | Encrypted file, wrong password | Provide correct password in translate request |
| "File too large" | Exceeds size limits | Split file or use Design Automation |

**Translation Debugging:**
```bash
# Check translation status
raps translate status <urn>

# Get full manifest with error details
raps translate manifest <urn>

# Re-translate with force flag
raps translate start <urn> --format svf2 --force --wait
```

---

## Design Automation Specific Errors

### WorkItem Failures

| Status | Description | Common Cause |
|--------|-------------|--------------|
| **failedLimitDataSize** | Output too large | Reduce output or increase limits |
| **failedLimitProcessingTime** | Timeout exceeded | Optimize script or increase timeout |
| **failedDownload** | Input download failed | Check input URLs and permissions |
| **failedInstructions** | Script execution failed | Debug script locally first |

**Design Automation Debugging:**
```bash
# List available engines
raps da engines

# Re-create and re-run
raps da appbundle-create --id MyPlugin --engine Autodesk.AutoCAD+24
raps da run --activity MyPlugin.MyActivity+prod --file workitem.json
```

---

## BIM360/ACC Specific Errors

### Project Access Issues

| Error Code | Context | Meaning | RAPS Check |
|------------|---------|---------|------------|
| **FORBIDDEN** | Project access | User not in project or app not provisioned | `raps hub list` then `raps project list` |
| **NOT_FOUND** | Project ID | Invalid or deleted project | `raps project list` |
| **INVALID_SCOPE** | API permissions | Wrong scope for operation | `raps auth status` then re-login with `--preset all` |

---

## OAuth/Authentication Deep Dive

### Scope Issues

| Required Action | Minimum Scopes | RAPS Command |
|----------------|----------------|--------------|
| Read files | `data:read` | `raps auth login --default` |
| Upload files | `data:read data:write data:create` | `raps auth login --default` |
| Translate models | `data:read viewables:read` | `raps auth login --default` |
| Design Automation | `code:all` | `raps auth login --preset all` |
| BIM360/ACC admin | `account:read account:write` | `raps auth login --preset all` |

> Scopes are selected interactively during `raps auth login`, or use `--default` for common scopes or `--preset all` for all scopes.

### Token Troubleshooting

```bash
# View current token info
raps auth status

# Check token details, expiry, and scopes
raps auth inspect

# Check token health with expiry warning (for CI)
raps auth inspect --warn-expiry-seconds 300

# Show authenticated user info
raps auth whoami
```

---

## Quick Diagnostic Commands

### Common Debug Workflow
```bash
# 1. Verify authentication
raps auth status

# 2. Check token details
raps auth inspect

# 3. Test basic connectivity
raps bucket list

# 4. Check specific resource
raps translate status <urn>
```

---

## Error Prevention Best Practices

### 1. Authenticate Properly
```bash
# Use default scopes for most operations
raps auth login --default

# Or use all scopes for full access
raps auth login --preset all

# For CI/CD, inject token directly
raps auth login --token $APS_ACCESS_TOKEN
```

### 2. Verify Before Operations
```bash
# Check auth before making API calls
raps auth inspect --warn-expiry-seconds 300

# List buckets before creating duplicates
raps bucket list

# Check translation status before re-translating
raps translate status <urn>
```

---

## Getting Help

### When Errors Persist
1. **Check [Autodesk Status Page](https://status.autodesk.com)**
2. **Search [APS Community Forums](https://forums.autodesk.com/t5/platform-services/bd-p/42)**
3. **Review [Official APS Documentation](https://aps.autodesk.com/en/docs/)**

---

*Last verified: February 2026 against APS API v2 and RAPS v4.14.0*
*APIs evolve. If something doesn't work, [open an issue](https://github.com/dmytro-yemelianov/raps/issues).*
