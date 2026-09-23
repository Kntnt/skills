"""The weekly windows the quota guard reads, and what it makes of each."""

from __future__ import annotations

import importlib.util
import inspect
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
READER: Path = SCRIPTS / "quota.py"

# The week, in the two units the two sources spell it in.
WEEK_MINUTES: int = 10080
WEEK_SECONDS: int = WEEK_MINUTES * 60

# A fixed instant every fixture is built around, so that a window's pace is
# arithmetic rather than a race against the clock the suite runs on. It is
# 2026-09-21T14:13:20Z, which is what the event timestamps below are near.
NOW: float = 1790000000.0

# An event instant an hour or so before `NOW`, which is what a session that is
# still open looks like, and the day directory Codex would have filed it under.
FRESH: str = "2026-09-21T13:00:00.000Z"
TODAY: str = "2026-09-21"


def _module() -> Any:
    """Load the reader under the name its siblings import it by."""

    if "quota" in sys.modules:
        return sys.modules["quota"]
    spec = importlib.util.spec_from_file_location("quota", READER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["quota"] = module
    spec.loader.exec_module(module)
    return module


quota = _module()


def _written(
    data_dir: Path,
    *,
    used: float = 10.0,
    elapsed: float = 0.5,
    age: float = 60.0,
    harness: str = "claude-code",
    window: int = WEEK_MINUTES,
    at: float = NOW,
) -> Path:
    """Write the file a status line writes, placed at a share of its window.

    *elapsed* is the share of the week gone at *at*, which is what the rule
    compares the used share against, so a fixture states its pace rather than
    an instant somebody has to divide back out.

    *at* is the instant the reader of this fixture will call now. It is `NOW`
    for every test that injects that same instant, and the real clock for the
    one test that runs the reader as a subprocess: that reader takes its own
    now from the clock, and a reading `age` seconds before a frozen constant
    passes its staleness rule only until the constant is a day old.
    """

    data_dir.mkdir(parents=True, exist_ok=True)
    path = data_dir / "quota.json"
    path.write_text(
        json.dumps(
            {
                "channels": {
                    harness: {
                        "used_percent": used,
                        "resets_at": int(at + (1.0 - elapsed) * WEEK_SECONDS),
                        "window_minutes": window,
                        "written_at": int(at - age),
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    return path


def _event(
    *,
    at: str = FRESH,
    used: float = 10.0,
    elapsed: float = 0.5,
    window: int = WEEK_MINUTES,
    limits: bool = True,
) -> str:
    """One `token_count` event, in the nesting Codex actually writes.

    Reduced from a real session log this repository holds under its evaluation
    corpus: `rate_limits` beside `info` under `payload` rather than inside it,
    `plan_type` beside `primary` rather than in it, and `used_percent` a JSON
    number that happens to be whole. The shape is copied here rather than read,
    so no test of this module opens a session log of anybody's.
    """

    payload: dict[str, Any] = {
        "type": "token_count",
        "info": {"total_token_usage": {"total_tokens": 47535}},
    }
    if limits:
        payload["rate_limits"] = {
            "limit_id": "codex",
            "limit_name": None,
            "primary": {
                "used_percent": used,
                "window_minutes": window,
                "resets_at": int(NOW + (1.0 - elapsed) * WEEK_SECONDS),
            },
            "secondary": None,
            "plan_type": "pro",
        }
    return json.dumps({"timestamp": at, "type": "event_msg", "payload": payload})


def _log(root: Path, name: str, *lines: str, day: str = TODAY) -> Path:
    """Write one session log where Codex keeps it, under `YYYY/MM/DD`."""

    directory = root / Path(day.replace("-", "/"))
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"rollout-{name}.jsonl"
    path.write_text("".join(f"{line}\n" for line in lines), encoding="utf-8")
    return path


def _account(data_dir: Path, codex_root: Path, harness: str) -> Any:
    """Return the one account the reader gives for a harness."""

    found = [
        row
        for row in quota.accounts(data_dir, codex_root, now=NOW)
        if row.harness == harness
    ]
    assert len(found) == 1, f"{harness} is reported once, not {len(found)} times"
    return found[0]


# --- the rule, on a figure that is there ----------------------------------


@pytest.mark.parametrize(
    ("used", "elapsed", "expected"),
    [
        (61.0, 0.5, True),  # eleven points ahead of the week
        (60.0, 0.5, False),  # exactly ten ahead, which is not more than ten
        (10.0, 0.5, False),  # far behind the week
        (90.0, 0.99, True),  # at ninety, though the week has nearly gone
        (89.0, 0.99, False),  # below ninety and behind the pace
    ],
)
def test_the_two_thresholds_are_what_hold_a_channel_back(
    tmp_path: Path, used: float, elapsed: float, expected: bool
) -> None:
    """More than ten points ahead of the week, or ninety whatever the pace.

    Both are asked at their own boundary, because a rule written with the
    wrong comparison passes every fixture that is not standing on it.
    """

    _written(tmp_path, used=used, elapsed=elapsed)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is expected
    assert account.used_percent == used
    assert account.elapsed_percent == pytest.approx(elapsed * 100)


def test_an_account_carries_everything_the_report_renders(tmp_path: Path) -> None:
    """The share used and elapsed, the reset instant, the source, and the age.

    `status` renders this account rather than recomputing the rule for the
    report, so every figure that page names is one this reader answers with.
    """

    _written(tmp_path, used=95.0, elapsed=0.5, age=3600.0)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.used_percent == 95.0
    assert account.elapsed_percent == pytest.approx(50.0)
    assert account.resets_at == int(NOW + 0.5 * WEEK_SECONDS)
    assert account.age_seconds == pytest.approx(3600.0)
    assert account.source == quota.WRITTEN
    assert account.held_back is True
    assert account.absent is None


def test_a_window_that_has_barely_opened_is_behind_rather_than_ahead(
    tmp_path: Path,
) -> None:
    """The elapsed share is clamped, so a reset further off than the window is nought."""

    _written(tmp_path, used=0.0, elapsed=-0.5)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.elapsed_percent == 0.0
    assert account.held_back is False


# --- no figure, from the file ---------------------------------------------


def test_an_absent_file_is_no_guard_and_no_error(tmp_path: Path) -> None:
    """Nothing has written one, which is the ordinary state of a fresh machine."""

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.used_percent is None
    assert account.absent == quota.NO_FILE


def test_an_unreadable_file_is_no_guard(tmp_path: Path) -> None:
    """A path that is there and cannot be opened at all."""

    (tmp_path / "quota.json").mkdir(parents=True)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent == quota.UNREADABLE


@pytest.mark.parametrize("document", ["[1, 2, 3]", '{"channels": []}', "not json"])
def test_a_file_in_another_shape_is_no_guard(tmp_path: Path, document: str) -> None:
    """Half-written, hand-edited, or from something that is not this writer."""

    (tmp_path / "quota.json").write_text(document, encoding="utf-8")

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent in {quota.ANOTHER_SHAPE, quota.UNREADABLE}


def test_an_entry_missing_its_members_is_no_guard(tmp_path: Path) -> None:
    """One entry read and one not is the file naming no window for that harness."""

    (tmp_path / "quota.json").write_text(
        json.dumps({"channels": {"claude-code": {"used_percent": 95.0}}}),
        encoding="utf-8",
    )

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent == quota.NOT_NAMED


def test_a_file_naming_another_window_is_no_guard(tmp_path: Path) -> None:
    """The rule is about the week, and any other window is not the week."""

    _written(tmp_path, used=99.0, elapsed=0.1, window=300)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent == quota.NOT_NAMED


def test_a_file_written_more_than_a_day_ago_is_no_guard(tmp_path: Path) -> None:
    """A status line runs on every render, so a day-old figure is nobody's machine.

    On a seven-day window a day of drift is already worth more than the ten
    points the rule turns on, so a stale ninety-five holds nothing back.
    """

    _written(tmp_path, used=95.0, elapsed=0.5, age=25 * 3600.0)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent == quota.STALE


def test_a_file_past_the_reset_it_names_is_no_guard(tmp_path: Path) -> None:
    """The window it describes has gone, so what it says of it is about nothing."""

    _written(tmp_path, used=99.0, elapsed=1.5)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is False
    assert account.absent == quota.PASSED


def test_a_figure_from_a_clock_a_moment_ahead_is_not_stale(tmp_path: Path) -> None:
    """A machine whose clock runs a few seconds fast is an ordinary machine."""

    _written(tmp_path, used=95.0, elapsed=0.5, age=-30.0)

    account = _account(tmp_path, tmp_path / "absent", "claude-code")

    assert account.held_back is True
    assert account.absent is None


# --- the Codex read -------------------------------------------------------


def test_the_codex_figure_is_the_latest_event_across_files(tmp_path: Path) -> None:
    """Concurrent sessions each hold their own last-fetched value.

    So the machine-wide figure is the newest by the event's own timestamp,
    which is neither the file's name nor when it was last written to.
    """

    root = tmp_path / "sessions"
    _log(
        root,
        "older-session",
        _event(at="2026-09-21T10:00:00.000Z", used=12.0),
        _event(at="2026-09-21T13:30:00.000Z", used=95.0),
    )
    _log(root, "newer-session", _event(at="2026-09-21T12:00:00.000Z", used=44.0))

    account = _account(tmp_path / "data", root, "codex")

    assert account.used_percent == 95.0
    assert account.source == quota.LOGGED
    assert account.held_back is True


def test_a_damaged_tree_yields_no_figure_rather_than_raising(tmp_path: Path) -> None:
    """Truncated, unparsable, unopenable, and not a log at all, in one tree."""

    root = tmp_path / "sessions"
    _log(root, "torn", '{"timestamp": "2026-09-21T13:00')
    _log(root, "noise", "not json at all", "")
    (root / "2026" / "09" / "21" / "rollout-shut.jsonl").mkdir()
    (root / "2026" / "09" / "21" / "notes.txt").write_text("nothing", encoding="utf-8")

    account = _account(tmp_path / "data", root, "codex")

    assert account.held_back is False
    assert account.absent == quota.NO_LOG


def test_an_event_with_no_rate_limits_does_not_end_the_scan(tmp_path: Path) -> None:
    """A log's last event is frequently not a `token_count` one.

    Stopping at the first event that carries no window would read almost every
    real session as a machine with no figure.
    """

    root = tmp_path / "sessions"
    _log(
        root,
        "quiet-tail",
        _event(at="2026-09-21T12:00:00.000Z", used=95.0),
        _event(at="2026-09-21T12:30:00.000Z", limits=False),
        _event(at="2026-09-21T13:00:00.000Z", limits=False),
    )

    account = _account(tmp_path / "data", root, "codex")

    assert account.used_percent == 95.0
    assert account.held_back is True


def test_a_primary_naming_another_window_is_no_figure(tmp_path: Path) -> None:
    """`primary` is the week on every log this repository holds, and is checked."""

    root = tmp_path / "sessions"
    _log(root, "five-hour", _event(used=99.0, elapsed=0.1, window=300))

    account = _account(tmp_path / "data", root, "codex")

    assert account.held_back is False
    assert account.absent == quota.NO_LOG


def test_a_missing_codex_tree_is_no_guard(tmp_path: Path) -> None:
    """A machine that has never run Codex, which needs saying nowhere."""

    account = _account(tmp_path / "data", tmp_path / "never", "codex")

    assert account.held_back is False
    assert account.absent == quota.NO_LOG


@pytest.mark.parametrize(
    ("at", "elapsed", "expected"),
    [
        ("2026-09-19T20:00:00.000Z", 0.5, quota.STALE),
        (FRESH, 1.5, quota.PASSED),
    ],
)
def test_a_codex_figure_ages_from_the_events_own_timestamp(
    tmp_path: Path, at: str, elapsed: float, expected: str
) -> None:
    """The same two bounds as the file, counted from the event rather than a write.

    `NOW` is 2026-09-21T14:13:20Z, so the first event is some forty-two hours
    old, and the second is current and names a window that has already reset.
    """

    root = tmp_path / "sessions"
    _log(root, "aged", _event(at=at, used=95.0, elapsed=elapsed))

    account = _account(tmp_path / "data", root, "codex")

    assert account.held_back is False
    assert account.absent == expected


def test_the_read_is_bounded_to_the_most_recent_files(tmp_path: Path) -> None:
    """Twenty files, newest by modification time, and no further.

    The read runs inside somebody else's turn, so the bound is the point: a
    machine with years of sessions costs the same as one with a week's.
    """

    root = tmp_path / "sessions"
    written = [
        _log(root, f"session-{index:03d}", _event(used=95.0))
        for index in range(quota.CODEX_FILES + 4)
    ]
    for index, path in enumerate(written):
        os.utime(path, (NOW - 1000 + index, NOW - 1000 + index))

    recent = quota._recent(root)

    assert len(recent) == quota.CODEX_FILES
    assert set(recent) == set(written[4:])


def test_an_event_beyond_the_tail_is_not_read(tmp_path: Path) -> None:
    """Only the end of each log is parsed, rather than the file whole.

    The one event carrying a window is current, so the absence below is the
    tail bound holding rather than the figure having aged out.
    """

    root = tmp_path / "sessions"
    padding = json.dumps({"type": "event_msg", "payload": {"note": "x" * 4096}})
    _log(
        root,
        "long-session",
        _event(used=95.0),
        *[padding] * (quota.CODEX_TAIL // 4096 + 4),
    )

    account = _account(tmp_path / "data", root, "codex")

    assert account.held_back is False
    assert account.absent == quota.NO_LOG


# --- what the guard answers with, and how it is run -----------------------


def test_held_back_names_the_harnesses_the_rule_holds(tmp_path: Path) -> None:
    """The one answer the selection engine asks this module for."""

    data = tmp_path / "data"
    root = tmp_path / "sessions"
    _written(data, used=95.0, elapsed=0.5)
    _log(root, "easy", _event(used=5.0))

    assert quota.held_back(data, root, now=NOW) == frozenset({"claude-code"})


def test_the_reader_runs_as_a_script_and_prints_one_account_per_harness(
    tmp_path: Path,
) -> None:
    """`status` renders one reader's answer rather than reimplementing the rule."""

    data = tmp_path / "data"
    _written(data, used=95.0, elapsed=0.5, at=time.time())

    completed = subprocess.run(
        [
            sys.executable,
            str(READER),
            f"--data={data}",
            f"--codex={tmp_path / 'sessions'}",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    named = {row["harness"]: row for row in json.loads(completed.stdout)["accounts"]}
    assert set(named) == {"claude-code", "codex"}
    assert named["claude-code"]["held_back"] is True
    assert named["claude-code"]["used_percent"] == 95.0
    assert named["claude-code"]["source"] == quota.WRITTEN
    assert named["codex"]["held_back"] is False
    assert named["codex"]["absent"] == quota.NO_LOG


def test_the_reader_reaches_nothing_and_takes_its_roots_as_arguments() -> None:
    """No network, no credential, and no machine of its own to resolve."""

    source = READER.read_text(encoding="utf-8")

    for forbidden in ("urllib", "socket", "curl", "find-generic-password"):
        assert forbidden not in source

    # Both trees are handed in, so nothing the rule reads is resolved from the
    # machine it happens to be running on — which is what lets every test here
    # point it at a fixture tree.
    for entry in (quota.accounts, quota.held_back):
        taken = list(inspect.signature(entry).parameters)
        assert taken[:2] == ["data_dir", "codex_root"]


def test_the_default_codex_root_is_the_one_the_skill_means(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Named once here, so the engine and the report mean the same tree."""

    monkeypatch.delenv("KNTNT_HOME", raising=False)
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("USERPROFILE", str(tmp_path))

    assert quota.codex_root() == tmp_path / ".codex" / "sessions"
    assert quota.data_root() == tmp_path / ".kntnt" / "model-selector"

    # And the isolated home every other script of this collection is pointed at
    # by, so that the reader and the status line writing the file agree.
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path / "elsewhere"))
    assert quota.data_root() == tmp_path / "elsewhere" / ".kntnt" / "model-selector"


def test_the_clock_is_what_an_instant_is_measured_against(tmp_path: Path) -> None:
    """With no instant given the reader asks the clock, as a real call does."""

    moment = time.time()
    (tmp_path / "quota.json").write_text(
        json.dumps(
            {
                "channels": {
                    "claude-code": {
                        "used_percent": 95.0,
                        "resets_at": int(moment + 0.5 * WEEK_SECONDS),
                        "window_minutes": WEEK_MINUTES,
                        "written_at": int(moment),
                    }
                }
            }
        ),
        encoding="utf-8",
    )

    assert quota.held_back(tmp_path, tmp_path / "absent") == frozenset({"claude-code"})
