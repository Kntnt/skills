"""The one spelling a flag of this collection's own grammar takes its value in."""

from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"
DOCS = REPO_ROOT / "docs"

# The record settling the spelling, cited by every failure below and by the
# coding standard's own statement of the rule.
RECORD = "ADR-0096"

# An `argparse` action that consumes no value. Everything else — the default
# `store`, `append`, `extend`, a custom action class — takes one.
VALUELESS_ACTIONS = frozenset(
    {"store_true", "store_false", "store_const", "count", "help", "version"}
)

# The helper the one engine that reads its options by hand calls to take a
# flag's value out of its arguments (ADR-0096): `observations.py`, for
# `observe --artifact` and `record --data`. A call to it is that engine's
# declaration that the flag it names carries a value.
HAND_PARSED_OPTION = "_option"

# A manpage option term declaring a value attached to its flag, in each
# spelling a term is written in: the bold run closing after the `=`, as
# `**--data=**_PATH_`; the `=` outside the bold, as `**--language**=*LANGUAGE*`;
# the bracketed optional value, as `**--in-place**[=**on**|**off**]`; and the
# enumerated one, as `**--action=save**`.
OPTION_TERM = re.compile(r"(--[a-z][a-z0-9-]*)(?:\*\*)?\[?=")


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

# A flag whose value is optional and that an operand may follow, with the whole
# of the vocabulary it accepts. Written bare it is compliant, and the operands
# now come after every flag (ADR-0097), so the token behind it is an operand
# rather than a value: `/proofread --in-place report.md` is the ordinary
# invocation. Only a token from the flag's own vocabulary is read as a
# space-separated value, which still refuses `--in-place on`. This decides
# nothing about what is valued — the derivation below does that, and a flag
# absent from here is valued whenever it is declared so — it only tells an
# operand behind a bare flag from a value, which no declaration states.
OPTIONAL_VALUE = {"--in-place": frozenset({"on", "off", "yes", "no", "true", "false"})}


def options_declaring_a_value(page: str) -> set[str]:
    """Return every flag one manpage's `## OPTIONS` section gives a value.

    A page without that section documents no option and declares nothing. Both
    spellings are read, the attached one and the space-separated one, because a
    flag written with a space on every surface it appears on is precisely the
    violation this file exists to catch — a derivation blind to it would let
    that flag out of the set for the same reason nobody noticed it (ADR-0105).
    """

    if "\n## OPTIONS\n" not in page:
        return set()

    declared: set[str] = set()
    section = page.partition("\n## OPTIONS\n")[2].partition("\n## ")[0]
    for line in section.splitlines():
        term = line.strip()
        if not term.startswith("**-"):
            continue
        declared |= {match.group(1) for match in OPTION_TERM.finditer(term)}
        declared |= {match.group(1) for match in BOLD_TERM.finditer(term)}
    return declared


def engine_flags_taking_a_value(source: str) -> set[str]:
    """Return every long flag one engine's own parser declares as valued.

    The source is read as a syntax tree rather than executed: what is wanted is
    the declaration, and a parser is built inside the function that immediately
    parses with it, so there is nothing to introspect without running the
    engine's command line. Both seams the collection has are read — the
    `argparse` declarations, and the hand-rolled one ADR-0096 names.
    """

    declared: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, ast.Call):
            continue
        named = {
            argument.value
            for argument in node.args
            if isinstance(argument, ast.Constant)
            and isinstance(argument.value, str)
            and argument.value.startswith("--")
        }
        if not named:
            continue

        # The hand-rolled seam reads exactly one flag's value per call, so the
        # call itself is the declaration and carries no options to read.
        if isinstance(node.func, ast.Name) and node.func.id == HAND_PARSED_OPTION:
            declared |= named
            continue
        if not (
            isinstance(node.func, ast.Attribute) and node.func.attr == "add_argument"
        ):
            continue

        # An action consuming nothing, and the `nargs=0` a custom action may
        # declare instead, are the two ways a flag says it takes no value.
        valueless = any(
            (
                keyword.arg == "action"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value in VALUELESS_ACTIONS
            )
            or (
                keyword.arg == "nargs"
                and isinstance(keyword.value, ast.Constant)
                and keyword.value.value == 0
            )
            for keyword in node.keywords
        )
        if not valueless:
            declared |= named
    return declared


def derived_valued_flags(
    pages: Iterable[str], engines: Iterable[str]
) -> frozenset[str]:
    """Return the valued set the given manpages and engines declare between them.

    Every long flag of this collection's own grammar that carries a value —
    whether it is written by a user at a Skill's invocation surface or by a
    Skill body constructing a call to one of the collection's Python engines.
    A flag taking no value is absent, because nothing about it is under this
    rule, and so is every flag belonging to `git`, `gh`, `uv`, or `npx`, whose
    grammar is not this collection's to normalise (ADR-0096).

    The two sources between them are complete. The suite already holds a
    Skill's `argument-hint`, its `## SYNOPSIS`, and its `## OPTIONS` to one
    identical set of flags, so the option terms name every flag any Skill
    surface offers; the engines' own declarations carry the rest, the flags
    only a Skill body ever writes (ADR-0105).
    """

    documented = set[str]().union(*(options_declaring_a_value(page) for page in pages))
    declared = set[str]().union(
        *(engine_flags_taking_a_value(engine) for engine in engines)
    )
    return frozenset(documented | declared)


def _shipped_pages() -> list[Path]:
    """Every Markdown file a Skill ships, repository order."""

    return sorted(SKILLS.rglob("*.md"))


def _shipped_engines() -> list[Path]:
    """Every Python engine a Skill ships, repository order."""

    return sorted(SKILLS.rglob("*.py"))


# The valued set, derived at test time from the declarations the collection
# already holds to completeness rather than enumerated beside them (ADR-0105).
VALUED_FLAGS = derived_valued_flags(
    [path.read_text(encoding="utf-8") for path in _shipped_pages()],
    [path.read_text(encoding="utf-8") for path in _shipped_engines()],
)


# One line per surface the scan reads, each carrying a flag it has to catch and
# a flag it must leave alone: the frontmatter hint, a body's engine invocation,
# a manpage term, a manpage example, a fenced block, a bare mention in prose, an
# already-attached value, and the optional value written bare. The last line is
# the case only a derived registry reaches, its flag being declared nowhere the
# collection ships (ADR-0105).
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
**/proofread --in-place report.md**
**/proofread --in-place on report.md**
Run `uv run engine.py emit --unshipped value` and read what it says.
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


def _in_command_line(fragment: str, valued: frozenset[str]) -> list[tuple[str, str]]:
    """Return each valued flag in *fragment* that is followed by a space value."""

    found: list[tuple[str, str]] = []
    for match in FLAG.finditer(fragment):
        name = match.group(1)
        if name not in valued:
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

        # A flag whose value is optional carries an operand behind it far more
        # often than a value, so only its own vocabulary counts as one.
        vocabulary = OPTIONAL_VALUE.get(name)
        if vocabulary is not None and token.strip("`\"'.,").lower() not in vocabulary:
            continue
        found.append((name, token))
    return found


def violations(text: str, valued: frozenset[str]) -> list[tuple[int, str, str]]:
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
                (number, flag, value)
                for flag, value in _in_command_line(fragment, valued)
            ]

        # The manpage form is markup rather than a code span, so it is read on
        # its own terms.
        if not fenced:
            found += [
                (number, m.group(1), m.group(2))
                for m in BOLD_TERM.finditer(line)
                if m.group(1) in valued
            ]
    return found


def test_the_scan_recognises_a_space_separated_flag_in_each_surface() -> None:
    """An empty result has to mean compliance rather than a broken pattern.

    The sample is read against declarations of its own rather than against the
    shipped tree's, so what it proves is the whole path: a declaration is read,
    the set is derived from it, and the patterns find the flag on every surface
    it can be written on. The last line is the case a hand-written registry
    could not reach — its flag is declared nowhere the collection ships, so
    only a set derived from the sample's own declarations carries it
    (ADR-0105).
    """

    valued = derived_valued_flags([SAMPLE_PAGE], [SAMPLE_ENGINE])
    assert "--unshipped" not in VALUED_FLAGS

    assert [(line, flag) for line, flag, _ in violations(SAMPLE, valued)] == [
        (1, "--at-once"),
        (2, "--ticket"),
        (3, "--commit"),
        (4, "--on"),
        (6, "--message"),
        (12, "--in-place"),
        (13, "--unshipped"),
    ]


def test_no_valued_flag_of_the_collections_grammar_is_written_with_a_space() -> None:
    """`--flag=value`, on every surface the collection owns (ADR-0096)."""

    scanned = _scanned()

    # A glob that matched nothing would pass the loop below without reading a
    # single file, which is the one outcome this test exists to catch.
    assert scanned

    for path in scanned:
        for number, flag, value in violations(
            path.read_text(encoding="utf-8"), VALUED_FLAGS
        ):
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


# The declarations the sample above is read against: one manpage's option
# terms and one engine's parser, between them declaring every flag the sample
# names. `--unshipped` is declared by neither shipped file, so a hand-written
# registry could not have carried it and only the derivation reaches it
# (ADR-0105).
SAMPLE_PAGE = """# example(1)

## OPTIONS

**--at-once=**_COUNT_

**--commit=**_COMMIT_

**--on=**_SKILL_

**--off=**_SKILL_

**--in-place**[=**on**|**off**]

**--project**, **--project=on**

**--unshipped**=*ANYTHING*

**--yes**

## FILES
"""

SAMPLE_ENGINE = '''"""An engine declaring the flags no manpage documents."""

parser.add_argument("--ticket", required=True, type=int)
parser.add_argument("--message", required=True)
parser.add_argument("--dry-run", action="store_true")
'''


def test_the_valued_set_is_derived_from_the_collections_own_declarations() -> None:
    """The registry answers for the shipped tree rather than for a list's date."""

    pages = _shipped_pages()
    engines = _shipped_engines()

    # A glob that matched nothing would derive an empty set, which is the one
    # outcome that makes every assertion below pass while judging nothing.
    assert pages and engines

    documented = set[str]().union(
        *(options_declaring_a_value(path.read_text(encoding="utf-8")) for path in pages)
    )
    declared = set[str]().union(
        *(
            engine_flags_taking_a_value(path.read_text(encoding="utf-8"))
            for path in engines
        )
    )

    assert documented and declared
    assert VALUED_FLAGS == documented | declared

    # Each source carries flags the other does not, which is why the set is the
    # union of both rather than either one alone.
    assert documented - declared
    assert declared - documented

    # A flag declared to take no value is under no part of this rule.
    assert VALUED_FLAGS.isdisjoint(
        {
            "--as-is",
            "--dry-run",
            "--force",
            "--no-build",
            "--session",
            "--status",
            "--user",
            "--write",
            "--yes",
        }
    )


def test_a_declaration_added_enters_the_derived_set_and_one_removed_leaves_it() -> None:
    """A new Skill's valued flag is enforced with no edit to this file."""

    page = "# example(1)\n\n## OPTIONS\n\n**--novel=**_VALUE_\n\n**--switch**\n\n## FILES\n"
    engine = (
        'parser.add_argument("--engine-only", required=True)\n'
        'parser.add_argument("--switch", action="store_true")\n'
    )

    derived = derived_valued_flags([page], [engine])
    assert derived == {"--novel", "--engine-only"}

    # And the flag is enforced by the same scan, with nothing here naming it.
    assert [flag for _, flag, _ in violations("`run --novel value`", derived)] == [
        "--novel"
    ]

    # A declaration removed leaves the set: the derivation reads what is there
    # now rather than what was there when somebody last edited a list.
    assert derived_valued_flags([], [engine]) == {"--engine-only"}
    assert derived_valued_flags([page], []) == {"--novel"}
    assert derived_valued_flags([], []) == frozenset[str]()
