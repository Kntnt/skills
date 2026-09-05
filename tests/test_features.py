"""The Catalog's second entry type, and the two Features shipped on it.

A Feature owns nothing a Harness loads, so nothing about it can be established
by looking for a file in a skills directory. What it owns is state inside files
the user maintains by hand — a Harness's own instruction file, a Harness's own
hook table, a single-valued setting somebody may already have taken — and every
test here is about the one property those share: this collection writes exactly
what it owns, reads back what it wrote, and never touches anything else.
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MANAGER: Path = REPO_ROOT / "skills" / "kntnt"
LIBRARY: Path = MANAGER / "library" / "scripts"
FEATURES: Path = MANAGER / "features"

SESSION_CLEANUP = FEATURES / "session-cleanup" / "scripts" / "session_cleanup.py"
STATUSLINE = FEATURES / "statusline" / "scripts" / "statusline_feature.py"

OWNER = "kntnt.session-cleanup"


def _module(path: Path, name: str) -> Any:
    """Load one shipped engine from the path it is installed at."""

    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)

    # Registered before it is executed, because a module defining a dataclass
    # resolves its own annotations through `sys.modules` while it runs.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _integrations() -> Any:
    return _module(LIBRARY / "integrations.py", "kntnt_integrations")


def _kntnt() -> Any:
    return _module(MANAGER / "scripts" / "kntnt.py", "kntnt_manager")


def _run(
    script: Path, *args: str, home: Path, stdin: str = ""
) -> subprocess.CompletedProcess[str]:
    """Run one Feature's own script against an isolated home."""

    environment = {**os.environ, "KNTNT_HOME": str(home)}
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=REPO_ROOT,
        env=environment,
        input=stdin,
        text=True,
        capture_output=True,
        check=False,
    )


def _answer(script: Path, *args: str, home: Path, stdin: str = "") -> dict[str, Any]:
    completed = _run(script, *args, home=home, stdin=stdin)
    assert completed.returncode == 0, completed.stderr
    return cast(dict[str, Any], json.loads(completed.stdout))


def _instructions(home: Path) -> str:
    return (home / ".claude" / "CLAUDE.md").read_text(encoding="utf-8")


def _settings(home: Path) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        json.loads((home / ".claude" / "settings.json").read_text(encoding="utf-8")),
    )


# --- the Library's own new mechanics --------------------------------------


def test_an_owned_block_lands_below_prose_it_never_touches(tmp_path: Path) -> None:
    """The file above the fence is the user's, and stays exactly as it was."""

    integrations = _integrations()
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "CLAUDE.md").write_text("# Mine\n\nKeep this.\n", "utf-8")

    record = integrations.install_block(OWNER, "claude-code", tmp_path, "Recorded.")

    assert record["status"] == "installed"
    assert record["entries"] == 1
    text = _instructions(tmp_path)
    assert text.startswith("# Mine\n\nKeep this.\n")
    assert f"<!-- {OWNER} begin -->\nRecorded.\n<!-- {OWNER} end -->" in text


def test_installing_a_block_twice_leaves_one_block(tmp_path: Path) -> None:
    """Convergence, not appending: a repair after damage is a no-op too."""

    integrations = _integrations()
    integrations.install_block(OWNER, "claude-code", tmp_path, "First.")
    integrations.install_block(OWNER, "claude-code", tmp_path, "Second.")

    text = _instructions(tmp_path)
    assert text.count(f"<!-- {OWNER} begin -->") == 1
    assert "Second." in text
    assert "First." not in text


def test_removing_a_block_takes_the_fence_and_nothing_around_it(
    tmp_path: Path,
) -> None:
    """Prose nobody fenced as ours is never this collection's to delete."""

    integrations = _integrations()
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "CLAUDE.md").write_text("# Mine\n\nKeep this.\n", "utf-8")
    integrations.install_block(OWNER, "claude-code", tmp_path, "Recorded.")

    record = integrations.remove_block(OWNER, "claude-code", tmp_path)

    assert record["status"] == "removed"
    assert record["entries"] == 1
    assert _instructions(tmp_path) == "# Mine\n\nKeep this.\n"


def test_a_half_written_fence_is_refused_rather_than_converged(
    tmp_path: Path,
) -> None:
    """Everything between two fences is the user's file, so one fence is not ours."""

    integrations = _integrations()
    (tmp_path / ".claude").mkdir()
    orphaned = f"# Mine\n\n<!-- {OWNER} begin -->\nHalf a block.\n"
    (tmp_path / ".claude" / "CLAUDE.md").write_text(orphaned, "utf-8")

    record = integrations.install_block(OWNER, "claude-code", tmp_path, "Recorded.")

    assert record["status"] == "failed"
    assert "unclosed" in str(record["detail"])
    assert _instructions(tmp_path) == orphaned


def test_a_harness_with_no_instruction_file_is_reported_not_skipped() -> None:
    """An unserved Harness answers in the words every Capability is said in."""

    integrations = _integrations()

    record = integrations.install_block(OWNER, "cursor", Path("/nowhere"), "Recorded.")

    assert record["status"] == "unsatisfied"
    assert record["capability"] == integrations.INSTRUCTIONS_UNSATISFIED


def test_a_status_line_somebody_else_holds_is_reported_not_taken(
    tmp_path: Path,
) -> None:
    """A single-valued setting has no room beside its value, and no ledger under it."""

    integrations = _integrations()
    (tmp_path / ".claude").mkdir()
    mine = {"type": "command", "command": "~/mine.sh"}
    (tmp_path / ".claude" / "settings.json").write_text(
        json.dumps({"statusLine": mine}), "utf-8"
    )

    record = integrations.install_statusline(
        "kntnt.statusline", "claude-code", tmp_path, ["bash", "/ours.sh"]
    )

    assert record["status"] == "failed"
    assert "~/mine.sh" in str(record["detail"])
    assert _settings(tmp_path)["statusLine"] == mine

    # And a removal leaves it exactly as it found it.
    cleared = integrations.remove_statusline(
        "kntnt.statusline", "claude-code", tmp_path
    )
    assert cleared["status"] == "removed"
    assert cleared["entries"] == 0
    assert _settings(tmp_path)["statusLine"] == mine


def test_an_owner_installs_only_the_moments_it_asked_for(tmp_path: Path) -> None:
    """An entry at a moment the owner does nothing at is one health still counts."""

    integrations = _integrations()

    integrations.install(
        OWNER,
        "claude-code",
        tmp_path,
        ["uv", "run", "/x.py", "hook"],
        events=("SessionStart", "SessionEnd"),
    )

    hooks = _settings(tmp_path)["hooks"]
    assert sorted(hooks) == ["SessionEnd", "SessionStart"]
    assert (
        integrations.health(
            OWNER, "claude-code", tmp_path, events=("SessionStart", "SessionEnd")
        )["status"]
        == "healthy"
    )


def test_several_records_about_one_harness_fold_into_one() -> None:
    """A reader told a disagreement is a finding must not meet two different things."""

    integrations = _integrations()
    healthy = {
        "harness": "claude-code",
        "status": "healthy",
        "entries": 1,
        "capability": None,
        "detail": None,
    }
    absent = {**healthy, "status": "absent", "entries": 0}

    folded = integrations.fold([healthy, absent])

    assert folded["harness"] == "claude-code"
    assert folded["status"] == "absent"
    assert folded["entries"] == 1


# --- the session-cleanup Feature ------------------------------------------


def test_both_halves_go_in_together_and_come_out_together(tmp_path: Path) -> None:
    """The block without the hook asks for a record nothing reads, and the reverse."""

    installed = _answer(
        SESSION_CLEANUP, "install-integrations", "--harness=claude-code", home=tmp_path
    )

    assert [record["status"] for record in installed["installed"]] == ["installed"]
    assert f"<!-- {OWNER} begin -->" in _instructions(tmp_path)
    assert sorted(_settings(tmp_path)["hooks"]) == ["SessionEnd", "SessionStart"]

    removed = _answer(SESSION_CLEANUP, "remove-integrations", home=tmp_path)

    assert {record["status"] for record in removed["removed"]} == {"removed"}
    assert OWNER not in _instructions(tmp_path)
    assert "hooks" not in _settings(tmp_path)


def test_the_installed_block_names_the_command_it_asks_for(tmp_path: Path) -> None:
    """A block naming a path that is not there asks for a recording that cannot happen."""

    _answer(
        SESSION_CLEANUP, "install-integrations", "--harness=claude-code", home=tmp_path
    )

    assert f"{SESSION_CLEANUP} add pid" in _instructions(tmp_path)


def test_a_path_outside_a_temp_root_is_never_recorded(tmp_path: Path) -> None:
    """Recording is where the bound is cheapest to state, so it is stated there too."""

    # `tmp_path` is itself under a temp root, so the path that has to be
    # refused is one that plainly is not: this repository's own tree.
    completed = _run(
        SESSION_CLEANUP, "add", "path", str(REPO_ROOT), "why", home=tmp_path
    )

    assert completed.returncode == 1
    assert "temp root" in completed.stderr


def test_a_manifest_line_naming_the_root_cannot_do_what_it_says(
    tmp_path: Path,
) -> None:
    """A manifest line is data and never an instruction."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")

    assert cleanup.under_temp(Path("/")) is None
    assert cleanup.remove_path({"id": "/"})["outcome"] == "refused"
    assert cleanup.stop_pid({"id": "1"})["outcome"] == "refused"


def test_a_reused_process_id_names_something_else_and_is_left_alone() -> None:
    """A manifest outliving its process must not hand the number to a stranger."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    mine = os.getppid()

    outcome = cleanup.stop_pid(
        {"id": str(mine), "started": "a start time this process never had"}
    )

    assert outcome["outcome"] == "reused"


def test_a_session_being_resumed_is_not_a_session_that_ended(tmp_path: Path) -> None:
    """Stopping a resumed session's work takes it from under the user coming back."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    os.environ["KNTNT_HOME"] = str(tmp_path)
    try:
        cleanup.open_session("S", "claude-code", "S")
        cleanup.append(
            cleanup.manifest_path("S"), {"kind": "path", "id": "/", "why": "x"}
        )

        answered = cleanup.hook(
            "claude-code",
            "",
            {"hook_event_name": "SessionEnd", "session_id": "S", "reason": "resume"},
        )

        assert answered["kept"] == "resume"
        assert cleanup.manifest_path("S").exists()
    finally:
        del os.environ["KNTNT_HOME"]


def test_a_start_leaves_a_manifest_whose_terminal_is_still_alive(
    tmp_path: Path,
) -> None:
    """Another session's dev server is not this session's to end."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    os.environ["KNTNT_HOME"] = str(tmp_path)
    try:
        elsewhere = cleanup.manifest_path("S-ELSEWHERE")
        cleanup.append(
            elsewhere,
            {
                "kind": "session",
                "id": "S-ELSEWHERE",
                # A live process this test knows is not this test's own terminal.
                "sid": os.getpid(),
                "harness": "claude-code",
            },
        )
        here = cleanup.manifest_path("S-GONE")
        cleanup.append(
            here,
            {"kind": "session", "id": "S-GONE", "sid": 0, "harness": "claude-code"},
        )

        foreign = cleanup.foreign_manifests("S-NEW")

        assert elsewhere not in foreign
        assert here in foreign
    finally:
        del os.environ["KNTNT_HOME"]


def test_a_session_that_recorded_nothing_says_so_in_the_log(tmp_path: Path) -> None:
    """Recording is the one step that depends on an agent remembering to take it."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    os.environ["KNTNT_HOME"] = str(tmp_path)
    try:
        cleanup.open_session("S", "claude-code", "S")
        cleanup.hook(
            "claude-code",
            "",
            {"hook_event_name": "SessionEnd", "session_id": "S", "reason": "other"},
        )

        log = cleanup.log_path().read_text(encoding="utf-8")
        assert '"event": "recorded-nothing"' in log
    finally:
        del os.environ["KNTNT_HOME"]


def test_the_hook_exits_zero_on_a_payload_that_is_not_json(tmp_path: Path) -> None:
    """A cleanup that breaks a shutdown is worse than a leak."""

    completed = _run(
        SESSION_CLEANUP, "hook", "--harness=claude-code", home=tmp_path, stdin="{oh no"
    )

    assert completed.returncode == 0
    assert completed.stdout == ""


# --- the statusline Feature -----------------------------------------------


def test_the_shipped_status_line_reads_stdin_and_draws_two_lines(
    tmp_path: Path,
) -> None:
    """What the Harness hands it, plus git, and nothing else."""

    payload = json.dumps(
        {
            "workspace": {"current_dir": str(REPO_ROOT)},
            "model": {"display_name": "Opus 5"},
            "effort": {"level": "high"},
            "context_window": {"total_input_tokens": 42000, "used_percentage": 21},
        }
    )
    completed = subprocess.run(
        ["bash", str(FEATURES / "statusline" / "statusline.sh")],
        input=payload,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0
    assert len(completed.stdout.splitlines()) == 2
    assert "Opus 5 high" in completed.stdout


def test_the_shipped_status_line_reads_no_credential_and_calls_nothing() -> None:
    """It runs on every render, so anything it did it would do again a moment later."""

    source = (FEATURES / "statusline" / "statusline.sh").read_text(encoding="utf-8")

    for forbidden in ("security find-generic-password", "curl", "api.anthropic.com"):
        assert forbidden not in source


def test_the_status_line_slot_is_taken_and_given_back(tmp_path: Path) -> None:
    """Install and removal are the same convergence every owned integration is."""

    installed = _answer(
        STATUSLINE, "install-integrations", "--harness=claude-code", home=tmp_path
    )
    assert [record["status"] for record in installed["installed"]] == ["installed"]
    assert "kntnt.statusline" in _settings(tmp_path)["statusLine"]["command"]

    assert (
        _answer(STATUSLINE, "health", home=tmp_path)["harnesses"][0]["status"]
        == "healthy"
    )

    removed = _answer(STATUSLINE, "remove-integrations", home=tmp_path)
    assert [record["status"] for record in removed["removed"]] == ["removed"]
    assert "statusLine" not in _settings(tmp_path)


# --- the Catalog and the list ---------------------------------------------


def test_the_shipped_catalog_carries_both_entry_types() -> None:
    """A Feature is a Catalog entry, listed beside the Skills and never among them."""

    catalog = json.loads((MANAGER / "catalog.json").read_text(encoding="utf-8"))

    assert isinstance(catalog["features"], list)
    names = {entry["name"] for entry in catalog["features"]}
    assert {"session-cleanup", "statusline"} <= names
    assert names.isdisjoint({entry["name"] for entry in catalog["skills"]})


def test_every_feature_states_what_it_writes_and_which_harnesses_it_serves() -> None:
    """A row that edits a file the user reads says so before it is checked."""

    catalog = json.loads((MANAGER / "catalog.json").read_text(encoding="utf-8"))

    for entry in catalog["features"]:
        assert entry["writes"], entry["name"]
        assert entry["harnesses"], entry["name"]
        assert entry["description"], entry["name"]
        assert entry["digest"], entry["name"]


def test_a_feature_page_with_no_writes_section_is_refused(tmp_path: Path) -> None:
    """Generation is where a Feature that would arrive silent has to fail."""

    kntnt = _kntnt()
    manager = tmp_path / "kntnt"
    directory = manager / "features" / "silent"
    (directory / "scripts").mkdir(parents=True)
    (directory / "scripts" / "silent.py").write_text("", encoding="utf-8")
    (directory / "FEATURE.md").write_text(
        "---\n"
        "name: silent\n"
        "description: Writes without saying so.\n"
        "metadata:\n"
        "  kntnt.harnesses: claude-code\n"
        "  kntnt.integrations: scripts/silent.py\n"
        "---\n\n# silent\n",
        encoding="utf-8",
    )

    try:
        kntnt.generate_features(manager, set())
    except kntnt.ManagerError as exc:
        assert "Writes" in str(exc)
    else:  # pragma: no cover - the refusal is the point
        raise AssertionError(
            "a Feature saying nothing about what it writes was accepted"
        )


def test_a_feature_may_not_take_a_skills_name(tmp_path: Path) -> None:
    """The list is answered as one checked set, so a name means one entry."""

    kntnt = _kntnt()
    manager = tmp_path / "kntnt"
    directory = manager / "features" / "commit"
    (directory / "scripts").mkdir(parents=True)
    (directory / "scripts" / "commit.py").write_text("", encoding="utf-8")
    (directory / "FEATURE.md").write_text(
        "---\n"
        "name: commit\n"
        "description: A Feature wearing a Skill's name.\n"
        "metadata:\n"
        "  kntnt.harnesses: claude-code\n"
        "  kntnt.integrations: scripts/commit.py\n"
        "---\n\n# commit\n\n## Writes\n\n- Nothing.\n",
        encoding="utf-8",
    )

    try:
        kntnt.generate_features(manager, {"commit"})
    except kntnt.ManagerError as exc:
        assert "also a Skill" in str(exc)
    else:  # pragma: no cover - the refusal is the point
        raise AssertionError("a Feature took a Skill's name")


def test_the_project_layer_offers_no_feature_and_says_why() -> None:
    """A checkbox that could never change anything is worse than a sentence."""

    kntnt = _kntnt()

    assert kntnt.feature_rows(["claude-code"], global_layer=False) == []

    # Nothing is placed and nothing is removed there, whatever the answer
    # named: what a Feature owns is keyed by owner inside a Harness's own
    # configuration, so a Project run reaching it would take away what a
    # standing Global Enable still describes.
    place, remove, _ = kntnt.feature_change(
        ["session-cleanup"], ["claude-code"], global_layer=False
    )
    assert (place, remove) == ([], [])
    assert "Global layer" in kntnt.PROJECT_LAYER_FEATURES_NOTE
    assert kntnt.unattempted_features(global_layer=False)["note"] == (
        kntnt.PROJECT_LAYER_FEATURES_NOTE
    )
