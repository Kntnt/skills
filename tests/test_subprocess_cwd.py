"""Where a process this collection starts begins, and where it must not."""

from __future__ import annotations

import ast
from pathlib import Path

from support.contract import PYTHON_STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"

# Every `subprocess` entry point that starts a process, each taking the same
# `cwd`. The rule reaches all of them rather than the one call this collection
# happens to write most often.
LAUNCHERS = frozenset({"run", "Popen", "call", "check_call", "check_output"})

# What a comment says an inherited working directory by. A call that names no
# `cwd` has to say why in the paragraph above it, and these are what make that
# statement findable rather than a matter of a reader's judgement.
DELIBERATE = ("working directory", "cwd")


def _shipped_engines() -> list[Path]:
    """Every Python file the Collection ships, repository order.

    The suite is deliberately outside it: the Collection is what is shipped,
    and a test fixture's own subprocess is state the test itself owns.
    """

    engines = sorted(SKILLS.rglob("*.py"))
    assert engines
    return engines


def _launches(tree: ast.AST) -> list[ast.Call]:
    """Return every call in *tree* that starts a process through `subprocess`."""

    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr in LAUNCHERS
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "subprocess"
    ]


def _comment_above(lines: list[str], line: int) -> str:
    """Return the contiguous comment block immediately above *line*, folded.

    The collection writes a paragraph's purpose above the paragraph, so the
    statement's own comment is where a deliberate inheritance is said.
    """

    collected: list[str] = []
    index = line - 2
    while index >= 0 and lines[index].lstrip().startswith("#"):
        collected.append(lines[index].strip().lstrip("#").strip())
        index -= 1
    return " ".join(reversed(collected)).lower()


def test_every_shipped_subprocess_call_settles_its_working_directory() -> None:
    """A launcher cannot start from a directory that no longer exists.

    A process outlives its own working directory: the directory it was started
    in can be replaced or removed while it runs, and this collection's own
    Update does exactly that to the Manager's installed tree. A call that
    inherits whatever directory the invoking agent stood in therefore fails
    for a reason that has nothing to do with what it was asked to run
    (issue #257), so every shipped call either names its directory or says in
    the paragraph above it why inheriting one is right here.
    """

    for path in _shipped_engines():
        source = path.read_text(encoding="utf-8")
        lines = source.splitlines()
        for call in _launches(ast.parse(source)):
            if any(keyword.arg == "cwd" for keyword in call.keywords):
                continue
            assert any(
                word in _comment_above(lines, call.lineno) for word in DELIBERATE
            ), (
                f"{path.relative_to(REPO_ROOT)}:{call.lineno}: this starts a"
                f" process without naming the directory it runs in, so it"
                f" inherits whichever one the caller stood in — a directory a"
                f" run of this collection can replace or remove while the"
                f" process is still going (issue #257). Pass `cwd`, or say in"
                f" the comment above the call why inheriting one is right"
                f" here. See {PYTHON_STANDARD}."
            )


def test_no_shipped_engine_imports_a_launcher_out_of_subprocess() -> None:
    """The rule above reads `subprocess.<launcher>`, so that is how they are written.

    A launcher bound to a bare name would be a process this collection starts
    that no scan of it can see, which is the one way the rule could be true of
    every call it finds and false of the Collection.
    """

    for path in _shipped_engines():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module == "subprocess":
                imported = ", ".join(alias.name for alias in node.names)
                raise AssertionError(
                    f"{path.relative_to(REPO_ROOT)}:{node.lineno}: import the"
                    f" `subprocess` module rather than {imported} out of it, so"
                    f" that every process this collection starts is written the"
                    f" one way its working directory is read off."
                    f" See {PYTHON_STANDARD}."
                )
