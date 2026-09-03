"""Owned cross-Harness integrations shipped by the Collection Library."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any, cast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
LIBRARY: Path = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts"

OWNER = "kntnt.model-selector.capture"
COMMAND = ["uv", "run", "/skills/model-selector/scripts/capture.py", "hook"]


def _load() -> Any:
    """Load the shipped integration module from its installed path."""

    path = LIBRARY / "integrations.py"
    spec = importlib.util.spec_from_file_location("kntnt_integrations", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _settings(root: Path) -> dict[str, Any]:
    loaded = (root / ".claude" / "settings.json").read_text(encoding="utf-8")
    return cast(dict[str, Any], json.loads(loaded))


def _codex_hooks(root: Path) -> dict[str, Any]:
    loaded = (root / ".codex" / "hooks.json").read_text(encoding="utf-8")
    return cast(dict[str, Any], json.loads(loaded))


def test_every_supported_harness_installs_its_own_shape(tmp_path: Path) -> None:
    """Each adapter writes the integration its own Harness actually reads."""

    module = _load()
    for harness in ("claude-code", "codex", "opencode"):
        root = tmp_path / harness
        result = module.install(OWNER, harness, root, COMMAND)
        assert result["status"] == "installed", result
        assert result["harness"] == harness

    assert _settings(tmp_path / "claude-code")["hooks"]["SessionStart"]

    # Codex's `hooks.json` deserializes through its own `HookEventsToml`,
    # confirmed live against `codex app-server`'s `hooks/list`: PascalCase
    # event keys, the same as Claude Code's `settings.json`. `sessionStart` /
    # `stop` / `sessionEnd` is a different surface — the camelCase
    # `HookEventName` `hooks/list` itself reports back — and is silently
    # dropped when written into the config file.
    assert _codex_hooks(tmp_path / "codex")["hooks"]["Stop"]

    plugin = tmp_path / "opencode" / ".config" / "opencode" / "plugins"
    assert list(plugin.glob("*.js"))


def test_codex_hooks_use_the_harnesss_own_pascal_case_event_names(
    tmp_path: Path,
) -> None:
    """Codex's `hooks.json` is keyed by the same event names Claude Code uses.

    `HookEventsToml` — the struct `~/.codex/hooks.json` deserializes into — is
    confirmed live (`codex app-server`, `initialize` + `hooks/list`) to accept
    `SessionStart` / `Stop` / `SessionEnd`, PascalCase, and to silently ignore
    the camelCase spelling: a hook count of zero and no warning, not a schema
    error. That camelCase spelling names a different struct entirely, the
    app-server protocol's own `HookEventName`, which is what `hooks/list`
    itself reports back — a normalized runtime view, never the config file's
    own shape.
    """

    module = _load()
    module.install(OWNER, "codex", tmp_path, COMMAND)
    written = _codex_hooks(tmp_path)

    assert set(written["hooks"]) == {"SessionStart", "Stop", "SessionEnd"}


def test_codex_hook_entries_match_the_harnesss_own_matcher_group(
    tmp_path: Path,
) -> None:
    """A Codex entry is the same nested matcher group Claude Code writes.

    Confirmed live: a PascalCase key holding this nested `{"hooks": [...]}`
    shape registers a hook (`hooks/list` reports it, `trustStatus` included);
    the same key holding the flat `handlerType`/`command` shape the
    app-server protocol's own `hooks/list` reports back registers nothing —
    that flat shape belongs to the normalized runtime view, not to what
    `HookEventsToml` accepts on disk.
    """

    module = _load()
    module.install(OWNER, "codex", tmp_path, COMMAND)
    entry = _codex_hooks(tmp_path)["hooks"]["SessionStart"][0]

    assert entry["hooks"][0]["type"] == "command"
    assert OWNER in entry["hooks"][0]["command"]
    assert "handlerType" not in entry


def test_an_unsupported_harness_reports_an_unsatisfied_capability(
    tmp_path: Path,
) -> None:
    """A Harness whose lifecycle cannot carry the contract is never called healthy."""

    module = _load()
    result = module.install(OWNER, "cursor", tmp_path, COMMAND)

    assert result["status"] == "unsatisfied"
    assert result["capability"]
    assert not any(tmp_path.iterdir())


def test_installation_is_idempotent(tmp_path: Path) -> None:
    """Installing twice converges on the same disk state rather than doubling."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    first = _settings(tmp_path)
    module.install(OWNER, "claude-code", tmp_path, COMMAND)

    assert _settings(tmp_path) == first
    entries = _settings(tmp_path)["hooks"]["SessionStart"]
    assert len(entries) == 1


def test_installation_preserves_an_unrelated_hook(tmp_path: Path) -> None:
    """Another owner's hook is left exactly as it was."""

    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    theirs: dict[str, Any] = {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": "their-own-thing"}]}
            ]
        },
        "model": "opus",
    }
    settings.write_text(json.dumps(theirs), encoding="utf-8")

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    after = _settings(tmp_path)

    assert after["model"] == "opus"
    assert theirs["hooks"]["SessionStart"][0] in after["hooks"]["SessionStart"]


def test_removal_takes_only_what_this_owner_installed(tmp_path: Path) -> None:
    """Removal is surgical: unrelated hooks and settings survive it."""

    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True)
    theirs: dict[str, Any] = {
        "hooks": {
            "SessionStart": [
                {"hooks": [{"type": "command", "command": "their-own-thing"}]}
            ]
        },
        "model": "opus",
    }
    settings.write_text(json.dumps(theirs), encoding="utf-8")

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    result = module.remove(OWNER, "claude-code", tmp_path)

    assert result["status"] == "removed"
    after = _settings(tmp_path)
    assert after["model"] == "opus"
    assert after["hooks"]["SessionStart"] == theirs["hooks"]["SessionStart"]


def test_removal_is_idempotent_and_verified_from_disk(tmp_path: Path) -> None:
    """Removing what is not there is a converged state rather than a failure."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    module.remove(OWNER, "claude-code", tmp_path)
    again = module.remove(OWNER, "claude-code", tmp_path)

    assert again["status"] == "removed"
    assert again["entries"] == 0
    assert module.health(OWNER, "claude-code", tmp_path)["status"] == "absent"


def test_removal_reports_a_harness_it_could_not_clear(tmp_path: Path) -> None:
    """Partial external state is reported per Harness, never as a clean removal."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    settings = tmp_path / ".claude" / "settings.json"
    settings.write_text("{not json", encoding="utf-8")

    result = module.remove(OWNER, "claude-code", tmp_path)

    assert result["status"] == "failed"
    assert result["detail"]


def test_health_reports_each_harness_separately(tmp_path: Path) -> None:
    """Health is per Harness, and an uninstalled one is absent rather than broken."""

    module = _load()
    module.install(OWNER, "opencode", tmp_path, COMMAND)

    assert module.health(OWNER, "opencode", tmp_path)["status"] == "healthy"
    assert module.health(OWNER, "codex", tmp_path)["status"] == "absent"
    assert module.health(OWNER, "cursor", tmp_path)["status"] == "unsatisfied"


def test_codex_health_is_gated_rather_than_healthy(tmp_path: Path) -> None:
    """Codex reviews a new hook before it runs it, so a fully written Codex
    integration is reported gated, never healthy, until a human clears it.

    `HookTrustStatus` (`managed`, `untrusted`, `trusted`, `modified`) and the
    TUI's own startup review ("Hooks need review... Trust all and continue...
    Continue without trusting (hooks won't run)") both confirm the gate; this
    collection forges no trust decision on the user's behalf, so it can never
    observe a Codex hook cross into `trusted` and must never call it healthy.
    """

    module = _load()
    module.install(OWNER, "codex", tmp_path, COMMAND)
    result = module.health(OWNER, "codex", tmp_path)

    assert result["status"] == "gated"
    assert result["entries"] == 3
    assert result["detail"]
    assert "trust" in result["detail"].lower()


def test_codex_install_names_the_trust_review_the_user_clears(
    tmp_path: Path,
) -> None:
    """Installation itself says the integration is present and not yet active."""

    module = _load()
    result = module.install(OWNER, "codex", tmp_path, COMMAND)

    assert result["status"] == "installed"
    assert result["detail"]
    assert "trust" in result["detail"].lower()


def test_repair_restores_an_integration_removed_behind_our_back(
    tmp_path: Path,
) -> None:
    """Installing again after external damage converges rather than duplicating."""

    module = _load()
    module.install(OWNER, "codex", tmp_path, COMMAND)
    (tmp_path / ".codex" / "hooks.json").unlink()

    result = module.install(OWNER, "codex", tmp_path, COMMAND)

    assert result["status"] == "installed"
    assert module.health(OWNER, "codex", tmp_path)["status"] == "gated"


def test_the_owner_is_carried_in_what_is_written(tmp_path: Path) -> None:
    """Every installed entry names its owner, so removal never has to guess."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    written = json.dumps(_settings(tmp_path))

    assert OWNER in written


def test_every_supported_harness_survives_a_whole_lifecycle(tmp_path: Path) -> None:
    """Install, repair, install again, remove, remove again — for each of them."""

    module = _load()

    # Codex never reaches "healthy" here: it gates a new hook behind a trust
    # review this collection cannot and must not clear on the user's behalf.
    expected_active = {
        "claude-code": "healthy",
        "codex": "gated",
        "opencode": "healthy",
    }
    for harness in ("claude-code", "codex", "opencode"):
        root = tmp_path / harness
        assert module.install(OWNER, harness, root, COMMAND)["status"] == "installed"
        assert module.install(OWNER, harness, root, COMMAND)["status"] == "installed"
        assert module.health(OWNER, harness, root)["status"] == expected_active[harness]

        first = module.remove(OWNER, harness, root)
        second = module.remove(OWNER, harness, root)

        assert first["status"] == "removed", harness
        assert second["status"] == "removed", harness
        assert module.health(OWNER, harness, root)["status"] == "absent", harness


def test_opencode_plugin_delivers_the_event_on_standard_input(
    tmp_path: Path,
) -> None:
    """The event payload — and the session identity inside it — reaches the
    hook, and the child never inherits this process's own standard input.

    OpenCode's own event carries the session identity nested inside it
    (`session.idle`'s `properties.sessionID`, `session.created`'s
    `properties.info.id`), never on the command line; a plugin that ran the
    owned command with only `--event=<type>` discarded that identity, and one
    that left standard input unredirected handed the child the caller's own
    standard input, which a hook reading to end-of-file can block on. Bun's
    shell forwards a parent's real standard input to a spawned command unless
    a redirect names an explicit source, so `< ${...}` here is what keeps a
    fail-open hook from ever blocking on it.
    """

    module = _load()
    module.install(OWNER, "opencode", tmp_path, COMMAND)
    source = (tmp_path / ".config" / "opencode" / "plugins" / f"{OWNER}.js").read_text(
        encoding="utf-8"
    )

    assert "JSON.stringify(event)" in source
    assert "< ${" in source
    assert "--event=${event.type}`.quiet().nothrow();" not in source


def test_removal_leaves_no_empty_leavings_of_ours(tmp_path: Path) -> None:
    """An event nobody else uses goes with our entry rather than staying empty."""

    module = _load()
    module.install(OWNER, "claude-code", tmp_path, COMMAND)
    module.remove(OWNER, "claude-code", tmp_path)

    assert "hooks" not in _settings(tmp_path)


# --- The session-record reader (#225) ---------------------------------------


def _load_session_records() -> Any:
    """Load the shipped session-record reader from its installed path."""

    path = LIBRARY / "session_records.py"
    spec = importlib.util.spec_from_file_location("kntnt_session_records", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _turn(
    model: str,
    effort: str,
    *,
    timestamp: str,
    input: int = 0,
    output: int = 0,
    cache_read: int = 0,
    cache_creation: int = 0,
    thinking: int | None = None,
) -> str:
    """Provide one assistant line exactly as Claude Code's own transcript writes it."""

    usage: dict[str, Any] = {
        "input_tokens": input,
        "output_tokens": output,
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
    }
    if thinking is not None:
        usage["output_tokens_details"] = {"thinking_tokens": thinking}
    return json.dumps(
        {
            "type": "assistant",
            "isSidechain": False,
            "message": {"model": model, "usage": usage},
            "effort": effort,
            "timestamp": timestamp,
        }
    )


def _subagent_turn(
    model: str,
    effort: str,
    *,
    timestamp: str,
    input: int = 0,
    output: int = 0,
    cache_read: int = 0,
    cache_creation: int = 0,
    thinking: int | None = None,
) -> str:
    """Provide one assistant line as a subagent's own transcript writes it."""

    usage: dict[str, Any] = {
        "input_tokens": input,
        "output_tokens": output,
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
    }
    if thinking is not None:
        usage["output_tokens_details"] = {"thinking_tokens": thinking}
    return json.dumps(
        {
            "type": "assistant",
            "isSidechain": True,
            "agentId": "a1",
            "message": {"model": model, "usage": usage},
            "effort": effort,
            "sessionId": "the-parent-session",
            "timestamp": timestamp,
        }
    )


def test_only_claude_code_is_a_supported_harness_at_this_ticket() -> None:
    """Codex and OpenCode reading follows once those integrations are verified."""

    module = _load_session_records()
    assert module.SUPPORTED == ("claude-code",)


def test_an_unsupported_harness_yields_nothing_to_read(tmp_path: Path) -> None:
    """A Harness this reader does not know is an absence, never a guess."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1)
        + "\n",
        encoding="utf-8",
    )

    assert module.usage("codex", str(transcript)) == []


def test_a_missing_record_yields_nothing_to_read(tmp_path: Path) -> None:
    """A session the Harness never wrote is an absence, not an error."""

    module = _load_session_records()
    assert module.usage("claude-code", str(tmp_path / "never-written.jsonl")) == []


def test_no_transcript_path_yields_nothing_to_read() -> None:
    """Nothing to open is nothing to read, and never a guessed location."""

    module = _load_session_records()
    assert module.usage("claude-code", None) == []
    assert module.usage("claude-code", "") == []


def test_a_truncated_or_garbled_record_yields_whatever_survives(tmp_path: Path) -> None:
    """A broken line is skipped rather than raised; a whole file of them reads empty."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        "\n".join(
            [
                _turn(
                    "claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1
                ),
                "{ not json at all",
                "",
                "not even an object",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 1
    assert groups[0]["tokens"]["input"] == 1

    garbled_only = tmp_path / "session-2.jsonl"
    garbled_only.write_text("{ nope\nstill nope\n", encoding="utf-8")
    assert module.usage("claude-code", str(garbled_only)) == []


def test_the_exact_model_and_deliberation_are_read_from_the_finished_transcript(
    tmp_path: Path,
) -> None:
    """A finished session's own record names its Seat, never a stale guess."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn(
            "claude-opus-5",
            "high",
            timestamp="2026-09-01T10:00:00Z",
            input=10,
            output=20,
            cache_read=5,
            cache_creation=3,
            thinking=7,
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 1
    group = groups[0]
    assert group["role"] == "main"
    assert group["model"] == "claude-opus-5"
    assert group["native_deliberation"] == "high"
    assert group["tokens"] == {
        "input": 10,
        "output": 20,
        "cache_read": 5,
        "cache_creation": 3,
        "thinking": 7,
    }
    assert group["started_at"] == "2026-09-01T10:00:00Z"
    assert group["completed_at"] == "2026-09-01T10:00:00Z"


def test_token_categories_absent_from_a_turn_stay_null_rather_than_zero(
    tmp_path: Path,
) -> None:
    """A missing usage category is never read as though it were a zero."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        json.dumps(
            {
                "type": "assistant",
                "isSidechain": False,
                "message": {"model": "claude-opus-5", "usage": {}},
                "effort": "high",
                "timestamp": "2026-09-01T10:00:00Z",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    group = module.usage("claude-code", str(transcript))[0]

    assert group["tokens"] == {
        "input": None,
        "output": None,
        "cache_read": None,
        "cache_creation": None,
        "thinking": None,
    }


def test_turns_in_the_same_seat_are_summed_and_timed_on_first_and_last(
    tmp_path: Path,
) -> None:
    """Two turns of one Seat give its total usage and its own active window."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        "\n".join(
            [
                _turn(
                    "claude-opus-5",
                    "high",
                    timestamp="2026-09-01T10:00:00Z",
                    input=10,
                    output=20,
                ),
                _turn(
                    "claude-opus-5",
                    "high",
                    timestamp="2026-09-01T10:05:00Z",
                    input=1,
                    output=2,
                    thinking=4,
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 1
    group = groups[0]
    assert group["tokens"]["input"] == 11
    assert group["tokens"]["output"] == 22
    assert group["tokens"]["thinking"] == 4
    assert group["started_at"] == "2026-09-01T10:00:00Z"
    assert group["completed_at"] == "2026-09-01T10:05:00Z"


def test_a_session_that_switched_model_mid_way_yields_one_group_per_seat(
    tmp_path: Path,
) -> None:
    """The main transcript's own turns split into a Seat per configuration."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        "\n".join(
            [
                _turn(
                    "claude-sonnet-5",
                    "high",
                    timestamp="2026-09-01T10:00:00Z",
                    input=10,
                ),
                _turn(
                    "claude-opus-5", "high", timestamp="2026-09-01T10:05:00Z", input=1
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 2
    models = {group["model"] for group in groups}
    assert models == {"claude-sonnet-5", "claude-opus-5"}
    assert {group["role"] for group in groups} == {"main"}


def test_a_subagents_turns_are_read_from_its_own_companion_directory(
    tmp_path: Path,
) -> None:
    """The Harness's record of one session is a transcript and a companion
    directory: a subagent's turns live beside it, never as a flag inline."""

    module = _load_session_records()
    session = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=10)
        + "\n",
        encoding="utf-8",
    )
    subagents = session / "subagents"
    subagents.mkdir(parents=True)
    (subagents / "agent-a1.jsonl").write_text(
        _subagent_turn(
            "claude-sonnet-5", "medium", timestamp="2026-09-01T10:01:00Z", input=3
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 2
    by_role = {group["role"]: group for group in groups}
    assert by_role["main"]["model"] == "claude-opus-5"
    assert by_role["delegated"]["model"] == "claude-sonnet-5"
    assert by_role["delegated"]["native_deliberation"] == "medium"
    assert by_role["delegated"]["tokens"]["input"] == 3


def test_two_subagents_on_the_same_seat_are_summed_into_one(tmp_path: Path) -> None:
    """Two delegated turns on one configuration are one Seat's usage, not two."""

    module = _load_session_records()
    session = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1)
        + "\n",
        encoding="utf-8",
    )
    subagents = session / "subagents"
    subagents.mkdir(parents=True)
    (subagents / "agent-a1.jsonl").write_text(
        _subagent_turn(
            "claude-sonnet-5", "medium", timestamp="2026-09-01T10:01:00Z", input=3
        )
        + "\n",
        encoding="utf-8",
    )
    (subagents / "agent-a2.jsonl").write_text(
        _subagent_turn(
            "claude-sonnet-5", "medium", timestamp="2026-09-01T10:02:00Z", input=5
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    delegated = [group for group in groups if group["role"] == "delegated"]
    assert len(delegated) == 1
    assert delegated[0]["tokens"]["input"] == 8


def test_a_missing_output_tokens_details_stays_null_rather_than_zero(
    tmp_path: Path,
) -> None:
    """`output_tokens_details` is absent on most subagent lines; that is an
    absence for `thinking`, never a zero (readiness addendum to #225)."""

    module = _load_session_records()
    session = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1)
        + "\n",
        encoding="utf-8",
    )
    subagents = session / "subagents"
    subagents.mkdir(parents=True)
    (subagents / "agent-a1.jsonl").write_text(
        _subagent_turn(
            "claude-sonnet-5", "medium", timestamp="2026-09-01T10:01:00Z", input=3
        )
        + "\n",
        encoding="utf-8",
    )

    delegated = next(
        group
        for group in module.usage("claude-code", str(transcript))
        if group["role"] == "delegated"
    )

    assert delegated["tokens"]["thinking"] is None


def test_a_non_assistant_line_is_never_read_as_a_turn(tmp_path: Path) -> None:
    """A user or tool-result line carries no model and no usage of its own."""

    module = _load_session_records()
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "type": "user",
                        "message": {"content": "the whole brief"},
                        "timestamp": "2026-09-01T09:59:00Z",
                    }
                ),
                _turn(
                    "claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 1
    assert "the whole brief" not in json.dumps(groups)


def test_no_prompt_response_reasoning_tool_output_or_path_reaches_a_group(
    tmp_path: Path,
) -> None:
    """The read is field by field onto an allow-list, and copies nothing else."""

    module = _load_session_records()
    session = tmp_path / "session-1"
    transcript = tmp_path / "session-1.jsonl"
    line = json.loads(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1)
    )
    line["message"]["content"] = [{"type": "text", "text": "the whole answer"}]
    line["cwd"] = "/Users/thomas/Projects/skills"
    line["message"]["reasoning"] = "the whole thinking"
    line["toolUseResult"] = {"stdout": "pytest ...", "diff": "--- a/x\n+++ b/x"}
    transcript.write_text(json.dumps(line) + "\n", encoding="utf-8")
    subagents = session / "subagents"
    subagents.mkdir(parents=True)
    (subagents / "agent-a1.jsonl").write_text(
        _subagent_turn(
            "claude-sonnet-5", "medium", timestamp="2026-09-01T10:01:00Z", input=1
        )
        + "\n",
        encoding="utf-8",
    )

    written = json.dumps(module.usage("claude-code", str(transcript)))

    for forbidden in (
        "the whole answer",
        "the whole thinking",
        "pytest ...",
        "+++ b/x",
        "/Users/thomas",
    ):
        assert forbidden not in written


def test_reading_walks_no_further_than_the_sessions_own_files(tmp_path: Path) -> None:
    """No encoding is derived and no other session's files are opened."""

    module = _load_session_records()
    other_session = tmp_path / "other-session.jsonl"
    other_session.write_text(
        _turn("claude-haiku-5", "low", timestamp="2026-09-01T09:00:00Z", input=999)
        + "\n",
        encoding="utf-8",
    )
    transcript = tmp_path / "session-1.jsonl"
    transcript.write_text(
        _turn("claude-opus-5", "high", timestamp="2026-09-01T10:00:00Z", input=1)
        + "\n",
        encoding="utf-8",
    )

    groups = module.usage("claude-code", str(transcript))

    assert len(groups) == 1
    assert groups[0]["model"] == "claude-opus-5"
