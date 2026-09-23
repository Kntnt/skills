"""The Collection Library's Credential File writer, driven as its callers do.

Every case runs the shipped script through `uv run` against a `KNTNT_HOME`
under the test's own `tmp_path`, with the platform's clipboard tools stood in
for on the `PATH`, so nothing here reads or writes the real clipboard or the
real `~/.kntnt`. The one exception is the failed write, which has to fail at
one exact moment inside the script and so imports it and patches `os.replace`,
as `test_kntnt.py` does for the same purpose.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path
from types import ModuleType

import pytest
from support.fake_binary import fake_binary_on_path, path_holding

REPO_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts" / "credentials.py"

# The exit status of every refusal the script can name, and of a usage error.
REFUSED = 2

# The shortest value `secrets.token_urlsafe` gives over 32 bytes, which is the
# least the script may draw.
GENERATED_LENGTH = 43

# A value long and distinctive enough that finding it in output is never an
# accident of some other text containing it.
SECRET = "s3cr3t-Value-0123456789-abcdefghij"

# The file modes the rule names: what a Credential File is written with, what
# its directory is created with, and a mode every reader refuses.
FILE_MODE = 0o600
DIRECTORY_MODE = 0o700
LOOSE_MODE = 0o644

# Mode bits mean nothing on Windows, where the script restricts the file's
# ACL instead, and nothing here can verify that without a Windows machine.
POSIX_ONLY = pytest.mark.skipif(
    os.name != "posix",
    reason="POSIX mode bits mean nothing on Windows, where the ACL is used",
)


def _module() -> ModuleType:
    """Load the shipped script as a module, without running its command line."""

    spec = importlib.util.spec_from_file_location("credentials", CREDENTIALS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _clipboard_pair() -> tuple[str, str]:
    """The binaries the script reads and writes the clipboard with here.

    The pair is read off the script's own table for the platform the suite is
    running on, so the fakes below stand in for exactly what the script's
    dispatch reaches for: `pbpaste` and `pbcopy` on macOS, and the first of the
    Linux tools on a CI runner.
    """

    module = _module()
    family = module.platform_family()
    return module.READERS[family][0][0], module.WRITERS[family][0][0]


def _fake_clipboard(tmp_path: Path, content: str) -> tuple[dict[str, str], Path]:
    """Stand in for the clipboard, holding *content*, and record what it is given.

    Returns the environment that reaches the fakes and the file the writing
    fake records its input to. The reading fake leaves `_clipboard_read`
    behind, so a case can tell that the clipboard was never read.
    """

    reader, writer = _clipboard_pair()
    held = tmp_path / "clipboard-held"
    held.write_text(content, encoding="utf-8")
    record = tmp_path / "clipboard-received"
    fake_binary_on_path(
        tmp_path,
        reader,
        '#!/bin/sh\ntouch "$FAKE_CLIPBOARD_READ"\ncat "$FAKE_CLIPBOARD_HELD"\n',
    )
    environment = fake_binary_on_path(
        tmp_path, writer, '#!/bin/sh\ncat > "$FAKE_CLIPBOARD_RECORD"\n'
    )
    environment |= {
        "FAKE_CLIPBOARD_HELD": str(held),
        "FAKE_CLIPBOARD_READ": str(_clipboard_read(tmp_path)),
        "FAKE_CLIPBOARD_RECORD": str(record),
    }
    return environment, record


def _clipboard_read(tmp_path: Path) -> Path:
    """The file the reading fake creates the moment the clipboard is read."""

    return tmp_path / "clipboard-read"


def _run(
    tmp_path: Path, *args: str, environment: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the shipped script against a home under *tmp_path*.

    The launcher is named by absolute path and handed the suite's own
    interpreter, so a case that empties the `PATH` still starts the script and
    only the script's own lookups see the emptied one.
    """

    uv = shutil.which("uv")
    assert uv is not None
    return subprocess.run(
        [uv, "run", "--python", sys.executable, str(CREDENTIALS), *args],
        env=os.environ | {"KNTNT_HOME": str(tmp_path)} | (environment or {}),
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )


def _credential_file(tmp_path: Path, skill: str = "demo") -> Path:
    return tmp_path / ".kntnt" / skill / "credentials.json"


def _write_credentials(tmp_path: Path, content: dict[str, str]) -> Path:
    """Put a Credential File in place the way a person writing it by hand would."""

    path = _credential_file(tmp_path)
    path.parent.mkdir(parents=True, mode=DIRECTORY_MODE)
    path.write_text(json.dumps(content), encoding="utf-8")
    path.chmod(FILE_MODE)
    return path


def _mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


# --- The command line -----------------------------------------------------


def test_the_script_declares_pep_723_metadata_and_no_dependency() -> None:
    """It runs anywhere `uv` does, on the standard library alone."""

    text = CREDENTIALS.read_text(encoding="utf-8")

    assert "# /// script\n" in text
    assert "# dependencies = []\n" in text


def test_an_unknown_subcommand_exits_2_with_a_usage_line(tmp_path: Path) -> None:
    result = _run(tmp_path, "rotate", "--skill=demo")

    assert result.returncode == REFUSED
    assert "usage:" in result.stderr


@pytest.mark.parametrize(
    "args",
    [
        ("set", "--key=token", "--from-clipboard"),
        ("set", "--skill=demo", "--from-clipboard"),
        ("set", "--skill=demo", "--key=token"),
        ("generate", "--skill=demo", "--key=token"),
        ("show",),
        ("exec", "--from-clipboard", "--", "true"),
        ("exec", "--env=TOKEN", "--skill=demo", "--", "true"),
        ("exec", "--env=TOKEN", "--from-clipboard"),
    ],
)
def test_a_missing_required_option_exits_2_with_a_usage_line(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    result = _run(tmp_path, *args)

    assert result.returncode == REFUSED
    assert "usage:" in result.stderr


@pytest.mark.parametrize(
    ("subcommand", "spelled"),
    [
        (
            "set",
            (
                "[--yes] --skill=<name> --key=<key> --from-clipboard"
                " [--set=<key>=<value>]..."
            ),
        ),
        (
            "generate",
            (
                "[--yes] --skill=<name> --key=<key> --to-clipboard"
                " [--set=<key>=<value>]..."
            ),
        ),
        ("show", "--skill=<name>"),
        (
            "exec",
            "--env=<VAR> (--from-clipboard | --skill=<name> --key=<key>) -- <command>...",
        ),
    ],
)
def test_the_usage_line_writes_every_valued_flag_attached(
    tmp_path: Path, subcommand: str, spelled: str
) -> None:
    """The collection's grammar attaches a flag's value, in usage as elsewhere."""

    result = _run(tmp_path, subcommand)

    assert result.returncode == REFUSED
    assert f"credentials.py {subcommand} {spelled}" in result.stderr


# --- set ------------------------------------------------------------------


def test_set_stores_the_clipboard_value_and_every_pair(tmp_path: Path) -> None:
    """The clipboard's text, trimmed, lands under the key beside the pairs."""

    environment, _ = _fake_clipboard(tmp_path, f"  {SECRET}\n")

    result = _run(
        tmp_path,
        "set",
        "--skill=demo",
        "--key=token",
        "--from-clipboard",
        "--set=account=acme",
        "--set=region=eu",
        environment=environment,
    )

    assert result.returncode == 0, result.stderr
    path = _credential_file(tmp_path)
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "account": "acme",
        "region": "eu",
        "token": SECRET,
    }
    report = json.loads(result.stdout)
    assert report == {
        "path": str(path),
        "keys": ["account", "region", "token"],
        "key": "token",
        "length": len(SECRET),
    }
    assert SECRET not in result.stdout + result.stderr


@POSIX_ONLY
def test_set_creates_the_directory_0700_and_the_file_0600(tmp_path: Path) -> None:
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(
        tmp_path,
        "set",
        "--skill=demo",
        "--key=token",
        "--from-clipboard",
        environment=environment,
    )

    assert result.returncode == 0, result.stderr
    path = _credential_file(tmp_path)
    assert _mode(path.parent) == DIRECTORY_MODE
    assert _mode(path) == FILE_MODE


def test_a_second_set_keeps_the_keys_the_file_already_holds(tmp_path: Path) -> None:
    _write_credentials(tmp_path, {"account": "acme", "token": "first"})
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(
        tmp_path,
        "set",
        "--skill=demo",
        "--key=secret",
        "--from-clipboard",
        "--set=region=eu",
        environment=environment,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(_credential_file(tmp_path).read_text(encoding="utf-8")) == {
        "account": "acme",
        "region": "eu",
        "secret": SECRET,
        "token": "first",
    }


@POSIX_ONLY
def test_set_refuses_a_file_whose_mode_admits_group_or_world(tmp_path: Path) -> None:
    """`set` is a reader too, and it does not quietly tighten what it found."""

    path = _write_credentials(tmp_path, {"token": "first"})
    path.chmod(LOOSE_MODE)
    before = path.read_bytes()
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(
        tmp_path,
        "set",
        "--yes",
        "--skill=demo",
        "--key=token",
        "--from-clipboard",
        environment=environment,
    )

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "0600" in result.stderr
    assert path.read_bytes() == before
    assert _mode(path) == LOOSE_MODE


def test_a_write_that_fails_after_its_temporary_file_leaves_the_file_standing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """No reader sees a partial file, and a failure costs the old one nothing."""

    path = _write_credentials(tmp_path, {"account": "acme", "token": "first"})
    before = path.read_bytes()
    environment, _ = _fake_clipboard(tmp_path, SECRET)
    for name, value in environment.items():
        monkeypatch.setenv(name, value)
    monkeypatch.setenv("KNTNT_HOME", str(tmp_path))
    module = _module()
    seen: list[Path] = []

    # Refuse the move into place, once the temporary file exists beside it.
    def fail_replace(source: str | Path, destination: str | Path) -> None:
        seen.append(Path(source))
        assert Path(source).exists()
        raise OSError("injected replace failure")

    monkeypatch.setattr(module.os, "replace", fail_replace)

    status = module.main(
        [
            "set",
            "--yes",
            "--skill=demo",
            "--key=token",
            "--from-clipboard",
            "--set=region=eu",
        ]
    )

    assert status == REFUSED
    assert seen and seen[0].parent == path.parent
    assert path.read_bytes() == before
    assert sorted(entry.name for entry in path.parent.iterdir()) == [path.name]
    assert SECRET not in capsys.readouterr().err


# --- generate -------------------------------------------------------------


def test_generate_stores_a_value_hands_it_to_the_clipboard_and_prints_none(
    tmp_path: Path,
) -> None:
    environment, record = _fake_clipboard(tmp_path, "")

    result = _run(
        tmp_path,
        "generate",
        "--skill=demo",
        "--key=webhook",
        "--to-clipboard",
        "--set=account=acme",
        environment=environment,
    )

    assert result.returncode == 0, result.stderr
    stored = json.loads(_credential_file(tmp_path).read_text(encoding="utf-8"))
    value = stored["webhook"]
    assert len(value) >= GENERATED_LENGTH
    assert stored["account"] == "acme"
    assert record.read_text(encoding="utf-8") == value
    assert value not in result.stdout
    assert value not in result.stderr
    report = json.loads(result.stdout)
    assert report["keys"] == ["account", "webhook"]
    assert report["key"] == "webhook"
    assert report["length"] == len(value)


# --- The overwrite gate ---------------------------------------------------

# Each writing subcommand as a caller spells it, without `--yes`.
WRITES = [
    ("set", "--skill=demo", "--key=token", "--from-clipboard"),
    ("generate", "--skill=demo", "--key=token", "--to-clipboard"),
]


@pytest.mark.parametrize("args", WRITES)
def test_replacing_a_held_key_without_yes_exits_2_and_touches_nothing(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    """Rotation destroys a working credential, so it is refused unless asserted.

    The refusal comes before the clipboard is read or written and before the
    file is, and it names the file, the key, and what `--yes` asserts.
    """

    path = _write_credentials(tmp_path, {"account": "acme", "token": "first"})
    before = path.read_bytes()
    environment, record = _fake_clipboard(tmp_path, SECRET)

    result = _run(tmp_path, *args, environment=environment)

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "token" in result.stderr
    assert "nothing was written" in result.stderr
    assert "--yes" in result.stderr
    assert "replace a working credential" in result.stderr
    assert path.read_bytes() == before
    assert not _clipboard_read(tmp_path).exists()
    assert not record.exists()
    assert "first" not in result.stdout + result.stderr


def test_a_pair_naming_a_held_key_is_refused_without_yes(tmp_path: Path) -> None:
    """A key beside the one filled is as much a working credential as that one."""

    path = _write_credentials(tmp_path, {"account": "acme"})
    before = path.read_bytes()
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(
        tmp_path,
        "set",
        "--skill=demo",
        "--key=token",
        "--from-clipboard",
        "--set=account=other",
        environment=environment,
    )

    assert result.returncode == REFUSED
    assert "account" in result.stderr
    assert path.read_bytes() == before
    assert not _clipboard_read(tmp_path).exists()
    assert "acme" not in result.stdout + result.stderr


@pytest.mark.parametrize("args", WRITES)
def test_replacing_a_held_key_with_yes_overwrites_it(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    _write_credentials(tmp_path, {"account": "acme", "token": "first"})
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(tmp_path, args[0], "--yes", *args[1:], environment=environment)

    assert result.returncode == 0, result.stderr
    stored = json.loads(_credential_file(tmp_path).read_text(encoding="utf-8"))
    assert stored["account"] == "acme"
    assert stored["token"] not in ("first", "")
    if args[0] == "set":
        assert stored["token"] == SECRET


@pytest.mark.parametrize("held", [None, {"token": ""}, {"account": "acme"}])
@pytest.mark.parametrize("args", WRITES)
def test_a_key_the_file_does_not_hold_is_written_without_yes(
    tmp_path: Path, args: tuple[str, ...], held: dict[str, str] | None
) -> None:
    """No file, an empty value and another key alike are nothing to overwrite."""

    if held is not None:
        _write_credentials(tmp_path, held)
    environment, _ = _fake_clipboard(tmp_path, SECRET)

    result = _run(tmp_path, *args, environment=environment)

    assert result.returncode == 0, result.stderr
    stored = json.loads(_credential_file(tmp_path).read_text(encoding="utf-8"))
    assert stored["token"]


# --- The clipboard's absence ----------------------------------------------


@pytest.mark.parametrize(
    "args",
    [
        ("set", "--skill=demo", "--key=token", "--from-clipboard"),
        ("generate", "--skill=demo", "--key=token", "--to-clipboard"),
    ],
)
def test_no_clipboard_tool_exits_2_naming_the_file_to_write_by_hand(
    tmp_path: Path, args: tuple[str, ...]
) -> None:
    """A server over SSH has no clipboard, and a person writes the file instead."""

    result = _run(
        tmp_path, *args, environment={"PATH": path_holding(tmp_path / "empty")}
    )

    assert result.returncode == REFUSED
    assert str(_credential_file(tmp_path)) in result.stderr
    assert "by hand" in result.stderr
    assert not _credential_file(tmp_path).exists()


def test_an_empty_clipboard_exits_2_naming_the_file_to_write_by_hand(
    tmp_path: Path,
) -> None:
    environment, _ = _fake_clipboard(tmp_path, " \n\t ")

    result = _run(
        tmp_path,
        "set",
        "--skill=demo",
        "--key=token",
        "--from-clipboard",
        environment=environment,
    )

    assert result.returncode == REFUSED
    assert str(_credential_file(tmp_path)) in result.stderr
    assert "by hand" in result.stderr
    assert not _credential_file(tmp_path).exists()


# --- show -----------------------------------------------------------------


def test_show_prints_the_keys_and_the_mode_and_no_value(tmp_path: Path) -> None:
    path = _write_credentials(tmp_path, {"account": "acme", "token": SECRET})

    result = _run(tmp_path, "show", "--skill=demo")

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {
        "path": str(path),
        "mode": f"{_mode(path):04o}",
        "keys": ["account", "token"],
    }
    assert SECRET not in result.stdout + result.stderr
    assert "acme" not in result.stdout + result.stderr


def test_show_on_a_missing_file_exits_2_naming_it(tmp_path: Path) -> None:
    result = _run(tmp_path, "show", "--skill=demo")

    assert result.returncode == REFUSED
    assert str(_credential_file(tmp_path)) in result.stderr


@POSIX_ONLY
def test_show_refuses_a_file_whose_mode_admits_group_or_world(tmp_path: Path) -> None:
    path = _write_credentials(tmp_path, {"token": SECRET})
    path.chmod(LOOSE_MODE)

    result = _run(tmp_path, "show", "--skill=demo")

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "0600" in result.stderr


# --- exec -----------------------------------------------------------------

# A child that writes down what it received and exits with a status of its
# own. It writes to a file rather than to its output, because its output is
# the script's output, and the value appearing there would be the child's doing.
CHILD = """
import json, os, sys
name, observed = sys.argv[1], sys.argv[2]
value = os.environ.get(name)
holders = sorted(key for key, held in os.environ.items() if value and value in held)
with open(observed, "w", encoding="utf-8") as handle:
    json.dump({"value": value, "holders": holders,
               "marker": os.environ.get("KNTNT_TEST_MARKER")}, handle)
sys.exit(7)
"""


def _child(tmp_path: Path) -> tuple[list[str], Path]:
    observed = tmp_path / "child-observed.json"
    return [sys.executable, "-c", CHILD, "TOKEN", str(observed)], observed


@pytest.mark.parametrize("source", ["clipboard", "file"])
def test_exec_gives_the_child_the_value_in_one_variable_and_its_status(
    tmp_path: Path, source: str
) -> None:
    """The value reaches a tool's own store without standing in an argument."""

    held = f"{SECRET}\n" if source == "clipboard" else ""
    environment, _ = _fake_clipboard(tmp_path, held)
    environment["KNTNT_TEST_MARKER"] = "inherited"
    if source == "clipboard":
        reading = ["--from-clipboard"]
    else:
        _write_credentials(tmp_path, {"token": SECRET})
        reading = ["--skill=demo", "--key=token"]
    child, observed = _child(tmp_path)

    result = _run(
        tmp_path, "exec", "--env=TOKEN", *reading, "--", *child, environment=environment
    )

    assert result.returncode == 7, result.stderr
    received = json.loads(observed.read_text(encoding="utf-8"))
    assert received == {"value": SECRET, "holders": ["TOKEN"], "marker": "inherited"}
    assert SECRET not in result.stdout + result.stderr


def test_exec_on_a_missing_key_exits_2_naming_it(tmp_path: Path) -> None:
    path = _write_credentials(tmp_path, {"account": "acme"})
    child, observed = _child(tmp_path)

    result = _run(
        tmp_path, "exec", "--env=TOKEN", "--skill=demo", "--key=token", "--", *child
    )

    assert result.returncode == REFUSED
    assert str(path) in result.stderr
    assert "token" in result.stderr
    assert not observed.exists()
