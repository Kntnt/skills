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


def _profile(*harnesses: str, makers: tuple[str, ...] = ()) -> Any:
    """Provide a profile that has the named harnesses and pays for everything.

    It chooses every maker the catalogue holds unless *makers* names fewer.
    """

    return profiles.Profile(
        harnesses=harnesses,
        makers=makers or tuple(dict.fromkeys(model.provider for model in CAT.models)),
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
        ASTRA,
        "high",
        "claude-code",
        _profile("codex"),
        CAT,
        repo="/repo",
        permissions="edits",
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
    assert "spacexai/grok-4.7" in plan.command


def _gateway_profile(gateway: str | None) -> Any:
    """Provide a profile that pays for Grok through opencode, via *gateway*."""

    return profiles.Profile(
        harnesses=("opencode",),
        makers=("spacexai",),
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

    `spacexai/grok-4.7` is a route this machine has no provider for: the one it
    is configured for is `openrouter/x-ai/grok-4.7`, and the slug after the
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
    assert _after(plan.command, "--model") == "openrouter/x-ai/grok-4.7"
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
    assert "grok-4.7" in plan.note
    assert "openrouter" in plan.note
    assert "no slug" in plan.note


def test_an_opencode_channel_without_a_gateway_plans_provider_and_id() -> None:
    """A direct channel is reached under the provider's own name, as before."""

    plan = launch.plan(GROK, "low", "process", _gateway_profile(None), CAT, repo=None)

    assert plan.command is not None
    assert _after(plan.command, "--model") == "spacexai/grok-4.7"
    assert _after(plan.command, "--variant") == "low"


def test_opencode_starts_only_what_a_chosen_maker_makes() -> None:
    """opencode fronts whatever the profile chooses, and nothing it does not."""

    plan = launch.plan(
        GROK,
        "high",
        "opencode",
        _profile("opencode", makers=("anthropic",)),
        CAT,
        repo="/repo",
    )

    assert plan.how == "inherit"
    assert plan.command is None


def test_opencode_with_no_channel_at_all_plans_provider_and_id() -> None:
    """A profile with no channels has no gateway to route through."""

    profile = dataclasses.replace(_gateway_profile("openrouter"), channels=())

    plan = launch.plan(GROK, "low", "process", profile, CAT, repo=None)

    assert plan.command is not None
    assert _after(plan.command, "--model") == "spacexai/grok-4.7"


def test_the_definition_matrix_covers_every_anthropic_point_and_nothing_else() -> None:
    """One file per point of every Anthropic family, where Anthropic is chosen.

    No single model is chosen or left out within a maker, so the matrix is
    every Anthropic family the catalogue holds at every level it supports —
    the family's newest release taking the file — and no point of any other
    maker however many of those are chosen beside it.
    """

    matrix = launch.definitions(
        _profile("claude-code", makers=("anthropic", "spacexai")), CAT
    )

    anthropic = [model for model in CAT.models if model.provider == "anthropic"]
    assert set(matrix) == {
        f"kntnt-{model.family}{f'-{level}' if level else ''}.md"
        for model in anthropic
        for level in (model.deliberation or (None,))
    }
    assert {f"kntnt-opus-{level}.md" for level in catalogue.LEVELS} <= set(matrix)
    assert not [name for name in matrix if "grok" in name]
    body = matrix["kntnt-opus-high.md"]
    assert body.startswith("---\n")
    frontmatter = dict(
        line.split(": ", 1) for line in body.split("---\n")[1].strip().splitlines()
    )
    assert frontmatter == {
        "name": "kntnt-opus-high",
        "description": "Delegated work on claude-opus-5-5 at high deliberation.",
        "model": "claude-opus-5-5",
        "effort": "high",
    }
    header = body.split("---\n")[2]
    assert "daily catalogue pass" in header
    assert "`/model-selector setup`" in header
    assert "update" not in header


def test_a_model_with_no_effort_control_gets_a_definition_with_no_effort_line() -> None:
    """An effort line naming a level the model lacks is a line worth not writing."""

    matrix = launch.definitions(_profile("claude-code", makers=("anthropic",)), CAT)

    assert not [name for name in matrix if name.startswith("kntnt-haiku-")]
    assert "effort:" not in matrix["kntnt-haiku.md"]
    assert f"model: {HAIKU.id}" in matrix["kntnt-haiku.md"]


def test_a_profile_that_does_not_choose_anthropic_defines_no_agent() -> None:
    """A subagent exists to start an Anthropic model, and none is chosen."""

    assert launch.definitions(_profile("claude-code", makers=("openai",)), CAT) == {}


def test_a_definition_needs_its_maker_chosen_and_no_channel() -> None:
    """The caller's own provider needs no channel, so its subagents need none."""

    unpaid = dataclasses.replace(
        _profile("claude-code", makers=("anthropic",)), channels=()
    )

    assert "kntnt-opus-high.md" in launch.definitions(unpaid, CAT)


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


def test_a_codex_bridge_writes_where_the_level_its_caller_named_lets_it() -> None:
    """Read-only is the judge's own posture, never every caller's.

    What decides the rest is the level the caller says it is running at, and
    nothing here decides one on the caller's behalf: a caller that named none
    is answered by the silence test below, not by a writable workspace chosen
    for it here.
    """

    plan = launch.plan(
        ASTRA,
        "high",
        "claude-code",
        _profile("codex"),
        CAT,
        repo="/repo",
        permissions="edits",
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


# Every flag on either bridge that grants or withholds permission, whichever
# level named it. A planned command carries the ones its own level names and
# no others, so silence can be told from a level by reading the command.
PERMISSION_FLAGS = frozenset(
    {
        "-s",
        "--sandbox",
        "--approve-for-me",
        "--dangerously-bypass-approvals-and-sandbox",
        "--permission-mode",
    }
)

# The two bridges a permission level is carried across, each as the model that
# reaches it and the harness the profile has to hold for it. The caller is
# `process` throughout, so the Anthropic row is planned as a command rather
# than as the native subagent, which inherits its parent's mode and is untouched.
BRIDGES: tuple[tuple[str, Any, str], ...] = (
    ("claude", OPUS, "claude-code"),
    ("codex", ASTRA, "codex"),
)

# The CLI versions the permission rows were read out of and tried against.
CODEX_TRIED_ON = "codex-cli 0.155.1"
CLAUDE_TRIED_ON = "Claude Code 2.1.278"


def _planned(model: Any, harness: str, **named: Any) -> tuple[str, ...]:
    """Return the bridge command planned for *model*, as the caller runs it."""

    plan = launch.plan(
        model, "high", "process", _profile(harness), CAT, repo="/repo", **named
    )
    assert plan.command is not None
    command: tuple[str, ...] = plan.command
    return command


def _carries(command: tuple[str, ...], flags: tuple[str, ...]) -> bool:
    """Say whether *command* holds *flags* whole and in order."""

    width = len(flags)
    return any(command[at : at + width] == flags for at in range(len(command)))


def test_every_permission_level_reaches_each_bridge_in_its_own_spelling() -> None:
    """One row per level, spelled the way the CLI being started spells it.

    The vocabulary is walked out of the module rather than restated here. A
    level added to the map is a level this covers, where a second copy of the
    table would go on passing while the table it copied was wrong.
    """

    walked = 0
    for level, spelling in launch.PERMISSIONS.items():
        for binary, model, harness in BRIDGES:
            wanted: tuple[str, ...] = getattr(spelling, binary)
            command = _planned(model, harness, permissions=level)
            walked += 1

            assert _carries(command, wanted), f"{level} on {binary}: {command}"
            assert PERMISSION_FLAGS & set(command) == PERMISSION_FLAGS & set(wanted)
            assert not any(token.startswith("approval_policy=") for token in command)
            assert not ("--approve-for-me" in command and "-s" in command)
            if binary == "claude":
                assert command[-2] not in VARIADIC

    assert walked == len(launch.PERMISSIONS) * len(BRIDGES)


def test_a_launch_that_names_no_level_names_no_permission_flag() -> None:
    """Silence is inheritance: the started CLI follows the user's own settings."""

    for _, model, harness in BRIDGES:
        command = _planned(model, harness)

        assert not PERMISSION_FLAGS & set(command)


def test_a_read_only_launch_is_the_same_command_whatever_level_it_carries() -> None:
    """Read-only outranks the level, so the judge's command is what it was.

    The Codex row is pinned whole rather than by the flag it turns on: the
    grader starts exactly this argv, and a permission level that moved one
    token of it would be a judge launched differently for nothing.
    """

    codex = _planned(ASTRA, "codex", read_only=True)
    assert codex == (
        "codex",
        "exec",
        "-C",
        "/repo",
        "--skip-git-repo-check",
        "-m",
        ASTRA.id,
        "-c",
        "model_reasoning_effort=high",
        "-s",
        "read-only",
        "--json",
    )

    for _, model, harness in BRIDGES:
        alone = _planned(model, harness, read_only=True)
        for level in launch.PERMISSIONS:
            assert _planned(model, harness, read_only=True, permissions=level) == alone


def test_a_level_this_module_does_not_know_is_answered_as_silence() -> None:
    """An unknown level is never a refusal: the caller still gets its launch."""

    for _, model, harness in BRIDGES:
        plan = launch.plan(
            model,
            "high",
            "process",
            _profile(harness),
            CAT,
            repo="/repo",
            permissions="paranoid",
        )

        assert plan.command is not None
        assert not PERMISSION_FLAGS & set(plan.command)
        assert plan.note is not None and "paranoid" in plan.note


def test_each_bridge_names_the_cli_it_read_its_permission_rows_from() -> None:
    """A row is worth the CLI version it was read off, so each docstring says it.

    Both claims the rows rest on are version-bound: which flags the tool has,
    and what a command naming none of them leaves the start at. The Codex row
    carries the correction as well — `codex exec` does have an approval flag —
    because a docstring asserting otherwise would be a permanent untruth.
    """

    codex = " ".join((launch._codex.__doc__ or "").split())
    claude = " ".join((launch._claude.__doc__ or "").split())

    assert CODEX_TRIED_ON in codex
    assert "--approve-for-me" in codex
    assert "config.toml" in codex
    assert CLAUDE_TRIED_ON in claude
    assert "defaultMode" in claude


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
# Read on 2026-09-20 from `claude --help` (Claude Code 2.1.278), `codex exec
# --help` (codex-cli 0.155.1) and, on 2026-09-11, `opencode run --help`
# (opencode 1.18.30). A
# flag the planner emits that is not here is one the CLI would refuse, which
# is how `--cwd` reached every opencode launch while opencode had only `--dir`
# (issue #308). Re-read the help and move these sets when a CLI is upgraded.
INSTALLED_FLAGS: dict[str, frozenset[str]] = {
    "claude": frozenset(
        {
            "-p",
            "--print",
            "--add-dir",
            "--tools",
            "--model",
            "--effort",
            "--permission-mode",
        }
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
            "--approve-for-me",
            "--dangerously-bypass-approvals-and-sandbox",
            "--json",
        }
    ),
    "opencode": frozenset({"--dir", "-m", "--model", "--variant"}),
}


def _flags(command: tuple[str, ...]) -> set[str]:
    """Return every flag a planned command passes, values left out."""

    return {token for token in command if token.startswith("-")}


def test_every_flag_a_bridge_emits_is_one_its_installed_cli_lists() -> None:
    """Held for every variant the planner emits.

    Read-only, with and without a deliberation level, and once for each
    permission level in the vocabulary as well as for naming none — a level
    reaching a CLI as a flag that CLI does not have is refused before the
    model is touched, which is the whole reason this walk exists.
    """

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
                for permissions in (None, *launch.PERMISSIONS):
                    plan = launch.plan(
                        model,
                        level,
                        "process",
                        profile,
                        CAT,
                        repo="/repo",
                        read_only=read_only,
                        permissions=permissions,
                    )
                    if plan.command is None:
                        continue
                    planned += 1
                    binary = plan.command[0]
                    unlisted = _flags(plan.command) - INSTALLED_FLAGS[binary]
                    assert not unlisted, f"{binary} lists no {sorted(unlisted)}"

    assert planned >= len(bridges) * 2
