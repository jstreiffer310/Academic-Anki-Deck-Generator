#!/bin/bash

echo "🔍 Quick Connection Test"
echo "======================="

# Check if IP is configured
if grep -q "YOUR_LOCAL_IP_HERE" ../.vscode/settings.json; then
    echo "⚠️  VS Code settings not configured yet"
    echo "💡 Run: ./connect_to_anki.sh to configure"
    exit 1
fi

# Get configured IP
LOCAL_IP=$(grep '"anki.api.hostname"' ../.vscode/settings.json | cut -d'"' -f4)
echo "🎯 Testing connection to: $LOCAL_IP:8765"

# Simple ping test first
echo "📡 Testing network connectivity..."
if ping -c 1 -W 3 "$LOCAL_IP" > /dev/null 2>&1; then
    echo "✅ Network reachable"
else
    echo "❌ Cannot reach $LOCAL_IP"
    echo "💡 Check that you're on the same network as your local machine"
    exit 1
fi

# Test AnkiConnect
echo "🧪 Testing AnkiConnect..."
python3 test_anki_connection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! You can now:"
    echo "   1. Open any .md file in anki-cards/"
    echo "   2. Press Ctrl+Shift+P"
    echo "   3. Search 'anki' and select 'Send to Deck'"
    echo "   4. Your cards will appear in Anki!"
else
    echo ""
    echo "❌ Connection failed. Make sure:"
    echo "   1. Anki is running on your local machine"
    echo "   2. You ran the setup script on your local machine first"
    echo "   3. AnkiConnect addon is installed in Anki"
fi