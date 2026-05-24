"""interactive_session --- PTY-based interactive session management and /session/* handlers

Note: pty and termios are Linux-only. The module imports on all platforms,
but InteractiveSession._run() will fail at runtime on non-Linux hosts.
"""

import os
import select
import signal
import threading
import uuid


SESSIONS: dict = {}
SESSIONS_LOCK = threading.Lock()


class InteractiveSession:
    """Manages a single interactive PTY process session."""

    def __init__(self, cmd: str) -> None:
        """Start a new session running the given shell command.

        Args:
            cmd: Shell command string to execute interactively.
        """
        self.session_id = str(uuid.uuid4())
        self.cmd = cmd
        self.output = ""
        self.running = True
        self.master_fd = None
        self.pid = None
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self) -> None:
        """Internal thread target: fork a PTY and relay its output to self.output."""
        import pty  # Linux-only — imported lazily so the module loads cross-platform
        try:
            pid, master_fd = pty.fork()
            if pid == 0:
                os.execl("/bin/sh", "/bin/sh", "-c", self.cmd)
            else:
                self.pid = pid
                self.master_fd = master_fd

                while self.running:
                    readable, _, _ = select.select([master_fd], [], [], 0.2)
                    if master_fd in readable:
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

    def send(self, text: str) -> tuple[bool, str]:
        """Write text input to the running PTY.

        Args:
            text: Text string to send (newline appended automatically).

        Returns:
            Tuple of (success_bool, message_string).
        """
        if not self.running or self.master_fd is None:
            return False, "Session is not running"
        try:
            os.write(self.master_fd, (text + "\n").encode())
            return True, "Input sent"
        except Exception as exc:
            return False, str(exc)

    def stop(self) -> None:
        """Send SIGTERM to the child process and mark session as stopped."""
        self.running = False
        if self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except OSError:
                pass

    def snapshot(self) -> dict:
        """Return current session state as a JSON-serialisable dict."""
        with self.lock:
            return {
                "success": True,
                "session_id": self.session_id,
                "cmd": self.cmd,
                "running": self.running,
                "output": self.output,
            }


def handle_session_start_post(body: dict) -> tuple[int, dict]:
    """Handle POST /session/start.

    Args:
        body: Parsed JSON body dict with key 'cmd'.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    cmd = body.get("cmd", "").strip()
    if not cmd:
        return 400, {"success": False, "error": "Field cmd is required"}

    session = InteractiveSession(cmd)
    with SESSIONS_LOCK:
        SESSIONS[session.session_id] = session

    return 200, {"success": True, "session_id": session.session_id, "cmd": cmd}


def handle_session_output_get(params: dict) -> tuple[int, dict]:
    """Handle GET /session/output?session_id=...

    Args:
        params: Parsed query string dict.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    session_id = params.get("session_id", [None])[0]
    if not session_id:
        return 400, {"success": False, "error": "Parameter session_id is required"}

    with SESSIONS_LOCK:
        session = SESSIONS.get(session_id)

    if not session:
        return 404, {"success": False, "error": "Session not found"}

    return 200, session.snapshot()


def handle_session_send_post(body: dict) -> tuple[int, dict]:
    """Handle POST /session/send.

    Args:
        body: Parsed JSON body with 'session_id' and 'input'.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    session_id = body.get("session_id", "")
    user_input = body.get("input", "")

    with SESSIONS_LOCK:
        session = SESSIONS.get(session_id)

    if not session:
        return 404, {"success": False, "error": "Session not found"}

    success, message = session.send(user_input)
    return (200 if success else 400), {"success": success, "message": message}


def handle_session_stop_post(body: dict) -> tuple[int, dict]:
    """Handle POST /session/stop.

    Args:
        body: Parsed JSON body with 'session_id'.

    Returns:
        Tuple of (http_status_code, response_dict).
    """
    session_id = body.get("session_id", "")

    with SESSIONS_LOCK:
        session = SESSIONS.get(session_id)

    if not session:
        return 404, {"success": False, "error": "Session not found"}

    session.stop()
    with SESSIONS_LOCK:
        SESSIONS.pop(session_id, None)

    return 200, {"success": True, "message": "Session stopped"}
