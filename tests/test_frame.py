"""The rules the framing Skill cannot be run without."""

from __future__ import annotations

import json
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "code" / "frame"
BODY = SKILL / "SKILL.md"
RECON = SKILL / "references" / "recon.md"
KNOWLEDGE = SKILL / "references" / "knowledge.md"
ROUTE_REQUEST_SCHEMA = (
    REPO_ROOT
    / "skills"
    / "models"
    / "model-selector"
    / "references"
    / "route-request.schema.json"
)


def test_the_body_sorts_every_open_point_before_it_asks_anything() -> None:
    """The three bins are the method, so the body is where they have to be.

    A framing that asks whatever it does not know is the interview this Skill
    replaces. What makes it a different thing is that a point the codebase can
    answer is fetched and a point the established constraints settle is
    decided — and the body is the only thing an agent executes.
    """

    text = BODY.read_text(encoding="utf-8")

    for phrase in (
        "The codebase answers it.",
        "The frames answer it.",
        "Only the owner answers it.",
        "The tie-break is reversibility.",
    ):
        assert phrase in text, (
            f"{BODY}: the body names the bin `{phrase}`. Sorting each open"
            f" point into one of three bins is the whole method, and a bin"
            f" left unstated is a point that reaches the owner as a question."
            f" See {STANDARD}."
        )

    assert "this Skill's own defect rather than an economy" in text, (
        f"{BODY}: the body says that asking the owner what a file could have"
        f" answered is a defect of this Skill. Left unsaid, the cheap question"
        f" wins every time recon looks like work. See {STANDARD}."
    )


def test_the_body_establishes_what_binds_before_the_first_question() -> None:
    """A decision taken in the owner's stead rests on a stated constraint.

    The frames are read from the repository the task is in, and they are what
    separates deciding from preferring. Read after the interview they would
    justify decisions already made.
    """

    text = BODY.read_text(encoding="utf-8")

    assert "before a single question" in text, (
        f"{BODY}: the body establishes what binds before it asks anything."
        f" A ledger entry decided under a constraint nobody read yet is a"
        f" preference wearing a frame's clothes. See {STANDARD}."
    )
    assert "always-loaded agent file" in text, (
        f"{BODY}: the frames start at the repository's always-loaded agent"
        f" file and the documents it points at, which is where a repository"
        f" states what binds. See {STANDARD}."
    )


def test_the_body_routes_recon_through_the_public_interface() -> None:
    """Delegated execution is routed, and a refusal is not a nearby model.

    The collection's rule is that a Skill delegating execution routes through
    model-selector's public `route` Interface and reproduces none of its
    policy. What this Skill adds is what it does with each answer — and the
    refusal branch is the one an agent in a hurry invents a substitute for.
    """

    text = BODY.read_text(encoding="utf-8")

    assert "/model-selector route <path>" in text, (
        f"{BODY}: recon is delegated through `/model-selector route <path>`,"
        f" the public Interface, rather than through a private arrangement of"
        f" this Skill's own. See {STANDARD}."
    )
    assert "Read none of that Skill's references" in text, (
        f"{BODY}: the body says that none of model-selector's references are"
        f" read. Peer internals are not an interface, and a caller that reads"
        f" them owns a copy of somebody else's policy. See {STANDARD}."
    )
    assert "Never put a nearby model in the place of a refusal." in text, (
        f"{BODY}: a routing refusal falls back to the main seat, never to a"
        f" model that looked close enough. A substituted model is an exact"
        f" instruction executed somewhere nobody decided on. See {STANDARD}."
    )
    assert "one execution class" in text, (
        f"{BODY}: one route request covers the wave as an ordered batch,"
        f" every brief in it being the same execution class — read-only,"
        f" reversible, and checked when it comes back. See {STANDARD}."
    )


def test_the_body_keeps_the_record_written_as_the_run_proceeds() -> None:
    """An interrupted framing costs the last round, not the framing.

    The record is the only durable thing a framing produces, and a record
    written at the close is a record written by whoever is still holding the
    session when the context runs out.
    """

    text = BODY.read_text(encoding="utf-8")

    assert "after every round and after every recon report" in text, (
        f"{BODY}: the record is written incrementally, after every round and"
        f" every recon report. Written at the end it is lost exactly when a"
        f" long framing needed it. See {STANDARD}."
    )
    assert "$LIBRARY/references/frame-record.md" in text, (
        f"{BODY}: the format is read from the Collection Library, where it is"
        f" stated once for the Skill that writes a record and the Skill that"
        f" reads one. See {STANDARD}."
    )


def test_the_body_buys_the_silence_without_touching_a_tracked_file() -> None:
    """A local artifact gets a local ignore, written once and only where needed."""

    text = BODY.read_text(encoding="utf-8")

    assert ".git/info/exclude" in text, (
        f"{BODY}: the ignore is written to `.git/info/exclude`, which is"
        f" local. A line in a tracked ignore file would be this Skill"
        f" committing to somebody's repository to hide its own scratch. See"
        f" {STANDARD}."
    )
    assert "git check-ignore -q .kntnt/" in text, (
        f"{BODY}: the body checks whether the directory is already ignored"
        f" before writing anything, so a repository that already ignores it"
        f" gains no second line. See {STANDARD}."
    )
    assert "of this run alone" in text, (
        f"{BODY}: the report names the ignore line on the run that wrote it"
        f" and stays silent on the runs that did not. A line reported every"
        f" run is a change the owner goes looking for and cannot find. See"
        f" {STANDARD}."
    )


def test_the_body_offers_every_unconsumed_record_back_at_the_start() -> None:
    """Nothing consumes a record yet, so the start of a run is the only sweep.

    The directory is read anyway to resolve a named record, which is what
    makes the offer free — and a discard is the one moment a framing's
    knowledge can be withdrawn against a manifest instead of guessed at.
    """

    text = BODY.read_text(encoding="utf-8")

    assert "resume it or discard it" in text, (
        f"{BODY}: a run reports the records still lying in `.kntnt/frames/`"
        f" and offers each of them for resuming or discarding. Nothing else"
        f" clears them. See {STANDARD}."
    )
    assert "references/knowledge.md" in text, (
        f"{BODY}: a discard follows the withdrawal the reference states,"
        f" against the record's own manifest. Knowledge withdrawn without one"
        f" is knowledge guessed at. See {STANDARD}."
    )


def test_the_body_shows_the_ledger_as_a_delta_each_round() -> None:
    """The veto window is open where reversing costs one entry.

    An entry standing unvetoed for three rounds has had three rounds of
    decisions built on top of it, and reversing it then costs the branch.
    """

    text = BODY.read_text(encoding="utf-8")

    assert "the entries taken since the last round, one line each" in text, (
        f"{BODY}: each round carries the ledger entries taken since the last"
        f" one, one line each. A ledger read only at the end is a ledger"
        f" nobody could still veto. See {STANDARD}."
    )
    assert "keeps its number and says it was vetoed" in text, (
        f"{BODY}: a vetoed entry stays at its number and says so, and the"
        f" answer that replaces it is the owner's own. A number that moves is"
        f" a veto that names the wrong decision. See {STANDARD}."
    )
    assert "verbatim" in text, (
        f"{BODY}: the owner's answers are written verbatim. A paraphrase is"
        f" this Skill's judgement carrying his name, which is the one"
        f" substitution the record exists to prevent. See {STANDARD}."
    )


def test_the_recon_brief_returns_an_answer_rather_than_its_material() -> None:
    """The raw material staying in the subagent is why the question was sent there.

    A brief that does not fix its return contract comes back as a reading
    list, and the context the interview needed is spent on it after all.
    """

    text = RECON.read_text(encoding="utf-8")

    assert "One brief asks one question" in text, (
        f"{RECON}: one brief asks one question. Two questions come back as"
        f" one answer with the weaker half unevidenced. See {STANDARD}."
    )
    for contract in (
        "**The direct answer**",
        "**The evidence**",
        "**Anomalies**",
        "**Coverage**",
    ):
        assert contract in text, (
            f"{RECON}: the return contract names {contract}. A brief that"
            f" leaves one out gets an answer nobody can check, an anomaly"
            f" nobody hears about, or a partial sweep presented as complete."
            f" See {STANDARD}."
        )
    assert "a reader can open and check for themselves" in text, (
        f"{RECON}: evidence carries addresses a reader can open. An answer"
        f" without one is a paraphrase the framing has to trust. See"
        f" {STANDARD}."
    )
    assert "change no file" in text, (
        f"{RECON}: recon is read-only, which is what makes a whole wave one"
        f" execution class and safe to route cheaply. See {STANDARD}."
    )


def test_the_knowledge_reference_gates_a_record_on_all_three_criteria() -> None:
    """A decision failing any of the three is a ledger entry and nothing more.

    An archive grown without that bar fills with how-texts wearing a
    why-document's clothes, in somebody else's repository, written by a Skill
    that was only passing through.
    """

    text = KNOWLEDGE.read_text(encoding="utf-8")

    for criterion in (
        "**Hard to reverse.**",
        "**Surprising without its context.**",
        "**The result of a real trade-off.**",
    ):
        assert criterion in text, (
            f"{KNOWLEDGE}: the bar names {criterion}. All three hold at once"
            f" or the decision is a ledger entry. See {STANDARD}."
        )
    assert "All three at once" in text, (
        f"{KNOWLEDGE}: the three criteria are conjunctive. Read as a menu"
        f" they admit every decision that was hard to make. See {STANDARD}."
    )
    assert "Follow the target repository's own convention where it declares one" in (
        text
    ), (
        f"{KNOWLEDGE}: knowledge goes where the repository being framed says"
        f" it goes, and the single-context default applies only where it says"
        f" nothing. See {STANDARD}."
    )
    assert "This is bounded because the manifest is" in text, (
        f"{KNOWLEDGE}: the withdrawal is bounded by the manifest. An"
        f" unbounded search has to guess, and a guess deletes records that"
        f" were never this framing's to remove. See {STANDARD}."
    )


def test_the_body_names_every_field_a_route_request_has_to_carry() -> None:
    """The body is the whole of the artifact's construction, so it has to be complete.

    This Skill ships no engine, and it may not read the peer's schema at run
    time — peer internals are not an interface — so what the body says is the
    only thing standing between a recon wave and an artifact refusal. That
    makes the body a hand-kept copy of somebody else's required set, and this
    is the check that keeps the copy true: the schema is read here, where the
    repository can see both halves at once.
    """

    schema = json.loads(ROUTE_REQUEST_SCHEMA.read_text(encoding="utf-8"))
    required = schema["$defs"]["request"]["required"]
    text = BODY.read_text(encoding="utf-8")

    # An empty required set would leave the loop below judging nothing.
    assert required

    for field in required:
        assert f"`{field}`" in text, (
            f"{BODY}: a route request carries `{field}`, and the body does not"
            f" name it. The Skill has no engine to build the artifact and may"
            f" not read model-selector's schema, so a field missing from the"
            f" body is a wave refused as malformed. See {STANDARD}."
        )

    assert "the integer `1`" in text, (
        f"{BODY}: the envelope's `schema_version` is the integer 1, and a"
        f" version written as a string is an artifact refusal before any"
        f" request is read. See {STANDARD}."
    )
