#!/bin/bash

echo "🔍 AnkiConnect Connection Diagnostics"
echo "====================================="

echo ""
echo "1. Testing localhost connection (will fail - this is expected):"
curl -s -X POST http://127.0.0.1:8765 -d '{"action": "version", "version": 6}' -H "Content-Type: application/json" || echo "❌ localhost:8765 - Connection refused (expected)"

curl -s -X POST http://127.0.0.1:8766 -d '{"action": "version", "version": 6}' -H "Content-Type: application/json" || echo "❌ localhost:8766 - Connection refused (expected)"

echo ""
echo "2. Current environment:"
echo "   - Running in: GitHub Codespace (Linux container)"
echo "   - AnkiConnect location: Your local machine"
echo "   - Network isolation: Container cannot reach your local machine directly"

echo ""
echo "3. Available solutions:"
echo "   A) Port forwarding (VS Code Ports tab)"
echo "   B) Use your local machine's IP address"
echo "   C) Work locally instead of in Codespace"

echo ""
echo "4. VS Code Port Forwarding check:"
echo "   - Look for 'Ports' tab at bottom of VS Code"
echo "   - Add port 8765 or 8766 (whichever AnkiConnect uses)"
echo "   - Get the forwarded URL and test with that"

echo ""
echo "🎯 What we need to know:"
echo "   1. What port is AnkiConnect actually running on? (8765 or 8766?)"
echo "   2. Can you see the VS Code 'Ports' tab?"
echo "   3. Do you want to try port forwarding or work locally?"