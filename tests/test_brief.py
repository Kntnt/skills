"""Brief's public invocation and shared template remain usable after installation."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
BRIEF = ROOT / "skills/editorial/brief"
MANAGER = ROOT / "skills/kntnt/scripts/kntnt.py"
TEMPLATE = ROOT / "skills/kntnt/library/references/editorial/writing-brief.md"


@pytest.mark.parametrize("payload", ["", "--output=brief.md notes.md"])
def test_brief_accepts_interview_and_material_through_the_manager(
    tmp_path: Path, payload: str
) -> None:
    """No material starts an interview; material and one destination also parse."""

    result = subprocess.run(
        [sys.executable, str(MANAGER), "invoke", f"--here={BRIEF}"],
        input=payload,
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env={**os.environ, "KNTNT_HOME": str(tmp_path)},
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert str(ROOT / "skills/kntnt/library") in result.stdout


def test_writing_brief_preserves_the_authoritative_question_schema() -> None:
    """The ticket's headings are an interchange format, not a prose snapshot."""

    headings = re.findall(r"^## (\d+\. .+)$", TEMPLATE.read_text(), re.MULTILINE)

    assert headings == [
        "1. What is the assignment?",
        "2. Who is the reader?",
        "3. What makes the text RIV for the reader?",
        "4. Which brand is the sender?",
        "5. What is the text's angle?",
        "6. What should the reader have understood afterwards?",
        "7. What should the reader feel, think or do afterwards?",
        "8. How should the text be structured?",
        "9. What is the hook?",
        "10. What sources and evidence do you have?",
        "11. What should be left out?",
        "12. What is the working title?",
        "13. What frame applies to the text?",
    ]
