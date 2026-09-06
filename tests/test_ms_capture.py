"""Units of Work the model-selector Skill derives from ordinary Harness sessions."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
from pathlib import Path
from typing import Any

from support.model_routing import attempt_line

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"

# One assistant turn's worth of tokens, in the Harness's own spelling. Kept as
# one constant because what matters in every test using it is that the five
# categories arrive under the names a measurement is priced in.
USAGE = {
    "input_tokens": 12,
    "cache_creation_input_tokens": 3400,
    "cache_read_input_tokens": 120000,
    "output_tokens": 900,
    "output_tokens_details": {"thinking_tokens": 250},
}


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


# In dependency order, so that a module importing a sibling by plain name
# finds the same object these tests are holding.
_module("catalogue")
_module("profiles")
_module("evidence")
_module("launch")
capture = _module("capture", "model_selector_capture")


class _Grader:
    """Stand in for the grading pass capture dispatches at a session's end.

    Registered under the name capture loads the real one by, so that no test
    ever starts the detached judging process the real `hook_pass` would.
    """

    def __init__(self) -> None:
        self.passes: list[Path] = []

    def hook_pass(self, data: Path) -> dict[str, Any]:
        self.passes.append(data)
        return {"verb": "grade", "graded": 0}


def _grader() -> _Grader:
    """Install the stub grader and return it."""

    stub = _Grader()
    sys.modules["model_selector_grade"] = stub  # type: ignore[assignment]
    return stub


def _user(
    text: str, at: str, *, kind: str | None = "human", meta: bool = False
) -> dict[str, Any]:
    """Provide one user line, as Claude Code writes one.

    *kind* is the `origin.kind` the Harness stamps on the line — a person
    typing, a peer session messaging, a background task reporting back, the
    session continuing itself — and `None` writes no `origin` at all, which is
    what an injected reminder or a command echo arrives as. *meta* writes the
    `isMeta` flag beside it.
    """

    line: dict[str, Any] = {
        "type": "user",
        "timestamp": at,
        "message": {"role": "user", "content": text},
    }
    if kind is not None:
        line["origin"] = {"kind": kind}
    if meta:
        line["isMeta"] = True
    return line


def _assistant(
    at: str,
    *,
    model: str = "claude-opus-5",
    effort: str = "high",
    text: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    usage: dict[str, Any] | None = None,
    api_error: bool = False,
) -> dict[str, Any]:
    """Provide one assistant turn, with whatever it said and whatever it called."""

    content: list[dict[str, Any]] = []
    if text is not None:
        content.append({"type": "text", "text": text})
    content += tools or []
    line: dict[str, Any] = {
        "type": "assistant",
        "timestamp": at,
        "effort": effort,
        "message": {
            "role": "assistant",
            "model": model,
            "content": content,
            "usage": usage if usage is not None else USAGE,
        },
    }
    if api_error:
        line["isApiErrorMessage"] = True
    return line


def _call(name: str, **arguments: Any) -> dict[str, Any]:
    """Provide one tool call inside an assistant turn."""

    return {
        "type": "tool_use",
        "id": f"toolu_{name}_{len(arguments)}",
        "name": name,
        "input": arguments,
    }


def _result(
    at: str, *, is_error: bool = False, stopped: bool = False
) -> dict[str, Any]:
    """Provide one tool result, which is a user line carrying no instruction."""

    return {
        "type": "user",
        "timestamp": at,
        "message": {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "toolu", "is_error": is_error}
            ],
        },
        "toolUseResult": {"stdout": "", "stderr": "", "interrupted": stopped},
    }


def _transcript(tmp_path: Path, *lines: dict[str, Any]) -> Path:
    """Write one session transcript and return its path."""

    path = tmp_path / "session.jsonl"
    path.write_text(
        "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
    )
    return path


def _subagent(transcript: Path, name: str, *lines: dict[str, Any]) -> Path:
    """Write one subagent transcript into the companion directory beside *transcript*."""

    directory = transcript.with_suffix("") / "subagents"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"agent-{name}.jsonl"
    path.write_text(
        "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
    )
    return path


def _long_unit(
    started: str, ended: str, instruction: str = "do the work"
) -> list[dict[str, Any]]:
    """Provide the lines of one Unit substantial by duration alone."""

    return [
        _user(instruction, started),
        _assistant(ended, text="Done.", tools=[_call("Read", file_path="/x")]),
    ]


# --- What a Unit is, and what is not one -------------------------------------


def test_a_unit_below_every_threshold_is_never_written(tmp_path: Path) -> None:
    """A session of quick questions and answers leaves no trace at all.

    One reading tool call, four seconds, and a few hundred output tokens is
    the ordinary back-and-forth of a working session, and measuring it would
    swamp the store with rows that say nothing about any model.
    """

    transcript = _transcript(
        tmp_path,
        _user("what does this file do?", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:00:04.000Z",
            text="It reads the catalogue.",
            tools=[_call("Bash", command="cat catalogue.py")],
        ),
        _result("2026-09-06T10:00:05.000Z"),
    )

    assert capture.units("s", "claude-code", str(transcript)) == []


def test_three_changing_tool_calls_make_a_unit_substantial(tmp_path: Path) -> None:
    """Work that changed three things is work, however quickly it was done."""

    transcript = _transcript(
        tmp_path,
        _user("rename the constant everywhere", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:00:03.000Z",
            text="Renamed.",
            tools=[
                _call("Edit", file_path="/a"),
                _call("Edit", file_path="/b"),
                _call("Bash", command="git commit -m x"),
            ],
        ),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert len(found) == 1
    assert found[0].changing_tool_calls == 3
    assert found[0].tool_calls == 3


def test_a_reading_shell_command_is_not_a_change(tmp_path: Path) -> None:
    """`cd` and `grep` looked at the machine; a commit changed it."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
        _assistant(
            "2026-09-06T10:05:01.000Z",
            tools=[
                _call("Bash", command="cd /repo && grep -rn thing ."),
                _call("Bash", command="git status"),
                _call("Bash", command="git push"),
            ],
        ),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert found[0].tool_calls == 4
    assert found[0].changing_tool_calls == 1


def test_the_main_transcript_splits_into_one_unit_per_instruction(
    tmp_path: Path,
) -> None:
    """A Unit runs from an instruction to the turn before the next one."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z", "first"),
        *_long_unit("2026-09-06T11:00:00.000Z", "2026-09-06T11:09:00.000Z", "second"),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert [unit.instruction_excerpt for unit in found] == ["first", "second"]
    assert [round(unit.seconds) for unit in found] == [300, 540]
    assert [unit.delegated for unit in found] == [False, False]


def test_a_tool_result_never_starts_a_unit_of_its_own(tmp_path: Path) -> None:
    """A user line carrying somebody else's output is not an instruction."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant("2026-09-06T10:00:01.000Z", tools=[_call("Bash", command="ls")]),
        _result("2026-09-06T10:00:02.000Z"),
        _assistant("2026-09-06T10:04:00.000Z", text="Done."),
    )

    assert len(capture.units("s", "claude-code", str(transcript))) == 1


def _spent(output: int) -> dict[str, Any]:
    """Provide one turn's usage, distinguishable by what it wrote."""

    return {
        "input_tokens": 10,
        "cache_creation_input_tokens": 0,
        "cache_read_input_tokens": 1000,
        "output_tokens": output,
        "output_tokens_details": {"thinking_tokens": 0},
    }


def test_a_background_report_continues_the_unit_it_arrives_in(
    tmp_path: Path,
) -> None:
    """A session splits where somebody typed, and nowhere else.

    A subagent finishing and a slash command echoing its own name are the
    session's bookkeeping. Splitting at either one files a Unit whose
    instruction is a notification and whose result is whatever happened next.
    """

    transcript = _transcript(
        tmp_path,
        _user("first", "2026-09-06T10:00:00.000Z"),
        _assistant("2026-09-06T10:01:30.000Z", text="one", usage=_spent(100)),
        _result("2026-09-06T10:01:31.000Z"),
        _user("second", "2026-09-06T10:10:00.000Z"),
        _assistant("2026-09-06T10:10:30.000Z", text="two", usage=_spent(200)),
        _result("2026-09-06T10:10:31.000Z"),
        _user(
            "<task-notification>agent aaa finished</task-notification>",
            "2026-09-06T10:11:00.000Z",
            kind="task-notification",
        ),
        _user(
            "<command-name>/orchestrate</command-name>",
            "2026-09-06T10:11:10.000Z",
            kind=None,
        ),
        _assistant("2026-09-06T10:12:00.000Z", text="two again", usage=_spent(300)),
        _user("third", "2026-09-06T10:20:00.000Z"),
        _assistant("2026-09-06T10:21:30.000Z", text="three", usage=_spent(400)),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert [unit.instruction_excerpt for unit in found] == ["first", "second", "third"]
    assert [unit.tokens["output"] for unit in found] == [100.0, 500.0, 400.0]
    assert [round(unit.seconds) for unit in found] == [91, 120, 90]


def test_a_peer_agents_message_begins_a_unit_of_its_own(tmp_path: Path) -> None:
    """A message from another session is an instruction an agent typed."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z", "mine"),
        _user(
            "please look at the branch",
            "2026-09-06T11:00:00.000Z",
            kind="peer",
            meta=True,
        ),
        _assistant("2026-09-06T11:05:00.000Z", text="Looked."),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert [unit.instruction_excerpt for unit in found] == [
        "mine",
        "please look at the branch",
    ]


def test_no_other_user_line_begins_a_unit(tmp_path: Path) -> None:
    """Everything the Harness itself put there is absorbed, never split at."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant("2026-09-06T10:00:30.000Z", tools=[_call("Bash", command="ls")]),
        _result("2026-09-06T10:00:31.000Z"),
        _user(
            "<task-notification>agent aaa finished</task-notification>",
            "2026-09-06T10:01:00.000Z",
            kind="task-notification",
        ),
        _user(
            "continue where you left off",
            "2026-09-06T10:02:00.000Z",
            kind="auto-continuation",
            meta=True,
        ),
        _user(
            "<local-command-stdout>ok</local-command-stdout>",
            "2026-09-06T10:03:00.000Z",
            kind=None,
        ),
        _assistant("2026-09-06T10:05:00.000Z", text="Done."),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert [unit.instruction_excerpt for unit in found] == ["do the work"]


def test_an_interruption_line_marks_the_unit_it_stopped(tmp_path: Path) -> None:
    """A stopped turn says so, and does not begin a Unit of its own."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:02:00.000Z", tools=[_call("Bash", command="rm -rf x")]
        ),
        _user(
            "[Request interrupted by user]",
            "2026-09-06T10:05:00.000Z",
            kind=None,
        ),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert len(found) == 1
    assert found[0].signals["interrupted"] is True


def test_a_subagent_transcript_becomes_its_own_unit_with_its_own_seat(
    tmp_path: Path,
) -> None:
    """The companion directory is the cleanest signal a delegated point leaves.

    Its own model and its own effort, rather than the session's, which is the
    whole reason a delegated Unit is worth measuring separately at all.
    """

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )
    _subagent(
        transcript,
        "aaa",
        {
            "type": "user",
            "timestamp": "2026-09-06T10:01:00.000Z",
            "isSidechain": True,
            "message": {"role": "user", "content": "survey the tree"},
        },
        _assistant(
            "2026-09-06T10:03:30.000Z",
            model="claude-haiku-4-5",
            effort="low",
            text="Surveyed.",
        ),
    )

    delegated = [
        unit
        for unit in capture.units("s", "claude-code", str(transcript))
        if unit.delegated
    ]

    assert len(delegated) == 1
    assert delegated[0].model == "claude-haiku-4-5"
    assert delegated[0].deliberation == "low"
    assert delegated[0].instruction_excerpt == "survey the tree"


def test_the_token_categories_arrive_under_the_names_a_measurement_prices(
    tmp_path: Path,
) -> None:
    """A Harness's own spelling is translated once, here, and never again."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )

    tokens = capture.units("s", "claude-code", str(transcript))[0].tokens

    assert tokens == {
        "input": 12.0,
        "cache_read": 120000.0,
        "cache_write": 3400.0,
        "output": 900.0,
        "reasoning": 250.0,
    }


def test_an_unreported_token_category_stays_null(tmp_path: Path) -> None:
    """A zero is a reading and an absence is not."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:05:00.000Z",
            text="Done.",
            usage={"input_tokens": 5, "output_tokens": 400},
        ),
    )

    tokens = capture.units("s", "claude-code", str(transcript))[0].tokens

    assert tokens["reasoning"] is None
    assert tokens["cache_read"] is None
    assert tokens["output"] == 400.0


# --- The free signals --------------------------------------------------------


def test_an_interrupted_unit_is_marked_as_one(tmp_path: Path) -> None:
    """Whoever stopped it, the Unit says so rather than looking finished."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:02:00.000Z", tools=[_call("Bash", command="rm -rf x")]
        ),
        _result("2026-09-06T10:05:00.000Z", stopped=True),
    )

    assert capture.units("s", "claude-code", str(transcript))[0].signals["interrupted"]


def test_an_api_failure_is_marked_as_errored(tmp_path: Path) -> None:
    """A Harness that failed the turn established nothing about the model."""

    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant("2026-09-06T10:05:00.000Z", api_error=True, text=""),
    )

    assert capture.units("s", "claude-code", str(transcript))[0].signals["errored"]


def test_tests_that_ran_and_came_back_clean_are_recorded_as_passing(
    tmp_path: Path,
) -> None:
    """The closest thing to an external checker an ordinary session contains."""

    transcript = _transcript(
        tmp_path,
        _user("fix it", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:04:00.000Z",
            text="Green.",
            tools=[_call("Bash", command="uv run pytest tests/")],
        ),
        _result("2026-09-06T10:05:00.000Z"),
    )

    signals = capture.units("s", "claude-code", str(transcript))[0].signals

    assert signals["tests_ran"] is True
    assert signals["tests_passed"] is True


def test_a_failing_test_run_is_not_recorded_as_passing(tmp_path: Path) -> None:
    """The tool result's own error flag is read, and its output never is."""

    transcript = _transcript(
        tmp_path,
        _user("fix it", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:04:00.000Z",
            text="Red.",
            tools=[_call("Bash", command="uv run pytest tests/")],
        ),
        _result("2026-09-06T10:05:00.000Z", is_error=True),
    )

    signals = capture.units("s", "claude-code", str(transcript))[0].signals

    assert signals["tests_ran"] is True
    assert signals["tests_passed"] is False


def test_an_instruction_given_again_marks_the_answer_that_preceded_it(
    tmp_path: Path,
) -> None:
    """The cheapest evidence there is that the first answer was not good enough."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z", "do it"),
        *_long_unit("2026-09-06T11:00:00.000Z", "2026-09-06T11:05:00.000Z", "do it"),
    )

    found = capture.units("s", "claude-code", str(transcript))

    assert found[0].signals["retried"] is True
    assert found[1].signals["retried"] is False


# --- What reaches disk -------------------------------------------------------


def test_a_finished_session_writes_its_units_and_forgets_the_draft(
    tmp_path: Path,
) -> None:
    """The session's last event is where a Unit is derived and nowhere else."""

    grader = _grader()
    data = tmp_path / "data"
    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )

    capture.hook(data, "SessionStart", {"session_id": "s", "harness": "claude-code"})
    assert list((data / "capture" / "drafts").glob("*.json"))

    answered = capture.hook(
        data,
        "SessionEnd",
        {
            "session_id": "s",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )

    assert answered["ok"] is True
    assert len(answered["recorded"]) == 1
    assert len(capture.pending(data)) == 1
    assert not list((data / "capture" / "drafts").glob("*.json"))
    assert grader.passes == [data]


def test_the_same_finished_session_answered_twice_adds_nothing(tmp_path: Path) -> None:
    """A lifecycle signal redelivered adds nothing the second time."""

    _grader()
    data = tmp_path / "data"
    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )
    payload = {
        "session_id": "s",
        "harness": "claude-code",
        "transcript_path": str(transcript),
    }

    capture.hook(data, "SessionEnd", payload)
    second = capture.hook(data, "SessionEnd", payload)

    assert second["recorded"] == []
    assert len(second["skipped"]) == 1
    assert len(capture.pending(data)) == 1


def test_a_harness_with_no_record_this_module_can_split_writes_no_unit(
    tmp_path: Path,
) -> None:
    """An absence is an absence, never a row with everything null in it."""

    _grader()
    data = tmp_path / "data"

    answered = capture.hook(data, "SessionEnd", {"session_id": "s", "harness": "codex"})

    assert answered["ok"] is True
    assert capture.pending(data) == []


def test_no_forbidden_content_reaches_a_pending_unit(tmp_path: Path) -> None:
    """A transcript carries far more than a Unit is allowed to hold."""

    _grader()
    data = tmp_path / "data"
    transcript = _transcript(
        tmp_path,
        _user("do the work", "2026-09-06T10:00:00.000Z"),
        _assistant(
            "2026-09-06T10:05:00.000Z",
            text="Done.",
            tools=[_call("Bash", command="cat /Users/secret/credentials.txt")],
        ),
    )

    capture.hook(
        data,
        "SessionEnd",
        {
            "session_id": "/Users/thomas/Projects/private-client",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )

    written = (data / "pending.jsonl").read_text(encoding="utf-8")
    for forbidden in ("credentials", "/Users/secret", "private-client", "cat "):
        assert forbidden not in written, forbidden


def test_the_transcript_path_never_reaches_a_persisted_draft(tmp_path: Path) -> None:
    """It is read to open one file and discarded inside the same invocation."""

    data = tmp_path / "data"

    capture.hook(
        data,
        "SessionStart",
        {
            "session_id": "s",
            "harness": "claude-code",
            "transcript_path": "/Users/thomas/.claude/projects/x/y.jsonl",
        },
    )

    drafts = list((data / "capture" / "drafts").glob("*.json"))
    assert "transcript_path" not in drafts[0].read_text(encoding="utf-8")


def test_the_session_identity_is_opaque(tmp_path: Path) -> None:
    """A raw session id is a path or a workspace name often enough."""

    _grader()
    data = tmp_path / "data"
    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )

    capture.hook(
        data,
        "SessionEnd",
        {
            "session_id": "/Users/thomas/Projects/skills",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )

    unit = capture.pending(data)[0]
    assert "/Users" not in unit["session"]
    assert unit["session"] == capture._opaque("/Users/thomas/Projects/skills")


# --- Status and purge --------------------------------------------------------


def test_status_reports_what_is_pending_and_when_the_grader_last_ran(
    tmp_path: Path,
) -> None:
    """The one surface any of this is reported on."""

    _grader()
    data = tmp_path / "data"
    data.mkdir()
    (data / "pending.jsonl").write_text('{"unit_id": "one"}\n', encoding="utf-8")
    (data / "grader.json").write_text(
        json.dumps({"last_run_at": "2026-09-06T09:00:00Z"}), encoding="utf-8"
    )

    reported = capture.status(data, tmp_path / "home")

    measures = {row["harness"]: row["measurements"] for row in reported["harnesses"]}

    assert reported["pending"] == 1
    assert reported["grader_last_ran_at"] == "2026-09-06T09:00:00Z"
    assert measures["claude-code"] is True
    assert measures["codex"] is False


def test_a_grader_that_has_never_run_is_reported_as_such(tmp_path: Path) -> None:
    """A store that stays empty must not look like one nothing has read."""

    data = tmp_path / "data"
    data.mkdir()

    assert capture.status(data, tmp_path / "home")["grader_last_ran_at"] is None


def test_purge_previews_and_then_removes_the_pending_units(tmp_path: Path) -> None:
    """The Harness hooks stay installed; what was captured does not."""

    data = tmp_path / "data"
    data.mkdir()
    (data / "pending.jsonl").write_text('{"unit_id": "one"}\n', encoding="utf-8")
    (data / "capture" / "drafts").mkdir(parents=True)
    (data / "capture" / "drafts" / "x.json").write_text("{}", encoding="utf-8")

    preview = capture.purge_paths(data)
    assert [entry["present"] for entry in preview[:2]] == [True, True]
    assert preview[1]["count"] == 1

    capture.purge(data)

    assert not (data / "pending.jsonl").exists()
    assert not (data / "capture").exists()


def test_what_the_retired_design_left_behind_is_previewed_and_removed(
    tmp_path: Path,
) -> None:
    """A file no version of this Skill writes any more is one nothing reads.

    Seventeen of them were left in every data directory by the design this one
    replaced. Harmless, and permanent: no verb knew they existed, so they would
    have sat there for as long as the Skill stayed installed.
    """

    data = tmp_path / "data"
    data.mkdir()
    (data / "standing-policy.json").write_text("{}", encoding="utf-8")
    (data / "run-observations.jsonl").write_text('{"a": 1}\n', encoding="utf-8")
    (data / "measurements.jsonl").write_text('{"kept": true}\n', encoding="utf-8")

    previewed = {entry["path"]: entry for entry in capture.purge_paths(data)}
    assert previewed[str(data / "standing-policy.json")]["present"] is True
    assert previewed[str(data / "config.json")]["present"] is False

    capture.purge(data)

    assert not (data / "standing-policy.json").exists()
    assert not (data / "run-observations.jsonl").exists()

    # The ledger is not this verb's to remove: `reset --evidence` names it
    # separately, and a purge that took it would take the whole store with it.
    assert (data / "measurements.jsonl").exists()


def test_status_says_how_much_of_a_retired_design_is_still_sitting_there(
    tmp_path: Path,
) -> None:
    """Told, or the tidying is a verb nobody knows to run."""

    data = tmp_path / "data"
    data.mkdir()
    (data / "config.json").write_text("{}", encoding="utf-8")
    (data / "alias-bindings.jsonl").write_text("", encoding="utf-8")

    assert capture.status(data, tmp_path / "home")["retired"] == 2


# --- What must survive inside somebody else's session ------------------------


def test_default_data_uses_the_shared_kntnt_skill_directory() -> None:
    """Keep model-selector's user data under the shared Kntnt root."""

    assert capture.default_data() == Path.home() / ".kntnt" / "model-selector"


def test_simultaneous_sessions_keep_separate_drafts(tmp_path: Path) -> None:
    """Two sessions at once are two drafts and two identities, never one."""

    _grader()
    data = tmp_path / "data"
    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )

    capture.hook(data, "SessionStart", {"session_id": "one", "harness": "claude-code"})
    capture.hook(data, "SessionStart", {"session_id": "two", "harness": "claude-code"})
    assert len(list((data / "capture" / "drafts").glob("*.json"))) == 2

    for session in ("one", "two"):
        capture.hook(
            data,
            "SessionEnd",
            {
                "session_id": session,
                "harness": "claude-code",
                "transcript_path": str(transcript),
            },
        )

    assert not list((data / "capture" / "drafts").glob("*.json"))
    assert len({unit["session"] for unit in capture.pending(data)}) == 2


def test_capture_writes_nothing_outside_its_own_data_directory(
    tmp_path: Path,
) -> None:
    """A whole session's capture touches the selected directory and nothing else."""

    _grader()
    data = tmp_path / "data"
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )

    capture.hook(data, "SessionStart", {"session_id": "s", "harness": "claude-code"})
    capture.hook(
        data,
        "SessionEnd",
        {
            "session_id": "s",
            "harness": "claude-code",
            "transcript_path": str(transcript),
        },
    )

    assert list(elsewhere.iterdir()) == []
    written = {path.relative_to(tmp_path).parts[0] for path in tmp_path.rglob("*")}
    assert written <= {"data", "elsewhere", "session.jsonl"}


def test_naming_no_harness_installs_into_every_supported_one(tmp_path: Path) -> None:
    """Naming no Harness means every Harness an adapter exists for."""

    report = capture.install(
        tmp_path / "data", tmp_path / "home", [], ["uv", "run", "hook"]
    )

    assert len(report["installed"]) == 3
    assert {entry["status"] for entry in report["installed"]} == {"installed"}
    assert report["unsupported"]["count"] == 0


def test_an_unsupported_harness_is_collapsed_to_a_single_count(
    tmp_path: Path,
) -> None:
    """A Harness no adapter exists for is never attempted, never one row each.

    A caller naming Detected Harnesses in bulk would otherwise get one
    Unsatisfied row per Harness this collection has no adapter for — seventy
    of them — burying the outcome that matters (#223 decision 3).
    """

    report = capture.install(
        tmp_path / "data", tmp_path / "home", ["cursor", "windsurf"], ["uv", "run"]
    )

    assert report["installed"] == []
    assert report["unsupported"] == {
        "count": 2,
        "supported": ["claude-code", "codex", "opencode"],
    }


def test_a_gated_harness_is_never_reported_healthy(tmp_path: Path) -> None:
    """Codex's own trust review is a gate this collection never forges past."""

    data = tmp_path / "data"
    capture.install(data, tmp_path / "home", ["codex"], ["uv", "run", "hook"])

    reported = {
        entry["harness"]: entry
        for entry in capture.status(data, tmp_path / "home")["harnesses"]
    }

    assert reported["codex"]["status"] == "gated"


def test_the_hook_path_is_local_only_and_bounded() -> None:
    """Provable from what this module can reach rather than from what it does.

    A module that cannot open a socket, cannot start a process, cannot start a
    thread and holds no waiting call cannot break the session it runs inside,
    however it is invoked.
    """

    source = (SCRIPTS / "capture.py").read_text(encoding="utf-8")

    for unreachable in (
        "import subprocess",
        "import threading",
        "import asyncio",
        "import socket",
        "import urllib",
        "import requests",
        "time.sleep",
    ):
        assert unreachable not in source, unreachable


def test_the_hook_path_is_fail_open(tmp_path: Path) -> None:
    """A capture that breaks a session is worse than no capture."""

    answered = capture.hook(tmp_path / "nowhere", "SessionEnd", "not a payload at all")

    assert answered["ok"] is True

    # A payload that names a session but a store that cannot be written is the
    # failure the swallow exists for, and it still exits clean.
    blocked = tmp_path / "blocked"
    blocked.write_text("not a directory", encoding="utf-8")
    broken = capture.hook(blocked, "SessionStart", {"session_id": "s"})

    assert broken["ok"] is False
    assert broken["fail_open"] is True


def test_the_hook_leaves_the_harnesss_own_channel_empty(
    tmp_path: Path, monkeypatch: Any
) -> None:
    """A Harness reads its own hook's standard output as its own protocol (#259)."""

    out, err = io.StringIO(), io.StringIO()
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"session_id": "s"})))
    monkeypatch.setattr(sys, "stdout", out)
    monkeypatch.setattr(sys, "stderr", err)

    code = capture.main(["hook", "--data", str(tmp_path), "--event", "SessionStart"])

    assert code == 0
    assert out.getvalue() == ""
    assert json.loads(err.getvalue())["ok"] is True


def test_the_ownership_identity_travels_inside_the_command(tmp_path: Path) -> None:
    """Removal is surgical because the owner is in what a Harness runs."""

    report = capture.install(
        tmp_path / "data", tmp_path / "home", ["claude-code"], ["uv", "run", "hook"]
    )

    assert report["installed"][0]["harness"] == "claude-code"
    settings = json.loads(
        (tmp_path / "home" / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    assert capture.owner() in json.dumps(settings)


def test_the_installed_hook_carries_the_data_directory_it_was_installed_for(
    tmp_path: Path,
) -> None:
    """A hook installed for one directory and run against another writes nowhere useful."""

    command = capture._hook_command([], tmp_path / "elsewhere")

    assert command[:2] == ["uv", "run"]
    assert command[-2:] == ["--data", str(tmp_path / "elsewhere")]


def test_a_lifecycle_payload_is_copied_onto_the_allow_list(tmp_path: Path) -> None:
    """Nothing forbidden enters by sitting beside something wanted."""

    cleaned = capture._clean(
        {
            "session_id": "s",
            "harness": "claude-code",
            "transcript": "the whole conversation",
            "prompt": "a secret",
            "cwd": "/Users/thomas/Projects/private",
        }
    )

    assert cleaned == {"session_id": "s", "harness": "claude-code"}


def test_the_opencode_envelope_still_yields_a_session_identity() -> None:
    """OpenCode's plugin hands its event object on unmodified, nested id and all."""

    created = capture._normalized(
        {"type": "session.created", "properties": {"info": {"id": "abc"}}}
    )
    idle = capture._normalized(
        {"type": "session.idle", "properties": {"sessionID": "abc"}}
    )

    assert created["session_id"] == "abc"
    assert idle["session_id"] == "abc"


def test_a_harness_naming_the_event_in_its_payload_is_understood() -> None:
    """Claude Code and Codex hand the moment over on stdin rather than on argv."""

    assert capture._moment("", {"hook_event_name": "SessionEnd"}) == "SessionEnd"
    assert capture._moment("", {"eventName": "SessionEnd"}) == "SessionEnd"
    assert capture._moment("", {"type": "session.deleted"}) == "session.deleted"
    assert capture._moment("Stop", {"type": "session.idle"}) == "Stop"


def test_a_subagent_briefed_with_an_attempt_is_that_attempt(tmp_path: Path) -> None:
    """A routed builder's row and its verdict's row are one attempt.

    Orchestrate files a `checker` row under the identity the router decided,
    carrying the verdict's grade and no tokens. This read of the same
    builder's transcript carries the tokens and no verdict. The brief's first
    line is what says the two are one build rather than two (issue #291).
    """

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )
    _subagent(
        transcript,
        "aaa",
        {
            "type": "user",
            "timestamp": "2026-09-06T10:01:00.000Z",
            "isSidechain": True,
            "message": {
                "role": "user",
                "content": f"{attempt_line('build-291')}\n\nYou are building one ticket.",
            },
        },
        _assistant("2026-09-06T10:03:30.000Z", text="Built."),
    )

    delegated = [
        unit
        for unit in capture.units("s", "claude-code", str(transcript))
        if unit.delegated
    ]

    assert [unit.unit_id for unit in delegated] == ["build-291"]


def test_a_subagent_nobody_routed_keeps_the_identity_capture_computes(
    tmp_path: Path,
) -> None:
    """Only a brief that names an attempt has one; everything else is hashed."""

    transcript = _transcript(
        tmp_path,
        *_long_unit("2026-09-06T10:00:00.000Z", "2026-09-06T10:05:00.000Z"),
    )
    _subagent(
        transcript,
        "aaa",
        {
            "type": "user",
            "timestamp": "2026-09-06T10:01:00.000Z",
            "isSidechain": True,
            "message": {"role": "user", "content": "survey the tree"},
        },
        _assistant("2026-09-06T10:03:30.000Z", text="Surveyed."),
    )

    delegated = [
        unit
        for unit in capture.units("s", "claude-code", str(transcript))
        if unit.delegated
    ]

    assert len(delegated) == 1
    assert delegated[0].unit_id.startswith("unit-")
