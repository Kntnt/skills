# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Count what the article anatomy counts, and judge only what a count settles.

`references/editorial/article-anatomy.md` fixes the parts of a text in the
genres `article`, `case-study`, `column` and `opinion`, their order and their
dimensions, and it says that the limits are exact and verified by counting. A
language model counts characters badly, so the counting happens here: Write
measures a draft before its source check, Redline takes every count a finding
reports from this output, and Redline's correction agent measures its own
repair before returning it.

The anatomy gives each statement one of three strengths, and this script keeps
them apart. A plain statement is a **requirement**, and a requirement a count
settles is decided here: each one that fails is reported under `failures` and
the exit status says so. *Should* marks a **norm**, reported under `norms` and
decided by nobody here — whether a departure is better for the reader is the
Skill's judgement. *Most* states what is typical across the whole text, so no
single paragraph or section can fail it; the figures it rests on are reported
under `typical` and nothing is concluded from them. Everything else stays the
Skill's too: whether a part does its job, whether the ending calls the reader
to action, and how a headline is written.

## The command line

    uv run --no-cache --no-project article_anatomy.py [--format=auto|markdown|html] <path>

`<path>` may be `-`, which reads the text from standard input, so a
response-targeted run needs no scratch file. `auto` reads the text as HTML
where it carries block tags (`<h1>`-`<h6>`, `<p>`) and no ATX heading line, and
as Markdown otherwise.

## The exit status is the verdict

`0` measured, and every requirement holds. `1` measured, and at least one
requirement fails. `2` not measured — an unreadable path, an empty text, or a
text carrying no heading and no paragraph in either form. All three print one
JSON object on stdout. A refusal carries `ok: false`, a stable `code`
(`unreadable-input`, `empty-text`, `no-structure`) and a `message`; an invalid
command line is `argparse`'s own refusal on stderr, as in the Library's other
engines.

## What is measured, and how

Leading YAML frontmatter is skipped and never parsed: a `kntnt` map is
configuration rather than text. What remains is read as blocks in order.

The headline is the level-1 heading. None, more than one, and one that is not
the first heading-or-paragraph block are each a requirement failure; a block
that is neither heading nor paragraph enters no limit, so a WordPress block
comment standing in front of the headline displaces nothing.

Between the headline and the first level-2 heading lie the standfirst, the
byline and the lead. The byline is found by shape and position rather than by
prefix, because a prefix rule reaches `By …` and `Text: …` and reports every
other language's convention missing: it is the first paragraph there that is a
single line of at most twelve words and does not end in `.`, `!`, `?` or `…`.
Paragraphs before it are the standfirst, paragraphs after it the lead. Where no
paragraph has that shape the byline is reported missing, the first paragraph is
taken as the standfirst and the rest as the lead. Each part reports the text it
was read from, so a Skill can overrule a wrong guess.

Each level-2 heading opens a section running to the next one, and the last
section is the ending.

Text is measured as the reader sees it. Markdown emphasis, code and link syntax
is stripped, HTML is reduced to its text with entities decoded, whitespace is
collapsed and the result normalised to NFC. A Markdown heading is ATX (`#`).
Characters are code points, spaces included. A word is a whitespace-separated
token holding at least one letter or digit, so a lone dash is no word.
Sentences are split on terminal punctuation and are always reported as
`sentences_estimate`, because only *most* rests on them and an abbreviation
ends a sentence as far as any splitter can tell.

## The shape of the answer

`ok`, `format`, `conforms`, `failures`, `norms`, `typical` and `parts`.

A `failures` or `norms` entry carries `part` (`headline`, `standfirst`,
`byline`, `lead`, `sections`, or `section <n>`), `rule` in the anatomy's own
words, `measured` as a figure in words, and `text`, which is the text measured
or `null` where the part is absent.

`typical` carries `paragraphs`, `paragraphs_of_two_or_three_sentences`,
`sections` and `sections_of_two_or_three_paragraphs`.

`parts` carries `headline`, `standfirst`, `byline`, `lead`, `sections` and
`other`. A measured text carries `text` — the whole of it for a headline, a
byline and a subheading, and its opening words for a paragraph — with
`characters` and `words` as the anatomy counts that part, and a paragraph
carries `words` and `sentences_estimate` beside them. `standfirst` and `lead`
also carry `paragraphs`, since a part that should be one paragraph can arrive
as two. A part nothing was found for is `null`. Each entry of `sections`
carries its `subheading` and its `paragraphs`. `other` holds every block that
is neither heading nor paragraph, each with its `kind`, the `part` it sits in,
and its opening `text`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, ClassVar

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

# The anatomy's own words, quoted so that a finding says what was required
# rather than this script's paraphrase of it.
ORDER = "A text conforms when every part is present in the order shown."
ONCE = "Each part appears once, except the section, which repeats."
HEADLINE_IS_A_HEADING = (
    "The headline is the text's level-1 heading (HTML `h1`, Markdown `#`)."
)
HEADLINE_LIMIT = "20-70 characters, spaces included."
HEADLINE_NORM = "It should be three to eight words and at most 60 characters."
STANDFIRST_LIMIT = "One paragraph, at most 60 words."
LEAD_IS_ONE_PARAGRAPH = (
    "The lead is the first paragraph of the body: one paragraph, meeting every"
    " requirement under *Paragraphs*."
)
SUBHEADING_LIMIT = "A subheading is at most 70 characters, spaces included."
SECTION_LIMIT = "A section holds at least one paragraph and should hold at most three."
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

# What the reader sees as the end of a sentence, and what may stand between
# that mark and the space after it.
SENTENCE = re.compile(r"(?<=[.!?…])[\"'”’»)\]]*\s+")
TERMINAL = ("." , "!", "?", "…")

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

# Markdown block syntax. Everything a line can open that is not a paragraph,
# recognised by the one line that opens it.
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
ATX = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]+(.*?))?[ \t]*(?<!\\)#*[ \t]*$")
LIST_ITEM = re.compile(r"^ {0,3}(?:[-*+]|\d{1,9}[.)])(?:[ \t]|$)")
QUOTE = re.compile(r"^ {0,3}>")
INDENTED = re.compile(r"^(?: {4}|\t)")
TABLE_DELIMITER = re.compile(r"^ {0,3}\|?[ :|-]*-[ :|-]*\|[ :|-]*$")
IMAGE_ONLY = re.compile(r"^\s*!\[[^\]]*\]\([^)]*\)\s*$")
THEMATIC = re.compile(r"^ {0,3}(?:([-*_])[ \t]*){3,}$")

# The ATX heading a text written in HTML never carries, and the block tags a
# text written in Markdown rarely does: between them they decide the form.
ATX_LINE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]|$)", re.MULTILINE)
BLOCK_TAG = re.compile(r"<(?:h[1-6]|p)\b[^>]*>", re.IGNORECASE)

# An HTML element that stands as a block of its own, and the kind it is
# reported as. A block nested inside one of these belongs to it: a paragraph
# inside a blockquote is the blockquote's text, not a paragraph of the article.
HTML_BLOCKS = {
    "h1": "heading",
    "h2": "heading",
    "h3": "heading",
    "h4": "heading",
    "h5": "heading",
    "h6": "heading",
    "p": "paragraph",
    "ul": "list",
    "ol": "list",
    "dl": "list",
    "blockquote": "blockquote",
    "pre": "code",
    "table": "table",
    "figure": "image",
}

# The frontmatter delimiters, either of which closes a block YAML header.
DELIMITERS = ("---", "...")


class Unmeasurable(RuntimeError):
    """A text this script will not report figures for, and the reason."""

    code: ClassVar[str] = "unmeasurable"


class UnreadableInput(Unmeasurable):
    """The text could not be read from where it was said to be."""

    code: ClassVar[str] = "unreadable-input"


class EmptyText(Unmeasurable):
    """There is nothing under the frontmatter to measure."""

    code: ClassVar[str] = "empty-text"


class NoStructure(Unmeasurable):
    """Neither form could be read: no heading and no paragraph anywhere."""

    code: ClassVar[str] = "no-structure"


@dataclass(frozen=True)
class Block:
    """One block of the text, as the reader meets it.

    *text* is already reduced to what is visible, so nothing downstream has to
    know which form the block was written in. *lines* counts the line breaks
    the reader sees rather than the ones the source happens to carry, which is
    what lets an HTML byline and its Markdown twin answer the same way.
    """

    kind: str
    text: str
    lines: int = 1
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


def characters(text: str) -> int:
    """Return the length of *text* in code points, spaces included."""

    return len(text)


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
            raise UnreadableInput(f"standard input could not be read: {exc}") from exc
    else:
        path = Path(source)
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise UnreadableInput(f"{path}: could not be read: {exc}") from exc

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


def detect(body: str) -> str:
    """Return the form *body* is written in.

    An ATX heading line decides for Markdown wherever it stands, because a
    Markdown text may carry a raw HTML block and an HTML document never carries
    a heading written with a hash.
    """

    if BLOCK_TAG.search(body) and not ATX_LINE.search(body):
        return "html"
    return "markdown"


def kind_of(chunk: list[str]) -> str:
    """Return the kind of a Markdown block from the lines that make it up."""

    first = chunk[0]
    if THEMATIC.match(first):
        return "thematic break"
    if QUOTE.match(first):
        return "blockquote"
    if LIST_ITEM.match(first):
        return "list"
    if INDENTED.match(first):
        return "code"
    if first.lstrip().startswith("<!--"):
        return "comment"
    if first.lstrip().startswith("|") or (
        len(chunk) > 1 and TABLE_DELIMITER.match(chunk[1])
    ):
        return "table"
    if len(chunk) == 1 and IMAGE_ONLY.match(first):
        return "image"
    if first.lstrip().startswith("<"):
        return "raw html"
    return "paragraph"


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
            blocks.append(Block(kind="code", text=""))
            continue

        # An ATX heading is one line and needs no run gathered for it.
        heading = ATX.match(line)
        if heading is not None:
            blocks.append(
                Block(
                    kind="heading",
                    text=plain(heading.group(2) or ""),
                    level=len(heading.group(1)),
                )
            )
            index += 1
            continue

        # Everything else runs until a blank line, a heading, or a fence, each
        # of which closes the paragraph it follows.
        start = index
        while index < len(lines):
            current = lines[index]
            if not current.strip():
                break
            if index > start and (ATX.match(current) or FENCE.match(current)):
                break
            index += 1
        chunk = lines[start:index]
        blocks.append(Block(kind=kind_of(chunk), text=plain("\n".join(chunk)), lines=len(chunk)))

    return blocks


class HtmlBlocks(HTMLParser):
    """Collect an HTML document's blocks, ignoring everything nested in one."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.tag: str | None = None
        self.depth = 0
        self.breaks = 0
        self.buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        # Inside a block, only the same tag nesting and a line break matter:
        # everything else is that block's own content.
        if self.tag is not None:
            if tag == self.tag:
                self.depth += 1
            elif tag == "br":
                self.breaks += 1
            return

        if tag in HTML_BLOCKS:
            self.tag = tag
            self.depth = 1
            self.breaks = 0
            self.buffer = []
        elif tag == "img":
            self.blocks.append(Block(kind="image", text=""))

    def handle_endtag(self, tag: str) -> None:
        if self.tag is None or tag != self.tag:
            return
        self.depth -= 1
        if self.depth == 0:
            self.close_block()

    def handle_data(self, data: str) -> None:
        if self.tag is not None:
            self.buffer.append(data)

    def handle_comment(self, data: str) -> None:
        # A comment inside a block is the block's markup rather than a block;
        # one standing on its own is what WordPress writes around each of them.
        if self.tag is None:
            self.blocks.append(Block(kind="comment", text=collapse(data)))

    def close_block(self) -> None:
        """Record the open block and start looking for the next one."""

        tag = self.tag
        assert tag is not None
        kind = HTML_BLOCKS[tag]
        self.blocks.append(
            Block(
                kind=kind,
                text=collapse("".join(self.buffer)),
                lines=self.breaks + 1,
                level=int(tag[1]) if kind == "heading" else None,
            )
        )
        self.tag = None
        self.depth = 0
        self.breaks = 0
        self.buffer = []


def html_blocks(body: str) -> list[Block]:
    """Return every block of an HTML text, in the order the reader meets it."""

    parser = HtmlBlocks()
    parser.feed(body)
    parser.close()

    # A document whose last block was never closed is still a document, and the
    # block it ends on is still text the reader sees.
    if parser.tag is not None:
        parser.close_block()

    return parser.blocks


def is_byline(block: Block) -> bool:
    """Return whether *block* has the shape a byline has.

    Shape and position rather than a prefix: Swedish writes `Text: …`, `Av …`,
    a bare name or a name and an organisation, English writes `By …`, and a
    rule matching prefixes reports every convention it was not told about as a
    missing byline.
    """

    if block.kind != "paragraph" or block.lines != 1:
        return False
    if len(words(block.text)) > BYLINE_WORDS:
        return False
    return not block.text.endswith(TERMINAL)


@dataclass
class Reading:
    """What the text was read as: each part, and where every other block sat."""

    headline: Block | None = None
    extra_headlines: list[Block] = field(default_factory=list)
    headline_is_first: bool = True
    standfirst: list[Block] = field(default_factory=list)
    byline: Block | None = None
    lead: list[Block] = field(default_factory=list)
    sections: list[Section] = field(default_factory=list)
    other: list[tuple[str, Block]] = field(default_factory=list)
    deeper: list[Block] = field(default_factory=list)


def _front(reading: Reading, blocks: list[Block], where: str) -> None:
    """Read the standfirst, the byline and the lead out of the front blocks."""

    paragraphs = [block for block in blocks if block.kind == "paragraph"]
    found = next((block for block in paragraphs if is_byline(block)), None)

    if found is None:
        reading.standfirst = paragraphs[:1]
        reading.lead = paragraphs[1:]
    else:
        at = paragraphs.index(found)
        reading.byline = found
        reading.standfirst = paragraphs[:at]
        reading.lead = paragraphs[at + 1 :]

    for block in blocks:
        if block.kind != "paragraph" and block.level is None:
            reading.other.append((where, block))


def read_structure(blocks: list[Block]) -> Reading:
    """Return what each block is, by its kind and its position.

    Position is judged among the headings and the paragraphs. A block that is
    neither enters no limit, so a comment or an image in front of the headline
    is reported where it sits and displaces nothing.
    """

    reading = Reading()

    # The headline and where the body starts: everything up to the first
    # level-2 heading belongs to the front of the text.
    front: list[Block] = []
    index = 0
    while index < len(blocks) and not (
        blocks[index].kind == "heading" and blocks[index].level == 2
    ):
        block = blocks[index]
        if block.kind == "heading" and block.level == 1:
            if reading.headline is None:
                reading.headline = block
                reading.headline_is_first = not any(
                    earlier.kind in {"heading", "paragraph"} for earlier in front
                )
            else:
                reading.extra_headlines.append(block)
        elif block.kind == "heading" and block.level is not None and block.level > 2:
            reading.deeper.append(block)
        else:
            front.append(block)
        index += 1

    _front(reading, front, "lead" if reading.headline is not None else "front")

    # Each level-2 heading opens a section that runs to the next one, and the
    # last of them is the ending.
    current: Section | None = None
    for block in blocks[index:]:
        if block.kind == "heading" and block.level == 2:
            current = Section(subheading=block)
            reading.sections.append(current)
            continue
        if current is None:
            continue
        where = f"section {len(reading.sections)}"
        if block.kind == "paragraph":
            current.paragraphs.append(block)
        elif block.kind == "heading":
            if block.level == 1:
                reading.extra_headlines.append(block)
            elif block.level is not None and block.level > 2:
                reading.deeper.append(block)
        else:
            reading.other.append((where, block))

    return reading


def entry(part: str, rule: str, measured: str, text: str | None) -> dict[str, Any]:
    """Return one reported requirement failure or norm departure."""

    return {"part": part, "rule": rule, "measured": measured, "text": text}


def first_word(text: str) -> str:
    """Return the first word of *text*, as a reader would say it aloud."""

    found = words(text)
    if not found:
        return ""
    return found[0].strip(".,:;!?\"'”“’«»()[]–—-…").casefold()


def requirements(reading: Reading) -> list[dict[str, Any]]:
    """Return every counted requirement the text fails, in the anatomy's order."""

    failures: list[dict[str, Any]] = []

    # The headline: that there is one, that there is only one, that it stands
    # first, and that it is the length the anatomy fixes.
    if reading.headline is None:
        failures.append(entry("headline", HEADLINE_IS_A_HEADING, "absent", None))
    else:
        if reading.extra_headlines:
            failures.append(
                entry(
                    "headline",
                    ONCE,
                    f"{len(reading.extra_headlines) + 1} level-1 headings",
                    reading.extra_headlines[0].text,
                )
            )
        if not reading.headline_is_first:
            failures.append(
                entry("headline", ORDER, "not the first block", reading.headline.text)
            )
        count = characters(reading.headline.text)
        low, high = HEADLINE_CHARACTERS
        if not low <= count <= high:
            failures.append(
                entry(
                    "headline",
                    HEADLINE_LIMIT,
                    f"{count} characters",
                    reading.headline.text,
                )
            )

    # The standfirst: present, one paragraph, and inside its word limit.
    if not reading.standfirst:
        failures.append(entry("standfirst", ORDER, "absent", None))
    else:
        if len(reading.standfirst) > 1:
            failures.append(
                entry(
                    "standfirst",
                    STANDFIRST_LIMIT,
                    f"{len(reading.standfirst)} paragraphs",
                    opening(reading.standfirst[0].text),
                )
            )
        count = len(words(reading.standfirst[0].text))
        if count > STANDFIRST_WORDS:
            failures.append(
                entry(
                    "standfirst",
                    STANDFIRST_LIMIT,
                    f"{count} words",
                    opening(reading.standfirst[0].text),
                )
            )

    if reading.byline is None:
        failures.append(entry("byline", ORDER, "absent", None))

    # The lead: present, and exactly one paragraph, so that the first
    # subheading follows it directly.
    if not reading.lead:
        failures.append(entry("lead", ORDER, "absent", None))
    elif len(reading.lead) > 1:
        failures.append(
            entry(
                "lead",
                LEAD_IS_ONE_PARAGRAPH,
                f"{len(reading.lead)} paragraphs",
                opening(reading.lead[0].text),
            )
        )

    if not reading.sections:
        failures.append(entry("sections", ORDER, "absent", None))

    # Each section: a subheading inside its limit, and something under it.
    for number, section in enumerate(reading.sections, start=1):
        count = characters(section.subheading.text)
        if count > SUBHEADING_CHARACTERS:
            failures.append(
                entry(
                    f"section {number}",
                    SUBHEADING_LIMIT,
                    f"{count} characters",
                    section.subheading.text,
                )
            )
        if not section.paragraphs:
            failures.append(
                entry(
                    f"section {number}",
                    SECTION_LIMIT,
                    "0 paragraphs",
                    section.subheading.text,
                )
            )

    return failures


def norms(reading: Reading) -> list[dict[str, Any]]:
    """Return every *should* the text departs from, judging none of them."""

    departures: list[dict[str, Any]] = []

    if reading.headline is not None:
        text = reading.headline.text
        count = len(words(text))
        low, high = HEADLINE_NORM_WORDS
        if not low <= count <= high:
            departures.append(entry("headline", HEADLINE_NORM, f"{count} words", text))
        if characters(text) > HEADLINE_NORM_CHARACTERS:
            departures.append(
                entry(
                    "headline",
                    HEADLINE_NORM,
                    f"{characters(text)} characters",
                    text,
                )
            )

    for heading in reading.deeper:
        departures.append(
            entry("sections", TWO_LEVELS, f"level {heading.level}", heading.text)
        )

    # The standfirst and the lead each work without the other, and a reader
    # meeting the same first word twice meets the standfirst said again.
    if reading.standfirst and reading.lead:
        opener = first_word(reading.standfirst[0].text)
        if opener and opener == first_word(reading.lead[0].text):
            departures.append(
                entry(
                    "lead",
                    DIFFERENT_FIRST_WORDS,
                    f"both open on “{opener}”",
                    opening(reading.lead[0].text),
                )
            )

    for number, section in enumerate(reading.sections, start=1):
        for paragraph in section.paragraphs:
            count = len(words(paragraph.text))
            if count > PARAGRAPH_NORM_WORDS:
                departures.append(
                    entry(
                        f"section {number}",
                        PARAGRAPH_NORM,
                        f"{count} words",
                        opening(paragraph.text),
                    )
                )
        if len(section.paragraphs) > SECTION_NORM_PARAGRAPHS:
            departures.append(
                entry(
                    f"section {number}",
                    SECTION_LIMIT,
                    f"{len(section.paragraphs)} paragraphs",
                    section.subheading.text,
                )
            )

    for paragraph in (*reading.standfirst[1:], *reading.lead):
        count = len(words(paragraph.text))
        if count > PARAGRAPH_NORM_WORDS:
            departures.append(
                entry("lead", PARAGRAPH_NORM, f"{count} words", opening(paragraph.text))
            )

    return departures


def all_paragraphs(reading: Reading) -> list[Block]:
    """Return every paragraph the text holds, in reading order."""

    return [
        *reading.standfirst,
        *reading.lead,
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
        "characters": characters(block.text),
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
    """Return the standfirst or the lead, which should each be one paragraph."""

    if not blocks:
        return None
    figures = paragraph_figures(blocks[0])
    figures["paragraphs"] = len(blocks)
    return figures


def parts(reading: Reading) -> dict[str, Any]:
    """Return what the script took as which part, and what each one measured."""

    return {
        "headline": (
            heading_figures(reading.headline) if reading.headline is not None else None
        ),
        "standfirst": opening_part(reading.standfirst),
        "byline": (
            {
                "text": reading.byline.text,
                "characters": characters(reading.byline.text),
                "words": len(words(reading.byline.text)),
            }
            if reading.byline is not None
            else None
        ),
        "lead": opening_part(reading.lead),
        "sections": [
            {
                "subheading": heading_figures(section.subheading),
                "paragraphs": [
                    paragraph_figures(block) for block in section.paragraphs
                ],
            }
            for section in reading.sections
        ],
        "other": [
            {"kind": block.kind, "part": where, "text": opening(block.text)}
            for where, block in reading.other
        ],
    }


def measure(text: str, form: str) -> dict[str, Any]:
    """Return the complete measurement of *text*, read in *form*."""

    body = body_of(text)
    if not body.strip():
        raise EmptyText("there is no text under the frontmatter to measure.")

    reading_form = detect(body) if form == "auto" else form
    blocks = (
        html_blocks(body) if reading_form == "html" else markdown_blocks(body)
    )
    if not any(block.kind in {"heading", "paragraph"} for block in blocks):
        raise NoStructure(
            f"read as {reading_form}, the text carries no heading and no"
            f" paragraph; name the form with `--format` where it was read as"
            f" the wrong one."
        )

    reading = read_structure(blocks)
    failures = requirements(reading)
    return {
        "ok": True,
        "format": reading_form,
        "conforms": not failures,
        "failures": failures,
        "norms": norms(reading),
        "typical": typical(reading),
        "parts": parts(reading),
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the measuring script's command line."""

    parser = argparse.ArgumentParser(
        description="Measure the counted limits of the article anatomy in one text."
    )
    parser.add_argument("--format", default="auto", choices=("auto", "markdown", "html"))
    parser.add_argument("path", help="the text to measure, or `-` for standard input")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Measure one text and return the verdict as the exit status."""

    args = parse_args(sys.argv[1:] if argv is None else argv)

    try:
        payload = measure(read(args.path), args.format)
    except Unmeasurable as exc:
        refusal = {"ok": False, "code": type(exc).code, "message": str(exc)}
        print(json.dumps(refusal, indent=2, ensure_ascii=False))
        return UNMEASURED

    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return CONFORMS if payload["conforms"] else FAILS


if __name__ == "__main__":
    raise SystemExit(main())
