"""Ordinary parent acquisition preserves genuine delegates without weakening guards."""

from __future__ import annotations

import importlib.util
import json
import os
import runpy
import subprocess
import sys
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT: Path = Path(__file__).resolve().parents[1]
RUNNER: Path = ROOT / "docs/evaluation/regressions/504/harness/ordinary_parent.py"
PROMPT: bytes = 'Neutral Åäö β\n`alpha` "bravo"\n\n'.encode()
RESULT: bytes = "Complete β\n".encode()


def load_runner() -> ModuleType:
    """Exercise the allocated recorder module, refusing a missing implementation."""
    spec: ModuleSpec | None = importlib.util.spec_from_file_location(
        "ordinary_redline_parent", RUNNER
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_sessions(root: Path) -> list[Path]:
    """Supply a documented synthetic parent trace and distinct delegate records."""

    # Reuse the intact native-v2 shape, never an actual historical result.
    fixture = runpy.run_path(str(ROOT / "tests/test_evaluation_dispatch.py"))
    parent: list[dict[str, Any]] = fixture["trace"]()
    parent[3]["payload"].update(model="gpt-6.1-sol", effort="xhigh")
    parent_path = root / "parent.jsonl"
    parent_path.write_text("".join(json.dumps(row) + "\n" for row in parent))

    # Distinct raw child identities link to the captured parent's exact identity.
    paths = [parent_path]
    for identity in ("correction-child", "checker-child"):
        child = {
            "type": "session_meta",
            "payload": {
                "id": identity,
                "session_id": "fresh",
                "source": {"subagent": {"thread_spawn": {"parent_thread_id": "fresh"}}},
                "thread_source": "subagent",
                "parent_thread_id": "fresh",
                "cli_version": "0.160.0",
            },
        }
        path = root / f"{identity}.jsonl"
        context = {
            "type": "turn_context",
            "payload": {"model": "gpt-6.1-sol", "effort": "xhigh"},
        }
        path.write_text(json.dumps(child) + "\n" + json.dumps(context) + "\n")
        paths.append(path)
    return paths


def test_one_completed_parent_preserves_every_genuine_child_session(
    tmp_path: Path,
) -> None:
    """A real multi-session parent has one result and three retained identities."""

    # Arrange complete exact input/result and linked, separately captured children.
    paths = write_sessions(tmp_path)
    recorder = load_runner()

    # Act through the public completed-parent capture boundary.
    receipt, result = recorder.capture_parent(
        tmp_path, PROMPT, RESULT, "gpt-6.1-sol", "xhigh", "0.160.0"
    )

    # Assert the native parent binding and all raw session identities independently.
    assert result == RESULT
    assert receipt["parent"]["thread_id"] == "fresh"
    assert {entry["thread_id"] for entry in receipt["sessions"]} == {
        "fresh",
        "correction-child",
        "checker-child",
    }
    assert {entry["path"] for entry in receipt["sessions"]} == {
        str(path) for path in paths
    }
    assert all(path.exists() for path in paths)


def test_an_unrelated_session_cannot_be_reported_as_a_genuine_delegate(
    tmp_path: Path,
) -> None:
    """Parent completion does not authenticate an unrelated captured child."""

    # Arrange a completed parent beside a delegate belonging to another root.
    paths = write_sessions(tmp_path)
    rows = [json.loads(line) for line in paths[1].read_text().splitlines()]
    rows[0]["payload"]["parent_thread_id"] = "other-root"
    paths[1].write_text("".join(json.dumps(row) + "\n" for row in rows))
    recorder = load_runner()

    # Act and assert through the capture boundary, preserving all raw evidence.
    with pytest.raises(recorder.DISPATCH.CaptureError, match="ancestry"):
        recorder.capture_parent(
            tmp_path, PROMPT, RESULT, "gpt-6.1-sol", "xhigh", "0.160.0"
        )
    assert all(path.exists() for path in paths)


@pytest.mark.parametrize("case", ["model", "effort", "version", "missing-context"])
def test_each_genuine_delegate_requires_its_actual_frozen_seat(
    tmp_path: Path, case: str
) -> None:
    """A parent seat cannot stand in for a child's missing or different context."""

    # Arrange one independently wrong or absent child seat boundary.
    paths = write_sessions(tmp_path)
    rows = [json.loads(line) for line in paths[1].read_text().splitlines()]
    if case == "model":
        rows[1]["payload"]["model"] = "gpt-6-astra"
    elif case == "effort":
        rows[1]["payload"]["effort"] = "high"
    elif case == "version":
        rows[0]["payload"]["cli_version"] = "0.159.3"
    else:
        rows.pop()
    paths[1].write_text("".join(json.dumps(row) + "\n" for row in rows))
    recorder = load_runner()

    # Act and assert each delegate's own seat without replacing its evidence.
    with pytest.raises(recorder.DISPATCH.CaptureError, match="delegate seat"):
        recorder.capture_parent(
            tmp_path, PROMPT, RESULT, "gpt-6.1-sol", "xhigh", "0.160.0"
        )
    assert paths[1].exists()


@pytest.mark.parametrize("case", ["second-root", "partial", "terminal", "input"])
def test_ambiguous_or_incomplete_parent_never_supplies_a_result(
    tmp_path: Path, case: str
) -> None:
    """The ordinary selector retains strict one-parent native binding checks."""

    # Arrange one unsupported parent boundary with intact raw session files.
    paths = write_sessions(tmp_path)
    parent = [json.loads(line) for line in paths[0].read_text().splitlines()]
    prompt = PROMPT
    terminal = RESULT
    if case == "second-root":
        (tmp_path / "another-parent.jsonl").write_bytes(paths[0].read_bytes())
    elif case == "partial":
        parent.pop()
        paths[0].write_text("".join(json.dumps(row) + "\n" for row in parent))
    elif case == "terminal":
        terminal = RESULT.rstrip()
    else:
        prompt = PROMPT.rstrip()
    recorder = load_runner()

    # Act and assert through the existing accepted binding, without any fallback.
    with pytest.raises(recorder.DISPATCH.CaptureError):
        recorder.capture_parent(
            tmp_path, prompt, terminal, "gpt-6.1-sol", "xhigh", "0.160.0"
        )
    assert all(path.exists() for path in paths)


@pytest.mark.parametrize(
    "case", ["duplicate", "empty", "parent-id", "session", "source"]
)
def test_each_delegate_has_a_distinct_identity_in_the_actual_parent_session(
    tmp_path: Path, case: str
) -> None:
    """Malformed child metadata cannot be authenticated by a parent result."""

    # Arrange one conflicting child identity without changing its retained bytes.
    paths = write_sessions(tmp_path)
    rows = [json.loads(line) for line in paths[1].read_text().splitlines()]
    meta = rows[0]["payload"]
    if case == "duplicate":
        meta["id"] = "checker-child"
    elif case == "empty":
        meta["id"] = ""
    elif case == "parent-id":
        meta["id"] = "fresh"
    elif case == "session":
        meta["session_id"] = "foreign-session"
    else:
        meta["thread_source"] = "user"
    paths[1].write_text("".join(json.dumps(row) + "\n" for row in rows))
    recorder = load_runner()

    # Act and assert the same public capture boundary rejects every wrong identity.
    with pytest.raises(recorder.DISPATCH.CaptureError, match="identity"):
        recorder.capture_parent(
            tmp_path, PROMPT, RESULT, "gpt-6.1-sol", "xhigh", "0.160.0"
        )
    assert all(path.exists() for path in paths)


@pytest.mark.parametrize(
    "observe_ephemeral,stop_fails,sampling_fails,replace_install",
    [
        (False, False, False, False),
        (True, False, False, False),
        (False, True, False, False),
        (False, False, True, False),
        (False, False, False, True),
    ],
)
def test_public_launcher_preserves_real_home_hooks_all_sessions_and_credentials(
    tmp_path: Path,
    observe_ephemeral: bool,
    stop_fails: bool,
    sampling_fails: bool,
    replace_install: bool,
) -> None:
    """One CLI attempt retains its entire ordinary parent tree and owned inventory."""

    # Arrange native-v2 records and a stand-in for the external native CLI only.
    templates = tmp_path / "templates"
    templates.mkdir()
    write_sessions(templates)
    native = tmp_path / "bin" / "codex"
    native.parent.mkdir()
    native.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os, pathlib, shutil, sys, time\n"
        "if '--version' in sys.argv:\n"
        " print('codex-cli 0.160.0'); sys.exit(0)\n"
        "prompt = sys.stdin.buffer.read()\n"
        "native_home = pathlib.Path(os.environ['CODEX_HOME'])\n"
        "sessions = native_home / 'sessions'; sessions.mkdir()\n"
        "for p in pathlib.Path(os.environ['SYNTHETIC_SESSIONS']).glob('*.jsonl'):\n"
        " shutil.copy2(p, sessions / p.name)\n"
        "assert os.environ['HOME'] == os.environ['EXPECTED_REAL_HOME']\n"
        "assert '--enable' in sys.argv and 'hooks' in sys.argv\n"
        "assert (native_home / 'hooks.json').read_text() == '{\"hooks\":{}}'\n"
        "work = pathlib.Path(sys.argv[sys.argv.index('-C') + 1])\n"
        "assert (work / '.agents/skills/redline/SKILL.md').exists()\n"
        "assert (work / '.agents/skills/kntnt/library/references/delivery.md').exists()\n"
        "assert (work / 'input.md').read_bytes() == b'Ordinary source\\n'\n"
        "if os.environ['SAMPLING_FAILS'] == '1':\n"
        " version_root = work.parent / 'file-versions'\n"
        " deadline = time.monotonic() + 5\n"
        " while not version_root.is_dir() and time.monotonic() < deadline:\n"
        "  time.sleep(0.01)\n"
        " assert version_root.is_dir(), 'observer never became ready'\n"
        " version_root.chmod(0o500)\n"
        " (work / 'new-stage.md').write_text('New observed stage after denied storage.\\n')\n"
        " time.sleep(0.3)\n"
        " version_root.chmod(0o700)\n"
        "if os.environ['OBSERVE_EPHEMERAL'] == '1':\n"
        " stage = pathlib.Path(os.environ['TMPDIR']) / 'mechanical-input.md'\n"
        " stage.write_text('Exact ephemeral quotation boundary.\\n')\n"
        " version_root = work.parent / 'file-versions'\n"
        " deadline = time.monotonic() + 5\n"
        " observed = False\n"
        " while time.monotonic() < deadline:\n"
        "  if any(p.read_text() == 'Exact ephemeral quotation boundary.\\n' for p in version_root.glob('*.md')):\n"
        "   observed = True; break\n"
        "  time.sleep(0.05)\n"
        " assert observed, 'recorder did not capture ready stage file'\n"
        " stage.unlink()\n"
        "(work / 'auth.json').write_text('ordinary artifact, not a credential')\n"
        "target = pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1])\n"
        "target.write_bytes('Complete β\\n'.encode())\n"
        "print(json.dumps({'type':'synthetic-native-test', 'input_bytes':len(prompt)}))\n"
    )
    native.chmod(0o755)

    # Supply private fixture authentication and a deterministic lifecycle stand-in.
    auth = tmp_path / "auth"
    auth.mkdir()
    (auth / "auth.json").write_text("fixture credential never retained")
    (auth / "hooks.json").write_text('{"hooks":{}}')
    (auth / "config.toml").write_text('model = "gpt-6.1-sol"\n')
    cleanup = tmp_path / "cleanup.py"
    cleanup.write_text("import sys\nprint('registered ' + ' '.join(sys.argv[1:]))\n")
    prompt = tmp_path / "prompt.txt"
    prompt.write_bytes(PROMPT)
    materials = tmp_path / "materials"
    materials.mkdir()
    (materials / "input.md").write_bytes(b"Ordinary source\n")
    if replace_install:
        replacement = materials / ".agents/skills/redline/SKILL.md"
        replacement.parent.mkdir(parents=True)
        replacement.write_text("Uncommitted replacement instructions")
    external = tmp_path / "external"
    external.mkdir()
    (external / "sentinel.txt").write_text("pre-existing evaluator-owned sentinel")
    packet = tmp_path / "evidence"
    env = dict(os.environ)
    env.update(
        SYNTHETIC_SESSIONS=str(templates),
        EXPECTED_REAL_HOME=env["HOME"],
        OBSERVE_EPHEMERAL="1" if observe_ephemeral else "0",
        SAMPLING_FAILS="1" if sampling_fails else "0",
        PYTHONDONTWRITEBYTECODE="1",
    )
    executable = RUNNER
    if stop_fails:
        executable = tmp_path / "termination_failure.py"
        executable.write_text(
            "import importlib.util, sys, threading\n"
            f"spec = importlib.util.spec_from_file_location('recorder', {str(RUNNER)!r})\n"
            "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)\n"
            "def failed_stop(child):\n"
            " raise module.DISPATCH.CaptureError('injected unresolved owned group')\n"
            "module.DISPATCH.stop_owned = failed_stop\n"
            "base = threading.Thread\n"
            "def confined_thread(*args, **kwargs):\n"
            " kwargs['daemon'] = True; return base(*args, **kwargs)\n"
            "module.threading.Thread = confined_thread\n"
            "raise SystemExit(module.main())\n"
        )

    # Act through the public CLI in a new group with one finite native attempt.
    result = subprocess.run(
        [
            sys.executable,
            str(executable),
            "--revision",
            "68a4c1b783359c31135423fd561d763454e4674a",
            "--prompt",
            str(prompt),
            "--materials",
            str(materials),
            "--packet",
            str(packet),
            "--model",
            "gpt-6.1-sol",
            "--effort",
            "xhigh",
            "--version",
            "0.160.0",
            "--native",
            str(native),
            "--auth-home",
            str(auth),
            "--cleanup-script",
            str(cleanup),
            "--inventory-root",
            str(external),
            "--timeout",
            "30",
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        check=False,
        timeout=60,
        start_new_session=True,
    )

    # Assert the result, raw descendants, exact credential exclusion and cleanup.
    if replace_install:
        assert result.returncode == 1
        assert result.stdout == b""
        receipt = json.loads((packet / "receipt.json").read_text())
        assert "materials cannot replace" in receipt["reason"]
        assert (packet / "prompt.txt").read_bytes() == PROMPT
        assert not (packet / "events.jsonl").exists()
        return
    if sampling_fails:
        assert result.returncode == 1
        assert result.stdout == b""
        receipt = json.loads((packet / "receipt.json").read_text())
        assert receipt["status"] == "failed"
        assert "stage observer" in receipt["reason"]
        assert (packet / "sampling-errors.json").exists()
        assert len(list((packet / "native-sessions").glob("*.jsonl"))) == 3
        assert not (packet / "runtime").exists()
        return
    if stop_fails:
        assert result.returncode == 1
        assert result.stdout == b""
        receipt = json.loads((packet / "receipt.json").read_text())
        assert receipt["status"] == "failed"
        assert "unresolved owned group" in receipt["reason"]
        assert (packet / "cleanup-failed.json").exists()
        assert (packet / "runtime/native/auth.json").exists()
        assert len(list((packet / "native-sessions").glob("*.jsonl"))) == 3
        return
    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout == RESULT
    receipt = json.loads((packet / "receipt.json").read_text())
    assert receipt["status"] == "complete"
    assert receipt["method"] == "ordinary-native-parent"
    assert len(receipt["capture"]["sessions"]) == 3
    assert len(list((packet / "native-sessions").glob("*.jsonl"))) == 3
    for session in receipt["capture"]["sessions"]:
        retained = packet / session["retained_path"]
        assert retained.exists()
        assert load_runner().DISPATCH.digest(retained.read_bytes()) == session["sha256"]
    assert receipt["recorder_sha256"] == load_runner().DISPATCH.digest(
        RUNNER.read_bytes()
    )
    assert receipt["helper_sha256"] == load_runner().DISPATCH.digest(
        (ROOT / "docs/evaluation/harness/native_dispatch.py").read_bytes()
    )
    after = json.loads((packet / "inventory-after.json").read_text())
    ordinary = next(
        entry for name, entry in after.items() if name.endswith("/work/auth.json")
    )
    private = next(
        entry for name, entry in after.items() if name.endswith("/native/auth.json")
    )
    assert ordinary["sha256"] is not None
    assert private["sha256"] is None and private["credential_redacted"]
    before = json.loads((packet / "inventory-before.json").read_text())
    assert after[str(external)] == before[str(external)]
    assert (
        after[str(external / "sentinel.txt")] == before[str(external / "sentinel.txt")]
    )
    assert (packet / "work/.git").is_dir()
    assert not (packet / "runtime").exists()
    assert (auth / "auth.json").read_text() == "fixture credential never retained"
    assert len((packet / "registrations.jsonl").read_text().splitlines()) == 2
    if observe_ephemeral:
        versions = list((packet / "file-versions").glob("*.md"))
        assert any(
            p.read_bytes() == b"Exact ephemeral quotation boundary.\n" for p in versions
        )
        assert not (packet / "runtime/tmpdir/mechanical-input.md").exists()
