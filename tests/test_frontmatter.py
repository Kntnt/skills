"""The frontmatter the Manager reads a skill's declaration out of."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path
from types import ModuleType
from typing import Any, cast

import yaml
from support.contract import STANDARD

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
        assert frontmatter.get("name") == skill_md.parent.name, (
            f"{skill_md}: `name` is the skill's directory name exactly, because"
            f" that is the name the Catalog identifies it by and the name a"
            f" user types to invoke it. See {STANDARD}."
        )
        assert frontmatter.get("description"), (
            f"{skill_md}: every skill declares a `description`. It is the only"
            f" hook a harness has for deciding when the skill applies"
            f" (ADR-0019), and it is what a Catalog row shows. See {STANDARD}."
        )
        assert kntnt.collection_block(frontmatter) is not None, (
            f"{skill_md}: every skill carries at least one `kntnt.`-prefixed"
            f" `metadata` key. The prefix is the marker the Manager recognises"
            f" its own by, and a skill without one is never refreshed or"
            f" removed by it (ADR-0061). See {STANDARD}."
        )


def test_the_manager_carries_no_collection_block() -> None:
    """The Manager is no Catalog entry, and the sweep must never read it as one."""

    assert kntnt.collection_block(_frontmatter("kntnt/SKILL.md")) is None


def test_a_description_holding_a_colon_survives_the_parser() -> None:
    """agents-md's description opens with `AGENTS.md:`, and the value is the whole line."""

    description = _frontmatter("agents/agents-md/SKILL.md")["description"]

    assert description.startswith("AGENTS.md: create, shrink, or tend")
    assert '"' not in description


def test_every_shipped_skill_declares_the_lists_the_checker_refuses_on() -> None:
    """All four lists written out, on every skill the collection ships.

    Held by the keys' presence rather than by what `skill_deps` makes of
    them, because that reading cannot tell the two cases apart: a key nobody
    wrote and a list written empty both come back empty, and only one of them
    is a declaration. So the frontmatter is read for the keys themselves, and
    the skills are discovered rather than named — a guard that listed them
    would hold nothing against the next skill added.
    """

    skill_mds = sorted(SKILLS.glob("*/*/SKILL.md"))

    # A glob that matched nothing would pass every assertion below it.
    assert skill_mds

    for skill_md in skill_mds:
        metadata = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))[
            "metadata"
        ]
        for kind in kntnt.DEP_KINDS:
            key = f"{kntnt.METADATA_PREFIX}{kind}"
            assert key in metadata, (
                f"{skill_md}: `metadata.{key}` is not written. All four"
                f" dependency lists are declared even where they are empty,"
                f" because a key nobody wrote is read as an empty list — the"
                f" same answer a skill that genuinely requires nothing gives,"
                f" so the omission cannot be seen (ADR-0012). Write it as an"
                f" empty string. See {STANDARD}."
            )


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
        assert isinstance(metadata, dict), (
            f"{skill_md}: `metadata` is a map from string keys to string"
            f" values, and every skill declares one (ADR-0061). See {STANDARD}."
        )
        for key, value in metadata.items():
            assert isinstance(key, str), (
                f"{skill_md}: the `metadata` key {key!r} is not a string. The"
                f" specification allows no other kind of key, and YAML reads an"
                f" unquoted `true` or `1` as neither (ADR-0060). See {STANDARD}."
            )
            assert isinstance(value, str), (
                f"{skill_md}: `metadata.{key}` holds {value!r}, which is not a"
                f" string. A reader outside this collection coerces any other"
                f" shape rather than refusing it, so a nested map arrives as a"
                f" Python repr and a boolean as its `str()` — the declaration is"
                f" lost without a word being said (ADR-0061). Write a list as"
                f" one space-separated string. See {STANDARD}."
            )


def test_every_shipped_skill_keeps_its_metadata_keys_under_the_collection() -> None:
    """One flat namespace, prefixed, so no key of ours is anybody else's.

    The specification asks for reasonably unique key names, and `internal`
    bare is the opposite of that: every collection that hides a skill from
    discovery has reason to write it, and the last one to write it wins.
    """

    for skill_md in sorted(SKILLS.glob("*/*/SKILL.md")):
        frontmatter = kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        for key in frontmatter["metadata"]:
            assert key.startswith("kntnt."), (
                f"{skill_md}: the `metadata` key `{key}` carries no `kntnt.`"
                f" prefix, and has to be written `kntnt.{key}`. `metadata` is"
                f" one flat namespace shared with every other collection, so an"
                f" unprefixed key is one anybody may claim and the last writer"
                f" of it wins (ADR-0061). See {STANDARD}."
            )


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
        assert isinstance(compatibility, str), (
            f"{skill_md}: `compatibility` is a string, being the field a"
            f" foreign reader reads a skill's environment requirements out of"
            f" (ADR-0062). See {STANDARD}."
        )

        # The specification bounds the field at 500 characters, and a skill
        # with no requirement to state omits it rather than writing it empty.
        assert 0 < len(compatibility) <= 500 or not compatibility, (
            f"{skill_md}: `compatibility` runs to {len(compatibility)}"
            f" characters, and the specification bounds it at 500. A skill with"
            f" no requirement to state carries no field at all rather than an"
            f" empty one (ADR-0062). See {STANDARD}."
        )

        # Every hard dependency is stated, and every binary the checker knows
        # that is stated is one this skill hard-requires or softly needs.
        named = _names(compatibility, kntnt.BINARY_HOW)
        allowed = set(deps["binaries"]) | soft.get(skill_md.parent.name, set())
        assert set(deps["binaries"]) <= named, (
            f"{skill_md}: `compatibility` names none of"
            f" {sorted(set(deps['binaries']) - named)}, which the dependency"
            f" declaration refuses the skill on. `compatibility` is the one"
            f" field a reader outside this collection knows to look at, so a"
            f" requirement left out of it reads as a requirement that is not"
            f" there (ADR-0062). See {STANDARD}."
        )
        assert named <= allowed, (
            f"{skill_md}: `compatibility` names {sorted(named - allowed)}, which"
            f" the dependency declaration does not hold. The two state one set"
            f" of binaries between them; the exception is a requirement the"
            f" skill degrades gracefully without, which is named in"
            f" `compatibility` in prose, deliberately kept out of the"
            f" declaration the checker refuses on, and listed in this test"
            f" (ADR-0062). See {STANDARD}."
        )
        assert _names(compatibility, kntnt.CAPABILITIES) == set(deps["capabilities"]), (
            f"{skill_md}: `compatibility` and the dependency declaration name"
            f" different Capabilities —"
            f" {sorted(_names(compatibility, kntnt.CAPABILITIES))} against"
            f" {sorted(deps['capabilities'])}. A Capability is stated as the"
            f" Capability and never as the harness product that has one"
            f" (ADR-0062, ADR-0030). See {STANDARD}."
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
            f"{skill_md}: the frontmatter carries"
            f" {sorted(set(frontmatter) - allowed)}, outside the six fields the"
            f" specification defines and the two ADR-0066 accepts on top of"
            f" them. The reference validator refuses every field it does not"
            f" know, so a third deviation is one the record has to accept"
            f" before it is shipped. See {STANDARD}."
        )


def test_both_deviating_fields_are_still_in_use() -> None:
    """A record accepting a field nothing writes any more is a record to withdraw."""

    written: set[str] = set()
    for skill_md in _shipped_skill_mds():
        written |= set(kntnt.parse_frontmatter(skill_md.read_text(encoding="utf-8")))

    assert HARNESS_FIELDS <= written


# Where a harness that does not read the frontmatter above finds the same two
# facts. Codex reads a skill's user-facing name and its invocation policy out
# of `agents/openai.yaml` and out of nothing else, so a skill declaring them
# only in its frontmatter arrives there unnamed and implicitly invocable.
SIDECAR = "agents/openai.yaml"


def _sidecar(directory: Path) -> dict[str, Any]:
    """Parse the Codex sidecar one shipped skill carries beside its SKILL.md."""

    path = directory / SIDECAR
    assert path.is_file(), (
        f"{path}: every skill the collection ships carries this sidecar. It is"
        f" where Codex reads the skill's user-facing name and its invocation"
        f" policy, neither of which it takes from the frontmatter, so a skill"
        f" without one is nameless in its picker and implicitly invocable"
        f" whatever the frontmatter says. See {STANDARD}."
    )

    return cast(dict[str, Any], yaml.safe_load(path.read_text(encoding="utf-8")))


def test_every_shipped_skill_names_itself_to_codex() -> None:
    """The sidecar's `interface` block is the skill's name in a picker.

    A `description` is written for a harness deciding when a skill applies and
    reads as an instruction rather than a label; the two fields here are
    written for a human reading a list, which is why the sidecar carries its
    own rather than pointing at the frontmatter's.
    """

    for skill_md in _shipped_skill_mds():
        interface = _sidecar(skill_md.parent).get("interface") or {}
        for field in ("display_name", "short_description"):
            value = interface.get(field)
            assert isinstance(value, str) and value.strip(), (
                f"{skill_md.parent / SIDECAR}: `interface.{field}` is missing"
                f" or empty. Both are what Codex shows a user choosing between"
                f" skills, and neither has a fallback it could take from the"
                f" frontmatter. See {STANDARD}."
            )


def test_the_sidecar_says_what_the_frontmatter_says_about_invocation() -> None:
    """One fact, written once per harness, and the two copies have to agree.

    `disable-model-invocation` and `allow_implicit_invocation` are the same
    decision under two spellings, and the failure they guard against is silent:
    a skill meant to run only when a user asks for it, arriving in Codex free
    to be invoked on a prompt that merely resembles its description. Both
    harnesses default to allowing it, and neither default is leaned on — a
    skill that says nothing has not decided, it has only failed to write the
    decision down, and the two spellings can then disagree without either
    file changing.
    """

    for skill_md in _shipped_skill_mds():
        declared = _frontmatter(str(skill_md.relative_to(SKILLS))).get(
            "disable-model-invocation"
        )
        assert isinstance(declared, bool), (
            f"{skill_md}: `disable-model-invocation` is {declared!r}. Every"
            f" skill writes it, `false` included, because the field is how the"
            f" collection says whose the invocation is and an unwritten field"
            f" says only that nobody decided. See {STANDARD}."
        )

        policy = _sidecar(skill_md.parent).get("policy") or {}
        expected = {"allow_implicit_invocation": not declared}
        assert policy == expected, (
            f"{skill_md.parent / SIDECAR}: the `policy` block is"
            f" {policy or 'absent'} where the frontmatter's"
            f" `disable-model-invocation: {str(declared).lower()}` makes it"
            f" {expected}. The two are one decision spelled twice, and Codex"
            f" reads only this copy. See {STANDARD}."
        )
