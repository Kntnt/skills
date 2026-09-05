"""What the re-explaining Skill loses if its perspective drifts toward its sibling's."""

from __future__ import annotations

from pathlib import Path

from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "agents" / "tldr"
BRIEF = REPO_ROOT / "skills" / "agents" / "brief"
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library"


def _mode() -> str:
    """The perspective text the replacement answer is written under."""

    return (SKILL / "references" / "mode.md").read_text(encoding="utf-8")


def test_the_perspective_treats_the_preceding_answer_as_inaccessible() -> None:
    """Correct but pitched at the wrong reader, never bloated.

    The Skill's usual input is text that is long with reason — an article, a
    research answer, a requested explanation, review output, a long design
    discussion. A perspective that read the invocation as a complaint about
    length would answer it by cutting, which is what the sibling Skill already
    does and is not what a reader who did not follow the answer needs.
    """

    text = _mode()

    assert "correct but inaccessible" in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective says the answer"
        f" above is correct but inaccessible. Read as bloated instead, the"
        f" Skill answers by cutting, and the reader who could not follow the"
        f" original gets a shorter version of it. See {STANDARD}."
    )
    assert "pitched at the wrong reader" in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective names what was"
        f" actually wrong with the answer — its reader, not its length. See"
        f" {STANDARD}."
    )
    assert "Re-explain, never compress." in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective forbids satisfying"
        f" the request by rewriting the previous answer's sentences more"
        f" tersely. Compression of a dense answer leaves a denser one. See"
        f" {STANDARD}."
    )


def test_the_perspective_is_additive_where_its_sibling_is_subtractive() -> None:
    """The background the original assumed is the part that has to come back.

    Every rule in the reframing Skill's perspective removes something. This
    reader did not follow the answer, so the need is partly the other way:
    what the original left out is exactly what would have made it legible.
    """

    text = _mode()

    assert "Give the background this work assumed." in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective requires the"
        f" background the original assumed. Leaving it out again reproduces"
        f" the problem the invocation reports. See {STANDARD}."
    )
    assert "Keep established vocabulary; unpack only what is local." in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective keeps ordinary"
        f" technical terms and unpacks what belongs to this work alone. The"
        f" reader is a senior developer who delegated the work, so replacing"
        f" terms they know is condescension that costs the words the"
        f" explanation needs elsewhere. See {STANDARD}."
    )
    assert "senior developer who delegated this work" in text, (
        f"{SKILL / 'references' / 'mode.md'}: the perspective names its reader."
        f" Unnamed, the reader defaults to somebody meeting software for the"
        f" first time, and the rule above turns into a tutorial. See"
        f" {STANDARD}."
    )


def test_the_closing_action_line_is_required_in_its_negative_form_too() -> None:
    """A reply that ends without the line is the failure this Skill exists to avoid.

    The Skill is invoked because the user is not reading closely, so an action
    buried mid-text is an action missed. The line is therefore unconditional:
    where nothing is required of the user, it says that rather than being
    omitted, which is the half a writer drops first.
    """

    surfaces = {
        SKILL / "references" / "mode.md": _mode(),
        SKILL / "SKILL.md": (SKILL / "SKILL.md").read_text(encoding="utf-8"),
        SKILL / "help.md": (SKILL / "help.md").read_text(encoding="utf-8"),
    }

    for where, text in surfaces.items():
        assert "nothing is required of them, say" in text or (
            "nothing is required of them, the closing line says" in text
        ), (
            f"{where}: this surface does not require the closing action line in"
            f" its negative form. An omitted line reads as *nothing needed*"
            f" only to a reader who noticed it was omitted, which is not this"
            f" reader. See {STANDARD}."
        )

    assert "always present" in _mode(), (
        f"{SKILL / 'references' / 'mode.md'}: the perspective says the closing"
        f" line is always present. Conditional, it is written where an action"
        f" is obvious and dropped where it is not. See {STANDARD}."
    )


def test_the_perspective_is_this_skills_own_and_not_the_librarys() -> None:
    """One reader, so no shared store, and no drift toward the sibling's text.

    The Library holds what more than one Skill reads (ADR-0076), and this file
    has a single consumer. The two Skills need different texts, so a copy that
    had converged on the sibling's would be the defect rather than the DRY fix.
    """

    assert (SKILL / "references" / "mode.md").is_file(), (
        f"{SKILL / 'references' / 'mode.md'}: the perspective is a file only"
        f" this Skill opens, so it lives under its own `references/`. See"
        f" {STANDARD}."
    )
    assert not (LIBRARY / "references" / "mode.md").exists(), (
        f"{LIBRARY / 'references' / 'mode.md'}: a file with one reader does not"
        f" belong in the Collection Library. See {STANDARD}."
    )

    brief_body = (BRIEF / "SKILL.md").read_text(encoding="utf-8")
    assert "agents/tldr" not in brief_body, (
        f"{BRIEF / 'SKILL.md'}: the reframing Skill reads its own perspective"
        f" and never a peer's `references/` — peer internals are not an"
        f" interface. See {STANDARD}."
    )
    assert _mode() != (BRIEF / "references" / "mode.md").read_text(encoding="utf-8"), (
        f"{SKILL / 'references' / 'mode.md'}: the two Skills carry the same"
        f" perspective, so one of them is answering the wrong reader. See"
        f" {STANDARD}."
    )


def test_the_grammar_carries_no_command_path_and_no_flag() -> None:
    """What makes bare free text unambiguous here, and the two spellings one thing.

    The separator may be omitted only because there is no verb for prose to
    shadow (ADR-0169). A subcommand page or a declared flag would restore the
    ambiguity, and the operand would have to go in the same change.
    """

    page = (SKILL / "help.md").read_text(encoding="utf-8")
    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert not (SKILL / "help").exists(), (
        f"{SKILL / 'help'}: a page under `help/` is a command path, and a"
        f" command path is a verb the bare operand would shadow. See"
        f" {STANDARD}."
    )
    assert "\n## OPTIONS\n" not in page, (
        f"{SKILL / 'help.md'}: this grammar declares no flag, and a declared"
        f" one would be a token the operand could be mistaken for. See"
        f" {STANDARD}."
    )

    for where, text in ((SKILL / "SKILL.md", body), (SKILL / "help.md", page)):
        assert "/tldr bara säkerhetsdelen" in text and (
            "/tldr -- bara säkerhetsdelen" in text
        ), (
            f"{where}: both spellings of one instruction are written where a"
            f" user reads them, or the shorter one is undocumented behaviour."
            f" See {STANDARD}."
        )

    assert "*INSTRUCTION*" in page.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0]
    assert "\n## POSITIONAL ARGUMENTS\n" in page, (
        f"{SKILL / 'help.md'}: the free text is an operand and takes its own"
        f" slot, which is what documents `/tldr <instruction>` at all. See"
        f" {STANDARD}."
    )


def test_the_range_is_the_preceding_answer_and_never_something_pointed_at() -> None:
    """A pasted document is something to act on, not the thing that was said about it.

    The two degenerate ranges are stated as well: nothing precedes the
    invocation, which is reported rather than answered, and a range compaction
    has truncated, which is reported as truncated rather than passed off as
    complete coverage.
    """

    body = (SKILL / "SKILL.md").read_text(encoding="utf-8")

    assert (
        "never a pasted document, a file, or tool output the user points at" in body
    ), (
        f"{SKILL / 'SKILL.md'}: the range excludes what the user points at."
        f" Without it the Skill becomes a summariser of arbitrary input, which"
        f" is a different Skill with a different contract. See {STANDARD}."
    )
    assert "no preceding answer to explain and stop" in body, (
        f"{SKILL / 'SKILL.md'}: an empty range is reported and nothing is"
        f" written. See {STANDARD}."
    )
    assert "compaction has left the range incomplete" in body, (
        f"{SKILL / 'SKILL.md'}: a range compaction has truncated is stated as"
        f" the limit it is, rather than answered as though it were whole. See"
        f" {STANDARD}."
    )
