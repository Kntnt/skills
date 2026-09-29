"""Two clean controls meet rules that landed after they were frozen.

`opinion-clean`'s closing sentence treated September as already named, and only
the standfirst named it. `case-study-clean`'s last subheading stated the
reservation Maya Lind's quotation is there to carry. Both rows stay frozen as
conforming, so the texts are what move (issue #431).
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CORPUS = REPO_ROOT / "docs" / "evaluation" / "corpus" / "editorial-quality"
CONTROLS = CORPUS / "controls"
MATRIX = CORPUS / "README.md"
ANATOMY = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts" / "article_anatomy.py"

# The anatomy's ceiling for a subheading, spaces included. The rows' bands are
# what the texts happen to measure, and are restated from the script; this is
# the limit the revised heading has to stay inside.
SUBHEADING_CEILING = 70

# The one line each control may differ in, and the digest of every other line
# joined by a newline. A second edit fails the digest rather than the property
# the line was revised for.
OPINION_LEAD_LINE = 6
OPINION_OTHER_SHA256 = (
    "94a1d829238e88b7c031450ec0e0b5def766a061bf655612946500185ee5574f"
)
CASE_STUDY_LAST_SUBHEADING_LINE = 20
CASE_STUDY_OTHER_SHA256 = (
    "24afcd641482b1ed5c7c2bb9b4048aacf589f53e1d300fa044ddac5c5667fb3e"
)

OPINION_CLOSE = (
    "Ett antagande blir inte ett beslutsunderlag för att kalendern säger september."
)
LEAD_OPENING = (
    "Kommunstyrelsen i Lervik bör skjuta upp bytet till enbart digital"
    " bokning av föreningslokaler"
)
LEAD_REST = (
    " Pröva först båda bokningsvägarna i alla sju lokaler under ett halvår"
    " och mät vad de kräver. Ett permanent beslut behöver bättre underlag"
    " än det som nu ligger på bordet."
)

# What Lind's quotation is there to carry. A subheading that uses one of these
# has said it before she does.
RESERVATION = (
    "förbered",
    "mer tid",
    "vecka",
    "avsätta",
    "gemensam",
    "hjälper",
    "välja",
    "igen",
)

# The headline reference allows a subheading over a quotation to name the
# speaker, the occasion or the subject, and not the point.
NAMED = (
    "lind",
    "arbetsledare",
    "försök",
    "tillbaka",
    "logg",
    "ärende",
    "elm quay",
    "kund",
)

# The counted figures a row states, in the form these two rows use. An en dash
# is the range mark the matrix already uses; a single figure has no high group.
COUNTED = re.compile(
    r"(?P<headline>\d+)-character headline, "
    r"(?P<standfirst>\d+)-word standfirst, "
    r"(?P<low>\d+)(?:[-\u2013](?P<high>\d+))?-character subheadings"
)

REVISION_DATE = "2026-09-29"


def _control(name: str) -> str:
    """Return one control text, including its trailing newline."""

    return (CONTROLS / name).read_text(encoding="utf-8")


def _other_lines_sha256(text: str, skip: int) -> str:
    """Digest every line but *skip*, so a second edit cannot hide in the file."""

    lines = text.splitlines()
    kept = [line for index, line in enumerate(lines) if index != skip]
    return hashlib.sha256("\n".join(kept).encode()).hexdigest()


def _measure(name: str) -> Any:
    """Measure one control and return the script's payload.

    The working directory is the repository root, which nothing in this test
    removes. The script's own path is absolute either way.
    """

    result = subprocess.run(
        ["uv", "run", "--no-cache", "--no-project", str(ANATOMY), str(CONTROLS / name)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (name, result.returncode, result.stderr)
    return json.loads(result.stdout)


def _stated_figures(label: str) -> tuple[int, int, tuple[int, int]]:
    """Return the headline, standfirst and subheading figures *label*'s row states."""

    row = next(
        line
        for line in MATRIX.read_text(encoding="utf-8").splitlines()
        if line.startswith(f"| {label} /")
    )
    match = COUNTED.search(row)
    assert match is not None, row
    low = int(match.group("low"))
    high = match.group("high")
    return (
        int(match.group("headline")),
        int(match.group("standfirst")),
        (low, int(high) if high is not None else low),
    )


def _measured_figures(payload: Any) -> tuple[int, int, tuple[int, int]]:
    """Return the same three figures from the script's payload."""

    parts = payload["parts"]
    lengths = [section["subheading"]["characters"] for section in parts["sections"]]
    return (
        parts["headline"]["characters"],
        parts["standfirst"]["words"],
        (min(lengths), max(lengths)),
    )


def test_opinion_clean_names_september_before_the_close_needs_it() -> None:
    """The closing sentence must not rest on a month only the standfirst names.

    The lead says what happens in September, in the author's register and in
    the fewest words, and every other line stays (issue #431).
    """

    text = _control("opinion-clean.md")
    assert text.endswith("\n")
    lead = text.splitlines()[OPINION_LEAD_LINE]

    # Cover the standfirst. September in the closing sentence then needs a
    # referent the body itself has already given.
    body = "\n".join(line for line in text.splitlines() if not line.startswith("**"))
    assert OPINION_CLOSE in body
    before_close = body.split(OPINION_CLOSE)[0]
    assert "september" in before_close.casefold(), (
        "with the standfirst covered, the closing sentence's September has"
        " no referent in the body"
    )

    # The lead is where the body first needs the month, and the clause names
    # the switch at the standfirst's own certainty rather than sharpening it.
    assert lead.startswith(LEAD_OPENING)
    assert lead.endswith(LEAD_REST)
    clause = lead[len(LEAD_OPENING) : -len(LEAD_REST)]
    folded = clause.casefold()
    assert "september" in folded, clause
    assert "byte" in folded, clause
    assert "kan" in folded, clause
    assert len(clause.split()) <= 8, clause

    # One line moved. A second edit is a control the row did not revise.
    assert _other_lines_sha256(text, OPINION_LEAD_LINE) == OPINION_OTHER_SHA256, (
        "a line other than the lead moved in opinion-clean"
    )


def test_case_study_clean_last_subheading_leaves_the_quotation() -> None:
    """A reader who has just read the last subheading meets Lind's quotation as new.

    The heading names the speaker, the occasion or the subject, stays inside
    the anatomy's ceiling, and every other line stays (issue #431).
    """

    text = _control("case-study-clean.md")
    assert text.endswith("\n")
    heading = text.splitlines()[CASE_STUDY_LAST_SUBHEADING_LINE].removeprefix("## ")
    folded = heading.casefold()

    # The reservation, and the appraisal around it, stay in the quotation.
    spent = [token for token in RESERVATION if token in folded]
    assert spent == [], f"{heading!r} states the quotation's point: {spent}"

    # Speaker, occasion or subject, and not a heading past the ceiling.
    assert any(token in folded for token in NAMED), heading
    assert len(heading) <= SUBHEADING_CEILING, (heading, len(heading))

    # One line moved.
    assert (
        _other_lines_sha256(text, CASE_STUDY_LAST_SUBHEADING_LINE)
        == CASE_STUDY_OTHER_SHA256
    ), "a line other than the last subheading moved in case-study-clean"


def test_the_matrix_records_the_revision_and_that_earlier_records_stand() -> None:
    """The opening says what was revised, on which date, under which two rules.

    A record made against an earlier corpus commit was judged then, and the
    note says so rather than reopening it (issue #431).
    """

    opening, separator, _rest = MATRIX.read_text(encoding="utf-8").partition(
        "## Material and staging"
    )
    assert separator, "the matrix no longer opens on its revision notes"

    note = next(
        (
            paragraph
            for paragraph in opening.split("\n\n")
            if REVISION_DATE in paragraph and "opinion-clean" in paragraph
        ),
        None,
    )
    assert note is not None, (
        "the matrix opening has no dated paragraph revising opinion-clean"
    )
    assert "case-study-clean" in note
    assert "article-anatomy.md" in note
    assert "headlines.md" in note
    assert "without the standfirst" in note
    assert "subheading over a quotation" in note
    assert "stands as judged" in note


def test_the_two_rows_restate_counted_figures_from_the_script() -> None:
    """Every counted figure the two rows state is the script's figure.

    The frozen expectation stays, except those figures, which are restated
    from `article_anatomy.py`. Exit 0 is the rows' claim that each text conforms.
    """

    for label, name in (
        ("opinion-clean", "opinion-clean.md"),
        ("case-study-clean", "case-study-clean.md"),
    ):
        assert _stated_figures(label) == _measured_figures(_measure(name)), label
