"""Keep the executable evaluator subject to the Python declaration contract.

Frozen transcripts and runner snapshots are evidence, so this check reads only
the maintained evaluator rather than rewriting or linting historical bytes.
"""

import ast
from pathlib import Path


def test_evaluator_module_declarations_have_explicit_type_annotations() -> None:
    """Evaluator constants expose their types even outside the mypy gate list."""
    evaluator = (
        Path(__file__).resolve().parents[1]
        / "docs/evaluation/editorial-492/harness/run.py"
    )
    module = ast.parse(evaluator.read_text(encoding="utf-8"))

    unannotated = [
        target.id
        for statement in module.body
        if isinstance(statement, ast.Assign)
        for target in statement.targets
        if isinstance(target, ast.Name)
    ]

    assert not unannotated, f"Module declarations lack types: {unannotated}"
