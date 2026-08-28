"""The content Digest: one computation, run on the collection and on the disk."""

from __future__ import annotations

import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"
CATALOG_JSON = REPO_ROOT / "skills" / "kntnt" / "catalog.json"


def _manager() -> ModuleType:
    """Import the manager's script as a module.

    The consuming side of the Digest is a function and not yet a verb — Select
    and Update are what will call it — so the CLI cannot reach it, and this is
    the lowest layer that constrains the computation at all.
    """

    # The loader API answers with optionals, so both are narrowed before use:
    # a missing script is a broken checkout and has to say which file.
    spec = importlib.util.spec_from_file_location("kntnt_digest", KNTNT_PY)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the manager from {KNTNT_PY}")

    # Register postponed annotations while executing the module object.
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


kntnt = _manager()


def _skill(directory: Path) -> Path:
    """Write a skill directory shaped like the ones the collection ships."""

    (directory / "scripts").mkdir(parents=True)
    (directory / "SKILL.md").write_text("---\nname: alpha\n---\n", encoding="utf-8")
    (directory / "help.md").write_text("# alpha\n", encoding="utf-8")
    (directory / "scripts" / "alpha.py").write_text(
        "print('alpha')\n", encoding="utf-8"
    )
    return directory


def _cache(directory: Path) -> None:
    """Leave behind what running a Python script leaves behind."""

    (directory / "scripts" / "__pycache__").mkdir(parents=True)
    (directory / "scripts" / "__pycache__" / "alpha.cpython-312.pyc").write_bytes(
        b"\x00compiled"
    )
    (directory / "scripts" / "stray.pyc").write_bytes(b"\x00compiled")


def test_a_copy_of_a_skill_digests_the_same_on_both_sides(tmp_path: Path) -> None:
    """The two sides are one computation, so identical files answer identically."""

    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")

    assert kntnt.directory_digest(installed) == kntnt.directory_digest(source)


def test_an_edited_file_changes_the_digest(tmp_path: Path) -> None:
    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")

    (installed / "help.md").write_text("# alpha, by hand\n", encoding="utf-8")

    assert kntnt.directory_digest(installed) != kntnt.directory_digest(source)


def test_a_renamed_file_changes_the_digest(tmp_path: Path) -> None:
    """Paths go into the digest, or a rename would pass for the same skill."""

    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")

    (installed / "help.md").rename(installed / "usage.md")

    assert kntnt.directory_digest(installed) != kntnt.directory_digest(source)


def test_an_added_file_changes_the_digest(tmp_path: Path) -> None:
    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")

    (installed / "notes.md").write_text("mine\n", encoding="utf-8")

    assert kntnt.directory_digest(installed) != kntnt.directory_digest(source)


def test_a_removed_file_changes_the_digest(tmp_path: Path) -> None:
    """A truncated install is what no version number could ever see."""

    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")

    (installed / "scripts" / "alpha.py").unlink()

    assert kntnt.directory_digest(installed) != kntnt.directory_digest(source)


def test_a_skill_that_has_been_run_does_not_deviate(tmp_path: Path) -> None:
    """A signal that is always on is a signal nobody reads (ADR-0041)."""

    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")
    _cache(installed)

    assert kntnt.directory_digest(installed) == kntnt.directory_digest(source)


def test_the_maintainer_s_own_cache_does_not_deviate_either(tmp_path: Path) -> None:
    """The list is applied identically on the producing side."""

    source = _skill(tmp_path / "collection" / "alpha")
    installed = shutil.copytree(source, tmp_path / "harness" / "alpha")
    _cache(source)

    assert kntnt.directory_digest(installed) == kntnt.directory_digest(source)


def test_the_ignore_list_is_exactly_the_two_python_artefacts() -> None:
    """One list, defined once, or the two sides could never agree."""

    assert kntnt.DIGEST_IGNORE == ("__pycache__/", "*.pyc")


def test_every_catalog_entry_carries_a_digest_and_the_manager_carries_none() -> None:
    """The Manager is no Catalog entry, so it has no Digest to compare."""

    catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    names = {entry["name"] for entry in catalog["skills"]}

    assert "kntnt" not in names
    assert names
    for entry in catalog["skills"]:
        assert len(entry["digest"]) == 64, entry["name"]


def test_an_installed_copy_matches_the_digest_the_catalog_carries(
    tmp_path: Path,
) -> None:
    """What the collection ships and what a harness holds answer the same value."""

    catalog = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    for entry in catalog["skills"]:
        shipped = REPO_ROOT / "skills" / entry["category"] / entry["name"]
        installed = shutil.copytree(shipped, tmp_path / entry["name"])
        assert kntnt.directory_digest(installed) == entry["digest"], entry["name"]
