# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Measure the article anatomy's counted limits in one text.

`references/editorial/article-anatomy.md` fixes the parts of a text in the
genres `article`, `case-study`, `column` and `opinion`, their order and their
dimensions. This script counts them and exposes heading/following-text pairs
with lexical overlap for the editorial agent to judge. ADR-0209 records why
counted dimensions belong to a script rather than to the agent reading them.

## The command line

    uv run --no-cache --no-project article_anatomy.py <path>

`<path>` may be `-`, which reads the text from standard input, so a
response-targeted run needs no scratch file. The form is read off the text
itself: HTML where it carries block tags (`<h1>`-`<h6>`, `<p>`) and no ATX
heading line, Markdown otherwise. The command line goes to `argparse` as in the
Library's other engines — the machine-readable refusals here are about the text
rather than about the line, so there is no JSON refusal for a malformed
invocation to travel in.

## The exit status is the verdict

`0` measured, and every counted requirement holds. `1` measured, and at least
one fails. `2` not measured. All three print one JSON object on stdout, and a
refusal carries `ok: false`, a stable `code` — `unreadable-input`, `empty-text`
or `no-structure` — and a `message`.

## What is read as what

Leading YAML frontmatter is skipped and never parsed. What remains is read as
blocks: a heading (ATX or setext in Markdown, `h1`-`h6` in HTML), a paragraph,
a code block, or `other`, which is a list, a quotation, a table, an image, raw
HTML or a comment. Only headings and paragraphs enter a limit; every other
block is reported under the part it sits in and counted in none.

The headline is the first level-1 heading. The standfirst, the byline and the
lead lie between it and the first level-2 heading, and the byline is the first
paragraph there of at most twelve words that does not end in `.`, `!`, `?` or
`…`. Paragraphs before it are the standfirst and those after it the lead; where
no paragraph has that shape the byline is reported missing, the first paragraph
is taken as the standfirst and the rest as the lead. The answer names which
block was taken as which, so a Skill can overrule it — as it has to where a
text opens on a byline-shaped dramatic line standing before the real byline,
which is the line this rule finds. Each level-2 heading opens a section running
to the next one. The ending is a section of its own after at least one other,
so a text of one section fails; whether its last section is an ending — closing
the piece rather than carrying the argument — is the Skill's to judge.

Text is measured as the reader sees it: Markdown emphasis, code and link syntax
stripped, HTML reduced to its text with entities decoded, whitespace collapsed
and the result normalised to NFC. Characters are code points, spaces included.
A word is a whitespace-separated token holding at least one letter or digit, so
a lone dash is no word. Sentences are split on terminal punctuation and are
always reported as `sentences_estimate`, an abbreviation ending a sentence as
far as any splitter can tell.

## The shape of the answer

`ok`, `format`, `conforms`, `failures`, `norms`, `typical`, `parts` and
`heading_pairs`.

Each entry of `failures` and of `norms` carries `part` — `headline`,
`standfirst`, `byline`, `lead`, `sections` or `section <n>` — `rule` in the
anatomy's words, `measured` as a figure in words, and `text`, which is the text
measured or `null` where the part is absent. No rule string is shared by a
failure and a norm, so the strength of a statement is readable off the entry.

`typical` carries `paragraphs`, `paragraphs_of_two_or_three_sentences`,
`sections` and `sections_of_two_or_three_paragraphs`.

`parts` carries `headline`, `standfirst`, `byline`, `lead`, `sections` and
`other`, and a part nothing was found for is `null`. `headline` and a section's
`subheading` carry `text`, `characters` and `words`; `byline` carries `text`
and `words`, the anatomy giving it no dimension; `standfirst`, `lead` and a
section's paragraphs carry their opening words as `text` beside `words` and
`sentences_estimate`, and `standfirst` and `lead` also carry `paragraphs`,
their figures covering every paragraph they hold. `other` names each remaining
block's `part` — `before the headline`, `standfirst`, `lead`, `section <n>`, or
`front` where no byline settles which side of it a block stands — and its
opening `text`.

`heading_pairs` is unjudged evidence, independent of `failures`, `norms`,
`conforms` and the exit status. Each entry carries `id`, `kind`, the complete
visible `heading` and `following` text, and `shared_words`. The first entry's
id and kind are `headline-standfirst`; it joins every standfirst paragraph
with two newlines. Subsequent ids are `subheading-1`, `subheading-2`, etc., in
document order across levels 2–6, with kind
`subheading-first-sentence-estimate`. Ids survive rewording and equivalent
Markdown/HTML, but inserting or removing a subheading renumbers later ones.
They identify positions within a measurement, not persistent document objects.

For each subheading, the first paragraph before the next heading of any level
supplies the sentence estimate; intervening non-prose blocks are skipped.
The estimate ends at the first `.`, `!`, `?` or `…` followed by optional closing
quotes/brackets and whitespace. Closing marks remain in the visible text.
Without such a boundary, the whole first paragraph is the estimate, even an
unterminated fragment. Abbreviations such as `Dr. Vik` and ellipses can split
prematurely; a decimal such as `3.5` does not split. No language-specific
sentence parser is implied. A missing member is `null`; a first paragraph
with no letter or digit is unpairable and supplies `null`, never a later
paragraph or another section's prose. The structural `parts` still show what
was parsed, and callers check ambiguous or missing pairs against the full text.

Overlap tokenization is separate from dimension word counts: casefold each
visible text, normalize to NFC, then take maximal Unicode alphanumeric runs
(`[^\\W_]+`). Punctuation, underscores and whitespace separate tokens, including
apostrophes and hyphens. Shared words are the unique intersection, sorted by
Unicode code point; repeated occurrences count once, with no stop-word
removal, stemming, synonyms or similarity score. `shared_words` is `null`
when a member is `null`, and `[]` when both are present but share no tokens.
The visible text keeps its original wording, case and punctuation beside the
normalized words. A repeated name or subject word can be necessary; an echo
can paraphrase with no shared word. Neither observation is an automatic finding.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from enum import StrEnum
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

# The anatomy's counted limits, each named for the part it belongs to. They are
# the one thing in this file that has to agree with a document, so they are
# written where a reader comparing the two finds them together.
HEADLINE_CHARACTERS = (20, 70)
HEADLINE_NORM_CHARACTERS = 60
HEADLINE_NORM_WORDS = (3, 8)
STANDFIRST_WORDS = 60
BYLINE_WORDS = 12
SUBHEADING_CHARACTERS = 70
PARAGRAPH_NORM_WORDS = 80
SECTION_NORM_PARAGRAPHS = 3

# What *most* is read against: the anatomy says most paragraphs come to two or
# three sentences and most sections hold two or three paragraphs.
TYPICAL = (2, 3)

# The anatomy's own words, one string per statement. A requirement and a norm
# never share one, so a reader of an entry can tell which strength it carries
# without looking at which list it came out of.
ORDER = "A text conforms when every part is present in the order shown."
ONCE = "Each part appears once, except the section, which repeats."
HEADLINE_IS_A_HEADING = (
    "The headline is the text's level-1 heading (HTML `h1`, Markdown `#`)."
)
HEADLINE_LIMIT = "20–70 characters, spaces included."
HEADLINE_NORM_LENGTH = "It should be at most 60 characters."
HEADLINE_NORM_WORDING = "It should be three to eight words."
STANDFIRST_ONE_PARAGRAPH = "The standfirst is one paragraph."
STANDFIRST_WORD_LIMIT = "The standfirst is at most 60 words."
LEAD_IS_ONE_PARAGRAPH = (
    "The lead is the first paragraph of the body: one paragraph, meeting every"
    " requirement under *Paragraphs*."
)
SUBHEADING_LIMIT = "A subheading is at most 70 characters, spaces included."
SECTION_HOLDS_A_PARAGRAPH = "A section holds at least one paragraph."
ENDING_IS_A_SECTION = (
    "The ending is a section of its own, opened by its own subheading, after at"
    " least one other section."
)
SECTION_NORM = "A section should hold at most three paragraphs."
TWO_LEVELS = "The text should use these two levels only."
DIFFERENT_FIRST_WORDS = (
    "They should begin with different first words, and an everyday word such as"
    " *the* or *it* counts like any other."
)
PARAGRAPH_NORM = (
    "A paragraph should be at most 80 words, so that a web reader takes it in at"
    " a glance."
)

# How much of a paragraph a report carries. Enough for a Skill to recognise
# which paragraph is meant, and not so much that the answer repeats the text.
OPENING_WORDS = 8

# The verdict, carried by the exit status rather than by a field a caller has
# to parse: a Skill running this from a step reads a status without reading
# anything.
CONFORMS = 0
FAILS = 1
UNMEASURED = 2


class Kind(StrEnum):
    """What a block is, to the extent that anything here turns on it."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    CODE = "code"
    OTHER = "other"


class Part(StrEnum):
    """The part a figure or a stray block is reported under."""

    HEADLINE = "headline"
    STANDFIRST = "standfirst"
    BYLINE = "byline"
    LEAD = "lead"
    SECTIONS = "sections"

    # Two positions rather than parts, for a block that is neither heading nor
    # paragraph: where it stands is a fact, and `FRONT` is what is said instead
    # of a guess where no byline divides the standfirst from the lead.
    BEFORE_HEADLINE = "before the headline"
    FRONT = "front"


class Form(StrEnum):
    """The form a text is written in, as the answer reports it."""

    MARKDOWN = "markdown"
    HTML = "html"


class Code(StrEnum):
    """The stable reasons a text is not measured at all."""

    UNREADABLE_INPUT = "unreadable-input"
    EMPTY_TEXT = "empty-text"
    NO_STRUCTURE = "no-structure"


# What the reader sees as the end of a sentence, and what may stand between
# that mark and the space after it.
SENTENCE = re.compile(r"(?<=[.!?…])[\"'”’»)\]]*\s+")
TERMINAL = (".", "!", "?", "…")

# Markdown inline syntax, in the order it is removed: a code span first, so
# that emphasis marks inside one are not read as emphasis, then what links and
# images spell, then the emphasis runs themselves.
CODE_SPAN = re.compile(r"(?P<fence>`+)(?P<code>.+?)(?P=fence)", re.DOTALL)
IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
REFERENCE = re.compile(r"\[([^\]]*)\]\[[^\]]*\]")
AUTOLINK = re.compile(r"<((?:https?|mailto):[^>]+)>")
EMPHASIS = (
    re.compile(r"\*\*(.+?)\*\*", re.DOTALL),
    re.compile(r"__(.+?)__", re.DOTALL),
    re.compile(r"~~(.+?)~~", re.DOTALL),
    re.compile(r"\*(.+?)\*", re.DOTALL),
    re.compile(r"(?<![0-9A-Za-z_])_(.+?)_(?![0-9A-Za-z_])", re.DOTALL),
)
TAG = re.compile(r"<[^>]+>")
ESCAPE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!>|~])")

# A fence, and the two ways Markdown writes a heading. The closing run of an
# ATX heading has to be preceded by whitespace, so a hash that ends a word —
# `C#` — is part of the headline rather than a decoration on it.
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
ATX = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?(?:[ \t]+#+)?[ \t]*$")
SETEXT = re.compile(r"^ {0,3}(=+|-+)[ \t]*$")

# A line opening something the reader does not meet as prose: an indented
# block, a list item, a quotation, a table row, raw HTML or a comment, or a
# thematic break. Which of them it is drives nothing, so the block is reported
# as `other` and enters no limit.
NOT_PROSE = re.compile(
    r"^(?: {4}|\t)"
    r"|^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:[ \t]|$)"
    r"|^ {0,3}[>|<]"
    r"|^ {0,3}(?:[-*_][ \t]*){3,}$"
)

# The ATX heading a text written in HTML never carries, and the block tags a
# text written in Markdown rarely does: between them they decide the form.
ATX_LINE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)", re.MULTILINE)
BLOCK_TAG = re.compile(r"<(?:h[1-6]|p)\b[^>]*>", re.IGNORECASE)

# An HTML element that stands as a block of its own, and the kind it is read
# as. A block nested inside one of these belongs to it: a paragraph inside a
# blockquote is the blockquote's text, not a paragraph of the article.
HTML_BLOCKS = {
    "h1": Kind.HEADING,
    "h2": Kind.HEADING,
    "h3": Kind.HEADING,
    "h4": Kind.HEADING,
    "h5": Kind.HEADING,
    "h6": Kind.HEADING,
    "p": Kind.PARAGRAPH,
    "pre": Kind.CODE,
    "ul": Kind.OTHER,
    "ol": Kind.OTHER,
    "dl": Kind.OTHER,
    "blockquote": Kind.OTHER,
    "table": Kind.OTHER,
    "figure": Kind.OTHER,
}

# The frontmatter delimiters, either of which closes a block YAML header.
DELIMITERS = ("---", "...")


class Unmeasurable(RuntimeError):
    """A text this script reports no figures for, carrying the reason's code."""

    def __init__(self, code: Code, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Block:
    """One block of the text, its *text* already reduced to what is visible.

    Nothing downstream has to know which form the block was written in, which
    is what lets an HTML text and its Markdown twin answer the same way.
    """

    kind: Kind
    text: str
    level: int | None = None


@dataclass
class Section:
    """A subheading and everything under it, up to the next subheading."""

    subheading: Block
    paragraphs: list[Block] = field(default_factory=list)


def collapse(text: str) -> str:
    """Return *text* as one normalised run of words.

    Whitespace is collapsed because the reader never sees where a source line
    ended, and the result is normalised to NFC because a decomposed `ä` is two
    code points and one letter.
    """

    return unicodedata.normalize("NFC", " ".join(text.split()))


def plain(text: str) -> str:
    """Return the text a reader sees where *text* is Markdown."""

    text = CODE_SPAN.sub(r"\g<code>", text)
    text = IMAGE.sub("", text)
    text = LINK.sub(r"\1", text)
    text = REFERENCE.sub(r"\1", text)
    text = AUTOLINK.sub(r"\1", text)
    for pattern in EMPHASIS:
        text = pattern.sub(r"\1", text)
    text = TAG.sub("", text)
    text = ESCAPE.sub(r"\1", text)

    return collapse(unescape(text))


def words(text: str) -> list[str]:
    """Return the words of *text*: tokens holding at least one letter or digit."""

    return [token for token in text.split() if any(sign.isalnum() for sign in token)]


def sentences(text: str) -> int:
    """Return how many sentences *text* is estimated to hold.

    Only *most* rests on this figure, and every splitter mistakes an
    abbreviation for a sentence end, so the answer is reported as an estimate
    wherever it is reported at all.
    """

    return len([part for part in SENTENCE.split(text) if part.strip()])


def opening(text: str) -> str:
    """Return enough of *text* for a Skill to recognise which passage is meant."""

    found = text.split()
    if len(found) <= OPENING_WORDS:
        return text
    return " ".join(found[:OPENING_WORDS]) + " …"


def read(source: str) -> str:
    """Return the text *source* names, reading stdin where it is `-`."""

    if source == "-":
        try:
            text = sys.stdin.read()
        except (OSError, UnicodeDecodeError) as exc:
            raise Unmeasurable(
                Code.UNREADABLE_INPUT, f"standard input could not be read: {exc}"
            ) from exc
    else:
        path = Path(source)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise Unmeasurable(
                Code.UNREADABLE_INPUT, f"{path}: could not be read: {exc}"
            ) from exc

    return text.lstrip("﻿").replace("\r\n", "\n").replace("\r", "\n")


def body_of(text: str) -> str:
    """Return *text* with any leading YAML frontmatter removed.

    The frontmatter is skipped rather than parsed: what a `kntnt` map holds is
    the Skill's business, and everything else in a header belongs to whoever
    wrote the document. An unclosed header is no header, and is measured.
    """

    lines = text.split("\n")
    if not lines or lines[0].strip() != DELIMITERS[0]:
        return text

    for index in range(1, len(lines)):
        if lines[index].strip() in DELIMITERS:
            return "\n".join(lines[index + 1 :])

    return text


def detect(body: str) -> Form:
    """Return the form *body* is written in.

    An ATX heading line decides for Markdown wherever it stands, because a
    Markdown text may carry a raw HTML block and an HTML document never carries
    a heading written with a hash.
    """

    if BLOCK_TAG.search(body) and not ATX_LINE.search(body):
        return Form.HTML
    return Form.MARKDOWN


def markdown_blocks(body: str) -> list[Block]:
    """Return every block of a Markdown text, in the order the reader meets it."""

    lines = body.split("\n")
    blocks: list[Block] = []
    index = 0
    while index < len(lines):
        line = lines[index]

        # Blank lines separate blocks and are nothing themselves.
        if not line.strip():
            index += 1
            continue

        # A fenced block runs to its closing fence whatever it holds, which is
        # why it is read before anything inside it can be mistaken for a block.
        fence = FENCE.match(line)
        if fence is not None:
            marker = fence.group(1)
            index += 1
            while index < len(lines) and not lines[index].strip().startswith(marker):
                index += 1
            index += 1
            blocks.append(Block(kind=Kind.CODE, text=""))
            continue

        # An ATX heading is one line and needs no run gathered for it.
        heading = ATX.match(line)
        if heading is not None:
            blocks.append(
                Block(
                    kind=Kind.HEADING,
                    text=plain(heading.group(2) or ""),
                    level=len(heading.group(1)),
                )
            )
            index += 1
            continue

        # Everything else runs until a blank line, a heading, a fence, or the
        # underline that turns the run itself into a heading.
        start = index
        while index < len(lines):
            current = lines[index]
            if not current.strip():
                break
            if index > start and (ATX.match(current) or FENCE.match(current)):
                break
            index += 1
            if index - start > 1 and SETEXT.match(lines[index - 1]):
                break
        chunk = lines[start:index]

        # A run of prose underlined with `=` or `-` is a heading in the other
        # spelling Markdown has for one.
        underline = SETEXT.match(chunk[-1]) if len(chunk) > 1 else None
        if underline is not None and not NOT_PROSE.match(chunk[0]):
            blocks.append(
                Block(
                    kind=Kind.HEADING,
                    text=plain("\n".join(chunk[:-1])),
                    level=1 if underline.group(1).startswith("=") else 2,
                )
            )
            continue

        kind = Kind.OTHER if NOT_PROSE.match(chunk[0]) else Kind.PARAGRAPH
        blocks.append(Block(kind=kind, text=plain("\n".join(chunk))))

    return blocks


class HtmlBlocks(HTMLParser):
    """Collect an HTML document's blocks, ignoring everything nested in one."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.tag: str | None = None
        self.depth = 0
        self.buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Inside a block, only the same tag nesting matters: everything else is
        # that block's own content.
        if self.tag is not None:
            if tag == self.tag:
                self.depth += 1
            return

        if tag in HTML_BLOCKS:
            self.tag = tag
            self.depth = 1
            self.buffer = []
        elif tag == "img":
            self.blocks.append(Block(kind=Kind.OTHER, text=""))

    def handle_endtag(self, tag: str) -> None:
        if self.tag is None or tag != self.tag:
            return
        self.depth -= 1
        if self.depth == 0:
            self.close_block(tag)

    def handle_data(self, data: str) -> None:
        if self.tag is not None:
            self.buffer.append(data)

    def handle_comment(self, data: str) -> None:
        # A comment inside a block is the block's markup rather than a block;
        # one standing on its own is what WordPress writes around each of them.
        if self.tag is None:
            self.blocks.append(Block(kind=Kind.OTHER, text=collapse(data)))

    def close_block(self, tag: str) -> None:
        """Record the block *tag* opened and start looking for the next one."""

        kind = HTML_BLOCKS[tag]
        self.blocks.append(
            Block(
                kind=kind,
                text=collapse("".join(self.buffer)),
                level=int(tag[1]) if kind is Kind.HEADING else None,
            )
        )
        self.tag = None
        self.depth = 0
        self.buffer = []


def html_blocks(body: str) -> list[Block]:
    """Return every block of an HTML text, in the order the reader meets it."""

    parser = HtmlBlocks()
    parser.feed(body)
    parser.close()

    # A document whose last block was never closed is still a document, and the
    # block it ends on is still text the reader sees.
    if parser.tag is not None:
        parser.close_block(parser.tag)

    return parser.blocks


def is_byline(block: Block) -> bool:
    """Return whether *block* has the shape a byline has.

    Shape and position rather than a prefix, for the reason ADR-0209 records:
    a prefix table reaches `By …` and `Text: …` and reports every convention it
    was not told about as a missing byline.
    """

    if block.kind is not Kind.PARAGRAPH:
        return False
    if len(words(block.text)) > BYLINE_WORDS:
        return False
    return not block.text.endswith(TERMINAL)


@dataclass
class Front:
    """Everything between the headline and the first subheading, read apart."""

    standfirst: list[Block] = field(default_factory=list)
    byline: Block | None = None
    lead: list[Block] = field(default_factory=list)
    strays: list[tuple[str, Block]] = field(default_factory=list)


@dataclass
class Reading:
    """What the text was read as: each part, and where every other block sat."""

    headline: Block | None = None
    extra_headlines: list[Block] = field(default_factory=list)
    headline_is_first: bool = True
    deeper: list[Block] = field(default_factory=list)
    front: Front = field(default_factory=Front)
    sections: list[Section] = field(default_factory=list)
    strays: list[tuple[str, Block]] = field(default_factory=list)


def read_the_front(blocks: list[Block], headline_at: int | None) -> Front:
    """Return the standfirst, the byline and the lead *blocks* hold.

    *blocks* is everything before the first level-2 heading, in order, and
    *headline_at* is where the headline stands among them. Every block that is
    neither heading nor paragraph comes back under the position it actually
    sits in, or under `front` where no byline says which side of it that is.
    """

    paragraphs = [
        (at, block) for at, block in enumerate(blocks) if block.kind is Kind.PARAGRAPH
    ]
    byline_at = next((at for at, block in paragraphs if is_byline(block)), None)

    front = Front()
    if byline_at is None:
        found = [block for _, block in paragraphs]
        front.standfirst = found[:1]
        front.lead = found[1:]
    else:
        front.byline = blocks[byline_at]
        front.standfirst = [block for at, block in paragraphs if at < byline_at]
        front.lead = [block for at, block in paragraphs if at > byline_at]

    # A stray block is placed by where it stands, and by nothing weaker than
    # that: with no byline to divide the region, `front` is the whole of what
    # is known about it.
    for at, block in enumerate(blocks):
        if block.kind is Kind.PARAGRAPH or block.kind is Kind.HEADING:
            continue
        if headline_at is not None and at < headline_at:
            front.strays.append((Part.BEFORE_HEADLINE, block))
        elif byline_at is None:
            front.strays.append((Part.FRONT, block))
        elif at > byline_at:
            front.strays.append((Part.LEAD, block))
        else:
            front.strays.append((Part.STANDFIRST, block))

    return front


def read_structure(blocks: list[Block]) -> Reading:
    """Return what each block is, by its kind and its position.

    Position is judged among the headings and the paragraphs, so a comment or
    an image in front of the headline is reported where it sits and displaces
    nothing.
    """

    headings = [block for block in blocks if block.kind is Kind.HEADING]
    level_one = [block for block in headings if block.level == 1]
    prose = [block for block in blocks if block.kind in {Kind.HEADING, Kind.PARAGRAPH}]

    reading = Reading(
        headline=level_one[0] if level_one else None,
        extra_headlines=level_one[1:],
        headline_is_first=bool(level_one) and prose[0] is level_one[0],
        deeper=[
            block for block in headings if block.level is not None and block.level > 2
        ],
    )

    # The front of the text is everything before the first subheading, which is
    # where the headline stands too unless the text put it out of order.
    boundary = next(
        (
            at
            for at, block in enumerate(blocks)
            if block.kind is Kind.HEADING and block.level == 2
        ),
        len(blocks),
    )
    front = blocks[:boundary]
    headline_at = next(
        (at for at, block in enumerate(front) if block is reading.headline), None
    )
    reading.front = read_the_front(front, headline_at)

    # Each level-2 heading opens a section that runs to the next one. Which of
    # them is the ending is not read here: only that there are enough of them
    # for the ending to be one of its own is counted.
    for block in blocks[boundary:]:
        if block.kind is Kind.HEADING and block.level == 2:
            reading.sections.append(Section(subheading=block))
            continue
        if block.kind is Kind.HEADING:
            continue
        if block.kind is Kind.PARAGRAPH:
            reading.sections[-1].paragraphs.append(block)
        else:
            reading.strays.append((section_part(len(reading.sections)), block))

    return reading


def section_part(number: int) -> str:
    """Return the name a section is reported under."""

    return f"section {number}"


def entry(part: str, rule: str, measured: str, text: str | None) -> dict[str, Any]:
    """Return one reported requirement failure or norm departure."""

    return {"part": part, "rule": rule, "measured": measured, "text": text}


def first_word(text: str) -> str:
    """Return the first word of *text*, as a reader would say it aloud."""

    found = words(text)
    if not found:
        return ""
    return found[0].strip(".,:;!?\"'”“’«»()[]–—-…").casefold()


def total_words(blocks: list[Block]) -> int:
    """Return how many words *blocks* hold between them."""

    return sum(len(words(block.text)) for block in blocks)


def requirements(reading: Reading) -> list[dict[str, Any]]:
    """Return every counted requirement the text fails, in the anatomy's order."""

    failures: list[dict[str, Any]] = []
    front = reading.front

    # The headline: that there is one, that there is only one, that it stands
    # first, and that it is the length the anatomy fixes.
    if reading.headline is None:
        failures.append(entry(Part.HEADLINE, HEADLINE_IS_A_HEADING, "absent", None))
    else:
        if reading.extra_headlines:
            failures.append(
                entry(
                    Part.HEADLINE,
                    ONCE,
                    f"{len(reading.extra_headlines) + 1} level-1 headings",
                    reading.extra_headlines[0].text,
                )
            )
        if not reading.headline_is_first:
            failures.append(
                entry(
                    Part.HEADLINE,
                    ORDER,
                    "not the first block",
                    reading.headline.text,
                )
            )
        count = len(reading.headline.text)
        low, high = HEADLINE_CHARACTERS
        if not low <= count <= high:
            failures.append(
                entry(
                    Part.HEADLINE,
                    HEADLINE_LIMIT,
                    f"{count} characters",
                    reading.headline.text,
                )
            )

    # The standfirst: present, one paragraph, and inside its word limit, which
    # is measured over everything the standfirst turned out to hold.
    if not front.standfirst:
        failures.append(entry(Part.STANDFIRST, ORDER, "absent", None))
    else:
        if len(front.standfirst) > 1:
            failures.append(
                entry(
                    Part.STANDFIRST,
                    STANDFIRST_ONE_PARAGRAPH,
                    f"{len(front.standfirst)} paragraphs",
                    opening(front.standfirst[0].text),
                )
            )
        count = total_words(front.standfirst)
        if count > STANDFIRST_WORDS:
            failures.append(
                entry(
                    Part.STANDFIRST,
                    STANDFIRST_WORD_LIMIT,
                    f"{count} words",
                    opening(front.standfirst[0].text),
                )
            )

    if front.byline is None:
        failures.append(entry(Part.BYLINE, ORDER, "absent", None))

    # The lead: present, and exactly one paragraph, so that the first
    # subheading follows it directly.
    if not front.lead:
        failures.append(entry(Part.LEAD, ORDER, "absent", None))
    elif len(front.lead) > 1:
        failures.append(
            entry(
                Part.LEAD,
                LEAD_IS_ONE_PARAGRAPH,
                f"{len(front.lead)} paragraphs",
                opening(front.lead[0].text),
            )
        )

    # The sections: present, and more than one, since the ending is a section
    # of its own after at least one other. Whether the last one closes the
    # piece is a judgement, and not made here.
    if not reading.sections:
        failures.append(entry(Part.SECTIONS, ORDER, "absent", None))
    elif len(reading.sections) == 1:
        failures.append(
            entry(
                Part.SECTIONS,
                ENDING_IS_A_SECTION,
                "1 section",
                reading.sections[0].subheading.text,
            )
        )

    # Each section: a subheading inside its limit, and something under it.
    for number, section in enumerate(reading.sections, start=1):
        count = len(section.subheading.text)
        if count > SUBHEADING_CHARACTERS:
            failures.append(
                entry(
                    section_part(number),
                    SUBHEADING_LIMIT,
                    f"{count} characters",
                    section.subheading.text,
                )
            )
        if not section.paragraphs:
            failures.append(
                entry(
                    section_part(number),
                    SECTION_HOLDS_A_PARAGRAPH,
                    "0 paragraphs",
                    section.subheading.text,
                )
            )

    return failures


def norms(reading: Reading) -> list[dict[str, Any]]:
    """Return every *should* the text departs from, judging none of them."""

    departures: list[dict[str, Any]] = []
    front = reading.front

    # The headline's two norms, each carrying the statement it rests on rather
    # than the sentence both of them were written in.
    if reading.headline is not None:
        text = reading.headline.text
        count = len(words(text))
        low, high = HEADLINE_NORM_WORDS
        if not low <= count <= high:
            departures.append(
                entry(Part.HEADLINE, HEADLINE_NORM_WORDING, f"{count} words", text)
            )
        if len(text) > HEADLINE_NORM_CHARACTERS:
            departures.append(
                entry(
                    Part.HEADLINE, HEADLINE_NORM_LENGTH, f"{len(text)} characters", text
                )
            )

    # A heading the text nests deeper than the two levels the anatomy uses.
    for heading in reading.deeper:
        departures.append(
            entry(Part.SECTIONS, TWO_LEVELS, f"level {heading.level}", heading.text)
        )

    # The standfirst and the lead each work without the other, and a reader
    # meeting the same first word twice meets the standfirst said again.
    if front.standfirst and front.lead:
        opener = first_word(front.standfirst[0].text)
        if opener and opener == first_word(front.lead[0].text):
            departures.append(
                entry(
                    Part.LEAD,
                    DIFFERENT_FIRST_WORDS,
                    f"both open on “{opener}”",
                    opening(front.lead[0].text),
                )
            )

    # A paragraph past the outer edge, wherever in the text it stands, reported
    # under the part it belongs to rather than under the nearest one.
    for part, paragraphs in (
        (Part.STANDFIRST, front.standfirst[1:]),
        (Part.LEAD, front.lead),
        *(
            (section_part(number), section.paragraphs)
            for number, section in enumerate(reading.sections, start=1)
        ),
    ):
        for paragraph in paragraphs:
            count = len(words(paragraph.text))
            if count > PARAGRAPH_NORM_WORDS:
                departures.append(
                    entry(
                        part, PARAGRAPH_NORM, f"{count} words", opening(paragraph.text)
                    )
                )

    # A section carrying more than the anatomy says most sections carry.
    for number, section in enumerate(reading.sections, start=1):
        if len(section.paragraphs) > SECTION_NORM_PARAGRAPHS:
            departures.append(
                entry(
                    section_part(number),
                    SECTION_NORM,
                    f"{len(section.paragraphs)} paragraphs",
                    section.subheading.text,
                )
            )

    return departures


def all_paragraphs(reading: Reading) -> list[Block]:
    """Return every paragraph the text holds, in reading order."""

    return [
        *reading.front.standfirst,
        *reading.front.lead,
        *(block for section in reading.sections for block in section.paragraphs),
    ]


def typical(reading: Reading) -> dict[str, int]:
    """Return the text-wide figures *most* is read against, concluding nothing."""

    paragraphs = all_paragraphs(reading)
    low, high = TYPICAL
    return {
        "paragraphs": len(paragraphs),
        "paragraphs_of_two_or_three_sentences": len(
            [block for block in paragraphs if low <= sentences(block.text) <= high]
        ),
        "sections": len(reading.sections),
        "sections_of_two_or_three_paragraphs": len(
            [
                section
                for section in reading.sections
                if low <= len(section.paragraphs) <= high
            ]
        ),
    }


def heading_figures(block: Block) -> dict[str, Any]:
    """Return one headline or subheading as it was measured."""

    return {
        "text": block.text,
        "characters": len(block.text),
        "words": len(words(block.text)),
    }


def paragraph_figures(block: Block) -> dict[str, Any]:
    """Return one paragraph as it was measured, by its opening words."""

    return {
        "text": opening(block.text),
        "words": len(words(block.text)),
        "sentences_estimate": sentences(block.text),
    }


def opening_part(blocks: list[Block]) -> dict[str, Any] | None:
    """Return the standfirst or the lead, whose figures cover all it holds."""

    if not blocks:
        return None
    return {
        "text": opening(blocks[0].text),
        "words": total_words(blocks),
        "sentences_estimate": sum(sentences(block.text) for block in blocks),
        "paragraphs": len(blocks),
    }


def heading_pair(
    identity: str, kind: str, heading: str | None, following: str | None
) -> dict[str, Any]:
    """Keep visible text beside shared words, without an editorial verdict."""

    # Lexical evidence has its own tokenizer; dimension counts stay unchanged.
    shared = None
    if heading is not None and following is not None:
        left, right = (
            set(re.findall(r"[^\W_]+", unicodedata.normalize("NFC", text.casefold())))
            for text in (heading, following)
        )
        shared = sorted(left & right)

    return {
        "id": identity,
        "kind": kind,
        "heading": heading,
        "following": following,
        "shared_words": shared,
    }


def first_sentence_after(blocks: list[Block], heading_at: int) -> str | None:
    """Estimate the first prose sentence before the next heading of any level."""

    for block in blocks[heading_at + 1 :]:
        if block.kind is Kind.HEADING:
            return None
        if block.kind is Kind.PARAGRAPH:
            if not words(block.text):
                return None
            boundary = SENTENCE.search(block.text)
            return block.text[: boundary.end()].rstrip() if boundary else block.text

    return None


def heading_pairs(reading: Reading, blocks: list[Block]) -> list[dict[str, Any]]:
    """Expose the headline and each section's opening for semantic judgment."""

    pairs = [
        heading_pair(
            "headline-standfirst",
            "headline-standfirst",
            reading.headline.text if reading.headline is not None else None,
            "\n\n".join(block.text for block in reading.front.standfirst) or None,
        )
    ]
    for at, block in enumerate(blocks):
        if block.kind is not Kind.HEADING or block.level == 1:
            continue
        pairs.append(
            heading_pair(
                f"subheading-{len(pairs)}",
                "subheading-first-sentence-estimate",
                block.text,
                first_sentence_after(blocks, at),
            )
        )

    return pairs


def parts(reading: Reading) -> dict[str, Any]:
    """Return what the script took as which part, and what each one measured."""

    front = reading.front
    return {
        Part.HEADLINE: (
            heading_figures(reading.headline) if reading.headline is not None else None
        ),
        Part.STANDFIRST: opening_part(front.standfirst),
        Part.BYLINE: (
            {"text": front.byline.text, "words": len(words(front.byline.text))}
            if front.byline is not None
            else None
        ),
        Part.LEAD: opening_part(front.lead),
        Part.SECTIONS: [
            {
                "subheading": heading_figures(section.subheading),
                "paragraphs": [
                    paragraph_figures(block) for block in section.paragraphs
                ],
            }
            for section in reading.sections
        ],
        "other": [
            {"part": where, "text": opening(block.text)}
            for where, block in (*front.strays, *reading.strays)
        ],
    }


def measure(text: str) -> dict[str, Any]:
    """Return the complete measurement of *text*."""

    body = body_of(text)
    if not body.strip():
        raise Unmeasurable(
            Code.EMPTY_TEXT, "there is no text under the frontmatter to measure."
        )

    form = detect(body)
    blocks = html_blocks(body) if form is Form.HTML else markdown_blocks(body)
    if not any(block.kind in {Kind.HEADING, Kind.PARAGRAPH} for block in blocks):
        raise Unmeasurable(
            Code.NO_STRUCTURE,
            f"read as {form}, the text carries no heading and no paragraph.",
        )

    reading = read_structure(blocks)
    failures = requirements(reading)
    return {
        "ok": True,
        "format": form,
        "conforms": not failures,
        "failures": failures,
        "norms": norms(reading),
        "typical": typical(reading),
        "parts": parts(reading),
        "heading_pairs": heading_pairs(reading, blocks),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the measuring script's command line."""

    parser = argparse.ArgumentParser(
        description="Measure the counted limits of the article anatomy in one text."
    )
    parser.add_argument("path", help="the text to measure, or `-` for standard input")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Measure one text and return the verdict as the exit status."""

    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        payload = measure(read(args.path))
    except Unmeasurable as exc:
        refusal = {"ok": False, "code": exc.code, "message": str(exc)}
        print(json.dumps(refusal, indent=2, ensure_ascii=False))
        return UNMEASURED

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return CONFORMS if payload["conforms"] else FAILS


if __name__ == "__main__":
    raise SystemExit(main())
