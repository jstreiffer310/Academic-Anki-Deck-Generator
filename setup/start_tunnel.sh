#!/bin/bash
echo "🚀 Starting tunnel to your local Anki..."
echo "⚠️  Make sure Anki is running on your local machine with:"
echo "   ANKICONNECT_BIND_ADDRESS=0.0.0.0"
echo ""

# Get local IP from user
read -p "Enter your local machine's IP address: " LOCAL_IP

if [ -z "$LOCAL_IP" ]; then
    echo "❌ No IP provided. Exiting."
    exit 1
fi

echo "🔗 Creating tunnel to $LOCAL_IP:8765..."

# Update VS Code settings with the IP
sed -i "s/YOUR_LOCAL_IP_HERE/$LOCAL_IP/g" .vscode/settings.json

echo "📝 Updated VS Code settings"
echo "🧪 Testing connection..."

# Test the connection
python3 test_anki_connection.py

if [ $? -eq 0 ]; then
    echo "🎉 Connection successful! You can now create Anki cards from VS Code!"
else
    echo "❌ Connection failed. Please check:"
    echo "   1. Anki is running on your local machine"
    echo "   2. AnkiConnect addon is installed"
    echo "   3. Environment variable ANKICONNECT_BIND_ADDRESS=0.0.0.0 is set"
    echo "   4. Your local IP address is correct"
fi
