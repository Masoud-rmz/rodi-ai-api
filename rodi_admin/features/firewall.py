"""firewall --- UFW port management for startup and graceful shutdown"""

import getpass
import subprocess
import sys


def verify_sudo_password(password: str) -> bool:
    """Verify a sudo password by running a harmless privileged command.

    Args:
        password: Plaintext sudo password to test.

    Returns:
        True if the password is accepted, False otherwise.
    """
    result = subprocess.run(
        f"echo {password} | sudo -S -k true",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=15,
    )
    return result.returncode == 0


def prompt_required_sudo_password() -> str:
    """Prompt the user until a valid non-empty sudo password is provided.

    Returns:
        Verified sudo password string.

    Raises:
        SystemExit: If user interrupts the prompt.
    """
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


def verify_firewall_port_open(port: int, sudo_password: str) -> bool:
    """Check whether UFW reports the given TCP port as allowed.

    Args:
        port: TCP port number to check.
        sudo_password: Sudo password for running ufw status.

    Returns:
        True if UFW shows an ALLOW rule for the port.
    """
    result = subprocess.run(
        f"echo {sudo_password} | sudo -S ufw status 2>/dev/null",
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


def open_firewall_port(port: int, sudo_password: str) -> None:
    """Open a TCP port in UFW; exit if the rule cannot be confirmed.

    Args:
        port: TCP port to open.
        sudo_password: Sudo password for ufw commands.

    Raises:
        SystemExit: If ufw rule cannot be added or confirmed.
    """
    print(f"[+] Opening TCP port {port} in UFW...")
    result = subprocess.run(
        f"echo {sudo_password} | sudo -S ufw allow {port}/tcp",
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

    if not verify_firewall_port_open(port, sudo_password):
        print(f"[!] UFW rule for port {port}/tcp was not confirmed. Exiting.")
        raise SystemExit(1)

    print(f"[+] Port {port}/tcp is open in UFW.")


def cleanup_firewall_port(port: int, sudo_password: str) -> None:
    """Remove the UFW rule for the given port.  Called via atexit.

    Args:
        port: TCP port whose rule should be removed.
        sudo_password: Sudo password for ufw commands.
    """
    print(f"\n[+] Closing port {port} and removing firewall rule...")
    subprocess.run(
        f"echo {sudo_password} | sudo -S ufw delete allow {port}/tcp",
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("[!] Port closed successfully.")
