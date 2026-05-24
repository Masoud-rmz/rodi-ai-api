#!/usr/bin/env bash
# basic_usage.sh --- common curl examples for rodi_admin
# Replace SERVER_IP and PORT with your actual values.

SERVER="http://192.168.1.100:8889"

# Check server status
curl "$SERVER/help"

# Run a shell command
curl "$SERVER/run?cmd=uname%20-a"

# Run a command via POST
curl -X POST "$SERVER/run" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "df -h"}'

# Read a file
curl "$SERVER/read?path=/etc/hostname"

# List a directory
curl "$SERVER/ls?path=/home"

# Find files
curl "$SERVER/find?path=/etc&name=*.conf&depth=2"

# Start an interactive session
SESSION=$(curl -s -X POST "$SERVER/session/start" \
  -H "Content-Type: application/json" \
  -d '{"cmd": "bash"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['session_id'])")

echo "Session ID: $SESSION"

# Poll output
sleep 0.5
curl "$SERVER/session/output?session_id=$SESSION"

# Send input
curl -X POST "$SERVER/session/send" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION\", \"input\": \"ls -la\"}"

# Stop session
curl -X POST "$SERVER/session/stop" \
  -H "Content-Type: application/json" \
  -d "{\"session_id\": \"$SESSION\"}"
