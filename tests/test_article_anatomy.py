"""CLI behaviour of the Collection Library's article-anatomy measuring script."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

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
FRONTMATTER = "---\nkntnt:\n  genre: article\n  technique: none\n  language: sv\n---"

# What a headline and a subheading of an exact length are cut from. Both carry
# `å`, `ä`, `ö` and an en dash inside the first seventy characters, so a script
# counting UTF-8 bytes or decomposed code points cannot agree with one counting
# what the reader sees.
LONG_HEADLINE = (
    "Mätförsöket i Björkskolan visar när, inte varför och hur länge luften var kall"
)
LONG_SUBHEADING = "Mätförsöket i Björkskolan – när, inte varför, och vad som ändå återstår att göra"


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
    assert payload["format"] == "markdown"


def test_a_conforming_article_reports_what_it_took_as_which_part(
    tmp_path: Path,
) -> None:
    """The Skill can overrule a wrong guess only where the guess is stated."""

    _, payload = _measure(tmp_path, _article(frontmatter=FRONTMATTER))

    parts = payload["parts"]
    assert parts["headline"]["text"] == HEADLINE
    assert parts["headline"]["characters"] == 48
    assert parts["headline"]["words"] == 7
    assert parts["standfirst"]["words"] == 30
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
    assert "byline" in _parts(payload)
    assert payload["parts"]["byline"] is None
    assert payload["parts"]["standfirst"]["words"] == 30
    assert payload["parts"]["lead"]["text"].startswith("En temperaturgivare")


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
    assert {"standfirst", "sections"} <= _parts(payload)
    assert payload["parts"]["sections"] == []


def test_a_headline_at_the_floor_passes_and_a_shorter_one_fails(
    tmp_path: Path,
) -> None:
    """Twenty characters is inside the limit; nineteen is outside it."""

    for characters, status in ((19, FAILS), (20, CONFORMS), (70, CONFORMS), (71, FAILS)):
        headline = _cut(LONG_HEADLINE, characters)
        verdict, payload = _measure(tmp_path, _article(headline=headline))

        assert verdict == status, (characters, payload)
        assert payload["parts"]["headline"]["characters"] == characters
        if status is FAILS:
            assert "headline" in _parts(payload)
            assert "characters" in _rules(payload)


def test_a_standfirst_is_measured_at_its_exact_word_limit(tmp_path: Path) -> None:
    """Sixty words conform; sixty-one is a requirement failure."""

    for count, status in ((60, CONFORMS), (61, FAILS)):
        verdict, payload = _measure(tmp_path, _article(standfirst=_words(count)))

        assert verdict == status, (count, payload)
        assert payload["parts"]["standfirst"]["words"] == count


def test_a_subheading_is_measured_at_its_exact_character_limit(
    tmp_path: Path,
) -> None:
    """Seventy characters conform; seventy-one is a requirement failure.

    Both cuts carry `å`, `ä`, `ö` and an en dash, so the count is code points
    the reader sees rather than the bytes they were stored as.
    """

    for characters, status in ((70, CONFORMS), (71, FAILS)):
        subheading = _cut(LONG_SUBHEADING, characters)
        body = f"## {subheading}\n\n{LEAD}"
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
    assert "lead" in _parts(payload)
    assert payload["parts"]["lead"]["paragraphs"] == 2


def test_a_section_holding_no_paragraph_fails(tmp_path: Path) -> None:
    """A subheading with nothing under it is a section that holds no text."""

    body = "## En gräns för det lokala försöket\n\n## Nästa försök behöver mer än givare\n\nLägg tiderna bredvid mätvärdena."

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == FAILS
    assert "section 1" in _parts(payload)
    assert payload["parts"]["sections"][0]["paragraphs"] == []


# --- Norms and typical figures --------------------------------------------


def test_a_level_three_heading_is_reported_as_a_norm(tmp_path: Path) -> None:
    """*Should* is a norm, and a norm the Skill weighs rather than a failure."""

    body = f"## En gräns för det lokala försöket\n\n### En underavdelning\n\n{LEAD}"

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == CONFORMS, payload
    assert "levels" in _rules(payload, "norms")


def test_a_paragraph_over_eighty_words_is_reported_as_a_norm(tmp_path: Path) -> None:
    """Eighty words is the outer edge of a *should*, so passing it fails nothing."""

    body = f"## En gräns för det lokala försöket\n\n{_words(81)}"

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
    assert _parts(payload) == {"standfirst"}
    assert payload["typical"]["sections"] == 2


# --- Blocks that are neither heading nor paragraph ------------------------


def test_a_block_that_is_neither_heading_nor_paragraph_is_reported_and_counted_nowhere(
    tmp_path: Path,
) -> None:
    """A list inside a section is reported by kind and enters no limit."""

    body = (
        "## En gräns för det lokala försöket\n"
        "\n"
        "- Ett mätvärde\n"
        "- Ett till\n"
        "\n"
        "> Ett citat ur rapporten.\n"
        "\n"
        f"{LEAD}"
    )

    status, payload = _measure(tmp_path, _article(body=body))

    assert status == CONFORMS, payload
    assert len(payload["parts"]["sections"][0]["paragraphs"]) == 1
    assert {entry["kind"] for entry in payload["parts"]["other"]} == {
        "list",
        "blockquote",
    }
    assert {entry["part"] for entry in payload["parts"]["other"]} == {"section 1"}


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
    assert html["format"] == "html"
    assert _figures(html) == _figures(markdown)


def test_wordpress_block_comments_change_no_figure(tmp_path: Path) -> None:
    """A comment is a block that is neither heading nor paragraph.

    It is reported by kind, it enters no limit, and it does not displace the
    headline from the front of the text.
    """

    _, markdown = _measure(tmp_path, _article())
    status, wordpress = _measure(tmp_path, WORDPRESS_TWIN)

    assert status == CONFORMS, wordpress
    assert _figures(wordpress) == _figures(markdown)
    assert {entry["kind"] for entry in wordpress["parts"]["other"]} == {"comment"}


def test_the_format_option_overrides_what_detection_would_choose(
    tmp_path: Path,
) -> None:
    """Detection is a default, and a caller who knows the form says so.

    Read as Markdown, an HTML document is raw HTML throughout: no heading and
    no paragraph, so there is nothing to measure.
    """

    auto, _ = _measure(tmp_path, HTML_TWIN)
    forced, payload = _measure(tmp_path, HTML_TWIN, "--format=markdown")

    assert auto == CONFORMS
    assert forced == UNMEASURED
    assert payload["code"] == "no-structure"


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
    assert payload["code"] == "unreadable-input"
    assert payload["message"]


def test_an_empty_text_is_not_measured(tmp_path: Path) -> None:
    """Frontmatter is not the text, so a document that is only frontmatter is empty."""

    status, payload = _measure(tmp_path, f"{FRONTMATTER}\n\n   \n")

    assert status == UNMEASURED
    assert payload["code"] == "empty-text"


def test_a_text_with_no_heading_and_no_paragraph_is_not_measured(
    tmp_path: Path,
) -> None:
    """Where neither form can be read, the script says so rather than guessing."""

    status, payload = _measure(tmp_path, "- Ett mätvärde\n- Ett till\n")

    assert status == UNMEASURED
    assert payload["code"] == "no-structure"
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
