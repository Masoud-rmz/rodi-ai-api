"""Tests for threaded server and client read timeout (disabled unless RODI_SMOKE_TEST=1)."""

import json
import os
import socket
import threading
import unittest
from unittest.mock import MagicMock, patch

import pytest

from rodi_admin.config import CLIENT_READ_TIMEOUT_SECONDS
from rodi_admin.features.http_server import (
    AdminHandler,
    RodiAdminThreadingServer,
    create_admin_server,
)


@pytest.mark.skipif(os.environ.get("RODI_SMOKE_TEST", "0") != "1", reason="Set RODI_SMOKE_TEST=1")
class TestAdminServerFactory(unittest.TestCase):
    """Unit tests for create_admin_server."""

    def test_create_admin_server_returns_threading_server(self) -> None:
        """Factory builds RodiAdminThreadingServer with daemon threads enabled."""
        server = create_admin_server("127.0.0.1", 0)
        try:
            self.assertIsInstance(server, RodiAdminThreadingServer)
            self.assertTrue(server.daemon_threads)
            self.assertTrue(server.allow_reuse_address)
        finally:
            server.server_close()


@pytest.mark.skipif(os.environ.get("RODI_SMOKE_TEST", "0") != "1", reason="Set RODI_SMOKE_TEST=1")
class TestAdminHandlerClientTimeout(unittest.TestCase):
    """Unit tests for AdminHandler socket timeout behavior."""

    def test_setup_sets_client_read_timeout_on_socket(self) -> None:
        """setup() applies CLIENT_READ_TIMEOUT_SECONDS to the connection socket."""
        handler = AdminHandler.__new__(AdminHandler)
        handler.connection = MagicMock()
        with patch("http.server.BaseHTTPRequestHandler.setup") as mock_super_setup:
            handler.setup()
        mock_super_setup.assert_called_once()
        handler.connection.settimeout.assert_called_once_with(CLIENT_READ_TIMEOUT_SECONDS)

    @patch("http.server.BaseHTTPRequestHandler.handle", side_effect=TimeoutError)
    def test_handle_returns_408_on_client_read_timeout(self, _mock_super_handle: MagicMock) -> None:
        """handle() responds with 408 JSON when the client read times out."""
        handler = AdminHandler.__new__(AdminHandler)
        handler.connection = MagicMock()
        handler.wfile = MagicMock()
        with patch.object(handler, "send_early_json") as mock_send_early_json:
            handler.handle()
        mock_send_early_json.assert_called_once()
        self.assertEqual(mock_send_early_json.call_args[0][0], 408)
        self.assertEqual(
            mock_send_early_json.call_args[0][1]["code"],
            "CLIENT_READ_TIMEOUT",
        )
        handler.connection.close.assert_called_once()


@pytest.mark.skipif(os.environ.get("RODI_SMOKE_TEST", "0") != "1", reason="Set RODI_SMOKE_TEST=1")
class TestClientReadTimeoutIntegration(unittest.TestCase):
    """Integration test: idle TCP client triggers timeout on a worker thread."""

    @patch("rodi_admin.features.http_server.CLIENT_READ_TIMEOUT_SECONDS", 1)
    def test_idle_connection_gets_408(self) -> None:
        """Server does not hang when a client connects without sending HTTP."""
        server = create_admin_server("127.0.0.1", 0)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            host, port = server.server_address
            with socket.create_connection((host, port), timeout=5) as client_socket:
                client_socket.settimeout(10)
                response = client_socket.recv(4096)
            self.assertTrue(response, "expected 408 response body from idle connection")
            self.assertIn(b"408", response.split(b"\r\n", 1)[0])
            self.assertIn(b"CLIENT_READ_TIMEOUT", response)
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=5)


@pytest.mark.skipif(os.environ.get("RODI_SMOKE_TEST", "0") != "1", reason="Set RODI_SMOKE_TEST=1")
class TestHelpEndpointTimeouts(unittest.TestCase):
    """GET /help exposes timeout metadata."""

    def test_help_includes_timeout_fields(self) -> None:
        """Help JSON includes client and command timeout seconds."""
        server = create_admin_server("127.0.0.1", 0)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        try:
            import urllib.request

            host, port = server.server_address
            with urllib.request.urlopen(f"http://{host}:{port}/help", timeout=5) as response:
                body = json.loads(response.read())
            self.assertIn("timeouts", body)
            self.assertIn("client_read_timeout_seconds", body["timeouts"])
            self.assertIn("command_timeout_seconds", body["timeouts"])
            self.assertIn("RODI_ADMIN_CLIENT_READ_TIMEOUT", body["env_vars"])
        finally:
            server.shutdown()
            server.server_close()
            server_thread.join(timeout=5)
