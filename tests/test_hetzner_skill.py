"""Where the hetzner Skill admits the agents to a server a tool converges.

The Skill is prose an agent executes, so what is held here is the shape that
prose has to keep: who manages a server is settled before anything that runs
the hand procedure, the path through a configuration tool states the whole
contract and the two checks after a converge, turning the agents off takes the
same two paths, and every surface that told its reader the procedure admits the
agents to any existing server names the tool path beside it (issue #425).
Whether an agent following the prose declares the agents in a real project's
tool is exercised by running it, not here.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL = REPO_ROOT / "skills" / "infrastructure" / "hetzner"

# The two headings this ticket adds to `references/access.md`, and the three
# it leaves where they were for a server nothing converges.
CHECK = "## Who manages the server"
TOOL_PATH = "## Admission through a configuration tool"
PROCEDURE = "## The procedure"
CASES = "## Who carries it out"
TURNING_OFF = "## Turning it off"

# The two conditions every surface opens its paths with.
MANAGED = "a server a configuration tool manages"
UNCONVERGED = "a server nothing converges"


def _read(name: str) -> str:
    return (SKILL / name).read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    """One section of a Markdown document, without the heading itself.

    The section ends at the next heading of the same level. It is empty where
    the document carries no such heading, so a caller asserts the heading's
    presence before reading anything out of what this returns.
    """

    level = heading.split(" ", 1)[0]
    return text.partition(f"\n{heading}\n")[2].partition(f"\n{level} ")[0]


def _headings(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("## ")]


def test_who_manages_a_server_is_settled_before_the_hand_procedure() -> None:
    """The check comes first, so no case runs the procedure on a tool's host."""

    access = _read("references/access.md")
    headings = _headings(access)

    assert CHECK in headings
    assert TOOL_PATH in headings
    assert headings.index(CHECK) < headings.index(TOOL_PATH)
    assert headings.index(TOOL_PATH) < headings.index(PROCEDURE)
    assert headings.index(PROCEDURE) < headings.index(CASES)


def test_the_check_reads_the_project_at_hand_and_settles_three_ways() -> None:
    """Managed, unconverged or unsettled; unsettled asks before a write."""

    check = _section(_read("references/access.md"), CHECK)

    assert "the project at hand" in check
    assert "deployment documentation" in check
    assert "infrastructure files" in check
    for outcome in (
        "**A tool manages it.**",
        "**Nothing converges it.**",
        "**Unsettled.**",
    ):
        assert outcome in check, outcome
    assert "before any write" in check
    assert MANAGED in check
    assert UNCONVERGED in check


def test_the_tool_path_states_the_whole_contract_a_managed_server_meets() -> None:
    """All three parts: what the server holds, the allow list, root's file."""

    tool = _section(_read("references/access.md"), TOOL_PATH)

    for part in (
        "*What the server holds*",
        "`kntnt-agent`",
        "`~/.ssh/kntnt-agent.pub`",
        "`AllowUsers`",
        "`AllowGroups`",
        "`/root/.ssh/authorized_keys`",
    ):
        assert part in tool, part


def test_the_tool_path_checks_the_converge_over_the_agents_own_login() -> None:
    """`sudo -n true` says they are in; root's file says their key is gone."""

    tool = _section(_read("references/access.md"), TOOL_PATH)

    login = "ssh -i ~/.ssh/kntnt-agent -o IdentitiesOnly=yes kntnt-agent@<server>"
    assert f"{login} sudo -n true" in tool
    assert f"{login} sudo -n cat /root/.ssh/authorized_keys" in tool


def test_turning_the_agents_off_on_a_managed_server_goes_through_the_tool() -> None:
    """The declaration is removed and converged; hand commands come after."""

    off = _section(_read("references/access.md"), TURNING_OFF)

    assert MANAGED in off
    assert UNCONVERGED in off
    assert off.index(MANAGED) < off.index("/etc/sudoers.d/kntnt-agent")


def test_setup_step_5_reads_the_project_at_hand_before_it_shows_both_paths() -> None:
    """Step 5 cannot tell servers apart, so it shows both paths.

    Each path is opened by the condition it applies under.
    """

    setup = _section(_read("SKILL.md"), "## Setup")
    step = setup.partition("\n5. ")[2]

    assert step
    read = step.index("infrastructure files of the project at hand")
    assert read < step.index("`key.public_key`")
    assert MANAGED in step
    assert UNCONVERGED in step
    assert "before any write" in step


def test_every_surface_naming_the_procedure_names_the_tool_path_too() -> None:
    """A page left saying the procedure fits every server keeps teaching it."""

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    creation = next(
        paragraph
        for paragraph in _read("references/provisioning.md").split("\n\n")
        if "--ssh-key <user's key> --ssh-key kntnt-agent" in paragraph
    )
    surfaces = {
        "help/setup.md": _section(_read("help/setup.md"), "## DESCRIPTION"),
        "help.md": _section(_read("help.md"), "## DESCRIPTION"),
        "README.md": _section(readme, "### hetzner"),
        "references/provisioning.md": creation,
    }

    for name, text in surfaces.items():
        assert text, name
        assert "configuration tool" in text, name
        assert "nothing converges" in text, name
