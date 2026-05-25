"""config --- centralized configuration with environment variable overrides"""

import os
import sys


def _read_int_env(variable_name: str, default_value: int) -> int:
    """Read an integer from environment; fall back to default on invalid value."""
    raw = os.environ.get(variable_name, "").strip()
    if not raw:
        return default_value
    try:
        return int(raw)
    except ValueError:
        print(
            f"[!] Warning: {variable_name}={raw!r} is not a valid integer. "
            f"Using default {default_value}.",
            file=sys.stderr,
        )
        return default_value


# HTTP port the server listens on
PORT: int = _read_int_env("RODI_ADMIN_PORT", 8889)

# Maximum bytes to read from a file via /read
MAX_READ_BYTES: int = _read_int_env("RODI_ADMIN_MAX_READ_BYTES", 256 * 1024)

# Seconds before a /run command is forcibly terminated
COMMAND_TIMEOUT_SECONDS: int = _read_int_env("RODI_ADMIN_COMMAND_TIMEOUT", 30)

# Seconds to wait for the client to finish sending the HTTP request
CLIENT_READ_TIMEOUT_SECONDS: int = _read_int_env("RODI_ADMIN_CLIENT_READ_TIMEOUT", 30)
