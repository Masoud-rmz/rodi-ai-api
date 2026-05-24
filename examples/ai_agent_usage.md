# AI Agent Usage Guide

This guide is written for AI coding agents (Cursor, Claude, Copilot, etc.) operating a server via `rodi_admin`.

## Quick Start

Once the user has started `python3 -m rodi_admin` on the server, you can:

```
Base URL: http://SERVER_IP:PORT
Auth: none
```

Start by fetching `/help` to confirm the service is running.

---

## Running Commands

```http
GET /run?cmd=uname%20-a
```

Or via POST:

```http
POST /run
Content-Type: application/json

{"cmd": "systemctl status nginx"}
```

Response:
```json
{"success": true, "stdout": "...", "stderr": "", "exit_code": 0}
```

---

## Reading Files

```http
GET /read?path=/etc/nginx/nginx.conf
```

Response includes `content`, `size`, `truncated` flag.

---

## Interactive Sessions

Use sessions for commands that prompt for input (e.g., installers, Python scripts).

**Step 1 — Start**
```http
POST /session/start
{"cmd": "python3 /home/user/setup.py"}
```
Save the `session_id` from the response.

**Step 2 — Poll output**
```http
GET /session/output?session_id=UUID
```
Check `output` field for prompts. Check `running` field to know if still active.

**Step 3 — Send reply**
```http
POST /session/send
{"session_id": "UUID", "input": "yes"}
```

**Step 4 — Stop when done**
```http
POST /session/stop
{"session_id": "UUID"}
```

---

## Tips for AI Agents

- Always check `/help` first to confirm the server is reachable
- Use `/run` for quick one-shot commands
- Use `/session/*` for interactive or long-running commands
- Poll `/session/output` every 1–2 seconds to detect prompts
- Always stop sessions when done to free resources
- The service is **temporary** — it stops when the user closes the terminal
