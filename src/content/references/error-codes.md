---
title: "APS/Forge API Error Codes Reference"
description: "Complete guide to Autodesk Platform Services error codes with solutions"
category: "error-codes"
lastUpdated: 2026-01-08
completeness: "complete"
keywords: ["APS", "error codes", "troubleshooting", "403", "401", "Forge API"]
raps_commands: ["raps auth status", "raps urn encode", "raps auth refresh"]
raps_version: ">=4.11.0"
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
| **All APIs** | Token expired | Get new token via auth flow | `raps auth refresh` |
| **All APIs** | Malformed token | Verify Bearer prefix and token format | `raps auth login` validates automatically |

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

# Refresh if expired
raps auth refresh

# Re-authenticate if needed
raps auth login
```

### 403 Forbidden

| Context | Likely Cause | Manual Solution | RAPS Solution |
|---------|--------------|-----------------|---------------|
| **Data Management** | Insufficient scopes | Add `data:read` or `data:write` to app | `raps auth status` shows current scopes |
| **BIM360/ACC** | No project access | User must be added to project | `raps acc projects` lists accessible projects |
| **OSS** | Wrong bucket permissions | Check bucket policy and ownership | `raps bucket list` shows accessible buckets |
| **Model Derivative** | Source file access denied | Verify file permissions in Data Management | `raps translate status <urn>` shows detailed errors |

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
| **Model Derivative** | URN not base64-encoded | Use base64url encoding | `raps urn encode <input>` |
| **Model Derivative** | Invalid output format | Check supported format list | `raps translate --formats` shows options |
| **Data Management** | Invalid folder/item hierarchy | Verify parent relationships | `raps dm folders <project>` shows structure |
| **OSS** | Invalid bucket name | Check naming conventions | `raps bucket create` validates names |

**URN Encoding Example:**
```bash
# Manual (error-prone):
echo -n "urn:adsk.objects:os.object:bucket/file.dwg" | base64 | tr '+/' '-_'

# With RAPS:
raps urn encode "urn:adsk.objects:os.object:bucket/file.dwg"
```

---

## Resource Not Found (404)

### 404 Not Found

| API Context | Likely Cause | Investigation Steps | RAPS Debugging |
|-------------|--------------|-------------------|----------------|
| **Model Derivative** | URN doesn't exist or wrong encoding | Check OSS bucket contents first | `raps oss list <bucket>` then `raps urn encode` |
| **Data Management** | Project/folder/item deleted | Verify in web interface | `raps dm projects` and `raps dm folders` |
| **OSS** | Bucket or object deleted | List bucket contents | `raps bucket list` and `raps oss list <bucket>` |
| **Design Automation** | Activity/AppBundle not found | Check DA console | `raps da activities` and `raps da appbundles` |

**Debugging Workflow:**
```bash
# 1. Check if file exists in OSS
raps oss list mybucket

# 2. Verify URN encoding
raps urn encode "urn:adsk.objects:os.object:mybucket/model.rvt"

# 3. Check translation status
raps translate status <encoded_urn>
```

---

## Conflict Errors (409)

### 409 Conflict

| API Context | Specific Issue | Manual Resolution | RAPS Resolution |
|-------------|----------------|-------------------|-----------------|
| **OSS** | Bucket already exists | Choose different name or use existing | `raps bucket list` first, then create |
| **Data Management** | Version/item conflict | Check existing versions | `raps dm versions <item-id>` |
| **Design Automation** | Activity/AppBundle name conflict | Use versioning or different name | `raps da create --increment-version` |

---

## Rate Limiting (429)

### 429 Too Many Requests

| API | Standard Limits | Backoff Strategy | RAPS Handling |
|-----|-----------------|------------------|---------------|
| **Authentication** | 500/min | Exponential backoff (2^n seconds) | Built-in rate limiting |
| **Data Management** | 100/min | Linear backoff (1s increments) | Automatic queuing |
| **Model Derivative** | 20 concurrent translations | Queue locally | `raps translate --parallel <n>` |
| **OSS** | 500/min | Exponential backoff | Smart batching |
| **Design Automation** | 50 concurrent WorkItems | Queue and monitor | Automatic WorkItem management |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

**RAPS Rate Limit Management:**
```bash
# Configure rate limits
raps config set rate-limit.enabled true
raps config set rate-limit.requests-per-minute 80

# Check current rate limit status
raps auth status --rate-limits
```

---

## Server Errors (500/503)

### 500 Internal Server Error

| When It Happens | Likely Cause | Action Required | RAPS Response |
|-----------------|--------------|-----------------|---------------|
| **Translation jobs** | Service overload or file corruption | Retry after delay | Automatic retry with exponential backoff |
| **File uploads** | Network interruption or service issue | Retry with same URN | Resumable upload support |
| **Any API** | Autodesk infrastructure issue | Check [status.autodesk.com](https://status.autodesk.com) | Configurable retry policies |

### 503 Service Unavailable

Usually indicates planned maintenance or unplanned service disruption.

**RAPS Resilience:**
```bash
# Configure robust retry policy
raps config set retry.max-attempts 5
raps config set retry.strategy exponential
raps config set retry.max-delay 300s

# Monitor service health
raps health check --aps-services
```

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
# Check translation status with details
raps translate status <urn> --verbose

# Get full manifest with error details
raps translate manifest <urn> --errors-only

# Retry translation with different options
raps translate <urn> --formats svf2 --retry
```

---

## Design Automation Specific Errors

### WorkItem Failures

| Status | Description | Common Cause | RAPS Investigation |
|--------|-------------|--------------|-------------------|
| **failedLimitDataSize** | Output too large | Reduce output or increase limits | `raps da workitem logs <id>` |
| **failedLimitProcessingTime** | Timeout exceeded | Optimize script or increase timeout | `raps da workitem details <id>` |
| **failedDownload** | Input download failed | Check input URLs and permissions | `raps da workitem retry <id>` |
| **failedInstructions** | Script execution failed | Debug script locally first | `raps da workitem logs <id> --detailed` |

**Design Automation Debugging:**
```bash
# Get detailed WorkItem logs
raps da workitem logs <workitem-id> --download

# Retry failed WorkItem
raps da workitem retry <workitem-id>

# Test Activity locally (if supported)
raps da activity test <activity-id>
```

---

## BIM360/ACC Specific Errors

### Project Access Issues

| Error Code | Context | Meaning | RAPS Check |
|------------|---------|---------|------------|
| **FORBIDDEN** | Project access | User not in project | `raps acc projects` |
| **NOT_FOUND** | Project ID | Invalid or deleted project | `raps acc hubs` then `raps acc projects <hub-id>` |
| **INVALID_SCOPE** | API permissions | Wrong scope for operation | `raps auth status --scopes` |

---

## OAuth/Authentication Deep Dive

### Scope Issues

| Required Action | Minimum Scopes | RAPS Command |
|----------------|----------------|--------------|
| Read files | `data:read` | `raps auth login --scopes data:read` |
| Upload files | `data:read data:write data:create` | `raps auth login --scopes data:read,data:write,data:create` |
| Translate models | `data:read data:write viewables:read` | `raps auth login --scopes data:read,data:write,viewables:read` |
| Design Automation | `code:all` | `raps auth login --scopes code:all` |
| BIM360/ACC admin | `account:read account:write` | `raps auth login --scopes account:read,account:write` |

### Token Troubleshooting

**Check Token Details:**
```bash
# View current token info
raps auth status --token-details

# Decode JWT token manually (if needed)
raps auth decode-token <jwt-token>

# Test token with specific endpoint
raps auth test-token --endpoint "/oss/v2/buckets"
```

---

## Network and Infrastructure Issues

### Timeout Errors

| Operation | Default Timeout | RAPS Configuration |
|-----------|----------------|-------------------|
| **File Upload** | 300s | `raps config set timeout.upload 600` |
| **Translation** | 3600s | `raps config set timeout.translation 7200` |
| **API Calls** | 30s | `raps config set timeout.api 60` |

### Regional Issues

Some APS services are region-specific:

| Service | US Region | EMEA Region | RAPS Setting |
|---------|-----------|-------------|--------------|
| **OSS** | us-west | emea-west | `raps config set region us-west` |
| **Data Management** | Global | Global | No setting needed |
| **Model Derivative** | Region-aware | Region-aware | Follows OSS setting |

---

## Quick Diagnostic Commands

### RAPS Health Check
```bash
# Full system diagnostic
raps health check --comprehensive

# Test APS connectivity
raps health check --aps-endpoints

# Verify authentication
raps health check --auth

# Check configuration
raps health check --config
```

### Common Debug Workflow
```bash
# 1. Verify authentication
raps auth status

# 2. Test basic connectivity
raps oss buckets --limit 1

# 3. Check specific resource
raps translate status <urn> --verbose

# 4. Review logs if available
raps logs --level error --last 24h
```

---

## Error Prevention Best Practices

### 1. Always Validate Inputs
```bash
# RAPS validates automatically, but for manual calls:
raps validate urn <urn>
raps validate bucket-name <name>
raps validate file-format <extension>
```

### 2. Implement Retry Logic
```bash
# Configure intelligent retries
raps config set retry.enabled true
raps config set retry.max-attempts 3
raps config set retry.strategy exponential
```

### 3. Monitor Rate Limits
```bash
# Enable rate limit monitoring
raps config set rate-limit.monitor true
raps config set rate-limit.alert-threshold 80
```

### 4. Use Health Checks
```bash
# Regular health monitoring
raps health monitor --interval 60s --alerts-webhook https://your-alerts.com
```

---

## Getting Help

### When Errors Persist
1. **Check [Autodesk Status Page](https://status.autodesk.com)**
2. **Search [APS Community Forums](https://forums.autodesk.com/t5/platform-services/bd-p/42)**
3. **Review [Official APS Documentation](https://aps.autodesk.com/en/docs/)**
4. **Ask in [RAPS Community Discord](https://discord.gg/raps-community)**

### Reporting Issues
```bash
# Generate diagnostic report
raps debug report --include-logs --sanitize-tokens

# Submit issue with context
raps support create-ticket --attach-diagnostics
```

---

**💡 Pro Tip:** Most APS errors can be avoided by using RAPS CLI, which includes built-in validation, retry logic, and error recovery mechanisms.

---

*Last verified: February 2026 against APS API v2 and RAPS v4.11.0*  
*APIs evolve. If something doesn't work, [open an issue](https://github.com/dmytro-yemelianov/raps-marketing/issues).*