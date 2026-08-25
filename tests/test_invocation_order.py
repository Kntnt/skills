"""The one order a Formal Invocation of this collection's grammar is written in."""

from __future__ import annotations

import re
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"

# The record settling the order, cited by every failure below and by the
# rules document's own statement of the rule.
RECORD = "ADR-0097"

# The optional Contextual Instruction closes every form and belongs to no
# region of the order, so it is removed before a form is read (ADR-0078). It is
# matched after the emphasis has gone, which is the one spelling both the
# manpage form and the harness hint share.
SUFFIX = re.compile(r"\[--\s*(?:INSTRUCTION|<instruction>)\]\s*$")

# A flag's attached value is part of the flag rather than an operand beside it
# (ADR-0096): the bracketed optional spelling, a metavariable that may itself
# offer alternatives, and a plain value, which carries any bare alternatives
# written after it rather than letting them read as operands.
ATTACHED_GROUP = re.compile(r"\[=[^\]]*\]")
ATTACHED_META = re.compile(r"=<[^>]*>")
ATTACHED_VALUE = re.compile(r"=[^\s\]|)]*(?:\|[^\s\]|)-][^\s\]|)]*)*")

# What separates the atoms inside one unit: whitespace, the alternation bar,
# and the brackets that group alternatives.
ATOMS = re.compile(r"[\s\[\]()|]+")


def _shipped_skills() -> list[Path]:
    """Every Skill directory the collection ships, the Manager's among them."""

    return sorted(SKILLS.glob("*/*/SKILL.md")) + sorted(SKILLS.glob("*/SKILL.md"))


def _command_paths(directory: Path) -> set[str]:
    """Every command path a page under this Skill's `help/` answers to.

    This is the boundary the order rule draws between the command path and the
    operands: a token belongs to the path when a page answers to it, which a
    builder can test against the shipped tree rather than against judgement
    (ADR-0077).
    """

    root = directory / "help"
    return {
        " ".join(page.relative_to(root).with_suffix("").parts)
        for page in root.rglob("*.md")
    }


def _hint(directory: Path) -> str:
    """Return one Skill's `argument-hint`, the grammar the harness shows."""

    for line in (directory / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("argument-hint:"):
            return line.partition(":")[2].strip().strip("\"'")
    raise AssertionError(f"{directory}: every Skill declares an `argument-hint`.")


def _synopsis(page: Path) -> list[str]:
    """Return every form of a manpage's `## SYNOPSIS`, one per line."""

    text = page.read_text(encoding="utf-8")
    if "\n## SYNOPSIS\n" not in text:
        return []
    section = text.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    return [line.strip() for line in section.splitlines() if line.strip()]


def _units(form: str) -> list[str]:
    """Split one form into its units, a bracketed group counting as one.

    Markup carries the semantics rather than the structure, so the emphasis is
    removed first and the split is made on whitespace outside any bracket. That
    keeps an attached value, a repeat marker, and an optional value group with
    the token they belong to: `[--on=SKILL]...` is one unit and not three.
    """

    form = SUFFIX.sub("", form.replace("**", "").replace("*", "").strip()).strip()

    units: list[str] = []
    current: list[str] = []
    depth = 0
    for character in form:
        if character in "[(":
            depth += 1
        elif character in "])":
            depth -= 1
        if character.isspace() and depth == 0:
            if current:
                units.append("".join(current))
                current = []
            continue
        current.append(character)
    if current:
        units.append("".join(current))
    return units


def _atoms(unit: str) -> list[str]:
    """Return the alternatives one unit offers, its attached values removed."""

    bare = ATTACHED_VALUE.sub("", ATTACHED_META.sub("", ATTACHED_GROUP.sub("", unit)))
    return [atom.rstrip(".") for atom in ATOMS.split(bare) if atom.strip(".")]


def _classify(unit: str) -> str:
    """Return `flag`, `operand`, or `mixed` for one unit's alternatives."""

    atoms = _atoms(unit)
    flags = any(atom.startswith("--") for atom in atoms)
    operands = any(not atom.startswith("--") for atom in atoms)
    if flags and operands:
        return "mixed"
    return "flag" if flags else "operand"


def _extends(unit: str, path: list[str], known: set[str]) -> bool:
    """Whether every alternative this unit offers extends the command path."""

    atoms = _atoms(unit)
    return bool(atoms) and all(" ".join([*path, atom]) in known for atom in atoms)


def violations(
    form: str, known: set[str], starts_with_command: bool = False
) -> list[str]:
    """Return what is out of order in one form, as one sentence per fault.

    A form is the command path, then the flags, then the operands (ADR-0097).
    An alternation naming both spellings of one slot is a single slot rather
    than a sequence, so it is read as one unit and allowed only at the boundary
    between the two regions: everything before it path or flag, everything
    after it operand.
    """

    units = _units(form)
    if starts_with_command and units:
        units = units[1:]

    # Consume the command path, which is what a page under `help/` answers to.
    path: list[str] = []
    while units and _extends(units[0], path, known):
        path.append(_atoms(units[0])[0])
        units.pop(0)

    faults: list[str] = []
    operands = False
    for unit in units:
        kind = _classify(unit)
        if _extends(unit, path, known):
            faults.append(
                f"the subcommand token `{unit}` follows a flag, and the command"
                f" path comes first"
            )
        elif kind == "flag" and operands:
            faults.append(f"the flag `{unit}` follows an operand")
        elif kind == "mixed" and operands:
            faults.append(
                f"`{unit}` names a flag spelling after an operand, so the form"
                f" does not say which region it sits in"
            )
        if kind != "flag":
            operands = True
    return faults


# One line per surface the scan reads, each carrying a form it has to refuse:
# a hint whose operand precedes its flags, a synopsis form doing the same, a
# subcommand token written after a flag, and a compliant form of each shape
# that it must leave alone.
SAMPLE = (
    ("[<message>] [--yes]", False),
    ("**/commit** [*MESSAGE*] [**--yes**]", True),
    ("**/orchestrate** [**--yes**] **reconcile** *TICKET*", True),
    ("[--yes] [<message>]", False),
    ("**/commit** [**--yes**] [*MESSAGE*]", True),
    ("**/delegation** [**session**|**--session**]", True),
)


def test_the_scan_recognises_an_out_of_order_form_in_each_surface() -> None:
    """An empty result has to mean compliance rather than a broken pattern."""

    known = {"reconcile"}
    found = [
        bool(violations(form, known, starts_with_command))
        for form, starts_with_command in SAMPLE
    ]

    assert found == [True, True, True, False, False, False]


def test_every_argument_hint_writes_its_forms_in_the_invocation_order() -> None:
    """The harness advertises the order the Skill accepts (ADR-0097)."""

    skills = _shipped_skills()

    # A glob that matched nothing would pass the loop below without reading a
    # single hint, which is the one outcome this test exists to catch.
    assert skills

    for body in skills:
        directory = body.parent
        known = _command_paths(directory)
        for form in _hint(directory).split(" | "):
            for fault in violations(form, known):
                raise AssertionError(
                    f"{directory.relative_to(REPO_ROOT)}: in the"
                    f" `argument-hint` form `{form.strip()}`, {fault}. A Formal"
                    f" Invocation is written in one order — the command path,"
                    f" then the flags, then the operands, then the reserved"
                    f" separator — so that everything after the first operand"
                    f" is operand and a free-text message may contain a word"
                    f" that looks like a flag ({RECORD}). See {STANDARD}."
                )


def test_every_synopsis_form_writes_itself_in_the_invocation_order() -> None:
    """The page a refusal quotes shows the order the refusal enforces."""

    pages = [
        (directory, page)
        for directory in (body.parent for body in _shipped_skills())
        for page in [directory / "help.md", *sorted((directory / "help").rglob("*.md"))]
        if page.exists()
    ]

    # The same defence as above: a page list that came back empty would leave
    # this check judging nothing at all.
    assert pages

    for directory, page in pages:
        known = _command_paths(directory)
        for form in _synopsis(page):
            for fault in violations(form, known, starts_with_command=True):
                raise AssertionError(
                    f"{page.relative_to(REPO_ROOT)}: in the `## SYNOPSIS` form"
                    f" `{form}`, {fault}. A Formal Invocation is written in one"
                    f" order — the command path, then the flags, then the"
                    f" operands, then the reserved separator — and this is the"
                    f" page a refusal prints verbatim ({RECORD}). See"
                    f" {STANDARD}."
                )


def test_the_standard_states_the_order_and_cites_the_record() -> None:
    """The rule is written where a contributor reads it before anything fails."""

    text = (REPO_ROOT / STANDARD).read_text(encoding="utf-8")

    assert "the command path, then the flags, then the operands" in text, (
        f"{STANDARD}: the Skills module states the order a Formal Invocation is"
        f" written in, because a contributor who has not written anything yet"
        f" cannot be helped by an assertion message ({RECORD})."
    )
    assert RECORD in text, (
        f"{STANDARD}: the rule is cited to {RECORD}, which carries the"
        f" reasoning and the alternative it was chosen over."
    )
