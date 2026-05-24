#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Temporary local admin API for Linux server inspection, command execution,
and interactive terminal sessions over HTTP.

CLI usage:
    python3 admin_api.py
    python3 admin_api.py --help
    python3 admin_api.py --help-ai
"""

import argparse
import atexit
import getpass
import http.server
import json
import os
import pty
import select
import signal
import socket
import subprocess
import threading
import time
import urllib.parse
import uuid

PORT = 8889
SUDO_PASS = ""
SESSIONS = {}
SESSIONS_LOCK = threading.Lock()
MAX_READ_BYTES = 256 * 1024


USER_HELP_TEXT = """admin_api.py - Temporary local admin HTTP API

Usage:
  python3 admin_api.py
  python3 admin_api.py --help
  python3 admin_api.py --help-ai

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

Notes:
  - Keep the terminal open while using the API
  - Press Ctrl+C to stop the service and close the firewall rule
  - Intended for LAN or private environments only
"""

AI_HELP_TEXT = """AI usage guide for admin_api.py

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

TERMINAL_HTML = r"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Admin API Terminal</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: sans-serif; margin: 20px; background: #111; color: #eee; }
    input, button, textarea { font: inherit; }
    textarea {
      width: 100%;
      height: 360px;
      background: #000;
      color: #0f0;
      border: 1px solid #444;
      padding: 12px;
      resize: vertical;
    }
    .row { margin-bottom: 12px; }
    input[type=text] {
      width: 100%;
      padding: 10px;
      border: 1px solid #555;
      background: #1d1d1d;
      color: #fff;
    }
    button {
      padding: 10px 16px;
      border: 1px solid #666;
      background: #222;
      color: #fff;
      cursor: pointer;
      margin-right: 8px;
    }
    .muted { color: #aaa; }
  </style>
</head>
<body>
  <h1>Admin API Terminal</h1>
  <p class="muted">Start a command, watch server output, and send replies to prompts.</p>

  <div class="row">
    <label>Command</label>
    <input id="cmd" type="text" placeholder="bash, python3 script.py, etc.">
  </div>

  <div class="row">
    <button onclick="startSession()">Start session</button>
    <button onclick="stopSession()">Stop session</button>
  </div>

  <div class="row">
    <label>Output</label>
    <textarea id="output" readonly></textarea>
  </div>

  <div class="row">
    <label>Input to running session</label>
    <input id="userInput" type="text" placeholder="Type reply and press Send">
  </div>

  <div class="row">
    <button onclick="sendInput()">Send</button>
  </div>

  <script>
    let sessionId = null;
    let pollTimer = null;

    async function startSession() {
      const cmd = document.getElementById('cmd').value.trim();
      if (!cmd) return alert('Enter a command');
      const res = await fetch('/session/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({cmd})
      });
      const data = await res.json();
      if (!data.success) return alert(data.error || 'Failed to start session');
      sessionId = data.session_id;
      document.getElementById('output').value = '';
      pollTimer = setInterval(fetchOutput, 1000);
    }

    async function fetchOutput() {
      if (!sessionId) return;
      const res = await fetch('/session/output?session_id=' + encodeURIComponent(sessionId));
      const data = await res.json();
      if (data.output !== undefined) {
        document.getElementById('output').value = data.output;
        document.getElementById('output').scrollTop = document.getElementById('output').scrollHeight;
      }
    }

    async function sendInput() {
      if (!sessionId) return alert('No active session');
      const input = document.getElementById('userInput').value;
      const res = await fetch('/session/send', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: sessionId, input})
      });
      const data = await res.json();
      if (!data.success) alert(data.message || 'Send failed');
      document.getElementById('userInput').value = '';
      fetchOutput();
    }

    async function stopSession() {
      if (!sessionId) return;
      await fetch('/session/stop', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({session_id: sessionId})
      });
      clearInterval(pollTimer);
      pollTimer = null;
      sessionId = null;
    }
  </script>
</body>
</html>
"""


def get_local_ips():
    ips = set(["127.0.0.1"])
    try:
        hostname = socket.gethostname()
        for item in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = item[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except Exception:
        pass
    return sorted(ips)


def verify_sudo_password(password: str) -> bool:
    """Verify sudo password by running a harmless privileged command."""
    result = subprocess.run(
        f"echo {password} | sudo -S -k true",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=15,
    )
    return result.returncode == 0


def prompt_required_sudo_password() -> str:
    """Prompt until a valid non-empty sudo password is provided."""
    while True:
        try:
            password = getpass.getpass(
                "Enter sudo password (required for UFW port open/close): "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[!] Sudo password is required. Exiting.")
            raise SystemExit(1) from None

        if not password:
            print("[!] Sudo password cannot be empty.")
            continue

        print("[+] Verifying sudo password...")
        if verify_sudo_password(password):
            print("[+] Sudo password accepted.")
            return password

        print("[!] Invalid sudo password. Try again.")


def get_listening_service_on_port(port: int) -> str:
    """Return human-readable process/service info listening on port, or empty string."""
    result = subprocess.run(
        f"echo {SUDO_PASS} | sudo -S ss -tlnp 'sport = :{port}' 2>/dev/null",
        shell=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0 or not result.stdout.strip():
        fallback = subprocess.run(
            f"echo {SUDO_PASS} | sudo -S lsof -iTCP:{port} -sTCP:LISTEN -P -n 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if fallback.returncode == 0 and fallback.stdout.strip():
            first_line = fallback.stdout.strip().splitlines()[0]
            return first_line
        return "unknown process"

    for line in result.stdout.splitlines():
        if f":{port}" not in line:
            continue
        if "users:" in line:
            start = line.find('(("') + 3
            end = line.find('"', start)
            if start >= 3 and end > start:
                process_name = line[start:end]
                pid_start = line.find("pid=", end)
                if pid_start != -1:
                    pid_end = line.find(",", pid_start)
                    if pid_end == -1:
                        pid_end = line.find(")", pid_start)
                    pid_value = line[pid_start + 4 : pid_end]
                    return f"{process_name} (pid={pid_value})"
                return process_name
        return line.strip()
    return "unknown process"


def is_port_in_use(port: int) -> bool:
    """Return True if another process is already bound to the TCP port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("0.0.0.0", port))
            return False
        except OSError:
            return True


def verify_firewall_port_open(port: int) -> bool:
    """Return True if UFW reports the TCP port as allowed."""
    result = subprocess.run(
        f"echo {SUDO_PASS} | sudo -S ufw status 2>/dev/null",
        shell=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    if result.returncode != 0:
        return False
    needle = f"{port}/tcp"
    for line in result.stdout.splitlines():
        if needle in line and "ALLOW" in line.upper():
            return True
    return False


def open_firewall_port() -> None:
    """Open PORT in UFW; exit if the rule cannot be confirmed."""
    print(f"[+] Opening TCP port {PORT} in UFW...")
    result = subprocess.run(
        f"echo {SUDO_PASS} | sudo -S ufw allow {PORT}/tcp",
        shell=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if result.returncode != 0:
        print("[!] Failed to add UFW rule. Service cannot run without an open port.")
        if result.stderr.strip():
            print(f"[!] {result.stderr.strip()}")
        raise SystemExit(1)

    if not verify_firewall_port_open(PORT):
        print(f"[!] UFW rule for port {PORT}/tcp was not confirmed. Exiting.")
        raise SystemExit(1)

    print(f"[+] Port {PORT}/tcp is open in UFW.")


def cleanup():
    print(f"\n[+] Closing port {PORT} and removing firewall rule...")
    subprocess.run(
        f"echo {SUDO_PASS} | sudo -S ufw delete allow {PORT}/tcp",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("[!] Port closed successfully.")


atexit.register(cleanup)


def safe_read_text_file(file_path, max_bytes=MAX_READ_BYTES):
    try:
        abs_path = os.path.abspath(os.path.expanduser(file_path))

        if not os.path.exists(abs_path):
            return {
                "success": False,
                "error": "file not found",
                "path": abs_path,
            }

        if not os.path.isfile(abs_path):
            return {
                "success": False,
                "error": "path is not a regular file",
                "path": abs_path,
            }

        size = os.path.getsize(abs_path)
        with open(abs_path, "rb") as f:
            raw = f.read(max_bytes + 1)

        truncated = len(raw) > max_bytes
        if truncated:
            raw = raw[:max_bytes]

        try:
            content = raw.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            content = raw.decode("utf-8", errors="replace")
            encoding = "utf-8-replaced"

        return {
            "success": True,
            "path": abs_path,
            "size": size,
            "encoding": encoding,
            "truncated": truncated,
            "max_bytes": max_bytes,
            "content": content,
        }

    except Exception as exc:
        return {
            "success": False,
            "error": str(exc),
            "path": file_path,
        }


class InteractiveSession:
    def __init__(self, cmd):
        self.session_id = str(uuid.uuid4())
        self.cmd = cmd
        self.output = ""
        self.running = True
        self.master_fd = None
        self.pid = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        try:
            pid, master_fd = pty.fork()
            if pid == 0:
                os.execl("/bin/sh", "/bin/sh", "-c", self.cmd)
            else:
                self.pid = pid
                self.master_fd = master_fd

                while self.running:
                    rlist, _, _ = select.select([master_fd], [], [], 0.2)
                    if master_fd in rlist:
                        try:
                            data = os.read(master_fd, 4096)
                            if not data:
                                break
                            with self.lock:
                                self.output += data.decode(errors="replace")
                        except OSError:
                            break

                    try:
                        finished_pid, _ = os.waitpid(pid, os.WNOHANG)
                        if finished_pid != 0:
                            break
                    except ChildProcessError:
                        break

        finally:
            self.running = False
            if self.master_fd is not None:
                try:
                    os.close(self.master_fd)
                except OSError:
                    pass

    def send(self, text):
        if not self.running or self.master_fd is None:
            return False, "Session is not running"
        try:
            os.write(self.master_fd, (text + "\n").encode())
            return True, "Input sent"
        except Exception as exc:
            return False, str(exc)

    def stop(self):
        self.running = False
        if self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError:
                pass

    def snapshot(self):
        with self.lock:
            return {
                "success": True,
                "session_id": self.session_id,
                "cmd": self.cmd,
                "running": self.running,
                "output": self.output,
            }


class AdminHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[HTTP] {self.address_string()} - {fmt % args}")

    def send_json(self, status, data):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, status, html_text):
        body = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def run_command(self, cmd_str):
        try:
            result = subprocess.run(
                cmd_str,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "timeout after 30s"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def _parse_json_body(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b"{}"
        try:
            return True, json.loads(body)
        except Exception:
            return False, {"error": "Invalid JSON format"}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        path = parsed.path.lstrip("/")

        if path in ("", "help"):
            self.send_json(200, {
                "status": "running",
                "mode": "educational (no_token)",
                "port": PORT,
                "purpose": "Temporary local admin API for server inspection, command execution, file reading, and interactive terminal access.",
                "cli_help": "python3 admin_api.py --help",
                "ai_help": "python3 admin_api.py --help-ai",
                "terminal_ui": "/terminal",
                "examples": {
                    "run": "/run?cmd=uname%20-a",
                    "read": "/read?path=/home/ash/3x-ui/admin_api.py",
                    "ls": "/ls?path=/home/ash/3x-ui",
                    "find": "/find?path=/home/ash&name=admin_api.py&depth=4"
                },
                "endpoints": [
                    "/help",
                    "/run?cmd=",
                    "/run",
                    "/read?path=",
                    "/ls?path=",
                    "/find?path=&name=&depth=",
                    "/terminal",
                    "/session/start",
                    "/session/send",
                    "/session/output?session_id=",
                    "/session/stop"
                ],
                "response_format": {
                    "success": True,
                    "stdout": "command output",
                    "stderr": "error output",
                    "exit_code": 0
                }
            })
            return

        if path == "terminal":
            self.send_html(200, TERMINAL_HTML)
            return

        if path == "session/output":
            session_id = params.get("session_id", [None])[0]
            if not session_id:
                self.send_json(400, {"success": False, "error": "Parameter session_id is required"})
                return

            with SESSIONS_LOCK:
                session = SESSIONS.get(session_id)

            if not session:
                self.send_json(404, {"success": False, "error": "Session not found"})
                return

            self.send_json(200, session.snapshot())
            return

        if path == "run":
            cmd = params.get("cmd", [None])[0]
            if not cmd:
                self.send_json(400, {"error": "Parameter 'cmd' is required"})
                return
            self.send_json(200, self.run_command(cmd))
            return

        if path == "read":
            file_path = params.get("path", [None])[0]
            if not file_path:
                self.send_json(400, {"error": "Parameter 'path' is required"})
                return

            res = safe_read_text_file(file_path)
            self.send_json(200 if res.get("success") else 404, res)
            return

        if path == "ls":
            dir_path = params.get("path", ["/"])[0]
            res = self.run_command(f"ls -la '{dir_path}'")
            res["path"] = dir_path
            self.send_json(200, res)
            return

        if path == "find":
            search_path = params.get("path", ["/"])[0]
            name = params.get("name", ["*"])[0]
            depth = params.get("depth", ["5"])[0]
            cmd = f"find '{search_path}' -maxdepth {depth} -name '{name}' 2>/dev/null"
            res = self.run_command(cmd)
            res["search_path"] = search_path
            res["name"] = name
            res["depth"] = depth
            self.send_json(200, res)
            return

        self.send_json(404, {"error": "Path not found"})

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.lstrip("/")

        if path == "run":
            ok, data = self._parse_json_body()
            if not ok:
                self.send_json(400, data)
                return

            cmd = data.get("cmd", "")
            if cmd:
                self.send_json(200, self.run_command(cmd))
            else:
                self.send_json(400, {"error": "Field 'cmd' is required"})
            return

        if path == "session/start":
            ok, data = self._parse_json_body()
            if not ok:
                self.send_json(400, data)
                return

            cmd = data.get("cmd", "").strip()
            if not cmd:
                self.send_json(400, {"success": False, "error": "Field cmd is required"})
                return

            session = InteractiveSession(cmd)
            with SESSIONS_LOCK:
                SESSIONS[session.session_id] = session

            self.send_json(200, {
                "success": True,
                "session_id": session.session_id,
                "cmd": cmd
            })
            return

        if path == "session/send":
            ok, data = self._parse_json_body()
            if not ok:
                self.send_json(400, data)
                return

            session_id = data.get("session_id", "")
            user_input = data.get("input", "")

            with SESSIONS_LOCK:
                session = SESSIONS.get(session_id)

            if not session:
                self.send_json(404, {"success": False, "error": "Session not found"})
                return

            success, message = session.send(user_input)
            self.send_json(200 if success else 400, {"success": success, "message": message})
            return

        if path == "session/stop":
            ok, data = self._parse_json_body()
            if not ok:
                self.send_json(400, data)
                return

            session_id = data.get("session_id", "")
            with SESSIONS_LOCK:
                session = SESSIONS.get(session_id)

            if not session:
                self.send_json(404, {"success": False, "error": "Session not found"})
                return

            session.stop()
            with SESSIONS_LOCK:
                SESSIONS.pop(session_id, None)

            self.send_json(200, {"success": True, "message": "Session stopped"})
            return

        self.send_json(404, {"error": "Path not found"})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def prompt_port_number(default: int = 8889) -> int:
    """Read a single port number from stdin; re-prompt on invalid input."""
    while True:
        raw = input(f"Enter port to open and listen on [{default}]: ").strip()
        if not raw:
            return default
        try:
            port = int(raw)
            if 1 <= port <= 65535:
                return port
        except ValueError:
            pass
        print("[!] Invalid port. Enter a number between 1 and 65535.")


def prompt_available_port(default: int = 8889) -> int:
    """Prompt until a port is free (not already bound by another service)."""
    while True:
        port = prompt_port_number(default)
        if not is_port_in_use(port):
            return port

        service_name = get_listening_service_on_port(port)
        print(f"[!] Port {port} is already in use.")
        if service_name:
            print(f"[!] Running service: {service_name}")
        print("[!] Choose another port.")


def print_startup_banner(access_ips):
    print("=" * 72)
    print("Server Admin API - Educational Mode (No Token)")
    print("=" * 72)
    print(f"Port         : {PORT}")
    print("CLI Help     : python3 admin_api.py --help")
    print("AI Help      : python3 admin_api.py --help-ai")
    print("HTTP Help    : /help")
    print("Terminal UI  : /terminal")
    print("Access URLs:")
    if access_ips:
        for ip in access_ips:
            print(f"  http://{ip}:{PORT}/help")
            print(f"  http://{ip}:{PORT}/terminal")
    else:
        print(f"  http://127.0.0.1:{PORT}/help")
        print(f"  http://127.0.0.1:{PORT}/terminal")
    print("Notes        : Keep this terminal open. Press Ctrl+C to stop.")
    print("=" * 72)


def main():
    global PORT, SUDO_PASS

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--help-ai", action="store_true")
    parser.add_argument("--help", action="store_true")
    args, _ = parser.parse_known_args()

    if args.help:
        print(USER_HELP_TEXT)
        return

    if args.help_ai:
        print(AI_HELP_TEXT)
        return

    SUDO_PASS = prompt_required_sudo_password()
    PORT = prompt_available_port(PORT)
    open_firewall_port()

    access_ips = get_local_ips()
    print_startup_banner(access_ips)

    server = http.server.ThreadingHTTPServer(("0.0.0.0", PORT), AdminHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()