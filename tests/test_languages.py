"""CLI behaviour of the Collection Library's Language Resource resolver."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library"
LANGUAGES = LIBRARY / "scripts" / "languages.py"
RESOURCES = LIBRARY / "references" / "languages"

# The four scopes a Language Resource carries, each named for the guidance it
# holds rather than for the Skill that reads it.
SCOPES = ("composition", "review", "anti-slop", "mechanics")

# The exit codes the resolver distinguishes its refusals with. A caller that
# guesses is exactly what this engine exists to make unnecessary, so each
# refusal has a code of its own rather than one shared failure.
ABSENT = 3
AMBIGUOUS = 4
MALFORMED = 5
INHERITANCE = 6


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    """Drive the shipped resolver from its installed location."""

    return subprocess.run(
        ["uv", "run", str(LANGUAGES), *args],
        text=True,
        capture_output=True,
        check=False,
    )


def _resolve(selector: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Resolve *selector* against the inventory the collection ships."""

    return _run("resolve", selector, *args)


def _json(result: subprocess.CompletedProcess[str]) -> Any:
    """Parse the engine's stdout, reporting stderr when it is not JSON."""

    assert result.stdout, result.stderr
    return json.loads(result.stdout)


def _resource(directory: Path, name: str, frontmatter: str, body: str = "") -> Path:
    """Write one Language Resource into a temporary inventory."""

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(f"---\n{frontmatter}---\n\n{body}", encoding="utf-8")
    return path


def _all_scopes(marker: str) -> str:
    """Return a body carrying all four scopes, each tagged with *marker*."""

    return "".join(
        f"## {heading}\n\n{marker} {heading.lower()}\n\n"
        for heading in ("Composition", "Review", "Anti-slop", "Mechanics")
    )


def _tree(directory: Path) -> dict[str, bytes]:
    """Snapshot every file under *directory*, so a write cannot go unnoticed."""

    return {
        str(path.relative_to(directory)): path.read_bytes()
        for path in sorted(directory.rglob("*"))
        if path.is_file()
    }


# --- The shipped inventory ------------------------------------------------


def test_the_collection_ships_the_three_initial_language_resources() -> None:
    """Swedish, British English, and American English, and nothing half-there."""

    result = _run("list")

    assert result.returncode == 0, result.stderr
    codes = {entry["code"] for entry in _json(result)["resources"]}
    assert codes == {"sv", "en_GB", "en_US"}


def test_a_canonical_code_resolves_to_its_own_resource() -> None:
    """The plainest selector there is: the code the resource declares."""

    result = _resolve("en_GB")

    assert result.returncode == 0, result.stderr
    assert _json(result)["code"] == "en_GB"


def test_a_canonical_code_normalises_across_case_and_separator() -> None:
    """`en-GB`, `EN_GB`, and `en_gb` are one language, not three."""

    for selector in ("en-GB", "EN_GB", "en_gb", "En-gB"):
        result = _resolve(selector)

        assert result.returncode == 0, result.stderr
        assert _json(result)["code"] == "en_GB", selector


def test_curated_aliases_reach_their_resource() -> None:
    """A human name and an abbreviation select as surely as a code does."""

    expected = {
        "british english": "en_GB",
        "BrE": "en_GB",
        "brittisk engelska": "en_GB",
        "american english": "en_US",
        "AmE": "en_US",
        "svenska": "sv",
        "Swedish": "sv",
    }

    for selector, code in expected.items():
        result = _resolve(selector)

        assert result.returncode == 0, result.stderr
        assert _json(result)["code"] == code, selector


def test_bare_english_resolves_to_the_declared_british_default() -> None:
    """No central table decides this; the British resource declares it."""

    for selector in ("en", "english"):
        result = _resolve(selector)

        assert result.returncode == 0, result.stderr
        assert _json(result)["code"] == "en_GB", selector

    listed = {entry["code"]: entry for entry in _json(_run("list"))["resources"]}
    assert "en" in listed["en_GB"]["default_for"]
    assert "en" not in listed["en_US"]["default_for"]


def test_bare_swedish_resolves_to_the_shipped_swedish_default() -> None:
    """The Swedish resource owns the bare selector it answers to."""

    result = _resolve("sv")

    assert result.returncode == 0, result.stderr
    assert _json(result)["code"] == "sv"

    listed = {entry["code"]: entry for entry in _json(_run("list"))["resources"]}
    assert "sv" in listed["sv"]["default_for"]


def test_en_uk_is_neither_a_code_nor_an_alias_anywhere() -> None:
    """The Collection does not institutionalise a locale code that does not exist."""

    result = _resolve("en_UK")

    assert result.returncode == ABSENT
    assert "no-such-language" in result.stderr

    for path in sorted(LIBRARY.rglob("*")):
        if path.is_file():
            assert b"en_UK" not in path.read_bytes(), path


def test_every_shipped_resource_populates_all_four_scopes() -> None:
    """A scope nobody wrote is a caller that gets nothing where it asked."""

    for code in ("sv", "en_GB", "en_US"):
        result = _resolve(code, *[f"--scope={scope}" for scope in SCOPES])

        assert result.returncode == 0, result.stderr
        scopes = _json(result)["scopes"]
        assert set(scopes) == set(SCOPES), code
        for name, scope in scopes.items():
            assert scope["content"].strip(), f"{code}: {name} is empty"
            assert scope["source"] == code


def test_the_shipped_resources_validate() -> None:
    """What a contributor runs after adding a locale must pass on what ships."""

    result = _run("validate")

    assert result.returncode == 0, result.stderr
    assert _json(result)["problems"] == []


def test_swedish_imported_punctuation_errors_resolve_only_as_mechanics() -> None:
    """A mechanical pass receives every planted Swedish punctuation error."""

    result = _resolve("sv", "--scope=anti-slop", "--scope=mechanics")

    assert result.returncode == 0, result.stderr
    scopes = _json(result)["scopes"]
    mechanics = scopes["mechanics"]["content"]
    anti_slop = scopes["anti-slop"]["content"]
    errors = (
        "*Dessutom, är det viktigt*",
        "*snabbare—det*",
        "*“kundresa”*",
        "*teknik, processer, och kultur*",
        "*Service & support*",
    )

    for error in errors:
        assert error in mechanics, error
        assert error not in anti_slop, error


def test_english_dash_and_connective_conventions_resolve_as_mechanics() -> None:
    """Both English locales settle the punctuation baits a pass encounters."""

    for code in ("en_GB", "en_US"):
        result = _resolve(code, "--scope=anti-slop", "--scope=mechanics")

        assert result.returncode == 0, result.stderr
        mechanics = _json(result)["scopes"]["mechanics"]["content"]
        assert "*Therefore we did*" in mechanics, code
        assert "*Therefore, we did*" in mechanics, code

    british = _json(_resolve("en_GB", "--scope=anti-slop", "--scope=mechanics"))[
        "scopes"
    ]
    assert "*—like this—*" in british["mechanics"]["content"]
    assert "*—like this—*" not in british["anti-slop"]["content"]

    american = _json(_resolve("en_US", "--scope=mechanics"))["scopes"]["mechanics"][
        "content"
    ]
    assert "*like — this*" in american
    assert "*like—this*" in american


# --- Scope selection ------------------------------------------------------


def test_only_the_requested_scopes_are_returned() -> None:
    """A caller applying the anti-slop pass alone never pays for the rest."""

    result = _resolve("sv", "--scope=anti-slop")

    assert result.returncode == 0, result.stderr
    assert set(_json(result)["scopes"]) == {"anti-slop"}


def test_an_unrequested_scope_leaves_no_trace_in_the_output(tmp_path: Path) -> None:
    """Absent means absent: not an empty key, and not the text under another."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("marker"))

    result = _run("resolve", "xa", "--scope=review", f"--resources={tmp_path}")

    assert result.returncode == 0, result.stderr
    assert "marker review" in result.stdout
    for absent in ("marker composition", "marker anti-slop", "marker mechanics"):
        assert absent not in result.stdout


def test_requesting_no_scope_returns_identity_alone() -> None:
    """Selecting a language is a question a caller may ask without a body."""

    result = _resolve("en_US")

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["code"] == "en_US"
    assert payload["scopes"] == {}


def test_two_scopes_are_returned_and_the_other_two_are_not() -> None:
    """Redline reads three of four; the fourth must be absent, not empty."""

    result = _resolve("en_GB", "--scope=composition", "--scope=review")

    assert result.returncode == 0, result.stderr
    assert set(_json(result)["scopes"]) == {"composition", "review"}


def test_an_unknown_scope_name_is_refused(tmp_path: Path) -> None:
    """A flag value the engine has no work for is an error, never a guess."""

    result = _resolve("sv", "--scope=proofreading")

    assert result.returncode == 2
    assert not list(tmp_path.iterdir())


def test_an_unknown_subcommand_is_refused() -> None:
    """The grammar is strict, as every other engine in the Collection is."""

    result = _run("resolv", "sv")

    assert result.returncode == 2


# --- Temporary inventories ------------------------------------------------


def test_a_selector_matching_two_resources_is_ambiguous(tmp_path: Path) -> None:
    """Two curated aliases can collide, and the answer is never a guess."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\naliases: [nordic]\n")
    _resource(tmp_path, "xb.md", "code: xb\nlanguage: Beta\naliases: [nordic]\n")

    result = _run("resolve", "nordic", f"--resources={tmp_path}")

    assert result.returncode == AMBIGUOUS
    assert "ambiguous-selector" in result.stderr
    assert "xa" in result.stderr and "xb" in result.stderr


def test_two_resources_claiming_one_default_are_ambiguous(tmp_path: Path) -> None:
    """A declared default is only a default while one resource declares it."""

    _resource(tmp_path, "xa.md", "code: xa_AA\nlanguage: Alpha\ndefault-for: [xa]\n")
    _resource(tmp_path, "xb.md", "code: xa_BB\nlanguage: Alpha\ndefault-for: [xa]\n")

    result = _run("resolve", "xa", f"--resources={tmp_path}")

    assert result.returncode == AMBIGUOUS
    assert "ambiguous-selector" in result.stderr


def test_an_absent_language_names_what_is_installed(tmp_path: Path) -> None:
    """The agent's semantic retry needs the inventory, not a guessed match."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("A"))

    result = _run("resolve", "klingon", f"--resources={tmp_path}")

    assert result.returncode == ABSENT
    assert "no-such-language" in result.stderr
    assert "xa" in result.stderr


def test_malformed_metadata_is_reported_rather_than_reinterpreted(
    tmp_path: Path,
) -> None:
    """Unparseable YAML in a resource is a defect, never an empty declaration."""

    _resource(tmp_path, "xa.md", "code: [xa\nlanguage: Alpha\n")

    result = _run("list", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "malformed-resource" in result.stderr
    assert "xa.md" in result.stderr


def test_a_resource_missing_its_canonical_code_is_malformed(tmp_path: Path) -> None:
    """Identity is the one thing frontmatter exists to carry."""

    _resource(tmp_path, "xa.md", "language: Alpha\n")

    result = _run("list", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "code" in result.stderr


def test_a_frontmatter_key_the_format_does_not_define_is_malformed(
    tmp_path: Path,
) -> None:
    """A misspelled field would otherwise be a selector nobody can reach."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\nalias: [alpha]\n")

    result = _run("list", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "alias" in result.stderr


def test_two_resources_claiming_one_canonical_code_are_malformed(
    tmp_path: Path,
) -> None:
    """A code names one resource, or nothing can say which it means."""

    _resource(tmp_path, "one.md", "code: xa\nlanguage: Alpha\n")
    _resource(tmp_path, "two.md", "code: XA\nlanguage: Alpha\n")

    result = _run("list", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "xa" in result.stderr.lower()


def test_an_alias_repeating_a_canonical_code_is_malformed(tmp_path: Path) -> None:
    """A curated alias carries a human name; the code already selects itself."""

    _resource(tmp_path, "xa.md", "code: xa_AA\nlanguage: Alpha\naliases: [xa-aa]\n")

    result = _run("list", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED


def test_a_scope_heading_the_format_does_not_define_is_malformed(
    tmp_path: Path,
) -> None:
    """A body section nothing can request is guidance nobody will ever read."""

    body = _all_scopes("A") + "## Proofreading\n\nstray\n"
    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", body)

    result = _run("resolve", "xa", "--scope=mechanics", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "Proofreading" in result.stderr


def test_a_base_resource_missing_a_scope_is_malformed(tmp_path: Path) -> None:
    """A resource that inherits from nothing has nowhere to borrow a scope from."""

    body = "## Composition\n\nA\n\n## Review\n\nA\n\n## Mechanics\n\nA\n"
    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", body)

    result = _run("resolve", "xa", "--scope=anti-slop", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED
    assert "anti-slop" in result.stderr


# --- Inheritance ----------------------------------------------------------


def _inheriting_inventory(tmp_path: Path) -> None:
    """A base language and one locale overriding a single scope."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("base"))
    _resource(
        tmp_path,
        "xa_FI.md",
        "code: xa_FI\nlanguage: Alpha\nterritory: FI\nterritory-name: Finland\n"
        "inherits: xa\n",
        "## Mechanics\n\nvariant mechanics\n",
    )


def test_a_variant_overrides_only_the_scope_it_writes(tmp_path: Path) -> None:
    """The whole point of inheritance: one file, only the genuine differences."""

    _inheriting_inventory(tmp_path)

    result = _run(
        "resolve",
        "xa_FI",
        "--scope=mechanics",
        "--scope=composition",
        f"--resources={tmp_path}",
    )

    assert result.returncode == 0, result.stderr
    payload = _json(result)
    assert payload["code"] == "xa_FI"
    assert payload["inherits"] == "xa"
    assert payload["scopes"]["mechanics"]["source"] == "xa_FI"
    assert "variant mechanics" in payload["scopes"]["mechanics"]["content"]
    assert payload["scopes"]["composition"]["source"] == "xa"
    assert "base composition" in payload["scopes"]["composition"]["content"]


def test_inheritance_from_an_absent_base_is_reported(tmp_path: Path) -> None:
    """A base nothing installs is an error, never a silently flattened resource."""

    _resource(
        tmp_path,
        "xa_FI.md",
        "code: xa_FI\nlanguage: Alpha\ninherits: xa\n",
        "## Mechanics\n\nvariant\n",
    )

    result = _run("resolve", "xa_FI", f"--resources={tmp_path}")

    assert result.returncode == INHERITANCE
    assert "inheritance-error" in result.stderr


def test_inheritance_of_more_than_one_step_is_reported(tmp_path: Path) -> None:
    """One step is the contract; a chain is a defect the caller has to see."""

    _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("base"))
    _resource(
        tmp_path,
        "xa_FI.md",
        "code: xa_FI\nlanguage: Alpha\ninherits: xa\n",
        "## Mechanics\n\nvariant\n",
    )
    _resource(
        tmp_path,
        "xa_AX.md",
        "code: xa_AX\nlanguage: Alpha\ninherits: xa_FI\n",
        "## Mechanics\n\nvariant\n",
    )

    result = _run("resolve", "xa_AX", f"--resources={tmp_path}")

    assert result.returncode == INHERITANCE
    assert "inheritance-error" in result.stderr


def test_a_resource_inheriting_from_itself_is_reported(tmp_path: Path) -> None:
    """The degenerate cycle is caught by the same rule as the long chain."""

    _resource(
        tmp_path,
        "xa.md",
        "code: xa\nlanguage: Alpha\ninherits: xa\n",
        _all_scopes("base"),
    )

    result = _run("resolve", "xa", f"--resources={tmp_path}")

    assert result.returncode == INHERITANCE


def test_a_scope_neither_the_variant_nor_its_base_carries_is_malformed(
    tmp_path: Path,
) -> None:
    """One step of inheritance answers, or the resource is incomplete."""

    _resource(
        tmp_path,
        "xa.md",
        "code: xa\nlanguage: Alpha\n",
        "## Composition\n\nbase\n\n## Review\n\nbase\n\n## Mechanics\n\nbase\n",
    )
    _resource(
        tmp_path,
        "xa_FI.md",
        "code: xa_FI\nlanguage: Alpha\ninherits: xa\n",
        "## Mechanics\n\nvariant\n",
    )

    result = _run("resolve", "xa_FI", "--scope=anti-slop", f"--resources={tmp_path}")

    assert result.returncode == MALFORMED


# --- What the engine reads, and what it never writes ----------------------


def test_inventorying_reads_frontmatter_and_never_the_body(tmp_path: Path) -> None:
    """A body that cannot be decoded proves the inventory never opened it."""

    path = _resource(tmp_path, "xa.md", "code: xa\nlanguage: Alpha\n")
    path.write_bytes(path.read_bytes() + b"## Composition\n\n\xff\xfe not text\n")

    listing = _run("list", f"--resources={tmp_path}")
    identity = _run("resolve", "xa", f"--resources={tmp_path}")
    scoped = _run("resolve", "xa", "--scope=composition", f"--resources={tmp_path}")

    assert listing.returncode == 0, listing.stderr
    assert identity.returncode == 0, identity.stderr
    assert scoped.returncode == MALFORMED


def test_resolving_writes_nothing(tmp_path: Path) -> None:
    """A resolver answers questions; a side effect here would be a surprise."""

    inventory = tmp_path / "inventory"
    _resource(inventory, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("base"))
    before = _tree(tmp_path)

    result = _run("resolve", "xa", "--scope=review", f"--resources={inventory}")

    assert result.returncode == 0, result.stderr
    assert _tree(tmp_path) == before


def test_a_refusal_writes_nothing(tmp_path: Path) -> None:
    """Neither does a refusal, which is the half a caller cannot see."""

    inventory = tmp_path / "inventory"
    _resource(inventory, "xa.md", "code: xa\nlanguage: Alpha\n", _all_scopes("base"))
    before = _tree(tmp_path)

    result = _run("resolve", "klingon", f"--resources={inventory}")

    assert result.returncode == ABSENT
    assert _tree(tmp_path) == before


# --- The format a contributor adding a locale reads -----------------------


def test_the_format_is_documented_beside_the_resources_it_describes() -> None:
    """A contributor adding a locale finds the contract where the files are."""

    page = (RESOURCES / "README.md").read_text(encoding="utf-8").casefold()

    for scope in SCOPES:
        assert scope in page
    for field in ("code", "aliases", "default-for", "inherits"):
        assert field in page


def test_the_format_places_objective_punctuation_only_in_mechanics() -> None:
    """Future resources keep mechanical rules reachable without duplicating them."""

    page = (RESOURCES / "README.md").read_text(encoding="utf-8")

    assert "An objectively wrong punctuation form belongs in Mechanics" in page
    assert "Anti-slop refers to that rule rather than restating it" in page
