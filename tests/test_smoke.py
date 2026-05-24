"""
test_smoke --- import and basic HTTP smoke tests for rodi_admin.

Tests are disabled by default (RODI_SMOKE_TEST=1 to enable).
"""

import os
import sys
import http.server
import threading
import urllib.request
import json
import time

# guard --- skip unless explicitly enabled
SMOKE_TESTS_ENABLED = os.environ.get("RODI_SMOKE_TEST", "0") == "1"

import pytest


@pytest.mark.skipif(not SMOKE_TESTS_ENABLED, reason="Set RODI_SMOKE_TEST=1 to enable")
def test_all_feature_modules_import_without_error():
    """All feature modules must be importable without raising ImportError."""
    import rodi_admin
    import rodi_admin.config
    import rodi_admin.help_texts
    import rodi_admin.features.command_execution
    import rodi_admin.features.file_inspection
    import rodi_admin.features.interactive_session
    import rodi_admin.features.firewall
    import rodi_admin.features.startup
    import rodi_admin.features.terminal
    import rodi_admin.features.http_server


@pytest.mark.skipif(not SMOKE_TESTS_ENABLED, reason="Set RODI_SMOKE_TEST=1 to enable")
def test_help_endpoint_returns_running_status():
    """Start server on a random port, call /help, assert status == 'running'."""
    from rodi_admin.features.http_server import AdminHandler

    # bind on a random free port
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), AdminHandler)
    port = server.server_address[1]

    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()

    try:
        time.sleep(0.1)
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/help", timeout=5) as response:
            body = json.loads(response.read())

        assert body.get("status") == "running", f"Unexpected response: {body}"
    finally:
        server.shutdown()
        server.server_close()


@pytest.mark.skipif(not SMOKE_TESTS_ENABLED, reason="Set RODI_SMOKE_TEST=1 to enable")
def test_run_command_echo():
    """run_command('echo hello') must return success=True and stdout containing 'hello'."""
    from rodi_admin.features.command_execution import run_command

    result = run_command("echo hello")
    assert result["success"] is True
    assert "hello" in result["stdout"]


@pytest.mark.skipif(not SMOKE_TESTS_ENABLED, reason="Set RODI_SMOKE_TEST=1 to enable")
def test_terminal_html_loads():
    """get_terminal_html() must return a non-empty string."""
    from rodi_admin.features.terminal import get_terminal_html

    html = get_terminal_html()
    assert isinstance(html, str)
    assert len(html) > 100
    assert "<html" in html.lower()
