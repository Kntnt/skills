# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Turn a captured Unit of Work into a graded measurement, cheaply or not at all.

Capture writes Units and never judges them. This is where a Unit becomes a
number, and the whole design is about what that number is allowed to cost and
what it is allowed to claim.

**Free signals decide first.** A Unit that was interrupted or errored and came
back with nothing is dropped rather than scored zero: nothing was established
about the model, and a zero says something false about it. A Unit whose
instruction was given again later was not good enough the first time. A Unit
whose tests ran and passed did the work. None of those costs anything.

**The judge is bought deliberately.** Where the signals decided nothing, one
call to a model this machine can reach reads the Unit's own two ends — the
instruction and the result — and answers with a kind, a number and one line.
Which model that is comes from the engine, asked for a `converse` point at high
stakes, because choosing a model is `selection.py`'s work and naming one here
would be a second place to keep current. The kind is what this call is and not
what the Unit was: two excerpts in and a number out is a short bounded exchange,
where `analyze` is priced at reading a million and a half cached tokens, which
would buy a judge dearer than the work it grades. High stakes is what grading
actually is: nothing checks the judge, and a judge that cannot do the job
returns a plausible wrong number rather than an obvious failure. So this asks
for the cheapest point the engine is confident in rather than the cheapest
point there is, and never one of the calls the engine spends on an
experiment — a store whose grades came from a lottery of graders would be
measuring the graders.

**It never invents a number.** Where no model can be reached, where the call
times out, where the answer will not parse, the Unit waits for the next pass.
After three such attempts it takes whatever grade its free signals support, and
is dropped where they support none. A grader that cannot run must lose nothing
and must claim nothing.

**It never costs a session.** Capture calls `hook_pass` at a session's end, and
that call does the free half only — local arithmetic over a file — and then
starts this same script again, detached and in its own session, to spend the
judge budget where nobody is waiting. Two copies must not both grade, so a
lock file is held for the length of a pass and a second copy exits silently.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager, suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol

import catalogue
import evidence
import profiles
from evidence import KINDS

# Where the pending Units wait, and where this module records that it ran.
# Both names are capture's, read here as an on-disk contract rather than
# imported, the posture every consumer of this Skill's stores already takes.
PENDING_FILE = "pending.jsonl"
GRADER_STATE_FILE = "grader.json"
LOCK_FILE = "grade.lock"

# How many judge calls one pass may buy. It is a hard limit rather than a
# guideline: everything above it waits for the next pass, and a pass that
# spends nothing is a pass that cost nothing.
BUDGET = 20

# How long one judge call may take, in seconds. A model that has not answered
# by then is a model that could not be reached, and the Unit is left pending.
CALL_SECONDS = 30.0

# How long the engine has to say which model to ask. It is a local script over
# local files, so this is generous rather than tight.
SELECT_SECONDS = 20.0

# How many judge-graded rows in the last day stop a pass entirely. A machine
# that has already bought fifty gradings today has bought enough of them.
DAILY_JUDGE_LIMIT = 50
DAILY_WINDOW = timedelta(hours=24)

# How many times one Unit may fail to reach a judge before it is settled on
# whatever its free signals support, or dropped.
MAX_ATTEMPTS = 3

# The grades the free signals award. An instruction given twice failed the
# first time without being worthless; tests that ran and passed are the closest
# thing to an external checker an ordinary session contains.
RETRIED_GRADE = 0.3
TESTS_PASSED_GRADE = 0.9

# How long a lock may sit before it is assumed to belong to a process that
# died. Fifteen minutes is longer than any pass can legitimately take.
LOCK_STALE_SECONDS = 900.0

# The scale the judge answers on, and what one line of reason may run to.
JUDGE_SCALE = 100.0
REASON_CHARS = 200

# How deep inside a bridge's own event stream the verdict is looked for. Three
# is one event, one message and one content block, which is every wrapping any
# bridge this Skill knows applies.
NESTING = 3


class Judge(Protocol):
    """The one seam this module reaches a model through."""

    def __call__(self, prompt: str, seconds: float) -> str | None:
        """Ask one model *prompt*, or answer None where none could be asked."""


def default_data() -> Path:
    """Return the data directory this Skill keeps its evidence in by default."""

    return Path.home() / ".kntnt" / "model-selector"


def _here() -> Path:
    """Return the Skill directory this module ships inside."""

    return Path(__file__).resolve().parent.parent


def _now() -> datetime:
    """Return this instant, as a measurement dates one."""

    return datetime.now(UTC)


def _stamp(instant: datetime) -> str:
    """Return one instant in the form every stored timestamp is written in."""

    return instant.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _parsed(instant: Any) -> datetime | None:
    """Return one recorded instant as a datetime, or None where it is unusable."""

    if not isinstance(instant, str) or not instant:
        return None
    try:
        parsed = datetime.fromisoformat(instant)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


def _safe_home() -> Path:
    """Return a directory nothing in this collection can remove under a process.

    Every process started here runs from it. A launcher resolves its own
    project from where it stands, so a process started in a directory this
    collection is in the middle of replacing fails with its own *No such file
    or directory* before it reaches the program it was asked to run (#257).
    """

    try:
        return Path.home()
    except RuntimeError:
        return Path.cwd()


def _pending(data: Path) -> list[dict[str, Any]]:
    """Return every Unit still waiting to be graded, skipping what will not parse."""

    path = data / PENDING_FILE
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []

    rows: list[dict[str, Any]] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            loaded = json.loads(stripped)
        except ValueError:
            continue
        if isinstance(loaded, dict):
            rows.append(loaded)
    return rows


def _write_pending(data: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    """Replace the pending store with what is still waiting.

    Through a temporary sibling and an atomic rename, so an interrupted pass
    leaves the whole of the previous queue standing rather than half of it.
    """

    path = data / PENDING_FILE
    if not rows:
        path.unlink(missing_ok=True)
        return

    data.mkdir(parents=True, exist_ok=True)
    staged = path.parent / f"{path.name}.tmp"
    staged.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    staged.replace(path)


@contextmanager
def _lock(data: Path) -> Iterator[bool]:
    """Hold the grading lock for the length of one pass, or yield False.

    Two copies grading at once would both read the same queue and both buy the
    same judgement, so the second one does nothing at all rather than doing it
    twice. A lock older than any pass can legitimately take belonged to a
    process that died and is taken over.
    """

    path = data / LOCK_FILE
    data.mkdir(parents=True, exist_ok=True)

    with suppress(OSError):
        held = time.time() - path.stat().st_mtime
        if held > LOCK_STALE_SECONDS:
            path.unlink(missing_ok=True)

    try:
        handle = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except OSError:
        yield False
        return

    os.close(handle)
    try:
        yield True
    finally:
        path.unlink(missing_ok=True)


def _judged_today(data: Path, now: datetime) -> int:
    """Return how many judge-graded rows the store holds from the last day."""

    since = now - DAILY_WINDOW
    return sum(
        1
        for row in evidence.load(data)
        if row.graded_by == "judge"
        and (at := _parsed(row.at)) is not None
        and at >= since
    )


def _tokens(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return one Unit's token counts, admitting a store somebody hand-edited."""

    counted = row.get("tokens")
    return counted if isinstance(counted, dict) else {}


def _signals(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return one Unit's free signals, admitting a store somebody hand-edited."""

    signals = row.get("signals")
    return signals if isinstance(signals, dict) else {}


def _signal_grade(signals: Mapping[str, Any]) -> float | None:
    """Return what the free signals alone establish, or None where they establish nothing.

    Order matters: an instruction given again is evidence about the answer that
    preceded it, and it outranks a test run that happened along the way.
    """

    if signals.get("retried"):
        return RETRIED_GRADE
    if signals.get("tests_ran") and signals.get("tests_passed"):
        return TESTS_PASSED_GRADE
    return None


def _established_nothing(row: Mapping[str, Any], signals: Mapping[str, Any]) -> bool:
    """Return whether this Unit says nothing at all about the model that ran it.

    An attempt somebody stopped, and an attempt the Harness itself failed, came
    back with no result and therefore with no evidence. Recording it as a zero
    would say the model tried and failed, which is not what happened.
    """

    stopped = bool(signals.get("interrupted")) or bool(signals.get("errored"))
    return stopped and not str(row.get("result_excerpt") or "").strip()


def _kind_from_signals(row: Mapping[str, Any]) -> str:
    """Return the coarsest honest kind for a Unit no judge read.

    Two answers, because the free signals support exactly two: work that
    changed something was building, and work that changed nothing was reading.
    A finer claim here would be a guess entering the store as a measurement.
    """

    changed = row.get("changing_tool_calls")
    return "implement" if isinstance(changed, int) and changed > 0 else "analyze"


def _kind_notes() -> dict[str, str]:
    """Return the shipped one-line note for each kind, for the judge to read by."""

    path = _here() / "data" / "kinds.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}

    entries = raw.get("kinds") if isinstance(raw, dict) else None
    if not isinstance(entries, dict):
        return {}
    return {
        kind: str(entry.get("note") or "")
        for kind, entry in entries.items()
        if kind in KINDS and isinstance(entry, dict)
    }


def prompt_for(row: Mapping[str, Any]) -> str:
    """Return exactly what one judge call sends, and nothing more.

    The Unit's own two ends, what it did, how long it took and what it burned.
    Never the model, the deliberation, the harness, the session, the Unit's own
    identity, the free signals, or any path — a judge told which model wrote
    the answer is grading the model rather than the answer.
    """

    notes = _kind_notes()
    vocabulary = "\n".join(
        f"- {kind}: {notes.get(kind, '')}".rstrip() for kind in KINDS
    )
    tokens = _tokens(row)
    counted = ", ".join(
        f"{category}={value}"
        for category, value in sorted(tokens.items())
        if isinstance(value, (int, float))
    )

    return (
        "Grade one unit of work. Answer with one JSON object and nothing else:\n"
        '{"kind": "<one of the kinds below>", "grade": <0-100>, '
        '"reason": "<one line>"}\n'
        "\n"
        "grade is how well the result answers the instruction: 0 is nothing "
        "useful, 100 is complete and correct.\n"
        "\n"
        "Kinds:\n"
        f"{vocabulary}\n"
        "\n"
        "Instruction:\n"
        f"{row.get('instruction_excerpt') or ''}\n"
        "\n"
        "Result:\n"
        f"{row.get('result_excerpt') or ''}\n"
        "\n"
        f"Tool calls: {row.get('tool_calls')}, of which "
        f"{row.get('changing_tool_calls')} changed something.\n"
        f"Duration: {row.get('seconds')} seconds.\n"
        f"Tokens: {counted or 'not measured'}.\n"
    )


def _verdict(answer: str | None) -> tuple[str | None, float, str] | None:
    """Return the kind, the grade and the reason one judge answered, or None.

    A bridge wraps a model's own words in its own event stream, so the object
    is looked for rather than assumed to be the whole of standard output. An
    answer with no readable grade in it is an answer that was not given.
    """

    if not answer:
        return None

    for candidate in _objects(answer):
        grade = candidate.get("grade")
        if not isinstance(grade, (int, float)) or isinstance(grade, bool):
            continue
        kind = candidate.get("kind")
        reason = candidate.get("reason")
        return (
            kind if isinstance(kind, str) and kind in KINDS else None,
            min(1.0, max(0.0, float(grade) / JUDGE_SCALE)),
            str(reason or "")[:REASON_CHARS],
        )
    return None


def _objects(text: str, depth: int = 0) -> list[dict[str, Any]]:
    """Return every JSON object *text* holds that carries a grade.

    A bridge hands a model's own words back as a string inside an event of its
    own, so an object that is not itself a verdict is looked into once more
    rather than discarded. The depth is bounded because the text arrived from
    a process this module does not control.
    """

    if depth > NESTING:
        return []

    found: list[dict[str, Any]] = []
    for candidate in _candidates(text):
        if "grade" in candidate:
            found.append(candidate)
            continue
        found += [
            nested
            for value in candidate.values()
            if isinstance(value, str)
            for nested in _objects(value, depth + 1)
        ]
    return found


def _candidates(text: str) -> list[dict[str, Any]]:
    """Return every JSON object that starts somewhere in *text*."""

    decoder = json.JSONDecoder()
    found: list[dict[str, Any]] = []
    for start, character in enumerate(text):
        if character != "{":
            continue
        try:
            loaded, _end = decoder.raw_decode(text, start)
        except ValueError:
            continue
        if isinstance(loaded, dict):
            found.append(loaded)
    return found


def _bridge(data: Path, seconds: float) -> list[str] | None:
    """Return the command that starts the model this machine grades with.

    The engine chooses it, for the kind of work this call is and at the stakes it
    carries. The kind is `converse` — two short excerpts in, a number and a line
    out — rather than the kind of the Unit being graded, and rather than
    `analyze`, whose token prior is a repository read and would price a judge
    above the work it judges. Grading is unchecked work — nothing downstream
    catches a wrong grade, and a wrong grade is worse than no grade — which is
    the engine's own definition of high stakes, so it answers with the cheapest
    point it is confident in and never explores.

    A point that is not a command — a subagent only an agent inside a Harness
    can name, or the caller's own seat — is not something a script can start,
    so there is no judge to call and the Unit waits.
    """

    engine = Path(__file__).resolve().parent / "selection.py"
    command = [
        "uv",
        "run",
        str(engine),
        "--kind=converse",
        "--scope=callable",
        "--stakes=high",
        f"--data={data}",
    ]
    try:
        answered = subprocess.run(
            command,
            cwd=_safe_home(),
            capture_output=True,
            text=True,
            timeout=seconds,
            check=False,
        )
        chosen = json.loads(answered.stdout)
    except (OSError, ValueError, subprocess.SubprocessError):
        return None

    started = chosen.get("launch") if isinstance(chosen, dict) else None
    if not isinstance(started, dict) or started.get("how") != "bridge-command":
        return None
    argv = started.get("command")
    if not isinstance(argv, list) or not all(isinstance(word, str) for word in argv):
        return None
    return [str(word) for word in argv]


def _judge_for(data: Path) -> Judge:
    """Return the judge this machine actually has, or one that always declines."""

    def ask(prompt: str, seconds: float) -> str | None:
        """Ask the model the engine trusts with this, or answer None."""

        argv = _bridge(data, SELECT_SECONDS)
        if argv is None:
            return None
        try:
            answered = subprocess.run(
                [*argv, prompt],
                cwd=_safe_home(),
                capture_output=True,
                text=True,
                timeout=seconds,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            return None
        return answered.stdout

    return ask


def _measurement(
    row: Mapping[str, Any],
    kind: str,
    grade: float,
    graded_by: str,
    at: str,
    cat: catalogue.Catalogue,
    kinds: evidence.KindPriors,
    profile: profiles.Profile,
) -> dict[str, Any]:
    """Return one Unit as the measurement the store holds.

    Priced here rather than left for a reader, because the rate card that
    applies is the one standing when the work ran, and a row that carries a
    cost is one nothing has to re-derive.

    The card is the one the channel that reached the model charges, where the
    profile carries one. A store priced at a list price nobody paid measures
    somebody else's arrangement, and this store exists to say what a point
    costs on this machine.
    """

    counted = {
        category: value if isinstance(value, (int, float)) else None
        for category, value in _tokens(row).items()
    }
    matched = catalogue.resolve(cat, str(row.get("model") or ""))
    channel = (
        profiles.channel_for(profile, matched[0], str(row.get("harness") or ""))
        if matched
        else None
    )
    cost = (
        catalogue.cost_usd(
            matched[0],
            counted,
            kind,
            kinds,
            rates=channel.rates if channel is not None else None,
        )
        if matched
        else None
    )

    return {
        "attempt_id": row.get("unit_id"),
        "at": at,
        "kind": kind,
        "label": None,
        "model": row.get("model"),
        "deliberation": row.get("deliberation"),
        "harness": row.get("harness"),
        "channel": None,
        "grade": grade,
        "graded_by": graded_by,
        "tokens": counted,
        "cost_usd": cost,
        "seconds": row.get("seconds"),
        "routed": False,
    }


def grade_pending(
    data: Path,
    *,
    judging: bool = True,
    budget: int = BUDGET,
    call_seconds: float = CALL_SECONDS,
    judge: Judge | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Run one grading pass over the Units waiting under *data*.

    Free signals first, the judge only where they decided nothing, and never a
    number nobody established. What is graded leaves the pending store; what
    could not be graded stays in it with one more attempt against its name,
    until three of them have failed.
    """

    instant = now or _now()
    stamp = _stamp(instant)
    ask = judge or _judge_for(data)
    cat = catalogue.load(data, _here())
    kinds = evidence.load_kinds(_here())
    profile = profiles.load(data, cat)

    counts = {"graded": 0, "judged": 0, "dropped": 0, "waiting": 0}
    written: list[dict[str, Any]] = []
    waiting: list[dict[str, Any]] = []
    spent = 0

    # A day's worth of bought gradings is enough of them, but the cap is on the
    # buying alone: the free half costs nothing and stopping it too would leave
    # a signal that already decided the matter sitting in the queue for a day.
    capped = judging and _judged_today(data, instant) >= DAILY_JUDGE_LIMIT
    judging = judging and not capped

    for row in _pending(data):
        signals = _signals(row)

        # A Unit with no model behind it, and one whose attempt established
        # nothing about the model that ran it, are both dropped rather than
        # recorded: neither is evidence about anything the store can rank.
        if not row.get("model") or _established_nothing(row, signals):
            counts["dropped"] += 1
            continue

        settled = _signal_grade(signals)
        if settled is not None:
            written.append(
                _measurement(
                    row,
                    _kind_from_signals(row),
                    settled,
                    "signal",
                    stamp,
                    cat,
                    kinds,
                    profile,
                )
            )
            counts["graded"] += 1
            continue

        # Below the budget line the Unit is simply left where it is: this
        # pass's own thrift is not a failure of the Unit's.
        if not judging or spent >= budget:
            waiting.append(row)
            counts["waiting"] += 1
            continue

        spent += 1
        verdict = _verdict(ask(prompt_for(row), call_seconds))
        if verdict is not None:
            kind, grade, _reason = verdict
            written.append(
                _measurement(
                    row,
                    kind or _kind_from_signals(row),
                    grade,
                    "judge",
                    stamp,
                    cat,
                    kinds,
                    profile,
                )
            )
            counts["graded"] += 1
            counts["judged"] += 1
            continue

        attempts = int(row.get("attempts") or 0) + 1
        if attempts < MAX_ATTEMPTS:
            waiting.append({**row, "attempts": attempts})
            counts["waiting"] += 1
            continue

        # Three failures to reach a judge, so the Unit is settled on what its
        # free signals support and dropped where they support nothing.
        counts["dropped"] += 1

    if written:
        evidence.append(data, written)
    _write_pending(data, waiting)
    return _report(data, stamp, counts, capped=capped)


def _report(
    data: Path, stamp: str, counts: dict[str, int], *, capped: bool
) -> dict[str, Any]:
    """Record that a pass happened, and return an account of it."""

    report = {
        "verb": "grade",
        "data": str(data),
        "last_run_at": stamp,
        "capped": capped,
        **counts,
        "pending": len(_pending(data)),
    }
    with suppress(OSError):
        data.mkdir(parents=True, exist_ok=True)
        (data / GRADER_STATE_FILE).write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    return report


def dispatch(data: Path) -> bool:
    """Start this same script again, detached, to spend the judge budget.

    The judge half runs in its own session so that nothing about it is charged
    to the session that ended: the Harness's hook has already returned by the
    time the first model call is made, and stopping the terminal that started
    it stops nothing here. Every failure to start it is an unspent budget
    rather than a failure of anybody's work.
    """

    command = ["uv", "run", str(Path(__file__).resolve()), "--once", f"--data={data}"]
    try:
        subprocess.Popen(
            command,
            cwd=_safe_home(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return True


def hook_pass(data: Path) -> dict[str, Any]:
    """Grade what the free signals settle, then hand the rest to a detached pass.

    This is what capture calls at a session's end, so it does local arithmetic
    over one file and nothing else — no model call, no network, no waiting —
    and the judging that costs money and time happens somewhere the session is
    not paying for it.
    """

    with _lock(data) as held:
        if not held:
            return {"verb": "grade", "skipped": "another pass holds the lock"}
        report = grade_pending(data, judging=False)

    report["dispatched"] = dispatch(data) if report["pending"] else False
    return report


def _emit(payload: dict[str, Any]) -> None:
    """Print one machine-readable answer."""

    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one grading invocation. The only thing here that may fail."""

    parser = argparse.ArgumentParser(
        prog="grade.py", description="Grade the Units of Work capture is holding."
    )
    parser.add_argument("--data", default=str(default_data()))
    parser.add_argument("--budget", type=int, default=BUDGET)
    parser.add_argument("--once", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one grading pass, and exit 0 whatever came of it."""

    args = parse_args(sys.argv[1:] if argv is None else argv)
    data = Path(args.data).expanduser()

    try:
        if not args.once:
            answered = hook_pass(data)
        else:
            with _lock(data) as held:
                answered = (
                    grade_pending(data, budget=args.budget)
                    if held
                    else {"verb": "grade", "skipped": "another pass holds the lock"}
                )
    except Exception as failure:  # noqa: BLE001 - grading never costs its caller
        answered = {"verb": "grade", "problem": f"grading failed: {failure!r}"}

    _emit(answered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
