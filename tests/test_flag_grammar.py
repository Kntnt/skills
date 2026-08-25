"""The one spelling a flag of this collection's own grammar takes its value in."""

from __future__ import annotations

import re
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"
DOCS = REPO_ROOT / "docs"

# The record settling the spelling, cited by every failure below and by the
# coding standard's own statement of the rule.
RECORD = "ADR-0096"

# Every long flag of this collection's own grammar that carries a value —
# whether it is written by a user at a Skill's invocation surface or by a Skill
# body constructing a call to one of the collection's Python engines. A flag
# taking no value is absent, because nothing about it is under this rule, and
# so is every flag belonging to `git`, `gh`, `uv`, or `npx`, whose grammar is
# not this collection's to normalise (ADR-0096).
VALUED_FLAGS = frozenset(
    {
        "--action",
        "--artifact",
        "--asset",
        "--at-once",
        "--attempt",
        "--blocked-by",
        "--budget",
        "--collided-with",
        "--command",
        "--commit",
        "--data",
        "--decision",
        "--deliberation",
        "--event",
        "--harness",
        "--here",
        "--id",
        "--message",
        "--metrics",
        "--model",
        "--off",
        "--on",
        "--outcome",
        "--owner",
        "--phase",
        "--project",
        "--quality",
        "--request",
        "--resolved-model",
        "--resources",
        "--response",
        "--review",
        "--root",
        "--scope",
        "--seat",
        "--started-at",
        "--state-dir",
        "--ticket",
        "--verdict-file",
        "--version",
    }
)

# A long flag, wherever one is written: never mid-word, and never the tail of
# an attached value that happens to contain a hyphen.
FLAG = re.compile(r"(?<![\w=-])(--[a-z][a-z0-9-]*)")

# An inline code span, which is how this collection writes a command line
# inside prose.
CODE_SPAN = re.compile(r"`([^`\n]+)`")

# A manpage synopsis or option term: the flag in bold, then its metavariable
# in italics. The attached form closes the bold run after the `=`, so this
# pattern sees only the separated one.
BOLD_TERM = re.compile(r"\*\*(--[a-z][a-z0-9-]*)\*\*[ \t]+([*_<]\S*)")

# A manpage example or `SEE ALSO` entry, which is a whole invocation in one
# bold run rather than a code span.
BOLD_INVOCATION = re.compile(r"\*\*(/[^*\n]+)\*\*")

# What counts as a value following a flag rather than the next word of a
# sentence: anything a command line would put there. A token opening a bracket
# or another flag is neither.
VALUE = re.compile(r"^(?:[<\"'$]|[*_][A-Za-z]|[A-Za-z0-9])")


# One line per surface the scan reads, each carrying a flag it has to catch and
# a flag it must leave alone: the frontmatter hint, a body's engine invocation,
# a manpage term, a manpage example, a fenced block, a bare mention in prose, an
# already-attached value, and the optional value written bare.
SAMPLE = """argument-hint: '[--at-once <n>] [--yes]'
Run `uv run engine.py record --ticket <number>` and read what it says.
**--commit** *COMMIT*
**/example select --on release --yes**
```
uv run engine.py apply commit --message hello
```
The `--on` and `--off` names are applied as a delta.
Run `uv run engine.py plan --at-once=2 --dry-run` first.
**--project**[=**on**|**off**]
"""


def _scanned() -> list[Path]:
    """Every file this rule is read out of, repository order.

    The files a Skill ships and the documents the coding standard governs. The
    changelog and the closed tickets are deliberately outside it: they record
    what was true when they were written (ADR-0096).
    """

    roots = sorted(SKILLS.rglob("*.md")) + sorted(DOCS.rglob("*.md"))
    named = [REPO_ROOT / name for name in ("README.md", "CONTEXT.md", "AGENTS.md")]
    return roots + [path for path in named if path.exists()]


def _in_command_line(fragment: str) -> list[tuple[str, str]]:
    """Return each valued flag in *fragment* that is followed by a space value."""

    found: list[tuple[str, str]] = []
    for match in FLAG.finditer(fragment):
        name = match.group(1)
        if name not in VALUED_FLAGS:
            continue

        # An attached value is the compliant spelling, and a flag written bare
        # ends its token — neither is followed by whitespace here.
        rest = fragment[match.end() :]
        if not rest[:1].isspace():
            continue

        # Only a token a command line would read as this flag's value counts.
        # The next flag, a closing bracket, or the next word of a sentence is
        # not one.
        token = rest.split(maxsplit=1)[0] if rest.strip() else ""
        if not token or token.startswith("-") or not VALUE.match(token):
            continue
        found.append((name, token))
    return found


def violations(text: str) -> list[tuple[int, str, str]]:
    """Return every space-separated valued flag in *text* as (line, flag, value).

    Four surfaces carry a command line in this collection, and each is read
    where it is written rather than by flattening the file: a fenced block; an
    inline code span, which is how a body writes an engine invocation and how
    the README and `CONTEXT.md` write an invocation of a Skill; a bold
    invocation, which is how a manpage writes an example; and a manpage option
    term, where the flag is bold and its metavariable italic.
    """

    found: list[tuple[int, str, str]] = []
    fenced = False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue

        # Inside a fence the whole line is a command line; outside one, the
        # code spans are, and so is the `argument-hint` the frontmatter carries.
        fragments = [line] if fenced else [m.group(1) for m in CODE_SPAN.finditer(line)]
        if not fenced:
            fragments += [m.group(1) for m in BOLD_INVOCATION.finditer(line)]
            if line.startswith("argument-hint:"):
                fragments.append(line)
        for fragment in fragments:
            found += [
                (number, flag, value) for flag, value in _in_command_line(fragment)
            ]

        # The manpage form is markup rather than a code span, so it is read on
        # its own terms.
        if not fenced:
            found += [
                (number, m.group(1), m.group(2))
                for m in BOLD_TERM.finditer(line)
                if m.group(1) in VALUED_FLAGS
            ]
    return found


def test_the_scan_recognises_a_space_separated_flag_in_each_surface() -> None:
    """An empty result has to mean compliance rather than a broken pattern."""

    assert [(line, flag) for line, flag, _ in violations(SAMPLE)] == [
        (1, "--at-once"),
        (2, "--ticket"),
        (3, "--commit"),
        (4, "--on"),
        (6, "--message"),
    ]


def test_no_valued_flag_of_the_collections_grammar_is_written_with_a_space() -> None:
    """`--flag=value`, on every surface the collection owns (ADR-0096)."""

    scanned = _scanned()

    # A glob that matched nothing would pass the loop below without reading a
    # single file, which is the one outcome this test exists to catch.
    assert scanned

    for path in scanned:
        for number, flag, value in violations(path.read_text(encoding="utf-8")):
            where = f"{path.relative_to(REPO_ROOT)}:{number}"
            raise AssertionError(
                f"{where}: `{flag} {value}` separates a valued flag from its"
                f" value with a space. A flag of this collection's own grammar"
                f" attaches its value with `=`, as `{flag}=…`, because that is"
                f" the only spelling an optional value has, the only one that"
                f" is unambiguous where a value begins with `-` or is empty,"
                f" and the one that keeps a flag and its value a single token"
                f" ({RECORD}). A `git`, `gh`, `uv`, or `npx` command line keeps"
                f" its own tool's spelling and is not under this rule. See"
                f" {STANDARD}."
            )


def test_the_standard_states_the_attached_form_and_cites_the_record() -> None:
    """The rule is written where a contributor reads it before anything fails."""

    text = (REPO_ROOT / STANDARD).read_text(encoding="utf-8")

    assert "`--flag=value`" in text, (
        f"{STANDARD}: the Skills module states the spelling a valued flag"
        f" takes its value in, because a contributor who has not written"
        f" anything yet cannot be helped by an assertion message ({RECORD})."
    )
    assert RECORD in text, (
        f"{STANDARD}: the rule is cited to {RECORD}, which carries the"
        f" reasoning and the alternatives it was chosen over."
    )
