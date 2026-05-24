"""__main__ --- entrypoint for `python3 -m rodi_admin`"""

import argparse

from rodi_admin.help_texts import AI_HELP_TEXT, USER_HELP_TEXT
from rodi_admin.features.firewall import open_firewall_port, prompt_required_sudo_password
from rodi_admin.features.startup import (
    get_local_ips,
    print_startup_banner,
    prompt_available_port,
)
from rodi_admin.features.http_server import start_server
from rodi_admin.config import PORT


def main() -> None:
    """Parse CLI args, acquire sudo, open firewall, start HTTP server."""
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

    sudo_password = prompt_required_sudo_password()
    port = prompt_available_port(sudo_password, PORT)
    open_firewall_port(port, sudo_password)

    access_ips = get_local_ips()
    print_startup_banner(port, access_ips)

    start_server(port, sudo_password)


if __name__ == "__main__":
    main()
