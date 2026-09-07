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
    # A test standing in for two binaries at once puts both in that one
    # directory, so a second call finds it already there.
    bin_dir = directory / "bin"
    bin_dir.mkdir(exist_ok=True)
    executable = bin_dir / name
    executable.write_text(script, encoding="utf-8")
    executable.chmod(executable.stat().st_mode | stat.S_IEXEC)

    return {"PATH": f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}"}


def path_holding(directory: Path, *names: str) -> str:
    """Return a `PATH` carrying exactly these binaries, and nothing else.

    `fake_binary_on_path` prepends its stand-in to the machine's own `PATH`, so
    it can say a binary is present and never that one is absent: the real thing
    is still behind it. An engine asked what this machine cannot start needs
    the absent half, and needs it to hold on the maintainer's machine as well
    as on a runner where neither CLI is installed — so this replaces the `PATH`
    rather than extending it, and naming no binary is a machine with none.

    The stand-ins are never run. What reads them is a `which`-style lookup,
    which asks the filesystem whether a name resolves to something runnable and
    stops there, so each is the smallest runnable file there is.
    """

    bin_dir = directory / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    for name in names:
        executable = bin_dir / name
        executable.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        executable.chmod(executable.stat().st_mode | stat.S_IEXEC)
    return str(bin_dir)
