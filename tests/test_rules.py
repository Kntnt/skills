"""The rules modules under `docs/rules/`, and the archive they hand a reader."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES = REPO_ROOT / "docs" / "rules"
ADR = REPO_ROOT / "docs" / "adr"

# The module saying where a rule is written down here, the module whose Body
# section it takes the prose half of, and the archive's ingress page. Named
# rather than discovered: what has to hold is that these particular files
# carry these particular rules, and a scan over whatever `docs/rules/` happens
# to hold would pass on a directory that lost the module entirely (issue #267).
DOCS = RULES / "docs.md"
SKILLS = RULES / "skills.md"
GENERAL = RULES / "general.md"
INGRESS = ADR / "README.md"

# The reform's own record, which the module cited by title while it was still
# unwritten and now cites by number, the record having been written (issue
# #271). The number is what a reader can follow and what the suite can refuse
# when nothing answers to it; a title is neither, and it was only ever the
# stand-in for the gap between the module and the record it needed. It is also
# where the retired pointer duty is argued, the record that imposed that duty
# having been folded into it.
REFORM = "ADR-0180"

# The three criteria `/domain-modeling` states, which are the bar a decision
# clears before it earns a record here at all.
CRITERIA = ("hard to reverse", "surprising", "trade-off")

# The `### Body` section of the module governing what a Skill ships, read to
# the next level-two heading.
BODY = re.compile(r"^### Body$(.*?)(?=^## )", re.MULTILINE | re.DOTALL)

# The bullet under `## Collection Library` governing how a Skill reaches a
# peer, matched by its bold lead-in: both ADR-0176 and ADR-0177 address it by
# that name, and a record is never rewritten, so the name is the handle and
# the rest of the line is what this module judges (issue #302).
PEER = re.compile(
    r"^- \*\*Peer internals are not an interface\.\*\*(.*)$", re.MULTILINE
)

# The `### Refactoring completeness` section of the code module, read to the
# next third-level heading. What survives there is the sweep over a symbol's
# callers; the sweep over prose moved to the module a prose author is actually
# routed to (issue #286).
COMPLETENESS = re.compile(
    r"^### Refactoring completeness$(.*?)(?=^### )", re.MULTILINE | re.DOTALL
)

# What a change owes what is already written, stated as claims rather than as
# wording: a rule is a shared contract whose sweep reaches its prose, a surface
# is enumerated by what it asserts, a pointer is enumerated too, and released
# history is left alone. Each has to stand in the module a prose author reads
# and nowhere else, a rule in two places being a rule that can disagree with
# itself (issue #286).
PROSE_SWEEP = (
    "shared contract",
    "what a surface asserts",
    "a pointer asserts nothing",
    "closed tickets",
)

# The pointers a contributor changing only prose meets before they change it,
# each with the line that has to carry them on to the module binding them. Both
# the module and the occasion are judged: the always-loaded guide names the
# module in the path it points at whatever its clause says, and a clause naming
# a narrower occasion is what sends that reader to a module they never open —
# which is what left nine commits of prose work unbound by the rule governing
# it (issue #286).
PROSE_POINTERS = {
    REPO_ROOT / "AGENTS.md": re.compile(
        r"^- `docs/rules/docs\.md` — read when [^\n]+$", re.MULTILINE
    ),
    REPO_ROOT / "CONTRIBUTING.md": re.compile(
        r"^3\. \*\*Follow the project's coding standard\.\*\*[^\n]+$", re.MULTILINE
    ),
    SKILLS: re.compile(
        r"^This module covers the form of a Catalog entry's[^\n]+$", re.MULTILINE
    ),
}


def _docs() -> str:
    """The module saying where a rule and a decision go, lowercased."""

    return DOCS.read_text(encoding="utf-8").lower()


def _peer_bullet() -> str:
    """The peer-internals bullet of `skills.md`, past its bold lead-in."""

    bullet = PEER.search(SKILLS.read_text(encoding="utf-8"))

    # A renamed lead-in would leave nothing to judge and pass regardless, and
    # would falsify two records that cannot be repaired from their own end.
    assert bullet is not None, (
        f"{SKILLS.relative_to(REPO_ROOT)} carries a bullet named **Peer"
        f" internals are not an interface**, which is the name ADR-0176 and"
        f" ADR-0177 both address it by."
    )

    return bullet.group(1)


def test_the_docs_module_separates_what_applies_now_from_why_it_became_so() -> None:
    """Two functions were living in one format, and only one document can serve each.

    `docs/rules/` answers what applies now and is edited whenever a rule
    changes; `docs/adr/` answers why a rule became what it is and is never
    rewritten, which is exactly why it cannot answer the first question. An
    agent that has to derive today's law by reading the archive forward is the
    cost this split removes, so the module has to state both halves and the
    relation between them (issue #267).
    """

    assert DOCS.exists(), f"{DOCS.relative_to(REPO_ROOT)} is where the model is stated."

    text = _docs()

    for phrase in (
        "docs/rules/",
        "docs/adr/",
        "historical archive",
        "loaded by default",
    ):
        assert phrase in text, (
            f"{phrase!r}: {DOCS.relative_to(REPO_ROOT)} states which document"
            f" is the authority on the present and which is the archive."
        )

    assert "edited rather than grown" in text, (
        f"{DOCS.relative_to(REPO_ROOT)} says how the rules modules are kept"
        f" current, a module grown by accretion being the pile again."
    )


def test_the_docs_module_states_the_bar_a_record_clears() -> None:
    """An archive that admits everything costs every later reader the same attention.

    The three criteria are what keep a how-text wearing a why-document's
    clothes out of `docs/adr/`, and a decision failing any of them is a rule
    that goes in a module instead. They are stated where a contributor is
    already asking where something goes (issue #267).
    """

    text = _docs()

    for criterion in CRITERIA:
        assert criterion in text, (
            f"{criterion!r}: {DOCS.relative_to(REPO_ROOT)} states the three"
            f" criteria `/domain-modeling` holds a record to."
        )


def test_the_docs_module_leaves_one_skills_own_rule_out_of_the_centre() -> None:
    """Audience decides placement, and it decides it before format does.

    A rule only one Skill obeys is met by its reader in that Skill's own
    shipped files, and a second statement in a rules module is a second thing
    to keep true for a reader who was never going to look there (issue #267).
    """

    text = _docs()

    assert "one skill's own behaviour" in text, (
        f"{DOCS.relative_to(REPO_ROOT)} states that a rule governing one"
        f" Skill's own behaviour lives in that Skill's shipped files."
    )
    assert "audience" in text, (
        f"{DOCS.relative_to(REPO_ROOT)} states the test that settles where a"
        f" document goes: who has to read it."
    )


def test_the_docs_module_states_the_convention_the_always_loaded_file_is_written_to() -> (
    None
):
    """`AGENTS.md` is loaded into every session, so a rule stated there is loaded too.

    What it does instead is route, and every entry is written to one shape so
    that a reader skimming for the occasion finds the file. The module that
    says where a document goes is where that convention is stated (issue #267).
    """

    text = _docs()

    assert "agents.md" in text and "read when" in text, (
        f"{DOCS.relative_to(REPO_ROOT)} states that `AGENTS.md` is a pointer"
        f" list written to the `read when` convention."
    )


def test_the_docs_module_retires_the_outrun_pointer_duty() -> None:
    """The pointer duty existed because the archive was read as current law.

    A record whose premise a later one replaced went on asserting it, and the
    reader who had nowhere better to look found a confident wrong answer. The
    rules modules remove that reader, so the archive no longer has to be kept
    self-consistent about a question it is not asked — and the module is the
    only place that says so, every record written while the duty stood being
    immutable and read as of its own date (issue #267).
    """

    text = DOCS.read_text(encoding="utf-8")

    assert "retired" in text.lower(), (
        f"{DOCS.relative_to(REPO_ROOT)} says the outrun-pointer duty is"
        f" retired, in that word."
    )
    assert REFORM in text, (
        f"{REFORM}: the reform's own record is cited by number, which is where"
        f" the reasoning for retiring the duty is carried."
    )


def test_the_docs_module_puts_a_skill_body_under_the_writing_skill() -> None:
    """A Skill body is an instruction loaded into somebody else's session.

    `skills.md` governs what the body carries; how its prose is written is
    `/writing-for-agents`, and the two are read together. The pointer lives
    here because this is the module about how a document is authored (issue
    #267).
    """

    text = _docs()

    assert "/writing-for-agents" in text, (
        f"{DOCS.relative_to(REPO_ROOT)} states that every Skill body is"
        f" authored under `/writing-for-agents`."
    )


def test_the_body_section_hands_a_skill_author_the_prose_half() -> None:
    """An author reading `skills.md` meets what the body carries and nothing about how.

    The two halves are split across two modules, and the split is invisible
    from the module an author actually opens unless that module says where the
    other half is (issue #267).
    """

    section = BODY.search(SKILLS.read_text(encoding="utf-8"))

    # A renamed heading, or a level this pattern stops matching, would leave
    # nothing to judge and pass regardless.
    assert section is not None, (
        f"{SKILLS.relative_to(REPO_ROOT)} carries a `### Body` section, which"
        f" is where a body's requirements are stated."
    )

    assert "docs.md" in section.group(1), (
        f"{SKILLS.relative_to(REPO_ROOT)}'s Body section points at"
        f" {DOCS.relative_to(REPO_ROOT)} for how a body's prose is written."
    )


def test_the_archive_ingress_hands_the_present_to_the_rules_modules() -> None:
    """A reader who opens `docs/adr/` needs to be told what it is before they read it.

    Every file under it is a record of its own date, and the directory as a
    whole states what was decided at many dates with nothing in it saying
    which survived. The ingress says so, names where the present is stated,
    and says that nothing here is annotated when it is outrun — the absence of
    a pointer meaning nothing at all (issue #267).
    """

    assert INGRESS.exists(), (
        f"{INGRESS.relative_to(REPO_ROOT)} is the archive's ingress page."
    )

    text = INGRESS.read_text(encoding="utf-8").lower()

    assert "historical" in text, (
        f"{INGRESS.relative_to(REPO_ROOT)} says the directory is historical."
    )
    assert "docs/rules/" in text, (
        f"{INGRESS.relative_to(REPO_ROOT)} names the rules modules as the"
        f" authority on what applies now."
    )
    assert "as of its own date" in text, (
        f"{INGRESS.relative_to(REPO_ROOT)} says a record is read as of its own date."
    )
    assert "annotat" in text, (
        f"{INGRESS.relative_to(REPO_ROOT)} says nothing here is annotated"
        f" when a later decision outruns it."
    )


def test_the_peer_bullet_admits_a_peers_documented_interface_script() -> None:
    """Two modules stated one question as law and gave it opposite answers.

    `skills.md` said a Skill never runs a peer's `scripts/`, while
    `routing.md` says that no Skill invokes Model Selector as a Skill and that
    a Skill routing work runs its script (ADR-0182) — which is what Orchestrate
    and delegation mode both do. The bullet therefore carries the one
    exception, and names the one script there is today, so that a second one
    is added to the sentence rather than smuggled past it (issue #302).
    """

    text = _peer_bullet()

    assert "exception" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet states the exception"
        f" for a peer's documented machine interface, without which it"
        f" contradicts `routing.md`."
    )
    assert "selection.py" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet names Model Selector's"
        f" `selection.py` as the one such script there is today."
    )
    assert "ADR-0182" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet cites ADR-0182 on the"
        f" exception, the record that made the script the machine interface."
    )


def test_the_peer_bullet_keeps_what_the_exception_does_not_license() -> None:
    """An exception nobody bounded is the prohibition gone rather than narrowed.

    What is licensed is running the documented entry point on the documented
    terms. The peer's other files, a reimplementation of what the script does,
    and that peer's own data are all still out of reach, and the bullet says
    so in its own words rather than leaving a reader to infer it (issue #302).
    """

    text = _peer_bullet()

    assert "never reads the peer's `references/`" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet still forbids reading"
        f" a peer's `references/`, which no exception reaches."
    )
    assert "reimplement" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet says the exception"
        f" licenses no reimplementation of what the script does."
    )
    assert "data" in text, (
        f"{SKILLS.relative_to(REPO_ROOT)}'s peer bullet says the exception"
        f" reaches nothing of the peer's own data."
    )


def _completeness() -> str:
    """The `### Refactoring completeness` section of `general.md`."""

    section = COMPLETENESS.search(GENERAL.read_text(encoding="utf-8"))

    # A renamed heading would leave nothing to judge and pass regardless.
    assert section is not None, (
        f"{GENERAL.relative_to(REPO_ROOT)} carries a `### Refactoring"
        f" completeness` section, which is where a change's sweep is stated."
    )

    return section.group(1)


def test_the_docs_module_states_what_a_change_owes_what_is_already_written() -> None:
    """A documented rule is a shared contract, and its surfaces are prose.

    The rules governing a change to what this repository has written down sat
    in the module named for code, which every pointer announces as the module
    for writing code, so a contributor editing a glossary entry, a manpage or a
    rules module was bound by them and routed away from them. They belong in
    the module that already governs where a rule is written down (issue #286).
    """

    text = _docs()

    for claim in PROSE_SWEEP:
        assert claim in text, (
            f"{claim!r}: {DOCS.relative_to(REPO_ROOT)} states what a change"
            f" owes the prose already stating what it changes."
        )


def test_the_code_module_keeps_the_caller_sweep_and_hands_the_prose_one_on() -> None:
    """One rule, one module: the code half stays where a code change meets it.

    Enumerating a symbol's callers is code work and is met by a reader
    changing code. The prose half moved, so what stays points at where it
    went, and none of what moved is left behind to be kept true twice (issue
    #286).
    """

    section = _completeness()

    assert "enumerate every caller" in section, (
        f"{GENERAL.relative_to(REPO_ROOT)} keeps the rule on enumerating a"
        f" shared symbol's callers, which is code work."
    )
    assert "docs.md" in section, (
        f"{GENERAL.relative_to(REPO_ROOT)} points at"
        f" {DOCS.relative_to(REPO_ROOT)} for the half of the sweep that"
        f" reaches prose, so a reader changing both is sent on."
    )

    text = GENERAL.read_text(encoding="utf-8").lower()
    for claim in PROSE_SWEEP:
        assert claim not in text, (
            f"{claim!r}: {GENERAL.relative_to(REPO_ROOT)} still states what"
            f" moved to {DOCS.relative_to(REPO_ROOT)}, so the rule stands in"
            f" two modules and can disagree with itself."
        )


def test_every_pointer_a_prose_change_meets_names_the_module_binding_it() -> None:
    """A pointer asserts nothing, so no search for the rule's content reaches one.

    A contributor who edits only prose meets the always-loaded guide, the
    contributor guide, and the module for whatever they touch. Each has to
    carry them to the module holding the rules that bind them, or the rule is
    documented and unreachable from every direction its reader arrives from
    (issue #286).
    """

    for path, line in PROSE_POINTERS.items():
        match = line.search(path.read_text(encoding="utf-8"))

        # A reworded pointer this pattern stops matching would leave nothing
        # to judge and pass regardless.
        assert match is not None, (
            f"{path.relative_to(REPO_ROOT)} carries the pointer a contributor"
            f" changing prose meets there."
        )
        for named in ("docs.md", "already written"):
            assert named in match.group(0), (
                f"{named!r}: the pointer a prose change meets in"
                f" {path.relative_to(REPO_ROOT)} does not send that"
                f" contributor to {DOCS.relative_to(REPO_ROOT)} for a change"
                f" to what is already written, so it routes them past the"
                f" rules binding them."
            )
