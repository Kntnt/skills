"""The command line the Library's hand-rolling engines parse, and what parses it."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts"

# The one implementation of this collection's argument grammar, which the two
# engines that read their own command lines reach from beside themselves.
GRAMMAR = "argument_grammar.py"


def _load(name: str, filename: str) -> Any:
    """Load one Library module from its shipped path, the way its callers do.

    Nothing here amends `sys.path` and nothing imports a Library module by bare
    name: a directory that is not this suite's to own is not made importable
    just because a test wants a module out of it (ADR-0149).
    """

    spec = importlib.util.spec_from_file_location(name, LIBRARY / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _declared(module: Any, name: str) -> Any:
    """Resolve one module-level annotation, deferred to a string or not."""

    annotation = module.__annotations__[name]
    if isinstance(annotation, str):
        return eval(annotation, vars(module))
    return annotation


def test_a_flag_declared_valueless_leaves_the_operand_behind_it_alone() -> None:
    """The one thing a hand-rolled parser cannot know by looking at a token.

    A flag that carries no value takes nothing from behind it, so the operand
    written there survives the normalisation. Which flags those are is not a
    property of the grammar but of the engine, so the engine names them and the
    grammar is told; the fork this replaced knew one engine's `--yes` as a
    literal and swallowed the operand behind every valueless flag the other
    engine could ever grow (issue #220).
    """

    grammar = _load("kntnt_argument_grammar", GRAMMAR)

    assert grammar.split(["--yes", "python-refactor"], {"--yes"}) == (
        ["python-refactor"],
        ["--yes"],
    )

    # An engine that declares none is parsed as a permissive command line
    # always was: the token behind a separated flag is that flag's value.
    assert grammar.split(["--data", "/tmp/store", "python-refactor"], ()) == (
        ["python-refactor"],
        ["--data", "/tmp/store"],
    )

    # An attached value is one token whatever the flag is, and the operands
    # come back in the order they were written, from either region of the line.
    assert grammar.split(["python-refactor", "--data=/tmp/store"], {"--yes"}) == (
        ["python-refactor"],
        ["--data=/tmp/store"],
    )


def test_the_option_reader_takes_a_value_in_either_spelling() -> None:
    """The engines stay permissive about the spelling they accept (ADR-0176)."""

    grammar = _load("kntnt_argument_grammar", GRAMMAR)

    assert grammar.option(["--data=/tmp/store"], "--data") == "/tmp/store"
    assert grammar.option(["--data", "/tmp/store"], "--data") == "/tmp/store"

    # Anything that is not this one flag and its value is not this flag's
    # value, which is how an engine tells an unsupported option from its own.
    assert grammar.option([], "--data") is None
    assert grammar.option(["--other=1"], "--data") is None
    assert grammar.option(["--data=/tmp/store", "--other"], "--data") is None


def test_no_library_engine_carries_its_own_copy_of_the_shared_grammar() -> None:
    """The normalising loop is written once and reached by path (ADR-0176)."""

    engines = sorted(LIBRARY.glob("*.py"))

    # A glob that matched nothing would leave the check below judging nothing.
    assert engines

    carrying = [
        path.name
        for path in engines
        if path.name != GRAMMAR
        and 'startswith("--")' in path.read_text(encoding="utf-8")
    ]
    assert carrying == [], (
        f"{carrying}: an engine that separates operands from options by hand"
        f" carries a second answer to how this collection's command lines are"
        f" read, and the two drift apart a token at a time. See {GRAMMAR}."
    )
