---
title: "Forge to APS Migration Guide"
description: "Complete guide for migrating from legacy Autodesk Forge APIs to modern Autodesk Platform Services (APS)"
keywords: ["Forge", "APS", "migration", "API", "upgrade", "legacy", "Autodesk Platform Services"]
raps_commands: ["raps auth migrate-from-forge", "raps config set", "raps auth login"]
raps_version: ">=4.2.0"
aps_apis:
  authentication: "v2"
  data_management: "v1"
  model_derivative: "v2"
  design_automation: "v3"
  oss: "v2"
forge_apis:
  authentication: "v1" 
  data_management: "v1"
  model_derivative: "v2"
  design_automation: "v2"
last_verified: "January 2026"
migration_deadline: "2026-12-31"
---

# Forge to APS Migration Guide

**Complete step-by-step guide for migrating from legacy Autodesk Forge APIs to modern Autodesk Platform Services (APS)**

> ⚠️ **Important:** Forge APIs are being phased out. New applications should use APS APIs. Existing Forge applications must migrate by December 31, 2026.

---

## Migration Overview

### What's Changing

| Aspect | Forge (Legacy) | APS (Current) | Impact |
|--------|-----------------|---------------|---------|
| **Base URL** | `developer.api.autodesk.com` | `developer.api.autodesk.com` | No change |
| **Branding** | "Forge" | "Autodesk Platform Services" | Marketing/docs only |
| **API Endpoints** | Mixed versions | Standardized versions | Some endpoints updated |
| **Authentication** | OAuth 2.0 | OAuth 2.0 | Scope format changes |
| **SDKs** | Forge SDKs | APS SDKs | Package names changed |
| **Documentation** | forge.autodesk.com | aps.autodesk.com | New doc site |

### What Stays the Same

✅ **OAuth 2.0 flow** - Same authentication mechanism  
✅ **Core API functionality** - Same capabilities  
✅ **File formats** - Same supported formats  
✅ **Data structure** - Same JSON responses  
✅ **Rate limits** - Same throttling rules  

---

## API Endpoint Migration

### Authentication API

| Forge Endpoint | APS Endpoint | Status | Notes |
|----------------|--------------|---------|-------|
| `/authentication/v1/authenticate` | `/authentication/v2/token` | ✅ **Updated** | New version required |
| `/authentication/v1/authorize` | `/authentication/v2/authorize` | ✅ **Updated** | New version required |

**Migration Steps:**
1. Update endpoint URLs to use `/v2/` instead of `/v1/`
2. Update scope format (see OAuth Scopes section)
3. Handle new response structure

**RAPS Migration:**
```bash
# Old Forge authentication
curl -X POST "https://developer.api.autodesk.com/authentication/v1/authenticate" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET&grant_type=client_credentials&scope=data:read"

# With RAPS (handles APS v2 automatically)
raps auth login --scopes data:read
```

### Data Management API

| Forge Endpoint | APS Endpoint | Status | Notes |
|----------------|--------------|---------|-------|
| `/project/v1/*` | `/project/v1/*` | ✅ **No change** | Same endpoints |
| `/data/v1/*` | `/data/v1/*` | ✅ **No change** | Same endpoints |

**Migration Steps:**
- ✅ No changes required for Data Management API endpoints
- Update authentication to use v2 tokens

### Model Derivative API

| Forge Endpoint | APS Endpoint | Status | Notes |
|----------------|--------------|---------|-------|
| `/modelderivative/v2/*` | `/modelderivative/v2/*` | ✅ **No change** | Same endpoints |

**Migration Steps:**
- ✅ No changes required for Model Derivative API endpoints
- Update authentication to use v2 tokens

### Object Storage Service (OSS)

| Forge Endpoint | APS Endpoint | Status | Notes |
|----------------|--------------|---------|-------|
| `/oss/v2/*` | `/oss/v2/*` | ✅ **No change** | Same endpoints |

**Migration Steps:**
- ✅ No changes required for OSS API endpoints
- Update authentication to use v2 tokens

### Design Automation API

| Forge Endpoint | APS Endpoint | Status | Notes |
|----------------|--------------|---------|-------|
| `/da/us-east/v2/*` | `/da/us-east/v3/*` | ⚠️ **Updated** | Version bump required |

**Migration Steps:**
1. Update endpoint URLs to use `/v3/` instead of `/v2/`
2. Review breaking changes in v3 API
3. Update WorkItem and Activity definitions

**RAPS Migration:**
```bash
# Check current DA API version
raps da engines --version

# RAPS automatically uses DA v3
raps da create-activity MyActivity --engine Autodesk.AutoCAD+24
```

---

## OAuth Scopes Migration

### Scope Format Changes

| Forge Scope (v1) | APS Scope (v2) | Notes |
|-------------------|----------------|-------|
| `data:read` | `data:read` | ✅ No change |
| `data:write` | `data:write` | ✅ No change |
| `data:create` | `data:create` | ✅ No change |
| `bucket:read` | `bucket:read` | ✅ No change |
| `bucket:create` | `bucket:create` | ✅ No change |
| `bucket:delete` | `bucket:delete` | ✅ No change |
| `code:all` | `code:all` | ✅ No change |
| `viewables:read` | `viewables:read` | ✅ No change |
| `account:read` | `account:read` | ✅ No change |
| `account:write` | `account:write` | ✅ No change |

**Good News:** OAuth scopes are identical between Forge and APS! No changes needed.

### Token Structure

| Aspect | Forge | APS | Migration Required? |
|--------|-------|-----|-------------------|
| **Token format** | JWT | JWT | ✅ No |
| **Expiration** | 3600 seconds | 3600 seconds | ✅ No |
| **Refresh tokens** | Supported | Supported | ✅ No |
| **Scope validation** | Same | Same | ✅ No |

---

## SDK Migration

### JavaScript/Node.js

| Forge Package | APS Package | Install Command |
|---------------|-------------|-----------------|
| `forge-apis` | `autodesk-aps-sdk` | `npm install autodesk-aps-sdk` |
| `forge-data-management` | `@aps/data-management` | `npm install @aps/data-management` |

**Code Changes:**
```javascript
// Old Forge SDK
const ForgeSDK = require('forge-apis');
const forgeApi = new ForgeSDK.AuthClientTwoLegged(clientId, clientSecret, scopes);

// New APS SDK
const APS = require('autodesk-aps-sdk');
const apsApi = new APS.AuthenticationClient(clientId, clientSecret, scopes);

// With RAPS (no SDK needed for prototyping)
// raps auth login && raps dm projects
```

### .NET

| Forge Package | APS Package | Install Command |
|---------------|-------------|-----------------|
| `Autodesk.Forge` | `Autodesk.APS.SDK` | `dotnet add package Autodesk.APS.SDK` |

### Python

| Forge Package | APS Package | Install Command |
|---------------|-------------|-----------------|
| `forge-python-wrapper` | `autodesk-aps-python` | `pip install autodesk-aps-python` |

### Java

| Forge Package | APS Package | Install Command |
|---------------|-------------|-----------------|
| `forge-java-sdk` | `aps-java-sdk` | Maven/Gradle dependency update |

---

## Documentation Migration

### URL Changes

| Forge Resource | APS Resource | Notes |
|----------------|--------------|-------|
| `forge.autodesk.com` | `aps.autodesk.com` | Main documentation |
| `learnforge.autodesk.io` | `tutorials.autodesk.io` | Tutorials moved |
| `forge-tutorials.autodesk.io` | `tutorials.autodesk.io/tutorials/` | Path updated |
| GitHub: `autodesk-forge/*` | GitHub: `autodesk-platform-services/*` | Repo organization |

### Postman Collections

| Collection | Forge | APS |
|------------|-------|-----|
| **Download** | [Forge Postman](https://github.com/Autodesk-Forge/forge-api-postman-collection) | [APS Postman](https://github.com/autodesk-platform-services/aps-api-postman-collection) |
| **Base URL** | Variable: `{{forge_base_url}}` | Variable: `{{aps_base_url}}` |

---

## Migration Checklist

### Phase 1: Assessment (Week 1)

- [ ] **Audit current Forge usage**
  - [ ] List all APIs currently used
  - [ ] Identify authentication flows
  - [ ] Document current scopes
  - [ ] List SDK dependencies

- [ ] **Check compatibility**
  - [ ] Review API version requirements
  - [ ] Verify scope requirements unchanged
  - [ ] Test current tokens with APS endpoints

- [ ] **Plan migration timeline**
  - [ ] Prioritize critical applications
  - [ ] Schedule testing phases
  - [ ] Plan rollback strategy

**RAPS Assessment:**
```bash
# Test current setup compatibility
raps auth migrate-assessment --forge-credentials

# Generate migration report
raps migrate plan --current-apis forge --target-apis aps
```

### Phase 2: Development Environment (Week 2)

- [ ] **Update development environment**
  - [ ] Install new APS SDKs
  - [ ] Update base URLs to use APS endpoints
  - [ ] Update authentication to v2
  - [ ] Test with development credentials

- [ ] **Code changes**
  - [ ] Update package dependencies
  - [ ] Replace Forge SDK calls with APS equivalents
  - [ ] Update error handling for new responses
  - [ ] Update logging and monitoring

**RAPS Development Testing:**
```bash
# Set up APS development profile
raps config create-profile dev-aps
raps auth login --profile dev-aps --scopes data:read,data:write,viewables:read

# Test common workflows
raps dm projects --profile dev-aps
raps translate <test-urn> --profile dev-aps --formats svf2
```

### Phase 3: Testing (Week 3)

- [ ] **Functional testing**
  - [ ] Test all API operations
  - [ ] Verify authentication flows
  - [ ] Test error handling
  - [ ] Performance benchmarking

- [ ] **Integration testing**
  - [ ] End-to-end workflow testing
  - [ ] Third-party integration validation
  - [ ] User acceptance testing

### Phase 4: Production Migration (Week 4)

- [ ] **Production deployment**
  - [ ] Update production environment
  - [ ] Switch API endpoints
  - [ ] Monitor application health
  - [ ] Validate data integrity

- [ ] **Post-migration**
  - [ ] Remove Forge SDK dependencies
  - [ ] Update documentation
  - [ ] Train support team
  - [ ] Monitor for issues

---

## Common Migration Issues

### 1. Authentication Token Issues

**Problem:** Forge v1 tokens not working with APS  
**Solution:** Update to Authentication API v2

```bash
# Check current token compatibility
raps auth diagnose --check-aps-compatibility

# Migrate authentication
raps auth migrate-from-forge --update-endpoints
```

### 2. SDK Breaking Changes

**Problem:** Method names changed in new SDKs  
**Solution:** Update method calls according to new SDK documentation

```javascript
// Old Forge method
forgeApi.authenticate().then(token => { ... });

// New APS method  
apsApi.getAccessToken().then(token => { ... });

// Or skip SDKs entirely
// raps auth login && raps <command>
```

### 3. Design Automation v3 Changes

**Problem:** DA v2 Activities not compatible with v3  
**Solution:** Recreate Activities using v3 format

```bash
# List existing DA v2 activities
raps da list-legacy-activities

# Migrate to v3 format
raps da migrate-activity <activity-name> --from-v2 --to-v3
```

### 4. URL Reference Updates

**Problem:** Hardcoded Forge URLs in application  
**Solution:** Update to APS URLs

```javascript
// Update base URLs
const OLD_BASE = 'https://forge.autodesk.com';
const NEW_BASE = 'https://aps.autodesk.com';

// Better: Use configurable base URL
const baseUrl = process.env.APS_BASE_URL || 'https://aps.autodesk.com';
```

---

## Performance Considerations

### API Rate Limits

| API | Forge Limits | APS Limits | Change |
|-----|-------------|------------|--------|
| Authentication | 500/min | 500/min | ✅ Same |
| Data Management | 100/min | 100/min | ✅ Same |
| Model Derivative | 20 concurrent | 20 concurrent | ✅ Same |
| OSS | 500/min | 500/min | ✅ Same |
| Design Automation | 50 concurrent | 50 concurrent | ✅ Same |

**No performance impact expected** from Forge to APS migration.

### Caching Strategy

- ✅ **Authentication tokens:** Same caching strategy
- ✅ **API responses:** Same response format, no caching changes
- ✅ **Rate limiting:** Same rate limiting logic

---

## Testing Your Migration

### Compatibility Testing

```bash
# Test APS authentication
raps auth login --scopes data:read,viewables:read

# Test core operations
raps dm projects --limit 1
raps bucket list --limit 1
raps translate status <test-urn>

# Compare Forge vs APS responses
raps compare-apis --forge-token <old-token> --aps-token <new-token> --endpoint /oss/v2/buckets
```

### Regression Testing

1. **API Response Validation**
   - Compare JSON structure between Forge and APS
   - Verify all fields present
   - Test error responses

2. **Workflow Testing**
   - Upload → Translate → View pipeline
   - Authentication → API call chains
   - Webhook event handling

3. **Performance Testing**
   - Compare response times
   - Test under load
   - Monitor memory usage

---

## Post-Migration Cleanup

### Remove Legacy Dependencies

```bash
# JavaScript/Node.js
npm uninstall forge-apis
npm uninstall forge-data-management

# Python
pip uninstall forge-python-wrapper

# .NET
dotnet remove package Autodesk.Forge
```

### Update Documentation

- [ ] Update API documentation references
- [ ] Change Forge → APS in user-facing text
- [ ] Update code examples
- [ ] Update support documentation

### Monitor Migration Success

```bash
# Check migration status
raps migration status --report

# Monitor API usage
raps logs --api-calls --since-migration

# Validate all systems operational
raps health check --comprehensive
```

---

## Migration Timeline Examples

### Simple Application (1-2 APIs)

| Week | Tasks | Effort |
|------|-------|--------|
| **Week 1** | Assessment, planning | 2-4 hours |
| **Week 2** | Code changes, testing | 4-8 hours |
| **Week 3** | Production deployment | 2-4 hours |

### Complex Application (Multiple APIs)

| Week | Tasks | Effort |
|------|-------|--------|
| **Week 1-2** | Assessment, planning | 8-16 hours |
| **Week 3-4** | Code changes, unit testing | 16-32 hours |
| **Week 5** | Integration testing | 8-16 hours |
| **Week 6** | Production deployment, monitoring | 4-8 hours |

### Enterprise Application

| Month | Phase | Tasks |
|-------|-------|-------|
| **Month 1** | Planning | Full audit, stakeholder alignment |
| **Month 2** | Development | Code changes, CI/CD updates |
| **Month 3** | Testing | Comprehensive testing, user training |
| **Month 4** | Migration | Phased rollout, monitoring |

---

## Getting Help

### Migration Support Resources

1. **Official Documentation**
   - [APS Migration Guide](https://aps.autodesk.com/en/docs/oauth/v2/developers_guide/migration/)
   - [API Breaking Changes](https://aps.autodesk.com/en/docs/oauth/v2/developers_guide/migration/breaking-changes/)

2. **Community Support**
   - [APS Developer Forum](https://forums.autodesk.com/t5/platform-services/bd-p/42)
   - [RAPS Discord](https://discord.gg/raps-community)
   - [Stack Overflow: autodesk-platform-services](https://stackoverflow.com/questions/tagged/autodesk-platform-services)

3. **Migration Tools**
   ```bash
   # RAPS migration utilities
   raps migrate --help
   raps auth migrate-from-forge
   raps compare-apis --forge-vs-aps
   ```

### Professional Migration Services

For complex enterprise migrations, consider:
- Autodesk Professional Services
- Certified Autodesk Partners
- Independent APS consultants

---

## FAQ

**Q: Do I have to migrate immediately?**  
A: No, but Forge APIs will be sunset December 31, 2026. Plan your migration well in advance.

**Q: Will my existing Forge tokens work with APS?**  
A: Forge v1 tokens will not work with APS v2 endpoints. You need to update to v2 authentication.

**Q: Are there any breaking changes in API responses?**  
A: Most API responses are identical. The main change is authentication (v1 → v2).

**Q: Can I use both Forge and APS during migration?**  
A: Yes, you can run both in parallel during your migration period.

**Q: Does RAPS work with both Forge and APS?**  
A: RAPS uses APS APIs by default, but can be configured for backward compatibility during migration.

**Q: What happens if I don't migrate by the deadline?**  
A: Forge APIs will be shut down, breaking your application. Migration is mandatory.

---

**💡 Pro Tip:** Use RAPS CLI to simplify your migration. Instead of updating complex SDK code, many operations can be replaced with simple `raps` commands, reducing migration effort significantly.

---

*Last updated: January 2026 | Migration deadline: December 31, 2026*  
*This guide covers the most common migration scenarios. For complex cases, consult the [official APS migration documentation](https://aps.autodesk.com/en/docs/oauth/v2/developers_guide/migration/).*