"""The snapshot the Manager stores beside itself."""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from types import ModuleType
from typing import Any
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"

# Two snapshots that cannot be mistaken for one another, so an assertion about
# which of them the file holds says which write reached it.
OLD: dict[str, Any] = {"skills": [{"name": "alpha"}]}
NEW: dict[str, Any] = {"skills": [{"name": "beta"}]}


def _manager() -> ModuleType:
    """Import the manager's script as a module.

    The store is a function and no verb of its own, and reaching it directly
    is what lets a test make the rename fail — the one condition the property
    below is about, and one no run driven from the command line can arrange.
    """

    # The loader API answers with optionals, so both are narrowed before use:
    # a missing script is a broken checkout and has to say which file.
    spec = importlib.util.spec_from_file_location("kntnt_catalog", KNTNT_PY)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the manager from {KNTNT_PY}")

    # Register postponed annotations while executing the module object.
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


kntnt = _manager()


def test_a_stored_catalog_reaches_the_target_only_by_rename(tmp_path: Path) -> None:
    """The old snapshot survives a write that cannot complete.

    A write in place would leave the target truncated where this leaves it
    untouched, and the reader treats a damaged snapshot as no snapshot at all
    — so the property that has to hold is that the new bytes reach the target
    by the rename or not at all.
    """

    stored = tmp_path / "catalog.json"
    stored.write_text(json.dumps(OLD), encoding="utf-8")

    # Fail the rename and nothing else: what the run does before it is exactly
    # what an interrupted run would already have done.
    with (
        mock.patch.dict(os.environ, {"KNTNT_HERE": str(tmp_path)}),
        mock.patch.object(Path, "replace", side_effect=OSError("interrupted")),
    ):
        raised = False
        try:
            kntnt.write_catalog(NEW)
        except OSError:
            raised = True

    assert json.loads(stored.read_text(encoding="utf-8")) == OLD
    assert list(tmp_path.iterdir()) == [stored]
    assert raised


def test_a_stored_catalog_leaves_no_sibling_behind(tmp_path: Path) -> None:
    """A write that completes hands the target over and keeps no second file."""

    with mock.patch.dict(os.environ, {"KNTNT_HERE": str(tmp_path)}):
        kntnt.write_catalog(NEW)

    assert json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8")) == NEW
    assert not list(tmp_path.glob("*.tmp"))
