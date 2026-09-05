"""The decision records under `docs/adr/`, and the numbers that cite them."""

from __future__ import annotations

import re
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
ADR = REPO_ROOT / "docs" / "adr"
SKILLS = REPO_ROOT / "skills"

# The prose outside the collection that cites records the same way a record
# cites another one, so a number that has gone stale is caught wherever it is
# written rather than only where records supersede each other.
CITING_DOCS = ("CONTEXT.md", "README.md", "AGENTS.md", "CONTRIBUTING.md")

# The two other places a record is cited from: the coding standard, which names
# a rule in a phrase and cites the record carrying its reasoning, and the suite
# itself, whose assertion messages do the same for the reader whose check has
# just gone red (issue #69). A pointer is the one part of that arrangement free
# to drift, so both are held to the same check as the prose above.
STANDARD_DIR = REPO_ROOT / "docs" / "coding-standard"
TESTS = REPO_ROOT / "tests"

# A record's file is `NNNN-slug.md` and its number is that four-digit prefix;
# a citation is the same number written as `ADR-NNNN`.
RECORD = re.compile(r"^(\d{4})-.+\.md$")
CITATION = re.compile(r"ADR-(\d{4})")

# The one edit the convention sanctions in a record that is otherwise never
# rewritten (ADR-0075): a later record that takes over an earlier one's ground
# leaves a sentence in it, the relation participle beside the later record's
# citation. The active form is the declaration a later record makes in its own
# text where it names what it takes, as ADR-0059's withdrawal paragraph does.
POINTER = re.compile(
    r"\b(?:superseded|amended|narrowed|withdrawn|replaced) by ADR-(\d{4})\b"
)
CLAIM = re.compile(
    r"\b(?:supersedes|amends|narrows|replaces|withdraws(?: from)?) ADR-(\d{4})\b"
)

# The relations the collection carries today, as (earlier, later) pairs. The
# scans below must find at least these: a record is never rewritten, so the
# floor only grows, and a pattern that drifted from the prose would otherwise
# match nothing and judge nothing.
RELATIONS = {
    ("0090", "0156"),
    ("0133", "0156"),
    ("0145", "0156"),
    ("0090", "0158"),
    ("0149", "0159"),
    ("0150", "0159"),
    ("0090", "0160"),
    ("0158", "0160"),
    ("0161", "0162"),
    ("0095", "0164"),
    ("0136", "0165"),
    ("0083", "0166"),
    ("0136", "0166"),
    ("0090", "0167"),
    ("0113", "0168"),
    ("0017", "0019"),
    ("0029", "0059"),
    ("0050", "0059"),
    ("0055", "0069"),
    ("0060", "0061"),
    ("0063", "0076"),
    ("0044", "0077"),
    ("0063", "0077"),
    ("0059", "0078"),
    ("0073", "0079"),
    ("0072", "0098"),
    ("0048", "0103"),
    ("0080", "0103"),
    ("0096", "0105"),
    ("0055", "0106"),
    ("0098", "0110"),
    ("0107", "0120"),
    ("0078", "0122"),
    ("0001", "0130"),
    ("0028", "0130"),
    ("0036", "0130"),
    ("0041", "0130"),
    ("0090", "0130"),
    ("0132", "0133"),
    ("0083", "0136"),
    ("0104", "0136"),
    ("0132", "0136"),
    ("0089", "0137"),
    ("0132", "0137"),
    ("0104", "0146"),
    ("0083", "0147"),
    ("0138", "0148"),
    ("0133", "0151"),
    ("0134", "0151"),
    ("0089", "0154"),
    ("0132", "0154"),
    ("0137", "0154"),
}

# The flag-refusal rule and the reasoning an installed reader needs. `delegation`
# states the rule in a longer sentence than its siblings, so what is pinned is
# the shared clause and rationale rather than the sentence in full.
REFUSAL_CLAUSE = "A flag is refused rather than ignored where it has no work to do here"
REFUSAL_RATIONALE = (
    "a flag accepted and ignored teaches that flags sometimes do nothing"
)


def _records() -> dict[str, list[str]]:
    """Map each four-digit number to the record filenames claiming it."""

    claimed: dict[str, list[str]] = {}
    for path in sorted(ADR.glob("*.md")):
        match = RECORD.match(path.name)
        if match is None:
            continue
        claimed.setdefault(match.group(1), []).append(path.name)
    return claimed


def _sources() -> list[Path]:
    """Every file the collection cites a record from."""

    return (
        sorted(ADR.glob("*.md"))
        + [REPO_ROOT / name for name in CITING_DOCS]
        + sorted(STANDARD_DIR.glob("*.md"))
        + sorted(TESTS.glob("*.py"))
    )


def _citations() -> dict[str, list[str]]:
    """Map each cited number to the files citing it, repository-relative."""

    cited: dict[str, list[str]] = {}
    for path in _sources():
        where = str(path.relative_to(REPO_ROOT))
        for number in CITATION.findall(path.read_text(encoding="utf-8")):
            citing = cited.setdefault(number, [])
            if where not in citing:
                citing.append(where)
    return cited


def test_no_two_records_claim_the_same_number() -> None:
    """A number names one record, or a citation cannot say which it means.

    Only collision is asserted. Gaps in the sequence are legitimate — 0031 to
    0034 are gaps today — so nothing here requires the numbering to be dense.
    """

    collisions = {
        number: names for number, names in _records().items() if len(names) > 1
    }

    assert collisions == {}


def test_every_cited_number_has_a_record() -> None:
    """A citation to a number no file carries is as broken as a stale record."""

    records = _records()
    dangling = {
        number: sources
        for number, sources in _citations().items()
        if number not in records
    }

    assert dangling == {}


def _relations() -> tuple[set[tuple[str, str]], set[tuple[str, str]]]:
    """Collect the supersession relations the records write, from both ends.

    Returns the pointers — each an (earlier, later) pair read off a sentence
    in the earlier record — and the claims, the same pairs read off a later
    record declaring in its own text what it takes over.
    """

    pointers: set[tuple[str, str]] = set()
    claims: set[tuple[str, str]] = set()
    for path in sorted(ADR.glob("*.md")):
        match = RECORD.match(path.name)
        if match is None:
            continue
        number = match.group(1)
        text = path.read_text(encoding="utf-8")
        pointers |= {(number, later) for later in POINTER.findall(text)}
        claims |= {(earlier, number) for earlier in CLAIM.findall(text)}
    return pointers, claims


def test_a_record_named_as_taken_over_carries_a_pointer_back() -> None:
    """A later record's declaration is answered by a pointer in the earlier one.

    A record whose premise a later record narrowed goes on asserting it, and a
    reader looking for how something works finds a confident wrong answer in
    the one place the collection points at for architecture (issue #86). So
    where a record names another as superseded, amended, narrowed, withdrawn
    from, or replaced, the record it names must carry the pointer sentence
    back to it. The relation is written in one direction and checked in both.

    What this cannot see is a later record that never states the relation in
    the declared vocabulary at all — whether prose claims a takeover is a
    reading, not a comparison, which is the same boundary the citation-aptness
    check below states. ADR-0075 makes writing the pointer the later author's
    duty precisely because the scan alone cannot conjure it.
    """

    pointers, claims = _relations()

    # A declaration vocabulary that matched no record would leave the loop
    # with nothing to judge and pass regardless.
    assert claims

    missing = claims - pointers
    assert missing == set(), (
        f"{missing}: each pair is an (earlier, later) relation a later record"
        f" declares in its own text, and the earlier record carries no"
        f" pointer sentence naming the later one back. See ADR-0075."
    )


def test_ticket_resolution_supersession_preserves_blocker_record_history() -> None:
    """The Ticket Resolution model points past ADR-0073 without rewriting
    the closure-based world that earlier record originally decided in."""

    # Read both ends of the supersession relation as repository documentation.
    earlier = (
        ADR
        / "0073-a-discovered-edge-corrects-the-graph-rather-than-burning-the-ticket.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0079-a-run-outcome-is-history-and-a-ticket-resolution-is-current.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "comes back workable when its blocker closes" in earlier
    assert "When the blocker closes" in earlier
    assert "waiting on open work" in earlier
    assert "superseded by ADR-0079" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "supersedes ADR-0073" in later


def test_the_gate_failing_mechanical_recut_preserves_the_wave_check_history() -> None:
    """The re-cut points past ADR-0072 without rewriting the world it decided in.

    ADR-0072 settled that the wave check reads coherence and that its fixes
    loop to a fixed point, both of which stand. Only its comparison of a
    non-mechanical finding to a failed gate was outrun, by a run in which a
    defect was mechanical and gate-failing at once (issue #117).
    """

    earlier = (
        ADR
        / "0072-the-wave-check-reads-coherence-and-its-fixes-loop-to-a-fixed-point.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0098-a-fully-determined-fix-is-mechanical-whatever-the-gate-says.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "it stops the run exactly as a failed gate does" in earlier
    assert "The loop runs to a fixed point" in earlier
    assert "superseded by ADR-0098" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "supersedes ADR-0072" in later

    # The road not taken is named, a fourth shape being a fourth thing two
    # briefs can state inconsistently.
    assert "fourth verdict shape" in later


def test_the_escalated_fix_round_preserves_the_no_progress_bound_history() -> None:
    """The escalation points past ADR-0098 without rewriting the world it decided in.

    ADR-0098's constructive obligation, its single-round bound, and its
    declined-findings bind all stand. Only its closing restatement of the
    no-progress bound — a round that changes nothing stops the run — was
    outrun, by a fixer that may now hold a seat cheaper than the one the
    inference assumed (issue #120).
    """

    earlier = (
        ADR / "0098-a-fully-determined-fix-is-mechanical-whatever-the-gate-says.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0110-a-changed-nothing-fix-round-escalates-once-from-a-selected-seat.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "a round that changes nothing stops the run" in earlier
    assert "buys exactly one fix round" in earlier
    assert "amended by ADR-0110" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "amends ADR-0098" in later

    # The road not taken is named, a no-op on the main seat being the
    # non-mechanical case wearing the mechanical one's clothes.
    assert "unconditional" in later


def test_the_emptying_guard_preserves_the_three_exit_loop_history() -> None:
    """The fourth stop points past ADR-0107 without rewriting its three.

    ADR-0107's fresh delegation, its verification by review, and each of the
    three exits it named all stand. Only its claim that those three are the
    whole of the loop was outrun, by a fixture on which every round made
    relevant progress and the text still came back emptier at a budget of
    three than at a budget of one (issue #144).
    """

    earlier = (
        ADR / "0107-a-correction-is-delegated-fresh-and-verified-by-review.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0120-a-repair-removes-the-pattern-and-not-the-claim-it-carries.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "the loop has three exits" in earlier
    assert "no relevant progress" in earlier
    assert "amended by ADR-0107" not in earlier
    assert "amended by ADR-0120" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "amends ADR-0107" in later

    # The road not taken is named: the two runs the defect was observed on sit
    # either side of the line at almost the same length, so nothing that
    # measures the text can tell them apart.
    assert "shrink" in later


def test_the_command_path_grammar_preserves_the_tldr_record_history() -> None:
    """The command path points past two records without rewriting either.

    ADR-0048's portable standing-instruction mechanism, its two scopes, and
    its persistence decisions all stand; only its closing argument for
    reaching the mode by flags was outrun, by the reserved separator the
    Invocation Envelope gave the whole collection (issue #115). ADR-0080 said
    in passing that it left that grammar intact, and that sentence went with
    it.
    """

    standing = (ADR / "0048-tldr-mode-is-a-standing-instruction.md").read_text(
        encoding="utf-8"
    )
    reframing = (ADR / "0080-tldr-selects-for-the-owner-of-the-outcome.md").read_text(
        encoding="utf-8"
    )
    later = (ADR / "0103-tldr-addresses-its-mode-through-a-command-path.md").read_text(
        encoding="utf-8"
    )

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "the mode reached by flags rather than by bare words" in standing
    assert "A flag can never be mistaken for prose" in standing
    assert "withdrawn by ADR-0103" in standing

    assert "persistence decisions intact" in reframing
    assert "amended by ADR-0103" in reframing

    # Declare the same relations from the later record for the scan in both
    # directions.
    assert "withdraws from ADR-0048" in later
    assert "amends ADR-0080" in later

    # The channel the operand's work moves to, which the removal rests on
    # entirely, and the cost of having to type the separator for it.
    assert "Contextual Instruction" in later
    assert "reserved separator" in later


def test_the_rename_record_settles_one_name_and_leaves_the_standard_alone() -> None:
    """A rename that falsifies no decision takes over no record's ground.

    ADR-0113 settles what this one Skill is called. It names what `tldr` got
    right and what `brief` costs, so the trade is on the record rather than
    only the outcome, and it states no collection-wide rule about whether a
    Skill's name has to hold for every form it offers — which is why the
    coding standard, where a rule binding more than one Skill would have to be
    written, cites it nowhere (issue #124).

    What moved is the pair of assertions that ADR-0113 carried neither a
    pointer nor a takeover claim. It carries a pointer now: ADR-0168 narrowed
    its closing correction of every occurrence of the former name to an
    occurrence that invokes this Skill, and the answering sentence sits beside
    that claim where ADR-0075 puts it (issue #253). The relation is read from
    both ends by the scans above and stands in the floor of relations, so
    dropping the two assertions loses no check. Everything else holds for the
    reason it always did: what a later record outran is one hygiene claim and
    not the naming decision, and a record narrowed from ahead still took over
    nothing behind it and still states no rule the coding standard must carry.
    """

    record = (ADR / "0113-the-reframing-skill-is-named-brief.md").read_text(
        encoding="utf-8"
    )

    # What the old name got right, and what the new one costs.
    assert "instantly legible" in record
    assert "What this costs" in record

    for path in sorted(STANDARD_DIR.glob("*.md")):
        assert "ADR-0113" not in path.read_text(encoding="utf-8"), (
            f"{path}: the rename states no rule binding more than one Skill,"
            f" and a citation here would say it does. See {STANDARD}."
        )


def test_the_derived_valued_registry_preserves_the_hand_list_record_history() -> None:
    """The derivation points past ADR-0096 without rewriting the cost it accepted.

    ADR-0096 settled the spelling a valued flag takes its value in, which
    stands. Only the price it accepted for the check behind that rule — a flag
    table maintained by hand — was outrun, by the first two Skills added after
    it, which introduced six valued flags the table never learned (issue #121).
    """

    earlier = (
        ADR / "0096-a-valued-flag-attaches-its-value-with-an-equals-sign.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR
        / "0105-the-valued-flag-registry-derives-from-the-collections-own-declarations.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "the flag table the check reads is maintained by hand" in earlier
    assert "the price of a scan that does not have to parse Python" in earlier
    assert "narrowed by ADR-0105" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "narrows ADR-0096" in later

    # The road not taken is named: a staleness check cannot see the flag whose
    # every surface spells it wrong, which is the violation the rule exists for.
    assert "staleness check" in later


def test_the_regenerated_collision_preserves_the_repair_record_history() -> None:
    """The regeneration points past ADR-0055 without rewriting what it decided.

    ADR-0055 settled how a collision two builders' decisions produced is
    answered: repaired on the losing branch, verified by a session that did not
    make the resolution, and rebuilt once where that verdict fails. All of that
    stands. Only its claim over every collision was outrun, by the class that
    carries no decision at all — the output of a deterministic command, which
    two builders who each ran it honestly cannot produce the same version of
    (issue #122).
    """

    earlier = (ADR / "0055-a-collision-is-repaired-on-the-losing-branch.md").read_text(
        encoding="utf-8"
    )
    later = (
        ADR / "0106-a-collision-in-generated-files-is-regenerated-not-repaired.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "a resolution that cannot be verified is not a resolution" in earlier
    assert "The repair happens on the losing ticket's own branch" in earlier
    assert "narrowed by ADR-0106" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "narrows ADR-0055" in later

    # The road not taken is named: the README section stays builder-owned,
    # because a ticket whose acceptance criteria name one has to ship it to
    # pass its own verification.
    assert "README" in later


def test_the_suppressed_instruction_preserves_the_envelope_record_history() -> None:
    """The narrowing points past ADR-0078 without rewriting the world it decided in.

    ADR-0078's split, its validation order, its semantic boundaries, and every
    other refusal category it named all stand. Only its word *ineffective* was
    outrun, by an invocation whose Contextual Instruction a documented
    precedence had already settled against — suppression being what that
    precedence is for, and not an error condition (issue #146).
    """

    earlier = (
        ADR
        / "0078-an-invocation-envelope-separates-strict-grammar-from-contextual-instruction.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR
        / "0122-guidance-a-precedence-has-settled-is-suppressed-rather-than-ineffective.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert "materially ambiguous, or scope-widening guidance receives a" in earlier
    assert "Mixed guidance is not partially applied" in earlier
    assert "narrowed by ADR-0122" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "narrows ADR-0078" in later

    # The precedence order itself is untouched: what changed is the fate of a
    # value the order has already settled against.
    assert "precedence order" in later

    # The road not taken is named twice over: rewriting the editorial ladders
    # so that level 3 could not be overridden, and reading the two rules as
    # already reconcilable with the run at fault.
    assert "level 3" in later
    assert "misapplied" in later


def test_the_genre_supplied_technique_preserves_the_no_default_record_history() -> None:
    """The genre's arc points past ADR-0095 without rewriting what it decided.

    ADR-0095's one shared contract, its one file per genre and technique, the
    directory as the list, the refusal of a value with no file, and `general`
    as a complete default contract all stand. Only its clause that there is no
    default technique was outrun, by installed genres that are not neutral
    about the arc they are ordinarily written with — and the reason that
    clause gave, that a technique is never applied because a text resembles
    one, is what the later record leaves exactly as it was.
    """

    earlier = (
        ADR
        / "0095-a-first-drafts-requirements-are-stated-once-and-review-guidance-extends-them.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0164-a-genre-names-the-technique-it-is-ordinarily-written-with.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claims intact and add only the sanctioned pointer.
    assert (
        "a value with no file is refused rather than resolved to a default" in earlier
    )
    assert "never because a text resembles one" in earlier
    assert "amended by ADR-0164" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "amends ADR-0095" in later

    # The prohibition that clause gave its reason for stands, and so does the
    # licence a run has when it infers a genre.
    assert "has not selected one" in later
    assert "ADR-0115" in later

    # The road not taken is named twice over: one arc for the whole Collection,
    # and a registry pairing each genre with its technique.
    assert "default technique for the Collection" in later
    assert "registry" in later


def test_the_rejected_profile_preserves_the_one_missing_facts_record_history() -> None:
    """The split profile state points past ADR-0136 without rewriting it.

    Everything ADR-0136 decided about inheriting rather than triggering setup
    stands, the rejected profile included: it inherits exactly as the absent
    one does. What the later record narrows is that record's premise that a
    missing profile and an invalid one are one state — and the refusal it
    retires was unreachable from every real profile, so no behaviour ADR-0136
    described was ever produced by it.
    """

    earlier = (
        ADR / "0136-model-selector-derives-routing-context-from-shipped-adapters.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0165-a-stored-profile-that-does-not-validate-is-rejected-not-absent.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claim intact and add only the sanctioned pointer.
    assert "A missing or invalid profile, no comparable main seat" in earlier
    assert "preserve the exact main seat" in earlier
    assert "narrowed by ADR-0165" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "narrows ADR-0136" in later

    # What the later record settles: the split itself, the token routing
    # renders it as, and the refusal code that leaves the public Module.
    assert "rejected_profile" in later
    assert "invalid_profile" in later
    assert "setup" in later

    # The road not taken is named: a migration for a shape with exactly one
    # documented version, and refusing the run instead of inheriting.
    assert "No migration is written" in later
    assert "start nothing" in later


def test_the_unattended_refresh_preserves_the_hook_path_record_history() -> None:
    """The bounded network path points past ADR-0090 without rewriting it.

    Everything that record protects about the hook path stands — fail-open,
    bounded, local, every failure swallowed, and no measurement reminder where
    the model reads it. What the later record narrows is the one phrase that
    made the path unable to check whether a source had moved at all.
    """

    earlier = (
        ADR / "0090-a-skill-owns-the-harness-integrations-it-installs.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR
        / "0167-an-unattended-pass-may-learn-what-a-model-can-do-never-what-it-costs.md"
    ).read_text(encoding="utf-8")

    # Keep the historical claim intact and add only the sanctioned pointer.
    assert "no network request, no model call, no test run" in earlier
    assert "narrowed by ADR-0167" in earlier

    # Declare the same relation from the later record for the scan in both
    # directions.
    assert "narrows ADR-0090" in later

    # What the later record settles: the module that performs the pass, the
    # number the budget is, and the field cadence is measured from.
    assert "scripts/refresh.py" in later
    assert "two seconds" in later
    assert "last_retrieved_at" in later

    # The invariant the whole design was bought with, and the fail-closed rule
    # that keeps it true of a source kind nobody has taught it about.
    assert "never what it is judged to cost" in later
    assert "including one absent or unreadable, are treated as commercial" in later

    # The road not taken is named: a daemon, and a reminder inside a routed run.
    assert "no daemon, no cron" in later
    assert "not a routed run's account" in later


def test_the_suspended_ceiling_preserves_both_records_it_narrows() -> None:
    """The unranked main seat points past two records without rewriting either.

    ADR-0083's authority ceiling and ADR-0136's derivation both stand: an
    execution point still cannot exceed a ceiling that exists, and a seat
    absent from the profile still empties the mappings. What the later record
    narrows is what happens where the ceiling cannot be stated at all, and
    what counts as a selection the derivation may admit.
    """

    ceiling = (ADR / "0083-model-selector-owns-exact-frozen-routing.md").read_text(
        encoding="utf-8"
    )
    derivation = (
        ADR / "0136-model-selector-derives-routing-context-from-shipped-adapters.md"
    ).read_text(encoding="utf-8")
    later = (
        ADR / "0166-an-unranked-main-seat-suspends-the-ceiling-it-cannot-state.md"
    ).read_text(encoding="utf-8")

    # Keep both historical claims intact and add only the sanctioned pointers.
    assert "refusals rather than optimistic fallbacks" in ceiling
    assert "narrowed by ADR-0166" in ceiling
    assert "unvalidated selections never become mappings" in derivation
    assert "narrowed by ADR-0166" in derivation

    # Declare the same relations from the later record for the scan in both
    # directions.
    assert "narrows ADR-0083" in later
    assert "narrows ADR-0136" in later

    # What the later record settles: the rank's two sources, the rule for a
    # seat neither of them scores, and the token the empty pool now inherits.
    assert "unavailable_safe_candidate" in later
    assert "no_scored_evaluation_for_main_seat" in later
    assert "candidate coverage alone" in later

    # The substitutes named as rejected, so neither returns as an idea.
    assert "Inheriting a predecessor's score" in later
    assert "top of the ladder" in later


def test_a_pointer_names_a_later_record() -> None:
    """A pointer cites the record that outran the one carrying it.

    The backward half of the check above: every pointer sentence must name a
    record that exists and comes later than the record it stands in — a
    pointer at a number nothing answers to, or at an earlier record, is the
    stale citation this suite already refuses, wearing the convention's
    clothes. The floor of known relations keeps the scan honest: records are
    never rewritten, so these pairs can only grow, and a pattern that cannot
    find them has drifted from the prose and judges nothing.
    """

    records = _records()
    pointers, _ = _relations()

    assert RELATIONS <= pointers, (
        f"the pointer scan missed {RELATIONS - pointers}: these relations are"
        f" in the collection's own prose, so a scan that cannot find them"
        f" judges nothing. See ADR-0075."
    )

    invalid = {
        (earlier, later)
        for earlier, later in pointers
        if later not in records or int(later) <= int(earlier)
    }
    assert invalid == set(), (
        f"{invalid}: a pointer names the record that outran the one carrying"
        f" it, so it must cite a record that exists and comes later."
        f" See ADR-0075."
    )


def _skill_bodies() -> list[Path]:
    """Every `SKILL.md` the collection ships, the Manager's among them."""

    return sorted(SKILLS.glob("*/*/SKILL.md")) + sorted(SKILLS.glob("*/SKILL.md"))


def test_the_flag_refusal_rule_carries_its_rationale_in_every_body() -> None:
    """The installed instruction carries its refusal rationale itself."""

    bodies = _skill_bodies()

    # A glob that matched nothing, or a clause reworded out of every body,
    # would leave the loop below with nothing to judge and pass regardless.
    assert bodies

    carrying: list[str] = []
    unsupported: list[str] = []
    for path in bodies:
        where = str(path.relative_to(REPO_ROOT))
        for paragraph in path.read_text(encoding="utf-8").split("\n\n"):
            if REFUSAL_CLAUSE not in paragraph:
                continue
            carrying.append(where)
            if REFUSAL_RATIONALE not in paragraph:
                unsupported.append(where)

    assert carrying, (
        f"no skill body carries the clause {REFUSAL_CLAUSE!r}, so this check"
        f" judged nothing. Every skill states the flag-refusal rule in that"
        f" wording, and a rewording that drops it takes the check with it."
        f" See {STANDARD}."
    )
    assert unsupported == [], (
        f"{unsupported}: the flag-refusal rule needs the reason an installed"
        f" reader uses to apply it, not repository-only provenance. See"
        f" {STANDARD}."
    )
