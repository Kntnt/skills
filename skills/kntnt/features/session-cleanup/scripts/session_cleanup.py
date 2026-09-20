# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Stop what an agent session started, at the moments that session begins and ends.

An agent starts a dev server to look at a page, writes a scratch directory to
hold an intermediate result, runs a container to reproduce a bug — and then the
session ends and every one of those outlives it. The judgement that separates
them from the things the user asked for is only cheap at one moment: the moment
something is started, by the agent that started it and knows why. Ten minutes
later, from outside, a process list cannot tell the agent's own dev server from
the user's, and a machine running several agent sessions at once cannot tell one
session's work from another's at all.

So this feature does not guess. The instruction block it installs asks the agent
to record what it starts; this hook stops exactly what is recorded and nothing
else. What that costs is that an unrecorded process survives; what it buys is
that no process anybody else owns is ever killed, which is the failure that
cannot be undone.

Both halves are installed together and removed together, because either alone is
worse than neither: the block without the hook asks for records nothing reads,
and the hook without the block reads an empty manifest forever while looking
perfectly healthy.

The sweep runs at a session's start as well as at its end. A hard kill, a crash,
and a Harness whose end event is weak can leave an ended session's manifest
behind. A nested session can also find its own launcher's manifest, so a start
never sweeps a manifest holding the current process or an ancestor. A manifest
without reliable Harness ownership waits for the age backstop; a known live
owner is protected regardless of age (ADR-0199). Sweeping eligible manifests at
the start makes cleanup converge over disk, as ADR-0179 requires.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

OWNER = "kntnt.session-cleanup"

# The lifecycle moments this feature asks each Harness for, in that Harness's
# own vocabulary. A turn ending is not a session ending and buys nothing here,
# so the turns between the two are left out: an entry at a moment this feature
# would do nothing at is an entry a health check still has to account for.
EVENTS: dict[str, tuple[str, ...]] = {
    "claude-code": ("SessionStart", "SessionEnd"),
    "codex": ("SessionStart", "SessionEnd"),
    "opencode": ("session.created", "session.deleted"),
}

START_EVENTS = frozenset({"SessionStart", "sessionStart", "session.created"})
END_EVENTS = frozenset({"SessionEnd", "sessionEnd", "session.deleted"})

# The one reason a session ends that is not an ending. Claude Code fires
# SessionEnd with this when a session is being suspended to be taken up again,
# and stopping that session's processes would take the work away from under
# the user who is about to come back to it. The judgement is made here rather
# than by a matcher in a Harness's own hook table, because only one of the
# three Harnesses has matchers and the decision is the same in all three.
RESUMING = frozenset({"resume"})

# Unknown ownership, including legacy terminal-only records, waits this long.
# Known live ownership never expires merely because no new work was recorded.
STALE_HOURS = 24

# How long a terminated process is given to go before it is killed outright.
TERMINATE_GRACE_SECONDS = 5.0

# A container id as the two runtimes that issue them write one.
CONTAINER_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,127}$")

KINDS = ("pid", "container", "path")


class RecordingError(RuntimeError):
    """A manifest line this feature refuses to write."""


def home() -> Path:
    """Return the home this feature resolves its own state against.

    `KNTNT_HOME` first, exactly as the Manager's own `home()` resolves it, so a
    dry run against a sandbox home reaches this feature's state too and a real
    run is never reached by one.
    """

    override = os.environ.get("KNTNT_HOME")
    return Path(override) if override else Path.home()


def data_dir() -> Path:
    """Return the directory this feature keeps manifests and its log in.

    Under `~/.kntnt/<feature>/` and never under a Harness's own home: a second
    Harness would otherwise have to write into the first one's directory to
    record a session it ran (ADR-0005).
    """

    return home() / ".kntnt" / "session-cleanup"


def sessions_dir() -> Path:
    """Return the directory holding one manifest per session."""

    return data_dir() / "sessions"


def retire_pointers() -> None:
    """Remove obsolete terminal pointers without following directory symlinks."""

    directory = data_dir() / "current"
    try:
        if directory.is_symlink():
            directory.unlink()
        elif directory.exists():
            for path in directory.iterdir():
                if path.name.isdecimal() and (path.is_file() or path.is_symlink()):
                    path.unlink(missing_ok=True)
            directory.rmdir()
    except OSError as exc:
        log("pointer-retirement-failed", detail=str(exc))


def log_path() -> Path:
    """Return the file every action is written to.

    The hook runs while the user's screen is disappearing, so there is nowhere
    to report to: it acts and it records, and the record is read afterwards by
    whoever wants to know what happened.
    """

    return data_dir() / "cleanup.log"


def _library(*relative: str) -> Path:
    """Return the Collection Library module this feature reads its mechanics from.

    A Feature ships inside the Manager, so there is one layout rather than the
    two an installed Skill has to try: `features/<name>/scripts/` sits two
    directories under the Manager, and `library/scripts/` sits one.
    """

    return Path(__file__).resolve().parents[3] / "library" / "scripts" / Path(*relative)


def _integrations() -> Any:
    """Load the Collection Library's owned-integration mechanics.

    Which file a Harness reads its instructions from, and how a hook table of
    its is written, is the Library's knowledge and never a Feature's (ADR-0177).
    """

    import importlib.util

    path = _library("integrations.py")
    spec = importlib.util.spec_from_file_location("kntnt_integrations", path)
    if spec is None or spec.loader is None:  # pragma: no cover - unreachable in tests
        raise RecordingError(f"the Collection Library is not readable at {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _now() -> str:
    """Return this moment, as every line this feature writes spells one."""

    return datetime.now(UTC).isoformat(timespec="seconds")


def log(event: str, **fields: Any) -> None:
    """Append one line about one thing this feature did, and never raise.

    A cleanup that cannot write its log still has a session to let go of, so
    the failure to record is swallowed here rather than becoming the reason a
    shutdown breaks.
    """

    line = json.dumps({"at": _now(), "event": event, **fields}, sort_keys=True)
    try:
        log_path().parent.mkdir(parents=True, exist_ok=True)
        with log_path().open("a", encoding="utf-8") as handle:
            handle.write(line + "\n")
    except OSError:
        pass


def safe_key(value: str) -> str:
    """Return *value* as a filename, with anything a path could use taken out."""

    cleaned = re.sub(r"[^A-Za-z0-9._-]", "-", value).strip("-.")
    return cleaned[:128] or "unnamed"


def recording_shell_session() -> int:
    """Return a recording-shell identifier used only for unowned filenames.

    Tool calls and hooks can each have a short-lived POSIX session. Its life
    says nothing about the Harness lifetime and never authorizes cleanup.
    """

    try:
        return os.getsid(0)
    except OSError:  # pragma: no cover - POSIX only
        return os.getpid()


def alive(pid: int) -> bool:
    """True when *pid* names a process this machine still holds."""

    if pid <= 1:
        return True
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return True
    return True


def started_at(pid: int) -> str:
    """Return when *pid* started, as the machine reports it, or an empty string.

    Recorded when a process is registered and compared before it is stopped,
    because a process id is reused: without this, a manifest that outlived its
    process could name a number some unrelated program now answers to. An
    answer this cannot get is an empty string, and a comparison against an
    empty string never authorizes a kill.
    """

    try:
        completed = subprocess.run(
            ["ps", "-o", "lstart=", "-p", str(pid)],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return completed.stdout.strip() if completed.returncode == 0 else ""


def temp_roots() -> list[Path]:
    """Return the directories a recorded path may be deleted from.

    A manifest line is data and never an instruction: it arrives from a file
    on disk, and a line naming `/` must not be able to do what it says. So a
    deletion is bounded by where scratch work belongs rather than by what the
    line asks for, and everything outside is logged and left.
    """

    candidates = [
        tempfile.gettempdir(),
        os.environ.get("TMPDIR") or "",
        "/tmp",
        "/private/tmp",
        "/var/folders",
        "/private/var/folders",
    ]
    roots: list[Path] = []
    for candidate in candidates:
        if not candidate:
            continue
        try:
            resolved = Path(candidate).resolve()
        except OSError:
            continue
        if resolved.is_dir() and resolved not in roots:
            roots.append(resolved)
    return roots


def under_temp(path: Path) -> Path | None:
    """Return *path* resolved when it lies inside a temp root, or None.

    Symbolic links are resolved before the test, so a link planted inside a
    temp root cannot reach out of one, and a root itself never passes: the
    directory scratch work lives in is not scratch work.
    """

    try:
        resolved = path.expanduser().resolve()
    except (OSError, RuntimeError):
        return None
    for root in temp_roots():
        if resolved != root and resolved.is_relative_to(root):
            return resolved
    return None


def manifest_path(key: str) -> Path:
    """Return the manifest file one session records into."""

    return sessions_dir() / f"{safe_key(key)}.jsonl"


def session_owner() -> tuple[str, int, str]:
    """Find the nearest Harness ancestor, ignoring inherited outer identities.

    Claude publishes its PID, including when its executable is version-named.
    Other supported local Harnesses are recognized by executable name. Shells,
    hook runners, and Claude's background PTY helpers are not owners.
    """

    chain = process_chain()
    if chain is None:
        return "", 0, ""
    for pid, command in chain:
        executable = Path(command).name
        if str(pid) == os.environ.get("CLAUDE_PID") or executable == "claude":
            return "claude-code", pid, started_at(pid)
        if executable in {"codex", "opencode"}:
            return executable, pid, started_at(pid)
    return "", 0, ""


def current_key() -> str:
    """Resolve shell identity using its nearest Harness, never an outer one.

    Claude and Codex expose the lifecycle session ID to tools. OpenCode does
    not consistently do so: its recordings belong to the server process until
    that process ends. With no identifiable owner the recording shell supplies
    only a filename, never evidence that the work has ended.
    """

    harness, pid, started = session_owner()
    variable = {
        "claude-code": "CLAUDE_CODE_SESSION_ID",
        "codex": "CODEX_SESSION_ID",
    }.get(harness)
    session = os.environ.get(variable, "") if variable else ""
    if session:
        return session
    if pid and started:
        return f"process-{pid}-{safe_key(started)}"
    return f"unowned-{recording_shell_session()}"


def read_manifest(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return one manifest's header and its entries, skipping what will not parse.

    A line that is not JSON is a line some interrupted write left half-finished
    or some hand edit mistyped. It is skipped rather than raised about: the
    entries around it name real processes, and refusing the whole file over one
    bad line would leave every one of them running.
    """

    header: dict[str, Any] = {}
    entries: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return header, entries

    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            loaded = json.loads(line)
        except ValueError:
            continue
        if not isinstance(loaded, dict):
            continue
        if loaded.get("kind") == "session":
            header = loaded
        elif loaded.get("kind") in KINDS:
            entries.append(loaded)
    return header, entries


def append(path: Path, record: dict[str, Any]) -> None:
    """Append one JSON line to a manifest, creating what it needs."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")


def open_session(key: str, harness: str, session: str) -> None:
    """Record a Harness lifetime independently of the hook's POSIX session."""

    detected, pid, started = session_owner()
    if harness and detected != harness:
        pid, started = 0, ""
    path = manifest_path(key)
    header, _ = read_manifest(path)
    if not header or (
        pid and (header.get("owner_pid"), header.get("owner_started")) != (pid, started)
    ):
        append(
            path,
            {
                "kind": "session",
                "id": key,
                "harness": harness or detected,
                "session": session,
                "owner_pid": pid,
                "owner_started": started,
                "started": _now(),
            },
        )


def stop_pid(entry: dict[str, Any]) -> dict[str, Any]:
    """Stop one recorded process, or say why it was left alone.

    The process group goes only where the recorded process leads one. A process
    that is not its own group leader shares a group with whatever started it —
    on this machine, the agent's own shell — and signalling that group would
    reach far past anything this feature was told about. So a leader is stopped
    with everything it spawned and a follower is stopped alone, which is the
    honest half of the job rather than a guess at the whole of it.
    """

    try:
        pid = int(str(entry.get("id")))
    except ValueError:
        return {"outcome": "unreadable", "detail": "the id is not a process number"}

    if pid <= 1 or pid == os.getpid():
        return {"outcome": "refused", "detail": "that is not a process to stop"}
    if not alive(pid):
        return {"outcome": "gone", "detail": None}

    recorded = str(entry.get("started") or "")
    if recorded and started_at(pid) != recorded:
        return {
            "outcome": "reused",
            "detail": "the process id now names something else and was left alone",
        }

    target, scope = pid, "process"
    try:
        if os.getpgid(pid) == pid:
            target, scope = -pid, "group"
    except OSError:
        pass

    try:
        os.kill(target, signal.SIGTERM)
    except OSError as exc:
        return {"outcome": "failed", "detail": str(exc)}

    deadline = time.monotonic() + TERMINATE_GRACE_SECONDS
    while time.monotonic() < deadline and alive(pid):
        time.sleep(0.1)
    if alive(pid):
        try:
            os.kill(target, signal.SIGKILL)
        except OSError as exc:
            return {"outcome": "failed", "detail": str(exc)}
        return {"outcome": "killed", "detail": scope}
    return {"outcome": "stopped", "detail": scope}


def stop_container(entry: dict[str, Any]) -> dict[str, Any]:
    """Remove one recorded container, where a runtime is here to remove it."""

    name = str(entry.get("id") or "")
    if not CONTAINER_ID.match(name):
        return {"outcome": "unreadable", "detail": "the id is not a container name"}

    runtime = shutil.which("docker") or shutil.which("podman")
    if runtime is None:
        return {"outcome": "unavailable", "detail": "no container runtime is on PATH"}

    try:
        completed = subprocess.run(
            [runtime, "rm", "--force", name],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"outcome": "failed", "detail": str(exc)}
    if completed.returncode != 0:
        return {"outcome": "failed", "detail": completed.stderr.strip()[:200]}
    return {"outcome": "removed", "detail": runtime}


def remove_path(entry: dict[str, Any]) -> dict[str, Any]:
    """Delete one recorded scratch path, where it lies inside a temp root."""

    named = str(entry.get("id") or "")
    if not named:
        return {"outcome": "unreadable", "detail": "the id names no path"}

    resolved = under_temp(Path(named))
    if resolved is None:
        return {
            "outcome": "refused",
            "detail": "the path is not under a temp root and was left alone",
        }
    if not resolved.exists() and not resolved.is_symlink():
        return {"outcome": "gone", "detail": None}

    try:
        if resolved.is_dir() and not resolved.is_symlink():
            shutil.rmtree(resolved)
        else:
            resolved.unlink()
    except OSError as exc:
        return {"outcome": "failed", "detail": str(exc)}
    return {"outcome": "deleted", "detail": str(resolved)}


ACTIONS = {"pid": stop_pid, "container": stop_container, "path": remove_path}


def sweep(
    path: Path, *, why: str, sweeper_session: str = "", sweeper_harness: str = ""
) -> dict[str, Any]:
    """Act on every entry one manifest holds, log all of it, and take it away.

    A manifest that recorded nothing is logged as exactly that. Recording is
    the one step of this design that depends on an agent remembering to take
    it, so whether it happens has to be visible somewhere, and a session that
    ended having written nothing down is the evidence that it did not.
    """

    header, entries = read_manifest(path)
    acted: list[dict[str, Any]] = []
    for entry in entries:
        action = ACTIONS.get(str(entry.get("kind")))
        result = (
            action(entry)
            if action is not None
            else {"outcome": "unreadable", "detail": "no such kind"}
        )
        acted.append({**result, "kind": entry.get("kind"), "id": entry.get("id")})
        log(
            "acted",
            why=why,
            sweeper_session=sweeper_session,
            sweeper_harness=sweeper_harness,
            session=header.get("id") or path.stem,
            kind=entry.get("kind"),
            id=entry.get("id"),
            reason=entry.get("why"),
            outcome=result["outcome"],
            detail=result["detail"],
        )

    if not entries:
        log(
            "recorded-nothing",
            why=why,
            sweeper_session=sweeper_session,
            sweeper_harness=sweeper_harness,
            session=header.get("id") or path.stem,
            harness=header.get("harness"),
        )

    try:
        path.unlink(missing_ok=True)
    except OSError as exc:
        log("manifest-kept", session=path.stem, detail=str(exc))

    return {
        "session": header.get("id") or path.stem,
        "entries": len(entries),
        "acted": acted,
    }


def stale(path: Path) -> bool:
    """True when an unknown-owner manifest has reached the fallback age."""

    try:
        age = time.time() - path.stat().st_mtime
    except OSError:
        return False
    return age > STALE_HOURS * 3600


def process_chain() -> list[tuple[int, str]] | None:
    """Read this process's ancestry in nearest-first order, or fail closed."""

    try:
        completed = subprocess.run(
            ["ps", "-axo", "pid=,ppid=,comm="],
            cwd=home(),
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        if completed.returncode:
            return None
        parents = {
            int(pid): (int(parent), command)
            for pid, parent, command in (
                line.split(maxsplit=2) for line in completed.stdout.splitlines()
            )
        }
    except (OSError, subprocess.SubprocessError, ValueError):
        return None

    # A missing link cannot establish which Harness owns the calling shell.
    chain: list[tuple[int, str]] = []
    seen: set[int] = set()
    pid = os.getpid()
    while pid > 1 and pid not in seen:
        seen.add(pid)
        if pid not in parents:
            return None
        parent, command = parents[pid]
        chain.append((pid, command))
        pid = parent
    return chain


def process_ancestors() -> set[int] | None:
    """Return identities protecting a nested launch, or None on read failure."""

    chain = process_chain()
    return {pid for pid, _ in chain} if chain is not None else None


def live_recorded_processes(entries: list[dict[str, Any]]) -> set[int]:
    """Return live recorded identities, retaining an unreadable start time.

    A known reused id establishes that the recorded process has gone. A start
    time that cannot be read establishes nothing, so keeping a manifest is
    safer than treating that missing evidence as permission to sweep it.
    """

    processes: set[int] = set()
    for entry in entries:
        if entry.get("kind") != "pid":
            continue
        try:
            pid = int(str(entry.get("id")))
        except ValueError:
            continue
        if pid <= 1 or not alive(pid):
            continue
        recorded = str(entry.get("started") or "")
        current = started_at(pid)
        if not recorded or not current or current == recorded:
            processes.add(pid)
    return processes


def foreign_manifests(mine: str) -> list[Path]:
    """Select ended owners, retaining live or unreadable known identities.

    A missing owner (including legacy SID headers) waits for the age fallback.
    Recorded ancestors protect the entire manifest regardless of age or header.
    A known owner is released only by death or a changed process start time.
    """

    found: list[Path] = []
    ancestors = process_ancestors()
    if ancestors is None:
        return found
    try:
        candidates = sorted(sessions_dir().glob("*.jsonl"))
    except OSError:
        return found

    for path in candidates:
        if path.stem == safe_key(mine):
            continue
        header, entries = read_manifest(path)
        processes = live_recorded_processes(entries)
        if ancestors & processes:
            continue
        try:
            pid = int(header.get("owner_pid") or 0)
        except (TypeError, ValueError):
            pid = 0
        recorded = str(header.get("owner_started") or "")
        if pid > 1 and recorded:
            if not alive(pid):
                found.append(path)
                continue
            current = started_at(pid)
            if current and current != recorded:
                found.append(path)
            # A live owner or unreadable identity overrides the age fallback.
            continue
        if stale(path):
            found.append(path)
    return found


def hook(harness: str, event: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Run the one lifecycle moment a Harness just handed this feature.

    Fail-open in every branch and answered rather than raised, because this
    runs while a session is closing: a cleanup that breaks a shutdown is worse
    than a leak, so the exit code is zero whatever happened and the account of
    what happened is in the log.
    """

    retire_pointers()
    named = str(payload.get("hook_event_name") or event or payload.get("type") or "")
    session = str(payload.get("session_id") or payload.get("sessionID") or "")
    if harness == "opencode":
        properties = payload.get("properties")
        info = properties.get("info") if isinstance(properties, dict) else None
        session = str(info.get("id") or "") if isinstance(info, dict) else ""
    reason = str(payload.get("reason") or payload.get("source") or "")

    if named in START_EVENTS:
        key = session or f"unowned-{recording_shell_session()}"
        open_session(key, harness, session)
        swept = [
            sweep(path, why="start", sweeper_session=key, sweeper_harness=harness)
            for path in foreign_manifests(key)
        ]
        return {"moment": "start", "session": key, "swept": swept}

    if named in END_EVENTS:
        if not session:
            return {
                "moment": "end",
                "session": "",
                "swept": [],
                "kept": "unknown-session",
            }
        if reason in RESUMING:
            log("kept", why="resume", session=session, harness=harness)
            return {"moment": "end", "session": session, "swept": [], "kept": "resume"}
        key = session
        swept = [sweep(manifest_path(key), why="end")]
        return {"moment": "end", "session": key, "swept": swept}

    return {"moment": "ignored", "event": named}


def add(kind: str, identifier: str, why: str) -> dict[str, Any]:
    """Record one thing this session started, so the sweep can stop it later."""

    if kind not in KINDS:
        raise RecordingError(f"kind must be one of {', '.join(KINDS)}, not '{kind}'")
    if not identifier.strip():
        raise RecordingError("an entry needs something to name")
    if not why.strip():
        raise RecordingError("an entry needs a reason, so the log can be read later")

    record: dict[str, Any] = {
        "kind": kind,
        "id": identifier.strip(),
        "why": why.strip(),
        "at": _now(),
    }
    if kind == "pid":
        try:
            pid = int(identifier)
        except ValueError as exc:
            raise RecordingError(f"'{identifier}' is not a process number") from exc
        if not alive(pid):
            raise RecordingError(f"process {pid} is not running")
        record["started"] = started_at(pid)
    if kind == "path" and under_temp(Path(identifier)) is None:
        raise RecordingError(
            f"'{identifier}' is not under a temp root, and only a temp root is "
            "ever deleted; delete it yourself in the session that made it"
        )

    key = current_key()
    open_session(key, "", key)
    append(manifest_path(key), record)
    log("recorded", session=key, kind=kind, id=record["id"], reason=record["why"])
    return {"session": key, "recorded": record, "manifest": str(manifest_path(key))}


def _harness_records(
    action: str, harnesses: list[str], body: str
) -> list[dict[str, Any]]:
    """Apply one word to every named Harness, one folded record each.

    A block of prose and a hook table entry are two parts of one integration in
    one Harness, so they are folded into the one record that Harness earns: a
    reader told that two records disagreeing about one Harness is itself a
    finding must never be handed two records that are simply about two things.
    """

    integrations = _integrations()
    root = home()
    records: list[dict[str, Any]] = []
    for harness in harnesses:
        events = EVENTS.get(harness)
        if action == "install":
            parts = [
                integrations.install_block(OWNER, harness, root, body),
                integrations.install(
                    OWNER, harness, root, hook_command(), events=events
                ),
            ]
        elif action == "remove":
            parts = [
                integrations.remove_block(OWNER, harness, root),
                integrations.remove(OWNER, harness, root),
            ]
        else:
            parts = [
                integrations.block_health(OWNER, harness, root),
                integrations.health(OWNER, harness, root, events=events),
            ]
        records.append(integrations.fold(parts))
    return records


def hook_command() -> list[str]:
    """Return the command a Harness runs at a lifecycle moment.

    The script is named where it is installed rather than copied somewhere a
    second copy could go stale, which is what the one integration this
    collection already ships does.
    """

    return ["uv", "run", str(Path(__file__).resolve()), "hook"]


def add_command() -> str:
    """Return the command the instruction block tells the agent to record with.

    Without its verb, because the block and the usage line below each write
    their own: one shows `add`, the other shows what `add` takes.
    """

    return f"uv run {Path(__file__).resolve()}"


def instructions() -> str:
    """Return the block this feature installs, with its own command written in.

    The command is resolved at install time because it is an absolute path on
    the machine being written to, and a block naming a path that is not there
    asks for a recording that cannot happen.
    """

    source = Path(__file__).resolve().parents[1] / "instructions.md"
    return source.read_text(encoding="utf-8").replace("{{COMMAND}}", add_command())


def install_integrations(harnesses: list[str]) -> dict[str, Any]:
    """Install this Feature's block and hook into every Harness the Manager named."""

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    return {
        "installed": _harness_records("install", attempted, instructions()),
        "unsupported": {"count": len(named) - len(attempted)},
    }


def remove_integrations(harnesses: list[str]) -> dict[str, Any]:
    """Take this Feature's block and hook out of the Harnesses it was named for.

    Naming none means every supported Harness rather than the ones this
    machine has now: a Harness uninstalled since the block was written still
    holds the file it was written into, and removing what is already gone is a
    converged state rather than an error. That is the Manager's own call.

    Naming some narrows it to those, exactly as it narrows the mirror word. The
    seam accepts `--harness` on both words, so a caller reading them as
    symmetric must not lose an integration it never named.
    """

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    return {
        "removed": _harness_records("remove", attempted, ""),
        "unsupported": {"count": len(named) - len(attempted)},
    }


def feature_health(harnesses: list[str]) -> dict[str, Any]:
    """Report what each Harness actually holds of this Feature right now."""

    integrations = _integrations()
    supported = set(integrations.SUPPORTED)
    named = list(harnesses) or list(integrations.SUPPORTED)
    attempted = [harness for harness in named if harness in supported]
    return {
        "harnesses": _harness_records("health", attempted, ""),
        "unsupported": {"count": len(named) - len(attempted)},
        "data": str(data_dir()),
    }


def _emit(payload: dict[str, Any], stream: Any = None) -> None:
    """Print one machine-readable answer, on *stream* or on standard output."""

    target = sys.stdout if stream is None else stream
    json.dump(payload, target, indent=2, sort_keys=True)
    target.write("\n")


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse one session-cleanup invocation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "action",
        choices=(
            "install-integrations",
            "remove-integrations",
            "health",
            "hook",
            "add",
        ),
    )
    parser.add_argument("rest", nargs="*")
    parser.add_argument("--harness", action="append", default=[])
    parser.add_argument("--event", default="")
    parser.add_argument("--owner", default=OWNER)

    # Part of the seam every Feature answers on rather than a flag of this
    # one's: the Manager says one word in one shape to every Feature it
    # installs, and a Feature it had to remember the argument list of would
    # make the seam a table of exceptions. It means *the user has confirmed,
    # so you may take state another owner holds*, and this Feature holds
    # nothing of that kind — everything it owns goes in beside what is
    # already there — so it accepts the word and has no use for it.
    parser.add_argument("--replace", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run one session-cleanup action."""

    args = parse_args(sys.argv[1:] if argv is None else argv)

    # Lifecycle hooks log to disk: shutdown may already have closed both
    # output pipes, and reporting must not turn cleanup into a hook failure.
    if args.action == "hook":
        try:
            raw = sys.stdin.read()
        except OSError:
            raw = ""
        try:
            payload = json.loads(raw or "{}")
        except ValueError:
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        harness = args.harness[0] if args.harness else ""
        try:
            hook(harness, args.event, payload)
        except Exception as exc:  # noqa: BLE001 - a hook never becomes the session's problem
            log("hook-failed", harness=harness, detail=str(exc))
        return 0

    if args.action == "add":
        if len(args.rest) != 3:
            print(
                f'usage: {add_command()} add <{"|".join(KINDS)}> <id> "<why>"',
                file=sys.stderr,
            )
            return 2
        try:
            _emit(add(args.rest[0], args.rest[1], args.rest[2]))
        except RecordingError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        return 0

    if args.action == "install-integrations":
        _emit(install_integrations(args.harness))
    elif args.action == "remove-integrations":
        _emit(remove_integrations(args.harness))
    else:
        _emit(feature_health(args.harness))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
