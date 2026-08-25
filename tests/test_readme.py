"""The README's Skill sections, and the Catalog they are supposed to describe."""

from __future__ import annotations

import json
import re
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
CATALOG = REPO_ROOT / "skills" / "kntnt" / "catalog.json"

# Every Skill gets a `### <name>` section under `## Usage`, and the Manager's
# verbs are documented in the prose above them rather than as sections of their
# own — so the heading level is what separates the two.
SECTION = re.compile(r"^### (\S+)$", re.MULTILINE)


def _documented() -> set[str]:
    """The Skill names the README's Usage part gives a section of its own."""

    usage = README.read_text(encoding="utf-8").partition("\n## Usage\n")[2]
    return set(SECTION.findall(usage.partition("\n## ")[0]))


def _catalogued() -> set[str]:
    """The Skill names the Catalog carries an entry for."""

    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    return {entry["name"] for entry in catalog["skills"]}


def test_the_readme_documents_exactly_the_skills_the_catalog_names() -> None:
    """A Skill nobody wrote a section for is a Skill the README hides.

    Both lists are authored by hand and neither is generated from the other —
    the collection's stance being that a text a reviewer can diff beats a
    regenerated one — so the only thing that keeps them together is this
    comparison. Adding a Skill and forgetting its section was caught by nobody
    before it (issue #69), and a section left behind by a withdrawn Skill
    advertises something `/kntnt select` no longer offers.

    **What this does not cover.** The paragraph that closes the Usage part —
    which Skills need which binaries and which Capabilities — is prose, and
    prose cannot be held against the dependency declarations without being
    generated from them, which this collection declines to do. It is read by
    eye, exactly like a `compatibility` field's soft requirements (ADR-0109),
    and a Skill whose dependencies change without that paragraph changing is
    still caught by nobody. See `docs/rules/skills.md`.
    """

    documented = _documented()
    catalogued = _catalogued()

    # A heading shape this pattern stopped matching, or a Usage heading that
    # moved, would leave two empty sets and pass regardless.
    assert documented

    assert documented == catalogued, (
        "the README's Usage sections and the Catalog's entries name one set of "
        "Skills between them: undocumented "
        f"{sorted(catalogued - documented)}, unshipped "
        f"{sorted(documented - catalogued)}. A Skill with no section is a Skill "
        "the README hides, and a section with no Skill advertises something "
        f"`/kntnt select` no longer offers. See {STANDARD}."
    )
