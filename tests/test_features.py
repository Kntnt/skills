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

import pytest

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


def _held_slot(tmp_path: Path) -> dict[str, str]:
    """Put somebody else's status line where this collection wants one."""

    mine = {"type": "command", "command": "~/mine.sh"}
    (tmp_path / ".claude").mkdir(exist_ok=True)
    (tmp_path / ".claude" / "settings.json").write_text(
        json.dumps({"statusLine": mine}), "utf-8"
    )
    return mine


def test_a_status_line_somebody_else_holds_is_held_not_taken(tmp_path: Path) -> None:
    """Untold, an install names what holds the slot and writes nothing."""

    integrations = _integrations()
    mine = _held_slot(tmp_path)

    record = integrations.install_statusline(
        "kntnt.statusline", "claude-code", tmp_path, ["bash", "/ours.sh"]
    )

    assert record["status"] == "held"
    assert record["held"] == "~/mine.sh"
    assert "~/mine.sh" in str(record["detail"])
    assert _settings(tmp_path)["statusLine"] == mine

    # And a removal leaves it exactly as it found it.
    cleared = integrations.remove_statusline(
        "kntnt.statusline", "claude-code", tmp_path
    )
    assert cleared["status"] == "removed"
    assert cleared["entries"] == 0
    assert _settings(tmp_path)["statusLine"] == mine


def test_a_status_line_is_replaced_only_when_the_answer_says_so(
    tmp_path: Path,
) -> None:
    """The answer arrives on the command line, because a script cannot ask."""

    integrations = _integrations()
    _held_slot(tmp_path)

    record = integrations.install_statusline(
        "kntnt.statusline", "claude-code", tmp_path, ["bash", "/ours.sh"], replace=True
    )

    assert record["status"] == "installed"
    assert "~/mine.sh" in str(record["detail"])
    assert "no copy of it is kept" in str(record["detail"])
    assert "kntnt.statusline" in _settings(tmp_path)["statusLine"]["command"]


def test_the_health_of_a_held_slot_names_what_holds_it(tmp_path: Path) -> None:
    """A row can only ask about what it can name."""

    integrations = _integrations()
    _held_slot(tmp_path)

    record = integrations.statusline_health("kntnt.statusline", "claude-code", tmp_path)

    assert record["status"] == "absent"
    assert record["held"] == "~/mine.sh"


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


def test_the_moments_this_feature_wants_are_stated_without_citing_captures() -> None:
    """The comment over `EVENTS` answers for this Feature's own set alone.

    Capture narrows its own set too — on Codex to the single moment against
    this Feature's two (#294) — so a comment calling this the narrower of the
    pair states a comparison the other side no longer bears out.
    """

    source = SESSION_CLEANUP.read_text(encoding="utf-8")
    stated = source.partition("EVENTS: dict")[0].rsplit(f'OWNER = "{OWNER}"', 1)[-1]

    assert "EVENTS" not in stated
    assert "capture" not in stated


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


def test_a_removal_narrowed_to_one_harness_leaves_the_others(tmp_path: Path) -> None:
    """`--harness` narrows removal exactly as it narrows installation.

    A caller reading the two seam words as symmetric — the flag is accepted by
    both — must not lose an integration it never named.
    """

    _answer(SESSION_CLEANUP, "install-integrations", home=tmp_path)

    removed = _answer(
        SESSION_CLEANUP, "remove-integrations", "--harness=codex", home=tmp_path
    )

    assert [record["harness"] for record in removed["removed"]] == ["codex"]
    assert f"<!-- {OWNER} begin -->" in _instructions(tmp_path)
    assert "hooks" in _settings(tmp_path)
    assert (
        not (tmp_path / ".codex" / "hooks.json")
        .read_text(encoding="utf-8")
        .count(OWNER)
    )


def test_naming_no_harness_still_clears_every_one_of_them(tmp_path: Path) -> None:
    """The Manager says the word with no `--harness` at all, and means all of them."""

    _answer(SESSION_CLEANUP, "install-integrations", home=tmp_path)

    removed = _answer(SESSION_CLEANUP, "remove-integrations", home=tmp_path)

    assert {record["status"] for record in removed["removed"]} == {"removed"}
    assert OWNER not in _instructions(tmp_path)
    assert OWNER not in (tmp_path / ".codex" / "hooks.json").read_text(encoding="utf-8")


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


def test_legacy_terminals_do_not_authorize_an_immediate_sweep(
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
                # Legacy terminal identities carry no owner-lifetime evidence.
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
        assert here not in foreign
    finally:
        del os.environ["KNTNT_HOME"]


@pytest.mark.parametrize(
    ("has_session_header", "detached_hook", "age_hours"),
    [(False, False, 0), (True, False, 0), (False, True, 0), (True, True, 25)],
)
def test_a_nested_start_preserves_its_recorded_launcher(
    tmp_path: Path, has_session_header: bool, detached_hook: bool, age_hours: int
) -> None:
    """A registered builder must survive its own session-start cleanup hook."""

    # Exercise the actual signal path in a separate process group, so the
    # regression can kill its launcher without reaching the pytest worker.
    program = """
import importlib.util
import os
import subprocess
import sys
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location("cleanup", sys.argv[1])
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)
if sys.argv[2] == "True":
    cleanup.open_session("parent", "codex", "parent")
record = cleanup.add("pid", str(os.getpid()), "nested builder")
scratch = Path(os.environ["KNTNT_HOME"]) / "builder-scratch"
scratch.mkdir()
cleanup.add("path", str(scratch), "builder scratch")
old = time.time() - int(sys.argv[4]) * 3600
os.utime(record["manifest"], (old, old))
answer = subprocess.run(
    [sys.executable, sys.argv[1], "hook", "--harness=codex", "--event=SessionStart"],
    cwd=Path(sys.argv[1]).parent,
    input='{"session_id": "child"}',
    text=True,
    start_new_session=sys.argv[3] == "True",
    capture_output=True,
    check=True,
)
assert Path(record["manifest"]).exists(), answer
assert scratch.exists(), answer
print("builder survived")
"""
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            program,
            str(SESSION_CLEANUP),
            str(has_session_header),
            str(detached_hook),
            str(age_hours),
        ],
        cwd=REPO_ROOT,
        env={**os.environ, "KNTNT_HOME": str(tmp_path)},
        start_new_session=True,
        text=True,
        capture_output=True,
        check=False,
        timeout=10,
    )

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "builder survived"


def test_a_start_keeps_a_recent_unowned_manifest_with_a_live_process(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A missing session header does not establish that a sibling has ended."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    path = cleanup.manifest_path("unowned")
    cleanup.append(path, {"kind": "pid", "id": "123456", "started": "then"})
    monkeypatch.setattr(cleanup, "alive", lambda pid: pid == 123456)
    monkeypatch.setattr(cleanup, "started_at", lambda pid: "then")

    assert path not in cleanup.foreign_manifests("new")


def test_an_unowned_manifest_with_a_gone_process_waits_for_the_backstop(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A finished recorded task does not establish that its owner has ended."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    path = cleanup.manifest_path("unowned")
    cleanup.append(path, {"kind": "pid", "id": "123456", "started": "then"})
    monkeypatch.setattr(cleanup, "alive", lambda pid: False)

    assert path not in cleanup.foreign_manifests("new")


@pytest.mark.parametrize(
    ("current_start", "expired"), [("different", False), ("then", True)]
)
def test_only_the_age_backstop_releases_unowned_manifests(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    current_start: str,
    expired: bool,
) -> None:
    """Conservative ownership does not disable orphan cleanup's existing bounds."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    path = cleanup.manifest_path("unowned")
    cleanup.append(path, {"kind": "pid", "id": "123456", "started": "then"})
    monkeypatch.setattr(cleanup, "alive", lambda pid: pid == 123456)
    monkeypatch.setattr(cleanup, "started_at", lambda pid: current_start)
    monkeypatch.setattr(cleanup, "stale", lambda path: expired)

    assert (path in cleanup.foreign_manifests("new")) is expired


def test_a_start_without_readable_ancestry_cannot_authorize_a_sweep(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Failure to establish live ownership cannot become permission to kill."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    path = cleanup.manifest_path("old")
    cleanup.append(path, {"kind": "path", "id": str(tmp_path / "scratch")})
    monkeypatch.setattr(cleanup, "process_ancestors", lambda: None)

    assert cleanup.foreign_manifests("new") == []
    assert path.exists()


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


def test_select_adds_no_flag_of_its_own_for_the_replacement_answer() -> None:
    """One more thing asked in the one confirmation, not a second grammar.

    `--yes` is what this collection has always meant by *answer yes to what you
    are about to ask me*, so the question a held setting raises is answered
    there rather than by a flag grown for one Feature's one setting (ADR-0174).
    """

    kntnt = _kntnt()
    parsed = kntnt.parse_args(["apply", "select", "statusline", "--yes"])

    assert parsed.yes is True
    assert not hasattr(parsed, "replace")


def test_the_feature_writes_nothing_until_the_answer_reaches_it(
    tmp_path: Path,
) -> None:
    """The Manager carries the confirmation down; the Feature never assumes it."""

    _held_slot(tmp_path)

    untold = _answer(
        STATUSLINE, "install-integrations", "--harness=claude-code", home=tmp_path
    )
    assert untold["installed"][0]["status"] == "held"
    assert _settings(tmp_path)["statusLine"]["command"] == "~/mine.sh"

    told = _answer(
        STATUSLINE,
        "install-integrations",
        "--harness=claude-code",
        "--replace",
        home=tmp_path,
    )
    assert told["installed"][0]["status"] == "installed"
    assert "kntnt.statusline" in _settings(tmp_path)["statusLine"]["command"]


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


def test_a_removal_named_for_a_harness_it_does_not_serve_says_so(
    tmp_path: Path,
) -> None:
    """A Feature serving one Harness answers a removal for another as its install does."""

    removed = _answer(
        STATUSLINE, "remove-integrations", "--harness=codex", home=tmp_path
    )

    assert removed["removed"] == []
    assert removed["unsupported"] == {"count": 1}


def test_every_feature_answers_the_words_the_manager_says(tmp_path: Path) -> None:
    """The Manager says one word in one shape to every Feature it installs.

    It hands each one the same argument vector — the word, one `--harness` per
    Detected Harness, and `--replace` where the user has confirmed — so a
    Feature that had to be invoked its own way would make the seam a table of
    exceptions the Manager has to keep. This is the check that was missing when
    `session-cleanup` shipped without `--replace` and refused the Manager's own
    install call with an argparse usage message.
    """

    for script in sorted(FEATURES.glob("*/scripts/*.py")):
        for word in ("install-integrations", "health"):
            completed = _run(
                script,
                word,
                "--harness=claude-code",
                "--replace",
                home=tmp_path / script.parent.parent.name,
            )
            assert completed.returncode == 0, (
                f"{script.relative_to(REPO_ROOT)} refused `{word} --harness=... "
                f"--replace`, which is what the Manager says: {completed.stderr}"
            )
        for arguments in ((), ("--harness=claude-code",)):
            removed = _run(
                script, "remove-integrations", *arguments, home=tmp_path / "removal"
            )
            assert removed.returncode == 0, (
                f"{script.relative_to(REPO_ROOT)} refused `remove-integrations "
                f"{' '.join(arguments)}`, which is what the Manager says: "
                f"{removed.stderr}"
            )


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


@pytest.mark.parametrize("recorded_kind", ["path", "live-pid", "gone-pid", "container"])
def test_detached_tools_remain_owned_until_the_harness_exits(
    tmp_path: Path, recorded_kind: str
) -> None:
    """Tool and hook POSIX sessions may die while their Harness keeps working."""

    program = """
import json, os, subprocess, sys
from pathlib import Path
script = sys.argv[1]
root = Path(os.environ['KNTNT_HOME'])
os.environ['CLAUDE_PID'] = str(os.getpid())
os.environ['CLAUDE_CODE_SESSION_ID'] = 'working'
os.environ['CODEX_SESSION_ID'] = 'outer-codex'
def call(*args, payload=''):
    result = subprocess.run([sys.executable, script, *args], cwd=root,
        input=payload, text=True, capture_output=True, start_new_session=True)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout) if result.stdout else None
call('hook', '--harness=claude-code', '--event=SessionStart',
     payload='{"session_id":"working"}')
scratch = root / 'scratch'
scratch.mkdir()
record = call('add', 'path', str(scratch), 'working scratch')
if sys.argv[2] == 'live-pid':
    call('add', 'pid', str(os.getpid()), 'live task')
if sys.argv[2] == 'gone-pid':
    child = subprocess.Popen([sys.executable, '-c', 'import sys; sys.stdin.read()'],
        cwd=root, stdin=subprocess.PIPE, start_new_session=True)
    call('add', 'pid', str(child.pid), 'short task')
    child.communicate(timeout=5)
if sys.argv[2] == 'container':
    call('add', 'container', 'test-owned/container', 'working container')
print(json.dumps(record), flush=True)
sys.stdin.read()
"""
    with subprocess.Popen(
        [sys.executable, "-c", program, str(SESSION_CLEANUP), recorded_kind],
        cwd=REPO_ROOT,
        env={**os.environ, "KNTNT_HOME": str(tmp_path)},
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    ) as owner:
        try:
            assert owner.stdout is not None
            record = json.loads(owner.stdout.readline())
            manifest = Path(record["manifest"])
            before = manifest.read_bytes()
            os.utime(manifest, (1, 1))
            _run(
                SESSION_CLEANUP,
                "hook",
                "--harness=codex",
                "--event=SessionStart",
                home=tmp_path,
                stdin='{"session_id":"sibling"}',
            )
            assert manifest.exists(), "a sibling swept the working session"
            assert manifest.read_bytes() == before
            assert (tmp_path / "scratch").exists()
            assert record["session"] == "working"
        finally:
            owner.kill()
            owner.communicate(timeout=5)

    # A hard-ended owner has no SessionEnd; the next start must reclaim it.
    if recorded_kind != "container":
        os.utime(manifest, None)
        _run(
            SESSION_CLEANUP,
            "hook",
            "--harness=codex",
            "--event=SessionStart",
            home=tmp_path,
            stdin='{"session_id":"after-crash"}',
        )
        assert not manifest.exists()
        assert not (tmp_path / "scratch").exists()


def test_lifecycle_retires_legacy_pointers_and_logs_the_sweeper(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Start/end need no terminal pointer and report subject and initiator."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    pointers = tmp_path / ".kntnt/session-cleanup/current"
    pointers.mkdir(parents=True)
    (pointers / "123").write_text("old")
    orphan = cleanup.manifest_path("orphan")
    cleanup.append(
        orphan,
        {
            "kind": "session",
            "id": "orphan",
            "owner_pid": 999999999,
            "owner_started": "gone",
        },
    )
    cleanup.append(
        orphan, {"kind": "path", "id": str(tmp_path / "gone"), "why": "scratch"}
    )
    empty = cleanup.manifest_path("empty")
    cleanup.append(
        empty,
        {
            "kind": "session",
            "id": "empty",
            "owner_pid": 999999999,
            "owner_started": "gone",
        },
    )

    cleanup.hook("codex", "SessionStart", {"session_id": "new"})
    cleanup.hook("codex", "SessionEnd", {"session_id": "new"})

    assert not pointers.exists()
    assert not cleanup.manifest_path("new").exists()
    records = [json.loads(line) for line in cleanup.log_path().read_text().splitlines()]
    swept = [row for row in records if row.get("why") == "start"]
    assert {row["session"] for row in swept} == {"orphan", "empty"}
    assert all(
        row["sweeper_session"] == "new" and row["sweeper_harness"] == "codex"
        for row in swept
    )


def test_opencode_end_uses_event_identity_not_the_shared_server(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A conversation ending does not end its shared OpenCode process."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    payload = {"type": "session.created", "properties": {"info": {"id": "oc-session"}}}
    answer = cleanup.hook("opencode", "", payload)
    assert answer["session"] == "oc-session"
    cleanup.append(cleanup.manifest_path("oc-session"), {"kind": "path", "id": "/"})
    ended = cleanup.hook(
        "opencode", "session.deleted", {"properties": {"info": {"id": "oc-session"}}}
    )
    assert ended["session"] == "oc-session"
    assert not cleanup.manifest_path("oc-session").exists()
    assert cleanup.hook("opencode", "session.deleted", {})["swept"] == []


def test_hook_with_closed_stderr_still_exits_zero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A shutdown may close the reporting pipe before cleanup has finished."""

    import io

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"session_id":"closed"}'))
    closed = io.StringIO()
    closed.close()
    monkeypatch.setattr(sys, "stderr", closed)

    assert cleanup.main(["hook", "--harness=codex", "--event=SessionStart"]) == 0
    assert (
        not cleanup.log_path().exists()
        or "hook-failed" not in cleanup.log_path().read_text()
    )


@pytest.mark.parametrize("inner", ["codex", "opencode"])
def test_inner_harness_does_not_record_under_inherited_claude_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, inner: str
) -> None:
    """The nearest Harness owns the call, even with an outer Claude PID."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    monkeypatch.setenv("CLAUDE_PID", "42")
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "outer-claude")
    monkeypatch.setenv("CODEX_SESSION_ID", "inner-codex")

    def process_table(
        args: list[str], **kwargs: Any
    ) -> subprocess.CompletedProcess[str]:
        """Model the OS process table at the external ps boundary."""
        output = (
            f"{os.getpid()} 43 python\n43 42 {inner}\n42 1 claude\n"
            if "-axo" in args
            else "start"
        )
        return subprocess.CompletedProcess(args, 0, output, "")

    monkeypatch.setattr(subprocess, "run", process_table)
    recorded = cleanup.add("container", "unit-test-container", "owned work")
    assert recorded["session"] == (
        "inner-codex" if inner == "codex" else "process-43-start"
    )
    assert not cleanup.manifest_path("outer-claude").exists()


@pytest.mark.parametrize(
    ("current", "swept"), [("same", False), ("", False), ("reused", True)]
)
def test_owner_identity_controls_even_old_manifests(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, current: str, swept: bool
) -> None:
    """Only a proven ended owner releases known ownership; age cannot do so."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    manifest = cleanup.manifest_path("old-owner")
    cleanup.append(
        manifest, {"kind": "session", "owner_pid": os.getpid(), "owner_started": "same"}
    )
    cleanup.append(manifest, {"kind": "container", "id": "unit-test-container"})
    os.utime(manifest, (1, 1))

    def process_table(
        args: list[str], **kwargs: Any
    ) -> subprocess.CompletedProcess[str]:
        """Keep the process alive while varying the OS identity lookup."""
        output = f"{os.getpid()} 1 python\n" if "-axo" in args else current
        return subprocess.CompletedProcess(args, 0, output, "")

    monkeypatch.setattr(subprocess, "run", process_table)
    assert (manifest in cleanup.foreign_manifests("new")) is swept


def test_an_unidentified_hook_cannot_claim_an_inherited_session(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A hook without payload identity must not borrow its launcher's ID."""

    cleanup = _module(SESSION_CLEANUP, "kntnt_session_cleanup")
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    monkeypatch.setenv("CODEX_SESSION_ID", "outer")

    def process_table(
        args: list[str], **kwargs: Any
    ) -> subprocess.CompletedProcess[str]:
        """Expose a nested Codex whose hook inherited the outer environment."""
        output = f"{os.getpid()} 43 python\n43 1 codex\n" if "-axo" in args else "start"
        return subprocess.CompletedProcess(args, 0, output, "")

    monkeypatch.setattr(subprocess, "run", process_table)
    answer = cleanup.hook("codex", "SessionStart", {})
    assert answer["session"] != "outer"
    assert not cleanup.manifest_path("outer").exists()
