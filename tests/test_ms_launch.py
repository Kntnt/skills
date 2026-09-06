"""How a chosen point is started, and the agent definitions that let it be."""

from __future__ import annotations

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
