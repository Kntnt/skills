"""CLI behaviour of the Collection Library's article-anatomy measuring script."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library"
ANATOMY = LIBRARY / "scripts" / "article_anatomy.py"
CONTROLS = (
    REPO_ROOT / "docs" / "evaluation" / "corpus" / "editorial-quality" / "controls"
)

# The verdict the exit status carries: measured and conforming, measured and
# failing a requirement, or not measured at all.
CONFORMS = 0
FAILS = 1
UNMEASURED = 2

# The names the answer reports a figure or a stray block under, and the codes a
# refusal carries. They are the script's published vocabulary, so the
# expectations below are written in it rather than in string literals of their
# own.
HEADLINE_PART = "headline"
STANDFIRST_PART = "standfirst"
BYLINE_PART = "byline"
LEAD_PART = "lead"
SECTIONS_PART = "sections"
FRONT_PART = "front"
BEFORE_HEADLINE_PART = "before the headline"
FIRST_SECTION = "section 1"
MARKDOWN = "markdown"
HTML = "html"
NO_STRUCTURE = "no-structure"
EMPTY_TEXT = "empty-text"
UNREADABLE_INPUT = "unreadable-input"

# The anatomy's requirement that the ending stands apart from the argument,
# which the script quotes as the rule of a text holding one section (#402).
ENDING_IS_A_SECTION = (
    "The ending is a section of its own, opened by its own subheading, after at"
    " least one other section."
)
ANATOMY_REFERENCE = LIBRARY / "references" / "editorial" / "article-anatomy.md"

# The four positive controls of the genres the anatomy binds. The corpus says
# each of them conforms to the skeleton, so each of them is a text this script
# has to agree with.
CLEAN_CONTROLS = (
    "article-clean.md",
    "case-study-clean.md",
    "column-clean.md",
    "opinion-clean.md",
)


# --- Fixtures -------------------------------------------------------------

# One conforming Swedish article, kept to the shape the corpus's own positive
# control has: a 48-character headline, a standfirst set in bold, the Swedish
# `Text:` byline, a one-paragraph lead, and two sections.
HEADLINE = "Mätförsöket i Björkskolan visar när, inte varför"
STANDFIRST = (
    "**Under 14 av 120 lektionspass registrerade givarna temperaturer under"
    " arbetsgränsen. Fyra veckors mätningar pekar ut tillfällen att undersöka"
    " närmare, men förklarar inte varför luften var kall.**"
)
BYLINE = "Text: Hedda Lund"
LEAD = (
    "En temperaturgivare mäter luften där den sitter. Det gör placeringen viktig"
    " när fastighetskontoret ska tolka fyra veckors mätningar. Genomgången nedan"
    " visar vad värdena räcker till."
)
BODY = (
    "## En gräns för det lokala försöket\n"
    "\n"
    "Kontoret valde 20 grader Celsius som arbetsgräns. Rapporten räknar 14"
    " lektionspass av 120 med minst en mätning under den gränsen.\n"
    "\n"
    "Givarna mätte varken luftdrag eller elevernas upplevelse.\n"
    "\n"
    "## Nästa försök behöver mer än givare\n"
    "\n"
    "Lägg tiderna för när rummen används bredvid mätvärdena innan nästa givare"
    " sätts upp."
)
# The second of `BODY`'s sections, for a fixture whose own section is what it is
# about: the ending is a section of its own after at least one other, so a text
# of one section fails a requirement the fixture is not testing.
ENDING_SUBHEADING = "Nästa försök behöver mer än givare"
ENDING_PARAGRAPH = (
    "Lägg tiderna för när rummen används bredvid mätvärdena innan nästa givare"
    " sätts upp."
)
ENDING = f"## {ENDING_SUBHEADING}\n\n{ENDING_PARAGRAPH}"
FRONTMATTER = "---\nkntnt:\n  genre: article\n  technique: none\n  language: sv\n---"

# What a headline and a subheading of an exact length are cut from. Both carry
# `å`, `ä`, `ö` and an en dash inside the first seventy characters, so a script
# counting UTF-8 bytes or decomposed code points cannot agree with one counting
# what the reader sees.
LONG_HEADLINE = "Mätförsöket i Björkskolan visar när, inte varför och inte hur länge luften var kall"
LONG_SUBHEADING = (
    "Mätförsöket i Björkskolan – när, inte varför, och vad som ändå återstår att göra"
)


def _article(
    *,
    frontmatter: str | None = None,
    headline: str | None = HEADLINE,
    standfirst: str | None = STANDFIRST,
    byline: str | None = BYLINE,
    lead: str | None = LEAD,
    body: str | None = BODY,
) -> str:
    """Assemble one Markdown article out of the parts named, omitting the rest."""

    blocks = [
        frontmatter,
        f"# {headline}" if headline is not None else None,
        standfirst,
        byline,
        lead,
        body,
    ]
    return "\n\n".join(block for block in blocks if block is not None) + "\n"


def _cut(source: str, characters: int) -> str:
    """Return the first *characters* code points of *source*.

    A heading measured at its exact limit is what the fixture is for, so the
    cut falls where the limit does rather than on a word boundary.
    """

    return source[:characters]


def _words(count: int) -> str:
    """Return a paragraph of exactly *count* words, ending in a full stop."""

    return " ".join(["mätvärde"] * (count - 1) + ["kvarstår."])


# --- Driving the script ---------------------------------------------------


def _run(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess[str]:
    """Drive the shipped script from its installed location."""

    return subprocess.run(
        ["uv", "run", "--no-cache", "--no-project", str(ANATOMY), *args],
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def _json(result: subprocess.CompletedProcess[str]) -> Any:
    """Parse the script's stdout, reporting stderr when it is not JSON."""

    assert result.stdout, result.stderr
    return json.loads(result.stdout)


def _measure(tmp_path: Path, text: str, *args: str) -> tuple[int, Any]:
    """Measure *text* from a file, returning the exit status and the payload."""

    path = tmp_path / "text.md"
    path.write_text(text, encoding="utf-8")
    result = _run(*args, str(path))
    return result.returncode, _json(result)


def _parts(payload: Any) -> set[str]:
    """Return the parts every reported failure names."""

    return {failure["part"] for failure in payload["failures"]}


def _rules(payload: Any, key: str = "failures") -> str:
    """Return every rule reported under *key*, folded into one string."""

    return " ".join(entry["rule"] for entry in payload[key])


def _measured(payload: Any, key: str = "failures") -> str:
    """Return every figure reported under *key*, folded into one string."""

    return " ".join(entry["measured"] for entry in payload[key])


def _figures(payload: Any) -> Any:
    """Return everything a text measures, whichever form it was written in.

    The reported blocks that are neither heading nor paragraph are left out:
    WordPress block comments are exactly such blocks, and the point of the
    comparison is that they change no figure.
    """

    parts = {name: value for name, value in payload["parts"].items() if name != "other"}
    return {
        "conforms": payload["conforms"],
        "failures": payload["failures"],
        "norms": payload["norms"],
        "typical": payload["typical"],
        "parts": parts,
        "heading_pairs": payload["heading_pairs"],
    }


# --- A conforming text ----------------------------------------------------


def test_a_conforming_article_measures_clean(tmp_path: Path) -> None:
    """Every counted requirement holds, so the verdict is the exit status.

    The fixture carries a `kntnt` frontmatter map and a standfirst set in
    bold: frontmatter is skipped rather than measured, and emphasis is markup
    rather than text, so neither reaches a count.
    """

    status, payload = _measure(tmp_path, _article(frontmatter=FRONTMATTER))

    assert status == CONFORMS, payload
    assert payload["ok"] is True
    assert payload["conforms"] is True
    assert payload["failures"] == []
    assert payload["format"] == MARKDOWN


def test_a_conforming_article_reports_what_it_took_as_which_part(
    tmp_path: Path,
) -> None:
    """The Skill can overrule a wrong guess only where the guess is stated."""

    _, payload = _measure(tmp_path, _article(frontmatter=FRONTMATTER))

    parts = payload["parts"]
    assert parts["headline"]["text"] == HEADLINE
    assert parts["headline"]["characters"] == 48
    assert parts["headline"]["words"] == 7
    assert parts["standfirst"]["words"] == 26
    assert parts["byline"]["text"] == BYLINE
    assert parts["lead"]["text"].startswith("En temperaturgivare mäter luften")
    assert [section["subheading"]["text"] for section in parts["sections"]] == [
        "En gräns för det lokala försöket",
        "Nästa försök behöver mer än givare",
    ]
    assert [len(section["paragraphs"]) for section in parts["sections"]] == [2, 1]


def test_a_conforming_article_reports_the_text_wide_figures(tmp_path: Path) -> None:
    """*Most* is read across the whole text, so the whole text is what is counted."""

    _, payload = _measure(tmp_path, _article(frontmatter=FRONTMATTER))

    assert payload["typical"] == {
        "paragraphs": 5,
        "paragraphs_of_two_or_three_sentences": 3,
        "sections": 2,
        "sections_of_two_or_three_paragraphs": 1,
    }


# --- Heading pairs -------------------------------------------------------


def test_heading_pairs_preserve_full_text_and_report_unjudged_overlap(
    tmp_path: Path,
) -> None:
    """An echo is evidence for an editor, never a counted failure."""

    headline = "Jag vet inte om rutan skulle hjälpa"
    standfirst = (
        "Jag vet inte om ytterligare en ruta gör möten bättre. Ändå vill jag prova."
    )
    text = _article(
        headline=headline,
        standfirst=standfirst,
        body=f"## {headline}\n\n{standfirst}\n\n{ENDING}",
    )

    status, payload = _measure(tmp_path, text)

    assert status == CONFORMS
    assert payload["conforms"] is True
    assert payload["failures"] == []
    assert payload["norms"] == []
    assert payload["heading_pairs"] == [
        {
            "id": "headline-standfirst",
            "kind": "headline-standfirst",
            "heading": headline,
            "following": standfirst,
            "shared_words": ["inte", "jag", "om", "vet"],
        },
        {
            "id": "subheading-1",
            "kind": "subheading-first-sentence-estimate",
            "heading": headline,
            "following": "Jag vet inte om ytterligare en ruta gör möten bättre.",
            "shared_words": ["inte", "jag", "om", "vet"],
        },
        {
            "id": "subheading-2",
            "kind": "subheading-first-sentence-estimate",
            "heading": ENDING_SUBHEADING,
            "following": ENDING_PARAGRAPH,
            "shared_words": ["givare", "nästa"],
        },
    ]


@pytest.mark.parametrize(
    ("paragraph", "first"),
    [
        ("”Ska vi prova?” Nästa fråga väntar.", "”Ska vi prova?”"),
        ("(Svaret är nej.) Nästa fråga väntar.", "(Svaret är nej.)"),
        ("Really?! Yes.", "Really?!"),
        ("Dr. Vik spoke. We listened.", "Dr."),
        (
            "Mätningen var 3.5 grader. Nästa mätning väntar.",
            "Mätningen var 3.5 grader.",
        ),
        ("En ofullbordad tanke", "En ofullbordad tanke"),
    ],
)
def test_first_sentence_is_an_estimate_that_preserves_terminal_closers(
    tmp_path: Path, paragraph: str, first: str
) -> None:
    """Quotes stay visible; abbreviations and fragments disclose the estimate."""

    _, payload = _measure(tmp_path, _article(body=f"## En fråga\n\n{paragraph}"))

    pair = payload["heading_pairs"][1]
    assert pair["kind"] == "subheading-first-sentence-estimate"
    assert pair["following"] == first


def test_each_subheading_pairs_only_with_its_own_first_prose(tmp_path: Path) -> None:
    """Deeper headings and non-prose never lend another section's sentence."""

    body = (
        "## Ingen egen prosa\n\n### En underrubrik\n\n"
        "```text\nInte prosa.\n```\n\n> Inte heller prosa.\n\n"
        "Här börjar prosan. Här fortsätter den.\n\n"
        "## Tomt avsnitt\n\n- Bara en lista\n\n"
        "## Sista avsnittet\n\nSista avsnittets första mening."
    )

    _, payload = _measure(tmp_path, _article(body=body))

    pairs = payload["heading_pairs"][1:]
    assert [pair["id"] for pair in pairs] == [
        "subheading-1",
        "subheading-2",
        "subheading-3",
        "subheading-4",
    ]
    assert [pair["following"] for pair in pairs] == [
        None,
        "Här börjar prosan.",
        None,
        "Sista avsnittets första mening.",
    ]
    assert pairs[0]["shared_words"] is None
    assert pairs[2]["shared_words"] is None


@pytest.mark.parametrize("first_paragraph", ["", "…"])
def test_unpairable_first_paragraph_does_not_select_a_later_one(
    tmp_path: Path, first_paragraph: str
) -> None:
    """A present but empty or punctuation-only paragraph supplies no sentence."""

    text = f"<h2>En rubrik</h2><p>{first_paragraph}</p><p>Senare prosa.</p>"

    _, payload = _measure(tmp_path, text)

    pair = payload["heading_pairs"][1]
    assert pair["following"] is None
    assert pair["shared_words"] is None


def test_shared_words_normalize_case_punctuation_and_repeated_tokens(
    tmp_path: Path,
) -> None:
    """Lexical tokens use NFC and casefold, without stemming or stop words."""

    heading = "Åsa, ÅSA — O’Neil 2026: STRASSE; ruta/rutor"
    paragraph = "A\u030asa möter O'NEIL 2026; Straße, ruta! Senare syns rutor."

    _, payload = _measure(tmp_path, _article(body=f"## {heading}\n\n{paragraph}"))

    pair = payload["heading_pairs"][1]
    assert pair["heading"] == heading
    assert pair["following"] == "Åsa möter O'NEIL 2026; Straße, ruta!"
    assert pair["shared_words"] == ["2026", "neil", "o", "ruta", "strasse", "åsa"]


@pytest.mark.parametrize(
    ("headline", "standfirst"),
    [(None, STANDFIRST), (HEADLINE, None), (None, None)],
)
def test_missing_front_members_are_null_without_changing_structural_failures(
    tmp_path: Path, headline: str | None, standfirst: str | None
) -> None:
    """Missing material is not a zero-overlap pair and cannot be invented."""

    status, payload = _measure(
        tmp_path, _article(headline=headline, standfirst=standfirst)
    )

    pair = payload["heading_pairs"][0]
    assert status == FAILS
    assert pair["heading"] == headline
    assert pair["following"] == (standfirst.strip("*") if standfirst else None)
    assert pair["shared_words"] is None
    expected = set()
    if headline is None:
        expected.add(HEADLINE_PART)
    if standfirst is None:
        expected.add(STANDFIRST_PART)
    assert _parts(payload) == expected


def test_standfirst_pair_contains_every_paragraph_and_ids_survive_rewording(
    tmp_path: Path,
) -> None:
    """Even a structurally invalid standfirst is shown whole, never truncated."""

    standfirst = "En första mening.\n\nEn andra mening."
    _, before = _measure(tmp_path, _article(standfirst=standfirst))
    _, after = _measure(
        tmp_path,
        _article(headline="En omformulerad huvudrubrik", standfirst=standfirst),
    )

    assert before["heading_pairs"][0]["following"] == standfirst
    assert [pair["id"] for pair in before["heading_pairs"]] == [
        pair["id"] for pair in after["heading_pairs"]
    ]


# --- The byline -----------------------------------------------------------


def test_every_conventional_byline_form_is_found_by_shape(tmp_path: Path) -> None:
    """A byline is a position and a shape, never a prefix.

    Swedish writes `Text: …`, `Av …`, a bare name, or a name and an
    organisation; English writes `By …`. A script matching prefixes would find
    the first and the last of those and report the rest missing.
    """

    for byline in (
        "Text: Hedda Lund",
        "Av Hedda Lund",
        "Hedda Lund",
        "Hedda Lund, Björkskolan",
        "By Hedda Lund",
    ):
        status, payload = _measure(tmp_path, _article(byline=byline))

        assert status == CONFORMS, payload
        assert payload["parts"]["byline"]["text"] == byline, byline


def test_a_paragraph_that_is_not_a_byline_leaves_the_part_missing(
    tmp_path: Path,
) -> None:
    """Where no block has the shape, the byline is reported missing.

    The standfirst then takes the first paragraph and the lead the rest, which
    is the reading the Skill is shown so that it can overrule it.
    """

    status, payload = _measure(tmp_path, _article(byline=None))

    assert status == FAILS
    assert BYLINE_PART in _parts(payload)
    assert payload["parts"]["byline"] is None
    assert payload["parts"]["standfirst"]["words"] == 26
    assert payload["parts"]["lead"]["text"].startswith("En temperaturgivare")


def test_a_byline_wrapped_over_two_source_lines_is_still_a_byline(
    tmp_path: Path,
) -> None:
    """A soft wrap is the source's, not the reader's.

    The same byline in HTML arrives as one run of text, so a rule that counted
    source lines answered one way for a text and another for its twin.
    """

    status, payload = _measure(
        tmp_path, _article(byline="Text: Hedda Lund,\nBjörkskolan")
    )

    assert status == CONFORMS, payload
    assert payload["parts"][BYLINE_PART]["text"] == "Text: Hedda Lund, Björkskolan"


def test_the_byline_carries_no_character_count(tmp_path: Path) -> None:
    """The anatomy gives the byline no dimension, so none is reported for it."""

    _, payload = _measure(tmp_path, _article())

    assert "characters" not in payload["parts"][BYLINE_PART]


# --- Missing parts --------------------------------------------------------


def test_a_text_with_no_standfirst_and_no_subheading_reports_both(
    tmp_path: Path,
) -> None:
    """The shape `column-flawed.md` has: headline, bare-name byline, lead, no section."""

    text = _article(
        headline="Möten förändrar allt",
        standfirst=None,
        byline="Nora Vik",
        lead="Vår mötesmall har plats för starttid och sluttid.",
        body="Samtal kan ha värde utan att leda till beslut.",
    )

    status, payload = _measure(tmp_path, text)

    assert status == FAILS
    assert payload["parts"]["byline"]["text"] == "Nora Vik"
    assert {STANDFIRST_PART, SECTIONS_PART} <= _parts(payload)
    assert payload["parts"]["sections"] == []


def test_a_hash_ending_a_word_belongs_to_the_headline(tmp_path: Path) -> None:
    """Markdown closes a heading only on a hash run preceded by whitespace.

    A headline naming `C#` is otherwise cut short by its own last character,
    and a text meeting the floor exactly is failed for a character it has.
    """

    status, payload = _measure(tmp_path, _article(headline="Vi valde tillslut C#"))

    assert status == CONFORMS, payload
    assert payload["parts"][HEADLINE_PART]["text"] == "Vi valde tillslut C#"
    assert payload["parts"][HEADLINE_PART]["characters"] == 20


def test_a_closing_hash_run_is_still_dropped(tmp_path: Path) -> None:
    """The decoration Markdown does have is still not part of the headline."""

    _, payload = _measure(tmp_path, _article(headline="Mätförsöket i Björkskolan ##"))

    assert payload["parts"][HEADLINE_PART]["text"] == "Mätförsöket i Björkskolan"


def test_an_underlined_heading_is_read_as_a_heading(tmp_path: Path) -> None:
    """Markdown has two spellings for a heading, and a text may use either.

    Read as paragraphs, the underlined headline and subheading here produce a
    missing headline and a missing section — two confident false failures.
    """

    text = (
        f"{HEADLINE}\n{'=' * 12}\n\n{STANDFIRST}\n\n{BYLINE}\n\n{LEAD}\n\n"
        f"En gräns för det lokala försöket\n{'-' * 8}\n\n{LEAD}\n\n"
        f"{ENDING_SUBHEADING}\n{'-' * 8}\n\n{ENDING_PARAGRAPH}\n"
    )

    status, payload = _measure(tmp_path, text)

    assert status == CONFORMS, payload
    assert payload["parts"][HEADLINE_PART]["text"] == HEADLINE
    assert payload["parts"][SECTIONS_PART][0]["subheading"]["text"] == (
        "En gräns för det lokala försöket"
    )


def test_a_headline_standing_after_the_first_subheading_is_reported_out_of_order(
    tmp_path: Path,
) -> None:
    """A level-1 heading below the body is the headline, in the wrong place.

    Reading it as no headline at all loses both the part and the defect: the
    text has a headline, and what is wrong is where it stands.
    """

    text = (
        f"{STANDFIRST}\n\n{BYLINE}\n\n{LEAD}\n\n"
        f"## En gräns för det lokala försöket\n\n# {HEADLINE}\n\n{LEAD}\n"
    )

    status, payload = _measure(tmp_path, text)

    assert status == FAILS
    assert payload["parts"][HEADLINE_PART]["text"] == HEADLINE
    assert "not the first block" in _measured(payload)


def test_a_headline_at_the_floor_passes_and_a_shorter_one_fails(
    tmp_path: Path,
) -> None:
    """Twenty characters is inside the limit; nineteen is outside it."""

    for characters, status in (
        (19, FAILS),
        (20, CONFORMS),
        (70, CONFORMS),
        (71, FAILS),
    ):
        headline = _cut(LONG_HEADLINE, characters)
        verdict, payload = _measure(tmp_path, _article(headline=headline))

        assert verdict == status, (characters, payload)
        assert payload["parts"]["headline"]["characters"] == characters
        if status is FAILS:
            assert HEADLINE_PART in _parts(payload)
            assert "characters" in _rules(payload)


def test_a_standfirst_is_measured_at_its_exact_word_limit(tmp_path: Path) -> None:
    """Sixty words conform; sixty-one is a requirement failure."""

    for count, status in ((60, CONFORMS), (61, FAILS)):
        verdict, payload = _measure(tmp_path, _article(standfirst=_words(count)))

        assert verdict == status, (count, payload)
        assert payload["parts"][STANDFIRST_PART]["words"] == count


def test_a_standfirst_of_two_paragraphs_is_measured_whole(tmp_path: Path) -> None:
    """The word limit is the standfirst's, so it counts all of the standfirst.

    Measuring the first paragraph alone reports a 40-word standfirst as 20 and
    lets a text twice over the limit come back inside it.
    """

    standfirst = f"{_words(40)}\n\n{_words(40)}"

    status, payload = _measure(tmp_path, _article(standfirst=standfirst))

    assert status == FAILS
    assert payload["parts"][STANDFIRST_PART]["words"] == 80
    assert payload["parts"][STANDFIRST_PART]["paragraphs"] == 2
    assert "80 words" in _measured(payload)


def test_a_subheading_is_measured_at_its_exact_character_limit(
    tmp_path: Path,
) -> None:
    """Seventy characters conform; seventy-one is a requirement failure.

    Both cuts carry `å`, `ä`, `ö` and an en dash, so the count is code points
    the reader sees rather than the bytes they were stored as.
    """

    for characters, status in ((70, CONFORMS), (71, FAILS)):
        subheading = _cut(LONG_SUBHEADING, characters)
        body = f"## {subheading}\n\n{LEAD}\n\n{ENDING}"
        verdict, payload = _measure(tmp_path, _article(body=body))

        assert verdict == status, (characters, payload)
        section = payload["parts"]["sections"][0]
        assert section["subheading"]["characters"] == characters


def test_two_paragraphs_before_the_first_subheading_fail_the_lead(
    tmp_path: Path,
) -> None:
    """The first subheading follows the lead directly, so the lead is one paragraph."""

    status, payload = _measure(tmp_path, _article(lead=f"{LEAD}\n\n{LEAD}"))

    assert status == FAILS
    assert LEAD_PART in _parts(payload)
    assert payload["parts"]["lead"]["paragraphs"] == 2


def test_a_section_holding_no_paragraph_fails(tmp_path: Path) -> None:
    """A subheading with nothing under it is a section that holds no text."""

    body = "## En gräns för det lokala försöket\n\n## Nästa försök behöver mer än givare\n\nLägg tiderna bredvid mätvärdena."

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == FAILS
    assert FIRST_SECTION in _parts(payload)
    assert payload["parts"]["sections"][0]["paragraphs"] == []


# --- Norms and typical figures --------------------------------------------


def test_a_level_three_heading_is_reported_as_a_norm(tmp_path: Path) -> None:
    """*Should* is a norm, and a norm the Skill weighs rather than a failure."""

    body = (
        f"## En gräns för det lokala försöket\n\n### En underavdelning\n\n{LEAD}"
        f"\n\n{ENDING}"
    )

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == CONFORMS, payload
    assert "levels" in _rules(payload, "norms")


def test_a_paragraph_over_eighty_words_is_reported_as_a_norm(tmp_path: Path) -> None:
    """Eighty words is the outer edge of a *should*, so passing it fails nothing."""

    body = f"## En gräns för det lokala försöket\n\n{_words(81)}\n\n{ENDING}"

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == CONFORMS, payload
    assert payload["parts"]["sections"][0]["paragraphs"][0]["words"] == 81
    assert "80 words" in _rules(payload, "norms")


def test_a_standfirst_and_a_lead_opening_alike_are_reported_as_a_norm(
    tmp_path: Path,
) -> None:
    """They should begin with different first words, whatever the word is."""

    status, payload = _measure(
        tmp_path,
        _article(standfirst="En mätning säger när luften var kall.", lead=LEAD),
    )

    assert status == CONFORMS, payload
    assert "first words" in _rules(payload, "norms")


def test_the_script_judges_nothing_but_the_counted_requirements(
    tmp_path: Path,
) -> None:
    """The shape `opinion-flawed.md` has: label subheadings and no proper ending.

    Whether `Bakgrund` describes its section, and whether the last one ends the
    piece, are the Skill's to judge. What the script reports here is the
    standfirst nobody wrote.
    """

    text = _article(
        headline="Kommunledningen hatar människor",
        standfirst=None,
        byline="Sanna Ek, Öppna beslut",
        lead="Kommunstyrelsen borde behålla telefonbokning under ett halvår.",
        body="## Bakgrund\n\nDet gjordes 96 bokningar på webben.\n\n## Diskussion\n\nHandlingarna saknar tidsmätning.\n\nNu är det dags att agera.",
    )

    status, payload = _measure(tmp_path, text)

    assert status == FAILS
    assert _parts(payload) == {STANDFIRST_PART}
    assert payload["typical"]["sections"] == 2


def test_a_text_of_one_section_fails_the_ending_section(tmp_path: Path) -> None:
    """The ending is a section of its own, so one section cannot be both.

    `opinion-flawed` was reported as meeting the anatomy while its closing line
    stood inside a section that carried the argument (#402). Whether a last
    section closes the piece stays the Skill's to judge; what the script can
    count is that the ending has a section beside the argument's, so at least
    two.
    """

    body = "## En gräns för det lokala försöket\n\nGivarna mätte varken luftdrag.\n\nNu är det dags att agera."

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == FAILS, payload
    assert payload["failures"] == [
        {
            "part": SECTIONS_PART,
            "rule": ENDING_IS_A_SECTION,
            "measured": "1 section",
            "text": "En gräns för det lokala försöket",
        }
    ]
    anatomy = " ".join(ANATOMY_REFERENCE.read_text(encoding="utf-8").split())
    assert ENDING_IS_A_SECTION in anatomy, (
        f"{ANATOMY_REFERENCE}: does not state the rule the script quotes."
    )


def test_a_requirement_and_a_norm_never_share_a_rule_string(tmp_path: Path) -> None:
    """The rule a finding quotes is what says which strength it carries.

    One string standing for both a section's floor and its ceiling, or for two
    separate norms on the headline, leaves the reader unable to tell a
    requirement from a *should* without counting the figure themselves.
    """

    body = (
        "## En gräns för det lokala försöket\n\n"
        "## Nästa försök behöver mer än givare\n\n" + "\n\n".join([LEAD] * 4) + "\n"
    )
    long_headline = _cut(LONG_HEADLINE, 65)

    _, payload = _measure(tmp_path, _article(headline=long_headline, body=body))

    failed = {entry["rule"] for entry in payload["failures"]}
    departed = {entry["rule"] for entry in payload["norms"]}
    assert failed & departed == set()
    assert len(departed) == len([entry["rule"] for entry in payload["norms"]])


def test_a_long_second_standfirst_paragraph_is_reported_under_the_standfirst(
    tmp_path: Path,
) -> None:
    """A part named wrongly is a fact the Skill has no reason to doubt."""

    standfirst = f"{_words(5)}\n\n{_words(81)}"

    status, payload = _measure(tmp_path, _article(standfirst=standfirst))

    assert status == FAILS
    assert [entry["part"] for entry in payload["norms"]] == [STANDFIRST_PART]


def test_a_stray_block_no_byline_can_place_is_reported_in_the_front(
    tmp_path: Path,
) -> None:
    """Where the byline is missing, nothing divides the standfirst from the lead.

    The quotation below stands somewhere in front of the first subheading, and
    that is the whole of what is known about it — so that is what is said.
    """

    text = _article(byline=None, lead=f"> Ett citat ur rapporten.\n\n{LEAD}")

    status, payload = _measure(tmp_path, text)

    assert status == FAILS
    assert [entry["part"] for entry in payload["parts"]["other"]] == [FRONT_PART]


# --- Blocks that are neither heading nor paragraph ------------------------


def test_a_block_that_is_neither_heading_nor_paragraph_is_reported_and_counted_nowhere(
    tmp_path: Path,
) -> None:
    """A list inside a section is reported where it sits and enters no limit."""

    body = (
        "## En gräns för det lokala försöket\n"
        "\n"
        "- Ett mätvärde\n"
        "- Ett till\n"
        "\n"
        "> Ett citat ur rapporten.\n"
        "\n"
        f"{LEAD}\n"
        "\n"
        f"{ENDING}"
    )

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == CONFORMS, payload
    assert len(payload["parts"]["sections"][0]["paragraphs"]) == 1
    assert [entry["part"] for entry in payload["parts"]["other"]] == [
        FIRST_SECTION,
        FIRST_SECTION,
    ]


# --- HTML -----------------------------------------------------------------

HTML_TWIN = """\
<h1>M&auml;tf&ouml;rs&ouml;ket i Bj&ouml;rkskolan visar n&auml;r, inte varf&ouml;r</h1>
<p><strong>Under 14 av 120 lektionspass registrerade givarna temperaturer under arbetsgränsen. Fyra veckors mätningar pekar ut tillfällen att undersöka närmare, men förklarar inte varför luften var kall.</strong></p>
<p>Text: Hedda Lund</p>
<p>En temperaturgivare mäter luften där den sitter. Det gör placeringen viktig när fastighetskontoret ska tolka fyra veckors mätningar. Genomgången nedan visar vad värdena räcker till.</p>
<h2>En gräns för det lokala försöket</h2>
<p>Kontoret valde 20 grader Celsius som arbetsgräns. Rapporten räknar 14 lektionspass av 120 med minst en mätning under den gränsen.</p>
<p>Givarna mätte varken luftdrag eller elevernas upplevelse.</p>
<h2>Nästa försök behöver mer än givare</h2>
<p>Lägg tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp.</p>
"""

WORDPRESS_TWIN = """\
<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">Mätförsöket i Björkskolan visar när, inte varför</h1>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Under 14 av 120 lektionspass registrerade givarna temperaturer under arbetsgränsen. Fyra veckors mätningar pekar ut tillfällen att undersöka närmare, men förklarar inte varför luften var kall.</strong></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Text: Hedda Lund</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>En temperaturgivare mäter luften där den sitter. Det gör placeringen viktig när fastighetskontoret ska tolka fyra veckors mätningar. Genomgången nedan visar vad värdena räcker till.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">En gräns för det lokala försöket</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Kontoret valde 20 grader Celsius som arbetsgräns. Rapporten räknar 14 lektionspass av 120 med minst en mätning under den gränsen.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Givarna mätte varken luftdrag eller elevernas upplevelse.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Nästa försök behöver mer än givare</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Lägg tiderna för när rummen används bredvid mätvärdena innan nästa givare sätts upp.</p>
<!-- /wp:paragraph -->
"""


def test_html_measures_exactly_as_its_markdown_twin_does(tmp_path: Path) -> None:
    """The anatomy names both forms, so both forms answer the same way.

    The HTML twin writes its headline in character entities, which decode to
    the letters the Markdown twin spells out.
    """

    _, markdown = _measure(tmp_path, _article())
    status, html = _measure(tmp_path, HTML_TWIN)

    assert status == CONFORMS, html
    assert html["format"] == HTML
    assert _figures(html) == _figures(markdown)


def test_wordpress_block_comments_change_no_figure(tmp_path: Path) -> None:
    """A comment is a block that is neither heading nor paragraph.

    It is reported where it stands, it enters no limit, and it does not
    displace the headline from the front of the text.
    """

    _, markdown = _measure(tmp_path, _article())
    status, wordpress = _measure(tmp_path, WORDPRESS_TWIN)

    assert status == CONFORMS, wordpress
    assert _figures(wordpress) == _figures(markdown)
    assert wordpress["parts"]["other"][0]["part"] == BEFORE_HEADLINE_PART


# --- Reading the text -----------------------------------------------------


def test_a_text_is_measured_from_standard_input(tmp_path: Path) -> None:
    """A response-targeted run has no file to point at, and needs none."""

    result = _run("-", stdin=_article())

    assert result.returncode == CONFORMS, result.stderr
    assert _json(result)["parts"]["headline"]["text"] == HEADLINE


def test_an_unreadable_path_is_not_measured(tmp_path: Path) -> None:
    """Exit 2 is *not measured*, and it says which of the ways it was not."""

    result = _run(str(tmp_path / "absent.md"))

    assert result.returncode == UNMEASURED
    payload = _json(result)
    assert payload["ok"] is False
    assert payload["code"] == UNREADABLE_INPUT
    assert payload["message"]


def test_an_empty_text_is_not_measured(tmp_path: Path) -> None:
    """Frontmatter is not the text, so a document that is only frontmatter is empty."""

    status, payload = _measure(tmp_path, f"{FRONTMATTER}\n\n   \n")

    assert status == UNMEASURED
    assert payload["code"] == EMPTY_TEXT


def test_a_text_with_no_heading_and_no_paragraph_is_not_measured(
    tmp_path: Path,
) -> None:
    """Where neither form can be read, the script says so rather than guessing."""

    status, payload = _measure(tmp_path, "- Ett mätvärde\n- Ett till\n")

    assert status == UNMEASURED
    assert payload["code"] == NO_STRUCTURE
    assert payload["ok"] is False


# --- The corpus's own positive controls -----------------------------------


def test_every_clean_control_of_the_four_article_genres_conforms() -> None:
    """The corpus says each of them conforms, and this is what says it again.

    A control that fails here is a disagreement between the corpus and the
    script, and one of the two is wrong — which is why the script is run
    against them rather than against a fixture written to agree with it.
    """

    for name in CLEAN_CONTROLS:
        result = _run(str(CONTROLS / name))

        assert result.returncode == CONFORMS, (name, result.stdout, result.stderr)


# --- The press release ----------------------------------------------------

# The press release states its own two counted limits in its genre file, and
# the script measures those and nothing else of it (#473): the headline, which
# is the release's level-1 heading, and the summary, which is the first
# paragraph after it. Everything else a release owes its reader is read.
PRESS_RELEASE = LIBRARY / "references" / "editorial" / "genres" / "pressrelease.md"
PRESS_GENRE = "--genre=pressrelease"
SUMMARY_PART = "summary"
NO_HEADLINE = "no-headline"
PRESS_HEADLINE_IS_A_HEADING = (
    "The headline is the release's level-1 heading (`h1` in HTML, `#` in Markdown)."
)
PRESS_HEADLINE_LIMIT = "The headline is at most 70 characters, spaces included."
PRESS_SUMMARY_IS_FIRST = "The summary is the first paragraph after the headline."
PRESS_SUMMARY_LIMIT = "The summary is at most 60 words."

RELEASE_EMBARGO = "Får publiceras från den 6 maj 2027 klockan 08.00."
RELEASE_HEADLINE = "Fagerviks stadsbibliotek öppnar reparationsverkstad den 6 maj"
RELEASE_SUMMARY = (
    "Fagervik, 22 april 2027 – Fagerviks stadsbibliotek öppnar en"
    " reparationsverkstad på plan två den 6 maj. Besökare lagar sin egen"
    " elektronik med hjälp av volontärer, tisdagar och torsdagar klockan 15–19,"
    " under ett försöksår som kommunen finansierar med 180 000 kronor."
)
# Counted by hand: the dateline's four words are among them, and its dash is
# no word.
RELEASE_SUMMARY_WORDS = 39
RELEASE_REST = (
    "”Vi vill se om lagandet får ett eget rum hos oss”, säger bibliotekschefen"
    " Anna Lindqvist.\n"
    "\n"
    "Fem volontärer från föreningen Fagerviks Reparatörer bemannar verkstaden."
    " Verkstaden tar inte emot apparater för reparation och säljer inga"
    " reservdelar.\n"
    "\n"
    "Kontakt: Anna Lindqvist, bibliotekschef, 070-000 00 00."
)


def _release(
    *,
    embargo: str | None = None,
    headline: str | None = RELEASE_HEADLINE,
    summary: str | None = RELEASE_SUMMARY,
    rest: str | None = RELEASE_REST,
) -> str:
    """Assemble one Markdown press release out of the parts named."""

    blocks = [
        embargo,
        f"# {headline}" if headline is not None else None,
        summary,
        rest,
    ]
    return "\n\n".join(block for block in blocks if block is not None) + "\n"


def test_a_conforming_press_release_measures_clean(tmp_path: Path) -> None:
    """A release inside both limits conforms, whatever else it carries.

    The release carries a publication time above its headline, a dateline
    opening its summary, a quotation, a body and a contact, and none of them
    is a part the anatomy knows: none of them may turn into a failure.
    """

    status, payload = _measure(tmp_path, _release(embargo=RELEASE_EMBARGO), PRESS_GENRE)

    assert status == CONFORMS, payload
    assert payload["ok"] is True
    assert payload["conforms"] is True
    assert payload["failures"] == []
    assert payload["format"] == MARKDOWN


def test_a_press_release_reports_its_two_parts_and_nothing_of_the_anatomy(
    tmp_path: Path,
) -> None:
    """The answer carries the headline and the summary, and no norm or pair.

    The anatomy's norms, its whole-text figures and its heading pairs belong
    to the four article genres; for a release the headline and the summary
    are read against each other by the agent, as the genre says.
    """

    _, payload = _measure(tmp_path, _release(embargo=RELEASE_EMBARGO), PRESS_GENRE)

    assert set(payload) == {"ok", "format", "conforms", "failures", "parts"}
    assert set(payload["parts"]) == {HEADLINE_PART, SUMMARY_PART}
    assert payload["parts"][HEADLINE_PART] == {
        "text": RELEASE_HEADLINE,
        "characters": len(RELEASE_HEADLINE),
        "words": len(RELEASE_HEADLINE.split()),
    }
    summary = payload["parts"][SUMMARY_PART]
    assert summary["text"].startswith("Fagervik, 22 april 2027 – Fagerviks")
    assert summary["words"] == RELEASE_SUMMARY_WORDS, summary


def test_a_press_release_headline_is_measured_at_its_exact_limit(
    tmp_path: Path,
) -> None:
    """Seventy characters pass and seventy-one fail, counted as code points."""

    at_limit = _cut(LONG_HEADLINE, 70)
    over = _cut(LONG_HEADLINE, 71)

    status, payload = _measure(tmp_path, _release(headline=at_limit), PRESS_GENRE)
    assert status == CONFORMS, payload

    status, payload = _measure(tmp_path, _release(headline=over), PRESS_GENRE)
    assert status == FAILS, payload
    assert _parts(payload) == {HEADLINE_PART}
    assert _rules(payload) == PRESS_HEADLINE_LIMIT
    assert _measured(payload) == "71 characters"


def test_a_short_press_release_headline_is_no_failure(tmp_path: Path) -> None:
    """The release states no floor, so the anatomy's twenty characters do not bind."""

    status, payload = _measure(
        tmp_path, _release(headline="Biblioteket lagar"), PRESS_GENRE
    )

    assert status == CONFORMS, payload


def test_a_press_release_summary_is_measured_at_its_exact_word_limit(
    tmp_path: Path,
) -> None:
    """Sixty words pass and sixty-one fail, the dateline counted with them."""

    dateline = "Fagervik, 22 april 2027 –"
    at_limit = f"{dateline} {_words(60 - 4)}"
    over = f"{dateline} {_words(61 - 4)}"

    status, payload = _measure(tmp_path, _release(summary=at_limit), PRESS_GENRE)
    assert status == CONFORMS, payload
    assert payload["parts"][SUMMARY_PART]["words"] == 60

    status, payload = _measure(tmp_path, _release(summary=over), PRESS_GENRE)
    assert status == FAILS, payload
    assert _parts(payload) == {SUMMARY_PART}
    assert _rules(payload) == PRESS_SUMMARY_LIMIT
    assert _measured(payload) == "61 words"


def test_a_publication_time_above_the_headline_does_not_become_the_summary(
    tmp_path: Path,
) -> None:
    """The summary is the first paragraph after the headline, never before it."""

    long_embargo = _words(70)
    status, payload = _measure(tmp_path, _release(embargo=long_embargo), PRESS_GENRE)

    assert status == CONFORMS, payload
    assert payload["parts"][SUMMARY_PART]["words"] == RELEASE_SUMMARY_WORDS


def test_a_press_release_with_no_level_one_heading_is_not_measured(
    tmp_path: Path,
) -> None:
    """Without the headline there is nothing to find the summary after."""

    text = f"## {RELEASE_HEADLINE}\n\n{RELEASE_SUMMARY}\n\n{RELEASE_REST}\n"
    status, payload = _measure(tmp_path, text, PRESS_GENRE)

    assert status == UNMEASURED, payload
    assert payload["ok"] is False
    assert payload["code"] == NO_HEADLINE


def test_the_first_of_two_level_one_headings_is_the_headline(
    tmp_path: Path,
) -> None:
    """A second level-1 heading is read past, and counted in no limit."""

    text = _release(rest=f"# {LONG_HEADLINE}\n\n{RELEASE_REST}")
    status, payload = _measure(tmp_path, text, PRESS_GENRE)

    assert status == CONFORMS, payload
    assert payload["parts"][HEADLINE_PART]["text"] == RELEASE_HEADLINE


def test_a_press_release_with_nothing_after_its_headline_lacks_a_summary(
    tmp_path: Path,
) -> None:
    """A headline standing alone leaves the summary's limit with nothing to hold."""

    status, payload = _measure(tmp_path, _release(summary=None, rest=None), PRESS_GENRE)

    assert status == FAILS, payload
    assert _parts(payload) == {SUMMARY_PART}
    assert _rules(payload) == PRESS_SUMMARY_IS_FIRST
    assert _measured(payload) == "absent"
    assert payload["parts"][SUMMARY_PART] is None


def test_a_press_release_in_html_measures_as_its_markdown_twin(
    tmp_path: Path,
) -> None:
    """The form is read off the text, for a release as for an article."""

    over = _cut(LONG_HEADLINE, 71)
    markdown = _release(embargo=RELEASE_EMBARGO, headline=over)
    html = (
        f"<p>{RELEASE_EMBARGO}</p>\n<h1>{over}</h1>\n<p>{RELEASE_SUMMARY}</p>\n"
        "<p>Kontakt: Anna Lindqvist, bibliotekschef, 070-000 00 00.</p>\n"
    )

    markdown_status, markdown_payload = _measure(tmp_path, markdown, PRESS_GENRE)
    html_status, html_payload = _measure(tmp_path, html, PRESS_GENRE)

    assert html_payload["format"] == HTML
    assert (html_status, html_payload["failures"]) == (
        markdown_status,
        markdown_payload["failures"],
    )
    assert html_payload["parts"] == markdown_payload["parts"]


def test_the_press_release_states_every_rule_the_script_quotes() -> None:
    """The script quotes the genre, so the genre has to say what it quotes."""

    genre = " ".join(PRESS_RELEASE.read_text(encoding="utf-8").split())

    for rule in (
        PRESS_HEADLINE_IS_A_HEADING,
        PRESS_HEADLINE_LIMIT,
        PRESS_SUMMARY_IS_FIRST,
        PRESS_SUMMARY_LIMIT,
    ):
        assert rule in genre, f"{PRESS_RELEASE}: does not state {rule!r}."


def test_an_article_genre_named_explicitly_measures_the_anatomy(
    tmp_path: Path,
) -> None:
    """Naming one of the four article genres changes nothing of the answer."""

    text = _article()
    default_status, default_payload = _measure(tmp_path, text)
    named_status, named_payload = _measure(tmp_path, text, "--genre=column")

    assert (named_status, named_payload) == (default_status, default_payload)


def test_a_genre_the_script_does_not_measure_is_refused(tmp_path: Path) -> None:
    """A genre with no counted limit here is a malformed invocation."""

    path = tmp_path / "text.md"
    path.write_text(_release(), encoding="utf-8")
    result = _run("--genre=report", str(path))

    assert result.returncode == UNMEASURED
    assert result.stdout == ""
