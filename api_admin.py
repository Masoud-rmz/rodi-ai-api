#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
api_admin.py — DEPRECATED shim.

This file is kept for backward compatibility only.
Use the package entrypoint instead:

    python3 -m rodi_admin

This shim will be removed in v2.0.
"""

import sys

print(
    "[!] Note: api_admin.py is deprecated. "
    "Use: python3 -m rodi_admin",
    file=sys.stderr,
)

from rodi_admin.__main__ import main  # noqa: E402

if __name__ == "__main__":
    main()
