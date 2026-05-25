"""http_server --- AdminHandler routing and threaded HTTP server setup"""

import http.server
import json
import socket
import urllib.parse
from socketserver import ThreadingMixIn

from rodi_admin import __version__
from rodi_admin.config import (
    CLIENT_READ_TIMEOUT_SECONDS,
    COMMAND_TIMEOUT_SECONDS,
    MAX_READ_BYTES,
    PORT,
)
from rodi_admin.features.command_execution import handle_run_get, handle_run_post
from rodi_admin.features.file_inspection import (
    handle_find_get,
    handle_ls_get,
    handle_read_get,
)
from rodi_admin.features.interactive_session import (
    handle_session_output_get,
    handle_session_send_post,
    handle_session_start_post,
    handle_session_stop_post,
)
from rodi_admin.features.terminal import get_terminal_html


class RodiAdminThreadingServer(ThreadingMixIn, http.server.HTTPServer):
    """HTTP server that handles each request on a separate daemon thread."""

    daemon_threads = True
    allow_reuse_address = True


def create_admin_server(host: str, port: int) -> RodiAdminThreadingServer:
    """Create a threading HTTP server bound to host:port.

    Args:
        host: Bind address (e.g. 0.0.0.0).
        port: TCP port number.

    Returns:
        Configured server instance (not started).
    """
    return RodiAdminThreadingServer((host, port), AdminHandler)


def _client_read_timeout_payload() -> dict:
    """Build JSON payload for HTTP 408 when the client read times out."""
    return {
        "success": False,
        "code": "CLIENT_READ_TIMEOUT",
        "message": (
            f"Client did not complete the request within "
            f"{CLIENT_READ_TIMEOUT_SECONDS} seconds."
        ),
        "help_url": "/help",
    }


def _build_help_payload(listen_port: int) -> dict:
    """Build the GET /help response body."""
    return {
        "status": "running",
        "version": __version__,
        "port": listen_port,
        "purpose": (
            "Temporary local admin API for server inspection, "
            "command execution, file reading, and interactive terminal access."
        ),
        "cli_help": "python3 -m rodi_admin --help",
        "ai_help": "python3 -m rodi_admin --help-ai",
        "terminal_ui": "/terminal",
        "timeouts": {
            "client_read_timeout_seconds": CLIENT_READ_TIMEOUT_SECONDS,
            "command_timeout_seconds": COMMAND_TIMEOUT_SECONDS,
        },
        "env_vars": [
            "RODI_ADMIN_PORT",
            "RODI_ADMIN_CLIENT_READ_TIMEOUT",
            "RODI_ADMIN_COMMAND_TIMEOUT",
            "RODI_ADMIN_MAX_READ_BYTES",
        ],
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
            "/session/stop",
        ],
        "limits": {
            "max_read_bytes": MAX_READ_BYTES,
        },
    }


class AdminHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler — routes all endpoints to feature modules."""

    server_version = "RodiAdmin/1.0"

    def log_message(self, fmt: str, *args) -> None:
        command = getattr(self, "command", "-")
        path = getattr(self, "path", "-")
        print(f"[HTTP] {self.address_string()} - {command} {path} - {fmt % args}")

    def send_early_json(self, status: int, data: dict, reason: str = "Request Timeout") -> None:
        """Write JSON response before the HTTP request line has been parsed."""
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        header_block = (
            f"HTTP/1.0 {status} {reason}\r\n"
            "Content-Type: application/json; charset=utf-8\r\n"
            "Access-Control-Allow-Origin: *\r\n"
            "Access-Control-Allow-Headers: Content-Type\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        )
        self.wfile.write(header_block.encode("ascii") + body)

    def log_request(self, code: str = "-", size: str = "-") -> None:
        """Skip access log when the request line was never parsed."""
        if not getattr(self, "requestline", None):
            return
        super().log_request(code, size)

    def log_error(self, format: str, *args) -> None:
        """Return 408 when stdlib request read times out (Python 3.13+)."""
        if "timed out" in format.lower():
            try:
                self.send_early_json(408, _client_read_timeout_payload())
            except OSError:
                pass
            return
        print(f"[HTTP] ERROR {format % args}")

    def setup(self) -> None:
        """Apply client read timeout so idle connections cannot block a worker thread."""
        super().setup()
        self.connection.settimeout(CLIENT_READ_TIMEOUT_SECONDS)

    def handle(self) -> None:
        """Handle requests; return 408 when the client read times out."""
        try:
            super().handle()
        except (TimeoutError, socket.timeout):
            try:
                self.send_early_json(408, _client_read_timeout_payload())
            except OSError:
                pass
            try:
                self.connection.close()
            except OSError:
                pass

    def send_json(self, status: int, data: dict) -> None:
        """Serialise data as JSON and write the HTTP response.

        Args:
            status: HTTP status code.
            data: Response payload dict.
        """
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, status: int, html_text: str) -> None:
        """Write an HTML response.

        Args:
            status: HTTP status code.
            html_text: HTML string to send.
        """
        body = html_text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)

    def _parse_json_body(self) -> tuple[bool, dict]:
        """Read and parse the JSON request body.

        Returns:
            Tuple of (success_bool, parsed_dict_or_error_dict).
        """
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return True, json.loads(raw)
        except Exception:
            return False, {"error": "Invalid JSON format"}

    def do_GET(self) -> None:
        """Route all GET requests to the appropriate feature handler."""
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        path = parsed.path.lstrip("/")

        if path in ("", "help"):
            listen_port = int(self.server.server_address[1])
            self.send_json(200, _build_help_payload(listen_port))
            return

        if path == "terminal":
            self.send_html(200, get_terminal_html())
            return

        if path == "session/output":
            status, response = handle_session_output_get(params)
            self.send_json(status, response)
            return

        if path == "run":
            status, response = handle_run_get(params)
            self.send_json(status, response)
            return

        if path == "read":
            status, response = handle_read_get(params)
            self.send_json(status, response)
            return

        if path == "ls":
            status, response = handle_ls_get(params)
            self.send_json(status, response)
            return

        if path == "find":
            status, response = handle_find_get(params)
            self.send_json(status, response)
            return

        self.send_json(404, {"error": "Path not found"})

    def do_POST(self) -> None:
        """Route all POST requests to the appropriate feature handler."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.lstrip("/")

        ok, body = self._parse_json_body()
        if not ok:
            self.send_json(400, body)
            return

        if path == "run":
            status, response = handle_run_post(body)
            self.send_json(status, response)
            return

        if path == "session/start":
            status, response = handle_session_start_post(body)
            self.send_json(status, response)
            return

        if path == "session/send":
            status, response = handle_session_send_post(body)
            self.send_json(status, response)
            return

        if path == "session/stop":
            status, response = handle_session_stop_post(body)
            self.send_json(status, response)
            return

        self.send_json(404, {"error": "Path not found"})

    def do_OPTIONS(self) -> None:
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_server(port: int, sudo_password: str) -> None:
    """Create and run the ThreadingHTTPServer until KeyboardInterrupt.

    Args:
        port: TCP port to bind to.
        sudo_password: Used only to set up atexit cleanup for firewall.
    """
    import atexit
    from rodi_admin.features.firewall import cleanup_firewall_port

    atexit.register(cleanup_firewall_port, port, sudo_password)

    server = create_admin_server("0.0.0.0", port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user.")
    finally:
        server.server_close()
