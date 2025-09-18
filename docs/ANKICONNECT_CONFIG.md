# 🔧 AnkiConnect Configuration for Remote Access

## Current Problem
Your AnkiConnect config only allows local connections:
```json
{
    "webBindAddress": "127.0.0.1",        ← Only local machine
    "webCorsOriginList": [
        "http://localhost"                  ← Only localhost
    ]
}
```

## ✅ Required Changes

### Option 1: Allow All Remote Connections (Easier)
```json
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "0.0.0.0",           ← Allow connections from any IP
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost",
        "*"                                 ← Allow any origin
    ]
}
```

### Option 2: Specific Codespace Access (More Secure)
```json
{
    "apiKey": null,
    "apiLogPath": null,
    "ignoreOriginList": [],
    "webBindAddress": "0.0.0.0",           ← Allow connections from any IP
    "webBindPort": 8765,
    "webCorsOriginList": [
        "http://localhost",
        "https://*.github.dev",             ← Allow GitHub Codespaces
        "https://*.gitpod.io"               ← Allow Gitpod (if using)
    ]
}
```

## 🔧 How to Change AnkiConnect Settings

### Method 1: Through Anki Interface
1. **Open Anki**
2. **Tools** → **Add-ons**
3. **Select AnkiConnect** → **Config**
4. **Replace the config** with Option 1 or 2 above
5. **Save and restart Anki**

### Method 2: Direct File Edit
**Config file location:**
- **Windows**: `%APPDATA%/Anki2/addons21/2055492159/config.json`
- **Mac**: `~/Library/Application Support/Anki2/addons21/2055492159/config.json`
- **Linux**: `~/.local/share/Anki2/addons21/2055492159/config.json`

## 🧪 Test After Changes

1. **Restart Anki** after changing config
2. **Run test from Codespace**:
   ```bash
   cd setup && ./test_connection.sh
   ```

## 🔒 Security Notes

- **Use Option 2** for better security (specific origins only)
- **Only use on trusted networks** (home/work)
- **Consider setting an API key** for additional security:
  ```json
  "apiKey": "your-secret-key-here"
  ```

## 🆘 Still Not Working?

If it still fails after config changes:
1. **Check firewall** - Allow port 8765
2. **Verify Anki restart** - Config changes need restart
3. **Test locally first** - Visit http://localhost:8765
4. **Check network** - Ensure same network as Codespace