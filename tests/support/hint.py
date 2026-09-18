"""Read a Skill's `argument-hint` into the forms it advertises.

The hint is one line, so it may write once what several forms share and group
what they do not: `[--language=<language>] ([--output=<target>] [<text>] |
--in-place <path>)` is two forms that both carry `--language`. A check that
splits the line on ` | ` cannot read that, and neither can one that splits it
on whitespace; this module expands the line into the forms themselves, each
unit still spelled as the hint writes it and still knowing where in the line
it stands — which is what tells one flag shared by two forms from the same
flag written twice.

The notation is the manpage's without its emphasis: square brackets around an
optional unit, parentheses around a required group, `|` between alternatives,
`...` after a repeatable unit, a metavariable in angle brackets, and a literal
bare. A bracket or a group whose alternatives are single atoms —
`[--project|--user]`, `(on|off)`, `[<text>|<path>|<url>]` — is one unit of a
form, as a `## SYNOPSIS` unit is; one whose alternatives are sequences is
opened into the forms it offers.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import product
from pathlib import Path

# The optional Contextual Instruction closing every hint, which belongs to no
# form and is taken off before the forms are read (ADR-0176).
SUFFIX = re.compile(r"\s*\[--\s*<instruction>\]\s*$")

# One alternative of a flag's value: a metavariable, which may hold spaces of
# its own, or a literal. A literal never opens with `-`, which is what keeps
# `[--config=<path>|--no-config]` two flags rather than one flag's two values.
_VALUE = r"(?:<[^>]*>|[^\s\[\]()|<-][^\s\[\]()|]*)"

# A flag, its name in the group `name`, with whatever value it carries: an
# optional value in brackets, or a value whose alternatives — `yes|no`,
# `response|<path>` — belong to the value rather than to the form.
FLAG = re.compile(
    rf"(?P<name>--[a-z][a-z0-9-]*)(?:\[=[^\]]*\]|={_VALUE}(?:\|{_VALUE})*)?"
)

# A metavariable, with the `#` a ticket reference is written behind.
META = re.compile(r"#?<[^>]*>")

# A literal: a command path, or an operand the hint names word for word.
WORD = re.compile(r"[A-Za-z0-9][\w.-]*")

# The markers that give a hint its structure rather than its words.
PUNCTUATION = re.compile(r"\.\.\.|[\[\]()|]")


@dataclass(frozen=True)
class Unit:
    """One unit of an advertised form, as written, and where it stands in the hint."""

    text: str
    start: int


# One advertised form: its units in the order the hint writes them.
type Form = tuple[Unit, ...]


@dataclass(frozen=True)
class _Atom:
    """A flag, a metavariable, or a literal, by its span in the hint."""

    start: int
    end: int


@dataclass(frozen=True)
class _Seq:
    """Units written one after another, all of which a form carries."""

    items: tuple[_Node, ...]


@dataclass(frozen=True)
class _Alt:
    """Sequences separated by `|`, exactly one of which a form carries."""

    branches: tuple[_Seq, ...]


@dataclass(frozen=True)
class _Bracket:
    """An optional `[...]` or a required `(...)`, by its span in the hint."""

    optional: bool
    inner: _Alt
    start: int
    end: int


type _Node = _Atom | _Bracket


def read_hint(directory: Path) -> str:
    """Return one Skill's `argument-hint`, the grammar the harness shows."""

    for line in (directory / "SKILL.md").read_text(encoding="utf-8").splitlines():
        if line.startswith("argument-hint:"):
            return line.partition(":")[2].strip().strip("\"'")
    raise AssertionError(
        f"{directory}: every Skill declares an `argument-hint`, the grammar the"
        f" harness shows before anything is typed (ADR-0176)."
    )


def _tokens(hint: str) -> list[tuple[str, int, int]]:
    """Split *hint* into its punctuation and its atoms, each with its span."""

    tokens: list[tuple[str, int, int]] = []
    index = 0
    while index < len(hint):
        if hint[index].isspace():
            index += 1
            continue
        for kind, pattern in (
            ("mark", PUNCTUATION),
            ("atom", FLAG),
            ("atom", META),
            ("atom", WORD),
        ):
            match = pattern.match(hint, index)
            if match:
                text = match.group(0)
                # A literal written straight against its repeat marker keeps
                # the marker apart from the word.
                if pattern is WORD and text.endswith("..."):
                    text = text[:-3]
                token = text if kind == "mark" else "atom"
                tokens.append((token, index, index + len(text)))
                index += len(text)
                break
        else:
            raise ValueError(f"cannot read the hint at `{hint[index:]}`")
    return tokens


class _Parser:
    """A recursive reader of the hint notation, alternation binding loosest."""

    def __init__(self, hint: str) -> None:
        self.tokens = _tokens(hint)
        self.index = 0

    def _peek(self) -> str | None:
        return self.tokens[self.index][0] if self.index < len(self.tokens) else None

    def alternation(self) -> _Alt:
        """Read sequences for as long as a `|` separates them."""

        branches = [self.sequence()]
        while self._peek() == "|":
            self.index += 1
            branches.append(self.sequence())
        return _Alt(tuple(branches))

    def sequence(self) -> _Seq:
        """Read units up to the `|` or the bracket that ends the sequence."""

        items: list[_Node] = []
        while self._peek() not in (None, "|", "]", ")"):
            items.append(self.item())
        return _Seq(tuple(items))

    def item(self) -> _Node:
        """Read one atom or one bracketed unit, with its repeat marker."""

        kind, start, end = self.tokens[self.index]
        self.index += 1
        node: _Node
        if kind in ("[", "("):
            inner = self.alternation()
            closing = "]" if kind == "[" else ")"
            if self._peek() != closing:
                raise ValueError(f"`{kind}` at {start} is never closed")
            end = self.tokens[self.index][2]
            self.index += 1
            node = _Bracket(kind == "[", inner, start, end)
        elif kind == "atom":
            node = _Atom(start, end)
        else:
            raise ValueError(f"`{kind}` at {start} stands where a unit belongs")

        # A repeat marker belongs to the unit it follows, inside or outside
        # its bracket alike, as the manpage writes both.
        while self._peek() == "...":
            end = self.tokens[self.index][2]
            self.index += 1
            node = (
                _Bracket(node.optional, node.inner, node.start, end)
                if isinstance(node, _Bracket)
                else _Atom(node.start, end)
            )
        return node


def _simple(node: _Node) -> bool:
    """Whether *node* is one unit of a form: an atom, or alternatives of atoms."""

    if isinstance(node, _Atom):
        return True
    return all(
        len(branch.items) == 1 and isinstance(branch.items[0], _Atom)
        for branch in node.inner.branches
    )


def _expand_alt(alt: _Alt, hint: str) -> Iterator[Form]:
    for branch in alt.branches:
        yield from _expand_seq(branch, hint)


def _expand_seq(seq: _Seq, hint: str) -> Iterator[Form]:
    choices = [list(_expand_node(item, hint)) for item in seq.items]
    for picked in product(*choices):
        yield tuple(unit for part in picked for unit in part)


def _expand_node(node: _Node, hint: str) -> Iterator[Form]:
    if _simple(node):
        yield (Unit(hint[node.start : node.end], node.start),)
        return

    # A group of sequences is opened into the forms it offers: none at all
    # where it is optional, and each of its alternatives.
    assert isinstance(node, _Bracket)
    if hint[node.end - 3 : node.end] == "...":
        raise ValueError(f"a repeated group of sequences at {node.start} has no form")
    if node.optional:
        yield ()
    yield from _expand_alt(node.inner, hint)


def hint_forms(hint: str) -> list[Form]:
    """Every form *hint* advertises, in the order it writes them.

    The Contextual Instruction suffix is taken off first; the forms that are
    left are what the hint says a Formal Invocation may be.

    Raises:
        ValueError: the hint is written in a notation this reader does not know.
    """

    body = SUFFIX.sub("", hint)
    parser = _Parser(body)
    alternation = parser.alternation()
    if parser.index != len(parser.tokens):
        stray = parser.tokens[parser.index][1]
        raise ValueError(f"cannot read the hint past `{body[stray:]}`")
    return list(_expand_alt(alternation, body))


def form_text(form: Form) -> str:
    """One advertised form written out as a single hint line."""

    return " ".join(unit.text for unit in form)


def to_synopsis(skill: str, form: Form) -> str:
    """One advertised form in the manpage's markup, for the engine to read.

    A flag keeps its name and whether it takes a value, which is all the
    engine reads of it; the value's own vocabulary is the Skill's (ADR-0181).
    A metavariable becomes italic and a literal bold, as `## SYNOPSIS` writes
    them.
    """

    def flag(match: re.Match[str]) -> str:
        name = match.group("name")
        value = match.group(0)[len(name) :]
        if value.startswith("[="):
            return f"**{name}**[=*VALUE*]"
        if value.startswith("="):
            return f"**{name}**=*VALUE*"
        return f"**{name}**"

    def metavariable(match: re.Match[str]) -> str:
        return f"*{match.group(0).strip('#<>').upper()}*"

    def literal(match: re.Match[str]) -> str:
        return f"**{match.group(0)}**"

    def unit(text: str) -> str:
        rendered: list[str] = []
        index = 0
        while index < len(text):
            for pattern, render in (
                (FLAG, flag),
                (META, metavariable),
                (WORD, literal),
            ):
                match = pattern.match(text, index)
                if match:
                    rendered.append(render(match))
                    index = match.end()
                    break
            else:
                # Punctuation and spacing are the same in both notations.
                rendered.append(text[index])
                index += 1
        return "".join(rendered)

    return " ".join([f"**/{skill}**", *(unit(part.text) for part in form)])
