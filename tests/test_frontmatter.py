"""The frontmatter the Manager reads a skill's declaration out of."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType
from typing import Any, cast

REPO_ROOT = Path(__file__).resolve().parent.parent
KNTNT_PY = REPO_ROOT / "skills" / "kntnt" / "scripts" / "kntnt.py"
SKILLS = REPO_ROOT / "skills"

# The six frontmatter fields the Agent Skills specification defines, which is
# also the closed allowlist its reference validator refuses everything else on.
SPECIFIED_FIELDS = frozenset(
    {
        "allowed-tools",
        "compatibility",
        "description",
        "license",
        "metadata",
        "name",
    }
)

# The two Claude Code fields ADR-0066 accepts on top of them, and the record
# that accepts them.
HARNESS_FIELDS = frozenset({"argument-hint", "disable-model-invocation"})
DEVIATION_RECORD = (
    REPO_ROOT
    / "docs"
    / "adr"
    / "0066-the-reference-validator-is-a-baseline-not-a-gate.md"
)


def _manager() -> ModuleType:
    """Import the manager's script as a module.

    Reading frontmatter is a function and no verb of its own, so the CLI
    cannot reach it directly, and this is the lowest layer that constrains it
    at all.
    """

    # The loader API answers with optionals, so both are narrowed before use:
    # a missing script is a broken checkout and has to say which file.
    spec = importlib.util.spec_from_file_location("kntnt_manager", KNTNT_PY)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import the manager from {KNTNT_PY}")

    # Execute the script under its own module object and hand that back.
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


kntnt = _manager()


def _frontmatter(relative: str) -> dict[str, Any]:
    """Parse the frontmatter of one shipped SKILL.md."""

    # The manager is imported dynamically, so everything it answers with is
    # `Any` as far as the type checker is concerned; the cast is what lets this
    # helper declare the shape it actually returns.
    text = (SKILLS / relative).read_text(encoding="utf-8")
    return cast(dict[str, Any], kntnt.parse_frontmatter(text))


def test_every_shipped_skill_carries_the_fields_the_catalog_reads() -> None:
    """Name, description, and the marker are what a Catalog entry is made of."""

    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))

    # A glob that matched nothing would pass every assertion below it, which is
    # the one outcome this test exists to catch.
    assert skill_mds

    for skill_md in skill_mds:
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        assert frontmatter.get("name") == skill_md.parent.name, skill_md
        assert frontmatter.get("description"), skill_md
        assert kntnt.collection_block(frontmatter) is not None, skill_md


def test_the_manager_carries_no_collection_block() -> None:
    """The Manager is no Catalog entry, and the sweep must never read it as one."""

    assert kntnt.collection_block(_frontmatter("kntnt/SKILL.md")) is None


def test_a_description_holding_a_colon_survives_the_parser() -> None:
    """agents-md's description opens with `AGENTS.md:`, and the value is the whole line."""

    description = _frontmatter("agents/agents-md/SKILL.md")["description"]

    assert description.startswith("AGENTS.md: create, shrink, or tend")
    assert '"' not in description


def test_the_shipped_skills_declare_the_lists_the_checker_refuses_on() -> None:
    """Every dependency list, read off the files the collection ships."""

    assert kntnt.skill_deps(_frontmatter("code/commit/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": [],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/push/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": ["commit"],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/release/SKILL.md")) == {
        "binaries": ["git", "uv"],
        "skills": ["push"],
        "externals": [],
        "capabilities": [],
    }
    assert kntnt.skill_deps(_frontmatter("code/orchestrate/SKILL.md")) == {
        "binaries": ["git", "gh", "uv"],
        "skills": [],
        "externals": [],
        "capabilities": ["subagents"],
    }
    assert kntnt.skill_deps(_frontmatter("agents/delegation/SKILL.md")) == {
        "binaries": ["uv"],
        "skills": [],
        "externals": [],
        "capabilities": ["subagents"],
    }


def test_a_skill_whose_frontmatter_is_broken_is_not_ours(tmp_path: Path) -> None:
    """A layer holds files the collection did not write, so bad YAML answers.

    The parser raises where the subset used to skip the line it could not
    read, and a traceback in place of the report is the failure of issue #5.
    """

    skill_dir = tmp_path / "stranger"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text(
        '---\nname: alpha\ndescription: "unterminated\nmetadata: [oops\n---\n',
        encoding="utf-8",
    )

    assert kntnt.carries_marker(skill_dir) is False


def test_text_with_no_frontmatter_is_no_frontmatter() -> None:
    assert kntnt.parse_frontmatter("# alpha\n\nA skill.\n") == {}


def test_unterminated_frontmatter_is_no_frontmatter() -> None:
    """A truncated file must answer empty rather than half a skill's declaration."""

    assert kntnt.parse_frontmatter("---\nname: alpha\n") == {}


def test_every_shipped_skill_declares_metadata_the_specification_allows() -> None:
    """`metadata` is a map from string keys to string values, and nothing else.

    A reader outside this collection holds the specification to that and
    coerces whatever else it is given rather than refusing it: a nested map
    arrives as a Python repr and a boolean as its `str()`, so a declaration in
    any other shape is lost without a word being said (issue #52).
    """

    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))

    # A glob that matched nothing would pass every assertion below it.
    assert skill_mds

    for skill_md in skill_mds:
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        metadata = frontmatter.get("metadata")
        assert isinstance(metadata, dict), skill_md
        for key, value in metadata.items():
            assert isinstance(key, str), (skill_md, key)
            assert isinstance(value, str), (skill_md, key)


def test_every_shipped_skill_keeps_its_metadata_keys_under_the_collection() -> None:
    """One flat namespace, prefixed, so no key of ours is anybody else's.

    The specification asks for reasonably unique key names, and `internal`
    bare is the opposite of that: every collection that hides a skill from
    discovery has reason to write it, and the last one to write it wins.
    """

    for skill_md in sorted(SKILLS.glob("*/*/SKILL.md")):
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        for key in frontmatter["metadata"]:
            assert key.startswith("kntnt."), (skill_md, key)


def test_a_skill_with_nothing_to_declare_carries_the_marker_anyway() -> None:
    """Four empty keys are what a skill with no Dependencies writes.

    The marker used to be the block's presence, so a skill with nothing under
    it needed an empty map spelled out for the key to survive parsing. It is
    now any `kntnt.` key at all, and the four lists written empty carry it.
    """

    frontmatter = _frontmatter("agents/tldr/SKILL.md")

    assert kntnt.collection_block(frontmatter) is not None
    assert kntnt.skill_deps(frontmatter) == {
        "binaries": [],
        "skills": [],
        "externals": [],
        "capabilities": [],
    }


def test_a_dependency_list_is_read_off_a_space_separated_string() -> None:
    """The spec's own `allowed-tools` is one string for the same reason."""

    frontmatter = {"metadata": {"kntnt.binaries": "git gh uv"}}

    assert kntnt.skill_deps(frontmatter)["binaries"] == ["git", "gh", "uv"]


def test_metadata_holding_no_key_of_ours_is_no_marker() -> None:
    """Another collection's `metadata` must never read as this one's mark."""

    assert kntnt.collection_block({"metadata": {"internal": "true"}}) is None
    assert kntnt.collection_block({"metadata": {}}) is None


def _names(compatibility: str, candidates: object) -> set[str]:
    """Return the *candidates* named as words in *compatibility*."""

    return {
        str(candidate)
        for candidate in cast(dict[str, Any], candidates)
        if re.search(rf"\b{re.escape(str(candidate))}\b", compatibility)
    }


def test_every_shipped_skill_states_its_dependencies_in_compatibility() -> None:
    """`compatibility` and the dependency block name the same requirements.

    `compatibility` is the one field a consumer outside this collection knows
    to read, and the same fact stated twice drifts. So every binary the
    checker refuses on is named there, nothing the checker does not refuse on
    is named there without being a soft requirement listed below, and a skill
    with nothing to declare carries no field at all (issue #53).
    """

    # `gh` is the case the dependency block deliberately cannot hold: release
    # step 9 degrades to a report when it is missing, so refusing on it would
    # be wrong and leaving it unsaid would be a lie about the requirement.
    soft: dict[str, set[str]] = {"release": {"gh"}}

    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))

    # A glob that matched nothing would pass every assertion below it.
    assert skill_mds

    for skill_md in skill_mds:
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        deps = kntnt.skill_deps(frontmatter)
        compatibility = frontmatter.get("compatibility", "")
        assert isinstance(compatibility, str), skill_md

        # The specification bounds the field at 500 characters, and a skill
        # with no requirement to state omits it rather than writing it empty.
        assert 0 < len(compatibility) <= 500 or not compatibility, skill_md

        # Every hard dependency is stated, and every binary the checker knows
        # that is stated is one this skill hard-requires or softly needs.
        named = _names(compatibility, kntnt.BINARY_HOW)
        allowed = set(deps["binaries"]) | soft.get(skill_md.parent.name, set())
        assert set(deps["binaries"]) <= named, skill_md
        assert named <= allowed, skill_md
        assert _names(compatibility, kntnt.CAPABILITIES) == set(deps["capabilities"]), (
            skill_md
        )


def _shipped_skill_mds() -> list[Path]:
    """Every SKILL.md the collection ships, the Manager's among them."""

    return sorted(SKILLS.glob("*/*/SKILL.md")) + sorted(SKILLS.glob("*/SKILL.md"))


def test_shipped_frontmatter_stays_within_the_recorded_deviation() -> None:
    """The specification's six fields, plus the two ADR-0066 names, and no third.

    The reference validator rejects every skill here on `argument-hint` and
    `disable-model-invocation`, which the collection ships knowingly because
    the harness reads them nowhere else. That deviation is bounded by the
    record rather than open: a skill added later that carries a third field
    outside the specification fails here until the record accepts it too
    (issue #63).
    """

    record = DEVIATION_RECORD.read_text(encoding="utf-8")
    for field in sorted(HARNESS_FIELDS):
        assert f"`{field}`" in record, field

    skill_mds = _shipped_skill_mds()

    # A glob that matched nothing would pass every assertion below it.
    assert skill_mds

    allowed = SPECIFIED_FIELDS | HARNESS_FIELDS
    for skill_md in skill_mds:
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        assert set(frontmatter) <= allowed, (
            skill_md,
            sorted(set(frontmatter) - allowed),
        )


def test_both_deviating_fields_are_still_in_use() -> None:
    """A record accepting a field nothing writes any more is a record to withdraw."""

    written: set[str] = set()
    for skill_md in _shipped_skill_mds():
        written |= set(kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8")))

    assert HARNESS_FIELDS <= written
