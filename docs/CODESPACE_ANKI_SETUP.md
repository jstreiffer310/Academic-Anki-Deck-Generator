# 🌐 Codespace to Local Anki Connection Setup

## The Challenge
You want to use VS Code in GitHub Codespace to create cards that get sent to Anki running on your local machine.

## 🔧 Solution: Configure Remote AnkiConnect Access

### Step 1: Configure AnkiConnect for Remote Access

**On your local machine:**

1. **Close Anki completely**

2. **Set environment variable** before starting Anki:

**Windows (PowerShell):**
```powershell
$env:ANKICONNECT_BIND_ADDRESS = "0.0.0.0"
# Then start Anki from the same PowerShell window
```

**Windows (Command Prompt):**
```cmd
set ANKICONNECT_BIND_ADDRESS=0.0.0.0
# Then start Anki from the same command prompt
```

**Mac/Linux:**
```bash
export ANKICONNECT_BIND_ADDRESS=0.0.0.0
# Then start Anki from the same terminal
```

3. **Start Anki** - AnkiConnect will now accept connections from any IP address

4. **Test locally** - visit http://localhost:8765 (should still work)

### Step 2: Get Your Local Machine's IP

**Find your local IP address:**

**Windows:**
```powershell
ipconfig | findstr "IPv4"
```

**Mac:**
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

**Linux:**
```bash
hostname -I
```

Look for something like `192.168.1.xxx` or `10.0.0.xxx`

### Step 3: Update Codespace Settings

**Update VS Code settings to point to your local machine:**

1. **Get your local IP** (from Step 2) - something like `192.168.1.100`

2. **Update settings**: The file `.vscode/settings.json` is already configured for remote access

3. **Replace YOUR_LOCAL_IP_HERE** with your actual IP address:
   ```json
   {
       "anki.api.hostname": "192.168.1.100",  // ← Put your IP here
       "anki.api.port": 8765,
       "anki.api.schema": "http",
       "anki.defaultDeck": "PSYC 2240 - High Priority",
       "anki.template": "Basic",
       "anki.md.createTagForTitle": true,
       "anki.md.defaultDeck": "PSYC 2240 - Supplemental",
       "anki.api.allowRemote": true
   }
   ```

### Step 4: Test the Connection

1. **Update test script** to use your local IP:

2. **Run test**:
   ```bash
   python3 test_anki_connection.py
   ```

3. **If successful**, try creating a card in VS Code!

## 🎯 Workflow Once Connected

**This setup enables:**
- ✅ Create cards in Codespace VS Code 
- ✅ Send directly to local Anki
- ✅ Maintain your existing deck structure
- ✅ Live card creation while studying
- ✅ Git version control of your card templates

**Perfect for streamlining your PSYC 2240 deck creation! 🚀**

## 🔒 Security Note

**Remember to:**
- Only use this on trusted networks (home/work)
- Close Anki when done to stop remote access
- The connection is HTTP (not encrypted) - only use on local networks

## 🆘 Troubleshooting

**If connection fails:**
1. Check firewall settings on local machine
2. Verify Anki is running with the environment variable set
3. Confirm IP address is correct
4. Try pinging your local machine from Codespace