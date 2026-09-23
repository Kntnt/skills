"""hetzner's engine, `scripts/hetzner.py`, driven as its body drives it.

Every case runs the shipped script through `uv run` with `HOME` and
`KNTNT_HOME` under the test's own `tmp_path` — two different directories, so
that a key written under the collection's home rather than the operating
system's is caught rather than hidden — and with `hcloud` and the clipboard
stood in for on the `PATH`. The stand-in `hcloud` keeps a small state file the
way the real one keeps `cli.toml`, records every call's argv and environment,
and answers from that state, so nothing here reaches the network, the real
`~/.config/hcloud`, the real `~/.ssh` or the real clipboard. `ssh-keygen` is
the real one: a stand-in would make the mode, key material and byte-identity
assertions test the stand-in.
"""

from __future__ import annotations

import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from support.fake_binary import fake_binary_on_path

REPO_ROOT = Path(__file__).resolve().parent.parent
HETZNER = REPO_ROOT / "skills" / "infrastructure" / "hetzner" / "scripts" / "hetzner.py"
LIBRARY = REPO_ROOT / "skills" / "kntnt" / "library"
UV_CACHE = Path(os.environ.get("UV_CACHE_DIR") or Path.home() / ".cache" / "uv")

# The exit status of a refusal the engine can name, and of a failure it met.
REFUSED = 2
FAILED = 1

# The project the maintainer's first context is named after, and a token long
# and distinctive enough that finding it in output is never an accident.
PROJECT = "kntnt-wordpress"
SECRET = "clipboard-Token-0123456789-abcdefghijklmnopqrstuvwxyz"
AMBIENT = "ambient-Token-9876543210-zyxwvutsrqponmlkjihgfedcba"

pytestmark = pytest.mark.skipif(
    os.name != "posix" or shutil.which("ssh-keygen") is None,
    reason="the engine's key is made by the real ssh-keygen, under POSIX modes",
)

# The stand-in for `hcloud`. It holds what the real one holds in `cli.toml` —
# the contexts, their tokens and the active one — plus what each project holds
# on the service side, and answers the handful of commands the engine sends.
FAKE_HCLOUD = """\
import json
import os
import sys

state_path = os.environ["FAKE_HCLOUD_STATE"]
with open(os.environ["FAKE_HCLOUD_RECORD"], "a", encoding="utf-8") as record:
    record.write(json.dumps({"argv": sys.argv[1:], "env": dict(os.environ)}) + "\\n")
with open(state_path, encoding="utf-8") as handle:
    state = json.load(handle)

args = sys.argv[1:]
context = None
if args[:1] == ["--context"]:
    context, args = args[1], args[2:]


def save():
    with open(state_path, "w", encoding="utf-8") as handle:
        json.dump(state, handle)


def fail(message):
    print(f"hcloud: {message}", file=sys.stderr)
    sys.exit(1)


def project():
    name = context or state["active"]
    if name not in state["contexts"]:
        fail(f"context not found: {name}")
    token = state["contexts"][name]
    if token not in state["accepted"]:
        fail("unable to authenticate your API token (unauthorized)")
    return state["projects"].setdefault(name, {"servers": 0, "keys": []})


match args[:2]:
    case ["context", "active"]:
        if state["active"]:
            print(state["active"])
    case ["context", "list"]:
        for name in state["contexts"]:
            print(name)
    case ["context", "create"]:
        name = args[-1]
        if name in state["contexts"]:
            fail("name already used")
        token = os.environ.get("HCLOUD_TOKEN", "")
        if not token:
            fail("HCLOUD_TOKEN is not set")
        state["contexts"][name] = token
        state["active"] = name
        save()
        print(f"Context {name} created and activated")
    case ["context", "delete"]:
        state["contexts"].pop(args[2])
        if state["active"] == args[2]:
            state["active"] = ""
        save()
    case ["context", "use"]:
        state["active"] = args[2]
        save()
    case ["context", "unset"]:
        state["active"] = ""
        save()
    case ["server", "list"]:
        for number in range(project()["servers"]):
            print(1000 + number)
    case ["ssh-key", "list"]:
        for name in project()["keys"]:
            print(name)
    case ["ssh-key", "create"]:
        name = args[args.index("--name") + 1]
        project()["keys"].append(name)
        save()
    case _:
        fail(f"the stand-in does not know {args}")
"""


class Fixture:
    """One machine under `tmp_path`: its homes, its stand-ins and their records."""

    def __init__(self, tmp_path: Path, state: dict[str, Any], clipboard: str) -> None:
        self.home = tmp_path / "home"
        self.kntnt_home = tmp_path / "kntnt-home"
        self.home.mkdir()
        self.kntnt_home.mkdir()
        self.state_path = tmp_path / "hcloud-state.json"
        self.record_path = tmp_path / "hcloud-record.jsonl"
        self.clipboard_path = tmp_path / "clipboard-held"
        self.state_path.write_text(json.dumps(state), encoding="utf-8")
        self.record_path.write_text("", encoding="utf-8")
        self.clipboard_path.write_text(clipboard, encoding="utf-8")

        # Stand in for `hcloud` and for every clipboard reader the Library
        # script may reach for first, on macOS and on a Linux runner alike.
        self.environment = fake_binary_on_path(
            tmp_path, "hcloud", f"#!{sys.executable}\n{FAKE_HCLOUD}"
        )
        for reader in ("pbpaste", "wl-paste"):
            fake_binary_on_path(tmp_path, reader, '#!/bin/sh\ncat "$FAKE_CLIPBOARD"\n')
        self.environment |= {
            "HOME": str(self.home),
            "KNTNT_HOME": str(self.kntnt_home),
            "UV_CACHE_DIR": str(UV_CACHE),
            "FAKE_HCLOUD_STATE": str(self.state_path),
            "FAKE_HCLOUD_RECORD": str(self.record_path),
            "FAKE_CLIPBOARD": str(self.clipboard_path),
            # An ambient token the engine has to keep away from every call.
            "HCLOUD_TOKEN": AMBIENT,
            "HCLOUD_CONTEXT": "",
        }
        self.tmp_path = tmp_path

    @property
    def key(self) -> Path:
        return self.home / ".ssh" / "kntnt-agent"

    def state(self) -> dict[str, Any]:
        result: dict[str, Any] = json.loads(self.state_path.read_text("utf-8"))
        return result

    def records(self) -> list[dict[str, Any]]:
        lines = self.record_path.read_text(encoding="utf-8").splitlines()
        return [json.loads(line) for line in lines if line]

    def calls(self, *prefix: str) -> list[dict[str, Any]]:
        """The recorded calls whose argv, past any `--context`, starts with *prefix*."""

        found = []
        for record in self.records():
            argv = record["argv"]
            if argv[:1] == ["--context"]:
                argv = argv[2:]
            if argv[: len(prefix)] == list(prefix):
                found.append(record)
        return found

    def run(self, *args: str) -> subprocess.CompletedProcess[str]:
        uv = shutil.which("uv")
        assert uv is not None
        return subprocess.run(
            [uv, "run", "--python", sys.executable, str(HETZNER), *args],
            env=os.environ | self.environment,
            cwd=self.tmp_path,
            text=True,
            capture_output=True,
            check=False,
        )

    def setup(self, *flags: str) -> subprocess.CompletedProcess[str]:
        return self.run("setup", *flags, f"--library={LIBRARY}", PROJECT)


def _state(
    contexts: dict[str, str] | None = None,
    active: str = "",
    projects: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """A stand-in `hcloud` whose clipboard token and every listed token work."""

    contexts = contexts or {}
    return {
        "contexts": contexts,
        "active": active,
        "accepted": [SECRET, *contexts.values()],
        "projects": projects or {PROJECT: {"servers": 3, "keys": []}},
    }


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


# --- setup: the token --------------------------------------------------------


def test_setup_hands_the_clipboard_token_to_context_create_and_nothing_else(
    tmp_path: Path,
) -> None:
    fixture = Fixture(tmp_path, _state({"other": "other-token"}, "other"), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    creates = fixture.calls("context", "create")
    assert [call["argv"] for call in creates] == [
        ["context", "create", "--token-from-env", PROJECT]
    ]
    assert creates[0]["env"]["HCLOUD_TOKEN"] == SECRET
    others = [call for call in fixture.records() if call not in creates]
    assert others, "the engine made no call beside the create"
    for call in others:
        assert "HCLOUD_TOKEN" not in call["env"], call["argv"]
    for call in fixture.records():
        assert all(SECRET not in word for word in call["argv"]), call["argv"]
    assert SECRET not in result.stdout
    assert SECRET not in result.stderr
    assert fixture.state()["contexts"][PROJECT] == SECRET


def test_setup_reports_the_server_count_it_verified_with(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["project"] == PROJECT
    assert report["context"] == "created"
    assert report["servers"] == 3
    verifies = fixture.calls("server", "list")
    assert verifies and all(
        call["argv"][:2] == ["--context", PROJECT] for call in verifies
    )


def test_setup_restores_the_context_that_was_active(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state({"other": "other-token"}, "other"), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    assert fixture.state()["active"] == "other"
    assert [call["argv"] for call in fixture.calls("context", "use")] == [
        ["context", "use", "other"]
    ]
    assert fixture.calls("context", "unset") == []


def test_setup_unsets_the_context_it_created_where_none_was_active(
    tmp_path: Path,
) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    assert fixture.state()["active"] == ""
    assert fixture.calls("context", "use") == []
    assert len(fixture.calls("context", "unset")) == 1


def test_setup_refuses_an_existing_context_without_yes_and_creates_nothing(
    tmp_path: Path,
) -> None:
    contexts = {PROJECT: "old-token", "other": "other-token"}
    fixture = Fixture(tmp_path, _state(contexts, "other"), SECRET)

    result = fixture.setup()

    assert result.returncode == REFUSED
    assert "--yes" in result.stderr
    assert PROJECT in result.stderr
    assert fixture.calls("context", "create") == []
    assert fixture.calls("context", "delete") == []
    assert fixture.calls("ssh-key", "create") == []
    assert fixture.state()["contexts"][PROJECT] == "old-token"
    assert not fixture.key.exists()
    assert [call["argv"] for call in fixture.calls("context", "use")] == [
        ["context", "use", "other"]
    ]
    assert SECRET not in result.stdout + result.stderr


def test_setup_with_yes_replaces_the_context_and_restores_the_active_one(
    tmp_path: Path,
) -> None:
    contexts = {PROJECT: "old-token", "other": "other-token"}
    fixture = Fixture(tmp_path, _state(contexts, "other"), SECRET)

    result = fixture.setup("--yes")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["context"] == "replaced"
    assert [call["argv"] for call in fixture.calls("context", "delete")] == [
        ["context", "delete", PROJECT]
    ]
    assert len(fixture.calls("context", "create")) == 1
    assert fixture.state()["contexts"][PROJECT] == SECRET
    assert fixture.state()["active"] == "other"
    assert [call["argv"] for call in fixture.calls("context", "use")] == [
        ["context", "use", "other"]
    ]


def test_setup_with_yes_restores_the_replaced_context_where_it_was_active(
    tmp_path: Path,
) -> None:
    fixture = Fixture(tmp_path, _state({PROJECT: "old-token"}, PROJECT), SECRET)

    result = fixture.setup("--yes")

    assert result.returncode == 0, result.stderr
    assert fixture.state()["active"] == PROJECT
    assert [call["argv"] for call in fixture.calls("context", "use")] == [
        ["context", "use", PROJECT]
    ]


def test_setup_reports_a_token_the_project_does_not_accept(tmp_path: Path) -> None:
    state = _state({"other": "other-token"}, "other")
    state["accepted"].remove(SECRET)
    fixture = Fixture(tmp_path, state, SECRET)

    result = fixture.setup()

    assert result.returncode == FAILED
    assert "not accept" in result.stderr
    assert f"setup --yes {PROJECT}" in result.stderr
    assert SECRET not in result.stdout + result.stderr
    assert fixture.state()["active"] == "other"


def test_setup_with_an_empty_clipboard_creates_nothing(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state({"other": "other-token"}, "other"), "  \n")

    result = fixture.setup()

    assert result.returncode == REFUSED
    assert "clipboard" in result.stderr
    assert PROJECT not in fixture.state()["contexts"]
    assert fixture.state()["active"] == "other"
    assert not fixture.key.exists()


def test_setup_requires_the_library(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    result = fixture.run("setup", PROJECT)

    assert result.returncode == REFUSED
    assert "--library" in result.stderr
    assert fixture.records() == []


# --- setup: the agents' key --------------------------------------------------


def test_setup_generates_the_agents_key_once_under_home(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    first = fixture.setup()

    assert first.returncode == 0, first.stderr
    private, public = fixture.key, fixture.key.with_suffix(".pub")
    assert private.is_file() and public.is_file()
    assert _mode(private) == 0o600
    assert not (fixture.kntnt_home / ".ssh").exists()
    assert public.read_text(encoding="utf-8").startswith("ssh-ed25519 ")
    assert " kntnt-agent@" in public.read_text(encoding="utf-8")
    assert "ENCRYPTED" not in private.read_text(encoding="utf-8")
    report = json.loads(first.stdout)
    assert report["key"]["generated"] is True
    assert report["key"]["public_key"] == public.read_text(encoding="utf-8").strip()

    private_bytes, public_bytes = private.read_bytes(), public.read_bytes()
    second = fixture.setup("--yes")

    assert second.returncode == 0, second.stderr
    assert json.loads(second.stdout)["key"]["generated"] is False
    assert private.read_bytes() == private_bytes
    assert public.read_bytes() == public_bytes
    private_text = private.read_text(encoding="utf-8")
    body = "".join(private_text.strip().splitlines()[1:-1])
    for output in (first.stdout, first.stderr, second.stdout, second.stderr):
        assert private_text not in output
        assert body not in output


def test_setup_registers_the_agents_key_where_the_project_lacks_it(
    tmp_path: Path,
) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    public = fixture.key.with_suffix(".pub")
    assert [call["argv"] for call in fixture.calls("ssh-key", "create")] == [
        [
            "--context",
            PROJECT,
            "ssh-key",
            "create",
            "--name",
            "kntnt-agent",
            "--public-key-from-file",
            str(public),
        ]
    ]
    assert json.loads(result.stdout)["agent_key"] == "registered"


def test_setup_leaves_a_registered_agents_key_alone(tmp_path: Path) -> None:
    projects = {PROJECT: {"servers": 1, "keys": ["thomas", "kntnt-agent"]}}
    fixture = Fixture(tmp_path, _state(projects=projects), SECRET)

    result = fixture.setup()

    assert result.returncode == 0, result.stderr
    assert fixture.calls("ssh-key", "create") == []
    assert json.loads(result.stdout)["agent_key"] == "present"


# --- status ------------------------------------------------------------------


def test_status_reports_contexts_counts_and_the_key_without_a_token(
    tmp_path: Path,
) -> None:
    contexts = {
        PROJECT: "first-Token-aaaaaaaaaaaaaaaaaaaaaaaa",
        "kntnt-se": "second-Token-bbbbbbbbbbbbbbbbbbbbbb",
        "stale": "stale-Token-cccccccccccccccccccccccc",
    }
    state = _state(
        contexts,
        PROJECT,
        {
            PROJECT: {"servers": 2, "keys": ["kntnt-agent"]},
            "kntnt-se": {"servers": 0, "keys": []},
        },
    )
    state["accepted"].remove(contexts["stale"])
    fixture = Fixture(tmp_path, state, SECRET)
    fixture.key.parent.mkdir()
    subprocess.run(
        ["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "kntnt-agent@test"]
        + ["-f", str(fixture.key)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )

    result = fixture.run("status")

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["active_context"] == PROJECT
    by_name = {entry["name"]: entry for entry in report["contexts"]}
    assert set(by_name) == set(contexts)
    assert by_name[PROJECT]["accepted"] is True
    assert by_name[PROJECT]["servers"] == 2
    assert by_name[PROJECT]["agent_key"] is True
    assert by_name["kntnt-se"]["accepted"] is True
    assert by_name["kntnt-se"]["servers"] == 0
    assert by_name["kntnt-se"]["agent_key"] is False
    assert by_name["stale"]["accepted"] is False
    assert by_name["stale"]["servers"] is None
    assert report["key"]["exists"] is True
    public = fixture.key.with_suffix(".pub").read_text(encoding="utf-8").strip()
    assert report["key"]["public_key"] == public
    for token in [*contexts.values(), SECRET, AMBIENT]:
        assert token not in result.stdout + result.stderr
    for call in fixture.records():
        assert "HCLOUD_TOKEN" not in call["env"], call["argv"]
    assert fixture.calls("context", "use") == []
    assert fixture.calls("context", "create") == []
    assert fixture.state()["active"] == PROJECT


def test_status_says_where_the_agents_key_is_missing(tmp_path: Path) -> None:
    fixture = Fixture(tmp_path, _state(), SECRET)

    result = fixture.run("status")

    assert result.returncode == 0, result.stderr
    report = json.loads(result.stdout)
    assert report["contexts"] == []
    assert report["key"] == {
        "path": str(fixture.key),
        "exists": False,
        "public_key": None,
    }
    assert not fixture.key.exists()
