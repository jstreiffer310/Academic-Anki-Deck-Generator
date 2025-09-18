#!/bin/bash

echo "🎯 AUTOMATED ANKI CODESPACE SETUP"
echo "================================="
echo ""

# Step 1: Download helper for local machine
echo "📦 Creating setup files for your local machine..."

# Check if Windows helper exists
if [ ! -f "setup_anki_windows.bat" ]; then
    echo "❌ Setup files missing. Running initial setup..."
    ./setup_anki_connection.sh
fi

echo ""
echo "✅ Setup files ready!"
echo ""

# Step 2: Get IP from user
echo "🌐 NETWORK SETUP"
echo "==============="
echo ""
echo "First, set up your local machine:"
echo ""

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "📁 Windows: Double-click 'setup_anki_windows.bat'"
else
    echo "🖥️  Mac/Linux: Run these commands in terminal:"
    echo "   export ANKICONNECT_BIND_ADDRESS=0.0.0.0"
    echo "   # Then start Anki from the same terminal"
fi

echo ""
echo "Then find your local IP address:"
echo "   Windows: ipconfig | findstr 'IPv4'"
echo "   Mac:     ifconfig | grep 'inet ' | grep -v 127.0.0.1"  
echo "   Linux:   hostname -I"
echo ""

# Get IP from user with validation
while true; do
    read -p "Enter your local machine's IP address: " LOCAL_IP
    
    if [[ $LOCAL_IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        break
    else
        echo "❌ Invalid IP format. Please enter something like: 192.168.1.100"
    fi
done

echo ""
echo "🔧 Configuring VS Code settings..."

# Update VS Code settings
sed -i "s/YOUR_LOCAL_IP_HERE/$LOCAL_IP/g" ../.vscode/settings.json

echo "✅ VS Code configured for: $LOCAL_IP"
echo ""

# Step 3: Test connection
echo "🧪 TESTING CONNECTION"
echo "===================="
echo ""

./test_connection.sh

echo ""
echo "🎉 SETUP COMPLETE!"
echo ""
echo "💡 To test card creation:"
echo "   1. Open: anki-cards/high-priority.md"
echo "   2. Press: Ctrl+Shift+P"
echo "   3. Type: 'anki' and select 'Send to Deck'"
echo "   4. Check your Anki - the cards should appear!"