#!/bin/bash

# Automated Anki Connection Setup for Codespace
echo "🚀 Setting up Anki connection from Codespace..."

# Function to detect local network IP ranges
get_likely_local_ip() {
    echo "💡 Your local machine is likely on one of these IP ranges:"
    echo "   • 192.168.1.x (most home routers)"
    echo "   • 192.168.0.x (some home routers)" 
    echo "   • 10.0.0.x (some networks)"
    echo "   • 172.16.x.x to 172.31.x.x (some networks)"
    echo ""
    echo "📍 To find your exact IP:"
    echo "   Windows: ipconfig | findstr 'IPv4'"
    echo "   Mac:     ifconfig | grep 'inet ' | grep -v 127.0.0.1"
    echo "   Linux:   hostname -I"
}

# Install ngrok for tunneling
install_ngrok() {
    echo "📦 Installing ngrok for tunneling..."
    
    # Download and install ngrok
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
    tar xzf ngrok-v3-stable-linux-amd64.tgz
    chmod +x ngrok
    rm ngrok-v3-stable-linux-amd64.tgz
    
    echo "✅ ngrok installed"
}

# Set up tunnel configuration
setup_tunnel() {
    echo "🌐 Setting up tunnel configuration..."
    
    cat > start_tunnel.sh << 'EOF'
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
EOF

    chmod +x start_tunnel.sh
    echo "✅ Tunnel script created"
}

# Create Windows batch file for easier setup
create_windows_helper() {
    cat > setup_anki_windows.bat << 'EOF'
@echo off
echo Setting up Anki for remote access...
echo.

echo Setting environment variable...
set ANKICONNECT_BIND_ADDRESS=0.0.0.0

echo.
echo Environment variable set. Now starting Anki...
echo Keep this window open while using the Codespace integration.
echo.

REM Try to find and start Anki
if exist "C:\Program Files\Anki\anki.exe" (
    start "Anki" "C:\Program Files\Anki\anki.exe"
) else if exist "C:\Program Files (x86)\Anki\anki.exe" (
    start "Anki" "C:\Program Files (x86)\Anki\anki.exe"
) else (
    echo Could not find Anki automatically.
    echo Please start Anki manually from this command prompt window.
    echo.
)

echo.
echo Find your IP address with: ipconfig | findstr "IPv4"
ipconfig | findstr "IPv4"

echo.
echo Use the IP address shown above in your Codespace setup.
pause
EOF

    echo "✅ Windows helper script created"
}

# Main execution
main() {
    get_likely_local_ip
    setup_tunnel
    create_windows_helper
    
    echo ""
    echo "🎯 NEXT STEPS:"
    echo "=============="
    echo ""
    echo "📍 ON YOUR LOCAL MACHINE:"
    echo "   Windows: Run 'setup_anki_windows.bat' (I created this for you)"
    echo "   Mac/Linux: Run these commands:"
    echo "     export ANKICONNECT_BIND_ADDRESS=0.0.0.0"
    echo "     # Then start Anki from the same terminal"
    echo ""
    echo "📍 IN THIS CODESPACE:"
    echo "   Run: ./start_tunnel.sh"
    echo "   Enter your local IP when prompted"
    echo ""
    echo "🎉 Then you'll be able to create Anki cards directly from VS Code!"
}

# Run the setup
main