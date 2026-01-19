---
title: "3-Legged OAuth Visual Walkthrough"
description: "Master APS 3-legged authentication with step-by-step diagrams and code"
category: "authentication"
difficulty: "intermediate"
readTime: 20
order: 1
---

# 3-Legged OAuth Visual Walkthrough

**Master APS 3-legged authentication with step-by-step diagrams and code**

---

## 🎯 Why This Guide Exists

The 3-legged OAuth flow is **the most confusing part of APS development**. Developers consistently get lost in:
- The difference between authorization code vs access token
- When to redirect vs when to make API calls
- How callback URLs actually work
- Managing token refresh properly

This guide provides **visual diagrams** and **working code** to eliminate the confusion.

---

## 🔄 The Complete Flow Diagram

```
┌──────────────┐     1. User clicks "Login"      ┌──────────────┐
│   Your App   │ ─────────────────────────────→  │   Autodesk   │
│              │                                  │   OAuth      │
│              │ ←───────────────────────────── │   Server     │
│              │     2. Redirect to /authorize   │              │
└──────────────┘                                  └──────────────┘
       │                                                 │
       │        3. User enters credentials               │
       │        4. User grants permissions               │
       ↓                                                 ↓
┌──────────────┐     5. Redirect with ?code=...  ┌──────────────┐
│   Callback   │ ←────────────────────────────── │   Autodesk   │
│   Endpoint   │                                  │              │
│              │ ─────────────────────────────→  │              │
│              │     6. Exchange code for token   │              │
└──────────────┘                                  └──────────────┘
       │
       │     7. Store tokens, redirect to app
       ↓
┌──────────────┐
│   App Home   │  Now authenticated!
└──────────────┘
```

---

## 📋 Step-by-Step Breakdown

### Step 1: Initiate Authentication

**What happens**: User clicks "Login with Autodesk" in your app

**Your code does**:
```javascript
// Construct authorization URL
const authUrl = 'https://developer.api.autodesk.com/authentication/v2/authorize?' +
  'response_type=code' +
  '&client_id=' + CLIENT_ID +
  '&redirect_uri=' + encodeURIComponent(REDIRECT_URI) +
  '&scope=' + encodeURIComponent('data:read data:write');

// Redirect user to Autodesk
window.location.href = authUrl;
```

**What user sees**: Redirected to Autodesk login page

**RAPS equivalent**: `raps auth login --3legged`

---

### Step 2: User Authentication

**What happens**: User logs into their Autodesk account

**User experience**:
```
┌─────────────────────────────────┐
│     Autodesk Login Page         │
│                                 │
│  Email: user@company.com        │
│  Password: ••••••••             │
│                                 │
│  [Login] [Forgot Password?]     │
└─────────────────────────────────┘
```

**Your app**: Waits for callback (no action needed)

---

### Step 3: Permission Grant

**What happens**: User sees permission request and clicks "Allow"

**User experience**:
```
┌─────────────────────────────────┐
│   Authorization Request         │
│                                 │
│  YourApp wants to:              │
│  ✓ Read your files              │
│  ✓ Write to your projects       │
│                                 │
│  [Allow] [Deny]                 │
└─────────────────────────────────┘
```

**Your app**: Still waiting for callback

---

### Step 4: Authorization Code Return

**What happens**: Autodesk redirects back to your app with authorization code

**HTTP Request to your callback**:
```
GET /callback?code=ABC123...&state=optional HTTP/1.1
Host: yourapp.com
```

**Your callback endpoint receives**:
```javascript
app.get('/callback', (req, res) => {
  const authCode = req.query.code;
  const state = req.query.state; // verify if you sent one
  
  if (!authCode) {
    // User denied permission or error occurred
    return res.redirect('/login?error=access_denied');
  }
  
  // Continue to Step 5...
});
```

---

### Step 5: Exchange Code for Tokens

**What happens**: Your server exchanges authorization code for access token

**API Call**:
```javascript
const tokenResponse = await fetch('https://developer.api.autodesk.com/authentication/v2/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded'
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authCode,
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    redirect_uri: REDIRECT_URI
  })
});

const tokens = await tokenResponse.json();
```

**Response**:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "refresh_token": "OjfMGp8pF7gQPq5wYiRnwP1kLp...",
  "token_type": "Bearer", 
  "expires_in": 3600
}
```

---

### Step 6: Store Tokens and Complete Login

**What happens**: Your app stores tokens securely and redirects user to app

**Security considerations**:
```javascript
// ✅ SECURE: Server-side session storage
req.session.accessToken = tokens.access_token;
req.session.refreshToken = tokens.refresh_token;

// ❌ INSECURE: Client-side storage
localStorage.setItem('token', tokens.access_token); // Don't do this!
```

**Complete the flow**:
```javascript
// Store tokens securely
await storeUserTokens(userId, tokens);

// Redirect to app home
res.redirect('/dashboard?login=success');
```

---

## 📊 Flow Summary Table

| Step | Endpoint | What You Send | What You Get | Who Initiates |
|------|----------|---------------|--------------|---------------|
| 1 | `/authorize` | client_id, redirect_uri, scope, response_type=code | Redirect to Autodesk login | Your app |
| 2-3 | (user action) | - | User logs in and grants permissions | User |
| 4 | `/callback` | (receive code parameter) | Authorization code | Autodesk |
| 5 | `/token` | code, client_id, client_secret, grant_type=authorization_code | access_token, refresh_token | Your app |

---

## 🔧 Complete Working Example

### Frontend (HTML + JavaScript)

```html
<!DOCTYPE html>
<html>
<head>
    <title>APS 3-Legged Auth Demo</title>
</head>
<body>
    <div id="loginSection">
        <h1>APS Authentication Demo</h1>
        <button onclick="startAuth()">Login with Autodesk</button>
    </div>
    
    <div id="userSection" style="display: none;">
        <h1>Welcome!</h1>
        <p>Access Token: <span id="tokenDisplay"></span></p>
        <button onclick="logout()">Logout</button>
    </div>

    <script>
        const CLIENT_ID = 'your_client_id';
        const REDIRECT_URI = 'http://localhost:3000/callback';
        const SCOPES = 'data:read data:write';

        function startAuth() {
            const authUrl = `https://developer.api.autodesk.com/authentication/v2/authorize?` +
                `response_type=code&` +
                `client_id=${CLIENT_ID}&` +
                `redirect_uri=${encodeURIComponent(REDIRECT_URI)}&` +
                `scope=${encodeURIComponent(SCOPES)}`;
            
            window.location.href = authUrl;
        }

        // Check if we just returned from auth
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.get('token')) {
            showUserSection(urlParams.get('token'));
        }

        function showUserSection(token) {
            document.getElementById('loginSection').style.display = 'none';
            document.getElementById('userSection').style.display = 'block';
            document.getElementById('tokenDisplay').textContent = token.substring(0, 20) + '...';
        }

        function logout() {
            // Clear session
            fetch('/logout', { method: 'POST' })
                .then(() => window.location.reload());
        }
    </script>
</body>
</html>
```

### Backend (Node.js + Express)

```javascript
const express = require('express');
const session = require('express-session');
const app = express();

// Configure session
app.use(session({
    secret: 'your-session-secret',
    resave: false,
    saveUninitialized: false
}));

const CLIENT_ID = process.env.APS_CLIENT_ID;
const CLIENT_SECRET = process.env.APS_CLIENT_SECRET;
const REDIRECT_URI = 'http://localhost:3000/callback';

// Serve static files
app.use(express.static('public'));

// OAuth callback endpoint
app.get('/callback', async (req, res) => {
    const authCode = req.query.code;
    
    if (!authCode) {
        return res.redirect('/?error=access_denied');
    }

    try {
        // Exchange code for tokens
        const response = await fetch('https://developer.api.autodesk.com/authentication/v2/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                grant_type: 'authorization_code',
                code: authCode,
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET,
                redirect_uri: REDIRECT_URI
            })
        });

        const tokens = await response.json();

        if (tokens.access_token) {
            // Store in session
            req.session.accessToken = tokens.access_token;
            req.session.refreshToken = tokens.refresh_token;
            
            // Redirect with success
            res.redirect(`/?token=${tokens.access_token}`);
        } else {
            res.redirect('/?error=token_exchange_failed');
        }
    } catch (error) {
        console.error('Token exchange error:', error);
        res.redirect('/?error=server_error');
    }
});

// Logout endpoint
app.post('/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true });
});

// API endpoint example
app.get('/api/user-info', async (req, res) => {
    const token = req.session.accessToken;
    
    if (!token) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    try {
        const userResponse = await fetch('https://developer.api.autodesk.com/userprofile/v1/users/@me', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const userData = await userResponse.json();
        res.json(userData);
    } catch (error) {
        res.status(500).json({ error: 'Failed to fetch user info' });
    }
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
```

---

## 🚨 Common Mistakes & Solutions

### 1. Callback URL Mismatch

**❌ Problem**: `redirect_uri_mismatch` error

**Cause**: URL in code doesn't exactly match APS app settings

**✅ Solution**: 
```javascript
// In APS app settings: http://localhost:3000/callback
// In your code: 
const REDIRECT_URI = 'http://localhost:3000/callback'; // Must match exactly
```

### 2. Storing Tokens Insecurely

**❌ Problem**: Tokens in localStorage or client-side cookies

**Cause**: Security vulnerability - tokens can be stolen by XSS

**✅ Solution**:
```javascript
// ✅ SECURE: Server-side session storage
req.session.accessToken = tokens.access_token;

// ✅ SECURE: Encrypted HTTP-only cookies
res.cookie('session_id', sessionId, { 
    httpOnly: true, 
    secure: true, 
    sameSite: 'strict' 
});
```

### 3. Not Handling Token Refresh

**❌ Problem**: App breaks when access token expires (after 1 hour)

**Cause**: No token refresh logic

**✅ Solution**:
```javascript
async function refreshTokenIfNeeded() {
    const tokenAge = Date.now() - req.session.tokenTimestamp;
    
    if (tokenAge > 55 * 60 * 1000) { // Refresh 5 min before expiry
        const response = await fetch('https://developer.api.autodesk.com/authentication/v2/token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                grant_type: 'refresh_token',
                refresh_token: req.session.refreshToken,
                client_id: CLIENT_ID,
                client_secret: CLIENT_SECRET
            })
        });
        
        const newTokens = await response.json();
        req.session.accessToken = newTokens.access_token;
        req.session.tokenTimestamp = Date.now();
    }
}
```

### 4. Forgetting State Parameter

**❌ Problem**: CSRF attacks possible

**Cause**: No state validation

**✅ Solution**:
```javascript
// Generate state when starting auth
const state = crypto.randomBytes(16).toString('hex');
req.session.oauthState = state;

const authUrl = `https://developer.api.autodesk.com/authentication/v2/authorize?` +
    `state=${state}&` + // Add state parameter
    `response_type=code&...`;

// Validate state in callback
app.get('/callback', (req, res) => {
    if (req.query.state !== req.session.oauthState) {
        return res.redirect('/?error=invalid_state');
    }
    // Continue with token exchange...
});
```

---

## 🎯 Testing Your Implementation

### 1. Test the Authorization URL

**Manually visit**:
```
https://developer.api.autodesk.com/authentication/v2/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fcallback&scope=data%3Aread%20data%3Awrite
```

**Expected**: Autodesk login page loads

### 2. Test Callback Handling

**Mock callback**:
```
http://localhost:3000/callback?code=test123&state=abc
```

**Expected**: Your callback handler receives the code

### 3. Test API Calls

**With valid token**:
```javascript
fetch('/api/user-info')
  .then(r => r.json())
  .then(data => console.log(data));
```

**Expected**: User profile data returned

---

## 💡 RAPS CLI Alternative

**Instead of implementing this yourself**:

```bash
# RAPS handles the entire flow automatically
raps auth login --3legged

# Check authentication status
raps auth status

# Make authenticated API calls
raps dm projects
```

**Benefits of RAPS**:
- ✅ Automatic token refresh
- ✅ Secure token storage
- ✅ Built-in error handling
- ✅ No callback URL setup needed
- ✅ Works across all platforms

---

## 📚 Related Resources

### APS Documentation
- [3-Legged OAuth Tutorial](https://aps.autodesk.com/en/docs/oauth/v2/tutorials/get-3-legged-token/)
- [OAuth 2.0 Specification](https://tools.ietf.org/html/rfc6749)

### Other RAPS Guides
- [ACC Provisioning Checklist](../acc-provisioning-checklist) — Fix 403 errors
- [Token Refresh Patterns](../token-refresh-patterns) — Production-ready token management

### Tools
- [Token Decoder Tool](../../tools/token-decoder) — Inspect your tokens
- [Token Cost Estimator](../../tools/token-estimator) — Calculate API costs

---

## ❓ Still Confused?

**Common questions**:

**Q**: Why do I need both authorization code AND access token?
**A**: Security. The authorization code proves user consent. The access token proves your app's identity. Two-step verification prevents token theft.

**Q**: Can I skip the callback URL?
**A**: No. It's required by OAuth 2.0 spec. Even for mobile apps, you need a custom scheme callback.

**Q**: What if my callback URL changes?
**A**: Update it in your APS app settings. Must match exactly or you'll get `redirect_uri_mismatch`.

**Q**: How long do tokens last?
**A**: Access tokens: 1 hour. Refresh tokens: 14 days. Plan accordingly.

---

*Last Updated: January 2026 | RAPS v4.2.1*  
*This guide eliminates 90% of OAuth implementation confusion*