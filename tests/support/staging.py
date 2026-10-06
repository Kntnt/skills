"""Committed fixture source for archive-layout checks, without native runs."""

from __future__ import annotations

import subprocess
from pathlib import Path


def archive_source(root: Path, names: tuple[str, ...]) -> Path:
    """Create the minimal frozen collection whose paths a staging check exports."""

    root.mkdir()
    for name in names:
        directory = root / "skills" / "editorial" / name
        directory.mkdir(parents=True)
        (directory / "SKILL.md").write_text(f"# {name} archive-layout fixture\n")
    manager = root / "skills" / "kntnt" / "scripts"
    manager.mkdir(parents=True)
    (manager / "kntnt.py").write_text("# Manager archive-layout fixture.\n")
    for arguments in (
        ["init", "-b", "main"],
        ["add", "."],
        ["commit", "-m", "Freeze archive layout fixture"],
    ):
        subprocess.run(
            [
                "git",
                "-c",
                "user.name=Staging fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "-c",
                "commit.gpgsign=false",
                "-c",
                "core.hooksPath=/dev/null",
                *arguments,
            ],
            cwd=root,
            capture_output=True,
            check=True,
        )
    return root
