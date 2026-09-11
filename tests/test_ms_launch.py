"""How a chosen point is started, and the agent definitions that let it be."""

from __future__ import annotations

import dataclasses
import importlib.util
import sys
from pathlib import Path
from typing import Any

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"
SHIPPED: Path = REPO_ROOT / "skills" / "models" / "model-selector"


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

CAT = catalogue.load(Path("/nowhere"), SHIPPED)
OPUS = catalogue.resolve(CAT, "claude-opus-5")[0]
HAIKU = catalogue.resolve(CAT, "haiku")[0]
ASTRA = catalogue.resolve(CAT, "gpt-6-astra")[0]
GROK = catalogue.resolve(CAT, "grok")[0]

# The Harness version `effort:` was observed to be honoured on (issue #297).
VERIFIED_ON = "Claude Code 2.1.263"


def _profile(*harnesses: str, models: tuple[str, ...] = ()) -> Any:
    """Provide a profile that has the named harnesses and pays for everything."""

    return profiles.Profile(
        harnesses=harnesses,
        providers=tuple({model.provider for model in CAT.models}),
        models=models or tuple(model.id for model in CAT.models),
        channels=tuple(
            profiles.Channel(provider, harness, "api", None, None, None)
            for harness in harnesses
            for provider in {model.provider for model in CAT.models}
        ),
        answered_at=None,
        source="file",
        problem=None,
    )


def test_claude_code_starts_an_anthropic_model_as_a_generated_subagent() -> None:
    """The native path names an agent that `definitions` has generated."""

    plan = launch.plan(
        OPUS, "high", "claude-code", _profile("claude-code"), CAT, repo="/repo"
    )

    assert plan.how == "claude-code-agent"
    assert plan.subagent_type == "kntnt-opus-high"
    assert plan.command is None
    assert f"{plan.subagent_type}.md" in launch.definitions(
        _profile("claude-code"), CAT
    )


def test_a_model_with_no_effort_control_is_one_point_named_without_a_level() -> None:
    """A level in the name would name something the model does not have."""

    plan = launch.plan(
        HAIKU, None, "claude-code", _profile("claude-code"), CAT, repo=None
    )

    assert plan.subagent_type == "kntnt-haiku"
    assert (
        launch.plan(
            HAIKU, "high", "claude-code", _profile("claude-code"), CAT, repo=None
        ).how
        == "inherit"
    )


def test_an_openai_model_is_started_through_the_codex_cli() -> None:
    """The bridge is a command, and its shape is what the caller runs verbatim."""

    plan = launch.plan(
        ASTRA, "high", "claude-code", _profile("codex"), CAT, repo="/repo"
    )

    assert plan.how == "bridge-command"
    assert plan.command == (
        "codex",
        "exec",
        "-C",
        "/repo",
        "--skip-git-repo-check",
        "-m",
        "gpt-6-astra",
        "-c",
        "model_reasoning_effort=high",
        "-s",
        "workspace-write",
        "--json",
    )


def test_the_codex_command_runs_outside_a_repository_without_being_refused() -> None:
    """A directory Codex does not trust is the caller's to choose, not Codex's.

    The CLI refuses a working directory that is neither a git repository nor
    one it has been told to trust, and refuses it in milliseconds, before the
    model is ever reached. Every launch this Skill plans for a directory of
    that kind - the grader's own, above all, which runs from a home directory
    on purpose - would fail for a reason that has nothing to do with the work.
    """

    plan = launch.plan(ASTRA, "low", "codex", _profile("codex"), CAT, repo=None)

    assert "--skip-git-repo-check" in (plan.command or ())


def test_a_model_neither_native_nor_bridged_is_started_by_inheriting() -> None:
    """An unreachable point is said out loud rather than handed over as a command."""

    plan = launch.plan(
        GROK, "high", "claude-code", _profile("claude-code"), CAT, repo=None
    )

    assert plan.how == "inherit"
    assert plan.subagent_type is None
    assert plan.command is None
    assert plan.note is not None


def test_opencode_starts_whatever_the_profile_says_it_fronts() -> None:
    """opencode implies no provider of its own, so the profile decides."""

    plan = launch.plan(
        GROK, "high", "opencode", _profile("opencode"), CAT, repo="/repo"
    )

    assert plan.how == "bridge-command"
    assert plan.command is not None
    assert plan.command[:2] == ("opencode", "run")
    assert "spacexai/grok-4.6" in plan.command


def _gateway_profile(gateway: str | None) -> Any:
    """Provide a profile that pays for Grok through opencode, via *gateway*."""

    return profiles.Profile(
        harnesses=("opencode",),
        providers=("spacexai",),
        models=(GROK.id,),
        channels=(
            profiles.Channel("spacexai", "opencode", "api", None, gateway, None),
        ),
        answered_at=None,
        source="file",
        problem=None,
    )


def _after(command: tuple[str, ...], flag: str) -> str:
    """Return the value a planned command gives *flag*."""

    return command[command.index(flag) + 1]


def test_opencode_names_the_model_the_way_the_channel_s_gateway_routes_it() -> None:
    """The gateway's own slug is a catalogue fact, never the provider's name.

    `spacexai/grok-4.6` is a route this machine has no provider for: the one it
    is configured for is `openrouter/x-ai/grok-4.6`, and the slug after the
    gateway's name is not derivable from the catalogue's provider by string
    surgery (issue #308).
    """

    plan = launch.plan(
        GROK, "high", "claude-code", _gateway_profile("openrouter"), CAT, repo="/repo"
    )

    assert plan.how == "bridge-command"
    assert plan.command is not None
    assert plan.command[:2] == ("opencode", "run")
    assert _after(plan.command, "--dir") == "/repo"
    assert _after(plan.command, "--model") == "openrouter/x-ai/grok-4.6"
    assert _after(plan.command, "--variant") == "high"
    assert "--cwd" not in plan.command


def test_opencode_carries_no_variant_for_a_point_with_no_level() -> None:
    """A level nobody chose is a level nothing should claim the work ran at."""

    plan = launch.plan(
        GROK, None, "process", _gateway_profile("openrouter"), CAT, repo=None
    )

    assert plan.command is not None
    assert "--variant" not in plan.command
    assert _after(plan.command, "--dir") == "."


def test_a_model_with_no_slug_for_the_gateway_is_inherited_rather_than_guessed() -> (
    None
):
    """A guessed slug is a command that fails in somebody else's terminal."""

    unslugged = dataclasses.replace(GROK, gateways=())

    plan = launch.plan(
        unslugged, "high", "process", _gateway_profile("openrouter"), CAT, repo=None
    )

    assert plan.how == "inherit"
    assert plan.command is None
    assert plan.note is not None
    assert "grok-4.6" in plan.note
    assert "openrouter" in plan.note
    assert "no slug" in plan.note


def test_an_opencode_channel_without_a_gateway_plans_provider_and_id() -> None:
    """A direct channel is reached under the provider's own name, as before."""

    plan = launch.plan(GROK, "low", "process", _gateway_profile(None), CAT, repo=None)

    assert plan.command is not None
    assert _after(plan.command, "--model") == "spacexai/grok-4.6"
    assert _after(plan.command, "--variant") == "low"


def test_opencode_with_no_channel_at_all_plans_provider_and_id() -> None:
    """The fallback profile has no channels, and so no gateway to route through."""

    profile = dataclasses.replace(_gateway_profile("openrouter"), channels=())

    plan = launch.plan(GROK, "low", "process", profile, CAT, repo=None)

    assert plan.command is not None
    assert _after(plan.command, "--model") == "spacexai/grok-4.6"


def test_the_definition_matrix_covers_every_enabled_point_and_nothing_else() -> None:
    """One file per Anthropic point the profile enables, and no other provider."""

    matrix = launch.definitions(_profile("claude-code", models=("claude-opus-5",)), CAT)

    assert set(matrix) == {f"kntnt-opus-{level}.md" for level in catalogue.LEVELS}
    body = matrix["kntnt-opus-high.md"]
    assert body.startswith("---\n")
    frontmatter = dict(
        line.split(": ", 1) for line in body.split("---\n")[1].strip().splitlines()
    )
    assert frontmatter == {
        "name": "kntnt-opus-high",
        "description": "Delegated work on claude-opus-5 at high deliberation.",
        "model": "claude-opus-5",
        "effort": "high",
    }
    assert "update" in body.split("---\n")[2]


def test_a_model_with_no_effort_control_gets_a_definition_with_no_effort_line() -> None:
    """An effort line naming a level the model lacks is a line worth not writing."""

    matrix = launch.definitions(_profile("claude-code", models=(HAIKU.id,)), CAT)

    assert set(matrix) == {"kntnt-haiku.md"}
    assert "effort:" not in matrix["kntnt-haiku.md"]
    assert f"model: {HAIKU.id}" in matrix["kntnt-haiku.md"]


def test_sync_writes_what_is_wanted_and_removes_only_its_own_leftovers(
    tmp_path: Path,
) -> None:
    """The directory belongs to the user and to every other tool that writes there."""

    dest = tmp_path / "agents"
    dest.mkdir()
    (dest / "kntnt-opus-high.md").write_text("stale\n", encoding="utf-8")
    (dest / "kntnt-gone-max.md").write_text("retired\n", encoding="utf-8")
    (dest / "somebody-elses.md").write_text("mine\n", encoding="utf-8")
    wanted = {"kntnt-opus-high.md": "fresh\n", "kntnt-opus-low.md": "fresh\n"}

    report = launch.sync_definitions(dest, wanted)

    assert report.created_directory is False
    assert sorted(report.written) == ["kntnt-opus-high.md", "kntnt-opus-low.md"]
    assert report.removed == ["kntnt-gone-max.md"]
    assert (dest / "somebody-elses.md").read_text() == "mine\n"

    again = launch.sync_definitions(dest, wanted)
    assert sorted(again.unchanged) == ["kntnt-opus-high.md", "kntnt-opus-low.md"]
    assert again.written == []


def test_sync_creates_the_directory_it_was_pointed_at(tmp_path: Path) -> None:
    """A machine that has never run this Skill has no agents directory yet."""

    report = launch.sync_definitions(tmp_path / "new", {"kntnt-opus-low.md": "x\n"})

    assert report.created_directory is True
    assert (tmp_path / "new" / "kntnt-opus-low.md").read_text() == "x\n"


# The Claude CLI flags that take a variable number of values. A prompt appended
# after one of them is read as another of its values rather than as the prompt,
# so a planned command ends with a flag that is not one of these.
VARIADIC = frozenset(
    {
        "--add-dir",
        "--tools",
        "--allowedTools",
        "--allowed-tools",
        "--disallowedTools",
        "--disallowed-tools",
        "--agents",
        "--betas",
    }
)


def test_a_read_only_codex_bridge_is_given_no_way_to_write() -> None:
    """The judge reads two excerpts and answers; it has nothing to write."""

    plan = launch.plan(
        ASTRA,
        "high",
        "claude-code",
        _profile("codex"),
        CAT,
        repo="/repo",
        read_only=True,
    )

    assert plan.command is not None
    assert plan.command[plan.command.index("-s") + 1] == "read-only"
    assert "workspace-write" not in plan.command


def test_an_ordinary_codex_bridge_still_writes_where_it_was_sent() -> None:
    """Read-only is the judge's own posture, never every caller's."""

    plan = launch.plan(
        ASTRA, "high", "claude-code", _profile("codex"), CAT, repo="/repo"
    )

    assert plan.command is not None
    assert plan.command[plan.command.index("-s") + 1] == "workspace-write"


def test_a_read_only_claude_bridge_grants_no_tool_at_all() -> None:
    """An empty tool list is what the CLI offers for a call that only answers."""

    plan = launch.plan(
        OPUS,
        "high",
        "process",
        _profile("claude-code"),
        CAT,
        repo="/repo",
        read_only=True,
    )

    assert plan.command is not None
    assert plan.command[plan.command.index("--tools") + 1] == ""
    assert plan.command[-2] not in VARIADIC


def test_an_ordinary_claude_bridge_names_no_tool_list() -> None:
    """A builder needs its tools, so nothing is said about them."""

    plan = launch.plan(OPUS, "high", "process", _profile("claude-code"), CAT, repo=None)

    assert plan.command is not None
    assert "--tools" not in plan.command
    assert plan.command[-2] not in VARIADIC


def test_a_claude_bridge_for_a_model_with_no_effort_still_ends_non_variadic() -> None:
    """The prompt follows the command, so the last flag must take one value."""

    plan = launch.plan(
        HAIKU,
        None,
        "process",
        _profile("claude-code"),
        CAT,
        repo="/repo",
        read_only=True,
    )

    assert plan.command is not None
    assert plan.command[-2] not in VARIADIC


def test_the_honoured_effort_line_names_the_version_it_was_verified_against() -> None:
    """A level the Harness ignored would make the whole ladder's evidence a fiction.

    Evidence accrues to the level a definition names, and a level nothing ever
    ran at is worth nothing (ADR-0182), so `effort:` being honoured is the
    assumption everything above it rests on. It was settled by observation and
    not by argument, and an observation is worth exactly the Harness version it
    was made against — so the two places that state it, the generator's own
    docstring and the reference that says a subagent's unit carries the level
    it ran on, each name that version, and both move when it is re-verified.
    """

    docstring = " ".join((launch._definition.__doc__ or "").split())
    measurement = " ".join(
        (SHIPPED / "references" / "measurement.md").read_text(encoding="utf-8").split()
    )

    assert "honour" in docstring.lower()
    assert VERIFIED_ON in docstring
    assert VERIFIED_ON in measurement


# The flags each installed CLI's own help lists, for exactly the flags the
# planner emits, each with the short alias its help lists beside the long form.
# Read on 2026-09-11 from `claude --help` (Claude Code 2.1.268), `codex exec
# --help` (codex-cli 0.154.0) and `opencode run --help` (opencode 1.18.30). A
# flag the planner emits that is not here is one the CLI would refuse, which
# is how `--cwd` reached every opencode launch while opencode had only `--dir`
# (issue #308). Re-read the help and move these sets when a CLI is upgraded.
INSTALLED_FLAGS: dict[str, frozenset[str]] = {
    "claude": frozenset(
        {"-p", "--print", "--add-dir", "--tools", "--model", "--effort"}
    ),
    "codex": frozenset(
        {
            "-C",
            "--cd",
            "--skip-git-repo-check",
            "-m",
            "--model",
            "-c",
            "--config",
            "-s",
            "--sandbox",
            "--json",
        }
    ),
    "opencode": frozenset({"--dir", "-m", "--model", "--variant"}),
}


def _flags(command: tuple[str, ...]) -> set[str]:
    """Return every flag a planned command passes, values left out."""

    return {token for token in command if token.startswith("-")}


def test_every_flag_a_bridge_emits_is_one_its_installed_cli_lists() -> None:
    """Held for every variant the planner emits: read-only, with and without a level."""

    bridges = (
        (OPUS, _profile("claude-code")),
        (HAIKU, _profile("claude-code")),
        (ASTRA, _profile("codex")),
        (GROK, _gateway_profile("openrouter")),
        (GROK, _gateway_profile(None)),
    )

    planned = 0
    for model, profile in bridges:
        levels = model.deliberation or (None,)
        for level in (*levels, None):
            for read_only in (False, True):
                plan = launch.plan(
                    model,
                    level,
                    "process",
                    profile,
                    CAT,
                    repo="/repo",
                    read_only=read_only,
                )
                if plan.command is None:
                    continue
                planned += 1
                binary = plan.command[0]
                unlisted = _flags(plan.command) - INSTALLED_FLAGS[binary]
                assert not unlisted, f"{binary} lists no {sorted(unlisted)}"

    assert planned >= len(bridges) * 2
