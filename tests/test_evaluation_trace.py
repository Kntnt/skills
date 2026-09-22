"""The trace index an evaluator reads a Claude-native evidence packet through."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
HARNESS: Path = REPO_ROOT / "docs" / "evaluation" / "editorial-388" / "harness"


def _module() -> Any:
    """Load the indexer under the name the runner beside it imports it by."""

    if "trace_index" in sys.modules:
        return sys.modules["trace_index"]
    spec = importlib.util.spec_from_file_location(
        "trace_index", HARNESS / "trace_index.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["trace_index"] = module
    spec.loader.exec_module(module)
    return module


trace_index = _module()


def _user(text: Any, **extra: Any) -> dict[str, Any]:
    """One user line of a Claude Code transcript."""

    return {
        "type": "user",
        "timestamp": "2026-09-22T06:00:00.000Z",
        "sessionId": "session-1",
        "message": {"role": "user", "content": text},
        **extra,
    }


def _assistant(*blocks: dict[str, Any], **extra: Any) -> dict[str, Any]:
    """One assistant turn carrying the given content blocks."""

    return {
        "type": "assistant",
        "timestamp": "2026-09-22T06:00:01.000Z",
        "effort": "high",
        "message": {
            "role": "assistant",
            "model": "claude-opus-5",
            "content": [*blocks],
        },
        **extra,
    }


def _call(tool: str, arguments: dict[str, Any], identifier: str) -> dict[str, Any]:
    """One tool call as an assistant message records it."""

    return {"type": "tool_use", "id": identifier, "name": tool, "input": arguments}


def _result(identifier: str, text: str, error: bool = False) -> dict[str, Any]:
    """One tool result as the user line after the call records it."""

    return {
        "type": "user",
        "timestamp": "2026-09-22T06:00:02.000Z",
        "message": {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": identifier,
                    "content": text,
                    "is_error": error,
                }
            ],
        },
    }


def _packet(
    root: Path,
    parent: list[dict[str, Any]] | None,
    children: dict[str, tuple[dict[str, Any], list[dict[str, Any]]]] | None = None,
    result: dict[str, Any] | None = None,
) -> Path:
    """Write one evidence packet holding the given transcripts and outcome."""

    transcripts = root / "transcripts"
    transcripts.mkdir(parents=True)
    if parent is not None:
        (transcripts / "parent.jsonl").write_text(
            "".join(json.dumps(line) + "\n" for line in parent)
        )
    for identity, (meta, lines) in (children or {}).items():
        directory = transcripts / "subagents"
        directory.mkdir(exist_ok=True)
        (directory / f"agent-{identity}.meta.json").write_text(json.dumps(meta))
        (directory / f"agent-{identity}.jsonl").write_text(
            "".join(json.dumps(line) + "\n" for line in lines)
        )
    (root / "result.json").write_text(
        json.dumps(
            result or {"returncode": 0, "timed_out": False, "interrupted": False}
        )
    )
    return root


def test_the_session_agent_carries_its_instruction_and_the_seat_it_ran_on(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write --genre=column --language=sv --output=response source.md"),
            _assistant({"type": "text", "text": "Done."}),
        ],
    )

    trace = trace_index.read_packet(packet)

    session = trace["agents"][0]
    assert session["agent_id"] == "session-1"
    assert session["role"] == "session"
    assert session["parent_agent_id"] is None
    assert (
        session["instruction"]
        == "/write --genre=column --language=sv --output=response source.md"
    )
    assert session["seats"] == [
        {"model": "claude-opus-5", "deliberation": "high", "turns": 1}
    ]


def test_an_injected_skill_body_is_recorded_as_the_installation_it_came_from(
    tmp_path: Path,
) -> None:
    body = "Base directory for this skill: /run/home/.claude/skills/write\n\n# write\n"
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _user(
                [{"type": "text", "text": body}],
                isMeta=True,
                turnCompanion=True,
            ),
            _assistant({"type": "text", "text": "Done."}),
        ],
    )

    trace = trace_index.read_packet(packet)

    loaded = trace["agents"][0]["skill_bodies"]
    assert [entry["base_directory"] for entry in loaded] == [
        "/run/home/.claude/skills/write"
    ]
    assert loaded[0]["chars"] == len(body)


def test_a_read_call_establishes_one_file_exactly(tmp_path: Path) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(
                _call("Read", {"file_path": "/lib/references/editorial/base.md"}, "t1")
            ),
            _result("t1", "1\t# Base\n"),
        ],
    )

    trace = trace_index.read_packet(packet)

    assert trace["agents"][0]["file_activity"] == [
        {
            "ordinal": 1,
            "at": "2026-09-22T06:00:01.000Z",
            "tool": "Read",
            "path": "/lib/references/editorial/base.md",
            "access": "read",
            "established_from": "tool-argument",
            "exact": True,
            "command": None,
        }
    ]


def test_a_shell_command_naming_one_file_establishes_a_shell_mediated_read(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(
                _call(
                    "Bash", {"command": "cat /lib/references/editorial/base.md"}, "t1"
                )
            ),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = trace["agents"][0]["file_activity"]
    assert [(item["path"], item["exact"]) for item in activity] == [
        ("/lib/references/editorial/base.md", True)
    ]
    assert activity[0]["established_from"] == "shell-command"
    assert activity[0]["command"] == "cat /lib/references/editorial/base.md"


def test_a_globbed_or_recursive_command_names_a_set_rather_than_a_file(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(_call("Bash", {"command": "cat /lib/genres/*.md"}, "t1")),
            _assistant(_call("Bash", {"command": "grep -r angle /lib/genres"}, "t2")),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = trace["agents"][0]["file_activity"]
    assert [item["exact"] for item in activity] == [False, False]


def test_a_search_tool_names_a_set_rather_than_a_file(tmp_path: Path) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(_call("Glob", {"pattern": "*.md", "path": "/lib/genres"}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = trace["agents"][0]["file_activity"]
    assert activity[0]["access"] == "search"
    assert activity[0]["exact"] is False
    assert activity[0]["path"] == "/lib/genres"


def test_a_delegation_is_matched_to_its_child_by_the_call_that_started_it(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(
                _call(
                    "Agent",
                    {
                        "description": "Correction round 1",
                        "prompt": "Repair the findings below.",
                        "subagent_type": "general-purpose",
                    },
                    "toolu_01",
                )
            ),
        ],
        {
            "abc123": (
                {
                    "agentType": "general-purpose",
                    "description": "Correction round 1",
                    "toolUseId": "toolu_01",
                    "spawnDepth": 1,
                },
                [
                    _user("Repair the findings below."),
                    _assistant({"type": "text", "text": "Done."}),
                ],
            )
        },
    )

    trace = trace_index.read_packet(packet)

    delegation = trace["agents"][0]["delegations"][0]
    assert delegation["child_agent_id"] == "abc123"
    assert delegation["prompt"] == "Repair the findings below."
    child = trace["agents"][1]
    assert child["role"] == "subagent"
    assert child["parent_agent_id"] == trace["agents"][0]["agent_id"]
    assert child["spawn_depth"] == 1
    assert trace["status"]["status"] == "complete"


def test_a_delegation_whose_child_transcript_is_absent_is_incomplete(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(
                _call("Agent", {"prompt": "Repair.", "description": "c"}, "toolu_01")
            ),
        ],
    )

    trace = trace_index.read_packet(packet)

    assert trace["agents"][0]["delegations"][0]["child_agent_id"] is None
    assert trace["status"]["status"] == "incomplete"
    assert "delegation-without-child" in trace["status"]["reasons"]
    assert trace["status"]["delegations_without_child"] == ["toolu_01"]


def test_a_child_transcript_no_call_started_is_incomplete(tmp_path: Path) -> None:
    packet = _packet(
        tmp_path / "packet",
        [_user("/redline input.md"), _assistant({"type": "text", "text": "Done."})],
        {
            "orphan1": (
                {"agentType": "general-purpose", "toolUseId": "toolu_09"},
                [_user("Repair.")],
            )
        },
    )

    trace = trace_index.read_packet(packet)

    assert trace["status"]["status"] == "incomplete"
    assert "child-without-delegation" in trace["status"]["reasons"]
    assert trace["status"]["children_without_delegation"] == ["orphan1"]


def test_a_truncated_transcript_is_counted_and_reported_incomplete(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [_user("/write source.md"), _assistant({"type": "text", "text": "Done."})],
    )
    with (packet / "transcripts" / "parent.jsonl").open("a") as transcript:
        transcript.write('{"type": "assistant", "message": {"content": [')

    trace = trace_index.read_packet(packet)

    assert trace["status"]["unparsable_lines"] == {"transcripts/parent.jsonl": 1}
    assert "unparsable-line" in trace["status"]["reasons"]
    assert trace["agents"][0]["instruction"] == "/write source.md"


def test_an_absent_parent_transcript_is_incomplete_and_keeps_the_children(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        None,
        {
            "abc123": (
                {"agentType": "general-purpose", "toolUseId": "toolu_01"},
                [_user("Repair.")],
            )
        },
    )

    trace = trace_index.read_packet(packet)

    assert trace["status"]["parent_transcript"] == "missing"
    assert "parent-transcript-missing" in trace["status"]["reasons"]
    assert [agent["agent_id"] for agent in trace["agents"]] == ["abc123"]


def test_an_interrupted_run_is_incomplete_and_retains_what_it_recorded(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [_user("/write source.md"), _assistant({"type": "text", "text": "Partial"})],
        result={"returncode": 143, "timed_out": True, "interrupted": True},
    )

    trace = trace_index.read_packet(packet)

    assert trace["status"]["status"] == "incomplete"
    assert "run-did-not-finish" in trace["status"]["reasons"]
    assert trace["agents"][0]["instruction"] == "/write source.md"


def test_the_status_is_read_from_the_recorded_activity_and_never_from_the_reply(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(
                _call("Agent", {"prompt": "Repair.", "description": "c"}, "toolu_01")
            ),
            _assistant(
                {
                    "type": "text",
                    "text": "The correction agent ran and the Proofread pass completed.",
                }
            ),
        ],
    )
    (packet / "response.txt").write_text(
        "The correction agent ran and the Proofread pass completed."
    )

    trace = trace_index.read_packet(packet)

    assert trace["status"]["status"] == "incomplete"


def test_the_index_is_written_beside_the_transcripts_it_reads(tmp_path: Path) -> None:
    packet = _packet(
        tmp_path / "packet",
        [_user("/write source.md"), _assistant({"type": "text", "text": "Done."})],
    )

    assert trace_index.main([str(packet)]) == 0

    written = json.loads((packet / "trace-index.json").read_text())
    status = json.loads((packet / "trace-status.json").read_text())
    assert written["agents"][0]["instruction"] == "/write source.md"
    assert status["status"] == "complete"


def test_a_shim_command_names_the_script_the_assignment_above_it_settles(
    tmp_path: Path,
) -> None:
    command = (
        'export HERE="/run/skills/write"\n'
        "export TMPDIR=$(mktemp -d)\n"
        "UV_NO_CACHE=1 uv run \"$HERE/scripts/invoke.py\" <<'EOF'\n"
        "--genre=column source.md\nEOF\nstatus=$?\nexit $status"
    )
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(_call("Bash", {"command": command}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = {
        item["path"]: item["exact"] for item in trace["agents"][0]["file_activity"]
    }
    assert activity == {
        "/run/skills/write": True,
        "/run/skills/write/scripts/invoke.py": True,
    }


def test_shell_punctuation_and_redirections_are_not_paths(tmp_path: Path) -> None:
    command = 'cd "/run/skills/write"; cat references/source-check.md 2>/dev/null'
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(_call("Bash", {"command": command}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    assert [item["path"] for item in trace["agents"][0]["file_activity"]] == [
        "/run/skills/write",
        "references/source-check.md",
    ]


def test_a_variable_assigned_in_the_same_command_is_expanded(tmp_path: Path) -> None:
    command = (
        'LIB="/run/skills/kntnt/library"\n'
        'cat "$LIB/references/editorial/base.md" "${LIB}/references/delivery.md"'
    )
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(_call("Bash", {"command": command}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = [
        (item["path"], item["exact"]) for item in trace["agents"][0]["file_activity"]
    ]
    assert activity == [
        ("/run/skills/kntnt/library", True),
        ("/run/skills/kntnt/library/references/editorial/base.md", True),
        ("/run/skills/kntnt/library/references/delivery.md", True),
    ]
    assert trace["agents"][0]["file_activity"][1]["command"] == command


def test_a_variable_no_assignment_in_the_command_settles_stays_unresolved(
    tmp_path: Path,
) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(_call("Bash", {"command": 'cat "$LIB/base.md"'}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    entry = trace["agents"][0]["file_activity"][0]
    assert entry["path"] == "$LIB/base.md"
    assert entry["exact"] is False


def test_a_markdown_link_inside_a_command_is_not_a_path(tmp_path: Path) -> None:
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(
                _call("Bash", {"command": "grep 'form](https://a.invalid/b)' x"}, "t1")
            ),
        ],
    )

    trace = trace_index.read_packet(packet)

    assert trace["agents"][0]["file_activity"] == []


def test_a_variable_a_command_substitution_settles_is_left_as_written(
    tmp_path: Path,
) -> None:
    command = 'MECHDIR=$(cat /tmp/where.txt)\ncat "$MECHDIR/artifact.md"'
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/redline input.md"),
            _assistant(_call("Bash", {"command": command}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    activity = [
        (item["path"], item["exact"]) for item in trace["agents"][0]["file_activity"]
    ]
    assert ("$MECHDIR/artifact.md", False) in activity


def test_a_heredoc_body_is_the_text_written_and_not_paths_read(tmp_path: Path) -> None:
    command = (
        "cat > /run/scratch/report.md <<'REPORT_EOF'\n"
        "1.1 Person/number: the draft says er/ni where the source says du.\n"
        "See https://example.invalid/svale/intresse for the route.\n"
        "REPORT_EOF\n"
        "wc -l /run/scratch/report.md"
    )
    packet = _packet(
        tmp_path / "packet",
        [
            _user("/write source.md"),
            _assistant(_call("Bash", {"command": command}, "t1")),
        ],
    )

    trace = trace_index.read_packet(packet)

    assert [item["path"] for item in trace["agents"][0]["file_activity"]] == [
        "/run/scratch/report.md",
        "/run/scratch/report.md",
    ]
