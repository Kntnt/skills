"""What every Skill's `argument-hint` advertises, held to what its engine accepts.

The hint is the grammar the harness shows before anything is typed, and the
only one of the three grammar surfaces a user meets unasked. It is one line, so
it may write once what several forms share; what it may not do is advertise a
form the engine refuses, drop one the engine accepts, or write one flag twice
for forms that could have shared it (ADR-0176, ADR-0181).
"""

from __future__ import annotations

import dataclasses
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import pytest
from support.contract import STANDARD
from support.hint import FLAG, Form, form_text, hint_forms, read_hint, to_synopsis

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"
MANAGER_DIR = SKILLS / "kntnt"
KNTNT_PY = MANAGER_DIR / "scripts" / "kntnt.py"
PROOFREAD_DIR = SKILLS / "editorial" / "proofread"

EXIT_VALID = 0
EXIT_REFUSED = 2


def _engine() -> Any:
    """Load the Manager's script so its grammar reader can be called in-process."""

    spec = importlib.util.spec_from_file_location("kntnt_argument_hint", KNTNT_PY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ENGINE = _engine()


def _shipped_skills() -> list[Path]:
    """Every Skill directory the collection ships, the Manager's among them."""

    directories = [p.parent for p in sorted(SKILLS.glob("*/*/SKILL.md"))]
    return [*directories, MANAGER_DIR]


def _normal(form: Any) -> tuple[Any, ...]:
    """One engine-read form, with what differs only in wording taken out.

    The operand's label is the metavariable's name, which the hint writes in
    lower case and the page in capitals; the flags are a set, their order in a
    form being no part of what the engine accepts.
    """

    operands = tuple(dataclasses.replace(unit, label="") for unit in form.operands)
    return (form.path, frozenset(form.flags), operands)


def _advertised(directory: Path, hint: str) -> list[tuple[Form, Any]]:
    """Each form *hint* advertises, beside the engine's reading of it."""

    known = ENGINE.command_paths(directory)
    return [
        (form, ENGINE.parse_form(to_synopsis(directory.name, form), known))
        for form in hint_forms(hint)
    ]


def _grammar_faults(directory: Path, hint: str) -> list[str]:
    """Where *hint* advertises other forms than the Skill's root page admits."""

    advertised = _advertised(directory, hint)
    page = ENGINE.page_grammar(directory, directory / "help.md")
    admitted = {_normal(form) for form in page.forms}
    offered = [_normal(read) for _, read in advertised]

    faults = [
        f"the hint advertises `{form_text(form) or '(nothing)'}`, which no"
        f" `## SYNOPSIS` form admits"
        for form, read in advertised
        if _normal(read) not in admitted
    ]
    faults += [
        f"the hint advertises `{form_text(form) or '(nothing)'}` twice"
        for index, (form, read) in enumerate(advertised)
        if _normal(read) in offered[:index]
    ]
    faults += [
        f"the `## SYNOPSIS` form `{line}` is advertised by no form of the hint"
        for line, form in zip(
            [ln for ln in ENGINE.synopsis_of(page.page).splitlines() if ln.strip()],
            page.forms,
            strict=True,
        )
        if _normal(form) not in offered
    ]
    return faults


def _repeated_flags(directory: Path, hint: str) -> list[str]:
    """Flags the hint writes more than once for forms of one command path.

    Two forms of one command path take their flags from one page, so a flag
    they share is written once and the forms that differ are grouped after
    it. Forms of different command paths are different pages, and a flag each
    of them takes is rightly written once per path.
    """

    written: dict[tuple[tuple[frozenset[str], ...], str], set[int]] = defaultdict(set)
    for form, read in _advertised(directory, hint):
        path = tuple(unit.alternatives for unit in read.path)
        flags = form[len(read.path) : len(read.path) + len(read.flags)]
        for unit in flags:
            for match in FLAG.finditer(unit.text):
                written[(path, match.group("name"))].add(unit.start + match.start())
    return [
        f"`{name}` is written {len(starts)} times for"
        f" {' '.join(min(p) for p in path) or 'the root'}'s forms"
        for (path, name), starts in written.items()
        if len(starts) > 1
    ]


@pytest.mark.parametrize("directory", _shipped_skills(), ids=lambda d: d.name)
def test_every_hint_advertises_exactly_the_forms_its_synopsis_admits(
    directory: Path,
) -> None:
    """The hint may collapse forms the page spells out; it may not change them.

    Each form the hint advertises is read by the engine that reads the page,
    so a form is compared as the engine would hold a user to it: its command
    path, its flags with how each takes a value and whether it repeats, and
    its operands. A hint advertising `/delegation --yes` offers a form the
    page refuses; one hiding that `--on` repeats drops one the page admits.
    """

    faults = _grammar_faults(directory, read_hint(directory))

    assert not faults, (
        f"{directory.relative_to(REPO_ROOT)}: {'; '.join(faults)}. The"
        f" `argument-hint` is the grammar the harness shows, and a form it"
        f" advertises that the engine refuses — or one it hides that the"
        f" engine accepts — is a disagreement a user meets as a refusal or"
        f" never meets at all (ADR-0176, ADR-0181). See {STANDARD}."
    )


@pytest.mark.parametrize("directory", _shipped_skills(), ids=lambda d: d.name)
def test_no_hint_writes_a_flag_twice_for_one_command_path(directory: Path) -> None:
    """A flag common to forms of one command path is written once."""

    repeated = _repeated_flags(directory, read_hint(directory))

    assert not repeated, (
        f"{directory.relative_to(REPO_ROOT)}: {'; '.join(repeated)}. Forms of"
        f" one command path share their page, so a flag they share is written"
        f" once before a group of what differs —"
        f" `[--language=<language>] ([--output=<target>] [<text>] |"
        f" --in-place <path>)` — rather than once per form. See {STANDARD}."
    )


SUFFIX = " [-- <instruction>]"


@pytest.mark.parametrize(
    ("directory", "hint"),
    [
        # A path left optional in front of its flags advertises the bare Skill
        # with flags the bare form refuses: `/delegation --yes`.
        (
            SKILLS / "agents" / "delegation",
            "[on|off] [--project|--user] [--yes] | status [--project|--user]" + SUFFIX,
        ),
        # A repeatable flag written as though it were single drops a form.
        (
            MANAGER_DIR,
            read_hint(MANAGER_DIR).replace("[--on=<entry> ...]", "[--on=<entry>]"),
        ),
        # A metavariable written bare reads as a literal word.
        (SKILLS / "agents" / "agents-md", "[--force] [--yes] [path]" + SUFFIX),
        # Destinations offered side by side advertise a combination the page
        # refuses.
        (
            PROOFREAD_DIR,
            "[--language=<language>] [--output=response|<path>]"
            " [--in-place[=on|off]] [<text>|<path>|<url>]" + SUFFIX,
        ),
    ],
    ids=[
        "optional-path",
        "single-repeatable",
        "bare-metavariable",
        "both-destinations",
    ],
)
def test_the_form_check_fails_a_hint_that_misstates_its_forms(
    directory: Path, hint: str
) -> None:
    """Each fault the form check exists for is one it reports."""

    assert hint != read_hint(directory)
    assert _grammar_faults(directory, hint)


def test_the_repetition_check_fails_one_path_and_passes_many() -> None:
    """A flag written per form of one path is caught; one written per path is not.

    The Proofread hint before issue #324 is the fault: two forms of the root
    path, each writing `--language` again. Model Selector writing `--data` on
    every subcommand is the repetition the check has to leave alone.
    """

    written_twice = (
        "[--language=<language>] [--output=response|<path>] [<text>|<path>|<url>]"
        " | [--language=<language>] --in-place[=on|off] <path>" + SUFFIX
    )
    selector = SKILLS / "models" / "model-selector"

    assert _repeated_flags(PROOFREAD_DIR, written_twice)
    assert not _grammar_faults(PROOFREAD_DIR, written_twice)
    assert not _repeated_flags(selector, read_hint(selector))


@pytest.mark.parametrize("directory", _shipped_skills(), ids=lambda d: d.name)
def test_no_hint_puts_literal_values_inside_a_metavariable(directory: Path) -> None:
    """A metavariable names one replaceable value; its alternatives stand bare.

    `--output=response|<path>` says `response` is typed as it stands and the
    path is the user's; `--output=<response|path>` says neither.
    """

    offending = re.findall(r"<[^>]*\|[^>]*>", read_hint(directory))

    assert not offending, (
        f"{directory.relative_to(REPO_ROOT)}: the `argument-hint` writes"
        f" {offending}, alternatives inside one metavariable. A literal is"
        f" written bare and each metavariable in its own angle brackets —"
        f" `yes|no`, `response|<path>`, `<name>|<path>`. See {STANDARD}."
    )


def test_proofreads_hint_shares_language_across_both_destinations() -> None:
    """Issue #324's case: `--language` once, and the destinations exclusive."""

    hint = read_hint(PROOFREAD_DIR)
    advertised = _advertised(PROOFREAD_DIR, hint)
    flag_sets = [
        {
            spec.name
            for group in read.flags
            for alternative in group.alternatives
            for spec in alternative
        }
        for _, read in advertised
    ]

    assert hint.count("--language") == 1
    assert flag_sets == [
        {"--language", "--output"},
        {"--language", "--in-place"},
    ]
    delivered, in_place = (read for _, read in advertised)
    assert [unit.optional for unit in delivered.operands] == [True]
    assert [unit.optional for unit in in_place.operands] == [False]

    for payload, status in (
        ("--language=sv --output=out.md report.md", EXIT_VALID),
        ("--language=sv report.md", EXIT_VALID),
        ("--language=sv --in-place report.md", EXIT_VALID),
        ("--language=sv --in-place=off report.md", EXIT_VALID),
        ("--language=sv --in-place", EXIT_REFUSED),
        ("--language=sv --output=out.md --in-place report.md", EXIT_REFUSED),
    ):
        reading = ENGINE.read_invocation(PROOFREAD_DIR, payload)
        assert reading.status == status, (payload, reading.text)
