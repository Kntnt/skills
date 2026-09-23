# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Put a Hetzner Cloud project's token on this machine, and say what it reaches.

hetzner names a project by an hcloud context of the project's own name, and the
token lives where hcloud keeps it, in its own configuration file, readable by
its owner alone — so this Skill keeps no Credential File beside it (ADR-0218).
This engine is how a context gets there without the token passing through a
conversation, and how the user sees which projects the agents can reach.

Two subcommands, each exiting 0 on success, 2 on a refusal it can name and 1
on a failure it met, with the reason on stderr and the report as JSON on
stdout:

- `setup [--yes] --library=<path> <project>` creates the project's context
  from the token on the clipboard, through the Collection Library's
  `credentials.py exec`, so the token stands in the environment of the one
  `hcloud context create` call and nowhere else. It refuses to replace an
  existing context without `--yes`, verifies the token by listing the
  project's servers, makes the agents' own SSH key where this machine has
  none, registers its public half in the project where the project holds no
  key of that name, and leaves hcloud's active context as it found it.
- `status` lists every context, whether its token is accepted and how many
  servers it sees, the agents' key and its public half, and per context
  whether the project holds the agents' key.

It runs `hcloud`, `ssh-keygen` and the Library script as subprocesses and
reaches nothing over the network itself. Nothing it prints is ever a token or
the private half of the key.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

# The exit status of a refusal this engine can name, and of a failure it met.
REFUSED: Final = 2
FAILED: Final = 1

# The name the agents' key carries on this machine, in its comment, and in
# every project it is registered in.
AGENT: Final = "kntnt-agent"

# How long one `hcloud` call may take. Most reach the Hetzner API, which
# answers in well under a second; a call still running after this is reported
# as the failure it is rather than waited on without end.
TIMEOUT_SECONDS: Final = 60

# The variables through which the environment overrides the context hcloud is
# told to use. Each is kept from every call: an ambient token would be used in
# place of the named context's, and an ambient context would stand in for the
# active one this engine reads and restores.
AMBIENT: Final = ("HCLOUD_TOKEN", "HCLOUD_CONTEXT")

# The modes of the directory the key lives in and of the private key itself.
SSH_DIRECTORY_MODE: Final = 0o700
KEY_MODE: Final = 0o600


class Refusal(Exception):
    """A refusal this engine can name, carrying the reason it prints."""


class Failure(Exception):
    """A failure this engine met, carrying the reason it prints."""


@dataclass(frozen=True)
class Answer:
    """What one `hcloud` call returned: its status and its two streams."""

    status: int
    stdout: str
    stderr: str

    def reason(self) -> str:
        """The last line hcloud wrote to stderr, which is where it says why."""

        lines = [line.strip() for line in self.stderr.splitlines() if line.strip()]
        return lines[-1] if lines else f"exit {self.status}"


def home() -> Path:
    """The user's home, which is where `~/.ssh` is and what calls run from.

    Raises:
        Refusal: where the operating system resolves no home directory.
    """

    try:
        return Path.home()
    except RuntimeError as error:
        raise Refusal(f"no home directory could be resolved ({error})") from error


def environment() -> dict[str, str]:
    """This process's environment without the variables in `AMBIENT`."""

    return {key: value for key, value in os.environ.items() if key not in AMBIENT}


def require(binary: str, source: str) -> None:
    """Refuse where *binary* is not on the `PATH`, naming where it comes from."""

    if shutil.which(binary) is None:
        raise Refusal(f"{binary} was not found on the PATH; install it from {source}")


def hcloud(*args: str) -> Answer:
    """Run `hcloud` with *args*, with no ambient token or context in its way.

    Raises:
        Failure: where the call runs past `TIMEOUT_SECONDS` or cannot start.
    """

    try:
        result = subprocess.run(
            ["hcloud", *args],
            cwd=home(),
            env=environment(),
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise Failure(
            f"`hcloud {' '.join(args)}` ran past {TIMEOUT_SECONDS} seconds"
        ) from error
    except OSError as error:
        raise Failure(f"hcloud could not be started ({error.strerror})") from error
    return Answer(result.returncode, result.stdout, result.stderr)


def checked(*args: str) -> Answer:
    """Run `hcloud` with *args* and fail where it does.

    Raises:
        Failure: where the call exits non-zero, with hcloud's own reason.
    """

    answer = hcloud(*args)
    if answer.status != 0:
        raise Failure(f"`hcloud {' '.join(args)}` failed: {answer.reason()}")
    return answer


def lines(text: str) -> list[str]:
    """The non-empty lines of *text*, each stripped."""

    return [line.strip() for line in text.splitlines() if line.strip()]


def contexts() -> list[str]:
    """The names of every context hcloud holds, in its own order."""

    return lines(
        checked("context", "list", "-o", "noheader", "-o", "columns=name").stdout
    )


def active_context() -> str | None:
    """The context hcloud's configuration names as active, or `None`."""

    return next(iter(lines(checked("context", "active").stdout)), None)


def restore(previous: str | None) -> None:
    """Make *previous* the active context again, or unset it where it was none."""

    if previous is None:
        checked("context", "unset")
    else:
        checked("context", "use", previous)


def servers(context: str) -> Answer:
    """List the ids of the servers *context*'s project holds."""

    return hcloud(
        "--context", context, "server", "list", "-o", "noheader", "-o", "columns=id"
    )


def key_names(context: str) -> list[str]:
    """The names of the SSH keys *context*'s project holds."""

    answer = checked(
        "--context", context, "ssh-key", "list", "-o", "noheader", "-o", "columns=name"
    )
    return lines(answer.stdout)


def key_path() -> Path:
    """The agents' private key, `~/.ssh/kntnt-agent`."""

    return home() / ".ssh" / AGENT


def public_half(private: Path) -> Path:
    """The public key beside *private*."""

    return private.with_name(f"{private.name}.pub")


def ensure_key() -> tuple[Path, bool]:
    """Make the agents' key where this machine has none, and return its path.

    An existing private key is left byte-identical. Where its public half is
    missing it is derived from the private key again, since it holds nothing
    the private key does not.

    Returns:
        The private key's path, and whether this call generated it.

    Raises:
        Failure: where `ssh-keygen` fails.
    """

    private = key_path()
    public = public_half(private)
    if private.exists():
        if not public.exists():
            derived = subprocess.run(
                ["ssh-keygen", "-y", "-f", str(private)],
                cwd=home(),
                stdin=subprocess.DEVNULL,
                capture_output=True,
                text=True,
                check=False,
            )
            if derived.returncode != 0:
                raise Failure(
                    f"ssh-keygen could not derive {public} from {private}:"
                    f" {derived.stderr.strip() or f'exit {derived.returncode}'}"
                )
            public.write_text(f"{derived.stdout.strip()}\n", encoding="utf-8")
        return private, False

    # Make `~/.ssh` for its owner alone where it is missing; an existing one is
    # the user's and is left as it is.
    directory = private.parent
    if not directory.exists():
        directory.mkdir(parents=True, mode=SSH_DIRECTORY_MODE)
        directory.chmod(SSH_DIRECTORY_MODE)

    # No passphrase: one would have to be typed by somebody, and the point of
    # this key is that nobody is there. What `ssh-keygen` prints is a
    # fingerprint and an image of it, never the key, and is not passed on.
    generated = subprocess.run(
        [
            "ssh-keygen",
            "-q",
            "-t",
            "ed25519",
            "-N",
            "",
            "-C",
            f"{AGENT}@{socket.gethostname()}",
            "-f",
            str(private),
        ],
        cwd=home(),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
    )
    if generated.returncode != 0:
        raise Failure(
            f"ssh-keygen could not make {private}:"
            f" {generated.stderr.strip() or f'exit {generated.returncode}'}"
        )
    private.chmod(KEY_MODE)
    return private, True


def public_key(private: Path) -> str | None:
    """The public half's one line, or `None` where there is none."""

    public = public_half(private)
    if not public.exists():
        return None
    return public.read_text(encoding="utf-8").strip()


def create_context(library: Path, project: str) -> None:
    """Create *project*'s context from the token on the clipboard.

    The Library script reads the clipboard and runs `hcloud context create`
    with the token in that one child's environment, so it never stands in an
    argument, on a terminal or in this engine.

    Raises:
        Refusal: where the Library script refuses, such as over an empty
            clipboard, with its own reason.
        Failure: where `hcloud context create` fails.
    """

    script = library / "scripts" / "credentials.py"
    if not script.is_file():
        raise Refusal(f"--library={library} holds no scripts/credentials.py")
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "exec",
            "--env=HCLOUD_TOKEN",
            "--from-clipboard",
            "--",
            "hcloud",
            "context",
            "create",
            "--token-from-env",
            project,
        ],
        cwd=home(),
        env=environment(),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return
    reason = result.stderr.strip() or f"exit {result.returncode}"
    if reason.startswith("credentials.py:"):
        raise Refusal(reason.removeprefix("credentials.py:").strip())
    raise Failure(f"`hcloud context create` failed: {reason}")


def setup(project: str, library: Path, replace: bool) -> dict[str, Any]:
    """Create *project*'s context, verify it, and ensure the agents' key.

    hcloud activates every context it creates, so the active context is read
    before anything else and put back on every path out, the refusal included.

    Raises:
        Refusal: where the context exists and *replace* is false, a binary is
            missing, or the clipboard holds no token.
        Failure: where hcloud or ssh-keygen fails, or the token is refused.
    """

    require("hcloud", "https://github.com/hetznercloud/cli")
    require("ssh-keygen", "the operating system's OpenSSH package")

    previous = active_context()
    try:
        # Refuse to replace a working token by accident: `--yes` is how a
        # token is rotated, and nothing else reaches the replacement.
        existed = project in contexts()
        if existed and not replace:
            raise Refusal(
                f"a context named {project!r} already exists; `setup --yes"
                f" {project}` replaces its token with the one on the clipboard,"
                " which is how a token is rotated"
            )
        if existed:
            checked("context", "delete", project)
        try:
            create_context(library, project)
        except (Refusal, Failure) as error:
            if existed:
                raise type(error)(
                    f"{error}; the context {project!r} was deleted, so copy the"
                    f" project's token and run `setup {project}` to create it again"
                ) from error
            raise

        # Verify the token against the project before anything relies on it.
        listed = servers(project)
        if listed.status != 0:
            raise Failure(
                f"the Hetzner API did not accept the token of context {project!r}"
                f" ({listed.reason()}); copy a Read & Write token of that project"
                f" and run `setup --yes {project}`"
            )

        # Give the agents a key of their own, and put it in the project so a
        # server created there gets it at creation.
        private, generated = ensure_key()
        registered = AGENT in key_names(project)
        if not registered:
            checked(
                "--context",
                project,
                "ssh-key",
                "create",
                "--name",
                AGENT,
                "--public-key-from-file",
                str(public_half(private)),
            )
    finally:
        restore(previous)

    return {
        "project": project,
        "context": "replaced" if existed else "created",
        "servers": len(lines(listed.stdout)),
        "active_context": previous,
        "key": {
            "path": str(private),
            "generated": generated,
            "public_key": public_key(private),
        },
        "agent_key": "present" if registered else "registered",
    }


def status() -> dict[str, Any]:
    """Say what every context reaches and what the agents' key is.

    Raises:
        Failure: where hcloud cannot list its contexts.
    """

    private = key_path()
    key = {
        "path": str(private),
        "exists": private.exists(),
        "public_key": public_key(private) if private.exists() else None,
    }
    if shutil.which("hcloud") is None:
        return {"hcloud": False, "active_context": None, "contexts": [], "key": key}

    reports = []
    for name in contexts():
        listed = servers(name)
        accepted = listed.status == 0
        reports.append(
            {
                "name": name,
                "accepted": accepted,
                "servers": len(lines(listed.stdout)) if accepted else None,
                "error": None if accepted else listed.reason(),
                "agent_key": AGENT in key_names(name) if accepted else None,
            }
        )
    return {
        "hcloud": True,
        "active_context": active_context(),
        "contexts": reports,
        "key": key,
    }


def parser() -> argparse.ArgumentParser:
    """The command line. A usage error exits 2 with the usage line."""

    root = argparse.ArgumentParser(
        prog="hetzner.py",
        usage="%(prog)s setup [--yes] --library=<path> <project>\n"
        "       %(prog)s status",
        description="Set up and report hetzner's Hetzner Cloud contexts.",
    )
    commands = root.add_subparsers(dest="command", required=True)
    setup_command = commands.add_parser(
        "setup",
        prog="hetzner.py setup",
        usage="%(prog)s [--yes] --library=<path> <project>",
    )
    setup_command.add_argument("--yes", action="store_true")
    setup_command.add_argument("--library", required=True, type=Path)
    setup_command.add_argument("project")
    commands.add_parser("status", prog="hetzner.py status", usage="%(prog)s")
    return root


def main(argv: Sequence[str] | None = None) -> int:
    """Parse *argv*, run the subcommand, and return its exit status."""

    args = parser().parse_args(argv)
    try:
        if args.command == "setup":
            report = setup(args.project, args.library, args.yes)
        else:
            report = status()
    except Refusal as refusal:
        print(f"hetzner.py: {refusal}", file=sys.stderr)
        return REFUSED
    except Failure as failure:
        print(f"hetzner.py: {failure}", file=sys.stderr)
        return FAILED
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
