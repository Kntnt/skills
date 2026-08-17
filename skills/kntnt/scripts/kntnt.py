# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Manage which collection skills are Enabled on which Harnesses."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, cast

ORIGIN = "Kntnt/skills"
MANAGER = "kntnt"
UNIVERSAL_PROJECT = ".agents/skills"
CANONICAL_GLOBAL = "~/.agents/skills"

# What a verb exits with when the disk does not show the change it made. The
# payload is still emitted: the user has to be told which skills and where.
EXIT_CHANGE_FAILED = 1
BINARY_HOW = {
    "uv": "install uv from https://docs.astral.sh/uv/",
    "git": "install git",
    "gh": "install GitHub CLI (gh) from https://cli.github.com/",
}

# A Capability is a Dependency on the Harness itself. No script can test one:
# this file cannot know which Harness invoked it, let alone what that Harness
# can do. So the checker reports the Capabilities a skill requires and the
# agent — which is the Harness — answers. Every name a skill may declare is
# defined here, so a typo is a refusal rather than a silently skipped check.
CAPABILITIES = {
    "subagents": {
        "confirm": "you can spawn subagents that work in their own context window",
        "how": "run this skill in a harness that can spawn subagents",
    },
}
MANAGER_HELP = """\
kntnt — manage this collection

Usage: /kntnt [subcommand] [skill...] [--project[=on|off]] [--yes]

Subcommands:
  help [skill]         this help, or help for one named collection skill
  status [skill...]    report Enabled/Disabled in Global and Project
  enable [skill...]    make skills Enabled (picker if none named)
  disable [skill...]   make skills Disabled (picker if none named)
  update               refresh this collection and re-check Dependencies

Options:
  --project    act on this Project instead of Global (--project=off is Global)
  --yes        assume yes; ask nothing that can be answered yes or no

Bare /kntnt is this help. Status lists every Catalog skill, Enabled or not.
Enable, Disable, and Update default to Global. They act on every Harness
present on this machine, working out which those are on every run.
"""


class ManagerError(RuntimeError):
    """A user-facing manager failure with an exit code."""

    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code


def fail(message: str, code: int = 1) -> int:
    """Print an error to stderr and return an exit code."""

    print(f"error: {message}", file=sys.stderr)
    return code


def emit(payload: Any) -> None:
    """Print *payload* as JSON."""

    print(json.dumps(payload, indent=2))


def home() -> Path:
    """Return the home used to resolve Global harness paths."""

    return Path(os.environ.get("KNTNT_HOME", str(Path.home())))


def here() -> Path:
    """Return the installed manager directory."""

    override = os.environ.get("KNTNT_HERE")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent


def project_root() -> Path:
    """Return the Project directory (cwd, unless tests override)."""

    override = os.environ.get("KNTNT_PROJECT")
    if override:
        return Path(override)
    return Path.cwd()


def collection_source() -> str:
    """Return the collection origin the transport and Catalog fetch use."""

    return os.environ.get("KNTNT_SOURCE", ORIGIN)


def harness_paths() -> dict[str, dict[str, str]]:
    """Load harness id → path templates."""

    override = os.environ.get("KNTNT_HARNESS_PATHS")
    path = Path(override) if override else here() / "harness-paths.json"
    return cast(dict[str, dict[str, str]], json.loads(path.read_text(encoding="utf-8")))


def expand_path(template: str, *, global_layer: bool) -> Path:
    """Resolve a harness path template against home or the Project."""

    if template.startswith("~/"):
        return home() / template[2:]
    if global_layer:
        return home() / template
    return project_root() / template


def layer_dir(harness: str, *, global_layer: bool) -> Path | None:
    """Return the skills directory for *harness* in the targeted layer."""

    spec = harness_paths().get(harness)
    if spec is None:
        return None
    key = "global" if global_layer else "project"
    template = spec.get(key)
    if not template:
        return None
    return expand_path(template, global_layer=global_layer)


def is_universal(harness: str) -> bool:
    """True when the transport installs *harness* into the shared .agents/skills tree."""

    spec = harness_paths().get(harness)
    return spec is not None and spec.get("project") == UNIVERSAL_PROJECT


def skill_dirs(harness: str, *, global_layer: bool) -> list[Path]:
    """Return directories where *harness* may hold a skill in this layer.

    The transport treats a harness whose project path is `.agents/skills` as
    universal and writes Global files to `~/.agents/skills`, ignoring that
    harness's documented globalSkillsDir.
    """

    dirs: list[Path] = []
    primary = layer_dir(harness, global_layer=global_layer)
    if primary is not None:
        dirs.append(primary)
    if global_layer and is_universal(harness):
        canonical = expand_path(CANONICAL_GLOBAL, global_layer=True)
        if canonical not in dirs:
            dirs.append(canonical)
    return dirs


def parse_yaml_scalar(raw: str) -> Any:
    """Parse a YAML scalar used in skill frontmatter."""

    if raw in {"true", "True"}:
        return True
    if raw in {"false", "False"}:
        return False
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
        return raw[1:-1]
    return raw


def _next_significant(lines: list[str], start: int) -> tuple[int, str] | None:
    """Return (indent, stripped) of the next non-empty, non-comment line."""

    for raw in lines[start:]:
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        return indent, raw.strip()
    return None


def parse_simple_yaml(text: str) -> dict[str, Any]:
    """Parse a restricted YAML subset: maps, lists of scalars, scalars."""

    lines = text.splitlines()
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]
    index = 0

    while index < len(lines):
        raw = lines[index]
        if not raw.strip() or raw.strip().startswith("#"):
            index += 1
            continue

        indent = len(raw) - len(raw.lstrip(" "))
        stripped = raw.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        container = stack[-1][1]

        if stripped.startswith("- "):
            if isinstance(container, list):
                container.append(parse_yaml_scalar(stripped[2:].strip()))
            index += 1
            continue

        if ":" not in stripped:
            index += 1
            continue

        key, _, rest = stripped.partition(":")
        key = key.strip()
        rest = rest.strip()
        if not isinstance(container, dict):
            index += 1
            continue

        if rest:
            container[key] = parse_yaml_scalar(rest)
            index += 1
            continue

        nxt = _next_significant(lines, index + 1)
        if nxt is not None and nxt[1].startswith("- ") and nxt[0] > indent:
            nested_list: list[Any] = []
            container[key] = nested_list
            stack.append((indent, nested_list))
        else:
            nested_map: dict[str, Any] = {}
            container[key] = nested_map
            stack.append((indent, nested_map))
        index += 1

    return root


def parse_frontmatter(text: str) -> dict[str, Any]:
    """Return the YAML frontmatter of a SKILL.md, or an empty dict."""

    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    return parse_simple_yaml(text[4:end])


DEP_KINDS = ("binaries", "skills", "externals", "capabilities")


def skill_deps(frontmatter: dict[str, Any]) -> dict[str, list[str]]:
    """Read Dependency lists from a skill's frontmatter."""

    empty: dict[str, list[str]] = {key: [] for key in DEP_KINDS}
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        return empty
    block = metadata.get("kntnt")
    if not isinstance(block, dict):
        return empty
    result: dict[str, list[str]] = {}
    for key in DEP_KINDS:
        values = block.get(key, [])
        result[key] = [str(item) for item in values] if isinstance(values, list) else []
    return result


def capability_notes(names: list[str]) -> list[dict[str, str]]:
    """Describe each required Capability so the agent can answer for itself."""

    notes: list[dict[str, str]] = []
    for name in names:
        note = CAPABILITIES.get(name)
        if note is None:
            raise ManagerError(f"unknown capability '{name}'")
        notes.append({"name": name, **note})
    return notes


def fetch_catalog() -> dict[str, Any]:
    """Load the Catalog from the collection origin. Never invent it."""

    source = collection_source()
    local = Path(source)
    if local.is_dir():
        candidate = local / "skills" / MANAGER / "catalog.json"
        if candidate.is_file():
            return cast(
                dict[str, Any], json.loads(candidate.read_text(encoding="utf-8"))
            )
        raise ManagerError(f"Catalog missing at {candidate}")

    url = (
        f"https://raw.githubusercontent.com/{source}/main/skills/{MANAGER}/catalog.json"
    )
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            return cast(dict[str, Any], json.loads(response.read().decode("utf-8")))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise ManagerError(f"Catalog could not be fetched from {url}") from exc


def write_catalog(catalog: dict[str, Any]) -> None:
    """Store *catalog* beside the Manager that is running."""

    path = here() / "catalog.json"
    path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def load_catalog() -> dict[str, Any]:
    """Return the shipped Catalog, fetching it once if the file is gone."""

    path = here() / "catalog.json"
    if path.is_file():
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    catalog = fetch_catalog()
    write_catalog(catalog)
    return catalog


def catalog_skills() -> list[dict[str, Any]]:
    """Return the Catalog's skill entries."""

    skills = load_catalog().get("skills", [])
    if not isinstance(skills, list):
        raise ManagerError("Catalog is corrupt")
    return [entry for entry in skills if isinstance(entry, dict)]


def catalog_names() -> set[str]:
    """Return every Catalog skill name."""

    return {str(entry["name"]) for entry in catalog_skills() if "name" in entry}


def is_project_detectable(template: str) -> bool:
    """True when a Project template names a hidden directory of the Harness's own.

    `skills`, `data/skills`, and `agent/skills` are things a repository has for
    its own reasons. Reading one of those as a Harness would write this
    collection into someone else's source tree, so such a Harness is not
    detected in the Project layer at all.
    """

    return template.startswith(".")


def detected_harnesses(*, global_layer: bool) -> list[str]:
    """Return the Harnesses present in this layer.

    Present means the Harness has a home here — the parent of its skills
    directory is on disk — not that it already holds skills. A Harness
    installed after the last Enable is therefore detected on the next run.
    """

    key = "global" if global_layer else "project"
    found: list[str] = []

    # A Harness qualifies only where it documents a path for this layer, and in
    # the Project layer only where that path is its own to claim.
    for harness, spec in harness_paths().items():
        template = spec.get(key)
        if not template:
            continue
        if not global_layer and not is_project_detectable(template):
            continue
        if expand_path(template, global_layer=global_layer).parent.is_dir():
            found.append(harness)

    return found


def shared_harness() -> str:
    """Return the harness id that reads the shared skills directory in both layers.

    The transport writes by agent id, so naming the shared directory means
    naming an agent that reads exactly it and nothing else. Several do, they
    all write the same files to the same place, and the first in a stable order
    is as good as any.
    """

    for harness, spec in sorted(harness_paths().items()):
        if (
            spec.get("global") == CANONICAL_GLOBAL
            and spec.get("project") == UNIVERSAL_PROJECT
        ):
            return harness
    raise ManagerError("no harness reads the shared skills directory")


def target_harnesses(*, global_layer: bool) -> list[str]:
    """Return every Harness this invocation acts on, never a subset of them.

    With nothing detected the answer is the shared skills directory alone. The
    transport's own fallback — every agent it knows of — would create skills
    directories for Harnesses the user has never installed.
    """

    return detected_harnesses(global_layer=global_layer) or [shared_harness()]


def target_dirs(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return the skills directories *harnesses* resolve to, for a payload.

    These are `skill_dirs`, not the documented path alone: a universal Harness
    has its Global files written to the canonical tree rather than to the
    directory its own entry names, so naming only the latter would report a
    place the file never landed in. Reporting both keeps the payload to what
    Status actually looked in.
    """

    directories = {
        str(directory)
        for harness in harnesses
        for directory in skill_dirs(harness, global_layer=global_layer)
    }
    return sorted(directories)


def skill_present_at(directory: Path, name: str) -> bool:
    """True when *name* is on disk in *directory*.

    The manager's one notion of presence. Status decides Enabled with it and a
    change is confirmed with it, so no verb can report what Status contradicts.
    """

    return (directory / name / "SKILL.md").is_file()


def skill_state(name: str, harnesses: list[str], *, global_layer: bool) -> str:
    """Return enabled, disabled, or partial for *name* in one layer."""

    if not harnesses:
        return "disabled"
    present = 0
    checked = 0
    for harness in harnesses:
        directories = skill_dirs(harness, global_layer=global_layer)
        if not directories:
            continue
        checked += 1
        if any(skill_present_at(directory, name) for directory in directories):
            present += 1
    if checked == 0 or present == 0:
        return "disabled"
    if present == checked:
        return "enabled"
    return "partial"


def enabled_names(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return Catalog skills Enabled in *layer* on any targeted Harness."""

    names: list[str] = []
    for entry in catalog_skills():
        name = str(entry["name"])
        if skill_state(name, harnesses, global_layer=global_layer) != "disabled":
            names.append(name)
    return names


def run_transport(args: list[str], *, internal: bool = False) -> None:
    """Run the transport. Skill files move only through this call."""

    raw = os.environ.get("KNTNT_TRANSPORT", "npx --yes skills")
    command = [*shlex.split(raw), *args]
    env = os.environ.copy()
    if internal:
        env["INSTALL_INTERNAL_SKILLS"] = "1"
    result = subprocess.run(
        command,
        cwd=project_root(),
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise ManagerError(detail or f"transport failed: {' '.join(args)}")


def contradicting_dirs(
    name: str, harnesses: list[str], *, global_layer: bool, expect_present: bool
) -> list[str]:
    """Return the directories where *name* contradicts the intended change."""

    directories: set[str] = set()

    # A Harness that agrees contributes nothing, even where one of its own
    # directories is empty: that is what the canonical tree does to a universal
    # Harness on a placement that did take effect.
    for harness in harnesses:
        presence = {
            directory: skill_present_at(directory, name)
            for directory in skill_dirs(harness, global_layer=global_layer)
        }
        if any(presence.values()) == expect_present:
            continue
        directories.update(
            str(directory)
            for directory, present in presence.items()
            if present != expect_present
        )

    return sorted(directories)


def verified_outcome(
    names: list[str], harnesses: list[str], *, global_layer: bool, expect_present: bool
) -> dict[str, Any]:
    """Report which of *names* the disk agrees were changed.

    The transport's exit code says only that it did not throw; a run that does
    nothing looks exactly like one that did the work (issue #7). Success is
    therefore the presence test Status uses, run again over the same layer and
    the same directories: a placement is confirmed where the skill is now
    Enabled, a removal where it is now Disabled. Whatever fails that is named,
    with the directories that contradict it, so the user knows where to look.
    """

    wanted = "enabled" if expect_present else "disabled"
    confirmed: list[str] = []
    failed: list[dict[str, Any]] = []

    # Ask the disk about each name, and name the directories behind a no.
    for name in names:
        if skill_state(name, harnesses, global_layer=global_layer) == wanted:
            confirmed.append(name)
            continue
        failed.append(
            {
                "name": name,
                "directories": contradicting_dirs(
                    name,
                    harnesses,
                    global_layer=global_layer,
                    expect_present=expect_present,
                ),
            }
        )

    return {"intended": list(names), "confirmed": confirmed, "failed": failed}


def outcome_exit_code(outcome: dict[str, Any]) -> int:
    """Return the exit code a verified outcome earns.

    One rule for every verb: a change the disk does not show fails the run,
    including a run where other skills succeeded. The payload is emitted
    either way — an exit code names neither the skill nor the directory.
    """

    return EXIT_CHANGE_FAILED if outcome["failed"] else 0


def add_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Enable *names* on *harnesses* in the targeted layer, and verify it."""

    # Nothing to place is not a call: the transport refuses an empty selection.
    if names and harnesses:
        args = ["add", collection_source()]
        for name in names:
            args.extend(["--skill", name])
        for harness in harnesses:
            args.extend(["--agent", harness])
        if global_layer:
            args.append("--global")
        args.append("--yes")
        run_transport(args, internal=True)

    return verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=True
    )


def remove_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> dict[str, Any]:
    """Disable *names* on *harnesses* in the targeted layer, and verify it."""

    # Nothing to remove is not a call: the transport refuses an empty selection.
    if names and harnesses:
        args = ["remove", *names]
        for harness in harnesses:
            args.extend(["--agent", harness])
        if global_layer:
            args.append("--global")
        args.append("--yes")
        run_transport(args, internal=True)

    return verified_outcome(
        names, harnesses, global_layer=global_layer, expect_present=False
    )


def withdraw_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> list[dict[str, Any]]:
    """Take the skills the collection has withdrawn off the disk.

    A skill that has left the Catalog can no longer be updated, supported, or
    reasoned about, so it is removed without asking (ADR-0037). It goes through
    Disable's own removal — the collection has one way to delete skill files —
    and each name is reported with what the disk then showed: `removed` where
    the files are gone, `absent` where there were none to delete, and `failed`
    with the directories they survive in. A failure is one skill's, not the
    run's: whatever else Update had to do still happens.
    """

    # A withdrawn skill that was never Enabled here has nothing to delete, and
    # the transport is not asked about one.
    on_disk = [
        name
        for name in names
        if skill_state(name, harnesses, global_layer=global_layer) != "disabled"
    ]

    # The transport takes the whole batch down when it refuses one name, so a
    # failure here is a verdict to be read off the disk rather than raised.
    try:
        outcome = remove_skills(on_disk, harnesses, global_layer=global_layer)
    except ManagerError:
        outcome = verified_outcome(
            on_disk, harnesses, global_layer=global_layer, expect_present=False
        )

    # Give every withdrawn name its verdict, whether or not it was asked of the
    # transport, so the report covers what left the Catalog and not just what
    # the removal touched.
    failed = {str(item["name"]): item["directories"] for item in outcome["failed"]}
    report: list[dict[str, Any]] = []
    for name in names:
        if name not in on_disk:
            report.append({"name": name, "disk": "absent"})
        elif name in failed:
            report.append({"name": name, "disk": "failed", "directories": failed[name]})
        else:
            report.append({"name": name, "disk": "removed"})

    return report


def parse_layer(value: str) -> bool:
    """True when the command targets Global."""

    if value in {"on", "true", "1"}:
        return False
    if value in {"off", "false", "0"}:
        return True
    raise ManagerError(f"unknown --project value '{value}'")


def validate_names(names: list[str]) -> list[str]:
    """Reject the Manager and unknown Catalog names."""

    known = catalog_names()
    cleaned: list[str] = []
    for name in names:
        if name == MANAGER:
            raise ManagerError("kntnt is the Manager; it is always Enabled")
        if name not in known:
            raise ManagerError(f"unknown skill '{name}'")
        if name not in cleaned:
            cleaned.append(name)
    return cleaned


def status_payload(names: list[str]) -> dict[str, Any]:
    """Build the Status report for *names*, or every Catalog skill."""

    global_targets = target_harnesses(global_layer=True)
    project_targets = target_harnesses(global_layer=False)
    wanted = (
        validate_names(names)
        if names
        else [str(entry["name"]) for entry in catalog_skills()]
    )
    by_name = {str(entry["name"]): entry for entry in catalog_skills()}
    skills: list[dict[str, Any]] = []
    for name in wanted:
        entry = by_name[name]
        skills.append(
            {
                "name": name,
                "category": entry.get("category", ""),
                "description": entry.get("description", ""),
                "capabilities": entry.get("capabilities", []),
                "global": skill_state(name, global_targets, global_layer=True),
                "project": skill_state(name, project_targets, global_layer=False),
            }
        )
    return {
        "directories": {
            "global": target_dirs(global_targets, global_layer=True),
            "project": target_dirs(project_targets, global_layer=False),
        },
        "skills": skills,
    }


def picker_payload(
    names: list[str], *, global_layer: bool, action: str
) -> dict[str, Any]:
    """Group Catalog skills by Category for an interactive Enable/Disable."""

    harnesses = target_harnesses(global_layer=global_layer)
    categories: dict[str, list[dict[str, Any]]] = {}
    for entry in catalog_skills():
        name = str(entry["name"])
        if names and name not in names:
            continue
        state = skill_state(name, harnesses, global_layer=global_layer)
        if action == "disable" and state == "disabled":
            continue
        category = str(entry.get("category") or "other")
        categories.setdefault(category, []).append(
            {
                "name": name,
                "description": entry.get("description", ""),
                "capabilities": entry.get("capabilities", []),
                "enabled": state == "enabled",
            }
        )
    return {
        "action": "pick",
        "layer": "global" if global_layer else "project",
        "categories": categories,
    }


def cmd_status(names: list[str]) -> int:
    """Print Status and return 0."""

    emit(status_payload(names))
    return 0


def cmd_plan_enable(names: list[str], *, global_layer: bool) -> int:
    """Print an Enable picker or a plan for the named skills."""

    if not names:
        emit(picker_payload([], global_layer=global_layer, action="enable"))
        return 2
    wanted = validate_names(names)
    harnesses = target_harnesses(global_layer=global_layer)
    emit(
        {
            "action": "enable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_plan_disable(names: list[str], *, global_layer: bool) -> int:
    """Print a Disable picker or a plan for the named skills."""

    if not names:
        emit(picker_payload([], global_layer=global_layer, action="disable"))
        return 2
    wanted = validate_names(names)
    harnesses = target_harnesses(global_layer=global_layer)
    emit(
        {
            "action": "disable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_apply_enable(names: list[str], *, global_layer: bool) -> int:
    """Enable the named skills in the targeted layer."""

    wanted = validate_names(names)
    if not wanted:
        raise ManagerError("name at least one skill to enable", 2)
    harnesses = target_harnesses(global_layer=global_layer)
    already = {
        name
        for name in wanted
        if skill_state(name, harnesses, global_layer=global_layer) == "enabled"
    }
    changing = [name for name in wanted if name not in already]
    outcome = add_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            **outcome,
            "noop": [name for name in wanted if name in already],
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return outcome_exit_code(outcome)


def cmd_apply_disable(names: list[str], *, global_layer: bool, yes: bool) -> int:
    """Disable the named skills in the targeted layer."""

    wanted = validate_names(names)
    if not wanted:
        raise ManagerError("name at least one skill to disable", 2)

    # Disable deletes skill files. Nothing here can prompt, so the confirmation
    # has to have happened before the call, and --yes is how that is asserted.
    if not yes:
        raise ManagerError(
            "disabling deletes these skills' files; confirm first, then pass --yes",
            2,
        )
    harnesses = target_harnesses(global_layer=global_layer)
    changing: list[str] = []
    noop: list[str] = []
    for name in wanted:
        state = skill_state(name, harnesses, global_layer=global_layer)
        if state == "disabled":
            noop.append(name)
            continue
        changing.append(name)
    outcome = remove_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            **outcome,
            "noop": noop,
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return outcome_exit_code(outcome)


def cmd_plan_update(*, global_layer: bool) -> int:
    """Print which Enabled skills Update will refresh."""

    harnesses = target_harnesses(global_layer=global_layer)
    refresh = enabled_names(harnesses, global_layer=global_layer)
    if global_layer:
        refresh = [MANAGER, *refresh]
    emit(
        {
            "action": "update",
            "layer": "global" if global_layer else "project",
            "refresh": refresh,
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )
    return 0


def cmd_apply_update(*, global_layer: bool) -> int:
    """Refresh this collection, report new Catalog entries, re-check Dependencies."""

    harnesses = target_harnesses(global_layer=global_layer)
    old_names = catalog_names()

    # The Catalog is adopted before anything is decided from it. Deciding first
    # would resolve the work against a list the collection has already moved
    # on from, and ask the transport for a skill the source no longer carries
    # (issue #5). The refresh below reaches only the Harnesses detected here,
    # which need not hold the copy of the Manager running right now, so this
    # Manager's own Catalog is written directly or Status goes on reporting the
    # snapshot it shipped with.
    catalog_refreshed = True
    try:
        write_catalog(fetch_catalog())
    except ManagerError:
        catalog_refreshed = False

    current_names = catalog_names()
    new_names = [name for name in sorted(current_names) if name not in old_names]
    withdrawn = [name for name in sorted(old_names) if name not in current_names]
    withdrawals = withdraw_skills(withdrawn, harnesses, global_layer=global_layer)

    desired = enabled_names(harnesses, global_layer=global_layer)
    refresh = [MANAGER, *desired] if global_layer else list(desired)

    # The transport's own `update` compares SKILL.md and skips a skill whose
    # SKILL.md is unchanged, leaving sidecars — catalog.json, helper documents,
    # scripts — frozen at the revision that last touched SKILL.md. `add`
    # re-copies the whole directory and is idempotent, so it is the refresh.
    outcome = add_skills(refresh, harnesses, global_layer=global_layer)

    unsatisfied: list[dict[str, str]] = []
    capabilities: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    seen_capabilities: set[tuple[str, str]] = set()
    for harness in harnesses:
        for directory in skill_dirs(harness, global_layer=global_layer):
            for name in desired:
                skill_dir = directory / name
                if not skill_present_at(directory, name):
                    continue
                for item in unsatisfied_at(skill_dir):
                    key = (item["kind"], item["name"], item["how"])
                    if key in seen:
                        continue
                    seen.add(key)
                    unsatisfied.append(item)
                for note in capabilities_at(skill_dir):
                    pair = (name, note["name"])
                    if pair in seen_capabilities:
                        continue
                    seen_capabilities.add(pair)
                    capabilities.append({"skill": name, **note})

    emit(
        {
            **outcome,
            "new": new_names,
            "removed": withdrawals,
            "catalog_refreshed": catalog_refreshed,
            "unsatisfied": unsatisfied,
            "capabilities": capabilities,
            "layer": "global" if global_layer else "project",
            "directories": target_dirs(harnesses, global_layer=global_layer),
        }
    )

    # ADR-0036's one rule reaches both halves of the run: a withdrawal whose
    # files are still there is as much a change the disk does not show as a
    # refresh that never landed.
    if any(item["disk"] == "failed" for item in withdrawals):
        return EXIT_CHANGE_FAILED

    return outcome_exit_code(outcome)


def declared_deps_at(skill_dir: Path) -> dict[str, list[str]]:
    """Return the Dependency lists declared in *skill_dir*/SKILL.md."""

    path = skill_dir / "SKILL.md"
    if not path.is_file():
        raise ManagerError(f"no SKILL.md at {skill_dir}")
    return skill_deps(parse_frontmatter(path.read_text(encoding="utf-8")))


def capabilities_at(skill_dir: Path) -> list[dict[str, str]]:
    """Return the Capabilities *skill_dir* requires of the running Harness."""

    return capability_notes(declared_deps_at(skill_dir)["capabilities"])


def unsatisfied_at(skill_dir: Path) -> list[dict[str, str]]:
    """Return Unsatisfied Dependencies declared in *skill_dir*/SKILL.md.

    Capabilities are absent by design: only the agent can answer those.
    """

    deps = declared_deps_at(skill_dir)
    missing: list[dict[str, str]] = []

    for binary in deps["binaries"]:
        if shutil.which(binary) is None:
            missing.append(
                {
                    "name": binary,
                    "kind": "binary",
                    "how": BINARY_HOW.get(binary, f"install {binary}"),
                }
            )

    for name in deps["skills"]:
        if not skill_is_effective(name):
            missing.append(
                {
                    "name": name,
                    "kind": "skill",
                    "how": f"/kntnt enable {name}",
                }
            )

    for name in deps["externals"]:
        if not skill_is_effective(name):
            missing.append(
                {
                    "name": name,
                    "kind": "external",
                    "how": f"add the External '{name}' with the transport (npx skills add)",
                }
            )

    return missing


def skill_is_effective(name: str) -> bool:
    """True when *name* is present in Global or this Project (the Effective union)."""

    for global_layer in (True, False):
        for harness in target_harnesses(global_layer=global_layer):
            if any(
                skill_present_at(directory, name)
                for directory in skill_dirs(harness, global_layer=global_layer)
            ):
                return True
    return False


def cmd_check(skill_dir: Path) -> int:
    """Refuse when a Dependency at *skill_dir* is Unsatisfied.

    `capabilities` is the unfinished half of the check: each entry is a
    Dependency this script cannot test, handed to the agent to answer. Exit 0
    with a non-empty list therefore means "nothing missing that I can see",
    not "go ahead".
    """

    capabilities = capabilities_at(skill_dir)
    missing = unsatisfied_at(skill_dir)
    if missing:
        emit({"ok": False, "unsatisfied": missing, "capabilities": capabilities})
        return 2
    emit({"ok": True, "unsatisfied": [], "capabilities": capabilities})
    return 0


def find_skill_md(name: str) -> Path | None:
    """Locate a SKILL.md for *name* on disk or in a local collection source."""

    for global_layer in (True, False):
        for harness in target_harnesses(global_layer=global_layer):
            for directory in skill_dirs(harness, global_layer=global_layer):
                candidate = directory / name / "SKILL.md"
                if candidate.is_file():
                    return candidate

    source = Path(collection_source())
    if source.is_dir():
        if name == MANAGER:
            candidate = source / "skills" / MANAGER / "SKILL.md"
            if candidate.is_file():
                return candidate
        matches = list((source / "skills").glob(f"*/{name}/SKILL.md"))
        if matches:
            return matches[0]
    return None


def help_section(text: str) -> str:
    """Return the Help section of a SKILL.md, or the whole body after frontmatter."""

    marker = "## Help"
    start = text.find(marker)
    if start < 0:
        end = text.find("\n---", 3)
        return text[end + 4 :].strip() if end >= 0 else text.strip()
    rest = text[start:]
    next_heading = rest.find("\n## ", 1)
    if next_heading >= 0:
        rest = rest[:next_heading]
    return rest.strip()


def cmd_help(name: str | None) -> int:
    """Print help for the manager or one named collection skill."""

    if not name or name == MANAGER:
        print(MANAGER_HELP, end="")
        return 0
    if name not in catalog_names() and name != MANAGER:
        raise ManagerError(f"unknown skill '{name}'")
    path = find_skill_md(name)
    if path is None:
        entry = next(
            (item for item in catalog_skills() if item.get("name") == name), None
        )
        description = entry.get("description", "") if entry else ""
        print(f"{name}\n\n{description}\n\nEnable this skill to read its full help.")
        return 0
    print(help_section(path.read_text(encoding="utf-8")))
    return 0


# The frontmatter parser reads a restricted YAML subset with no block scalars,
# so `description: >` yields this indicator as the value. Generation is where
# that has to fail: past it the character ships as the skill's whole help text.
BLOCK_SCALARS = frozenset({">", "|", ">-", "|-", ">+", "|+"})


def generate_catalog(source: Path) -> dict[str, Any]:
    """Build a Catalog from SKILL.md files under *source*/skills."""

    entries: list[dict[str, Any]] = []
    skills_root = source / "skills"
    for skill_md in sorted(skills_root.glob("*/*/SKILL.md")):
        category = skill_md.parent.parent.name
        frontmatter = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = str(frontmatter.get("name") or skill_md.parent.name)
        if name == MANAGER:
            continue
        deps = skill_deps(frontmatter)
        description = str(frontmatter.get("description") or "")

        # Generation is where a misspelt Capability has to fail. Past this
        # point the name would ride into the Catalog and only surface when a
        # user ran the skill. The same is true of the two fields the Catalog
        # exists to carry: the transport installs by directory name, and the
        # description is a skill's entire help until it is Enabled.
        capability_notes(deps["capabilities"])
        if name != skill_md.parent.name:
            raise ManagerError(
                f"{skill_md}: name '{name}' is not the directory "
                f"'{skill_md.parent.name}'; the transport installs by directory"
            )
        if not description:
            raise ManagerError(f"{skill_md}: description is empty")
        if description in BLOCK_SCALARS:
            raise ManagerError(
                f"{skill_md}: description '{description}' is a YAML block "
                "scalar, which the frontmatter parser does not support; "
                "write it on one line"
            )
        entries.append(
            {
                "name": name,
                "category": category,
                "description": description,
                "binaries": deps["binaries"],
                "skills": deps["skills"],
                "externals": deps["externals"],
                "capabilities": deps["capabilities"],
            }
        )
    return {"origin": ORIGIN, "skills": entries}


def cmd_catalog(*, write: bool) -> int:
    """Print a generated Catalog from a local collection source."""

    source = Path(collection_source())
    if not source.is_dir():
        raise ManagerError(
            "KNTNT_SOURCE must be a local collection to generate the Catalog"
        )
    catalog = generate_catalog(source)
    text = json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"
    if write:
        path = here() / "catalog.json"
        path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


def add_project_flag(parser: argparse.ArgumentParser) -> None:
    """Add the --project flag that defaults to Global."""

    parser.add_argument("--project", choices=("on", "off"), default="off")


def add_yes_flag(parser: argparse.ArgumentParser) -> None:
    """Add --yes to a verb.

    Every verb takes it, so passing the user's flag through is never a crash.
    It only carries meaning where something is asked or deleted.
    """

    parser.add_argument("--yes", action="store_true")


def normalize_argv(argv: list[str]) -> list[str]:
    """Turn bare `--project` into `--project on` so it cannot steal a skill name."""

    normalized: list[str] = []
    for arg in argv:
        if arg == "--project":
            normalized.extend(["--project", "on"])
        elif arg.startswith("--project="):
            normalized.extend(["--project", arg.split("=", 1)[1]])
        else:
            normalized.append(arg)
    return normalized


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the manager CLI."""

    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    status = sub.add_parser("status", help="Report Enabled and Disabled.")
    status.add_argument("skills", nargs="*")
    add_yes_flag(status)

    help_cmd = sub.add_parser("help", help="Print help.")
    help_cmd.add_argument("skill", nargs="?")
    add_yes_flag(help_cmd)

    check = sub.add_parser("check", help="Refuse when a Dependency is Unsatisfied.")
    check.add_argument("--here", required=True, type=Path)

    catalog = sub.add_parser(
        "catalog", help="Generate the Catalog from a local source."
    )
    catalog.add_argument("--write", action="store_true")

    plan = sub.add_parser("plan", help="Print a JSON plan and stop.")
    plan_sub = plan.add_subparsers(dest="verb", required=True)
    plan_enable = plan_sub.add_parser("enable")
    plan_enable.add_argument("skills", nargs="*")
    add_project_flag(plan_enable)
    add_yes_flag(plan_enable)
    plan_disable = plan_sub.add_parser("disable")
    plan_disable.add_argument("skills", nargs="*")
    add_project_flag(plan_disable)
    add_yes_flag(plan_disable)
    plan_update = plan_sub.add_parser("update")
    add_project_flag(plan_update)
    add_yes_flag(plan_update)

    apply = sub.add_parser("apply", help="Apply a plan.")
    apply_sub = apply.add_subparsers(dest="verb", required=True)
    apply_enable = apply_sub.add_parser("enable")
    apply_enable.add_argument("skills", nargs="*")
    add_project_flag(apply_enable)
    add_yes_flag(apply_enable)
    apply_disable = apply_sub.add_parser("disable")
    apply_disable.add_argument("skills", nargs="*")
    add_project_flag(apply_disable)
    add_yes_flag(apply_disable)
    apply_update = apply_sub.add_parser("update")
    add_project_flag(apply_update)
    add_yes_flag(apply_update)

    return parser.parse_args(argv)


def dispatch(args: argparse.Namespace) -> int:
    """Run the parsed command."""

    if args.command == "status":
        return cmd_status(args.skills)
    if args.command == "help":
        return cmd_help(args.skill)
    if args.command == "check":
        return cmd_check(args.here)
    if args.command == "catalog":
        return cmd_catalog(write=args.write)
    if args.command == "plan":
        if args.verb == "update":
            return cmd_plan_update(global_layer=parse_layer(args.project))
        global_layer = parse_layer(args.project)
        if args.verb == "enable":
            return cmd_plan_enable(args.skills, global_layer=global_layer)
        return cmd_plan_disable(args.skills, global_layer=global_layer)
    if args.verb == "update":
        return cmd_apply_update(global_layer=parse_layer(args.project))
    global_layer = parse_layer(args.project)
    if args.verb == "enable":
        return cmd_apply_enable(args.skills, global_layer=global_layer)
    return cmd_apply_disable(args.skills, global_layer=global_layer, yes=args.yes)


def main(argv: list[str] | None = None) -> int:
    """Dispatch a manager command. Return an exit code."""

    raw = normalize_argv(list(sys.argv[1:] if argv is None else argv))
    if not raw:
        raw = ["help"]
    args = parse_args(raw)
    try:
        return dispatch(args)
    except ManagerError as exc:
        return fail(str(exc), exc.code)


if __name__ == "__main__":
    raise SystemExit(main())
