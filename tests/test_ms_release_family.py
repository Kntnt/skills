"""Every Claude release the Claude list returns belongs to the family of its line.

Claude Code's answer to `initialize` names most models by a family word —
`opus`, `sonnet`, `haiku` — and some by a full id: on 2026-09-29 one read of it
returned `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`,
`claude-sonnet-4-6`, `claude-fable-5`, `claude-opus-5` and `claude-sonnet-5`
that way, and a read a few minutes earlier returned none of them. The catalogue
pass then took each unknown full id as a family of its own, so the rule keeping
only the newest release of a family could not reach it: five superseded
releases were written 23 subagent definitions, and `claude-sonnet-4-6` was
answered to a `mechanical` call as a Trial (issue #446).

The fixture `catalogue-anthropic-2026-09-29.json` is the eleven Anthropic
entries that pass wrote, exactly as it wrote them, own-id families included.
The lists below are the two shapes the two reads returned, built on the
recorded `initialize` envelope, since the raw list of that day was not kept.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SHIPPED: Path = REPO_ROOT / "skills" / "models" / "model-selector"
FIXTURES: Path = REPO_ROOT / "tests" / "support" / "model_selector_refresh"

# The pass after the one that wrote the fixture, early the next day.
NEXT = datetime(2026, 9, 30, 3, 0, 0, tzinfo=UTC)


def _module(stem: str, name: str | None = None) -> Any:
    """Load one shipped module under the name its siblings import it by."""

    registered = name or stem
    if registered in sys.modules:
        return sys.modules[registered]
    spec = importlib.util.spec_from_file_location(registered, SCRIPTS / f"{stem}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[registered] = module
    spec.loader.exec_module(module)
    return module


catalogue = _module("catalogue")
profiles = _module("profiles")
launch = _module("launch")
evidence = _module("evidence")
_module("quota")
# Registered as the selection tests register it: the file's own name is the
# standard library's `select`.
select = _module("selection", "ms_selection")


@pytest.fixture(autouse=True)
def elsewhere(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point every test at a home of its own, as the selection tests do."""

    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("KNTNT_HOME", raising=False)
    return home


# --- The two lists ----------------------------------------------------------------

EVERY_LEVEL: tuple[str, ...] = ("low", "medium", "high", "xhigh", "max")
NO_XHIGH: tuple[str, ...] = ("low", "medium", "high", "max")

# (value, resolvedModel, supportedEffortLevels) — None for Haiku, which reports
# no levels at all.
Entry = tuple[str, str, tuple[str, ...] | None]

# The five short entries a read returned from one working directory.
SHORT: tuple[Entry, ...] = (
    ("default", "claude-opus-5-5[1m]", EVERY_LEVEL),
    ("opus", "claude-opus-5-5", EVERY_LEVEL),
    ("sonnet", "claude-sonnet-5-5", EVERY_LEVEL),
    ("haiku", "claude-haiku-4-5-20251001", None),
    ("claude-fable-5-1[1m]", "claude-fable-5-1[1m]", EVERY_LEVEL),
)

# The list the pass of 2026-09-29 read, with the seven full ids beside them.
FULL: tuple[Entry, ...] = (
    *SHORT,
    ("claude-sonnet-5", "claude-sonnet-5", EVERY_LEVEL),
    ("claude-opus-5", "claude-opus-5", EVERY_LEVEL),
    ("claude-fable-5", "claude-fable-5", EVERY_LEVEL),
    ("claude-opus-4-8", "claude-opus-4-8", EVERY_LEVEL),
    ("claude-opus-4-7", "claude-opus-4-7", EVERY_LEVEL),
    ("claude-opus-4-6", "claude-opus-4-6", NO_XHIGH),
    ("claude-sonnet-4-6", "claude-sonnet-4-6", NO_XHIGH),
)

# Every release of the eleven a newer release of its own line supersedes.
OLDER: tuple[str, ...] = (
    "claude-fable-5",
    "claude-opus-4-6",
    "claude-opus-4-7",
    "claude-opus-4-8",
    "claude-opus-5",
    "claude-sonnet-4-6",
    "claude-sonnet-5",
)

# The families the five entries written under their own id belong to.
LINES: dict[str, str] = {
    "claude-fable-5": "fable",
    "claude-opus-4-6": "opus",
    "claude-opus-4-7": "opus",
    "claude-opus-4-8": "opus",
    "claude-sonnet-4-6": "sonnet",
}

# The 23 files the pass of 2026-09-29 wrote for the five, which no pass may
# write again.
STRAY: frozenset[str] = frozenset(
    {
        *(f"kntnt-claude-fable-5-{level}.md" for level in EVERY_LEVEL),
        *(f"kntnt-claude-opus-4-6-{level}.md" for level in NO_XHIGH),
        *(f"kntnt-claude-opus-4-7-{level}.md" for level in EVERY_LEVEL),
        *(f"kntnt-claude-opus-4-8-{level}.md" for level in EVERY_LEVEL),
        *(f"kntnt-claude-sonnet-4-6-{level}.md" for level in NO_XHIGH),
    }
)

# What the eleven entries want: one file per level of `claude-fable-5-1`,
# `claude-opus-5-5` and `claude-sonnet-5-5`, and Haiku's one, and no other.
WANTED: frozenset[str] = frozenset(
    {
        *(f"kntnt-fable-{level}.md" for level in EVERY_LEVEL),
        *(f"kntnt-opus-{level}.md" for level in EVERY_LEVEL),
        *(f"kntnt-sonnet-{level}.md" for level in EVERY_LEVEL),
        "kntnt-haiku.md",
    }
)

# Files in the agents directory that this Skill did not write, one of them
# named the way the stray files are but without the prefix.
FOREIGN: dict[str, str] = {
    "my-reviewer.md": "---\nname: my-reviewer\n---\n",
    "claude-opus-4-8-high.md": "---\nname: claude-opus-4-8-high\n---\n",
    "kntnt.md": "not ours either\n",
    "kntnt-notes.txt": "a prefix without the suffix\n",
}


def _messages(entries: Sequence[Entry]) -> list[dict[str, Any]]:
    """Return the recorded `initialize` answer carrying *entries* as its model list."""

    text = (FIXTURES / "claude-initialize.jsonl").read_text(encoding="utf-8")
    messages = [json.loads(line) for line in text.splitlines() if line.strip()]
    answer = next(
        message for message in messages if message.get("type") == "control_response"
    )
    models: list[dict[str, Any]] = []
    for value, resolved, levels in entries:
        model: dict[str, Any] = {
            "value": value,
            "resolvedModel": resolved,
            "displayName": value,
        }
        if levels is not None:
            model["supportsEffort"] = True
            model["supportedEffortLevels"] = list(levels)
        models.append(model)
    answer["response"]["response"]["models"] = models
    return messages


def _families(entries: Sequence[Entry]) -> dict[str, str]:
    """Return the family `claude_reading` gives each release a list offers."""

    reading = catalogue.claude_reading(_messages(entries))
    assert reading.outcome == "complete"
    return {offer.id: offer.family for offer in reading.listed}


# --- The reading ----------------------------------------------------------------


def test_a_release_listed_by_its_full_id_takes_the_family_of_its_line() -> None:
    """A full id beside the family words is a release of the line it names."""

    families = _families(FULL)

    assert families == {
        "claude-opus-5-5": "opus",
        "claude-sonnet-5-5": "sonnet",
        "claude-haiku-4-5-20251001": "haiku",
        "claude-fable-5-1": "fable",
        "claude-sonnet-5": "sonnet",
        "claude-opus-5": "opus",
        "claude-fable-5": "fable",
        "claude-opus-4-8": "opus",
        "claude-opus-4-7": "opus",
        "claude-opus-4-6": "opus",
        "claude-sonnet-4-6": "sonnet",
    }


def test_a_release_nobody_has_seen_yet_takes_the_family_of_its_line() -> None:
    """No table of known releases stands behind the answer."""

    families = _families(
        (
            ("claude-sonnet-5-6", "claude-sonnet-5-6", EVERY_LEVEL),
            ("claude-opus-6", "claude-opus-6[1m]", EVERY_LEVEL),
            ("claude-haiku-5-20270101", "claude-haiku-5-20270101", None),
            ("claude-3-5-sonnet-20241022", "claude-3-5-sonnet-20241022", None),
            ("claude-quill-1", "claude-quill-1", EVERY_LEVEL),
        )
    )

    assert families == {
        "claude-sonnet-5-6": "sonnet",
        "claude-opus-6": "opus",
        "claude-haiku-5-20270101": "haiku",
        "claude-3-5-sonnet-20241022": "sonnet",
        "claude-quill-1": "quill",
    }


def test_a_family_word_is_still_the_family_and_the_value_still_the_alias() -> None:
    """Only the family changes: what the list calls a release stays its alias."""

    reading = catalogue.claude_reading(_messages(FULL))
    offers = {offer.id: offer for offer in reading.listed}

    assert offers["claude-opus-5-5"].aliases == ("opus",)
    assert offers["claude-opus-4-8"].aliases == ("claude-opus-4-8",)
    assert offers["claude-fable-5-1"].aliases == ("claude-fable-5-1",)
    assert offers["claude-opus-4-6"].levels == NO_XHIGH


def test_a_release_whose_line_cannot_be_told_keeps_its_own_id_rather_than_a_guess() -> (
    None
):
    """An id naming no line, or two, is given no family it does not state."""

    families = _families(
        (
            ("claude-5", "claude-5", EVERY_LEVEL),
            ("claude-opus-sonnet-6", "claude-opus-sonnet-6", EVERY_LEVEL),
        )
    )

    assert families == {
        "claude-5": "claude-5",
        "claude-opus-sonnet-6": "claude-opus-sonnet-6",
    }


@pytest.mark.parametrize("word_first", [True, False], ids=["word-first", "id-first"])
def test_a_family_word_for_a_release_whose_id_names_no_line_is_its_family(
    word_first: bool,
) -> None:
    """Whichever entry comes first, the list's own word outranks a family of one."""

    by_word: Entry = ("mythos", "claude-5", EVERY_LEVEL)
    by_id: Entry = ("claude-5", "claude-5", EVERY_LEVEL)

    families = _families((by_word, by_id) if word_first else (by_id, by_word))

    assert families == {"claude-5": "mythos"}


# --- The pass over what the pass of 2026-09-29 wrote --------------------------------


def _fixture() -> dict[str, Any]:
    """Return the eleven Anthropic entries the pass of 2026-09-29 wrote."""

    document: dict[str, Any] = json.loads(
        (FIXTURES / "catalogue-anthropic-2026-09-29.json").read_text(encoding="utf-8")
    )
    return document


def _as_written(tmp_path: Path) -> tuple[Path, Path, Path]:
    """Return a machine standing as the pass of 2026-09-29 left it.

    A seed, a data directory holding a profile choosing Anthropic, the eleven
    entries, a measurement store and a queue of pending Units, and an agents
    directory holding every file that pass left there beside four that are not
    this Skill's.
    """

    here = tmp_path / "skill"
    (here / "data").mkdir(parents=True)
    (here / "data" / "catalogue-seed.json").write_bytes(
        (SHIPPED / "data" / "catalogue-seed.json").read_bytes()
    )
    data = tmp_path / "data"
    data.mkdir()
    (data / "profile.json").write_text(
        json.dumps(
            {
                "harnesses": ["claude-code"],
                "makers": ["anthropic"],
                "channels": [
                    {
                        "provider": "anthropic",
                        "harness": "claude-code",
                        "pay": "subscription",
                        "plan": "Claude Max 20x",
                        "gateway": None,
                        "rates": None,
                    }
                ],
                "answered_at": "2026-09-29T11:00:00Z",
            }
        ),
        encoding="utf-8",
    )
    (data / "catalogue.json").write_text(json.dumps(_fixture()), encoding="utf-8")
    _store(data)
    _queue(data)

    agents = tmp_path / "agents"
    agents.mkdir()
    for name in (*STRAY, *WANTED):
        (agents / name).write_text(f"written 2026-09-29: {name}\n", encoding="utf-8")
    for name, text in FOREIGN.items():
        (agents / name).write_text(text, encoding="utf-8")
    return here, data, agents


def _rows(kind: str, model: str, level: str | None, grade: float, count: int) -> str:
    """Return *count* routed rows of one graded attempt, as the ledger holds them."""

    return "".join(
        json.dumps(
            {
                "attempt_id": f"ms-{kind}-{model}-{level}-{grade}-{index}",
                "at": "2026-09-20T00:00:00Z",
                "kind": kind,
                "model": model,
                "deliberation": level,
                "grade": grade,
                "graded_by": "checker",
                "routed": True,
            }
        )
        + "\n"
        for index in range(count)
    )


def _store(data: Path) -> None:
    """Write a store shaped like the maintainer's: most rows on older releases.

    `mechanical` holds a measured Opus 5.5 that fails a third of the time and a
    long, clean record of Sonnet 5, which makes the newest Sonnet a plausible
    model with nothing of its own — the shape that is owed a Trial. `implement`
    holds measured points of every newest release, so nothing is owed there
    and the exploration's coin is tossed. Every other kind holds nothing at
    all. Sonnet 4.6 and Opus 4.8 hold rows too, which are theirs to keep and
    never a reason to offer them: before the fix, Sonnet 4.6's two rows made
    it the Trial in progress on `mechanical`, as on the maintainer's machine.
    """

    (data / "measurements.jsonl").write_text(
        _rows("mechanical", "claude-opus-5-5", "high", 1.0, 8)
        + _rows("mechanical", "claude-opus-5-5", "high", 0.0, 4)
        + _rows("mechanical", "claude-sonnet-5", "high", 1.0, 40)
        + _rows("mechanical", "claude-sonnet-4-6", "high", 1.0, 2)
        + _rows("implement", "claude-opus-5-5", "xhigh", 1.0, 20)
        + _rows("implement", "claude-opus-5-5", "low", 0.0, 10)
        + _rows("implement", "claude-sonnet-5-5", "high", 0.0, 10)
        + _rows("implement", "claude-fable-5-1", "xhigh", 0.0, 10)
        + _rows("implement", "claude-haiku-4-5-20251001", None, 0.0, 10)
        + _rows("implement", "claude-opus-4-8", "high", 1.0, 1),
        encoding="utf-8",
    )


def _queue(data: Path) -> None:
    """Write pending Units for a newest and an older release alike."""

    (data / "pending.jsonl").write_text(
        "".join(
            json.dumps({"unit_id": f"unit-{model}", "model": model}, sort_keys=True)
            + "\n"
            for model in ("claude-opus-4-8", "claude-sonnet-5", "claude-opus-5-5")
        ),
        encoding="utf-8",
    )


def _pass(
    here: Path, data: Path, agents: Path, entries: Sequence[Entry], now: datetime
) -> dict[str, Any]:
    """Run one pass reading *entries* from Claude, with OpenRouter unreachable.

    OpenRouter is left unread so that nothing but the Claude list moves an
    entry, which is what makes a comparison of every other field meaningful.
    """

    messages = _messages(entries)
    report: dict[str, Any] = catalogue.refresh(
        data,
        here,
        agents,
        now=now,
        readers={
            "claude": lambda started, seconds: catalogue.claude_reading(messages),
            "openrouter": lambda started, seconds: catalogue.unreadable(
                "openrouter", "not reached in this test"
            ),
        },
    )
    return report


def _stored(data: Path) -> dict[str, dict[str, Any]]:
    """Return the stored catalogue's entries by id."""

    document = json.loads((data / "catalogue.json").read_text(encoding="utf-8"))
    return {entry["id"]: entry for entry in document["models"]}


@pytest.mark.parametrize("entries", [FULL, SHORT], ids=["full-list", "short-list"])
def test_the_next_pass_gives_each_entry_written_under_its_own_id_its_line(
    tmp_path: Path, entries: Sequence[Entry]
) -> None:
    """Corrected whichever of the two lists the pass is handed.

    The short list does not name the five at all, and the entries still move:
    what corrects them is their own id, not whether the list happened to
    return it that day.
    """

    here, data, agents = _as_written(tmp_path)
    written = _stored(data)

    _pass(here, data, agents, entries, NEXT)

    stored = _stored(data)
    assert {model: stored[model]["family"] for model in LINES} == LINES
    assert {
        model: {field: value for field, value in entry.items() if field != "family"}
        for model, entry in stored.items()
    } == {
        model: {field: value for field, value in entry.items() if field != "family"}
        for model, entry in written.items()
    }
    families = {
        model: entry["family"] for model, entry in written.items() if model not in LINES
    }
    assert {model: stored[model]["family"] for model in families} == families


@pytest.mark.parametrize("entries", [FULL, SHORT], ids=["full-list", "short-list"])
def test_the_eleven_entries_want_the_files_of_four_releases_and_no_others(
    tmp_path: Path, entries: Sequence[Entry]
) -> None:
    """The 23 files go, the 16 stay, and nothing without the prefix is touched."""

    here, data, agents = _as_written(tmp_path)

    report = _pass(here, data, agents, entries, NEXT)

    assert set(report["definitions"]["removed"]) == STRAY
    assert {path.name for path in agents.iterdir()} == WANTED | set(FOREIGN)
    for name, text in FOREIGN.items():
        assert (agents / name).read_text(encoding="utf-8") == text
    wanted = launch.definitions(
        profiles.load(data, catalogue.load(data, here)), catalogue.load(data, here)
    )
    assert set(wanted) == WANTED
    for name in WANTED:
        assert (agents / name).read_text(encoding="utf-8") == wanted[name]


@pytest.mark.parametrize("entries", [FULL, SHORT], ids=["full-list", "short-list"])
def test_the_correction_deletes_and_rewrites_no_row_and_no_unit(
    tmp_path: Path, entries: Sequence[Entry]
) -> None:
    """The rows of the five are kept, and the newest release reads them as kin."""

    here, data, agents = _as_written(tmp_path)
    rows = (data / "measurements.jsonl").read_bytes()
    units = (data / "pending.jsonl").read_bytes()

    _pass(here, data, agents, entries, NEXT)

    assert (data / "measurements.jsonl").read_bytes() == rows
    assert (data / "pending.jsonl").read_bytes() == units
    kin = [
        release.id
        for release in catalogue.older_releases(
            catalogue.load(data, here), "claude-opus-5-5"
        )
    ]
    assert kin == [
        "claude-opus-5",
        "claude-opus-4-8",
        "claude-opus-4-7",
        "claude-opus-4-6",
    ]


def test_the_correction_is_journalled_once_as_a_change_of_family(
    tmp_path: Path,
) -> None:
    """Each of the five moves once, from its own id to its line, and never again."""

    here, data, agents = _as_written(tmp_path)

    _pass(here, data, agents, FULL, NEXT)
    _pass(here, data, agents, FULL, NEXT.replace(hour=4))

    journal = [
        json.loads(line)
        for line in (data / "catalogue-journal.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    moved = [row for row in journal if row["field"] == "family"]
    assert sorted((row["model"], row["old"], row["new"]) for row in moved) == sorted(
        (model, model, line) for model, line in LINES.items()
    )
    assert {row["source"] for row in moved} == {"claude"}


# --- What selection may name --------------------------------------------------------

# The eight kinds, stated here as the selection tests state them.
VOCABULARY: tuple[str, ...] = (
    "mechanical",
    "implement",
    "design",
    "debug",
    "review",
    "analyze",
    "prose",
    "converse",
)

# The seeds each kind is asked over, at each stakes. A reversible call tosses
# the exploration's coin off its seed, and six of the first sixty seeds land
# it, so every kind that owes no Trial is explored on some of them. A call at
# high stakes draws nothing, so a few seeds are the whole of what it can say.
SEEDS: dict[str, range] = {"reversible": range(60), "high": range(3)}

# The call the maintainer's session made, less the kind and the stakes.
ASKED: tuple[str, ...] = (
    "--scope=callable",
    "--harness=claude-code",
    "--seat=claude-fable-5-1@high",
    "--n=20",
)

OLDER_NAMED = re.compile(
    r"(?<![\w.-])(?:" + "|".join(re.escape(model) for model in OLDER) + r")(?![\w.-])"
)


def _answer(capsys: pytest.CaptureFixture[str], *flags: str) -> dict[str, Any]:
    """Run the selection entry point in process and return the one object it printed."""

    assert select.main(list(flags)) == 0
    printed = capsys.readouterr().out.strip().splitlines()
    assert len(printed) == 1
    parsed: dict[str, Any] = json.loads(printed[0])
    return parsed


def _corrected(tmp_path: Path) -> Path:
    """Return the data directory once the next pass has run over the fixture."""

    here, data, agents = _as_written(tmp_path)
    _pass(here, data, agents, FULL, NEXT)
    return data


def test_no_call_of_any_kind_names_an_older_release_of_any_family(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Not as the answer, not as the point explored or tried, not as an alternative.

    The sweep has to reach both ways a model nobody asked for is tried, or it
    proves nothing about them: it asserts that a Trial and an exploration each
    happened before it asserts what they named.
    """

    data = _corrected(tmp_path)
    offending: list[tuple[str, str, int, str]] = []
    explored: set[str | None] = set()

    for kind in VOCABULARY:
        for stakes, seeds in SEEDS.items():
            for seed in seeds:
                answer = _answer(
                    capsys,
                    f"--data={data}",
                    f"--kind={kind}",
                    f"--stakes={stakes}",
                    f"--seed={seed}",
                    *ASKED,
                )
                explored.add(answer["explored"])
                named = [
                    answer["model"],
                    *(row["model"] for row in answer["alternatives"]),
                    *OLDER_NAMED.findall(json.dumps(answer)),
                ]
                offending.extend(
                    (kind, stakes, seed, model) for model in named if model in OLDER
                )

    assert "trial" in explored
    assert explored - {None, "trial"}
    assert offending == []


def test_an_exact_id_lock_on_an_older_release_is_still_answered_with_it(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The lock runs before the newest-release rule, as it did before the fix."""

    data = _corrected(tmp_path)

    answer = _answer(
        capsys,
        f"--data={data}",
        "--kind=mechanical",
        "--model=claude-sonnet-4-6",
        *ASKED,
    )

    assert answer["model"] == "claude-sonnet-4-6"
    note = answer["note"] or ""
    assert "lock" not in note
    assert "did not offer" not in note


def test_a_family_lock_resolves_to_the_newest_release_of_the_line(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`sonnet` now names three releases, and the newest of them is the answer."""

    data = _corrected(tmp_path)

    answer = _answer(
        capsys, f"--data={data}", "--kind=mechanical", "--model=sonnet", *ASKED
    )

    assert answer["model"] == "claude-sonnet-5-5"
    assert "the lock 'sonnet' names several models; claude-sonnet-5-5 is newest" in (
        answer["note"] or ""
    )


# --- A release whose line cannot be told --------------------------------------------


def test_a_release_whose_line_cannot_be_told_is_reported_by_the_pass_and_journalled_once(
    tmp_path: Path,
) -> None:
    """Said in the pass's own report every pass, and in the journal when it arrives."""

    here, data, agents = _as_written(tmp_path)
    entries = (*FULL, ("claude-5", "claude-5", EVERY_LEVEL))

    first = _pass(here, data, agents, entries, NEXT)
    second = _pass(here, data, agents, entries, NEXT.replace(hour=4))

    assert first["untold"] == ["claude-5"]
    assert second["untold"] == ["claude-5"]
    assert _stored(data)["claude-5"]["family"] == "claude-5"
    journal = [
        json.loads(line)
        for line in (data / "catalogue-journal.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    untold = [row for row in journal if row.get("note") == catalogue.FAMILY_UNTOLD]
    assert [(row["model"], row["field"], row["source"]) for row in untold] == [
        ("claude-5", "family", "claude")
    ]
    shown = catalogue.journal(data, 7, now=NEXT.replace(hour=5))
    assert shown["last_pass"]["untold"] == ["claude-5"]
    assert any(row.get("note") == catalogue.FAMILY_UNTOLD for row in shown["journal"])


def test_a_pass_with_every_line_told_reports_none_untold(tmp_path: Path) -> None:
    """The field is always there, so a reader never has to tell absent from empty."""

    here, data, agents = _as_written(tmp_path)

    report = _pass(here, data, agents, FULL, NEXT)

    assert report["untold"] == []


def test_the_fixture_is_the_catalogue_the_pass_of_2026_09_29_wrote() -> None:
    """Five of its eleven entries carry their own id as their family."""

    entries = {entry["id"]: entry for entry in _fixture()["models"]}

    assert len(entries) == 11
    assert {
        model for model, entry in entries.items() if entry["family"] == model
    } == set(LINES)
    assert all(entry["provider"] == "anthropic" for entry in entries.values())
