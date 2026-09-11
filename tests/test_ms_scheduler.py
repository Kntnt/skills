"""The daily catalogue pass, run by an owned `launchd` job that follows the Skill.

Enabling Model Selector installs the job and Disabling it removes it, the same
two seams that install and remove its capture hooks (#312). Nothing here loads
anything into the maintainer's real `launchd` account: every test writes under
a temporary root, and the adapter issues `launchctl` only where the plist it
wrote lies inside the real user's home. A test that wants to see the commands
points that lookup at its temporary root and puts a stand-in `launchctl`,
which records what it was asked and keeps its own idea of what is loaded,
first on `PATH`.
"""

from __future__ import annotations

import importlib.util
import json
import os
import plistlib
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from support.fake_binary import fake_binary_on_path

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
SCRIPTS: Path = REPO_ROOT / "skills" / "models" / "model-selector" / "scripts"

LABEL = "com.kntnt.model-selector.refresh"
COMMAND = ["uv", "run", "hook"]
NOW = datetime(2026, 9, 11, 14, 3, 8, tzinfo=UTC)


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


_module("catalogue")
_module("profiles")
_module("evidence")
_module("launch")
capture = _module("capture", "model_selector_capture")


# --- The stand-in and the account it speaks for ---------------------------------


def _launchctl(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Put a recording `launchctl` first on `PATH`, and return its log.

    It keeps what is loaded as one file per label, so `bootstrap` loads,
    `bootout` unloads, and `print` answers 0 only for a loaded label, the way
    the real one answers.
    """

    log = tmp_path / "launchctl.log"
    loaded = tmp_path / "loaded"
    loaded.mkdir()
    script = f"""#!/bin/sh
echo "$*" >> "{log}"
case "$1" in
  bootstrap)
    label=$(basename "$3" .plist)
    touch "{loaded}/$label"
    exit 0 ;;
  bootout|print)
    label=${{2##*/}}
    if [ -f "{loaded}/$label" ]; then
      [ "$1" = bootout ] && rm "{loaded}/$label"
      exit 0
    fi
    echo "Could not find service" >&2
    exit 113 ;;
esac
exit 64
"""
    env = fake_binary_on_path(tmp_path, "launchctl", script)
    monkeypatch.setenv("PATH", env["PATH"])
    return log


def _real_home_is(monkeypatch: pytest.MonkeyPatch, root: Path) -> None:
    """Make *root* the real user's home, as the adapter's gate reads it."""

    import pwd

    monkeypatch.setattr(pwd, "getpwuid", lambda uid: SimpleNamespace(pw_dir=str(root)))


def _calls(log: Path) -> list[str]:
    """Return every command the stand-in was given, oldest first."""

    if not log.exists():
        return []
    return log.read_text(encoding="utf-8").splitlines()


def _plist(root: Path, label: str = LABEL) -> Path:
    return root / "Library" / "LaunchAgents" / f"{label}.plist"


def _job(root: Path) -> dict[str, Any]:
    with _plist(root).open("rb") as stream:
        loaded: dict[str, Any] = plistlib.load(stream)
    return loaded


def _rewrite(root: Path, **changes: Any) -> None:
    """Change the job on disk the way a hand edit or another copy would."""

    job = _job(root)
    job.update(changes)
    _plist(root).write_bytes(plistlib.dumps(job))


def _domain() -> str:
    return f"gui/{os.getuid()}"


@pytest.fixture
def account(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path, Path]:
    """Return a data directory, a root that is the real home, and the stand-in's log."""

    root = tmp_path / "home"
    root.mkdir()
    log = _launchctl(tmp_path, monkeypatch)
    _real_home_is(monkeypatch, root)
    return tmp_path / "data", root, log


# --- Enabling installs one job, Disabling removes it -----------------------------


def test_enabling_on_macos_installs_one_owned_job_that_runs_the_pass_daily(
    account: tuple[Path, Path, Path],
) -> None:
    """The plist names the pass beside this capture, at 05:00 and at load."""

    data, root, log = account

    report = capture.install(data, root, [], COMMAND, platform="darwin")

    assert report["scheduler"]["state"] == "loaded", report["scheduler"]
    assert [path.name for path in _plist(root).parent.iterdir()] == [f"{LABEL}.plist"]
    job = _job(root)
    assert job["Label"] == LABEL
    uv, run, script, *arguments = job["ProgramArguments"]
    assert Path(uv).is_absolute() and Path(uv).name == "uv"
    assert run == "run"
    assert script == str(SCRIPTS / "catalogue.py")
    assert arguments == ["refresh", "--scheduled"]
    assert job["EnvironmentVariables"] == {"PATH": os.environ["PATH"]}
    assert job["StartCalendarInterval"] == {"Hour": 5, "Minute": 0}
    assert job["RunAtLoad"] is True
    assert _calls(log) == [
        f"bootout {_domain()}/{LABEL}",
        f"bootstrap {_domain()} {_plist(root)}",
    ]


def test_the_job_never_carries_a_data_directory(
    account: tuple[Path, Path, Path],
) -> None:
    """The hooks carry theirs; the job always runs against the default one."""

    _, root, _ = account

    capture.install(
        Path("/elsewhere/data"),
        root,
        [],
        ["uv", "run", "x", "--data", "/elsewhere"],
        platform="darwin",
    )

    assert "--data" not in _job(root)["ProgramArguments"]


def test_any_install_puts_the_job_in_place_whatever_harness_it_names(
    account: tuple[Path, Path, Path],
) -> None:
    """The job is per machine, not per Harness."""

    data, root, _ = account

    report = capture.install(data, root, ["codex"], COMMAND, platform="darwin")

    assert report["scheduler"]["state"] == "loaded"
    assert _plist(root).is_file()


def test_disabling_removes_the_job_and_leaves_every_other_job_alone(
    account: tuple[Path, Path, Path],
) -> None:
    """Removal boots out our label, deletes our plist, and touches nothing else."""

    data, root, log = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    other = _plist(root, "com.example.other")
    other.write_bytes(plistlib.dumps({"Label": "com.example.other"}))
    before = len(_calls(log))

    report = capture.disable(data, root, [], platform="darwin")

    assert report["scheduler"] == {"state": "removed", "detail": None}
    assert not _plist(root).exists()
    assert other.is_file()
    assert _calls(log)[before:] == [f"bootout {_domain()}/{LABEL}"]


def test_a_removal_naming_a_harness_leaves_the_job(
    account: tuple[Path, Path, Path],
) -> None:
    """Only a removal naming no Harness is the Skill being Disabled."""

    data, root, log = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    before = len(_calls(log))

    report = capture.disable(data, root, ["codex"], platform="darwin")

    assert report["scheduler"]["state"] == "left"
    assert _plist(root).is_file()
    assert _calls(log)[before:] == []


def test_the_manager_s_two_words_answer_with_the_job(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both answers carry the `scheduler` key the Manager is handed."""

    monkeypatch.setenv("HOME", str(tmp_path))
    _launchctl(tmp_path, monkeypatch)

    installed = capture.install_integrations([])
    removed = capture.remove_integrations([])

    assert installed["scheduler"]["state"] in {"not loaded", "unsatisfied"}
    assert removed["scheduler"]["state"] in {"removed", "unsatisfied"}


# --- Nothing reaches the real account from a dry run ----------------------------


def test_under_a_redirected_home_install_writes_the_plist_and_loads_nothing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A Manager Sandbox redirects HOME, and the real `launchd` is never reached."""

    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    log = _launchctl(tmp_path, monkeypatch)

    report = capture.install(
        capture.default_data(), Path.home(), [], [], platform="darwin"
    )

    assert report["scheduler"]["state"] == "not loaded"
    assert _plist(home).is_file()
    assert _calls(log) == []


def test_an_install_status_and_disable_under_a_temporary_root_call_no_launchctl(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The gate is where the plist is written, so a temporary root never loads."""

    log = _launchctl(tmp_path, monkeypatch)
    data, root = tmp_path / "data", tmp_path / "home"

    capture.install(data, root, [], COMMAND, platform="darwin")
    reported = capture.status(data, root, platform="darwin")["scheduler"]
    removed = capture.disable(data, root, [], platform="darwin")["scheduler"]

    assert reported["health"] == "degraded"
    assert removed["state"] == "removed"
    assert not _plist(root).exists()
    assert _calls(log) == []


# --- Install converges without killing a pass -----------------------------------


def test_reinstalling_an_unchanged_loaded_job_rewrites_it_and_reloads_nothing(
    account: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """A running pass is never booted out by a Manager refresh that changed nothing."""

    data, root, log = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    before = len(_calls(log))
    monkeypatch.setenv("PATH", f"{os.environ['PATH']}{os.pathsep}/opt/elsewhere")

    report = capture.install(data, root, [], COMMAND, platform="darwin")

    assert report["scheduler"]["state"] == "loaded"
    assert _job(root)["EnvironmentVariables"]["PATH"].endswith("/opt/elsewhere")
    assert _calls(log)[before:] == [f"print {_domain()}/{LABEL}"]


def test_a_second_install_of_a_changed_job_boots_out_before_bootstrapping(
    account: tuple[Path, Path, Path],
) -> None:
    """A job whose own keys moved is reloaded, the old one out first."""

    data, root, log = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    _rewrite(root, StartCalendarInterval={"Hour": 7, "Minute": 0})
    before = len(_calls(log))

    capture.install(data, root, [], COMMAND, platform="darwin")

    assert _calls(log)[before:] == [
        f"bootout {_domain()}/{LABEL}",
        f"bootstrap {_domain()} {_plist(root)}",
    ]
    assert _job(root)["StartCalendarInterval"] == {"Hour": 5, "Minute": 0}


def test_a_second_install_of_a_job_that_is_not_loaded_boots_out_and_bootstraps(
    account: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    """An unchanged plist nobody loaded is loaded."""

    data, root, log = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    (tmp_path / "loaded" / LABEL).unlink()
    before = len(_calls(log))

    report = capture.install(data, root, [], COMMAND, platform="darwin")

    assert report["scheduler"]["state"] == "loaded"
    assert _calls(log)[before:] == [
        f"print {_domain()}/{LABEL}",
        f"bootout {_domain()}/{LABEL}",
        f"bootstrap {_domain()} {_plist(root)}",
    ]


# --- What status says of the job -------------------------------------------------


def _scheduler(data: Path, root: Path, *, platform: str = "darwin") -> dict[str, Any]:
    reported: dict[str, Any] = capture.status(data, root, NOW, platform=platform)[
        "scheduler"
    ]
    return reported


def test_a_loaded_job_install_would_write_is_healthy(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")

    assert _scheduler(data, root)["health"] == "healthy"


def test_a_healthy_job_checked_from_another_path_or_another_copy_stays_healthy(
    account: tuple[Path, Path, Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Neither the captured `PATH`, the `uv` path nor the script's path is compared."""

    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    arguments = _job(root)["ProgramArguments"]
    _rewrite(
        root,
        ProgramArguments=[
            arguments[0],
            "run",
            "/another/copy/catalogue.py",
            *arguments[3:],
        ],
    )
    monkeypatch.setenv("PATH", f"{os.environ['PATH']}{os.pathsep}/opt/elsewhere")

    assert _scheduler(data, root)["health"] == "healthy"


def test_no_plist_is_absent(account: tuple[Path, Path, Path]) -> None:
    data, root, _ = account

    reported = _scheduler(data, root)

    assert reported["health"] == "absent"
    assert reported["next_due"] is None


@pytest.mark.parametrize(
    "change",
    [
        {"StartCalendarInterval": {"Hour": 6, "Minute": 0}},
        {"RunAtLoad": False},
        {"Label": "com.kntnt.model-selector.other"},
    ],
)
def test_a_job_whose_own_keys_differ_is_degraded(
    account: tuple[Path, Path, Path], change: dict[str, Any]
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    _rewrite(root, **change)

    assert _scheduler(data, root)["health"] == "degraded"


def test_a_job_whose_arguments_after_the_script_differ_is_degraded(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    arguments = _job(root)["ProgramArguments"]
    _rewrite(root, ProgramArguments=[*arguments[:3], "refresh"])

    assert _scheduler(data, root)["health"] == "degraded"


def test_a_job_whose_uv_is_gone_is_degraded(
    account: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    arguments = _job(root)["ProgramArguments"]
    _rewrite(root, ProgramArguments=[str(tmp_path / "no-uv"), *arguments[1:]])

    assert _scheduler(data, root)["health"] == "degraded"


def test_a_job_that_is_not_loaded_is_degraded_and_still_due(
    account: tuple[Path, Path, Path], tmp_path: Path
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")
    (tmp_path / "loaded" / LABEL).unlink()

    reported = _scheduler(data, root)

    assert reported["health"] == "degraded"
    assert reported["next_due"] is not None


def test_the_next_pass_is_due_at_the_next_five_o_clock_local_time(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account
    capture.install(data, root, [], COMMAND, platform="darwin")

    due = datetime.fromisoformat(_scheduler(data, root)["next_due"])

    assert due.tzinfo is not None
    local = due.astimezone()
    assert (local.hour, local.minute, local.second) == (5, 0, 0)
    assert NOW < due <= NOW + timedelta(hours=25)


def _marker(data: Path, ended: datetime, bound: str | None = None) -> None:
    data.mkdir(parents=True, exist_ok=True)
    (data / "refresh-marker.json").write_text(
        json.dumps(
            {
                "date": ended.astimezone(UTC).date().isoformat(),
                "ended_at": ended.isoformat(),
                "bound_hit": bound,
            }
        ),
        encoding="utf-8",
    )


def test_status_names_the_last_scheduled_pass_and_the_bound_it_hit(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account
    ended = NOW - timedelta(hours=3)
    _marker(data, ended, "source:claude")

    reported = _scheduler(data, root)

    assert reported["last_pass"] == {
        "ended_at": ended.isoformat(),
        "bound_hit": "source:claude",
    }
    assert reported["overdue"] is False


def test_a_last_scheduled_pass_more_than_a_day_ago_is_overdue(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account
    _marker(data, NOW - timedelta(hours=25))

    assert _scheduler(data, root)["overdue"] is True


def test_with_no_scheduled_pass_yet_overdue_and_the_last_pass_are_null(
    account: tuple[Path, Path, Path],
) -> None:
    data, root, _ = account

    reported = _scheduler(data, root)

    assert reported["overdue"] is None
    assert reported["last_pass"] is None


# --- An operating system with no adapter ------------------------------------------


def test_an_operating_system_with_no_scheduler_adapter_is_unsatisfied(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reported by name, never skipped silently, and nothing is written."""

    log = _launchctl(tmp_path, monkeypatch)
    data, root = tmp_path / "data", tmp_path / "home"

    installed = capture.install(data, root, [], COMMAND, platform="linux")
    reported = _scheduler(data, root, platform="linux")
    removed = capture.disable(data, root, [], platform="linux")

    assert installed["scheduler"]["state"] == "unsatisfied"
    assert installed["scheduler"]["capability"]
    assert reported["health"] == "unsatisfied"
    assert reported["next_due"] is None
    assert removed["scheduler"]["state"] == "unsatisfied"
    assert not (root / "Library").exists()
    assert _calls(log) == []
