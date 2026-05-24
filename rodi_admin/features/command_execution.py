"""command_execution --- run shell commands and handle /run endpoint"""

import subprocess
from rodi_admin.config import COMMAND_TIMEOUT_SECONDS


def run_command(cmd_str: str) -> dict:
    """Execute a shell command and return structured result.

    Args:
        cmd_str: Shell command string to execute.

    Returns:
        Dict with keys: success, stdout, stderr, exit_code (or error on timeout).
    """
    try:
        result = subprocess.run(
            cmd_str,
            shell=True,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT_SECONDS,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"timeout after {COMMAND_TIMEOUT_SECONDS}s"}
    except Exception as exc:
        return {"success": False, "error": str(exc)}


def handle_run_get(params: dict) -> tuple[int, dict]:
    """Handle GET /run?cmd=... request.

    Args:
        params: Parsed query string dict from urllib.parse.parse_qs.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    cmd = params.get("cmd", [None])[0]
    if not cmd:
        return 400, {"error": "Parameter 'cmd' is required"}
    return 200, run_command(cmd)


def handle_run_post(body: dict) -> tuple[int, dict]:
    """Handle POST /run with JSON body {"cmd": "..."}.

    Args:
        body: Parsed JSON body dict.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    cmd = body.get("cmd", "")
    if not cmd:
        return 400, {"error": "Field 'cmd' is required"}
    return 200, run_command(cmd)
