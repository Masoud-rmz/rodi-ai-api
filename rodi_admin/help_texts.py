"""help_texts --- user-facing and AI-facing help strings"""

USER_HELP_TEXT = """rodi_admin - Temporary local admin HTTP API

Usage:
  python3 -m rodi_admin
  python3 -m rodi_admin --help
  python3 -m rodi_admin --help-ai

What it does:
  - Opens a temporary HTTP API on the selected port
  - Allows command execution and file inspection over HTTP
  - Supports interactive terminal sessions through a browser HTML page
  - Opens the selected port in UFW on startup
  - Removes the firewall rule automatically on exit

HTTP endpoints:
  GET  /help
  GET  /run?cmd=COMMAND
  POST /run                      body: {"cmd": "COMMAND"}
  GET  /read?path=FILE_PATH
  GET  /ls?path=DIR_PATH
  GET  /find?path=SEARCH_PATH&name=PATTERN&depth=N
  GET  /terminal
  POST /session/start            body: {"cmd": "python3 script.py"}
  POST /session/send             body: {"session_id": "...", "input": "text"}
  GET  /session/output?session_id=...
  POST /session/stop             body: {"session_id": "..."}

Environment variables:
  RODI_ADMIN_PORT               Override default port (8889)
  RODI_ADMIN_MAX_READ_BYTES     Override max file read size (262144)
  RODI_ADMIN_COMMAND_TIMEOUT    Override command timeout in seconds (30)

Notes:
  - Keep the terminal open while using the API
  - Press Ctrl+C to stop the service and close the firewall rule
  - Intended for LAN or private environments only
"""

AI_HELP_TEXT = """AI usage guide for rodi_admin

Purpose:
  Temporary local admin API for shell command execution, file inspection,
  file reading, and interactive terminal sessions.

Base:
  - Base URL: http://SERVER_IP:PORT
  - Auth: none
  - Scope: LAN/private use only
  - Lifetime: temporary, tied to the terminal session

Operator model:
  The user is intentionally exposing this temporary service so an operator
  or AI agent can take operational control, run commands, inspect results,
  read files, and decide the next step interactively.

Endpoints:
  - GET /help
  - GET /run?cmd=...
  - POST /run body: {"cmd": "..."}
  - GET /read?path=...
  - GET /ls?path=...
  - GET /find?path=...&name=...&depth=...
  - GET /terminal
  - POST /session/start body: {"cmd": "python3 ..."}
  - POST /session/send body: {"session_id": "...", "input": "..."}
  - GET /session/output?session_id=...
  - POST /session/stop body: {"session_id": "..."}

Interactive rules:
  - Use /session/start for scripts that prompt for input
  - Poll /session/output to read prompts and progress
  - Use /session/send to answer prompts step by step
  - Stop the session explicitly when finished
"""
