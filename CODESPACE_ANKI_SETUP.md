# Port Forwarding Setup for AnkiConnect + Codespaces

## 🔧 Method 1: GitHub CLI Port Forwarding

**On your local machine** (where Anki is running):

```bash
# Forward local port 8765 to your Codespace
gh codespace ports forward 8765:8765 --codespace YOUR_CODESPACE_NAME
```

## 🔧 Method 2: VS Code Port Forwarding

1. **In VS Code Codespace**:
   - Open **Ports** tab (next to Terminal)
   - Click **Add Port**
   - Enter port: `8765`
   - Set visibility to **Public** or **Private**

2. **Get the forwarded URL** and test:
   ```bash
   curl -X POST https://YOUR-FORWARDED-URL/
   ```

## 🔧 Method 3: Direct IP Connection

**Find your local machine's IP:**
```bash
# On Windows
ipconfig | findstr "IPv4"

# On macOS/Linux  
ifconfig | grep "inet "
```

**Update test script to use your machine's IP:**
```python
# Instead of localhost:8765, use YOUR_IP:8765
request = urllib.request.Request('http://YOUR_LOCAL_IP:8765', request_json)
```

## 🎯 Quick Test Commands

Once connected, try:
```bash
# Test version
curl -X POST http://CONNECTION_URL:8765 -d '{"action": "version", "version": 6}'

# Test deck names  
curl -X POST http://CONNECTION_URL:8765 -d '{"action": "deckNames", "version": 6}'
```

**Which method would you like to try first?**
