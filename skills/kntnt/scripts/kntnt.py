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
BINARY_HOW = {
    "uv": "install uv from https://docs.astral.sh/uv/",
    "git": "install git",
    "gh": "install GitHub CLI (gh) from https://cli.github.com/",
}
MANAGER_HELP = """\
kntnt — manage this collection

Usage: /kntnt [subcommand] [skill...] [--project[=on|off]] [--yes]

Subcommands:
  help [skill]         this help, or help for one named collection skill
  status [skill...]    report Enabled/Disabled in Global and Project
  setup                record the Harness list
  enable [skill...]    make skills Enabled (picker if none named)
  disable [skill...]   make skills Disabled (picker if none named)
  update               refresh this collection and re-check Dependencies

Options:
  --project    act on this Project instead of Global (--project=off is Global)
  --yes        assume yes; ask nothing that can be answered yes or no

Bare /kntnt is this help. Status lists every Catalog skill, Enabled or not.
Enable, Disable, and Update default to Global.
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


def skill_deps(frontmatter: dict[str, Any]) -> dict[str, list[str]]:
    """Read Dependency lists from a skill's frontmatter."""

    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        return {"binaries": [], "skills": [], "externals": []}
    block = metadata.get("kntnt")
    if not isinstance(block, dict):
        return {"binaries": [], "skills": [], "externals": []}
    result: dict[str, list[str]] = {}
    for key in ("binaries", "skills", "externals"):
        values = block.get(key, [])
        result[key] = [str(item) for item in values] if isinstance(values, list) else []
    return result


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


def harness_list_path() -> Path:
    """Return the path Setup writes the Harness list to."""

    return home() / ".config" / "kntnt" / "harnesses.json"


def read_harness_list_file() -> list[str] | None:
    """Return the stored Harness list, or None if it is missing or corrupt."""

    path = harness_list_path()
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    harnesses = data.get("harnesses")
    if not isinstance(harnesses, list) or not all(
        isinstance(item, str) for item in harnesses
    ):
        return None
    return list(harnesses)


def write_harness_list(harnesses: list[str]) -> None:
    """Persist the Harness list."""

    path = harness_list_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"harnesses": harnesses}, indent=2) + "\n", encoding="utf-8"
    )


def collection_skill_present(directory: Path) -> bool:
    """True when *directory* holds a collection skill other than the Manager."""

    names = catalog_names()
    if not directory.is_dir():
        return False
    for child in directory.iterdir():
        if child.name == MANAGER:
            continue
        if child.name in names and (child / "SKILL.md").is_file():
            return True
    return False


def rebuild_harness_list() -> list[str]:
    """Rebuild the Harness list from Global disks that hold a collection skill."""

    found: list[str] = []
    for harness, spec in harness_paths().items():
        template = spec.get("global")
        if not template:
            continue
        directory = expand_path(template, global_layer=True)
        if collection_skill_present(directory):
            found.append(harness)
    if found:
        write_harness_list(found)
    return found


def require_harnesses() -> list[str]:
    """Return the Harness list, rebuilding if needed. Raise when Unsatisfied."""

    stored = read_harness_list_file()
    if stored:
        return stored
    rebuilt = rebuild_harness_list()
    if rebuilt:
        return rebuilt
    raise ManagerError("Harness list is unsatisfied; run /kntnt setup", 2)


def optional_harnesses() -> list[str]:
    """Return the Harness list, or an empty list when Unsatisfied."""

    try:
        return require_harnesses()
    except ManagerError:
        return []


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
        if any((directory / name / "SKILL.md").is_file() for directory in directories):
            present += 1
    if checked == 0 or present == 0:
        return "disabled"
    if present == checked:
        return "enabled"
    return "partial"


def enabled_names(harnesses: list[str], *, global_layer: bool) -> list[str]:
    """Return Catalog skills Enabled in *layer* on any recorded Harness."""

    names: list[str] = []
    for entry in catalog_skills():
        name = str(entry["name"])
        if skill_state(name, harnesses, global_layer=global_layer) != "disabled":
            names.append(name)
    return names


def detected_harnesses() -> list[str]:
    """Return harness ids whose Global parent directory exists."""

    found: list[str] = []
    for harness, spec in harness_paths().items():
        template = spec.get("global")
        if not template:
            continue
        directory = expand_path(template, global_layer=True)
        if directory.parent.is_dir():
            found.append(harness)
    return found


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


def add_skills(names: list[str], harnesses: list[str], *, global_layer: bool) -> None:
    """Enable *names* on *harnesses* in the targeted layer."""

    if not names or not harnesses:
        return
    args = ["add", collection_source()]
    for name in names:
        args.extend(["--skill", name])
    for harness in harnesses:
        args.extend(["--agent", harness])
    if global_layer:
        args.append("--global")
    args.append("--yes")
    run_transport(args, internal=True)


def remove_skills(
    names: list[str], harnesses: list[str], *, global_layer: bool
) -> None:
    """Disable *names* on *harnesses* in the targeted layer."""

    if not names or not harnesses:
        return
    args = ["remove", *names]
    for harness in harnesses:
        args.extend(["--agent", harness])
    if global_layer:
        args.append("--global")
    args.append("--yes")
    run_transport(args, internal=True)


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

    stored = read_harness_list_file()
    if stored is None:
        stored = rebuild_harness_list() or None
    harnesses = stored or []
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
                "global": skill_state(name, harnesses, global_layer=True),
                "project": skill_state(name, harnesses, global_layer=False),
            }
        )
    return {
        "harness_list": "ok" if harnesses else "unsatisfied",
        "harnesses": harnesses,
        "skills": skills,
    }


def picker_payload(
    names: list[str], *, global_layer: bool, action: str
) -> dict[str, Any]:
    """Group Catalog skills by Category for an interactive Enable/Disable."""

    harnesses = require_harnesses()
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

    harnesses = require_harnesses()
    if not names:
        emit(picker_payload([], global_layer=global_layer, action="enable"))
        return 2
    wanted = validate_names(names)
    emit(
        {
            "action": "enable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "harnesses": harnesses,
        }
    )
    return 0


def cmd_plan_disable(names: list[str], *, global_layer: bool) -> int:
    """Print a Disable picker or a plan for the named skills."""

    harnesses = require_harnesses()
    if not names:
        emit(picker_payload([], global_layer=global_layer, action="disable"))
        return 2
    wanted = validate_names(names)
    emit(
        {
            "action": "disable",
            "layer": "global" if global_layer else "project",
            "skills": wanted,
            "harnesses": harnesses,
        }
    )
    return 0


def cmd_apply_enable(names: list[str], *, global_layer: bool) -> int:
    """Enable the named skills in the targeted layer."""

    wanted = validate_names(names)
    if not wanted:
        raise ManagerError("name at least one skill to enable", 2)
    harnesses = require_harnesses()
    already = {
        name
        for name in wanted
        if skill_state(name, harnesses, global_layer=global_layer) == "enabled"
    }
    changing = [name for name in wanted if name not in already]
    add_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            "changed": changing,
            "noop": [name for name in wanted if name in already],
            "layer": "global" if global_layer else "project",
            "harnesses": harnesses,
        }
    )
    return 0


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
    harnesses = require_harnesses()
    changing: list[str] = []
    noop: list[str] = []
    for name in wanted:
        state = skill_state(name, harnesses, global_layer=global_layer)
        if state == "disabled":
            noop.append(name)
            continue
        changing.append(name)
    remove_skills(changing, harnesses, global_layer=global_layer)
    emit(
        {
            "changed": changing,
            "noop": noop,
            "layer": "global" if global_layer else "project",
            "harnesses": harnesses,
        }
    )
    return 0


def cmd_plan_setup() -> int:
    """Print detected Harnesses, pre-checking those that should stay selected."""

    current = read_harness_list_file() or []
    detected = detected_harnesses()
    selected = set(current) if current else set(detected)
    items = []
    seen: set[str] = set()
    for harness in [*detected, *current]:
        if harness in seen:
            continue
        seen.add(harness)
        items.append(
            {
                "id": harness,
                "present": harness in detected,
                "selected": harness in selected,
            }
        )
    emit(
        {
            "action": "setup",
            "detected": items,
            "current": current,
            "first": not current,
        }
    )
    return 0


def unique(items: list[str]) -> list[str]:
    """Return *items* without duplicates, keeping order."""

    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def cmd_apply_setup(harnesses: list[str], *, yes: bool) -> int:
    """Record the Harness list and apply Global skills to added Harnesses."""

    wanted = unique(harnesses)
    if not wanted:
        raise ManagerError("pass --harness for each Harness to keep", 2)
    known = harness_paths()
    for harness in wanted:
        if harness not in known:
            raise ManagerError(f"unknown harness '{harness}'")

    current = read_harness_list_file() or []
    added = [harness for harness in wanted if harness not in current]
    removed = [harness for harness in current if harness not in wanted]
    if removed and not yes:
        raise ManagerError(
            f"removing {', '.join(removed)} deletes this collection's skills there; pass --yes",
            2,
        )

    globally_enabled = enabled_names(current, global_layer=True) if current else []
    if added:
        add_skills([MANAGER], added, global_layer=True)
        add_skills(globally_enabled, added, global_layer=True)
    if removed:
        drop = [*sorted(catalog_names()), MANAGER]
        remove_skills(drop, removed, global_layer=True)

    write_harness_list(wanted)
    changed = [*added, *removed]
    emit({"changed": changed, "harnesses": wanted, "removed": removed, "added": added})
    return 0


def cmd_plan_update(*, global_layer: bool) -> int:
    """Print which Enabled skills Update will refresh."""

    harnesses = require_harnesses()
    refresh = enabled_names(harnesses, global_layer=global_layer)
    if global_layer:
        refresh = [MANAGER, *refresh]
    emit(
        {
            "action": "update",
            "layer": "global" if global_layer else "project",
            "refresh": refresh,
            "harnesses": harnesses,
        }
    )
    return 0


def cmd_apply_update(*, global_layer: bool) -> int:
    """Refresh this collection, report new Catalog entries, re-check Dependencies."""

    harnesses = require_harnesses()
    old_names = catalog_names()
    desired = enabled_names(harnesses, global_layer=global_layer)
    refresh = [MANAGER, *desired] if global_layer else list(desired)

    # The transport's own `update` compares SKILL.md and skips a skill whose
    # SKILL.md is unchanged, leaving sidecars — catalog.json, helper documents,
    # scripts — frozen at the revision that last touched SKILL.md. `add`
    # re-copies the whole directory and is idempotent, so it is the refresh.
    add_skills(refresh, harnesses, global_layer=global_layer)

    # That reaches only the recorded Harnesses, which need not hold the copy of
    # the Manager running right now. Refresh its Catalog directly, or Status goes
    # on reporting the snapshot this Manager shipped with.
    catalog_refreshed = True
    try:
        write_catalog(fetch_catalog())
    except ManagerError:
        catalog_refreshed = False

    current_names = catalog_names()
    new_names = [name for name in sorted(current_names) if name not in old_names]
    removed_names = [name for name in sorted(old_names) if name not in current_names]
    unsatisfied: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for harness in harnesses:
        for directory in skill_dirs(harness, global_layer=global_layer):
            for name in desired:
                skill_dir = directory / name
                if not (skill_dir / "SKILL.md").is_file():
                    continue
                for item in unsatisfied_at(skill_dir):
                    key = (item["kind"], item["name"], item["how"])
                    if key in seen:
                        continue
                    seen.add(key)
                    unsatisfied.append(item)

    emit(
        {
            "new": new_names,
            "removed": removed_names,
            "refreshed": refresh,
            "catalog_refreshed": catalog_refreshed,
            "unsatisfied": unsatisfied,
            "layer": "global" if global_layer else "project",
        }
    )
    return 0


def unsatisfied_at(skill_dir: Path) -> list[dict[str, str]]:
    """Return Unsatisfied Dependencies declared in *skill_dir*/SKILL.md."""

    path = skill_dir / "SKILL.md"
    if not path.is_file():
        raise ManagerError(f"no SKILL.md at {skill_dir}")
    deps = skill_deps(parse_frontmatter(path.read_text(encoding="utf-8")))
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

    for harness in optional_harnesses() or detected_harnesses():
        for global_layer in (True, False):
            if any(
                (directory / name / "SKILL.md").is_file()
                for directory in skill_dirs(harness, global_layer=global_layer)
            ):
                return True
    return False


def cmd_check(skill_dir: Path) -> int:
    """Refuse when a Dependency at *skill_dir* is Unsatisfied."""

    missing = unsatisfied_at(skill_dir)
    if missing:
        emit({"ok": False, "unsatisfied": missing})
        return 2
    emit({"ok": True, "unsatisfied": []})
    return 0


def find_skill_md(name: str) -> Path | None:
    """Locate a SKILL.md for *name* on disk or in a local collection source."""

    for harness in optional_harnesses() or detected_harnesses():
        for global_layer in (True, False):
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
        entries.append(
            {
                "name": name,
                "category": category,
                "description": str(frontmatter.get("description") or ""),
                "binaries": deps["binaries"],
                "skills": deps["skills"],
                "externals": deps["externals"],
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
    add_yes_flag(plan_sub.add_parser("setup"))
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
    apply_setup = apply_sub.add_parser("setup")
    apply_setup.add_argument("--harness", action="append", default=[])
    add_yes_flag(apply_setup)
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
        if args.verb == "setup":
            return cmd_plan_setup()
        if args.verb == "update":
            return cmd_plan_update(global_layer=parse_layer(args.project))
        global_layer = parse_layer(args.project)
        if args.verb == "enable":
            return cmd_plan_enable(args.skills, global_layer=global_layer)
        return cmd_plan_disable(args.skills, global_layer=global_layer)
    if args.verb == "setup":
        return cmd_apply_setup(args.harness, yes=args.yes)
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
