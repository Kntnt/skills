"""Release selection through the existing Manager refresh boundary."""

from __future__ import annotations

import shutil
from pathlib import Path

from test_kntnt import (
    _apply_update,
    _present,
    _publication_artifacts,
    _transport_add,
    _world,
)


def test_update_publishes_a_manager_without_editorial_support(tmp_path: Path) -> None:
    """A selected origin must replace the old complete Manager generation.

    Editorial support is not required by any retained Manager verb. Refresh
    must accept its absence and retire it with the old generation.
    """

    world = _world(tmp_path)
    _present(world, "home", ".claude")
    assert _transport_add(world, "kntnt").returncode == 0
    installed = world["home"] / ".claude" / "skills" / "kntnt"
    library = world["source"] / "skills" / "kntnt" / "library"

    # The origin selects only support for retained non-editorial behavior.
    for relative in ("references/editorial", "references/languages"):
        path = library / relative
        if path.exists():
            shutil.rmtree(path)
    for relative in (
        "scripts/languages.py",
        "scripts/article_anatomy.py",
        "references/delivery.md",
    ):
        (library / relative).unlink(missing_ok=True)

    result = _apply_update(world, installed=installed)

    assert result.returncode == 0, result.stdout + result.stderr
    assert (installed / "library" / "scripts" / "ship.py").is_file()
    assert not (installed / "library" / "scripts" / "languages.py").exists()
    assert not (installed / "library" / "references" / "editorial").exists()
    assert _publication_artifacts(tmp_path) == []
