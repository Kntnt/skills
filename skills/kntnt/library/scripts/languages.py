#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///

"""Refuse a retired language-resolver entry point during Manager migration.

Older Managers require this published filename when validating an Update.
No language resources or resolution behavior are delivered in this generation.
"""

from __future__ import annotations

import sys


def main() -> int:
    """Report the unavailable Editorial runtime without reading or writing files."""

    print(
        "Editorial language resources are withdrawn from this generation.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
