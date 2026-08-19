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
    """Return the home the Global layer is written under.

    `HOME` and nothing else, because that is what the real transport resolves
    its global directory through — the property a Sandbox stands on (ADR-0042).
    A double that read a variable of its own would write inside the Sandbox
    whether or not the manager had redirected the one that matters, and a dry
    run that escaped into the real home would pass the suite anyway.
    """

    return Path(os.environ["HOME"])


def project() -> Path:
    """Return the project directory the caller is acting on."""

    return Path(os.environ.get("KNTNT_PROJECT", os.getcwd()))


def source() -> Path:
    """Return the collection root to copy skills from."""

    return Path(os.environ["KNTNT_SOURCE"])


def harness_paths() -> dict[str, dict[str, str]]:
    """Load this transport's own path table.

    The real `npx skills` carries its table with it and would not lose it by
    deleting a skill. Reading the manager's variable would tie the two together
    and leave the stand-in blind exactly where a test removes the manager.
    """

    return json_load(Path(os.environ["KNTNT_TRANSPORT_PATHS"]))


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
    """Replace *name* in *dest* with the collection's copy of it.

    `npx skills add` empties the skill's directory before copying rather than
    merging into it, so nothing that was there survives. ADR-0028 records why
    this double has to model that rather than copy over what it finds.
    """

    src = find_skill(name)

    # Empty the directory first, so what the collection ships is all that is left.
    target = dest / name
    if target.is_dir():
        shutil.rmtree(target)
    target.mkdir(parents=True)

    # Copy the skill in, every file of it and none of its directory entries.
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


def grumbled() -> set[str]:
    """Return the skills this run does the work for and then fails over anyway.

    A transport can exit non-zero with the files already moved — bookkeeping of
    its own after the copy is enough — and a manager that judges by the disk
    rather than by the exit code is only tested by staging exactly that.
    """

    raw = os.environ.get("KNTNT_TRANSPORT_GRUMBLE", "")
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

    # The work is done and the call fails regardless: the disk is right and
    # the exit code is not.
    grumbling = sorted(grumbled().intersection(names))
    if grumbling:
        print(
            f"error: skills {', '.join(grumbling)} moved but the ledger did not",
            file=sys.stderr,
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
