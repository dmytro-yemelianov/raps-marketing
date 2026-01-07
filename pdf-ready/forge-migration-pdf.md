---
title: "Forge to APS Migration Guide"
subtitle: "Complete step-by-step migration walkthrough"
version: "RAPS v4.2.1 | Migration deadline: December 31, 2026"
date: "January 2026"
layout: "a4-guide"
columns: 2
font-size: 8pt
---

# Forge to APS Migration Guide
**Complete step-by-step guide for migrating from legacy Autodesk Forge APIs to modern APS**

> ⚠️ **Migration Deadline:** December 31, 2026

---

## 📋 Migration Overview

### What's Changing

| **Aspect** | **Forge (Legacy)** | **APS (Current)** |
|------------|-------------------|-------------------|
| **Base URL** | `developer.api.autodesk.com` | `developer.api.autodesk.com` |
| **Branding** | "Forge" | "APS" |
| **API Endpoints** | Mixed versions | Standardized |
| **Authentication** | OAuth 2.0 | OAuth 2.0 |
| **SDKs** | Forge SDKs | APS SDKs |
| **Documentation** | forge.autodesk.com | aps.autodesk.com |

### What Stays the Same ✅

- ✅ OAuth 2.0 flow
- ✅ Core API functionality  
- ✅ File formats
- ✅ JSON response structure
- ✅ Rate limits

---

## 🔄 API Endpoint Migration

### Authentication API

| **Forge** | **APS** | **Notes** |
|-----------|---------|-----------|
| `/authentication/v1/authenticate` | `/authentication/v2/token` | ✅ **Updated** |
| `/authentication/v1/authorize` | `/authentication/v2/authorize` | ✅ **Updated** |

**Migration:**
1. Update endpoints to `/v2/`
2. Update scope format
3. Handle new response structure

### Data Management API

| **Forge** | **APS** | **Status** |
|-----------|---------|------------|
| `/project/v1/*` | `/project/v1/*` | ✅ **No change** |
| `/data/v1/*` | `/data/v1/*` | ✅ **No change** |

### Model Derivative API

| **Forge** | **APS** | **Status** |
|-----------|---------|------------|
| `/modelderivative/v2/*` | `/modelderivative/v2/*` | ✅ **No change** |

### Object Storage Service

| **Forge** | **APS** | **Status** |
|-----------|---------|------------|
| `/oss/v2/*` | `/oss/v2/*` | ✅ **No change** |

### Design Automation API

| **Forge** | **APS** | **Status** |
|-----------|---------|------------|
| `/da/us-east/v2/*` | `/da/us-east/v3/*` | ⚠️ **Updated** |

**Migration:** Update to v3, review breaking changes

---

## 🔑 OAuth Scopes Migration

### Scope Compatibility

| **Forge Scope** | **APS Scope** | **Notes** |
|------------------|---------------|-----------|
| `data:read` | `data:read` | ✅ No change |
| `data:write` | `data:write` | ✅ No change |
| `data:create` | `data:create` | ✅ No change |
| `bucket:read` | `bucket:read` | ✅ No change |
| `bucket:create` | `bucket:create` | ✅ No change |
| `viewables:read` | `viewables:read` | ✅ No change |
| `code:all` | `code:all` | ✅ No change |

**Good News:** All OAuth scopes are identical! ✅

---

## 📦 SDK Migration

### JavaScript/Node.js

```bash
# Remove Forge SDK
npm uninstall forge-apis

# Install APS SDK  
npm install autodesk-aps-sdk
```

**Code Changes:**
```javascript
// Old Forge SDK
const ForgeSDK = require('forge-apis');
const forgeApi = new ForgeSDK.AuthClientTwoLegged(
  clientId, clientSecret, scopes
);

// New APS SDK
const APS = require('autodesk-aps-sdk');
const apsApi = new APS.AuthenticationClient(
  clientId, clientSecret, scopes
);

// With RAPS (no SDK needed)
// raps auth login && raps dm projects
```

### .NET

```bash
# Remove Forge package
dotnet remove package Autodesk.Forge

# Add APS package
dotnet add package Autodesk.APS.SDK
```

### Python

```bash
# Remove Forge wrapper
pip uninstall forge-python-wrapper

# Install APS Python SDK
pip install autodesk-aps-python
```

---

## 📚 Documentation Migration

### URL Changes

| **Forge Resource** | **APS Resource** |
|--------------------|------------------|
| `forge.autodesk.com` | `aps.autodesk.com` |
| `learnforge.autodesk.io` | `tutorials.autodesk.io` |
| `forge-tutorials.autodesk.io` | `tutorials.autodesk.io/tutorials/` |

### GitHub Organizations

| **Forge** | **APS** |
|-----------|---------|
| `github.com/autodesk-forge/*` | `github.com/autodesk-platform-services/*` |

---

## ✅ Migration Checklist

### Phase 1: Assessment (Week 1)

**🔍 Audit Current Usage**
- [ ] List all APIs currently used
- [ ] Document authentication flows  
- [ ] Identify current scopes
- [ ] List SDK dependencies

**🔧 RAPS Assessment:**
```bash
# Test compatibility
raps auth migrate-assessment --forge-credentials

# Generate migration plan
raps migrate plan --current-apis forge --target-apis aps
```

### Phase 2: Development (Week 2)

**⚙️ Update Environment**
- [ ] Install new APS SDKs
- [ ] Update base URLs
- [ ] Update authentication to v2
- [ ] Test with dev credentials

**🧪 RAPS Development Testing:**
```bash
# Set up APS profile
raps config create-profile dev-aps
raps auth login --profile dev-aps --scopes data:read,data:write

# Test workflows
raps dm projects --profile dev-aps
raps translate <test-urn> --profile dev-aps
```

### Phase 3: Testing (Week 3)

**🧪 Testing Tasks**
- [ ] Test all API operations
- [ ] Verify authentication flows
- [ ] Test error handling
- [ ] Performance benchmarking
- [ ] End-to-end workflow testing

### Phase 4: Production (Week 4)

**🚀 Deployment Tasks**
- [ ] Update production environment
- [ ] Switch API endpoints
- [ ] Monitor application health
- [ ] Validate data integrity
- [ ] Remove Forge dependencies

---

## 🐛 Common Issues & Solutions

### 1. Authentication Token Issues

**Problem:** Forge v1 tokens not working  
**Solution:**
```bash
raps auth diagnose --check-aps-compatibility
raps auth migrate-from-forge --update-endpoints
```

### 2. SDK Breaking Changes

**Problem:** Method names changed  
**Solution:** Update method calls per new SDK docs

```javascript
// Old: forgeApi.authenticate()
// New: apsApi.getAccessToken()
// Better: raps auth login && raps <command>
```

### 3. Design Automation v3 Changes

**Problem:** DA v2 Activities incompatible  
**Solution:**
```bash
raps da list-legacy-activities
raps da migrate-activity <name> --from-v2 --to-v3
```

---

## ⏱️ Migration Timeline

### Simple Application (1-2 APIs)

| **Week** | **Tasks** | **Effort** |
|----------|-----------|------------|
| **Week 1** | Assessment, planning | 2-4 hours |
| **Week 2** | Code changes, testing | 4-8 hours |
| **Week 3** | Production deployment | 2-4 hours |

### Complex Application (Multiple APIs)

| **Week** | **Tasks** | **Effort** |
|----------|-----------|------------|
| **Week 1-2** | Assessment, planning | 8-16 hours |
| **Week 3-4** | Development, testing | 16-32 hours |
| **Week 5** | Integration testing | 8-16 hours |
| **Week 6** | Production deployment | 4-8 hours |

### Enterprise Application

| **Month** | **Phase** | **Focus** |
|-----------|-----------|-----------|
| **Month 1** | Planning | Full audit, stakeholder alignment |
| **Month 2** | Development | Code changes, CI/CD updates |
| **Month 3** | Testing | Comprehensive testing, training |
| **Month 4** | Migration | Phased rollout, monitoring |

---

## 📊 Performance Considerations

### API Rate Limits (No Change)

| **API** | **Forge** | **APS** | **Status** |
|---------|-----------|---------|------------|
| Authentication | 500/min | 500/min | ✅ Same |
| Data Management | 100/min | 100/min | ✅ Same |
| Model Derivative | 20 concurrent | 20 concurrent | ✅ Same |
| OSS | 500/min | 500/min | ✅ Same |

**No performance impact** expected from migration.

---

## 🧪 Testing Your Migration

### Compatibility Testing

```bash
# Test APS authentication
raps auth login --scopes data:read,viewables:read

# Test core operations
raps dm projects --limit 1
raps bucket list --limit 1
raps translate status <test-urn>

# Compare responses
raps compare-apis --forge-token <old> --aps-token <new>
```

### Regression Testing

1. **API Response Validation**
   - Compare JSON structure
   - Verify all fields present
   - Test error responses

2. **Workflow Testing**
   - Upload → Translate → View
   - Authentication chains
   - Webhook handling

3. **Performance Testing**
   - Response time comparison
   - Load testing
   - Memory usage monitoring

---

## 🗑️ Post-Migration Cleanup

### Remove Legacy Dependencies

```bash
# JavaScript
npm uninstall forge-apis forge-data-management

# Python
pip uninstall forge-python-wrapper

# .NET
dotnet remove package Autodesk.Forge
```

### Update Documentation

- [ ] Update API documentation references
- [ ] Change Forge → APS in user text
- [ ] Update code examples
- [ ] Update support docs

### Monitor Success

```bash
# Migration status
raps migration status --report

# API usage monitoring
raps logs --api-calls --since-migration

# System health validation
raps health check --comprehensive
```

---

## ❓ FAQ

**Q: Must I migrate immediately?**  
A: No, but Forge APIs sunset December 31, 2026

**Q: Will Forge tokens work with APS?**  
A: Forge v1 tokens need updating to APS v2

**Q: Are there breaking changes?**  
A: Most responses identical. Main change: auth v1→v2

**Q: Can I run both during migration?**  
A: Yes, parallel operation supported during transition

**Q: Does RAPS work with both?**  
A: RAPS uses APS by default, migration-compatible

---

## 📞 Migration Support

### Resources

1. **Official Migration Guide:** [aps.autodesk.com/migration](https://aps.autodesk.com/en/docs/oauth/v2/developers_guide/migration/)
2. **Community Support:** [APS Forums](https://forums.autodesk.com/t5/platform-services/bd-p/42)
3. **RAPS Community:** [RAPS Discord](https://discord.gg/raps-community)

### Migration Tools

```bash
raps migrate --help
raps auth migrate-from-forge  
raps compare-apis --forge-vs-aps
```

---

**💡 Pro Tip:** Use RAPS CLI to simplify migration. Many operations can be replaced with simple `raps` commands, reducing migration effort significantly.

---

*RAPS v4.2.1 | Migration Deadline: December 31, 2026 | January 2026*