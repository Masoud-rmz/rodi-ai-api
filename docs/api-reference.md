# API Reference

Base URL: `http://SERVER_IP:PORT`

All responses are JSON unless noted. All endpoints include `Access-Control-Allow-Origin: *`.

---

## GET /help

Returns server status and endpoint list.

**Response**
```json
{
  "status": "running",
  "version": "1.0.0",
  "port": 8889,
  "purpose": "...",
  "endpoints": [...]
}
```

---

## GET /run?cmd=COMMAND

Execute a shell command.

| Parameter | Required | Description |
|---|---|---|
| `cmd` | Yes | Shell command string |

**Response**
```json
{"success": true, "stdout": "hello\n", "stderr": "", "exit_code": 0}
```

**Error (400)** — missing cmd parameter.

---

## POST /run

Execute a shell command via JSON body.

**Body**
```json
{"cmd": "uname -a"}
```

**Response** — same as GET /run.

---

## GET /read?path=FILE_PATH

Read a text file.

| Parameter | Required | Description |
|---|---|---|
| `path` | Yes | Absolute or relative file path |

**Response**
```json
{
  "success": true,
  "path": "/etc/hostname",
  "size": 12,
  "encoding": "utf-8",
  "truncated": false,
  "max_bytes": 262144,
  "content": "myserver\n"
}
```

**Error (404)** — file not found.

---

## GET /ls?path=DIR_PATH

List directory contents (output of `ls -la`).

**Response**
```json
{"success": true, "stdout": "total 12\n...", "path": "/home"}
```

---

## GET /find?path=P&name=N&depth=D

Search for files by name pattern.

| Parameter | Required | Default | Description |
|---|---|---|---|
| `path` | No | `/` | Search root |
| `name` | No | `*` | Name pattern (shell glob) |
| `depth` | No | `5` | Max directory depth |

---

## GET /terminal

Returns browser-based terminal UI (HTML page).

---

## POST /session/start

Start an interactive PTY session.

**Body**
```json
{"cmd": "python3 script.py"}
```

**Response**
```json
{"success": true, "session_id": "uuid", "cmd": "python3 script.py"}
```

---

## GET /session/output?session_id=ID

Poll output from a running session.

**Response**
```json
{"success": true, "session_id": "uuid", "cmd": "bash", "running": true, "output": "$ "}
```

---

## POST /session/send

Send text input to a running session.

**Body**
```json
{"session_id": "uuid", "input": "ls -la"}
```

---

## POST /session/stop

Stop and remove a session.

**Body**
```json
{"session_id": "uuid"}
```

**Response**
```json
{"success": true, "message": "Session stopped"}
```
