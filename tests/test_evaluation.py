"""The shared fixture corpus and the protocol an evaluation is run under."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATION = REPO_ROOT / "docs" / "evaluation"
PROTOCOL = EVALUATION / "protocol.md"
TEMPLATE = EVALUATION / "record-template.md"
CORPUS = EVALUATION / "corpus"
INDEX = CORPUS / "README.md"
MODEL_INVOKED_PROOFREAD_RECORD = (
    EVALUATION / "records" / "proofread-gpt-2026-08-26-170.md"
)

# The material the wave has to survive, one tag per kind. A fixture entry
# declares what it covers from this vocabulary, and the corpus is complete when
# every one of these is claimed by at least one entry (issue #101).
REQUIRED_COVERAGE = frozenset(
    {
        "short brief",
        "interview transcript",
        "long factual source",
        "clean prose",
        "mechanically flawed prose",
        "ai slop",
        "swedish ai slop",
        "code",
        "genre",
        "technique",
        "handoff metadata present",
        "handoff metadata conflicting",
        "partial handoff metadata",
        "unrelated frontmatter",
        "no frontmatter",
        "inline material",
        "local file material",
        "immutable url",
        "response default",
        "new file",
        "existing file",
        "existing directory",
        "derived-name collision",
        "read-only source",
        "in-place request",
    }
)

# Tags a fixture may also carry. They cover material the corpus is better for
# holding without the acceptance criteria naming it, and they are listed here
# so that a mistyped required tag cannot pass as an optional one.
OPTIONAL_COVERAGE = frozenset(
    {
        "ambiguous language",
        "locale mechanics",
        "no-change status",
        "refusal",
        "unusable metadata",
        "sentence-boundary punctuation",
    }
)

# Every fixture entry is a level-three heading naming the fixture, followed by
# the five bullets a reader needs before the fixture means anything: which
# files it is, what it covers, what the material is, how it is supplied, and
# what a correct run must never do with it.
ENTRY = re.compile(r"^### `([A-Za-z0-9_-]+)`$", re.MULTILINE)
FIELDS = ("Files", "Covers", "Material", "Use", "Reject")

# A field bullet is the field name in bold, an em dash, and its value.
FIELD = re.compile(r"^- \*\*([A-Za-z ]+)\*\* — (.+)$", re.MULTILINE)

# A path a field names, written the way every other path in this repository's
# prose is written.
PATH = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|txt))`")

# The Swedish Language Resource, whose `## Anti-slop` scope is loaded beside
# the shared catalogue whenever a Skill applies the anti-slop pass in Swedish.
# Its items are Swedish strings rather than patterns to be read semantically,
# so a fixture either carries them or does not.
SWEDISH = (
    REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "languages" / "sv.md"
)

# How an item is written inside that scope, and the shortest one worth
# matching on: the scope also italicises punctuation samples, which are not
# items a fixture can be said to carry.
ITEM = re.compile(r"\*([^*\n]+)\*")
ITEM_FLOOR = 4

# How many of that scope's items a fixture carries before it is concentrated
# slop rather than prose that happens to contain one of them.
SWEDISH_ITEMS = 12

# The three forms a code sample takes in Markdown. A pass reads past all of
# them, so a fixture staging only the fenced one leaves the other two to be
# settled per run, which is the defect ADR-0125 ends.
FENCE = re.compile(r"^ {0,3}(?:```|~~~)", re.MULTILINE)
FENCED_BLOCK = re.compile(r"^ {0,3}(```+|~~~+).*?^ {0,3}\1", re.MULTILINE | re.DOTALL)
INDENTED_CODE = re.compile(r"^(?: {4}|\t)\S", re.MULTILINE)
INLINE_CODE = re.compile(r"(?<!`)`[^`\n]+`(?!`)")

# What a code-carrying entry has to tell an evaluator before the fixture means
# anything: which forms the sample takes, that the code holds a mechanical
# error of its own, that nothing inside it is a finding, and that every byte of
# it survives.
CODE_FORMS = ("fenced", "indented", "inline")

# The parameters a Kntnt map may settle, and the three levels of the
# resolution order a single invocation can be made to exercise at once.
PARAMETERS = ("genre", "technique", "language")
LEVELS = ("invocation", "map", "contextual instruction")

# The leading YAML of a Text Artifact, and the Kntnt map inside it.
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
KNTNT = re.compile(r"^kntnt:\n((?:[ \t]+\S.*\n?)+)", re.MULTILINE)
KEY = re.compile(r"^[ \t]+([A-Za-z_-]+):", re.MULTILINE)

# The record fields an evaluation writes. A later cross-family comparison is
# made by reading records rather than by re-running anything, so a field
# absent from one family's records is a comparison that cannot be made.
RECORD_FIELDS = (
    "record",
    "date",
    "ticket",
    "skill",
    "provider family",
    "model",
    "harness",
    "corpus commit",
    "fixture",
    "invocation",
    "contextual instruction",
    "output target",
    "observed delivery",
    "side effects",
    "criteria",
    "unresolved findings",
    "defects filed",
    "notes",
)

# What blinded judging rejects however well the text reads. These are the
# specification's five, and they are what keeps a semantic criterion from
# degrading into approval of anything fluent.
REJECTIONS = (
    "unsupported fact",
    "wrong locale behaviour",
    "substantive edit",
    "unresolved mandatory finding",
    "incorrect side effect",
)

# Wording that would turn fixture material into an exact-prose assertion. The
# corpus supplies material and states what must not happen to it; it never
# supplies the sentence a model is supposed to write back.
FORBIDDEN = (
    "expected output",
    "exact output",
    "must produce exactly",
    "must output exactly",
    "verbatim output",
    "guaranteed to",
    "guarantees perfect",
)


def _index() -> str:
    return INDEX.read_text(encoding="utf-8")


def _protocol() -> str:
    return PROTOCOL.read_text(encoding="utf-8")


def _entries() -> dict[str, str]:
    """Map each fixture's name to the body of its entry in the index."""

    text = _index()
    starts = [(match.group(1), match.start()) for match in ENTRY.finditer(text)]
    bodies: dict[str, str] = {}
    for position, (name, start) in enumerate(starts):
        end = starts[position + 1][1] if position + 1 < len(starts) else len(text)
        bodies[name] = text[start:end]
    return bodies


def _fields(body: str) -> dict[str, str]:
    """Map each field name in one entry to the value written beside it."""

    return {match.group(1): match.group(2) for match in FIELD.finditer(body)}


def _fixture_files() -> set[str]:
    """Every fixture file the corpus carries, corpus-relative.

    The index and the staging notes beside it are prose about the corpus
    rather than material fed to a Skill, so they are not fixtures and are not
    expected to be listed as any entry's file.
    """

    return {
        str(path.relative_to(CORPUS))
        for path in CORPUS.rglob("*")
        if path.is_file() and path.name != "README.md"
    }


def _tagged(tag: str) -> dict[str, dict[str, str]]:
    """Every fixture claiming one coverage tag, mapped to its fields."""

    return {
        name: _fields(body)
        for name, body in _entries().items()
        if tag
        in {claim.strip() for claim in _fields(body).get("Covers", "").split(";")}
    }


def _material(fields: dict[str, str]) -> str:
    """The text of every file one fixture entry names, concatenated."""

    return "\n".join(
        (CORPUS / name).read_text(encoding="utf-8")
        for name in PATH.findall(fields.get("Files", ""))
    )


def _outside_fences(text: str) -> str:
    """One fixture's text with its fenced blocks taken out.

    An indented line and a backtick span inside a fence are part of the fenced
    sample rather than a second and third form of code, so they are removed
    before the other two are looked for.
    """

    return FENCED_BLOCK.sub("", text)


def _swedish_anti_slop_items() -> set[str]:
    """The items the Swedish Language Resource's own anti-slop scope names."""

    sections = SWEDISH.read_text(encoding="utf-8").split("\n## ")
    scope = next(part for part in sections if part.startswith("Anti-slop\n"))

    return {
        item.strip().lower()
        for item in ITEM.findall(scope)
        if len(item.strip()) >= ITEM_FLOOR and any(char.isalpha() for char in item)
    }


def _kntnt_keys(text: str) -> set[str]:
    """The keys the Kntnt map in a Text Artifact's leading YAML carries."""

    frontmatter = FRONTMATTER.match(text)
    if frontmatter is None:
        return set()

    block = KNTNT.search(frontmatter.group(1))

    return set() if block is None else set(KEY.findall(block.group(1)))


def test_the_corpus_lives_at_one_discoverable_location() -> None:
    """A fixture is reachable from the guide an agent always has loaded."""

    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert INDEX.exists()
    assert PROTOCOL.exists()
    assert TEMPLATE.exists()
    assert "docs/evaluation/protocol.md" in agents


def test_model_invoked_proofread_regression_observes_loaded_resources() -> None:
    """Both implicit triggers are judged at the rule-loading seam.

    A correct artifact cannot show which guidance was in context. The
    regression therefore records the Harness trace for both model-invocation
    branches and names the scoped resolver output and every admitted resource
    directly (issue #170).
    """

    text = MODEL_INVOKED_PROOFREAD_RECORD.read_text(encoding="utf-8")

    for heading in (
        "model trigger by proofreading term",
        "model trigger by mechanical-only request",
    ):
        start = text.index(f"## `flawed-en-US` — {heading}")
        end = text.find("\n## ", start + 1)
        entry = text[start:] if end == -1 else text[start:end]

        for evidence in (
            "Harness trace",
            "resolve --scope=mechanics",
            "only the `mechanics` scope",
            "editorial/mechanics.md",
            "No Language Resource file was opened",
            "no composition, review, or anti-slop guidance",
        ):
            assert evidence in entry, (
                f"{MODEL_INVOKED_PROOFREAD_RECORD}: the {heading} entry does"
                f" not record {evidence!r}, so its rule-loading verdict can"
                f" be inferred from the artifact instead of observed in the"
                f" Harness trace (issue #170)."
            )


def test_every_fixture_entry_documents_the_fixture_on_its_own() -> None:
    """An evaluator uses a fixture without reading the Skill that consumes it.

    The five fields are what makes that possible: which files the fixture is,
    what it covers, what the material actually is, how it reaches the Skill,
    and what a correct run must never do with it. An entry missing one of them
    sends the evaluator to the Skill for the answer, which is exactly the
    dependency the corpus exists to remove.
    """

    entries = _entries()

    # An index reworded out of the heading shape would leave nothing to judge
    # and pass regardless.
    assert entries

    incomplete = {
        name: sorted(set(FIELDS) - set(_fields(body)))
        for name, body in entries.items()
        if set(FIELDS) - set(_fields(body))
    }

    assert incomplete == {}


def test_the_corpus_covers_the_material_the_wave_has_to_survive() -> None:
    """Every kind the specification names is claimed by some fixture."""

    claimed: set[str] = set()
    for body in _entries().values():
        covers = _fields(body).get("Covers", "")
        claimed |= {tag.strip() for tag in covers.split(";") if tag.strip()}

    unknown = claimed - REQUIRED_COVERAGE - OPTIONAL_COVERAGE
    assert unknown == set(), (
        f"{unknown}: a fixture claims coverage this suite does not know, which"
        f" is either a mistyped required tag passing as an optional one or a"
        f" kind of material the vocabulary here has not caught up with."
    )

    assert REQUIRED_COVERAGE <= claimed, f"uncovered: {REQUIRED_COVERAGE - claimed}"


def test_the_index_and_the_corpus_directory_describe_the_same_fixtures() -> None:
    """A file nothing documents, and an entry pointing at nothing, both fail."""

    listed: set[str] = set()
    for body in _entries().values():
        listed |= set(PATH.findall(_fields(body).get("Files", "")))

    missing = {name for name in listed if not (CORPUS / name).exists()}
    assert missing == set(), f"{missing}: named by an entry, absent from disk"

    undocumented = _fixture_files() - listed
    assert undocumented == set(), (
        f"{undocumented}: present in the corpus and named by no entry, so an"
        f" evaluator meets material with no account of what it is for."
    )


def test_the_corpus_stages_concentrated_slop_in_swedish() -> None:
    """The anti-slop pass is asked for in a language the catalogue is not in.

    The shared catalogue is one condensed English document applied by what
    each pattern does, and every language carries its own scope of items
    beside it. A corpus whose only concentrated slop is English can say
    nothing about whether either half reaches Swedish: a run that finds no
    pattern in a text that has none has not shown that it would find one
    (issue #142).
    """

    items = _swedish_anti_slop_items()

    # A scope reworded out of its italics would leave nothing to count and
    # would pass whatever the fixture carried.
    assert len(items) >= SWEDISH_ITEMS

    fixtures = _tagged("swedish ai slop")
    assert fixtures

    thin = {
        name: len(carried)
        for name, fields in fixtures.items()
        if len(carried := {item for item in items if item in _material(fields).lower()})
        < SWEDISH_ITEMS
    }

    assert thin == {}, (
        f"{thin}: fewer than {SWEDISH_ITEMS} of the Swedish scope's own items,"
        f" which is a text that happens to contain slop rather than one that"
        f" stages it in concentration."
    )


def test_a_fixture_stages_both_sides_of_the_clause_boundary_rule() -> None:
    """A conditional rule is provable only where the corpus stages both answers.

    A comma joining two main clauses is an error where the second does not
    cohere with the first and correct usage where it does, and both shipped
    languages' authorities draw that line the same way. A corpus carrying only
    the accepted joint can say nothing about whether a run corrects the other,
    and a corpus carrying only the error would reward a Skill that corrects
    every such comma it meets (issue #125).
    """

    fixtures = _tagged("sentence-boundary punctuation")
    assert fixtures

    for name, fields in fixtures.items():
        described = f"{fields.get('Material', '')} {fields.get('Reject', '')}".lower()

        for half in ("explains", "unrelated"):
            assert half in described, (
                f"{name}: the entry does not say which of its comma-joined"
                f" clause pairs is the error and which is established usage, so"
                f" an evaluator has to derive the conditional from the prose."
            )

        assert "joint" in described, (
            f"{name}: the entry says nothing about how the erroneous joint is"
            f" corrected, and a correction free to reach past it is the"
            f" substantive edit the protocol rejects."
        )


def test_a_fixture_leaves_a_kntnt_map_partial_for_a_lower_level_to_settle() -> None:
    """Level 3 exists to settle what levels 1 and 2 leave open.

    A complete map settles every parameter the invocation does not, so a
    corpus carrying only complete maps can stage any two of the first three
    levels and never all three. The fixture that carries a partial map is
    where a flag, a metadata value, and a contextual value settle three
    different parameters in one invocation, and its entry says which
    parameter each level is expected to settle so that an evaluator stages
    the case rather than deriving it (issue #142).
    """

    fixtures = _tagged("partial handoff metadata")
    assert fixtures

    for name, fields in fixtures.items():
        carried = _kntnt_keys(_material(fields)) & set(PARAMETERS)
        assert 0 < len(carried) < len(PARAMETERS), (
            f"{name}: a map carrying {sorted(carried)} leaves no parameter for"
            f" a level below it to settle."
        )

        use = fields.get("Use", "").lower()
        unnamed = [word for word in PARAMETERS + LEVELS if word not in use]
        assert unnamed == [], f"{name}: the staging leaves {unnamed} to be derived"


def test_the_protocol_states_what_blinded_judging_rejects() -> None:
    """A semantic criterion tolerates several texts and still says no.

    Blinded judging without a stated floor becomes approval of whatever reads
    well, so the five rejections are written down and are what a criterion is
    checked against however the output is worded.
    """

    protocol = _protocol().lower()

    assert "blinded" in protocol

    unstated = [rejection for rejection in REJECTIONS if rejection not in protocol]
    assert unstated == [], f"{unstated}: rejected regardless of wording, unstated"


def test_the_protocol_defines_a_recording_format_the_template_carries() -> None:
    """Two families compare their runs by reading records, not by re-running.

    So the format is defined once and materialised as a skeleton an evaluation
    fills in. A field the protocol names and the template omits is a field the
    second family's run will not have recorded when the comparison is made.
    """

    protocol = _protocol().lower()
    template = TEMPLATE.read_text(encoding="utf-8").lower()

    undefined = [field for field in RECORD_FIELDS if field not in protocol]
    assert undefined == [], f"{undefined}: recording fields the protocol omits"

    unrecorded = [field for field in RECORD_FIELDS if field not in template]
    assert unrecorded == [], f"{unrecorded}: recording fields the template omits"


def test_the_protocol_isolates_the_provider_families_in_both_directions() -> None:
    """The isolation rule binds whoever runs an evaluation, both ways round.

    Stated in one direction only, it reads as a rule about Codex that a Claude
    session may ignore. Both sentences are therefore present, and so is the
    consequence: the shared corpus is run in provider-native sessions and
    compared from the records afterwards.
    """

    protocol = _protocol().lower()

    assert "a codex session runs only gpt-family evaluations" in protocol
    assert "a claude session runs only claude-family evaluations" in protocol
    assert "cross-provider orchestration" in protocol


def test_nothing_in_the_corpus_or_the_protocol_asserts_exact_prose() -> None:
    """Fixture material, not a snapshot of sentences a model has to write.

    The corpus states what the material is and what must not happen to it. A
    fixture that also carried the answer would turn a semantic criterion into
    a string comparison and would fail every model that wrote something else
    that was true.
    """

    sources = sorted(EVALUATION.rglob("*.md"))

    # A corpus moved out from under this glob would leave nothing to judge.
    assert sources

    offending: dict[str, list[str]] = {}
    for path in sources:
        text = path.read_text(encoding="utf-8").lower()
        found = [phrase for phrase in FORBIDDEN if phrase in text]
        if found:
            offending[str(path.relative_to(REPO_ROOT))] = found

    assert offending == {}


def test_the_url_fixture_names_a_source_that_cannot_change_under_a_run() -> None:
    """Two families run the corpus at different times against one text.

    A live page would let the material move between the runs, and the records
    would then disagree about a difference neither model made.
    """

    entries = _entries()
    urls = [
        name
        for name, body in entries.items()
        if "immutable url" in _fields(body).get("Covers", "")
    ]

    assert urls

    for name in urls:
        body = entries[name]
        assert "https://" in body, f"{name}: claims a URL source and names none"


def test_the_corpus_stages_code_a_pass_has_to_read_past() -> None:
    """A code sample is quoted material, and the corpus has to hold some.

    Every editorial Skill is under a preservation obligation that names code,
    and ADR-0125 settles what a sample is to a pass: quoted material whose
    contents produce no findings and are never altered. Neither claim is
    answerable from a corpus carrying no code, which is what sent one
    evaluation to run-local probe material the other provider family had
    nothing to mirror (issue #150).

    A fixture stages all three forms a sample takes, because a pass that reads
    past a fence and edits an indented block honours none of the rule; it
    carries a mechanical error inside the code, because the tempting change is
    the one a mechanical pass makes on the way past; and its prose earns
    findings, because a run that changes nothing has shown nothing about what
    it leaves alone.
    """

    fixtures = _tagged("code")
    assert fixtures

    for name, fields in fixtures.items():
        material = _material(fields)
        assert FENCE.search(material), f"{name}: stages no fenced block"

        outside = _outside_fences(material)
        assert INDENTED_CODE.search(outside), (
            f"{name}: stages no indented block outside its fences, so the form"
            f" a pass is likeliest to mistake for prose is missing."
        )
        assert INLINE_CODE.search(outside), f"{name}: stages no inline code span"

        described = f"{fields.get('Material', '')} {fields.get('Reject', '')}".lower()

        absent = [form for form in CODE_FORMS if form not in described]
        assert absent == [], (
            f"{name}: the entry does not say the fixture carries {absent} code,"
            f" so an evaluator has to find the forms by reading the material."
        )

        assert "mechanical" in described, (
            f"{name}: the entry says nothing about the mechanical error inside"
            f" the code, which is the correction a pass must not make and the"
            f" one this fixture exists to catch."
        )

        reject = fields.get("Reject", "").lower()
        assert "finding" in reject, (
            f"{name}: the entry does not reject a finding located inside the"
            f" code, which is half of what ADR-0125 settles."
        )
        assert "byte" in reject, (
            f"{name}: the entry does not reject the code coming back altered,"
            f" which is the other half."
        )
