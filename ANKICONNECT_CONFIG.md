# 🔧 AnkiConnect Configuration for GitHub Codespaces

## 🎯 The Problem Identified!

Your AnkiConnect settings show:
```json
{
    "webBindAddress": "127.0.0.1",
    "webCorsOriginList": ["http://localhost"]
}
```

**This blocks external connections!** Codespaces run on different domains/IPs.

## ✅ Solution: Configure AnkiConnect for Remote Access

### Step 1: Update AnkiConnect Settings

1. **Open Anki**
2. **Tools** → **Add-ons** → **AnkiConnect** → **Config**
3. **Replace the settings** with:

```json
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "0.0.0.0",
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost",
        "https://*.githubpreview.dev",
        "https://*.github.dev", 
        "https://*.githubusercontent.com",
        "https://*.codespaces.githubusercontent.com",
        "https://glowing-space-dollop-wr5r957xv9wqfgq6g-8765.app.github.dev"
    ]
}
```

**IMPORTANT**: Add your specific Codespace URL to the CORS list!

### Step 2: Restart Anki

**Important**: Restart Anki completely for changes to take effect.

### Step 3: Test Connection
