---
title: "APS API Error Codes Reference"
subtitle: "Complete troubleshooting guide for Autodesk Platform Services"
version: "RAPS v4.2.1 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3"
date: "January 2026"
layout: "a4-reference"
columns: 2
font-size: 8pt
---

# APS API Error Codes Reference
**Complete troubleshooting guide for Autodesk Platform Services with RAPS solutions**

---

## 🔐 Authentication Errors (401/403)

### 401 Unauthorized

| **Context** | **Cause** | **RAPS Solution** |
|-------------|-----------|-------------------|
| **All APIs** | Token missing/invalid | `raps auth status` |
| **All APIs** | Token expired | `raps auth refresh` |
| **All APIs** | Malformed token | `raps auth login` |

**Example Error:**
```json
{
  "developerMessage": "The request requires user authentication",
  "errorCode": "AUTH-001"
}
```

**Quick Fix:**
```bash
raps auth status    # Check current status
raps auth refresh   # Refresh if expired  
raps auth login     # Re-authenticate if needed
```

### 403 Forbidden

| **Context** | **Cause** | **RAPS Solution** |
|-------------|-----------|-------------------|
| **Data Mgmt** | Insufficient scopes | `raps auth status --scopes` |
| **BIM360/ACC** | No project access | `raps acc projects` |
| **OSS** | Wrong bucket permissions | `raps bucket list` |
| **Model Deriv** | Source access denied | `raps translate status <urn>` |

---

## 📝 Request Format Errors (400)

### 400 Bad Request

| **API Context** | **Common Causes** | **RAPS Prevention** |
|-----------------|-------------------|---------------------|
| **All APIs** | Invalid JSON syntax | Built-in validation |
| **Model Deriv** | URN not base64-encoded | `raps urn encode <input>` |
| **Model Deriv** | Invalid output format | `raps translate --formats` |
| **Data Mgmt** | Invalid hierarchy | `raps dm folders <project>` |
| **OSS** | Invalid bucket name | `raps bucket create` validates |

**URN Encoding Fix:**
```bash
# Manual (error-prone):
echo -n "urn:..." | base64 | tr '+/' '-_'

# With RAPS:
raps urn encode "urn:adsk.objects:os.object:bucket/file.dwg"
```

---

## 🔍 Resource Not Found (404)

### 404 Not Found

| **API Context** | **Likely Cause** | **RAPS Debugging** |
|-----------------|------------------|--------------------|
| **Model Deriv** | URN doesn't exist | `raps oss list <bucket>` |
| **Data Mgmt** | Project/folder deleted | `raps dm projects` |
| **OSS** | Bucket/object deleted | `raps bucket list` |
| **Design Auto** | Activity not found | `raps da activities` |

**Debugging Workflow:**
```bash
# 1. Check file exists
raps oss list mybucket

# 2. Verify URN encoding  
raps urn encode "urn:adsk.objects:os.object:mybucket/model.rvt"

# 3. Check translation
raps translate status <encoded_urn>
```

---

## ⚔️ Conflict Errors (409)

### 409 Conflict

| **API Context** | **Issue** | **RAPS Resolution** |
|-----------------|-----------|---------------------|
| **OSS** | Bucket exists | `raps bucket list` first |
| **Data Mgmt** | Version conflict | `raps dm versions <item-id>` |
| **Design Auto** | Name conflict | `raps da create --increment-version` |

---

## 🚦 Rate Limiting (429)

### 429 Too Many Requests

| **API** | **Limit** | **RAPS Handling** |
|---------|-----------|-------------------|
| **Authentication** | 500/min | Built-in rate limiting |
| **Data Management** | 100/min | Automatic queuing |
| **Model Derivative** | 20 concurrent | Queue locally |
| **OSS** | 500/min | Smart batching |
| **Design Automation** | 50 concurrent | WorkItem management |

**Rate Limit Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1640995200
```

**RAPS Configuration:**
```bash
raps config set rate-limit.enabled true
raps config set rate-limit.requests-per-minute 80
raps auth status --rate-limits
```

---

## 🔥 Server Errors (500/503)

### 500 Internal Server Error

| **When** | **Cause** | **RAPS Response** |
|----------|-----------|-------------------|
| **Translation** | Service overload | Automatic retry with backoff |
| **File uploads** | Network interruption | Resumable upload support |
| **Any API** | Infrastructure issue | Configurable retry policies |

### 503 Service Unavailable

Usually indicates maintenance or service disruption.

**RAPS Resilience:**
```bash
# Configure robust retry
raps config set retry.max-attempts 5
raps config set retry.strategy exponential
raps config set retry.max-delay 300s

# Monitor health
raps health check --aps-services
```

---

## 🔄 Model Derivative Specific

### Translation Failed

| **Error Message** | **Cause** | **Solution** |
|-------------------|-----------|-------------|
| "Unsupported format" | Extension not recognized | Check supported formats |
| "File corrupted" | Upload incomplete | Re-upload source |
| "Missing dependencies" | Assembly refs missing | Upload all files |
| "Invalid password" | Wrong password | Provide correct password |
| "File too large" | Exceeds limits | Use Design Automation |

**Translation Debugging:**
```bash
# Detailed status check
raps translate status <urn> --verbose

# Get error manifest
raps translate manifest <urn> --errors-only

# Retry with options
raps translate <urn> --formats svf2 --retry
```

---

## 🤖 Design Automation Specific

### WorkItem Failures

| **Status** | **Cause** | **RAPS Investigation** |
|------------|-----------|------------------------|
| `failedLimitDataSize` | Output too large | `raps da workitem logs <id>` |
| `failedLimitProcessingTime` | Timeout | `raps da workitem details <id>` |
| `failedDownload` | Input download failed | `raps da workitem retry <id>` |
| `failedInstructions` | Script execution failed | `raps da workitem logs <id> --detailed` |

---

## 🏢 BIM360/ACC Specific

### Project Access Issues

| **Error Code** | **Meaning** | **RAPS Check** |
|----------------|-------------|----------------|
| `FORBIDDEN` | User not in project | `raps acc projects` |
| `NOT_FOUND` | Invalid project ID | `raps acc hubs` |
| `INVALID_SCOPE` | Wrong permissions | `raps auth status --scopes` |

---

## 🔑 OAuth/Authentication Deep Dive

### Scope Issues

| **Action** | **Minimum Scopes** | **RAPS Command** |
|------------|-------------------|------------------|
| Read files | `data:read` | `raps auth login --scopes data:read` |
| Upload files | `data:read data:write data:create` | `raps auth login --scopes data:read,data:write,data:create` |
| Translate | `data:read viewables:read` | `raps auth login --scopes data:read,viewables:read` |
| Design Auto | `code:all` | `raps auth login --scopes code:all` |
| BIM360 admin | `account:read account:write` | `raps auth login --scopes account:read,account:write` |

### Token Troubleshooting

```bash
# View current token
raps auth status --token-details

# Decode JWT manually
raps auth decode-token <jwt-token>

# Test specific endpoint
raps auth test-token --endpoint "/oss/v2/buckets"
```

---

## 🌐 Network Issues

### Timeout Errors

| **Operation** | **Default** | **RAPS Config** |
|---------------|-------------|-----------------|
| File Upload | 300s | `raps config set timeout.upload 600` |
| Translation | 3600s | `raps config set timeout.translation 7200` |
| API Calls | 30s | `raps config set timeout.api 60` |

### Regional Issues

| **Service** | **US Region** | **EMEA Region** |
|-------------|---------------|-----------------|
| OSS | us-west | emea-west |
| Data Mgmt | Global | Global |
| Model Deriv | Region-aware | Region-aware |

---

## 🔧 Quick Diagnostics

### Health Check Commands

```bash
# Full system diagnostic
raps health check --comprehensive

# APS connectivity test
raps health check --aps-endpoints

# Authentication verification
raps health check --auth

# Configuration check
raps health check --config
```

### Debug Workflow

```bash
# 1. Verify auth
raps auth status

# 2. Test connectivity  
raps oss buckets --limit 1

# 3. Check specific resource
raps translate status <urn> --verbose

# 4. Review logs
raps logs --level error --last 24h
```

---

## ✅ Error Prevention

### Best Practices

```bash
# Validate inputs
raps validate urn <urn>
raps validate bucket-name <name>

# Configure retries
raps config set retry.enabled true
raps config set retry.max-attempts 3

# Monitor rate limits
raps config set rate-limit.monitor true

# Health monitoring
raps health monitor --interval 60s
```

---

## 📞 Getting Help

### Support Resources

1. **Autodesk Status:** [status.autodesk.com](https://status.autodesk.com)
2. **APS Forums:** [forums.autodesk.com](https://forums.autodesk.com/t5/platform-services/bd-p/42)  
3. **APS Docs:** [aps.autodesk.com](https://aps.autodesk.com/en/docs/)
4. **RAPS Discord:** [discord.gg/raps-community](https://discord.gg/raps-community)

### Report Issues

```bash
# Generate diagnostic report
raps debug report --include-logs --sanitize-tokens

# Submit support ticket
raps support create-ticket --attach-diagnostics
```

---

**💡 Pro Tip:** Most APS errors can be avoided by using RAPS CLI, which includes built-in validation, retry logic, and error recovery.

---

*RAPS v4.2.1 | APS APIs: Auth v2, DM v1, MD v2, OSS v2, DA v3 | January 2026*