"""Shared support for standing in for a binary an engine under test calls."""

from __future__ import annotations

import os
import stat
from pathlib import Path


def fake_binary_on_path(directory: Path, name: str, script: str) -> dict[str, str]:
    """Install *script* as *name* and return the environment that runs it.

    The engines shell out to binaries a test has no business really invoking —
    `gh` would talk to GitHub — so a test stands one in and observes what it
    was asked to do. The stand-in has to be reached the same way the real one
    is, by name through `PATH`, because that is what the engine does; anything
    the engine could tell apart would stop being a substitute.

    *directory* is where the bin/ holding the stand-in is made, normally the
    test's `tmp_path`. The returned environment carries `PATH` alone, so a
    caller merges whatever else its stand-in reads.
    """

    # Write the stand-in into a directory of its own, and make it runnable.
    bin_dir = directory / "bin"
    bin_dir.mkdir()
    executable = bin_dir / name
    executable.write_text(script, encoding="utf-8")
    executable.chmod(executable.stat().st_mode | stat.S_IEXEC)

    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"}
