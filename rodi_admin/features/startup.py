"""startup --- port prompts, banner, and local IP detection"""

import socket
import subprocess
from rodi_admin.config import PORT


def get_local_ips() -> list[str]:
    """Return all non-loopback IPv4 addresses for the current host.

    Returns:
        Sorted list of IP address strings (always includes 127.0.0.1).
    """
    ips = {"127.0.0.1"}
    try:
        hostname = socket.gethostname()
        for item in socket.getaddrinfo(hostname, None, socket.AF_INET):
            ip = item[4][0]
            if not ip.startswith("127."):
                ips.add(ip)
    except Exception:
        pass
    return sorted(ips)


def is_port_in_use(port: int) -> bool:
    """Return True if another process is already bound to the TCP port.

    Args:
        port: TCP port number to check.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("0.0.0.0", port))
            return False
        except OSError:
            return True


def get_listening_service_on_port(port: int, sudo_password: str) -> str:
    """Return human-readable process info listening on a port, or empty string.

    Args:
        port: TCP port to query.
        sudo_password: Sudo password for ss/lsof commands.

    Returns:
        Process name / pid string, or 'unknown process'.
    """
    result = subprocess.run(
        f"echo {sudo_password} | sudo -S ss -tlnp 'sport = :{port}' 2>/dev/null",
        shell=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    if result.returncode != 0 or not result.stdout.strip():
        fallback = subprocess.run(
            f"echo {sudo_password} | sudo -S lsof -iTCP:{port} -sTCP:LISTEN -P -n 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if fallback.returncode == 0 and fallback.stdout.strip():
            return fallback.stdout.strip().splitlines()[0]
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
                    pid_value = line[pid_start + 4: pid_end]
                    return f"{process_name} (pid={pid_value})"
                return process_name
        return line.strip()
    return "unknown process"


def prompt_port_number(default: int = PORT) -> int:
    """Read a single port number from stdin; re-prompt on invalid input.

    Args:
        default: Default port to use when user presses Enter.

    Returns:
        Valid TCP port number (1–65535).
    """
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


def prompt_available_port(sudo_password: str, default: int = PORT) -> int:
    """Prompt until the user selects a port that is not already in use.

    Args:
        sudo_password: Used for querying the listening process on a busy port.
        default: Default port value to suggest.

    Returns:
        Free TCP port number.
    """
    while True:
        port = prompt_port_number(default)
        if not is_port_in_use(port):
            return port

        service_name = get_listening_service_on_port(port, sudo_password)
        print(f"[!] Port {port} is already in use.")
        if service_name:
            print(f"[!] Running service: {service_name}")
        print("[!] Choose another port.")


def print_startup_banner(port: int, access_ips: list[str]) -> None:
    """Print the startup summary banner to stdout.

    Args:
        port: Port the server is listening on.
        access_ips: List of IP addresses the server is reachable from.
    """
    print("=" * 72)
    print("rodi_admin - Temporary Local Admin API")
    print("=" * 72)
    print(f"Port         : {port}")
    print("CLI Help     : python3 -m rodi_admin --help")
    print("AI Help      : python3 -m rodi_admin --help-ai")
    print("HTTP Help    : /help")
    print("Terminal UI  : /terminal")
    print("Access URLs:")
    if access_ips:
        for ip in access_ips:
            print(f"  http://{ip}:{port}/help")
            print(f"  http://{ip}:{port}/terminal")
    else:
        print(f"  http://127.0.0.1:{port}/help")
        print(f"  http://127.0.0.1:{port}/terminal")
    print("Notes        : Keep this terminal open. Press Ctrl+C to stop.")
    print("=" * 72)

