# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Keep the Standing Policy every routed Cohort starts from, and its history.

A Standing Policy is where one Cohort of work starts on the Rung ladder and how
far up and down that ladder routing may go. It ships working: the constants
below are the whole policy until something moves one Cohort, so a user never
edits a file to get a routing decision. The user layer beside `config.json`
holds only the overrides a threshold movement created, and the append-only
history beside it says what moved each one and from where.

The module lives in the Collection Library rather than under either Skill that
reads it. Model Selector's context derivation freezes the policy into the route
snapshot, its `config policy` adapter renders and resets it, and the evidence
import that evaluates the failure threshold runs inside the Library's own
`record`; a peer Skill's `scripts/` is not an interface any of them may reach
into, so the one store they share is here.

Nothing in this module resolves a symbolic bound into a concrete Rung. The
shipped values are symbolic on purpose: `cold_start`, `weakest_enabled`, and
`main_seat` mean whatever the request's own filtered candidate ladder makes
them mean, and only the route module holds that ladder.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# The version shared by the user layer and the frozen projection.
SCHEMA_VERSION: int = 1

# The two files the store owns, beside `config.json` in the data directory.
POLICY_FILE: str = "standing-policy.json"
HISTORY_FILE: str = "standing-policy-history.jsonl"

# The shipped default layer, as constants rather than as data: the failure
# threshold is read from here by the same import that evaluates it, and a
# second file nobody may edit would only be a second place to look.
DEFAULT_STARTING_RUNG: str = "cold_start"
DEFAULT_FLOOR: str = "weakest_enabled"
DEFAULT_CEILING: str = "main_seat"
DEFAULT_FAILURE_THRESHOLD: dict[str, int] = {"failures": 2, "window": 4}
DEFAULT_EXPLORATION: dict[str, Any] = {
    "epsilon": 0.1,
    "max_per_run": 1,
    "seed": "kntnt-standing-policy-v1",
}

# The revision a Cohort carries while the shipped default is the whole of its
# policy. A Cohort's own revision starts at 1 with its first override.
DEFAULT_REVISION: int = 0

# The causes a history row is allowed to name. A threshold movement carries the
# run keys that tripped it; a reset carries nothing, having no evidence behind
# it beyond the user asking.
THRESHOLD_CAUSE: str = "failure_threshold"
RESET_CAUSE: str = "reset"


def shipped_default() -> dict[str, Any]:
    """Return the policy every Cohort has until something moves it."""

    return {
        "revision": DEFAULT_REVISION,
        "starting_rung": DEFAULT_STARTING_RUNG,
        "floor": DEFAULT_FLOOR,
        "ceiling": DEFAULT_CEILING,
        "failure_threshold": dict(DEFAULT_FAILURE_THRESHOLD),
        "exploration": dict(DEFAULT_EXPLORATION),
    }


def _rung_error(rung: Any) -> str | None:
    """Return why a value is not a concrete Rung, or None where it is one.

    The portable scale itself belongs to the routing contract, so a level is
    checked for being a non-empty string here and for being on the scale where
    the frozen snapshot is validated. One scale written down twice is two
    scales the day either one moves.
    """

    if not isinstance(rung, dict) or set(rung) != {"model", "portable_deliberation"}:
        return "a Rung is exactly a model and a portable deliberation level"
    if any(
        not isinstance(rung[field], str) or not rung[field]
        for field in ("model", "portable_deliberation")
    ):
        return "a Rung's model and portable deliberation are non-empty strings"
    return None


def _entry_is_usable(entry: Any) -> bool:
    """Recognize one stored Cohort override this module can still read.

    A hand-damaged or half-written override is not a reason to refuse a route
    the shipped default answers perfectly well, so an unusable entry is dropped
    rather than raised. The history keeps what happened either way.
    """

    if not isinstance(entry, dict):
        return False
    revision = entry.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        return False
    return _rung_error(entry.get("starting_rung")) is None


def read_policy(directory: Path) -> dict[str, Any]:
    """Read the user layer, answering an absent or damaged file as no override."""

    # Treat every unreadable shape as an empty layer: the shipped default is a
    # complete policy, so nothing here can make routing fail for lack of one.
    try:
        stored = json.loads((directory / POLICY_FILE).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError):
        return {"schema_version": SCHEMA_VERSION, "cohorts": {}}
    cohorts = stored.get("cohorts") if isinstance(stored, dict) else None
    if not isinstance(cohorts, dict):
        return {"schema_version": SCHEMA_VERSION, "cohorts": {}}
    return {
        "schema_version": SCHEMA_VERSION,
        "cohorts": {
            cohort: entry
            for cohort, entry in sorted(cohorts.items())
            if isinstance(cohort, str) and cohort and _entry_is_usable(entry)
        },
    }


def effective_policy(directory: Path, cohort: str | None) -> dict[str, Any]:
    """Return the policy one Cohort routes under, override or shipped default.

    A request naming no Cohort routes under the shipped default and can never
    receive an override, so `None` resolves to exactly what an unmoved Cohort
    resolves to.
    """

    default = shipped_default()
    if cohort is None:
        return default
    entry = read_policy(directory)["cohorts"].get(cohort)
    return default if entry is None else default | dict(entry)


def frozen_policy(directory: Path) -> dict[str, Any]:
    """Project the whole store into the block a routing snapshot freezes.

    Every Cohort with an override travels, not only the ones this artifact's
    requests happen to name: the projection is the store's own state, so the
    snapshot identity moves when the policy moves and never because a batch
    was composed differently.
    """

    return {
        "schema_version": SCHEMA_VERSION,
        "default": shipped_default(),
        "cohorts": {
            cohort: shipped_default() | dict(entry)
            for cohort, entry in read_policy(directory)["cohorts"].items()
        },
    }


def history(directory: Path) -> list[dict[str, Any]]:
    """Read the append-only movement history in the order it was written."""

    try:
        content = (directory / HISTORY_FILE).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []
    rows: list[dict[str, Any]] = []
    for line in content.splitlines():
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict):
            rows.append(row)
    return rows


def _write_policy(directory: Path, cohorts: dict[str, Any]) -> None:
    """Replace the user layer atomically, or remove it once nothing overrides."""

    directory.mkdir(parents=True, exist_ok=True)
    path = directory / POLICY_FILE
    if not cohorts:
        path.unlink(missing_ok=True)
        return
    document = {
        "schema_version": SCHEMA_VERSION,
        "cohorts": {cohort: cohorts[cohort] for cohort in sorted(cohorts)},
    }
    temporary = path.with_name(f"{POLICY_FILE}.writing")
    temporary.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _append_history(directory: Path, row: dict[str, Any]) -> None:
    """Append one movement to the history without rewriting what came before."""

    directory.mkdir(parents=True, exist_ok=True)
    with (directory / HISTORY_FILE).open("a", encoding="utf-8") as rows:
        rows.write(json.dumps(row, sort_keys=True) + "\n")


def _row(
    cohort: str,
    previous: dict[str, Any],
    starting_rung: Any,
    revision: int,
    cause: dict[str, Any],
) -> dict[str, Any]:
    """Build the one history shape every movement is written in."""

    return {
        "effective_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "workload_cohort": cohort,
        "from": previous["starting_rung"],
        "to": starting_rung,
        "revision_before": previous["revision"],
        "revision_after": revision,
        "cause": cause,
    }


def move_starting_rung(
    directory: Path,
    cohort: str,
    rung: dict[str, Any],
    cause: dict[str, Any],
) -> dict[str, Any]:
    """Move one Cohort's starting Rung and record what moved it.

    This is the only write a threshold trip makes. The Rung is stored exactly
    as it was measured; whether it is still reachable is a question the route
    module answers per request, because the answer changes with the profile,
    the Harness, and the request's own locks.

    Raises:
        ValueError: the Cohort is not a name, the Rung is not a Rung, or the
            cause does not name the run keys that established it.
    """

    if not isinstance(cohort, str) or not cohort:
        raise ValueError("a Cohort override is keyed by a non-empty cohort name")
    if error := _rung_error(rung):
        raise ValueError(error)
    if cause.get("kind") != THRESHOLD_CAUSE or not cause.get("run_keys"):
        raise ValueError("a threshold movement names the run keys that tripped it")

    # Raise the Cohort's own revision, which is what the audit block reports.
    previous = effective_policy(directory, cohort)
    stored = read_policy(directory)["cohorts"]
    revision = int(previous["revision"]) + 1
    entry = {"revision": revision, "starting_rung": dict(rung)}
    _write_policy(directory, stored | {cohort: entry})
    _append_history(directory, _row(cohort, previous, dict(rung), revision, cause))
    return shipped_default() | entry


def reset(directory: Path, cohort: str | None = None) -> list[str]:
    """Restore the shipped default for one Cohort, or for every overridden one.

    Returns the Cohorts actually removed, in order, each of which received its
    own history row. Resetting a Cohort that never moved changes nothing and
    writes nothing, there being no movement to record.
    """

    stored = read_policy(directory)["cohorts"]
    if cohort is None:
        removed = sorted(stored)
    else:
        removed = [cohort] if cohort in stored else []
    if not removed:
        return []

    # Write the remaining overrides once, then one row per Cohort restored.
    remaining = {name: entry for name, entry in stored.items() if name not in removed}
    _write_policy(directory, remaining)
    for name in removed:
        previous = shipped_default() | dict(stored[name])
        _append_history(
            directory,
            _row(
                name,
                previous,
                DEFAULT_STARTING_RUNG,
                DEFAULT_REVISION,
                {"kind": RESET_CAUSE},
            ),
        )
    return removed


def _refusal(code: str, detail: str) -> dict[str, Any]:
    """Return the one machine-readable shape a refused invocation takes."""

    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "policy",
        "refusal": {"code": code, "detail": detail},
    }


def _option(rest: list[str], name: str) -> str | None:
    """Return the sole option's value in either spelling, or None where it is not one."""

    if len(rest) == 1 and rest[0].startswith(f"{name}="):
        return rest[0].split("=", 1)[1]
    if len(rest) == 2 and rest[0] == name:
        return rest[1]
    return None


def _data_directory(flags: list[str]) -> Path | None:
    """Resolve the selected data directory, or None where the flags are not ours."""

    if not flags:
        return Path.home() / ".kntnt" / "model-selector"
    value = _option(flags, "--data")
    return None if value is None else Path(value).expanduser()


def _split(arguments: list[str]) -> tuple[list[str], list[str]]:
    """Separate operands from options whichever order the caller wrote them in.

    The Skills write the flags before the operands (ADR-0097) while this parser
    reads its Cohort first, and the engines stay permissive about a spelling of
    their own (ADR-0096), so both orders are normalised here.
    """

    operands: list[str] = []
    options: list[str] = []
    index = 0
    while index < len(arguments):
        token = arguments[index]
        index += 1
        if not token.startswith("--"):
            operands.append(token)
            continue

        # A separated value belongs to the flag before it and travels with it.
        options.append(token)
        if "=" not in token and token != "--yes" and index < len(arguments):
            options.append(arguments[index])
            index += 1
    return operands, options


def _show(directory: Path, cohort: str | None) -> dict[str, Any]:
    """Render the effective policy and the movements behind it."""

    rows = history(directory)
    if cohort is not None:
        return {
            "schema_version": SCHEMA_VERSION,
            "verb": "policy",
            "action": "show",
            "data": str(directory),
            "workload_cohort": cohort,
            "effective": effective_policy(directory, cohort),
            "history": [row for row in rows if row.get("workload_cohort") == cohort],
        }
    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "policy",
        "action": "show",
        "data": str(directory),
        "workload_cohort": None,
        "default": shipped_default(),
        "cohorts": frozen_policy(directory)["cohorts"],
        "history": rows,
    }


def _policy_command(arguments: list[str]) -> tuple[dict[str, Any], int]:
    """Run one read or one reset of the store and report what it found or did."""

    # Read the action, then the optional Cohort operand, then the flags.
    if not arguments or arguments[0] not in {"show", "reset"}:
        return _refusal(
            "invalid_arguments",
            "Use policy show [<cohort>] or policy reset [<cohort>].",
        ), 2
    action, *rest = arguments
    operands, options = _split(rest)
    confirmed = "--yes" in options
    options = [option for option in options if option != "--yes"]
    if len(operands) > 1:
        return _refusal("invalid_arguments", "At most one Cohort is addressed."), 2
    directory = _data_directory(options)
    if directory is None:
        return _refusal("invalid_arguments", "Unsupported options."), 2
    cohort = operands[0] if operands else None

    if action == "show":
        return _show(directory, cohort), 0

    # Refuse an unconfirmed reset rather than performing a destructive act the
    # caller has not stated it wants.
    if not confirmed:
        return _refusal(
            "unconfirmed_reset",
            "A reset restores the shipped default; re-run it with --yes.",
        ), 2
    removed = reset(directory, cohort)
    return {
        "schema_version": SCHEMA_VERSION,
        "verb": "policy",
        "action": "reset",
        "data": str(directory),
        "workload_cohort": cohort,
        "reset": removed,
    }, 0


def main(argv: list[str] | None = None) -> int:
    """Route one command to its seam and emit only machine-readable JSON."""

    arguments = sys.argv[1:] if argv is None else argv
    if not arguments or arguments[0] != "policy":
        response: dict[str, Any] = _refusal(
            "invalid_arguments",
            "Use policy show [<cohort>] or policy reset [<cohort>].",
        )
        status = 2
    else:
        response, status = _policy_command(arguments[1:])
    print(json.dumps(response, sort_keys=True, separators=(",", ":")))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
