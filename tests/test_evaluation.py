"""The shared fixture corpus and the protocol an evaluation is run under."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from support.editorial import ordinary_technique, ordinary_technique_section

REPO_ROOT = Path(__file__).resolve().parent.parent
EVALUATION = REPO_ROOT / "docs" / "evaluation"
PROTOCOL = EVALUATION / "protocol.md"
TEMPLATE = EVALUATION / "record-template.md"
CORPUS = EVALUATION / "corpus"
INDEX = CORPUS / "README.md"
MODEL_INVOKED_PROOFREAD_RECORD = (
    EVALUATION / "records" / "proofread-gpt-2026-08-26-170.md"
)
UNSLOP_LOCALE_RECORD = EVALUATION / "records" / "unslop-gpt-2026-08-26-177.md"
WRITE_RESPONSE_DEFAULT_RECORD = EVALUATION / "records" / "write-gpt-2026-08-26-180.md"
REDLINE_CLOSING_PROOFREAD_RECORD = (
    EVALUATION / "records" / "redline-gpt-2026-08-26-174.md"
)
REDLINE_383_RECORD = EVALUATION / "records" / "redline-claude-2026-09-22-383.md"
EDITORIAL_383 = EVALUATION / "editorial-383"
EDITORIAL_383_RESULTS = EDITORIAL_383 / "results.md"

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
        "genre-supplied technique",
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
SWEDISH = EVALUATION / "held-source-28330ae1" / "languages" / "sv.md"

# How an item is written inside that scope, and the shortest one worth
# matching on: the scope also italicises punctuation samples, which are not
# items a fixture can be said to carry.
ITEM = re.compile(r"\*([^*\n]+)\*")
ITEM_FLOOR = 4

# How many of that scope's items a fixture carries before it is concentrated
# slop rather than prose that happens to contain one of them.
SWEDISH_ITEMS = 12

# The installed genres a Skill resolves a selection against. The directory is
# the list, so what a genre supplies is read from the files here rather than
# from anything enumerating them.
GENRES = EVALUATION / "held-source-28330ae1" / "editorial" / "genres"

# The three forms a code sample takes in Markdown. A pass reads past all of
# them, so a fixture staging only the fenced one leaves the other two to be
# settled per run, which is the defect ADR-0178 ends.
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

# The matrix the editorial Skills are judged against. Most of the corpus's
# clean controls are rows of its Redline controls, and a later wave copies its
# invocations rather than restating them.
MATRIX = CORPUS / "editorial-quality" / "README.md"

# The protocol's rule on how a clean control is run, and the rule it follows:
# one says which run a criterion is answered from, the other which record.
TRACE_HEADING = "## The trace a criterion is answered from"
CLEAN_CONTROL_HEADING = "## A clean control"

# The protocol's opening section, which says what an evaluation can and cannot
# be held to, and the section that follows it. The record of the rejection
# clause no run has reached goes inside the first, under no heading of its own
# (issue #413).
EVALUATION_HEADING = "## What an evaluation is"
BLINDED_HEADING = "## Blinded semantic judging"

# The clause of Redline's and Unslop's rejection rule that no native run has
# reached, worded as both Skills' correction step words it, and the regression
# packet whose runs establish that it is unreached.
REVIEWING_SKILLS = (
    EVALUATION / "held-source-28330ae1" / "redline-body.md",
    EVALUATION / "held-source-28330ae1" / "unslop-body.md",
)
UNREACHED_CLAUSE = (
    "where the round that introduced it is not the last, restore the state"
    " immediately before that round and discard every state built on it"
)
UNREACHED_EVIDENCE = "regressions/389/README.md"

# The protocol's rules for staging an evaluation, kept apart by family: those
# binding every family, then the mechanics only the Claude family's Harness
# needs. Each rule opens its paragraph under its name in bold, and carries the
# words a later author would otherwise have to find in a closed ticket's thread
# (issue #439).
STAGING_HEADING = "## How an evaluation is staged"
STAGING_RULES = {
    "### In every family": {
        "One seat": ("same seat", "model actually launched"),
        "A fresh pre-change arm": (
            "commit the ticket started from",
            "same inputs",
            "carried over",
        ),
        "Not reproduced": (
            "maintainer's ruling",
            "each miss becomes its own ticket",
            "conditional on the measurement",
            "no product change",
            "ADR-0212",
            "ADR-0214",
            "ADR-0220",
            "ADR-0221",
            "ADR-0223",
        ),
        "One revise round": (
            "at most one",
            "subset that failed",
            "beats the pre-change arm",
            "`needs-triage`",
            "(#what-an-evaluation-is)",
        ),
        "Whose miss": ("that ticket's number", "split rule"),
        "The frozen plan": (
            "committed before the first run",
            "void",
            "only paths and the seat",
        ),
        "Interrupted runs are void": ("usage limit", "5xx", "overload", "apart"),
        "Blind paths": ("neither the arm nor the ticket",),
        "The record name": ("issue number", "(#the-recording-format)"),
    },
    "### In the Claude family": {
        "Staging": (
            "`git archive`",
            "never copied from a working tree",
            "committed before the post-change install",
        ),
        "Top-level runs": ("`claude --print`", "subagent"),
        "A scratchpad": ("`CLAUDE_CODE_ARTIFACT=1`", "(regressions/401/README.md)"),
        "The trace runner": ("(editorial-388/harness/staged_run.py)", "trace"),
    },
}

# A model named where a rule would outlive it. The protocol names the seat a
# plan chooses rather than any model, because a model is retired long before
# the rule that says a run and its baseline share one is.
MODEL_NAME = re.compile(r"\b(?:claude-(?:opus|sonnet|haiku|fable)|gpt)-\d")

# The editorial Skills an install holds beside the Manager. A run of one of
# them can reach the others — Redline closes on Proofread — so every install
# holds all four.
EDITORIAL_SKILLS = ("write", "redline", "proofread", "unslop")

# The name every new record takes, and the rule it replaced, which put the
# issue number in a name only where a record of the same Skill, family and date
# already existed (issue #439).
RECORD_NAME = "`<skill>-<provider-family>-<YYYY-MM-DD>-<issue>.md`"
RETIRED_NAMING = "same date as the record it follows"
RECORD_TEMPLATE_FIELD = "`<skill>-<provider-family>-<YYYY-MM-DD>-<issue>`"
RECORDS_README = EVALUATION / "records" / "README.md"
REGRESSIONS_README = EVALUATION / "regressions" / "README.md"

# How the clean-control rule takes the five rejections one at a time: the
# rejection in bold, as the protocol's own list names it, then whether a
# no-change reply to a response target can be held to it.
NO_CHANGE_VERDICT = re.compile(
    r"^- \*\*(?:An? )?([^*]+)\*\*[^—\n]* — (can|cannot)\b", re.MULTILINE
)

# What that reply can be held to. A fact the run added and an edit it made
# exist only in a text it delivered; the status's language, a finding the
# staged input visibly carries, and the inventory are all there without one.
NO_CHANGE_VERDICTS = {
    "unsupported fact": "cannot",
    "wrong locale behaviour": "can",
    "substantive edit": "cannot",
    "unresolved mandatory finding": "can",
    "incorrect side effect": "can",
}

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


def _section(text: str, heading: str) -> str:
    """One `## ` section of a Markdown document, without the heading itself.

    Empty where the document carries no such heading, so a caller asserts the
    heading's presence before reading anything out of what this returns.
    """

    return text.partition(f"\n{heading}\n")[2].partition("\n## ")[0]


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


def _genre_technique(genre: str) -> str:
    """The technique one installed genre's base half says it is written with.

    `none` where the genre names none. Reading it from the directory is what
    lets a fixture's premise be checked rather than restated beside it, and
    the resource format's own suite is what holds the section to being there.
    """

    section = ordinary_technique_section(GENRES / f"{genre}.md")
    assert section, f"{genre}: neither names a technique nor states it has none"

    return ordinary_technique(section)


def _named_genre(fixture: str) -> str:
    """The one installed genre a fixture's staging names on the invocation."""

    use = _fields(_entries()[fixture])["Use"].lower()
    named = {
        path.stem
        for path in GENRES.glob("*.md")
        if not path.name.endswith(".review.md") and f"{path.stem} genre" in use
    }

    assert len(named) == 1, (
        f"{fixture}: the staging names {sorted(named)} rather than exactly one"
        f" genre, so what the run resolves is left to inference."
    )

    return named.pop()


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


def test_unslop_locale_regression_stays_inside_the_anti_slop_lens() -> None:
    """Both English locales leave locale-divergent clean under Unslop.

    The American run originally reported British spelling, vocabulary,
    currency, and an ambiguous date as one anti-slop finding. A focused GPT
    rerun over the same fixture holds both locale branches to the lens boundary
    and records no unresolved finding (issue #177).
    """

    text = UNSLOP_LOCALE_RECORD.read_text(encoding="utf-8")

    for locale in ("en_GB", "en_US"):
        start = text.index(f"## `locale-divergent` — `{locale}`")
        end = text.find("\n## ", start + 1)
        entry = text[start:] if end == -1 else text[start:end]

        for evidence in (
            "`anti-slop lens` — `pass`",
            "`mechanics preserved` — `pass`",
            "**unresolved findings** — `none`",
            "No anti-slop findings",
        ):
            assert evidence in entry, (
                f"{UNSLOP_LOCALE_RECORD}: the {locale} entry does not record"
                f" {evidence!r}, so the locale-divergent lens-boundary"
                f" criterion has not passed under both English locales"
                f" (issue #177)."
            )


def test_redline_closing_proofread_regression_records_complete_delegation() -> None:
    """The focused GPT rerun observes delegation and every planted correction."""

    text = REDLINE_CLOSING_PROOFREAD_RECORD.read_text(encoding="utf-8")

    for evidence in (
        "`complete delegation` — `pass`",
        "Proofread's `SKILL.md` exactly once",
        "`resolve --scope=mechanics sv` exactly once",
        "complete current Text Artifact",
        "`planted mechanics` — `pass`",
        "`same planted result` — `pass`",
        "`side effects` — `pass`",
    ):
        assert evidence in text, (
            f"{REDLINE_CLOSING_PROOFREAD_RECORD}: the focused Redline rerun"
            f" does not record {evidence!r}, so the closing Proofread verdict"
            f" is not held at the complete nested-Skill seam (issue #174)."
        )


def test_response_default_inventory_reaches_every_writable_evaluation_location() -> (
    None
):
    """A response-targeted run is checked beyond its material directory.

    The defect wrote an artifact into Harness scratch while the staged source
    directory stayed clean. The fixture and protocol therefore require a
    before-and-after inventory of both locations (issue #180).
    """

    # Read the fixture and protocol that govern the real Harness run.
    response_default = _fields(_entries()["response-default"])
    use = response_default["Use"]
    reject = response_default["Reject"]
    protocol = _protocol()

    # Require the fixture to widen observation beyond supplied material.
    for expected in ("filesystem inventory", "Harness scratch area"):
        assert expected in use, (
            f"{INDEX}: response-default does not require {expected!r}, so an"
            f" artifact outside the supplied material directory can escape"
            f" the regression check (issue #180)."
        )

    # Reject a change in any one writable location.
    assert "any writable location in the evaluation workspace" in reject, (
        f"{INDEX}: response-default rejects writes only near its material"
        f" rather than throughout the evaluation workspace (issue #180)."
    )
    # Require the protocol to use observed state across that widened scope.
    assert "before-and-after filesystem inventory" in protocol, (
        f"{PROTOCOL}: the side-effects field can still be copied from a"
        f" Skill's account instead of observed across the run's writable"
        f" locations (issue #180)."
    )
    assert "separate Harness scratch area" in protocol, (
        f"{PROTOCOL}: the inventory scope does not expressly reach scratch"
        f" outside the supplied material directory (issue #180)."
    )


def test_write_response_default_regression_leaves_the_wide_inventory_unchanged() -> (
    None
):
    """A focused Write run passes the widened filesystem observation."""

    # Read the evidence produced by the focused real-Harness rerun.
    text = WRITE_RESPONSE_DEFAULT_RECORD.read_text(encoding="utf-8")

    # Require the record to carry both the observation and its verdicts.
    for evidence in (
        "whole staged working copy",
        "separate Harness scratch area",
        "before-and-after inventories were identical",
        "`filesystem unchanged` — `pass`",
        "`delivery account truthful` — `pass`",
        "No artifact copy was written",
    ):
        assert evidence in text, (
            f"{WRITE_RESPONSE_DEFAULT_RECORD}: the focused response-default"
            f" regression does not record {evidence!r}, so it cannot show"
            f" that the artifact stayed out of Harness scratch or that the"
            f" delivery account matched the filesystem (issue #180)."
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


def test_interview_volume_assessments_are_source_fidelity_rejections() -> None:
    """The supported count survives without an unsupported size judgement."""

    rejection = _fields(_entries()["interview-transcript"])["Reject"].lower()

    for term in (
        "source fidelity",
        "eleven full services",
        "shorter jobs",
        "high",
        "low",
        "modest",
        "comparison",
        "target",
        "capacity",
        "speaker assessment",
    ):
        assert term in rejection, (
            f"interview-transcript: the fixture does not stage the supported"
            f" count against its unsupported relative characterisation"
            f" ({term!r} unstated, issue #171)."
        )


def test_handoff_chronology_rejects_causal_verbs_and_hedges_everywhere() -> None:
    """Sequence remains sequence in every part and strength of the artifact."""

    rejection = _fields(_entries()["handoff-conflicting"])["Reject"].lower()

    for term in (
        "source fidelity",
        "chronology",
        "causality",
        "causal verb",
        "causal hedge",
        "title",
        "summary",
        "body",
    ):
        assert term in rejection, (
            f"handoff-conflicting: the fixture leaves its before-and-after"
            f" sequence free to become a causal claim ({term!r} unstated,"
            f" issues #171 and #172)."
        )


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


def test_an_arc_fixture_names_the_genre_that_settles_its_technique() -> None:
    """A genre supplies a technique, so a fixture about one names its genre.

    Both of these fixtures turn on what the run resolved rather than on what
    the material looks like, and a staging that leaves the genre to inference
    hands that back: the genres installed beside the material settle which
    contract it is read against, so the same entry means one thing today and
    another after a genre is added or reworded elsewhere. Naming the genre
    fixes the entry, and this is where the naming is held to what the genre
    directory actually says (issue #248).
    """

    # The fixture for the rule that nothing infers a technique from a text's
    # shape needs a genre supplying none, or the arc it rejects can have
    # arrived legitimately and the entry no longer separates a pass from a
    # failure without the evaluator reasoning it out.
    resembles = _named_genre("resembles-abt")
    assert _genre_technique(resembles) == "none", (
        f"resembles-abt: the {resembles} genre supplies a technique of its"
        f" own, so a reported arc is a legitimate resolution and the fixture"
        f" no longer isolates the rule it exists for."
    )

    # Its counterpart needs the opposite, the arc being what a correct run is
    # expected to reach and its provenance the only thing left to get wrong.
    fixtures = _tagged("genre-supplied technique")
    assert fixtures

    for name in fixtures:
        genre = _named_genre(name)
        assert _genre_technique(genre) != "none", (
            f"{name}: the {genre} genre supplies no technique, so the fixture"
            f" stages nothing at the level of the resolution order it claims."
        )


def test_the_protocol_records_the_rejection_clause_no_run_has_reached() -> None:
    """A limit left in a closed ticket's thread is one the next evaluator meets cold.

    Redline's and Unslop's rejection rule has a clause for a defect a later
    re-review establishes against an earlier round, and no native run has
    reached it: thirty-one runs made for #389 rejected five rounds, each at
    round 1. Both routes to staging it are refused, so the clause is carried by
    the contract prose and the test that holds it in place. The protocol states
    the limit where whoever stages the next evaluation reads it, says what
    would reopen the question, and points at the preserved runs rather than
    restating them (issue #413).
    """

    # Read the protocol's top-level sections and the one the record goes in.
    protocol = _protocol()
    headings = re.findall(r"^## .+$", protocol, re.MULTILINE)
    section = _section(protocol, EVALUATION_HEADING)
    lowered = section.lower()

    # Require the record inside the opening section, after what that section
    # already says and under no heading of its own.
    following = headings[headings.index(EVALUATION_HEADING) + 1]
    assert following == BLINDED_HEADING, (
        f"{PROTOCOL}: `{following}` follows `{EVALUATION_HEADING}`, so the"
        f" record of the unreached clause sits under a heading of its own."
    )
    assert not re.search(r"^#{3,} ", section, re.MULTILINE), (
        f"{PROTOCOL}: `{EVALUATION_HEADING}` carries a subheading, so the"
        f" record of the unreached clause sits under a heading of its own."
    )
    assert UNREACHED_CLAUSE in section, (
        f"{PROTOCOL}: `{EVALUATION_HEADING}` does not name the clause of the"
        f" rejection rule no run has reached, so the next evaluation stages a"
        f" wave to reach it or reads a run as having reached it."
    )
    assert section.index(UNREACHED_CLAUSE) > section.index("editing the corpus"), (
        f"{PROTOCOL}: the record of the unreached clause comes before what"
        f" `{EVALUATION_HEADING}` already says an evaluation is."
    )

    # Require the clause named to be the one both reviewing Skills carry.
    for skill in REVIEWING_SKILLS:
        assert UNREACHED_CLAUSE in skill.read_text(encoding="utf-8"), (
            f"{skill}: the correction step no longer carries the clause the"
            f" protocol records as unreached, so the record names a rule that"
            f" is not there."
        )

    # Require the runs that establish the clause as unreached, and a pointer
    # to the packet that holds them in place of a restatement.
    assert f"({UNREACHED_EVIDENCE})" in section, (
        f"{PROTOCOL}: the record does not point at `{UNREACHED_EVIDENCE}`,"
        f" so the runs it rests on have to be restated or found by hand."
    )
    assert (EVALUATION / UNREACHED_EVIDENCE).is_file()
    for evidence in (
        "thirty-one",
        "round-1 starting state",
        "`checks/rounds.json`",
        "not why",
    ):
        assert evidence in lowered, (
            f"{PROTOCOL}: the record does not carry {evidence!r}, so what"
            f" establishes the clause as unreached is left unstated."
        )

    # Require both routes to it refused in the terms the refusal turns on,
    # and what would reopen the question.
    for evidence in ("controlled setup", "unprompted reproduction", "reopen"):
        assert evidence in lowered, (
            f"{PROTOCOL}: the record does not carry {evidence!r}, so an"
            f" evaluation that arranges the miss can still be read as"
            f" evidence that the Skill misses."
        )


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


def test_the_protocol_runs_a_clean_control_to_a_file_as_well_as_the_response() -> None:
    """A no-change status carries no text, so it cannot show that none changed.

    A clean control run only to the response comes back with the short status,
    and the criterion it exists to test is then answered from the run's own
    word and from the source's unmoved digest, neither of which shows what the
    run would have delivered. A second run of the same input to a file has a
    delivered text to compare, so the protocol runs both and says what each is
    evidence for (issue #404).
    """

    # Read the protocol's top-level sections in the order a reader meets them.
    protocol = _protocol()
    headings = re.findall(r"^## .+$", protocol, re.MULTILINE)

    # Require the rule directly after the rule on the trace, which it answers.
    assert CLEAN_CONTROL_HEADING in headings, (
        f"{PROTOCOL}: no `{CLEAN_CONTROL_HEADING}` section, so a clean control"
        f" is still run once, to the response, and judged on its own word."
    )
    following = headings[headings.index(TRACE_HEADING) + 1]
    assert following == CLEAN_CONTROL_HEADING, (
        f"{PROTOCOL}: `{CLEAN_CONTROL_HEADING}` does not directly follow"
        f" `{TRACE_HEADING}`; `{following}` does."
    )

    # Require both runs, with the file target the matrix's invocations take.
    section = _section(protocol, CLEAN_CONTROL_HEADING)
    lowered = section.lower()
    for evidence in (
        "response-target run",
        "file-target run",
        "`--output=response`",
        "`--output=output.md`",
        "delivery.md",
    ):
        assert evidence in section, (
            f"{PROTOCOL}: the clean-control rule does not name {evidence!r},"
            f" so the second run and what makes it deliver a text are unstated."
        )

    # Require the criterion answered from the delivered file, and never from
    # the run's account of itself or the source's unmoved digest.
    for evidence in (
        "`r1`",
        "compared with",
        "own statement that it changed nothing",
        "digest",
        "never evidence",
    ):
        assert evidence in lowered, (
            f"{PROTOCOL}: the clean-control rule does not carry {evidence!r},"
            f" so the criterion can still be answered from the run's own word."
        )

    # Require the two runs to be two entries a record tells apart by target.
    assert "two fixture entries" in lowered and "output target" in lowered, (
        f"{PROTOCOL}: the clean-control rule does not say how its two runs are"
        f" recorded, so a record has one entry for two runs."
    )


def test_the_protocol_defines_a_clean_control_by_its_frozen_expectation() -> None:
    """Which controls owe the second run is a property, and examples show it.

    A list would go stale the day a control is added, so the rule defines a
    clean control by its frozen expectation that the text comes back unchanged
    and names examples as examples. The Redline run of a pipeline is excluded
    by name, because it can end in the same short status without being one.
    """

    # Read the rule and the corpus files its examples come from.
    section = _section(_protocol(), CLEAN_CONTROL_HEADING)
    lowered = section.lower()
    matrix = MATRIX.read_text(encoding="utf-8")

    # Require the definition as a property, with its examples marked as such.
    for evidence in ("frozen expectation", "examples", "not a complete list"):
        assert evidence in lowered, (
            f"{PROTOCOL}: the clean-control rule does not carry {evidence!r},"
            f" so it reads as a closed list rather than a property."
        )

    # Require the three examples, each naming something the corpus carries.
    for example in ("`*-clean`", "`clean-en-GB`", "`metadata-none`"):
        assert example in section, (
            f"{PROTOCOL}: the clean-control rule does not name {example}"
            f" among its examples."
        )
    assert "clean-en-GB" in _entries()
    assert "| metadata-none |" in matrix
    assert re.search(r"^\| [a-z-]+-clean / ", matrix, re.MULTILINE)

    # Require the pipeline's Redline run to be excluded in so many words.
    assert "pipeline" in lowered and "not a clean control" in lowered, (
        f"{PROTOCOL}: the clean-control rule does not exclude the Redline run"
        f" of a Write-to-Redline pipeline."
    )


def test_the_protocol_says_which_rejections_a_no_change_reply_can_be_held_to() -> None:
    """A reply with no text in it can still fail some rejections and not others.

    The test for each is whether a `fail` could be shown from the reply's own
    words, the staged input and the inventory without a delivered text. Only a
    delivered text shows a fact the run added or an edit it made, so those two
    rejections are answered from the file-target run and never from the reply.
    """

    # Read the rule's verdicts, one bullet per rejection.
    section = _section(_protocol(), CLEAN_CONTROL_HEADING)
    verdicts = {
        match.group(1).strip().lower(): match.group(2)
        for match in NO_CHANGE_VERDICT.finditer(section)
    }

    # Require all five rejections taken, and each one answered as decided.
    assert set(verdicts) == set(REJECTIONS), (
        f"{PROTOCOL}: the clean-control rule takes {sorted(verdicts)} rather"
        f" than the five rejections {sorted(REJECTIONS)}."
    )
    assert verdicts == NO_CHANGE_VERDICTS


def _staging_rules(family: str) -> dict[str, str]:
    """Map each staging rule under *family*'s heading to its whole text.

    A rule opens a line with its name in bold and runs to the next rule or the
    end of the family's subsection, so a rule carrying a code block keeps it.
    """

    section = _section(_protocol(), STAGING_HEADING)
    subsection = section.partition(f"\n{family}\n")[2].partition("\n### ")[0]
    starts = list(re.finditer(r"^\*\*([^*\n]+)\.\*\* ", subsection, re.MULTILINE))
    return {
        match.group(1): subsection[
            match.start() : starts[position + 1].start()
            if position + 1 < len(starts)
            else len(subsection)
        ]
        for position, match in enumerate(starts)
    }


def test_the_protocol_states_how_an_evaluation_is_staged() -> None:
    """A staging rule kept in a ticket's thread is restated by every ticket.

    The unattended run of 2026-09-23 wrote the same clause into ten readiness
    addenda, and its builders then learned three more rules by voiding runs.
    The protocol states every one of them, each with the reason a later author
    would otherwise talk themselves out of, and keeps the rules binding every
    family apart from the mechanics of the Claude family's Harness (issue #439).
    """

    # Require the section, with the two families in order under it.
    protocol = _protocol()
    headings = re.findall(r"^## .+$", protocol, re.MULTILINE)
    assert STAGING_HEADING in headings, (
        f"{PROTOCOL}: no `{STAGING_HEADING}` section, so how an evaluation is"
        f" staged is still stated in ticket threads and nowhere in the tree."
    )
    section = _section(protocol, STAGING_HEADING)
    families = re.findall(r"^### .+$", section, re.MULTILINE)
    assert families == list(STAGING_RULES), (
        f"{PROTOCOL}: `{STAGING_HEADING}` carries {families} rather than"
        f" {list(STAGING_RULES)}, so the rules every family keeps are not kept"
        f" apart from one family's mechanics."
    )

    # Require every rule, in its family, carrying what makes it a rule.
    for family, rules in STAGING_RULES.items():
        stated = _staging_rules(family)
        assert list(stated) == list(rules), (
            f"{PROTOCOL}: `{family}` states {list(stated)} rather than {list(rules)}."
        )
        for rule, evidence in rules.items():
            missing = [phrase for phrase in evidence if phrase not in stated[rule]]
            assert missing == [], (
                f"{PROTOCOL}: the staging rule `{rule}` does not carry"
                f" {missing}, so what it asks of an evaluation is left unstated."
            )

    # Require the rules to stand on their own words: no model a rule would
    # outlive, no ticket comment as a source, and the rule that a miss is
    # never absorbed pointed at rather than said twice.
    named = MODEL_NAME.findall(protocol)
    assert named == [], (
        f"{PROTOCOL}: names the model {named}, which a rule outlives; the"
        f" plan and the record name the model a run launched."
    )
    assert "comment" not in section.lower(), (
        f"{PROTOCOL}: `{STAGING_HEADING}` cites a ticket comment, which a"
        f" reader of the tree cannot be expected to open."
    )
    assert protocol.count("softening a criterion") == 1, (
        f"{PROTOCOL}: the rule that a real defect is never absorbed is stated"
        f" more than once, so there are two copies to keep true."
    )


def test_the_staging_example_lays_out_the_install_the_shim_reads(
    tmp_path: Path,
) -> None:
    """The protocol's staging commands, run as written, stage a usable install.

    Each Skill's shim looks for the Manager in a `kntnt/` directory beside the
    Skill's own, so an install holds the editorial Skills and `kntnt/` side by
    side and nothing else at its root. Stripping the Manager's path by as many
    components as a Skill's spills its contents into the root instead, which
    is the example one ticket's thread carried and three frozen plans had to
    correct (issue #439).
    """

    # Read the one command block the staging rule carries.
    staging = _staging_rules("### In the Claude family")["Staging"]
    blocks = re.findall(r"^```\n(.*?)^```$", staging, re.MULTILINE | re.DOTALL)
    assert len(blocks) == 1, (
        f"{PROTOCOL}: the staging rule carries {len(blocks)} command blocks"
        f" rather than one."
    )
    assert set(re.findall(r"<[a-z-]+>", blocks[0])) == {"<rev>", "<install>"}, (
        f"{PROTOCOL}: the staging commands carry placeholders other than"
        f" `<rev>` and `<install>`, so they cannot be run as written."
    )

    # Run them against the commit checked out, into an empty install.
    install = tmp_path / "install"
    install.mkdir()
    script = blocks[0].replace("<rev>", "HEAD").replace("<install>", str(install))
    subprocess.run(
        ["bash", "-euo", "pipefail", "-c", script], cwd=REPO_ROOT, check=True
    )

    # Require each Skill and the Manager side by side, and nothing spilled.
    for skill in EDITORIAL_SKILLS:
        assert (install / skill / "SKILL.md").is_file(), (
            f"{PROTOCOL}: the staging commands do not put `{skill}/SKILL.md`"
            f" at the install's root."
        )
    assert (install / "kntnt" / "scripts" / "kntnt.py").is_file(), (
        f"{PROTOCOL}: the staging commands do not put the Manager at"
        f" `kntnt/scripts/kntnt.py`, where each Skill's shim looks for it."
    )
    root = sorted(path.name for path in install.iterdir())
    assert root == sorted((*EDITORIAL_SKILLS, "kntnt")), (
        f"{PROTOCOL}: the staging commands leave {root} at the install's root,"
        f" so something was extracted beside the Skills and the Manager."
    )


def test_every_new_record_name_carries_the_issue_it_was_run_for() -> None:
    """Two tickets built side by side can evaluate one Skill on one day.

    The name used to take the issue number only where a record of the same
    Skill, family and date already existed, which two builders working at once
    cannot know. Every new record now carries it, stated wherever the name is
    stated, and records already written keep the names they have (issue #439).
    """

    recording = _section(_protocol(), "## The recording format")
    surfaces = {
        PROTOCOL: recording,
        RECORDS_README: RECORDS_README.read_text(encoding="utf-8"),
        TEMPLATE: TEMPLATE.read_text(encoding="utf-8"),
    }
    for path, text in surfaces.items():
        assert RECORD_NAME in text, f"{path}: does not name a record {RECORD_NAME}"
        assert RETIRED_NAMING not in text, (
            f"{path}: still adds the issue number only where a record of that"
            f" Skill, family and date already exists."
        )
    for path in (PROTOCOL, RECORDS_README):
        assert "keep the names" in surfaces[path], (
            f"{path}: does not say that records already written keep their"
            f" names, so one is renamed to match the rule."
        )
    assert RECORD_TEMPLATE_FIELD in surfaces[TEMPLATE], (
        f"{TEMPLATE}: the `record` field does not carry the issue number."
    )


def test_whoever_writes_or_builds_an_evaluation_is_pointed_at_the_staging() -> None:
    """The staging rules are read where an evaluation's author already reads.

    The always-loaded guide sends whoever writes an evaluation ticket to the
    protocol, not only whoever runs one, and the index of focused regressions
    points at the staging rules those regressions keep too (issue #439).
    """

    agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    line = re.search(
        r"^- `docs/evaluation/protocol\.md` — (read when .+)$", agents, re.MULTILINE
    )
    assert line is not None, "AGENTS.md: no pointer to the evaluation protocol"
    assert "evaluation ticket" in line.group(1), (
        "AGENTS.md: the pointer to the evaluation protocol does not fire for"
        " writing an evaluation ticket, so its author meets the staging rules"
        " only after the ticket is written."
    )

    regressions = REGRESSIONS_README.read_text(encoding="utf-8")
    assert "(../protocol.md#how-an-evaluation-is-staged)" in regressions, (
        f"{REGRESSIONS_README}: does not point at the staging rules a focused"
        f" regression keeps."
    )
    for rule in (
        "The frozen plan",
        "Interrupted runs are void",
        "Top-level runs",
        "A scratchpad",
    ):
        assert rule in regressions, (
            f"{REGRESSIONS_README}: does not name `{rule}` among the staging"
            f" rules a focused regression keeps."
        )


def test_the_matrix_runs_a_clean_redline_control_to_a_file_as_well() -> None:
    """A later wave copies the matrix's invocation, so the matrix carries both.

    Left alone, the matrix would go on prescribing one run to the response, and
    a wave that copied it would inherit the gap the protocol closes. Its
    staging paragraph also treated the input as the final text of a no-change
    run, which is the gap itself (issue #404).
    """

    # Read the matrix's staging and control sections.
    matrix = MATRIX.read_text(encoding="utf-8")
    staging = _section(matrix, "## Material and staging")
    controls = _section(matrix, "## Redline controls")
    rule = "(../../protocol.md#a-clean-control)"

    # Require the control paragraph to add the file-target run beside the
    # response-target one, and point at the rule that asks for it.
    for evidence in (
        "`/redline --genre=<genre> --language=<locale> --output=response input.md`",
        "`/redline --genre=<genre> --language=<locale> --output=output.md input.md`",
        rule,
    ):
        assert evidence in controls, (
            f"{MATRIX}: `## Redline controls` does not carry {evidence!r}, so a"
            f" wave copying it runs a clean control only to the response."
        )

    # Require the staging paragraph to stop treating the input as the result.
    assert "the input is final" not in staging, (
        f"{MATRIX}: a no-change status is still read as delivering the input."
    )
    assert "delivers no final text" in staging and rule in staging, (
        f"{MATRIX}: the staging paragraph does not say that a no-change status"
        f" delivers no final text, or where the rule on its reply is."
    )

    # Require a revision note directly after the anatomy revision's.
    paragraphs = matrix.split("\n\n")
    anatomy = next(
        position
        for position, paragraph in enumerate(paragraphs)
        if paragraph.startswith("Revised for the [article anatomy]")
    )
    note = paragraphs[anatomy + 1].lower()
    assert "clean control" in note and "judged against" in note, (
        f"{MATRIX}: no note after the anatomy revision says that a clean"
        f" control is now run differently and nothing it is judged against"
        f" changed."
    )


def test_the_pipeline_matrix_names_a_genre_independently_of_legacy_fixture_paths() -> (
    None
):
    """Write staging cannot derive an installed genre from an immutable fixture name."""

    matrix = MATRIX.read_text(encoding="utf-8")
    staging = _section(matrix, "## Material and staging")
    pipeline = _section(matrix, "## Pipeline matrix")

    assert "sources/<genre>.md" not in staging
    assert "the source linked in the pipeline matrix" in staging
    assert "the genre in that row's Genre column" in staging
    for genre in ("article", "casestudy", "column", "opinion", "webcopy"):
        assert f"| {genre} |" in pipeline


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

    sources = [PROTOCOL, TEMPLATE, *sorted(CORPUS.rglob("*.md"))]

    # Observed outputs and historical records are evidence, not requirements.
    # A corpus moved out from under this glob would leave nothing to judge.
    assert any(path.is_relative_to(CORPUS) for path in sources)

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
    and ADR-0178 settles what a sample is to a pass: quoted material whose
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
            f" code, which is half of what ADR-0178 settles."
        )
        assert "byte" in reject, (
            f"{name}: the entry does not reject the code coming back altered,"
            f" which is the other half."
        )


# The twelve draft runs `N1` covers, not the controls. Two judgements each is
# the count the results paragraph may name; a sentence tally is not, because
# the two judges of one run rarely list the same number of items (issue #427).
DRAFT_RUNS_383 = (
    "pre-column-sv-r1",
    "pre-column-sv-r2",
    "pre-opinion-en_GB-r1",
    "pre-opinion-en_GB-r2",
    "post-column-sv-r1-a",
    "post-column-sv-r1-b",
    "post-column-sv-r2-a",
    "post-column-sv-r2-b",
    "post-opinion-en_GB-r1-a",
    "post-opinion-en_GB-r1-b",
    "post-opinion-en_GB-r2-a",
    "post-opinion-en_GB-r2-b",
)
N1_OPENING = (
    "  - `N1` — `pass` — no limiting sentence deleted, weakened or hardened"
    " on either judgement; "
)
N1_VERBATIM = f"{N1_OPENING}all of them verbatim."
N1_VERBATIM_DISCLAIMER = (
    f"{N1_OPENING}all of them verbatim, both halves of every two-part"
    " disclaimer included."
)
N1_EXCEPTIONS_383 = {
    "post-column-sv-r2-a": (
        f"{N1_OPENING}all of them verbatim except `gör det` becoming `vet det`"
        " in `och jag tänker inte låtsas att jag gör det`, which both judges"
        " record, both halves of every two-part disclaimer included."
    ),
    "post-opinion-en_GB-r2-a": (
        f"{N1_OPENING}all of them verbatim except `channel` becoming `route`"
        " in `before the channel goes`, which judge A records, both halves of"
        " every two-part disclaimer included."
    ),
    "post-column-sv-r2-b": (
        f"{N1_OPENING}all of them verbatim except the dash in `Det som retar"
        " mig är något annat — att tid i kalendern` set as an en dash, which"
        " judge A records, both halves of every two-part disclaimer included."
    ),
}
# What #403 left after the count. The count is the only phrase this ticket moves.
N1_PARAGRAPH_REST_383 = (
    "not one sentence was deleted, weakened or hardened; every judgement"
    " records them surviving byte for byte, both halves of every two-part"
    " disclaimer included, except in four judgements that each record one"
    " change inside a sentence they list as limiting: both judges of"
    " `post-column-sv-r2-a` record `gör det` becoming `vet det` in `och jag"
    " tänker inte låtsas att jag gör det`, judge A of `post-opinion-en_GB-r2-a`"
    " records `channel` becoming `route` in `before the channel goes`, and"
    " judge A of `post-column-sv-r2-b` records the dash in `Det som retar mig"
    " är något annat — att tid i kalendern` set as an en dash. `We make no"
    " claim to have funded or costed that trial` comes back verbatim in the"
    " six `opinion-en_GB` runs, and `Det är min reflektion, inte något jag har"
    " mätt hos andra` and `Det här är en iakttagelse av ett dokument, inte en"
    " scen från ett visst möte` in the three `column-sv-r2` runs —"
    " `pre-column-sv-r2`, `post-column-sv-r2-a` and `post-column-sv-r2-b` —"
    " in each case the only runs of either arm whose input carries the"
    " sentence. What #377 repaired stays repaired."
)
N1_PARAGRAPH_383 = (
    "**`N1` — met in all eight post-change runs, and in all four pre-change"
    " runs.** Across the twenty-four judgements of the twelve draft runs "
    f"{N1_PARAGRAPH_REST_383}"
)
RECORD_MISSTATEMENT = (
    "A record line that misstates what the run's own committed artefacts show"
    " is corrected in place to what they show, and the commit names the"
    " artefact the corrected line now agrees with. Such a correction never"
    " changes a verdict or a criterion outcome; a line whose outcome is itself"
    " in doubt is raised as a ticket instead."
)


def _fixture_sections(record: str) -> dict[str, str]:
    """Map each `## ` fixture heading to the entry that follows it."""

    parts = re.split(r"^## `([^`]+)`\n", record, flags=re.MULTILINE)
    return {parts[index]: parts[index + 1] for index in range(1, len(parts), 2)}


def _criterion_line(section: str, identifier: str) -> str:
    """The one criteria bullet that opens on *identifier*."""

    prefix = f"  - `{identifier}` — "
    matches = [line for line in section.splitlines() if line.startswith(prefix)]
    assert len(matches) == 1, matches
    return matches[0]


def test_the_383_n1_paragraph_names_the_judgements_not_a_reading_count() -> None:
    """A reading count the tree does not support is not evidence.

    `N1` covers the twelve draft runs, two judgements each. Those judgements
    do not agree on how many limiting sentences a run holds, so the paragraph
    names the judgements and states no count of readings (issue #427).
    """

    runs = EDITORIAL_383 / "runs"
    judgements = [
        runs / name / judge
        for name in DRAFT_RUNS_383
        for judge in ("judgement-a.md", "judgement-b.md")
    ]

    # The figure the paragraph names is the one the tree holds.
    missing = [path for path in judgements if not path.is_file()]
    assert missing == [], missing
    assert len(DRAFT_RUNS_383) == 12
    assert len(judgements) == 24

    paragraph = next(
        line
        for line in EDITORIAL_383_RESULTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("**`N1` — met in all eight post-change runs")
    )

    assert "limiting-sentence readings" not in paragraph
    assert "forty-eight" not in paragraph
    assert paragraph == N1_PARAGRAPH_383


def test_the_383_record_names_the_three_limiting_sentence_changes() -> None:
    """Three `N1` lines said verbatim where their own judgements record a change.

    The verdict stays `pass`. The sentence that supports it names the one
    change and the judge or judges who record it, and the other nine draft
    runs stay as written (issue #427).
    """

    sections = _fixture_sections(REDLINE_383_RECORD.read_text(encoding="utf-8"))
    unchanged = {
        "pre-column-sv-r1": N1_VERBATIM,
        "pre-column-sv-r2": N1_VERBATIM,
        "pre-opinion-en_GB-r1": N1_VERBATIM,
        "pre-opinion-en_GB-r2": N1_VERBATIM,
        "post-column-sv-r1-a": N1_VERBATIM_DISCLAIMER,
        "post-column-sv-r1-b": N1_VERBATIM_DISCLAIMER,
        "post-opinion-en_GB-r1-a": N1_VERBATIM_DISCLAIMER,
        "post-opinion-en_GB-r1-b": N1_VERBATIM_DISCLAIMER,
        "post-opinion-en_GB-r2-b": N1_VERBATIM_DISCLAIMER,
    }

    assert set(unchanged) | set(N1_EXCEPTIONS_383) == set(DRAFT_RUNS_383)

    for name, expected in {**unchanged, **N1_EXCEPTIONS_383}.items():
        line = _criterion_line(sections[name], "N1")
        assert line == expected, name
        assert "`pass`" in line


def test_a_record_line_that_misstates_its_artefacts_is_corrected_in_place() -> None:
    """Append-only protects a run from a later repair of the Skill.

    It does not protect a line that was false against the run's own committed
    artefacts on the day it was written. That line is corrected in place, the
    commit names the artefact it now agrees with, and the correction never
    moves a verdict or a criterion outcome. A line whose outcome is itself in
    doubt is a ticket, not an edit (issue #427).
    """

    section = _section(_protocol(), "## The recording format")
    append_only = section.index("Records are append-only in practice.")
    correction = section.index(RECORD_MISSTATEMENT)
    suite = section.index("Committed evidence is never edited to satisfy the suite.")

    assert append_only < correction < suite
