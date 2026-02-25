---
title: "BIM360/ACC Provisioning Checklist: Fix 403 Errors"
description: "The #1 cause of APS API 403 errors — and how to fix them"
category: "troubleshooting"
difficulty: "beginner"
readTime: 10
order: 3
---

# BIM360/ACC Provisioning Checklist: Fix 403 Errors

**The #1 cause of APS API 403 errors — and how to fix them**

---

## ⚠️ The Problem

Getting `403 Forbidden` errors when calling APS APIs with BIM360 or Autodesk Construction Cloud (ACC)? You're not alone. 

**The root cause**: Developers don't realize they must manually enable custom integrations from the ACC admin console. This isn't mentioned in most tutorials, causing hours of frustration.

## 🎯 Quick Fix

**If you're getting 403 errors, skip to Step 3** — that's usually the missing piece.

---

## 📋 Complete Setup Checklist

### Step 1: Create APS Application

**✅ Prerequisites:**
- [ ] Autodesk account with developer access
- [ ] Access to [aps.autodesk.com](https://aps.autodesk.com)

**✅ App Creation:**
- [ ] Logged into APS Developer Portal
- [ ] Created new application
- [ ] Noted **Client ID** (you'll need this exact value)
- [ ] Noted **Client Secret** (keep secure!)
- [ ] Set **Callback URL** correctly:
  - Development: `http://localhost:3000/callback`
  - Production: Your actual domain
- [ ] Selected required **API access**:
  - ✅ Data Management API
  - ✅ Model Derivative API
  - ✅ Any other APIs you need

---

### Step 2: Verify ACC Admin Access

**✅ Account Requirements:**
- [ ] You are an **Account Admin** in ACC/BIM360 (not just Project Admin)
- [ ] Your ACC subscription is active
- [ ] You can access Account Administration settings

**❌ If you're NOT an Account Admin:**
```
Contact your ACC Account Admin and ask them to:
1. Add your APS Client ID to custom integrations
2. Grant required permissions
3. Share the integration details with you
```

---

### Step 3: Enable Custom Integration (CRITICAL STEP)

**🚨 This step is missed by 90% of developers**

**✅ In ACC Admin Console:**
- [ ] Logged into ACC as **Account Admin**
- [ ] Navigated to: **Account Admin → Settings → Custom Integrations**
- [ ] Clicked **"Add Custom Integration"**
- [ ] Entered your **exact Client ID** from Step 1
- [ ] Selected **required access levels**:
  - ✅ BIM 360 Account Admin (for account-level operations)
  - ✅ BIM 360 Docs (for file operations)
  - ✅ Any additional services you need
- [ ] Completed the integration wizard
- [ ] Waited **5-10 minutes** for propagation

**⏱️ Common mistake**: Not waiting for propagation. Changes take 5-10 minutes.

---

### Step 4: Per-Project Setup (If Using 2-Legged Auth)

**✅ Project-Level Access:**
- [ ] Added the custom integration to specific projects
- [ ] Verified integration appears in Project Admin → Integrations
- [ ] Granted necessary project permissions

**✅ For 3-Legged Auth:**
- [ ] Ensured user has project access
- [ ] User accepted any pending invitations
- [ ] User has appropriate role (Admin, Member, etc.)

---

### Step 5: Test Authentication

**✅ Basic Connection Test:**

```bash
# Using RAPS CLI
raps auth login
raps hub list
raps project list

# Should list your ACC projects without 403 errors
```

**✅ Manual API Test:**

```bash
# Get 3-legged token first, then:
curl -X GET \
  'https://developer.api.autodesk.com/project/v1/hubs' \
  -H 'Authorization: Bearer YOUR_3LEGGED_TOKEN'

# Should return hub data, not 403
```

---

## 🔧 Troubleshooting 403 Errors

### Error: "client_id does not have access"
**❌ Cause**: Integration not added to ACC (Step 3 skipped)
**✅ Fix**: Complete Step 3 — add Client ID to Custom Integrations

### Error: "User not authorized"  
**❌ Cause**: User lacks project permissions
**✅ Fix**: Grant user project access or use 2-legged auth

### Error: "Project not found"
**❌ Cause**: 3-legged token from wrong user
**✅ Fix**: Ensure user has access to the specific project

### Error: "Forbidden" (generic)
**❌ Cause**: Multiple possible issues
**✅ Fix**: Work through checklist step by step

---

## 🎭 Auth Flow Comparison

| Auth Type | When to Use | Setup Requirements | Common Issues |
|-----------|-------------|-------------------|---------------|
| **2-Legged** | Server-to-server automation | Custom Integration + Project access | Forget project setup |
| **3-Legged** | User-interactive apps | Custom Integration + User consent | Wrong user permissions |

**💡 RAPS CLI handles both flows automatically:**

```bash
# 3-legged (interactive)
raps auth login

# 2-legged (automated)  
raps auth set --client-id ID --client-secret SECRET
```

---

## 🕐 Timeline for Setup

| Step | Time Required | Can Be Automated? |
|------|---------------|-------------------|
| 1. Create APS app | 5 minutes | No |
| 2. Verify admin access | 0-24 hours | No |
| 3. Add custom integration | 5 minutes | No |
| 4. Project setup | 2 minutes/project | Partially |
| 5. Test connection | 1 minute | Yes |

**Total: 15-30 minutes + admin approval time**

---

## 🚨 Common Gotchas

### 1. Client ID Copy-Paste Errors
**Problem**: Typos when copying Client ID to ACC
**Solution**: Copy-paste, don't type manually

### 2. Regional Differences
**Problem**: EMEA accounts have different requirements
**Solution**: Use correct base URL and region headers

### 3. Multi-Tenant Confusion
**Problem**: Multiple ACC accounts, wrong integration
**Solution**: Verify you're in the correct account

### 4. Permission Inheritance
**Problem**: Assuming project permissions = account permissions
**Solution**: Grant both account AND project access

---

## 🔄 Migration from Forge

**If migrating from Forge:**

```markdown
Old Forge App → New APS App:
✅ Same process applies
✅ Must still add Client ID to ACC Custom Integrations  
✅ No automatic permission transfer
```

**Migration checklist:**
- [ ] Created new APS app (or migrated existing)
- [ ] Updated ACC Custom Integrations with new Client ID
- [ ] Tested all project access
- [ ] Updated application code to use APS endpoints

---

## 💻 Testing with RAPS CLI

**Validate your setup:**

```bash
# 1. Check authentication
raps auth status

# 2. List accessible hubs
raps hub list

# 3. List projects in a hub
raps project list

# 4. Test file operations
raps folder list
```

**Expected output:**
- ✅ No 403 errors
- ✅ Your ACC projects listed
- ✅ Folder structure visible

---

## 📞 When You Need Help

### Still getting 403s after following this guide?

**Check these:**
1. **Timing**: Wait 15+ minutes after adding integration
2. **Region**: Ensure consistent US/EMEA region usage  
3. **Scopes**: Verify your token has required scopes
4. **User**: Confirm the user actually has project access

**Get support:**
- 🆘 **RAPS Discord**: [discord.gg/raps](https://discord.gg/raps)
- 📧 **Email**: [support@rapscli.xyz](mailto:support@rapscli.xyz)
- 🤖 **RAPS CLI**: `raps support create-ticket`

---

## 🎯 Success Checklist

**You're ready when:**
- [ ] No 403 errors on basic API calls
- [ ] Can list ACC projects via API
- [ ] Can upload/download files  
- [ ] RAPS CLI authentication works
- [ ] All team members can access

**Time saved**: ~4 hours of debugging per developer 🎉

---

## 📚 Related Guides

- [3-Legged Auth Visual Walkthrough](../3legged-auth-visual) — Understanding OAuth flow
- [Token Refresh Patterns](../token-refresh-patterns) — Production authentication  
- [Region Mismatch Debugger](../../tools/region-checker) — US/EMEA troubleshooting

---

*Last Updated: February 2026 | RAPS v4.14.0*  
*Based on community feedback from 1000+ developers*