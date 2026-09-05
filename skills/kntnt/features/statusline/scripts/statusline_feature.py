# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Point Claude Code's status line at the one this collection ships.

A status line is a single-valued setting rather than a table: `statusLine` in
`~/.claude/settings.json` names one command, and a second owner cannot be added
beside the first. That changes what installation means here. A hook table entry
is added to whatever is already there and taken back out by the owner it
carries; a status line either is ours or is somebody's.

Finding somebody's there is a question and not a verdict (ADR-0174). Enabling
this Feature is a user saying they want this status line, and answering that
with *no, something is already there* leaves them holding an outcome they did
not ask for and no way forward from the list they are standing in. So an
install that has not been told to replace what it found reports what holds the
slot and writes nothing — which is what lets the question be asked where
questions are asked — and one that has been told replaces it and names what
went. `--replace` is how the Manager carries the user's answer down here; it is
not a flag anybody types, the answer being given to Select's own confirmation.

What this collection will not do either way is stash the displaced value
somewhere of its own so that a later removal can put it back. That is a private
ledger, and disk is the truth this collection converges on (ADR-0090): a ledger
goes stale the moment the user edits the setting by hand, and a removal
restoring a value the user has since replaced is worse than one that restores
nothing. The name of what was replaced is in the report and nowhere else, which
is why the question has to say so before it is answered.
"""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path
from typing import Any

OWNER = "kntnt.statusline"

# The one Harness with a status line the Collection Library has an adapter for.
# Every other Detected Harness is reported through the Capability the Library
# states rather than quietly skipped (ADR-0030).
HARNESS = "claude-code"


def home() -> Path:
    """Return the home this Feature resolves the Harness's own files against."""

    import os

    override = os.environ.get("KNTNT_HOME")
    return Path(override) if override else Path.home()


def _library(*relative: str) -> Path:
    """Return the Collection Library module this Feature reads its mechanics from."""

    return Path(__file__).resolve().parents[3] / "library" / "scripts" / Path(*relative)


def _integrations() -> Any:
    """Load the Collection Library's owned-integration mechanics.

    How a Harness's own settings file is read and written is the Library's
    knowledge and never a Feature's (ADR-0076).
    """

    import importlib.util

    path = _library("integrations.py")
    spec = importlib.util.spec_from_file_location("kntnt_integrations", path)
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable in tests
        raise RuntimeError(f"the Collection Library is not readable at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def statusline_command() -> list[str]:
    """Return the command the Harness runs to draw the status line.

    The shipped script is named where it is installed rather than copied
    somewhere a second copy could go stale, which is what every other owned
    integration in this collection does. The path is quoted because it is
    joined into one command string, and a home directory with a space in it
    would otherwise be read as two arguments.
    """

    script = Path(__file__).resolve().parents[1] / "statusline.sh"
    return ["bash", shlex.quote(str(script))]


def install_integrations(
    harnesses: list[str], *, replace: bool = False
) -> dict[str, Any]:
    """Take the status line, replacing another owner's only when told to."""

    integrations = _integrations()
    named = list(harnesses) or [HARNESS]
    root = home()
    attempted = [harness for harness in named if harness == HARNESS]
    return {
        "installed": [
            integrations.install_statusline(
                OWNER, harness, root, statusline_command(), replace=replace
            )
            for harness in attempted
        ],
        "unsupported": {"count": len(named) - len(attempted)},
    }


def remove_integrations() -> dict[str, Any]:
    """Clear the status line where this collection holds it, and never otherwise."""

    integrations = _integrations()
    return {"removed": [integrations.remove_statusline(OWNER, HARNESS, home())]}


def feature_health(harnesses: list[str]) -> dict[str, Any]:
    """Report who holds the status line right now."""

    integrations = _integrations()
    named = list(harnesses) or [HARNESS]
    attempted = [harness for harness in named if harness == HARNESS]
    return {
        "harnesses": [
            integrations.statusline_health(OWNER, harness, home())
            for harness in attempted
        ],
        "unsupported": {"count": len(named) - len(attempted)},
    }


def _emit(payload: dict[str, Any]) -> None:
    """Print one machine-readable answer."""

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one statusline invocation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=("install-integrations", "remove-integrations", "health"),
    )
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--owner", default=OWNER)

    # The user's own answer, carried in rather than assumed: a script cannot
    # ask (ADR-0029), so what it may overwrite has to arrive on its command
    # line from whatever did the asking.
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one statusline action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    if args.action == "install-integrations":
        _emit(install_integrations(args.harness, replace=args.replace))
    elif args.action == "remove-integrations":
        _emit(remove_integrations())
    else:
        _emit(feature_health(args.harness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
