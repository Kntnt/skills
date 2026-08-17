# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Stand-in for `npx skills` that copies collection skills onto disk."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import cast


def home() -> Path:
    """Return the isolated home directory tests give us."""

    return Path(os.environ["KNTNT_HOME"])


def project() -> Path:
    """Return the project directory the caller is acting on."""

    return Path(os.environ.get("KNTNT_PROJECT", os.getcwd()))


def source() -> Path:
    """Return the collection root to copy skills from."""

    return Path(os.environ["KNTNT_SOURCE"])


def harness_paths() -> dict[str, dict[str, str]]:
    """Load the same path table the manager uses."""

    return json_load(Path(os.environ["KNTNT_HARNESS_PATHS"]))


def json_load(path: Path) -> dict[str, dict[str, str]]:
    """Read a JSON object from *path*."""

    return cast(dict[str, dict[str, str]], json.loads(path.read_text(encoding="utf-8")))


def log_call(
    command: str, agents: list[str], names: list[str], *, global_layer: bool
) -> None:
    """Record this invocation so a test can see which agents were named.

    Whether the manager names every target or only some of them is invisible
    on disk when several agents share one directory, and that is exactly the
    property worth pinning.
    """

    destination = os.environ.get("KNTNT_TRANSPORT_LOG")
    if not destination:
        return
    entry = {
        "command": command,
        "agents": agents,
        "skills": names,
        "global": global_layer,
    }
    with Path(destination).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry) + "\n")


def expand(template: str, *, global_layer: bool) -> Path:
    """Resolve a harness path template against home or the project."""

    if template.startswith("~/"):
        return home() / template[2:]
    if global_layer:
        return home() / template
    return project() / template


def find_skill(name: str) -> Path:
    """Locate *name* under the collection's skills/ tree."""

    skills = source() / "skills"
    if name == "kntnt":
        candidate = skills / "kntnt"
        if (candidate / "SKILL.md").is_file():
            return candidate
    for skill_md in skills.glob("*/*/SKILL.md"):
        if skill_md.parent.name == name:
            return skill_md.parent
    raise SystemExit(f"error: skill '{name}' not in source")


def dest_dir(agent: str, global_layer: bool) -> Path:
    """Return the skills directory for *agent* in the targeted layer."""

    spec = harness_paths()[agent]
    key = "global" if global_layer else "project"
    if key not in spec:
        raise SystemExit(f"error: harness '{agent}' has no {key} path")
    return expand(spec[key], global_layer=global_layer)


def copy_skill(name: str, dest: Path) -> None:
    """Copy *name* into *dest*, leaving extra files already there."""

    src = find_skill(name)
    target = dest / name
    target.mkdir(parents=True, exist_ok=True)
    for path in src.rglob("*"):
        if path.is_dir():
            continue
        relative = path.relative_to(src)
        out = target / relative
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, out)


def update_skill(name: str, dest: Path) -> None:
    """Refresh *name* the way the real transport does — and no better.

    `npx skills update` compares SKILL.md and skips the skill when it matches,
    so a revision that changes only a sidecar never lands. The manager must not
    rely on update; modelling the real behaviour is what keeps it honest.
    """

    src = find_skill(name)
    target = dest / name
    current = target / "SKILL.md"
    if current.is_file() and current.read_bytes() == (src / "SKILL.md").read_bytes():
        return
    copy_skill(name, dest)


def remove_skill(name: str, dest: Path) -> None:
    """Delete *name* from *dest* if it is there."""

    target = dest / name
    if target.is_dir():
        shutil.rmtree(target)


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse a small subset of the skills CLI."""

    parser = argparse.ArgumentParser(prog="skills")
    sub = parser.add_subparsers(dest="command", required=True)

    add = sub.add_parser("add")
    add.add_argument("source")
    add.add_argument("-s", "--skill", action="append", default=[])
    add.add_argument("-a", "--agent", action="append", default=[])
    add.add_argument("-g", "--global", dest="global_layer", action="store_true")
    add.add_argument("-y", "--yes", action="store_true")
    add.add_argument("--copy", action="store_true")

    remove = sub.add_parser("remove")
    remove.add_argument("skills", nargs="*")
    remove.add_argument("-s", "--skill", action="append", default=[])
    remove.add_argument("-a", "--agent", action="append", default=[])
    remove.add_argument("-g", "--global", dest="global_layer", action="store_true")
    remove.add_argument("-y", "--yes", action="store_true")

    update = sub.add_parser("update")
    update.add_argument("skills", nargs="*")
    update.add_argument("-g", "--global", dest="global_layer", action="store_true")
    update.add_argument("-p", "--project", dest="project_layer", action="store_true")
    update.add_argument("-a", "--agent", action="append", default=[])
    update.add_argument("-y", "--yes", action="store_true")

    return parser.parse_args(argv)


def names_of(args: argparse.Namespace) -> list[str]:
    """Collect skill names from positional and --skill flags."""

    names = list(getattr(args, "skill", []) or [])
    names.extend(getattr(args, "skills", []) or [])
    return [name for name in names if name and name != "*"]


def skipped() -> set[str]:
    """Return the skills this run reports as done and leaves untouched.

    A transport that exits zero having changed nothing is the failure the
    manager is meant to catch, and staging it is the only way to test that.
    """

    raw = os.environ.get("KNTNT_TRANSPORT_SKIP", "")
    return {name.strip() for name in raw.split(",") if name.strip()}


def refused() -> set[str]:
    """Return the skills this run refuses to touch, failing the whole call.

    The real transport errors rather than working around what it will not do —
    a skill missing from the source, a directory it declines to delete — and it
    takes the batch with it. A manager that must survive that has to be tested
    against it.
    """

    raw = os.environ.get("KNTNT_TRANSPORT_REFUSE", "")
    return {name.strip() for name in raw.split(",") if name.strip()}


def main(argv: list[str] | None = None) -> int:
    """Dispatch add, remove, or update against the isolated dirs."""

    args = parse_args(argv if argv is not None else sys.argv[1:])
    agents = args.agent or ["claude-code"]
    names = names_of(args)
    if not names:
        return 1

    global_layer = bool(getattr(args, "global_layer", False))
    if args.command == "update" and getattr(args, "project_layer", False):
        global_layer = False
    log_call(args.command, agents, names, global_layer=global_layer)

    # A refused name fails the call before anything moves, batch and all.
    blocked = sorted(refused().intersection(names))
    if blocked:
        print(f"error: skills {', '.join(blocked)} refused", file=sys.stderr)
        return 1

    skip = skipped()
    for agent in agents:
        dest = dest_dir(agent, global_layer)
        dest.mkdir(parents=True, exist_ok=True)
        for name in names:
            if name in skip:
                continue
            if args.command == "remove":
                remove_skill(name, dest)
            elif args.command == "update":
                update_skill(name, dest)
            else:
                copy_skill(name, dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
