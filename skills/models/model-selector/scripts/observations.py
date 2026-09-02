# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Adapt Model Selector's observation CLI to the Collection Library."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any


def _library() -> Any:
    """Load the shared routed-observation implementation in any shipped layout."""

    # Try the repository, installed Manager sibling, then Skill-local fallback.
    here = Path(__file__).resolve().parent
    candidates = (
        here.parent.parent.parent / "kntnt/library/scripts/routed_observations.py",
        here.parent.parent / "kntnt/library/scripts/routed_observations.py",
        here.parent / "library/scripts/routed_observations.py",
    )
    for candidate in candidates:
        if not candidate.exists():
            continue
        spec = importlib.util.spec_from_file_location(
            "kntnt_routed_observations", candidate
        )
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    raise RuntimeError(
        "routed observation mechanics are missing; install or update the Manager"
    )


# Re-export the one shared implementation through the established Skill seam.
_IMPLEMENTATION: Any = _library()
SCHEMA_VERSION: int = _IMPLEMENTATION.SCHEMA_VERSION
observe: Callable[[Any], dict[str, Any]] = _IMPLEMENTATION.observe
merge: Callable[[Any, list[dict[str, Any]]], dict[str, Any]] = _IMPLEMENTATION.merge
validate: Callable[[Any], dict[str, str] | None] = _IMPLEMENTATION.validate
record: Callable[[Any, Path], dict[str, Any]] = _IMPLEMENTATION.record
projected_evidence: Callable[[Path], dict[str, Any]] = (
    _IMPLEMENTATION.projected_evidence
)


def main(argv: list[str] | None = None) -> int:
    """Run the shared CLI adapter and return its process status."""

    return int(_IMPLEMENTATION.main(argv))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
