# Onshape OAuth 401 Error: Complete Authentication Fix Guide

## The Quick Fix
**Onshape OAuth 401 errors** are almost always caused by improper URL encoding of client credentials, especially trailing `=` characters in client secrets.

## Why Onshape OAuth Fails

### The #1 Cause: URL Encoding Issues
```javascript
// WRONG - This will cause 401
const clientSecret = "abc123==";
const body = `client_id=${clientId}&client_secret=${clientSecret}`;

// CORRECT - URL encode everything
const body = `client_id=${encodeURIComponent(clientId)}&client_secret=${encodeURIComponent(clientSecret)}`;
```

**Real Developer Quote:**
> "The body of the form needs to contain the client ID, client secret, authorization_code... Each of the parameters in the POST body need to be URL encoded - this is especially important for the Client ID and secret since either or both may contain multiple trailing '=' characters."

## Complete OAuth Implementation

### Step 1: Proper Token Request
```javascript
async function getOnshapeToken(code) {
  const params = new URLSearchParams();
  params.append('grant_type', 'authorization_code');
  params.append('client_id', CLIENT_ID);
  params.append('client_secret', CLIENT_SECRET);
  params.append('code', code);
  params.append('redirect_uri', REDIRECT_URI);

  const response = await fetch('https://oauth.onshape.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body: params.toString() // URLSearchParams handles encoding
  });

  if (!response.ok) {
    const error = await response.text();
    console.error('OAuth failed:', response.status, error);
    throw new Error(`OAuth 401: ${error}`);
  }

  return response.json();
}
```

### Step 2: Handle Refresh Tokens
```javascript
async function refreshOnshapeToken(refreshToken) {
  const params = new URLSearchParams();
  params.append('grant_type', 'refresh_token');
  params.append('client_id', CLIENT_ID);
  params.append('client_secret', CLIENT_SECRET);
  params.append('refresh_token', refreshToken);

  const response = await fetch('https://oauth.onshape.com/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: params.toString()
  });

  if (response.status === 401) {
    // Refresh token expired - need full reauth
    throw new Error('Refresh token expired - reauthenticate');
  }

  return response.json();
}
```

## Common 401 Scenarios

### Scenario 1: Webhook Response Codes
**Problem**: Returning wrong HTTP status
```javascript
// WRONG - Causes webhook deregistration
res.status(201).send('Created');

// CORRECT - Onshape requires exactly 200
res.status(200).send('OK');
```

### Scenario 2: Authorization Header Format
**Problem**: Incorrect Bearer token format
```javascript
// WRONG
headers: {
  'Authorization': accessToken
}

// CORRECT
headers: {
  'Authorization': `Bearer ${accessToken}`
}
```

### Scenario 3: Expired Tokens
**Problem**: Not handling token expiration
```javascript
// Implement token refresh before expiry
if (Date.now() >= tokenExpiryTime - 60000) { // Refresh 1 min early
  const newTokens = await refreshOnshapeToken(refreshToken);
  accessToken = newTokens.access_token;
  refreshToken = newTokens.refresh_token;
  tokenExpiryTime = Date.now() + (newTokens.expires_in * 1000);
}
```

## Python Implementation

```python
import urllib.parse
import requests
import base64

def get_onshape_token(code, client_id, client_secret, redirect_uri):
    """Get Onshape OAuth token with proper encoding"""
    
    # URL encode all parameters
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    # Use requests library encoding
    response = requests.post(
        'https://oauth.onshape.com/oauth/token',
        data=data,  # requests handles URL encoding
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
    )
    
    if response.status_code == 401:
        print(f"401 Error: {response.text}")
        # Common issues to check:
        # 1. Client secret has trailing '=' not encoded
        # 2. Redirect URI doesn't match exactly
        # 3. Authorization code expired (very short TTL)
        raise Exception(f"OAuth failed: {response.text}")
    
    return response.json()
```

## Debugging 401 Errors

### Enable Detailed Logging
```javascript
// Log exact request being sent
console.log('OAuth Request:', {
  url: 'https://oauth.onshape.com/oauth/token',
  body: params.toString(),
  headers: headers
});

// Log raw response
const responseText = await response.text();
console.log('OAuth Response:', response.status, responseText);
```

### Common Error Messages

| Error Message | Cause | Solution |
|--------------|-------|----------|
| `invalid_client` | Client ID/Secret wrong | Check encoding, trailing spaces |
| `invalid_grant` | Code expired or invalid | Codes expire quickly, use immediately |
| `invalid_request` | Malformed request | Check Content-Type header |
| `unauthorized_client` | App not authorized | Check Onshape app settings |

## Local Testing Challenges

### HTTPS Certificate Requirements
Onshape webhooks **require valid HTTPS certificates**:

```javascript
// WRONG - Self-signed certificate
https.createServer({
  key: fs.readFileSync('self-signed.key'),
  cert: fs.readFileSync('self-signed.cert')
}, app);

// CORRECT - Use ngrok or similar
// Terminal: ngrok http 3000
// Use the ngrok HTTPS URL for webhooks
```

## Comparison with Other Platforms

| Platform | OAuth Complexity | Common 401 Cause |
|----------|-----------------|------------------|
| **Onshape** | HIGH | URL encoding of secrets |
| **Autodesk APS** | HIGH | 2-legged vs 3-legged confusion |
| **3DEXPERIENCE** | HIGH | Multi-platform sessions |
| **Teamcenter** | HIGH | SSO configuration |

## Best Practices

### 1. Always Use URL Encoding Libraries
```javascript
// Good - Let libraries handle encoding
const params = new URLSearchParams();

// Bad - Manual string concatenation
const body = `param=${value}`;
```

### 2. Implement Exponential Backoff
```javascript
async function retryWithBackoff(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (error.message.includes('401') && i < maxRetries - 1) {
        await new Promise(r => setTimeout(r, Math.pow(2, i) * 1000));
      } else {
        throw error;
      }
    }
  }
}
```

### 3. Store Tokens Securely
```javascript
// Use environment variables
const CLIENT_SECRET = process.env.ONSHAPE_CLIENT_SECRET;

// Never commit credentials
// .gitignore should include .env
```

## Why This Matters

Onshape OAuth issues waste countless developer hours:
- No clear documentation on encoding requirements
- Error messages don't indicate encoding issues
- Community forums full of confused developers
- Trial and error debugging

## Tools That Can Help

### URL Encoding Testers
- Online URL encoder/decoder tools
- Postman for testing OAuth flows
- Browser developer tools network tab

### Authentication Libraries
- Passport.js Onshape strategy
- OAuth2 client libraries with proper encoding

## SEO Keywords Covered
- onshape oauth 401 error
- onshape authentication failed
- onshape invalid client
- onshape url encoding oauth
- onshape bearer token 401
- onshape webhook authentication
- onshape api 401 unauthorized

---

*Part of our Cross-Platform CAD API Error Solutions series. Because every platform has authentication pain, but the solutions are knowable.*