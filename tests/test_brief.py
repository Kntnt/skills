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
    """The template's title and headings are an interchange format (issue #471).

    Redline reports a brief by these headings and a brief written by `/brief`
    carries them, so they are pinned exactly as the ticket fixed them rather
    than left to each translation of the template.
    """

    text = TEMPLATE.read_text()
    title = re.findall(r"^# (.+)$", text, re.MULTILINE)
    headings = re.findall(r"^## (\d+\. .+)$", text, re.MULTILINE)

    assert title == ["Questions to answer before you write"]
    assert headings == [
        "1. What is the assignment?",
        "2. Which brand is the sender?",
        "3. What does the sender want to convey with this text?",
        "4. Who is the reader?",
        "5. What is the text's angle?",
        "6. What is the hook?",
        "7. How should the text be structured?",
        "8. What should be left out?",
        "9. What should the reader have understood afterwards?",
        "10. What should the reader feel, think or do afterwards?",
        "11. What makes the text RIV for the reader, and does the brief hold together?",
        "12. What sources do you know of, and what do you need to find out?",
    ]


def _question(number: int) -> str:
    """The guidance under one numbered question, with its lines joined."""

    sections = re.split(r"^## ", TEMPLATE.read_text(), flags=re.MULTILINE)
    for section in sections:
        if section.startswith(f"{number}. "):
            return " ".join(section.split())
    return ""


# The one-sentence form of each arc, as the template states it, and the work
# each form was taken from. The template names its sources and carries no URL,
# as no editorial reference does (issue #471).
SENTENCE_FORMS = (
    (
        "[the situation] and if [...] then [...], but [the problem] because"
        " [...], therefore [...] by [...]"
    ),
    (
        "[the question or starting point], and [what the analysis shows],"
        " which means that [the conclusion]"
    ),
)
FORM_SOURCES = ("Lincoln But Trump", "Elements of the Essay", "Utredande text")


def test_the_structure_question_states_each_arcs_sentence_and_its_source() -> None:
    """Question 7 asks for the whole text in one sentence before the sketch.

    The template once linked instructions for people that no Skill can reach,
    so the form the sentence takes is written where the Skill reads it.
    """

    structure = _question(7)
    text = TEMPLATE.read_text()

    for form in SENTENCE_FORMS:
        assert form in structure, f"{TEMPLATE}: question 7 lacks the form {form!r}."
    for source in FORM_SOURCES:
        assert source in structure, f"{TEMPLATE}: {source!r} is not named."
    assert "http" not in text, f"{TEMPLATE}: an editorial reference carries no URL."


def test_the_senders_message_stays_apart_from_the_texts_conclusion() -> None:
    """The message may stay unsaid; the conclusion carries it (issue #471).

    A brief that made them one thing got either a conclusion stating the
    sender's message outright or a message the structure never reached.
    """

    message = _question(3)
    conclusion = _question(9)
    check = _question(11)

    assert "need not appear in the text" in message
    assert "carries the message" in conclusion
    assert "does it carry the message" in check


def test_the_template_sets_no_quality_gate() -> None:
    """The template's own guidance replaces per-question criteria (issue #471)."""

    text = TEMPLATE.read_text()

    assert "**Quality:**" not in text
    assert "quality criteri" not in text.lower()
    assert "[WEAK" not in text


# Every file that describes the brief's questions or the Skill. None of them
# says how many questions there are, so the next change to the template
# changes no count anywhere else (issue #471).
COUNT_FREE = (
    BRIEF / "SKILL.md",
    BRIEF / "help.md",
    BRIEF / "agents/openai.yaml",
    ROOT / "README.md",
    ROOT / "CONTEXT.md",
    ROOT / "docs/rules/skills.md",
    ROOT / "skills/kntnt/library/references/editorial/README.md",
    ROOT / "skills/editorial/redline/references/brief-review.md",
    ROOT / "skills/editorial/redline/help.md",
)
QUESTION_COUNT = re.compile(
    r"\b(?:\d+|twelve|thirteen)[- ](?:numbered[- ])?(?:questions?|headings?|points?)\b"
    r"|\ball \d+\b",
    re.IGNORECASE,
)


@pytest.mark.parametrize(
    "path", COUNT_FREE, ids=lambda path: str(path.relative_to(ROOT))
)
def test_nothing_describing_the_brief_states_a_question_count(path: Path) -> None:
    stated = QUESTION_COUNT.findall(path.read_text())

    assert stated == [], f"{path}: states a question count {stated} (issue #471)."


def test_brief_marks_no_answer_weak_and_withholds_no_readiness_for_research() -> None:
    """A brief is a direction, not a finished dossier (issue #471)."""

    for path in (BRIEF / "SKILL.md", BRIEF / "help.md"):
        text = path.read_text()
        # A brief written to the older template may still carry the marker,
        # and Review reads it as the answer it marks; nothing writes one.
        writes = [
            sentence
            for sentence in re.split(r"(?<=\.)\s+", text)
            if "[WEAK" in sentence and "is read as the answer it marks" not in sentence
        ]
        assert writes == [], f"{path}: still marks answers weak: {writes}"
        assert "two follow-up" not in text, f"{path}: still allows two follow-ups."
        assert "never reported ready to write" not in text, (
            f"{path}: still withholds readiness from a brief with open research."
        )


def test_nothing_shipped_links_the_templates_google_documents() -> None:
    """The template is self-contained wherever the Skill runs (issue #471)."""

    linked = [
        str(path.relative_to(ROOT))
        for path in (ROOT / "skills").rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".yaml", ".json", ".py"}
        and "docs.google.com" in path.read_text(errors="replace")
    ]

    assert linked == []
