# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Persist and recover one dispatch run without owning dispatch policy."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import sys
import tempfile
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Final, NamedTuple, TypedDict, cast

type JsonValue = None | bool | int | str | list[JsonValue] | dict[str, JsonValue]

SCHEMA: Final[str] = "kntnt.dispatch-journal/v1"
ARCHIVE_PENDING_NAME: Final[str] = ".archive-pending"
ARCHIVE_RECEIPT_NAME: Final[str] = "receipt.json"
SAFE_INTEGER_LIMIT: Final[int] = 9_007_199_254_740_991
OPENING_KEYS: Final[frozenset[str]] = frozenset(
    {
        "repository",
        "integration_ref",
        "opening_head",
        "invocation",
        "instruction",
        "selection",
        "at_once",
        "route",
    }
)


class EventType(StrEnum):
    """Name every durable boundary without deciding workflow policy."""

    SELECTION_RECORDED = "selection-recorded"
    BUNDLE_CONSUMED = "bundle-consumed"
    BUNDLE_RELEASED = "bundle-released"
    ROUTE_RECORDED = "route-recorded"
    TICKET_ASSIGNED = "ticket-assigned"
    ATTEMPT_STARTED = "attempt-started"
    ATTEMPT_RETURNED = "attempt-returned"
    PATCH_CAPTURED = "patch-captured"
    DISPATCHER_WRITE_RECORDED = "dispatcher-write-recorded"
    REVIEW_COMPLETED = "review-completed"
    REVISE_REQUESTED = "revise-requested"
    EXECUTOR_REHYDRATED = "executor-rehydrated"
    REBUILD_REQUESTED = "rebuild-requested"
    OWNER_ANSWERED = "owner-answered"
    LANDING_STARTED = "landing-started"
    HUMAN_CONFLICT = "human-conflict"
    LANDED = "landed"
    PARKED = "parked"
    STRANDED = "stranded"
    TRACKER_TRANSITION_PLANNED = "tracker-transition-planned"
    TRACKER_TRANSITION_COMPLETED = "tracker-transition-completed"
    BUNDLE_RETIRED = "bundle-retired"
    RESOURCE_CLEANED = "resource-cleaned"
    OBSERVATION_RECORDED = "observation-recorded"
    RUN_COMPLETED = "run-completed"


class TransitionId(StrEnum):
    """Identify one already resolved portable tracker mutation."""

    LAND = "T-LAND"
    PARK_INFO = "T-PARK-INFO"
    PARK_HUMAN = "T-PARK-HUMAN"


class TerminalState(StrEnum):
    """Represent the three terminal ticket projections."""

    LANDED = "landed"
    PARKED = "parked"
    STRANDED = "stranded"


class RecoveryAction(StrEnum):
    """Represent the next crash-safe persistence boundary."""

    START_TICKET = "start-ticket"
    CONTINUE_TICKET = "continue-ticket"
    REPLAY_ATTEMPT = "replay-attempt"
    REVIEW_PATCH = "review-patch"
    RESUME_REVISION = "resume-revision"
    AWAIT_RECOMPILE = "await-recompile"
    RECONCILE_LANDING = "reconcile-landing"
    RESUME_HUMAN_CONFLICT = "resume-human-conflict"
    COMPLETE_TRACKER_TRANSITION = "complete-tracker-transition"
    RETIRE_BUNDLE = "retire-bundle"
    RELEASE_BUNDLE = "release-bundle"
    CLEAN_RESOURCES = "clean-resources"
    CLEAN_STRANDED = "clean-stranded"
    COMPLETE_RUN = "complete-run"
    ARCHIVE_RUN = "archive-run"
    COMPLETE = "complete"


class ContinuationMode(StrEnum):
    """Distinguish live revision continuation from R3 rehydration."""

    LIVE = "live-context"
    FRESH = "fresh-context"


class TerminalRequirements(NamedTuple):
    """Describe the durable prerequisites for one terminal state."""

    requires_tracker_completion: bool
    bundle_boundary: EventType
    bundle_action: RecoveryAction
    cleanup_action: RecoveryAction


class GitEvidence(TypedDict):
    """Carry observations for one exact ticket landing window."""

    ticket: str
    landing_sequence: int
    integration_ref_head: str
    candidate_commit: str
    candidate_reachable: bool
    candidate_tree: str
    test_blobs: dict[str, str]
    expected_trailers: dict[str, str]
    observed_trailers: dict[str, str]


# Publish typed vocabulary sets and self-describing lexical validators for
# callers and focused schema tests.
EVENT_TYPES: Final[frozenset[EventType]] = frozenset(EventType)
TRANSITION_IDS: Final[frozenset[TransitionId]] = frozenset(TransitionId)
TERMINAL_TYPES: Final[frozenset[TerminalState]] = frozenset(TerminalState)
TERMINAL_REQUIREMENTS: Final[dict[TerminalState, TerminalRequirements]] = {
    TerminalState.LANDED: TerminalRequirements(
        requires_tracker_completion=True,
        bundle_boundary=EventType.BUNDLE_RETIRED,
        bundle_action=RecoveryAction.RETIRE_BUNDLE,
        cleanup_action=RecoveryAction.CLEAN_RESOURCES,
    ),
    TerminalState.PARKED: TerminalRequirements(
        requires_tracker_completion=True,
        bundle_boundary=EventType.BUNDLE_RETIRED,
        bundle_action=RecoveryAction.RETIRE_BUNDLE,
        cleanup_action=RecoveryAction.CLEAN_RESOURCES,
    ),
    TerminalState.STRANDED: TerminalRequirements(
        requires_tracker_completion=False,
        bundle_boundary=EventType.BUNDLE_RELEASED,
        bundle_action=RecoveryAction.RELEASE_BUNDLE,
        cleanup_action=RecoveryAction.CLEAN_STRANDED,
    ),
}
ARTIFACT_KIND_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[a-z][a-z0-9-]*$")
TICKET_REFERENCE_PATTERN: Final[re.Pattern[str]] = re.compile(r"^#[1-9][0-9]*$")
OBJECT_ID_PATTERN: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{40,64}$")
CONTENT_DIGEST_PATTERN: Final[re.Pattern[str]] = re.compile(r"^sha256:[0-9a-f]{64}$")
COMPILED_BLOB_PATTERN: Final[re.Pattern[str]] = re.compile(r"^git:[0-9a-f]{40,64}$")
UTC_INSTANT_PATTERN: Final[re.Pattern[str]] = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$"
)

# Define the exact recovery payload surface for every durable event type.
EVENT_PAYLOAD_FIELDS: Final[dict[EventType, frozenset[str]]] = {
    EventType.SELECTION_RECORDED: frozenset({"tickets"}),
    EventType.BUNDLE_CONSUMED: frozenset(
        {
            "bundle_fingerprint",
            "execution_base",
            "source_fingerprints",
            "footprint",
            "allocations",
            "tests",
            "command_ids",
            "done_criterion_ids",
        }
    ),
    EventType.BUNDLE_RELEASED: frozenset({"bundle_fingerprint", "reason"}),
    EventType.ROUTE_RECORDED: frozenset({"attempt", "decision"}),
    EventType.TICKET_ASSIGNED: frozenset({"assignee"}),
    EventType.ATTEMPT_STARTED: frozenset(
        {"attempt", "attempt_id", "base", "worktree", "branch"}
    ),
    EventType.ATTEMPT_RETURNED: frozenset({"attempt"}),
    EventType.PATCH_CAPTURED: frozenset({"attempt", "changed_paths"}),
    EventType.DISPATCHER_WRITE_RECORDED: frozenset({"paths"}),
    EventType.REVIEW_COMPLETED: frozenset({"attempt", "verdict", "finding_summary"}),
    EventType.REVISE_REQUESTED: frozenset(
        {"attempt", "prior_attempt", "review_sequence"}
    ),
    EventType.EXECUTOR_REHYDRATED: frozenset(
        {"attempt", "revision_sequence", "route_sequence"}
    ),
    EventType.REBUILD_REQUESTED: frozenset(
        {"review_sequence", "head", "compile_invocation", "resume_invocation"}
    ),
    EventType.OWNER_ANSWERED: frozenset({"for_sequence", "answer"}),
    EventType.LANDING_STARTED: frozenset(
        {
            "review_sequence",
            "previous_head",
            "candidate",
            "tree",
            "test_blobs",
        }
    ),
    EventType.HUMAN_CONFLICT: frozenset(
        {"landing_sequence", "attempt", "branch", "worktree"}
    ),
    EventType.LANDED: frozenset(
        {"landing_sequence", "commit", "tree", "bundle_fingerprint", "test_blobs"}
    ),
    EventType.PARKED: frozenset({"park_class", "message", "reason", "patch_sequence"}),
    EventType.STRANDED: frozenset({"reason"}),
    EventType.TRACKER_TRANSITION_PLANNED: frozenset(
        {"transition_id", "resolution", "pre_projection"}
    ),
    EventType.TRACKER_TRANSITION_COMPLETED: frozenset(
        {
            "transition_id",
            "planned_sequence",
            "resolution",
            "observed_post_projection",
        }
    ),
    EventType.BUNDLE_RETIRED: frozenset({"bundle_fingerprint"}),
    EventType.RESOURCE_CLEANED: frozenset({"resources"}),
    EventType.OBSERVATION_RECORDED: frozenset({"attempt"}),
    EventType.RUN_COMPLETED: frozenset({"tickets"}),
}

# Bind artifact-bearing events to every byte stream recovery needs durable.
EVENT_ARTIFACT_FIELDS: Final[dict[EventType, frozenset[str]]] = {
    event_type: frozenset() for event_type in EventType
}
EVENT_ARTIFACT_FIELDS.update(
    {
        EventType.BUNDLE_CONSUMED: frozenset(
            {"bundle-plan", "bundle-manifest", "bundle-tests"}
        ),
        EventType.ROUTE_RECORDED: frozenset({"route-response"}),
        EventType.PATCH_CAPTURED: frozenset({"patch"}),
        EventType.DISPATCHER_WRITE_RECORDED: frozenset({"dispatcher-write-proposal"}),
        EventType.REVIEW_COMPLETED: frozenset({"review-finding"}),
        EventType.OBSERVATION_RECORDED: frozenset({"observation-input"}),
    }
)


class JournalRefusal(RuntimeError):
    """Report durable state that cannot be interpreted without guessing."""


def sha256_hex(content: bytes) -> str:
    """Return the lowercase SHA-256 digest for exact bytes."""

    return hashlib.sha256(content).hexdigest()


def canonical_json(value: Any) -> bytes:
    """Serialize the no-float manifest domain with RFC 8785 property order.

    Raises:
        JournalRefusal: The value falls outside the shared JSON domain.
    """

    # Validate before serialization so Python-specific values never leak into
    # an event whose bytes another implementation must reproduce.
    normalized = _normalize_json(value, "$", set())
    return _encode_json(normalized).encode("utf-8")


def run_fingerprint(opening: Mapping[str, Any]) -> str:
    """Fingerprint every immutable input that defines one dispatch run."""

    normalized = _validate_opening(opening)
    return f"sha256:{sha256_hex(canonical_json(normalized))}"


def _normalize_json(value: Any, path: str, ancestors: set[int]) -> JsonValue:
    """Copy one value into the bounded canonical JSON domain."""

    # Keep booleans ahead of integers because bool is an int subclass.
    if value is None or isinstance(value, (bool, str)):
        if isinstance(value, str):
            _validate_unicode(value, path)
        return value

    if isinstance(value, int):
        if abs(value) > SAFE_INTEGER_LIMIT:
            raise JournalRefusal(f"{path} exceeds the RFC 8785 safe integer domain")
        return value

    if isinstance(value, float):
        raise JournalRefusal(f"{path} contains a floating-point value")

    if isinstance(value, Mapping):
        # Reject cycles and non-string property names before descending.
        identity = id(value)
        if identity in ancestors:
            raise JournalRefusal(f"{path} contains a cyclic object")
        ancestors.add(identity)
        normalized: dict[str, JsonValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise JournalRefusal(f"{path} contains a non-string property name")
            _validate_unicode(key, f"{path}.<key>")
            normalized[key] = _normalize_json(item, f"{path}.{key}", ancestors)
        ancestors.remove(identity)
        return normalized

    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        # Arrays retain their order but share the same cycle guard as objects.
        identity = id(value)
        if identity in ancestors:
            raise JournalRefusal(f"{path} contains a cyclic array")
        ancestors.add(identity)
        normalized_array = [
            _normalize_json(item, f"{path}[{index}]", ancestors)
            for index, item in enumerate(value)
        ]
        ancestors.remove(identity)
        return normalized_array

    raise JournalRefusal(f"{path} contains unsupported {type(value).__name__}")


def _validate_unicode(value: str, path: str) -> None:
    """Reject lone surrogates outside the I-JSON string domain."""

    try:
        value.encode("utf-8")
    except UnicodeEncodeError as error:
        raise JournalRefusal(f"{path} contains an invalid Unicode surrogate") from error


def _encode_json(value: JsonValue) -> str:
    """Encode a previously normalized value in canonical form."""

    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    if isinstance(value, list):
        return f"[{','.join(_encode_json(item) for item in value)}]"

    # RFC 8785 orders object properties by their UTF-16 code units.
    keys = sorted(value, key=lambda key: key.encode("utf-16be"))
    members = (f"{_encode_json(key)}:{_encode_json(value[key])}" for key in keys)
    return f"{{{','.join(members)}}}"


def _validate_opening(opening: Mapping[str, Any]) -> dict[str, JsonValue]:
    """Validate and normalize all inputs covered by a run fingerprint."""

    # Refuse omissions and extensions so a fingerprint never hides an input.
    if set(opening) != OPENING_KEYS:
        missing = sorted(OPENING_KEYS - set(opening))
        extra = sorted(set(opening) - OPENING_KEYS)
        raise JournalRefusal(f"opening keys differ; missing={missing}, extra={extra}")

    # Validate identities and exact invocation fields at the trust boundary.
    for key in ("repository", "invocation", "instruction"):
        if not isinstance(opening[key], str) or not opening[key]:
            raise JournalRefusal(f"opening {key} must be a non-empty string")
    if not isinstance(opening["integration_ref"], str) or not opening[
        "integration_ref"
    ].startswith("refs/"):
        raise JournalRefusal("opening integration_ref must be a full ref")
    if not isinstance(opening["opening_head"], str) or not OBJECT_ID_PATTERN.fullmatch(
        opening["opening_head"]
    ):
        raise JournalRefusal("opening opening_head must be a full lowercase object ID")

    # Keep selection and concurrency mechanically unambiguous.
    selection = opening["selection"]
    if not isinstance(selection, list) or not selection:
        raise JournalRefusal("opening selection must be a non-empty ordered array")
    if any(
        not isinstance(ticket, str) or not TICKET_REFERENCE_PATTERN.fullmatch(ticket)
        for ticket in selection
    ):
        raise JournalRefusal("opening selection contains an invalid ticket reference")
    if len(set(selection)) != len(selection):
        raise JournalRefusal("opening selection contains a duplicate ticket")
    if (
        not isinstance(opening["at_once"], int)
        or isinstance(opening["at_once"], bool)
        or opening["at_once"] < 1
    ):
        raise JournalRefusal("opening at_once must be a positive integer")

    # Both route fields remain explicit even when the caller leaves one open.
    route = opening["route"]
    if not isinstance(route, Mapping) or set(route) != {"model", "deliberation"}:
        raise JournalRefusal("opening route must contain model and deliberation")
    if any(
        value is not None and not isinstance(value, str) for value in route.values()
    ):
        raise JournalRefusal("opening route overrides must be strings or null")

    return cast(dict[str, JsonValue], _normalize_json(dict(opening), "$", set()))


def _validate_instant(value: str, field: str) -> None:
    """Require one normalized UTC instant suitable for metadata and events."""

    if not UTC_INSTANT_PATTERN.fullmatch(value):
        raise JournalRefusal(f"{field} must be an RFC 3339 UTC instant")
    try:
        datetime.fromisoformat(value)
    except ValueError as error:
        raise JournalRefusal(f"{field} is not a real UTC instant") from error


def _now() -> str:
    """Return a second-precision UTC instant for a durable boundary."""

    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _flush_directory(directory: Path) -> None:
    """Flush a directory entry after an atomic filesystem transition."""

    descriptor = os.open(directory, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _ensure_directory(directory: Path) -> None:
    """Create and flush each missing directory entry in path order."""

    missing: list[Path] = []
    cursor = directory
    while not cursor.exists():
        missing.append(cursor)
        cursor = cursor.parent

    # Each new name becomes durable before a child can depend on it.
    for path in reversed(missing):
        path.mkdir()
        _flush_directory(path.parent)


def _atomic_publish(path: Path, content: bytes) -> None:
    """Publish complete bytes through a flushed temporary sibling."""

    # A sibling keeps rename on one filesystem and a distinctive prefix makes
    # an interrupted unpublished file safe to identify as temporary.
    _ensure_directory(path.parent)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        # Flush the complete file before its name becomes authoritative.
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        _flush_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _publish_or_verify(path: Path, content: bytes) -> None:
    """Publish once, or verify an identical crash residue without rewriting it."""

    if path.exists():
        if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
            raise JournalRefusal(f"immutable publication conflicts at {path.name}")
        return
    _atomic_publish(path, content)


@contextmanager
def _exclusive_lock(path: Path) -> Iterator[None]:
    """Serialize writers within one branch-scoped active slot."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class Journal:
    """Hide atomic journal persistence behind four public operations."""

    def __init__(
        self,
        root: Path,
        path: Path,
        metadata: dict[str, JsonValue],
        *,
        archive_pending: bool = False,
    ) -> None:
        """Bind an already published active slot to its immutable metadata."""

        self.root = root
        self.path = path
        self.metadata = metadata
        self.archive_pending = archive_pending

    @classmethod
    def open(
        cls,
        root: Path,
        opening: Mapping[str, Any],
        *,
        opened_at: str | None = None,
    ) -> Journal:
        """Create or resume the active slot selected by the full ref.

        Raises:
            JournalRefusal: Existing state or opening inputs are ambiguous.
        """

        # Normalize every fingerprint input before consulting persistent state.
        normalized = _validate_opening(opening)
        fingerprint = run_fingerprint(opening)
        ref = cast(str, normalized["integration_ref"])
        slot = root / "active" / sha256_hex(ref.encode("utf-8"))
        root.mkdir(parents=True, exist_ok=True)
        (root / "active").mkdir(exist_ok=True)
        (root / "archive").mkdir(exist_ok=True)

        # A published slot wins; only an exact opening may resume it.
        if slot.exists():
            journal = cls._load(root, slot)
            if journal.metadata["run_fingerprint"] != fingerprint:
                raise JournalRefusal(
                    "active run opening does not match this invocation"
                )
            journal.validate()
            return journal

        # A crash after the atomic archive move resumes cleanup from the
        # uniquely marked archive instead of opening a second branch run.
        pending = cls._find_pending_archive(root, fingerprint)
        if pending is not None:
            journal = cls._load(root, pending, archive_pending=True)
            journal._validate_pending_archive()
            return journal

        instant = opened_at or _now()
        _validate_instant(instant, "opened_at")
        metadata = {
            "schema": SCHEMA,
            "opened_at": instant,
            **normalized,
            "run_fingerprint": fingerprint,
        }

        # Assemble metadata out of sight, then claim the branch slot atomically.
        temporary = Path(tempfile.mkdtemp(prefix=f".{slot.name}.", dir=slot.parent))
        try:
            (temporary / "events").mkdir()
            (temporary / "artifacts").mkdir()
            _atomic_publish(temporary / "metadata.json", canonical_json(metadata))
            _flush_directory(temporary)
            try:
                temporary.rename(slot)
            except FileExistsError:
                journal = cls._load(root, slot)
                if journal.metadata["run_fingerprint"] != fingerprint:
                    raise JournalRefusal(
                        "active run opening does not match this invocation"
                    )
                journal.validate()
                return journal
            _flush_directory(slot.parent)
        finally:
            if temporary.exists():
                for child in sorted(temporary.rglob("*"), reverse=True):
                    child.rmdir() if child.is_dir() else child.unlink()
                temporary.rmdir()

        return cls(root, slot, metadata)

    @classmethod
    def _load(cls, root: Path, slot: Path, *, archive_pending: bool = False) -> Journal:
        """Load immutable metadata without accepting non-canonical bytes."""

        metadata_path = slot / "metadata.json"
        if metadata_path.is_symlink() or not metadata_path.is_file():
            raise JournalRefusal("active run metadata is missing or not a regular file")
        try:
            content = metadata_path.read_bytes()
            value = json.loads(content)
        except (OSError, json.JSONDecodeError) as error:
            raise JournalRefusal(
                "active run metadata is missing or malformed"
            ) from error
        if canonical_json(value) != content:
            raise JournalRefusal("active run metadata is not canonical JSON")
        if not isinstance(value, dict):
            raise JournalRefusal("active run metadata is not an object")
        return cls(
            root,
            slot,
            cast(dict[str, JsonValue], value),
            archive_pending=archive_pending,
        )

    @classmethod
    def _find_pending_archive(cls, root: Path, fingerprint: str) -> Path | None:
        """Resolve the one incomplete archive for an exact run fingerprint."""

        candidates: list[Path] = []
        for marker in (root / "archive").glob(f"*/{ARCHIVE_PENDING_NAME}"):
            try:
                value = json.loads(marker.read_bytes())
            except (OSError, json.JSONDecodeError) as error:
                raise JournalRefusal("archive pending marker is malformed") from error
            if isinstance(value, dict) and value.get("run_fingerprint") == fingerprint:
                candidates.append(marker.parent)
        if len(candidates) > 1:
            raise JournalRefusal("multiple pending archives match this invocation")
        return candidates[0] if candidates else None

    def record(
        self,
        event_type: str,
        *,
        ticket: str | None = None,
        payload: Mapping[str, Any] | None = None,
        artifacts: Mapping[str, bytes] | None = None,
        recorded_at: str | None = None,
    ) -> dict[str, JsonValue]:
        """Durably store artifacts, then append their immutable event.

        Raises:
            JournalRefusal: Existing state or the proposed event is invalid.
        """

        # Reject invalid event inputs before any artifact can become orphaned.
        try:
            typed_event = EventType(event_type)
        except ValueError as error:
            raise JournalRefusal(f"unknown event type: {event_type}") from error
        if ticket is not None and not TICKET_REFERENCE_PATTERN.fullmatch(ticket):
            raise JournalRefusal(f"invalid ticket reference: {ticket}")
        selection = cast(list[str], self.metadata["selection"])
        if ticket is not None and ticket not in selection:
            raise JournalRefusal(f"event names unselected ticket {ticket}")
        normalized_payload = cast(
            dict[str, JsonValue],
            _normalize_json(dict(payload or {}), "$.payload", set()),
        )
        instant = recorded_at or _now()
        _validate_instant(instant, "recorded_at")

        with _exclusive_lock(self.path / ".write.lock"):
            # Validate the complete prefix before deriving its next sequence.
            state = self._read_validated()
            prior_events = state["events"]
            _validate_event_payload(
                typed_event,
                ticket,
                normalized_payload,
                set(artifacts or {}),
                prior_events,
            )
            if (
                typed_event is EventType.SELECTION_RECORDED
                and normalized_payload.get("tickets") != selection
            ):
                raise JournalRefusal("selection event contradicts opening metadata")
            if typed_event is EventType.RUN_COMPLETED:
                completed_tickets = normalized_payload.get("tickets")
                if not isinstance(completed_tickets, dict) or set(
                    completed_tickets
                ) != set(selection):
                    raise JournalRefusal("run completion omits selected tickets")
            sequence = len(prior_events) + 1

            # Artifacts become durable before an event is allowed to name them.
            references = {
                kind: self._store_artifact(kind, content)
                for kind, content in (artifacts or {}).items()
            }
            previous_bytes = (
                (self.path / "metadata.json").read_bytes()
                if not prior_events
                else cast(bytes, state["event_bytes"][-1])
            )
            event: dict[str, JsonValue] = {
                "schema": SCHEMA,
                "sequence": sequence,
                "type": typed_event.value,
                "recorded_at": instant,
                "previous_sha256": f"sha256:{sha256_hex(previous_bytes)}",
                "ticket": ticket,
                "payload": normalized_payload,
                "artifacts": cast(dict[str, JsonValue], references),
            }

            # The write lock makes the absence check and rename one publication.
            path = self.path / "events" / f"{sequence:08d}.json"
            if path.exists():
                raise JournalRefusal(f"immutable event already exists: {path.name}")
            _atomic_publish(path, canonical_json(event))
            return event

    def validate(self) -> dict[str, JsonValue]:
        """Validate all identities and return a compact durable-state count."""

        state = self._read_validated()
        references = {
            cast(str, reference["path"])
            for event in cast(list[dict[str, JsonValue]], state["events"])
            for reference in cast(
                dict[str, dict[str, JsonValue]], event["artifacts"]
            ).values()
        }
        return {
            "event_count": len(cast(list[JsonValue], state["events"])),
            "artifact_count": len(references),
            "last_event_sha256": state["last_event_sha256"],
        }

    def project(
        self, *, git_evidence: Sequence[Mapping[str, Any]] | None = None
    ) -> dict[str, JsonValue]:
        """Project run and ticket recovery state without mutating the journal.

        Raises:
            JournalRefusal: Supplied external evidence contradicts a durable fact.
        """

        # An archive cleanup may have retired event artifacts already; its
        # compact receipt remains the authoritative resumable projection.
        if self.archive_pending:
            if git_evidence is not None:
                raise JournalRefusal(
                    "pending archive projection accepts no Git evidence"
                )
            return self._project_pending_archive()

        state = self._read_validated()
        events = cast(list[dict[str, JsonValue]], state["events"])
        tickets = {
            ticket: _empty_ticket_projection()
            for ticket in cast(list[str], self.metadata["selection"])
        }

        # Fold the immutable log into a replaceable in-memory recovery view.
        for event in events:
            ticket = cast(str | None, event["ticket"])
            if ticket is None:
                continue
            if ticket not in tickets:
                raise JournalRefusal(f"event names unselected ticket {ticket}")
            _apply_event(tickets[ticket], event)

        # Fixed Git evidence confirms one landing window without giving this
        # persistence module Git integration or branch-advance policy.
        if git_evidence is not None:
            _validate_git_evidence(events, git_evidence)

        # Run completion supersedes each ticket's cleanup action; otherwise the
        # newest durable ticket boundary determines recovery.
        completed = any(
            _event_type(event) is EventType.RUN_COMPLETED for event in events
        )
        for ticket, projection in tickets.items():
            ticket_events = [event for event in events if event["ticket"] == ticket]
            projection["recovery_action"] = (
                RecoveryAction.ARCHIVE_RUN.value
                if completed
                else _recovery_action(ticket_events)
            )

        # Completion is contradictory until every selected ticket is terminal.
        if completed and any(
            projection["terminal"]
            not in {terminal.value for terminal in TERMINAL_TYPES}
            for projection in tickets.values()
        ):
            raise JournalRefusal("run-completed precedes a selected terminal state")

        projected_tickets = cast(dict[str, JsonValue], tickets)
        return {
            "schema": SCHEMA,
            "run_fingerprint": self.metadata["run_fingerprint"],
            "event_count": len(events),
            "tickets": projected_tickets,
            "completed": completed,
        }

    def archive(self) -> Path:
        """Atomically archive a complete run and finish bounded bulk cleanup."""

        with _exclusive_lock(self.path / ".write.lock"):
            if self.archive_pending:
                self._finalize_archive()
                return self.path

            # Every ticket must cross its terminal-specific tracker and cleanup
            # boundaries before the active branch slot can disappear.
            state = self._read_validated()
            events = cast(list[dict[str, JsonValue]], state["events"])
            if not events or _event_type(events[-1]) is not EventType.RUN_COMPLETED:
                raise JournalRefusal("archive requires a final run-completed event")
            projection = self.project()
            _validate_archive_readiness(events, projection)

            # The compact receipt and pending marker are durable before the
            # single rename removes the active branch slot.
            receipt = _compact_archive_receipt(
                self.metadata, events, projection, state["last_event_sha256"]
            )
            receipt_bytes = canonical_json(receipt)
            _publish_or_verify(self.path / ARCHIVE_RECEIPT_NAME, receipt_bytes)
            marker = {
                "run_fingerprint": self.metadata["run_fingerprint"],
                "receipt_sha256": f"sha256:{sha256_hex(receipt_bytes)}",
            }
            _publish_or_verify(self.path / ARCHIVE_PENDING_NAME, canonical_json(marker))

            # Path punctuation is removed while the fingerprint remains exact.
            opened = cast(str, self.metadata["opened_at"])
            archive_name = f"{opened.replace('-', '').replace(':', '')}-{cast(str, self.metadata['run_fingerprint']).removeprefix('sha256:')}"
            archive = self.root / "archive" / archive_name
            if archive.exists():
                raise JournalRefusal("archive destination already exists")
            active_parent = self.path.parent
            os.replace(self.path, archive)
            _flush_directory(active_parent)
            _flush_directory(archive.parent)
            self.path = archive
            self.archive_pending = True
            self._finalize_archive()
            return archive

    def _finalize_archive(self) -> None:
        """Delete retired bulk while preserving the receipt-selected artifacts."""

        receipt = self._read_archive_receipt()
        self._validate_archive_authentication(receipt)
        retained_paths = _validate_retained_artifacts(self.path, receipt)

        # Artifact deletion is idempotent, so a crash resumes from the same
        # marker without reconstructing decisions from absent bulk.
        artifact_root = self.path / "artifacts"
        if artifact_root.exists():
            for path in sorted(artifact_root.rglob("*"), reverse=True):
                if (
                    path.is_file()
                    and path.relative_to(self.path).as_posix() not in retained_paths
                ):
                    path.unlink()
                    _flush_directory(path.parent)
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()
                    _flush_directory(path.parent)

        # Removing the marker is the last durable archive-completion boundary.
        marker = self.path / ARCHIVE_PENDING_NAME
        if marker.exists():
            marker.unlink()
            _flush_directory(marker.parent)
        self.archive_pending = False

    def _validate_pending_archive(self) -> None:
        """Validate cleanup receipts without requiring already deleted bulk."""

        # The pending marker authenticates the exact receipt that authorizes
        # cleanup after the active-slot rename.
        receipt = self._read_archive_receipt()
        self._validate_archive_authentication(receipt)
        _validate_retained_artifacts(self.path, receipt)

    def _validate_archive_authentication(self, receipt: dict[str, JsonValue]) -> None:
        """Bind pending cleanup to one canonical compact receipt."""

        # Read the marker independently so neither receipt can rewrite the
        # expected digest used to authorize artifact deletion.
        marker_path = self.path / ARCHIVE_PENDING_NAME
        try:
            marker_bytes = marker_path.read_bytes()
            marker = json.loads(marker_bytes)
        except (OSError, json.JSONDecodeError) as error:
            raise JournalRefusal("archive pending marker is malformed") from error
        receipt_bytes = canonical_json(receipt)
        expected_marker = {
            "run_fingerprint": self.metadata["run_fingerprint"],
            "receipt_sha256": f"sha256:{sha256_hex(receipt_bytes)}",
        }
        if canonical_json(marker) != marker_bytes or marker != expected_marker:
            raise JournalRefusal("archive pending marker is not canonical or exact")

        # Invocation identity remains explicit inside the authenticated receipt.
        if receipt.get("run_fingerprint") != self.metadata["run_fingerprint"]:
            raise JournalRefusal("archive receipt names a different invocation")

    def _read_archive_receipt(self) -> dict[str, JsonValue]:
        """Read the canonical compact receipt shared by archive operations."""

        receipt_path = self.path / ARCHIVE_RECEIPT_NAME
        try:
            receipt_bytes = receipt_path.read_bytes()
            receipt = json.loads(receipt_bytes)
        except (OSError, json.JSONDecodeError) as error:
            raise JournalRefusal("archive receipt is missing or malformed") from error
        if canonical_json(receipt) != receipt_bytes or not isinstance(receipt, dict):
            raise JournalRefusal("archive receipt is not canonical JSON")
        return cast(dict[str, JsonValue], receipt)

    def _project_pending_archive(self) -> dict[str, JsonValue]:
        """Project a moved archive solely from its compact durable receipt."""

        receipt = self._read_archive_receipt()
        receipt_tickets = receipt.get("tickets")
        event_count = receipt.get("event_count")
        if not isinstance(receipt_tickets, dict) or not isinstance(event_count, int):
            raise JournalRefusal("archive receipt projection is malformed")

        # Only terminal identity and the next archive action survive retired
        # event bulk; audit receipts remain available separately in the receipt.
        tickets: dict[str, JsonValue] = {}
        for ticket, value in receipt_tickets.items():
            if not isinstance(value, dict):
                raise JournalRefusal("archive ticket receipt is malformed")
            try:
                terminal = TerminalState(cast(str, value.get("terminal")))
            except (TypeError, ValueError) as error:
                raise JournalRefusal("archive ticket terminal is malformed") from error
            continuation_value = value.get("continuation")
            if continuation_value is not None:
                try:
                    continuation_value = ContinuationMode(
                        cast(str, continuation_value)
                    ).value
                except (TypeError, ValueError) as error:
                    raise JournalRefusal(
                        "archive ticket continuation is malformed"
                    ) from error
            tickets[ticket] = {
                "last_event": terminal.value,
                "terminal": terminal.value,
                "continuation": continuation_value,
                "receipts": {},
                "recovery_action": RecoveryAction.ARCHIVE_RUN.value,
            }

        return {
            "schema": SCHEMA,
            "run_fingerprint": self.metadata["run_fingerprint"],
            "event_count": event_count,
            "tickets": tickets,
            "completed": True,
        }

    def _store_artifact(self, kind: str, content: bytes) -> dict[str, JsonValue]:
        """Publish one content-addressed artifact and return its receipt."""

        if not ARTIFACT_KIND_PATTERN.fullmatch(kind):
            raise JournalRefusal(f"invalid artifact kind: {kind}")
        if not isinstance(content, bytes):
            raise JournalRefusal(f"artifact {kind} must be exact bytes")
        digest = sha256_hex(content)
        relative = Path("artifacts") / kind / digest
        path = self.path / relative

        # Reuse only an identical artifact left by an interrupted event append.
        if path.exists():
            if path.is_symlink() or not path.is_file() or path.read_bytes() != content:
                raise JournalRefusal(
                    f"artifact digest collision at {relative.as_posix()}"
                )
        else:
            _atomic_publish(path, content)
        return {
            "path": relative.as_posix(),
            "sha256": f"sha256:{digest}",
            "byte_length": len(content),
        }

    def _read_validated(self) -> dict[str, Any]:
        """Read and validate the metadata, chain, schemas, and artifacts."""

        # Re-read metadata so an on-disk mutation cannot hide behind this
        # object.
        metadata_bytes = (self.path / "metadata.json").read_bytes()
        try:
            metadata = json.loads(metadata_bytes)
        except json.JSONDecodeError as error:
            raise JournalRefusal("metadata is malformed JSON") from error
        if canonical_json(metadata) != metadata_bytes or metadata != self.metadata:
            raise JournalRefusal("immutable opening metadata changed")
        metadata_keys = OPENING_KEYS | {"schema", "opened_at", "run_fingerprint"}
        if set(metadata) != metadata_keys:
            raise JournalRefusal("immutable opening metadata fields are incomplete")
        opening = {key: metadata[key] for key in OPENING_KEYS}
        if metadata.get("schema") != SCHEMA or metadata.get(
            "run_fingerprint"
        ) != run_fingerprint(opening):
            raise JournalRefusal("opening metadata fingerprint is invalid")
        _validate_instant(cast(str, metadata.get("opened_at")), "opened_at")

        # Temporary siblings are invisible; authoritative event names must form
        # one exact sequence with no gaps or alternate files.
        event_directory = self.path / "events"
        if event_directory.is_symlink() or not event_directory.is_dir():
            raise JournalRefusal("event directory is missing or not a directory")
        paths = sorted(
            path for path in event_directory.iterdir() if not path.name.startswith(".")
        )
        expected_names = [
            f"{sequence:08d}.json" for sequence in range(1, len(paths) + 1)
        ]
        if [path.name for path in paths] != expected_names:
            raise JournalRefusal(
                "event sequence is non-contiguous or contains an invalid name"
            )

        events: list[dict[str, JsonValue]] = []
        event_bytes: list[bytes] = []
        previous = metadata_bytes
        for sequence, path in enumerate(paths, start=1):
            # Canonical bytes and the predecessor digest jointly make mutation
            # or reordering visible before projection begins.
            if path.is_symlink() or not path.is_file():
                raise JournalRefusal(f"event {path.name} is not a regular file")
            content = path.read_bytes()
            try:
                value = json.loads(content)
            except json.JSONDecodeError as error:
                raise JournalRefusal(f"event {path.name} is malformed JSON") from error
            if canonical_json(value) != content or not isinstance(value, dict):
                raise JournalRefusal(f"event {path.name} is not canonical JSON")
            event = cast(dict[str, JsonValue], value)
            _validate_event_envelope(event, sequence, previous, events)
            if _event_type(event) is EventType.SELECTION_RECORDED:
                payload = cast(dict[str, JsonValue], event["payload"])
                if payload.get("tickets") != metadata["selection"]:
                    raise JournalRefusal("selection event contradicts opening metadata")
            if _event_type(event) is EventType.RUN_COMPLETED:
                payload = cast(dict[str, JsonValue], event["payload"])
                completed = payload.get("tickets")
                selection = cast(list[str], metadata["selection"])
                if not isinstance(completed, dict) or set(completed) != set(selection):
                    raise JournalRefusal("run completion omits selected tickets")
            self._validate_artifacts(event)
            events.append(event)
            event_bytes.append(content)
            previous = content

        return {
            "events": events,
            "event_bytes": event_bytes,
            "last_event_sha256": f"sha256:{sha256_hex(previous)}",
        }

    def _validate_artifacts(self, event: dict[str, JsonValue]) -> None:
        """Verify every referenced artifact remains exact and contained."""

        artifacts = event.get("artifacts")
        if not isinstance(artifacts, dict):
            raise JournalRefusal("event artifacts must be an object")
        for kind, value in artifacts.items():
            if not ARTIFACT_KIND_PATTERN.fullmatch(kind) or not isinstance(value, dict):
                raise JournalRefusal("event contains an invalid artifact reference")
            if set(value) != {"path", "sha256", "byte_length"}:
                raise JournalRefusal("artifact reference fields are incomplete")
            relative = value["path"]
            digest = value["sha256"]
            length = value["byte_length"]
            if (
                not isinstance(relative, str)
                or not isinstance(digest, str)
                or not isinstance(length, int)
                or isinstance(length, bool)
            ):
                raise JournalRefusal("artifact reference has invalid field types")
            expected_prefix = f"artifacts/{kind}/"
            if not relative.startswith(expected_prefix) or "/../" in f"/{relative}/":
                raise JournalRefusal(
                    "artifact reference escapes its content-addressed directory"
                )
            path = self.path / relative
            if path.is_symlink() or not path.is_file():
                raise JournalRefusal(
                    f"referenced artifact is not a regular file: {relative}"
                )
            try:
                content = path.read_bytes()
            except OSError as error:
                raise JournalRefusal(
                    f"referenced artifact is missing: {relative}"
                ) from error
            actual = sha256_hex(content)
            if (
                relative != f"{expected_prefix}{actual}"
                or digest != f"sha256:{actual}"
                or length != len(content)
            ):
                raise JournalRefusal(
                    f"referenced artifact identity is invalid: {relative}"
                )


def _validate_event_envelope(
    event: dict[str, JsonValue],
    sequence: int,
    previous: bytes,
    prior_events: list[dict[str, JsonValue]],
) -> None:
    """Validate one event envelope and its event-specific receipt."""

    required = {
        "schema",
        "sequence",
        "type",
        "recorded_at",
        "previous_sha256",
        "ticket",
        "payload",
        "artifacts",
    }
    if set(event) != required:
        raise JournalRefusal(f"event {sequence} has incomplete envelope fields")
    if event["schema"] != SCHEMA or event["sequence"] != sequence:
        raise JournalRefusal(f"event {sequence} has contradictory schema or sequence")
    if not isinstance(event["sequence"], int) or isinstance(event["sequence"], bool):
        raise JournalRefusal(f"event {sequence} sequence is not an integer")
    if event["previous_sha256"] != f"sha256:{sha256_hex(previous)}":
        raise JournalRefusal(f"event {sequence} breaks the predecessor hash chain")
    if not isinstance(event["type"], str):
        raise JournalRefusal(f"event {sequence} has an unknown type")
    try:
        event_type = EventType(event["type"])
    except ValueError as error:
        raise JournalRefusal(f"event {sequence} has an unknown type") from error
    if not isinstance(event["recorded_at"], str):
        raise JournalRefusal(f"event {sequence} has no recorded instant")
    _validate_instant(event["recorded_at"], f"event {sequence} recorded_at")
    if event["ticket"] is not None and (
        not isinstance(event["ticket"], str)
        or not TICKET_REFERENCE_PATTERN.fullmatch(event["ticket"])
    ):
        raise JournalRefusal(f"event {sequence} has an invalid ticket")
    if not isinstance(event["payload"], dict):
        raise JournalRefusal(f"event {sequence} payload is not an object")
    if not isinstance(event["artifacts"], dict):
        raise JournalRefusal(f"event {sequence} artifacts is not an object")
    _validate_event_payload(
        event_type,
        event["ticket"],
        event["payload"],
        set(event["artifacts"]),
        prior_events,
    )


def _validate_event_payload(
    event_type: EventType,
    ticket: str | None,
    payload: dict[str, JsonValue],
    artifact_kinds: set[str],
    prior_events: list[dict[str, JsonValue]],
) -> None:
    """Validate the receipts whose exact fields affect safe recovery."""

    # Every event has one exact durable payload and artifact surface.
    if set(payload) != EVENT_PAYLOAD_FIELDS[event_type]:
        raise JournalRefusal(f"{event_type.value} payload fields are incomplete")
    if artifact_kinds != EVENT_ARTIFACT_FIELDS[event_type]:
        raise JournalRefusal(f"{event_type.value} recovery artifacts are incomplete")

    # Run-wide events are the only events allowed to omit a ticket identity.
    run_events = {EventType.SELECTION_RECORDED, EventType.RUN_COMPLETED}
    if event_type not in run_events and ticket is None:
        raise JournalRefusal(f"{event_type} requires a ticket")
    if any(_event_type(event) is EventType.RUN_COMPLETED for event in prior_events):
        raise JournalRefusal("no event may follow run-completed")

    # Selection is the unique first event, making every later receipt part of
    # one explicitly opened run rather than an implicit ticket fragment.
    if event_type is EventType.SELECTION_RECORDED:
        if prior_events:
            raise JournalRefusal("selection-recorded must be the first event")
    elif (
        not prior_events
        or _event_type(prior_events[0]) is not EventType.SELECTION_RECORDED
    ):
        raise JournalRefusal(f"{event_type.value} requires recorded selection")

    # Common scalar checks keep corrupt receipts out of the immutable log.
    _validate_common_payload_values(event_type, payload)
    _validate_event_references(event_type, ticket, payload, prior_events)

    if event_type is EventType.TRACKER_TRANSITION_PLANNED:
        _validate_transition_plan(ticket, payload)
        expected_terminal = (
            EventType.LANDED
            if payload["transition_id"] == TransitionId.LAND.value
            else EventType.PARKED
        )
        if not any(
            event["ticket"] == ticket and _event_type(event) is expected_terminal
            for event in prior_events
        ):
            raise JournalRefusal(
                f"tracker transition requires prior {expected_terminal.value} state"
            )
    elif event_type is EventType.TRACKER_TRANSITION_COMPLETED:
        _validate_transition_completion(ticket, payload, prior_events)
    elif event_type is EventType.BUNDLE_RETIRED and not any(
        _event_type(event) is EventType.TRACKER_TRANSITION_COMPLETED
        for event in _events_after_latest_terminal(ticket, prior_events)
    ):
        raise JournalRefusal("bundle retirement requires tracker completion")
    elif event_type is EventType.RESOURCE_CLEANED:
        _validate_cleanup_order(ticket, prior_events)
    elif event_type is EventType.RUN_COMPLETED:
        _validate_run_completion_payload(payload, prior_events)


def _event_type(event: dict[str, JsonValue]) -> EventType:
    """Return the typed event identity from a validated envelope."""

    return EventType(cast(str, event["type"]))


def _require_string(payload: dict[str, JsonValue], field: str) -> str:
    """Return one required non-empty string field."""

    value = payload[field]
    if not isinstance(value, str) or not value:
        raise JournalRefusal(f"payload {field} must be a non-empty string")
    return value


def _require_positive_integer(payload: dict[str, JsonValue], field: str) -> int:
    """Return one required positive integer field."""

    value = payload[field]
    if not isinstance(value, int) or isinstance(value, bool) or value < 1:
        raise JournalRefusal(f"payload {field} must be a positive integer")
    return value


def _require_string_array(payload: dict[str, JsonValue], field: str) -> list[str]:
    """Return one duplicate-free string-array field."""

    value = payload[field]
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item for item in value)
        or len(value) != len(set(cast(list[str], value)))
    ):
        raise JournalRefusal(f"payload {field} must be a unique string array")
    return cast(list[str], value)


def _require_matching_string(
    payload: dict[str, JsonValue], field: str, pattern: re.Pattern[str]
) -> str:
    """Return one required string matching its recovery identity grammar."""

    value = _require_string(payload, field)
    if not pattern.fullmatch(value):
        raise JournalRefusal(f"payload {field} has an invalid identity")
    return value


def _validate_blob_map(value: JsonValue, field: str) -> None:
    """Validate one destination-to-compiled-blob identity mapping."""

    if not isinstance(value, dict) or any(
        not isinstance(path, str)
        or not path
        or not isinstance(blob, str)
        or not COMPILED_BLOB_PATTERN.fullmatch(blob)
        for path, blob in value.items()
    ):
        raise JournalRefusal(f"payload {field} must map paths to compiled blobs")


def _validate_common_payload_values(
    event_type: EventType, payload: dict[str, JsonValue]
) -> None:
    """Validate recovery-critical scalar and collection values by event."""

    # Attempt-scoped receipts always identify the exact paid attempt.
    attempt_events = {
        EventType.ROUTE_RECORDED,
        EventType.ATTEMPT_STARTED,
        EventType.ATTEMPT_RETURNED,
        EventType.PATCH_CAPTURED,
        EventType.REVIEW_COMPLETED,
        EventType.REVISE_REQUESTED,
        EventType.EXECUTOR_REHYDRATED,
        EventType.HUMAN_CONFLICT,
        EventType.OBSERVATION_RECORDED,
    }
    if event_type in attempt_events:
        _require_positive_integer(payload, "attempt")

    # Identity fields are opaque here; their producers own their semantics.
    string_fields: dict[EventType, tuple[str, ...]] = {
        EventType.BUNDLE_CONSUMED: ("bundle_fingerprint", "execution_base"),
        EventType.BUNDLE_RELEASED: ("bundle_fingerprint", "reason"),
        EventType.TICKET_ASSIGNED: ("assignee",),
        EventType.ATTEMPT_STARTED: ("attempt_id", "base", "worktree", "branch"),
        EventType.REVIEW_COMPLETED: ("verdict", "finding_summary"),
        EventType.REBUILD_REQUESTED: (
            "head",
            "compile_invocation",
            "resume_invocation",
        ),
        EventType.OWNER_ANSWERED: ("answer",),
        EventType.LANDING_STARTED: ("previous_head", "candidate", "tree"),
        EventType.HUMAN_CONFLICT: ("branch", "worktree"),
        EventType.LANDED: ("commit", "tree", "bundle_fingerprint"),
        EventType.PARKED: ("park_class", "message", "reason"),
        EventType.STRANDED: ("reason",),
        EventType.BUNDLE_RETIRED: ("bundle_fingerprint",),
    }
    for field in string_fields.get(event_type, ()):
        _require_string(payload, field)

    # Content and object identities must be independently verifiable rather
    # than merely non-empty strings inside an immutable receipt.
    for field in {
        EventType.BUNDLE_CONSUMED: ("bundle_fingerprint",),
        EventType.BUNDLE_RELEASED: ("bundle_fingerprint",),
        EventType.LANDED: ("bundle_fingerprint",),
        EventType.BUNDLE_RETIRED: ("bundle_fingerprint",),
    }.get(event_type, ()):
        _require_matching_string(payload, field, CONTENT_DIGEST_PATTERN)
    for field in {
        EventType.BUNDLE_CONSUMED: ("execution_base",),
        EventType.ATTEMPT_STARTED: ("base",),
        EventType.REBUILD_REQUESTED: ("head",),
        EventType.LANDING_STARTED: ("previous_head", "candidate", "tree"),
        EventType.LANDED: ("commit", "tree"),
    }.get(event_type, ()):
        _require_matching_string(payload, field, OBJECT_ID_PATTERN)

    # Lists and opaque objects must still have their recovery-required shape.
    for field in {
        EventType.PATCH_CAPTURED: ("changed_paths",),
        EventType.DISPATCHER_WRITE_RECORDED: ("paths",),
        EventType.RESOURCE_CLEANED: ("resources",),
    }.get(event_type, ()):
        _require_string_array(payload, field)
    for field in {
        EventType.ROUTE_RECORDED: ("decision",),
        EventType.BUNDLE_CONSUMED: (
            "source_fingerprints",
            "footprint",
        ),
        EventType.LANDING_STARTED: ("test_blobs",),
        EventType.LANDED: ("test_blobs",),
        EventType.RUN_COMPLETED: ("tickets",),
    }.get(event_type, ()):
        if not isinstance(payload[field], dict):
            raise JournalRefusal(f"payload {field} must be an object")

    # Landing receipts carry the complete protected-test identity rather than
    # an optional caller-selected evidence subset.
    if event_type in {EventType.LANDING_STARTED, EventType.LANDED}:
        _validate_blob_map(payload["test_blobs"], "test_blobs")

    # A Route decision may be opaque to persistence but cannot be absent.
    if event_type is EventType.ROUTE_RECORDED and not payload["decision"]:
        raise JournalRefusal("payload decision must be a non-empty object")

    # Bundle audit lists are retained compactly after their bulk is retired.
    if event_type is EventType.BUNDLE_CONSUMED:
        for field in ("command_ids", "done_criterion_ids"):
            _require_string_array(payload, field)
        for field in ("allocations", "tests"):
            if not isinstance(payload[field], list):
                raise JournalRefusal(f"payload {field} must be an array")
        _validate_bundle_audit_payload(payload)

    # A revision receipt names both the rejected paid attempt and its one next
    # attempt, preventing an ambiguous round from becoming durable.
    if event_type is EventType.REVISE_REQUESTED:
        prior_attempt = _require_positive_integer(payload, "prior_attempt")
        if payload["attempt"] != prior_attempt + 1:
            raise JournalRefusal(
                "revise-requested attempt does not follow prior_attempt"
            )


def _validate_bundle_audit_payload(payload: dict[str, JsonValue]) -> None:
    """Validate the compact bundle identities needed after bulk retirement."""

    # Source identities must remain independently checkable after the escrowed
    # compiler artifacts are removed.
    sources = payload["source_fingerprints"]
    if (
        not isinstance(sources, dict)
        or set(sources) != {"child_fingerprint", "parent_fingerprint"}
        or any(
            not isinstance(digest, str) or not CONTENT_DIGEST_PATTERN.fullmatch(digest)
            for digest in sources.values()
        )
    ):
        raise JournalRefusal("bundle source_fingerprints are invalid")

    # Footprint classes are exact and retain ordered, duplicate-free paths or
    # resource identities for later audit.
    footprint = payload["footprint"]
    footprint_fields = {
        "reads",
        "modifies",
        "creates",
        "deletes",
        "compiler_owned_tests",
        "dispatcher_owned_writes",
        "serial_resources",
    }
    if not isinstance(footprint, dict) or set(footprint) != footprint_fields:
        raise JournalRefusal("bundle footprint fields are incomplete")
    for field, values in footprint.items():
        if (
            not isinstance(values, list)
            or any(
                not isinstance(value, str) or not _is_relative_posix_path(value)
                for value in values
            )
            or len(values) != len(set(cast(list[str], values)))
        ):
            raise JournalRefusal(f"bundle footprint {field} is invalid")

    # The four executor/test write classes are disjoint, and dispatcher-owned
    # writes overlap none of them, exactly as the compiled-plan Interface says.
    write_fields = ("modifies", "creates", "deletes", "compiler_owned_tests")
    write_sets = [set(cast(list[str], footprint[field])) for field in write_fields]
    if any(
        left & right
        for index, left in enumerate(write_sets)
        for right in write_sets[index + 1 :]
    ):
        raise JournalRefusal("bundle write footprint classes overlap")
    dispatcher_writes = set(cast(list[str], footprint["dispatcher_owned_writes"]))
    if any(dispatcher_writes & writes for writes in write_sets):
        raise JournalRefusal("bundle dispatcher writes overlap another write class")

    # Serial allocations retain their exact registry and identifiers, and may
    # name only registries declared by the plan footprint.
    allocations = payload["allocations"]
    if not isinstance(allocations, list):
        raise JournalRefusal("bundle allocations must be an array")
    allocation_registries: set[str] = set()
    serial_resources = set(cast(list[str], footprint["serial_resources"]))
    for allocation in allocations:
        if not isinstance(allocation, dict) or set(allocation) != {
            "registry",
            "identifiers",
        }:
            raise JournalRefusal("bundle allocation receipt is invalid")
        registry = allocation["registry"]
        identifiers = allocation["identifiers"]
        if (
            not isinstance(registry, str)
            or registry not in serial_resources
            or registry in allocation_registries
            or not isinstance(identifiers, list)
            or not identifiers
            or any(
                not isinstance(identifier, str) or not identifier
                for identifier in identifiers
            )
            or len(identifiers) != len(set(cast(list[str], identifiers)))
        ):
            raise JournalRefusal("bundle allocation receipt is invalid")
        allocation_registries.add(registry)
    if allocation_registries != serial_resources:
        raise JournalRefusal("bundle allocations do not cover serial_resources")

    # Test receipts preserve only their destination and compiled Git blob after
    # the compiler-owned byte copies are retired.
    tests = payload["tests"]
    if not isinstance(tests, list):
        raise JournalRefusal("bundle tests must be an array")
    for test in tests:
        if (
            not isinstance(test, dict)
            or set(test) != {"destination", "compiled_blob"}
            or not isinstance(test["destination"], str)
            or not _is_relative_posix_path(test["destination"])
            or not isinstance(test["compiled_blob"], str)
            or not COMPILED_BLOB_PATTERN.fullmatch(test["compiled_blob"])
        ):
            raise JournalRefusal("bundle test receipt is invalid")
    destinations = [
        cast(str, cast(dict[str, JsonValue], test)["destination"]) for test in tests
    ]
    if len(destinations) != len(set(destinations)) or destinations != cast(
        list[str], footprint["compiler_owned_tests"]
    ):
        raise JournalRefusal("bundle tests contradict compiler_owned_tests")


def _is_relative_posix_path(value: str) -> bool:
    """Return whether a string satisfies the compiled-plan path grammar."""

    return (
        bool(value)
        and not value.startswith("/")
        and not value.endswith("/")
        and not any(marker in value for marker in ("*", "?", "[", "]"))
        and all(segment not in {"", ".", ".."} for segment in value.split("/"))
    )


def _validate_event_references(
    event_type: EventType,
    ticket: str | None,
    payload: dict[str, JsonValue],
    prior_events: list[dict[str, JsonValue]],
) -> None:
    """Validate recovery pointers against the immutable prior prefix."""

    # fmt: off
    # Validate the initial bundle and its one optional REBUILD replacement.
    if event_type is EventType.BUNDLE_CONSUMED:

        # Count prior consumptions and enforce the one-replacement limit.
        ticket_events = [event for event in prior_events if event["ticket"] == ticket]
        consumed_bundles = [
            event
            for event in ticket_events
            if _event_type(event) is EventType.BUNDLE_CONSUMED
        ]
        if len(consumed_bundles) >= 2:
            raise JournalRefusal("ticket already consumed its REBUILD replacement")
        if not consumed_bundles:
            return

        # Find and verify the newer REBUILD boundary for the replacement.
        latest_rebuild = _latest_ticket_event(
            ticket_events, ticket, EventType.REBUILD_REQUESTED
        )
        latest_bundle = consumed_bundles[-1]
        if latest_rebuild is None or cast(int, latest_rebuild["sequence"]) <= cast(
            int, latest_bundle["sequence"]
        ):
            raise JournalRefusal(
                "duplicate bundle consumption requires a newer rebuild"
            )

        # Find the bundle release recorded after that REBUILD boundary.
        release = next(
            (
                event
                for event in reversed(ticket_events)
                if _event_type(event) is EventType.BUNDLE_RELEASED
                and cast(int, event["sequence"]) > cast(int, latest_rebuild["sequence"])
            ),
            None,
        )
        if release is None:
            raise JournalRefusal("recompiled bundle requires post-rebuild release")

        # Verify the replacement bundle against the recorded base and identity.
        rebuild_payload = cast(dict[str, JsonValue], latest_rebuild["payload"])
        bundle_payload = cast(dict[str, JsonValue], latest_bundle["payload"])
        if payload["execution_base"] != rebuild_payload["head"]:
            raise JournalRefusal("recompiled bundle targets a different head")
        if payload["bundle_fingerprint"] == bundle_payload["bundle_fingerprint"]:
            raise JournalRefusal("recompiled bundle repeats the old fingerprint")

    # fmt: on

    # Sequence pointers bind a later receipt to one exact earlier boundary.
    references: dict[EventType, tuple[str, EventType]] = {
        EventType.REVISE_REQUESTED: ("review_sequence", EventType.REVIEW_COMPLETED),
        EventType.EXECUTOR_REHYDRATED: (
            "revision_sequence",
            EventType.REVISE_REQUESTED,
        ),
        EventType.REBUILD_REQUESTED: ("review_sequence", EventType.REVIEW_COMPLETED),
        EventType.OWNER_ANSWERED: ("for_sequence", EventType.HUMAN_CONFLICT),
        EventType.LANDING_STARTED: ("review_sequence", EventType.REVIEW_COMPLETED),
        EventType.HUMAN_CONFLICT: ("landing_sequence", EventType.LANDING_STARTED),
        EventType.LANDED: ("landing_sequence", EventType.LANDING_STARTED),
    }
    reference = references.get(event_type)
    if reference is not None:
        field, expected_type = reference
        sequence = _require_positive_integer(payload, field)
        referenced = _require_prior_event(prior_events, sequence, ticket, expected_type)
        if event_type is EventType.REVISE_REQUESTED:
            referenced_payload = cast(dict[str, JsonValue], referenced["payload"])
            if referenced_payload["attempt"] != payload["prior_attempt"]:
                raise JournalRefusal("revision review names a different prior attempt")
        elif event_type is EventType.EXECUTOR_REHYDRATED:
            referenced_payload = cast(dict[str, JsonValue], referenced["payload"])
            if referenced_payload["attempt"] != payload["attempt"]:
                raise JournalRefusal("rehydration names a different revision attempt")

    # R3 rehydration binds the fresh context to the exact previously recorded
    # Route decision whose execution role and configuration it recreates.
    if event_type is EventType.EXECUTOR_REHYDRATED:
        route_sequence = _require_positive_integer(payload, "route_sequence")
        route = _require_prior_event(
            prior_events, route_sequence, ticket, EventType.ROUTE_RECORDED
        )
        revision = _require_prior_event(
            prior_events,
            cast(int, payload["revision_sequence"]),
            ticket,
            EventType.REVISE_REQUESTED,
        )
        route_payload = cast(dict[str, JsonValue], route["payload"])
        revision_payload = cast(dict[str, JsonValue], revision["payload"])
        if route_payload["attempt"] != revision_payload["prior_attempt"]:
            raise JournalRefusal("rehydration Route point names a different attempt")

    # Attempt persistence is meaningful only beside the exact earlier attempt
    # boundary whose work it makes recoverable.
    required_predecessors: dict[EventType, EventType] = {
        EventType.ROUTE_RECORDED: EventType.BUNDLE_CONSUMED,
        EventType.TICKET_ASSIGNED: EventType.ROUTE_RECORDED,
        EventType.ATTEMPT_STARTED: EventType.ROUTE_RECORDED,
        EventType.PATCH_CAPTURED: EventType.ATTEMPT_STARTED,
        EventType.ATTEMPT_RETURNED: EventType.ATTEMPT_STARTED,
        EventType.DISPATCHER_WRITE_RECORDED: EventType.ATTEMPT_STARTED,
        EventType.REVIEW_COMPLETED: EventType.PATCH_CAPTURED,
        EventType.OBSERVATION_RECORDED: EventType.REVIEW_COMPLETED,
        EventType.BUNDLE_RELEASED: EventType.BUNDLE_CONSUMED,
    }
    predecessor = required_predecessors.get(event_type)
    if predecessor is not None:
        previous = next(
            (
                event
                for event in reversed(prior_events)
                if event["ticket"] == ticket and _event_type(event) is predecessor
            ),
            None,
        )
        if previous is None:
            raise JournalRefusal(
                f"{event_type.value} requires prior {predecessor.value}"
            )
        if "attempt" in payload:
            previous_payload = cast(dict[str, JsonValue], previous["payload"])
            previous_attempt = previous_payload.get("attempt")
            if previous_attempt is not None and previous_attempt != payload["attempt"]:
                raise JournalRefusal(
                    f"{event_type.value} attempt contradicts {predecessor.value}"
                )

    # Starting an executor also requires the assignment durable first.
    if event_type is EventType.ATTEMPT_STARTED and not any(
        event["ticket"] == ticket and _event_type(event) is EventType.TICKET_ASSIGNED
        for event in prior_events
    ):
        raise JournalRefusal("attempt-started requires prior ticket assignment")

    # A parked receipt points at the latest accepted patch and never an older
    # paid attempt; null is valid only when no patch was captured.
    if event_type is EventType.PARKED:
        patch_sequence = payload["patch_sequence"]
        latest_patch = next(
            (
                cast(int, event["sequence"])
                for event in reversed(prior_events)
                if event["ticket"] == ticket
                and _event_type(event) is EventType.PATCH_CAPTURED
            ),
            None,
        )
        if patch_sequence != latest_patch:
            raise JournalRefusal("parked patch_sequence is not the latest patch")

    # A landing window repeats the compiler-owned destinations and blob
    # identities from the exact latest consumed bundle.
    if event_type is EventType.LANDING_STARTED:
        bundle = _latest_ticket_event(prior_events, ticket, EventType.BUNDLE_CONSUMED)
        if bundle is None:
            raise JournalRefusal("landing-started requires a consumed bundle")
        bundle_payload = cast(dict[str, JsonValue], bundle["payload"])
        if payload["test_blobs"] != _bundle_test_blobs(bundle_payload):
            raise JournalRefusal("landing tests contradict the consumed bundle")

    # Bundle lifecycle receipts must name the latest consumed identity, never a
    # stale or caller-invented fingerprint.
    if event_type in {
        EventType.BUNDLE_RELEASED,
        EventType.LANDED,
        EventType.BUNDLE_RETIRED,
    }:
        bundle = next(
            (
                event
                for event in reversed(prior_events)
                if event["ticket"] == ticket
                and _event_type(event) is EventType.BUNDLE_CONSUMED
            ),
            None,
        )
        if bundle is None:
            raise JournalRefusal(f"{event_type.value} requires a consumed bundle")
        bundle_payload = cast(dict[str, JsonValue], bundle["payload"])
        if payload["bundle_fingerprint"] != bundle_payload["bundle_fingerprint"]:
            raise JournalRefusal(f"{event_type.value} names a different bundle")

    # Landing completion repeats the exact candidate, tree, and protected-test
    # identities from its referenced landing window.
    if event_type is EventType.LANDED:
        landing = _require_prior_event(
            prior_events,
            cast(int, payload["landing_sequence"]),
            ticket,
            EventType.LANDING_STARTED,
        )
        landing_payload = cast(dict[str, JsonValue], landing["payload"])
        if (
            payload["commit"] != landing_payload["candidate"]
            or payload["tree"] != landing_payload["tree"]
            or payload["test_blobs"] != landing_payload["test_blobs"]
        ):
            raise JournalRefusal("landed receipt contradicts its landing window")

    # Cleanup proves that every disposable attempt resource named by the log was
    # included in the caller's completed cleanup boundary.
    if event_type is EventType.RESOURCE_CLEANED:
        cleaned = set(cast(list[str], payload["resources"]))
        required_resources = {
            cast(str, attempt_payload[field])
            for event in prior_events
            if event["ticket"] == ticket
            and _event_type(event) is EventType.ATTEMPT_STARTED
            for attempt_payload in [cast(dict[str, JsonValue], event["payload"])]
            for field in ("worktree", "branch")
        }
        if not required_resources.issubset(cleaned):
            raise JournalRefusal("resource cleanup omits an attempt resource")

    # Landed and parked tickets always consume a bundle whose audit fields the
    # compact archive must preserve after retirement.
    if event_type in {EventType.LANDED, EventType.PARKED} and not any(
        event["ticket"] == ticket and _event_type(event) is EventType.BUNDLE_CONSUMED
        for event in prior_events
    ):
        raise JournalRefusal(f"{event_type.value} requires a consumed bundle")


def _require_prior_event(
    prior_events: list[dict[str, JsonValue]],
    sequence: int,
    ticket: str | None,
    expected_type: EventType,
) -> dict[str, JsonValue]:
    """Return one exact prior ticket event selected by sequence."""

    if sequence > len(prior_events):
        raise JournalRefusal(f"{expected_type.value} sequence points beyond the log")
    event = prior_events[sequence - 1]
    if event["ticket"] != ticket or _event_type(event) is not expected_type:
        raise JournalRefusal(f"sequence does not name prior {expected_type.value}")
    return event


def _latest_ticket_event(
    events: list[dict[str, JsonValue]],
    ticket: str | None,
    event_type: EventType,
) -> dict[str, JsonValue] | None:
    """Return the latest typed event for one ticket."""

    return next(
        (
            event
            for event in reversed(events)
            if event["ticket"] == ticket and _event_type(event) is event_type
        ),
        None,
    )


def _bundle_test_blobs(payload: dict[str, JsonValue]) -> dict[str, str]:
    """Return the canonical destination-to-blob mapping for one bundle."""

    tests = cast(list[JsonValue], payload["tests"])
    return {
        cast(str, cast(dict[str, JsonValue], test)["destination"]): cast(
            str, cast(dict[str, JsonValue], test)["compiled_blob"]
        )
        for test in tests
    }


def _validate_cleanup_order(
    ticket: str | None, prior_events: list[dict[str, JsonValue]]
) -> None:
    """Require the terminal-specific durable boundary before cleanup."""

    tail = _events_after_latest_terminal(ticket, prior_events)
    if not tail:
        raise JournalRefusal("resource cleanup requires a terminal ticket state")
    terminal = TerminalState(_event_type(tail[0]).value)
    requirements = TERMINAL_REQUIREMENTS[terminal]
    tail_types = {_event_type(event) for event in tail[1:]}
    if requirements.bundle_boundary not in tail_types:
        raise JournalRefusal(
            f"{terminal.value} cleanup requires "
            f"{requirements.bundle_boundary.value.replace('-', ' ')}"
        )


def _events_after_latest_terminal(
    ticket: str | None, events: list[dict[str, JsonValue]]
) -> list[dict[str, JsonValue]]:
    """Return the latest terminal event and only its subsequent ticket tail."""

    ticket_events = [event for event in events if event["ticket"] == ticket]
    terminal_index = next(
        (
            index
            for index in range(len(ticket_events) - 1, -1, -1)
            if _event_type(ticket_events[index])
            in {EventType.LANDED, EventType.PARKED, EventType.STRANDED}
        ),
        None,
    )
    return ticket_events[terminal_index:] if terminal_index is not None else []


def _validate_run_completion_payload(
    payload: dict[str, JsonValue], prior_events: list[dict[str, JsonValue]]
) -> None:
    """Require cleanup for every terminal named by run completion."""

    tickets = payload["tickets"]
    if not isinstance(tickets, dict) or not tickets:
        raise JournalRefusal("run completion tickets must be a non-empty object")
    for ticket, terminal_value in tickets.items():
        try:
            terminal = TerminalState(cast(str, terminal_value))
        except (TypeError, ValueError) as error:
            raise JournalRefusal(
                f"run completion has invalid state for {ticket}"
            ) from error
        tail = _events_after_latest_terminal(ticket, prior_events)
        if not tail or _event_type(tail[0]).value != terminal.value:
            raise JournalRefusal(
                f"run completion contradicts terminal state for {ticket}"
            )
        _validate_terminal_prerequisites(ticket, terminal, tail, "run completion")


def _validate_terminal_prerequisites(
    ticket: str,
    terminal: TerminalState,
    tail: list[dict[str, JsonValue]],
    boundary: str,
) -> None:
    """Require the shared terminal facts before completion or archive."""

    requirements = TERMINAL_REQUIREMENTS[terminal]
    tail_types = {_event_type(event) for event in tail[1:]}
    if EventType.RESOURCE_CLEANED not in tail_types:
        raise JournalRefusal(f"{boundary} precedes cleanup for {ticket}")
    if requirements.requires_tracker_completion and (
        EventType.TRACKER_TRANSITION_COMPLETED not in tail_types
    ):
        raise JournalRefusal(f"{boundary} precedes tracker completion for {ticket}")
    if requirements.bundle_boundary not in tail_types:
        raise JournalRefusal(
            f"{boundary} precedes {requirements.bundle_boundary.value} for {ticket}"
        )


def _validate_transition_plan(
    ticket: str | None, payload: dict[str, JsonValue]
) -> None:
    """Validate a concrete pre-mutation tracker transition receipt."""

    if set(payload) != {"transition_id", "resolution", "pre_projection"}:
        raise JournalRefusal("tracker-transition-planned has incomplete fields")
    transition_id = payload["transition_id"]
    resolution = payload["resolution"]
    pre = payload["pre_projection"]
    try:
        typed_transition = TransitionId(cast(str, transition_id))
    except (TypeError, ValueError) as error:
        raise JournalRefusal(
            "tracker-transition-planned has an invalid transition"
        ) from error
    if not isinstance(resolution, dict) or not isinstance(pre, dict):
        raise JournalRefusal("tracker-transition-planned has invalid field types")
    _validate_resolution(typed_transition, resolution, pre)


def _validate_resolution(
    transition_id: TransitionId,
    resolution: dict[str, JsonValue],
    pre: dict[str, JsonValue],
) -> None:
    """Validate portable labels, assignment, status, and convention sources."""

    resolution_keys = {
        "executable_ready_label",
        "target_label",
        "preserved_labels",
        "milestone",
        "status",
        "assignees",
        "agent_instruction_address",
        "issue_tracker_convention_address",
    }
    projection_keys = {"labels", "milestone", "status", "assignees"}
    if set(resolution) != resolution_keys or set(pre) != projection_keys:
        raise JournalRefusal("tracker transition receipt fields are incomplete")
    if not isinstance(resolution["executable_ready_label"], str):
        raise JournalRefusal("tracker transition has no executable-ready label")
    for key in ("preserved_labels", "assignees"):
        values = resolution[key]
        if not isinstance(values, list) or any(
            not isinstance(item, str) for item in values
        ):
            raise JournalRefusal(f"tracker transition {key} must be a string array")
        if len(values) != len(set(values)):
            raise JournalRefusal(f"tracker transition {key} contains duplicates")
        if any(not value for value in values):
            raise JournalRefusal(f"tracker transition {key} contains an empty identity")
    for key in ("agent_instruction_address", "issue_tracker_convention_address"):
        if not isinstance(resolution[key], str) or not resolution[key]:
            raise JournalRefusal(f"tracker transition {key} must be concrete")
    if not isinstance(pre["labels"], list) or any(
        not isinstance(item, str) for item in pre["labels"]
    ):
        raise JournalRefusal("tracker pre-projection labels must be a string array")
    if len(pre["labels"]) != len(set(pre["labels"])):
        raise JournalRefusal("tracker pre-projection labels contain duplicates")
    pre_assignees = pre["assignees"]
    if (
        not isinstance(pre_assignees, list)
        or any(
            not isinstance(assignee, str) or not assignee for assignee in pre_assignees
        )
        or len(pre_assignees) != len(set(pre_assignees))
    ):
        raise JournalRefusal("tracker pre-projection assignees are invalid")
    if resolution["milestone"] is not None and not isinstance(
        resolution["milestone"], str
    ):
        raise JournalRefusal("tracker transition milestone must be a string or null")
    if not isinstance(resolution["status"], str) or not resolution["status"]:
        raise JournalRefusal("tracker transition status must be a non-empty string")

    # The preservation receipt is the exact old label set minus readiness.
    ready = resolution["executable_ready_label"]
    pre_labels = cast(list[str], pre["labels"])
    preserved = [label for label in pre_labels if label != ready]
    if ready not in pre_labels or resolution["preserved_labels"] != preserved:
        raise JournalRefusal(
            "tracker transition preserved labels do not match pre-state"
        )
    if (
        resolution["milestone"] != pre["milestone"]
        or resolution["status"] != pre["status"]
    ):
        raise JournalRefusal(
            "tracker transition changes an unowned milestone or status"
        )

    # Landing preserves assignment; both parking transitions unassign and add
    # one concretely resolved lifecycle label.
    if transition_id is TransitionId.LAND:
        if (
            resolution["target_label"] is not None
            or resolution["assignees"] != pre["assignees"]
        ):
            raise JournalRefusal("T-LAND must preserve assignment and add no label")
    elif (
        not isinstance(resolution["target_label"], str)
        or not resolution["target_label"]
        or resolution["assignees"] != []
    ):
        raise JournalRefusal(
            f"{transition_id} must resolve one target label and unassign"
        )


def _validate_transition_completion(
    ticket: str | None,
    payload: dict[str, JsonValue],
    prior_events: list[dict[str, JsonValue]],
) -> None:
    """Verify post-mutation state against the durable plan, not conventions."""

    required = {
        "transition_id",
        "planned_sequence",
        "resolution",
        "observed_post_projection",
    }
    if (
        set(payload) != required
        or not isinstance(payload["planned_sequence"], int)
        or isinstance(payload["planned_sequence"], bool)
    ):
        raise JournalRefusal("tracker-transition-completed has incomplete fields")
    sequence = payload["planned_sequence"]
    if sequence < 1 or sequence > len(prior_events):
        raise JournalRefusal("tracker-transition-completed names no prior plan")
    planned = prior_events[sequence - 1]
    if (
        _event_type(planned) is not EventType.TRACKER_TRANSITION_PLANNED
        or planned["ticket"] != ticket
    ):
        raise JournalRefusal("tracker-transition-completed names the wrong plan")
    planned_payload = cast(dict[str, JsonValue], planned["payload"])
    if (
        payload["transition_id"] != planned_payload["transition_id"]
        or payload["resolution"] != planned_payload["resolution"]
    ):
        raise JournalRefusal(
            "tracker-transition-completed changed its durable resolution"
        )
    observed = payload["observed_post_projection"]
    if not isinstance(observed, dict):
        raise JournalRefusal("observed tracker projection is not an object")

    # Apply only the already planned label and assignment delta.
    resolution = cast(dict[str, JsonValue], payload["resolution"])
    expected_labels = list(cast(list[str], resolution["preserved_labels"]))
    if (
        resolution["target_label"] is not None
        and resolution["target_label"] not in expected_labels
    ):
        expected_labels.append(cast(str, resolution["target_label"]))
    observed_labels = observed.get("labels")
    observed_assignees = observed.get("assignees")
    if (
        set(observed) != {"labels", "milestone", "status", "assignees"}
        or not isinstance(observed_labels, list)
        or not isinstance(observed_assignees, list)
        or any(not isinstance(label, str) for label in observed_labels)
        or any(not isinstance(assignee, str) for assignee in observed_assignees)
        or len(observed_labels) != len(set(cast(list[str], observed_labels)))
        or len(observed_assignees) != len(set(cast(list[str], observed_assignees)))
        or set(observed_labels) != set(expected_labels)
        or set(observed_assignees) != set(cast(list[str], resolution["assignees"]))
        or observed["milestone"] != resolution["milestone"]
        or observed["status"] != resolution["status"]
    ):
        raise JournalRefusal("observed tracker projection does not match durable plan")


def _empty_ticket_projection() -> dict[str, JsonValue]:
    """Return the replaceable in-memory state for one selected ticket."""

    return {
        "last_event": None,
        "terminal": None,
        "continuation": None,
        "receipts": {},
        "recovery_action": RecoveryAction.START_TICKET.value,
    }


def _apply_event(projection: dict[str, JsonValue], event: dict[str, JsonValue]) -> None:
    """Apply one validated event to a ticket's recovery projection."""

    event_type = _event_type(event)
    projection["last_event"] = event_type.value
    receipts = cast(dict[str, JsonValue], projection["receipts"])
    event_receipts = cast(list[JsonValue], receipts.setdefault(event_type.value, []))
    event_receipts.append(
        {
            "sequence": event["sequence"],
            "payload": event["payload"],
            "artifacts": event["artifacts"],
        }
    )

    # Revision requests begin as live continuations; only a durable R3 event
    # changes the reportable fact to fresh-context rehydration.
    if event_type is EventType.REVISE_REQUESTED:
        projection["continuation"] = ContinuationMode.LIVE.value
    elif event_type is EventType.EXECUTOR_REHYDRATED:
        projection["continuation"] = ContinuationMode.FRESH.value

    terminal_types = {
        EventType.LANDED: TerminalState.LANDED,
        EventType.PARKED: TerminalState.PARKED,
        EventType.STRANDED: TerminalState.STRANDED,
    }
    terminal = terminal_types.get(event_type)
    if terminal is not None and projection["terminal"] not in {
        None,
        terminal.value,
    }:
        raise JournalRefusal("ticket has contradictory terminal events")
    if terminal is not None:
        projection["terminal"] = terminal.value


def _recovery_action(events: list[dict[str, JsonValue]]) -> str:
    """Map the newest durable boundary to one crash-safe next action."""

    event_types = [_event_type(event) for event in events]
    if not event_types:
        return RecoveryAction.START_TICKET.value
    if EventType.RUN_COMPLETED in event_types:
        return RecoveryAction.ARCHIVE_RUN.value

    # Terminal recovery advances through tracker, retirement, and cleanup in
    # order; older attempt history cannot override these later boundaries.
    terminal_index = next(
        (
            index
            for index in range(len(event_types) - 1, -1, -1)
            if event_types[index]
            in {EventType.LANDED, EventType.PARKED, EventType.STRANDED}
        ),
        None,
    )
    if terminal_index is not None:
        terminal = TerminalState(event_types[terminal_index].value)
        requirements = TERMINAL_REQUIREMENTS[terminal]
        tail = event_types[terminal_index + 1 :]
        if requirements.requires_tracker_completion and (
            EventType.TRACKER_TRANSITION_COMPLETED not in tail
        ):
            return RecoveryAction.COMPLETE_TRACKER_TRANSITION.value
        if requirements.bundle_boundary not in tail:
            return requirements.bundle_action.value
        if EventType.RESOURCE_CLEANED not in tail:
            return requirements.cleanup_action.value
        return RecoveryAction.COMPLETE_RUN.value

    # A REBUILD remains authoritative through release of its old bundle. Only
    # a later fully validated consumption proves recompilation completed.
    latest_rebuild = _latest_event_index(event_types, EventType.REBUILD_REQUESTED)
    latest_bundle = _latest_event_index(event_types, EventType.BUNDLE_CONSUMED)
    if latest_rebuild is not None and (
        latest_bundle is None or latest_bundle < latest_rebuild
    ):
        return RecoveryAction.AWAIT_RECOMPILE.value

    # Other nonterminal recovery follows the newest state-changing event. A new
    # attempt or verified bundle supersedes older revision state.
    last = event_types[-1]
    if last is EventType.OWNER_ANSWERED:
        payload = cast(dict[str, JsonValue], events[-1]["payload"])
        referenced = next(
            event for event in events if event["sequence"] == payload["for_sequence"]
        )
        last = _event_type(referenced)
    actions: dict[EventType, RecoveryAction] = {
        EventType.HUMAN_CONFLICT: RecoveryAction.RESUME_HUMAN_CONFLICT,
        EventType.REBUILD_REQUESTED: RecoveryAction.AWAIT_RECOMPILE,
        EventType.LANDING_STARTED: RecoveryAction.RECONCILE_LANDING,
        EventType.REVISE_REQUESTED: RecoveryAction.RESUME_REVISION,
        EventType.EXECUTOR_REHYDRATED: RecoveryAction.RESUME_REVISION,
        EventType.ATTEMPT_STARTED: RecoveryAction.REPLAY_ATTEMPT,
        EventType.ATTEMPT_RETURNED: RecoveryAction.REPLAY_ATTEMPT,
        EventType.PATCH_CAPTURED: RecoveryAction.REVIEW_PATCH,
    }
    if last in actions:
        return actions[last].value
    if EventType.BUNDLE_CONSUMED in event_types:
        return RecoveryAction.CONTINUE_TICKET.value
    return RecoveryAction.START_TICKET.value


def _latest_event_index(
    event_types: list[EventType], expected: EventType
) -> int | None:
    """Return the latest index for one typed event, or null when absent."""

    return next(
        (
            index
            for index in range(len(event_types) - 1, -1, -1)
            if event_types[index] is expected
        ),
        None,
    )


def _validate_git_evidence(
    events: list[dict[str, JsonValue]], evidence_items: Sequence[Mapping[str, Any]]
) -> None:
    """Validate observations for explicitly identified landing windows."""

    if not evidence_items:
        raise JournalRefusal("Git evidence must be a non-empty array")

    # Each ticket and sequence pair selects one window, preventing concurrent
    # candidates from borrowing another ticket's observations.
    seen: set[tuple[str, int]] = set()
    for raw_evidence in evidence_items:
        evidence = _validate_git_evidence_shape(raw_evidence)
        identity = (evidence["ticket"], evidence["landing_sequence"])
        if identity in seen:
            raise JournalRefusal("duplicate Git evidence for landing window")
        seen.add(identity)

        landing = _require_prior_event(
            events,
            evidence["landing_sequence"],
            evidence["ticket"],
            EventType.LANDING_STARTED,
        )
        payload = cast(dict[str, JsonValue], landing["payload"])
        bundle = next(
            (
                event
                for event in reversed(events[: evidence["landing_sequence"] - 1])
                if event["ticket"] == evidence["ticket"]
                and _event_type(event) is EventType.BUNDLE_CONSUMED
            ),
            None,
        )
        if bundle is None:
            raise JournalRefusal("Git evidence landing window has no bundle")
        bundle_payload = cast(dict[str, JsonValue], bundle["payload"])
        bundle_test_blobs = _bundle_test_blobs(bundle_payload)
        expected_trailers = {
            "Kntnt-Ticket": evidence["ticket"],
            "Kntnt-Plan": cast(str, bundle_payload["bundle_fingerprint"]),
        }

        # Candidate identity is checked even while the integration ref remains
        # at previous_head; only reachability changes between the two states.
        if (
            evidence["candidate_commit"] != payload["candidate"]
            or evidence["candidate_tree"] != payload["tree"]
            or evidence["test_blobs"] != payload["test_blobs"]
            or evidence["test_blobs"] != bundle_test_blobs
            or payload["test_blobs"] != bundle_test_blobs
            or evidence["expected_trailers"] != expected_trailers
            or evidence["observed_trailers"] != expected_trailers
        ):
            raise JournalRefusal("contradictory Git evidence for landing window")
        if evidence["integration_ref_head"] == payload["previous_head"]:
            if evidence["candidate_reachable"]:
                raise JournalRefusal("candidate cannot be reachable from previous_head")
        elif evidence["integration_ref_head"] == payload["candidate"]:
            if not evidence["candidate_reachable"]:
                raise JournalRefusal("landed candidate must be reachable")
        else:
            raise JournalRefusal("integration ref contradicts landing window")


def _validate_git_evidence_shape(evidence: Mapping[str, Any]) -> GitEvidence:
    """Return one fully typed R1 evidence receipt after shape validation."""

    # Require the complete ticket/window, candidate, and trailer evidence set.
    required = {
        "ticket",
        "landing_sequence",
        "integration_ref_head",
        "candidate_commit",
        "candidate_reachable",
        "candidate_tree",
        "test_blobs",
        "expected_trailers",
        "observed_trailers",
    }
    if set(evidence) != required:
        raise JournalRefusal("Git evidence fields are incomplete")
    ticket = evidence["ticket"]
    landing_sequence = evidence["landing_sequence"]

    # Validate the durable window selector before consulting the event log.
    if (
        not isinstance(ticket, str)
        or not TICKET_REFERENCE_PATTERN.fullmatch(ticket)
        or not isinstance(landing_sequence, int)
        or isinstance(landing_sequence, bool)
        or landing_sequence < 1
    ):
        raise JournalRefusal("Git evidence landing identity is invalid")

    # Candidate identities are mandatory in previous and advanced states.
    if (
        not isinstance(evidence["integration_ref_head"], str)
        or not OBJECT_ID_PATTERN.fullmatch(evidence["integration_ref_head"])
        or not isinstance(evidence["candidate_commit"], str)
        or not OBJECT_ID_PATTERN.fullmatch(evidence["candidate_commit"])
        or not isinstance(evidence["candidate_reachable"], bool)
        or not isinstance(evidence["candidate_tree"], str)
        or not OBJECT_ID_PATTERN.fullmatch(evidence["candidate_tree"])
    ):
        raise JournalRefusal("Git evidence has invalid candidate fields")
    _validate_blob_map(cast(JsonValue, evidence["test_blobs"]), "test_blobs")

    # Both expected and observed maps carry the complete fixed R1 trailer pair.
    for field in ("expected_trailers", "observed_trailers"):
        trailers = evidence[field]
        if (
            not isinstance(trailers, dict)
            or set(trailers) != {"Kntnt-Ticket", "Kntnt-Plan"}
            or any(not isinstance(value, str) for value in trailers.values())
        ):
            raise JournalRefusal(f"Git evidence {field} is invalid")
    return cast(GitEvidence, dict(evidence))


def _validate_archive_readiness(
    events: list[dict[str, JsonValue]], projection: dict[str, JsonValue]
) -> None:
    """Require every terminal-specific completion boundary before archiving."""

    projected_tickets = projection["tickets"]
    if not isinstance(projected_tickets, dict):
        raise JournalRefusal("archive projection has no ticket account")
    for ticket, projected in projected_tickets.items():
        if not isinstance(projected, dict):
            raise JournalRefusal(f"archive projection for {ticket} is malformed")
        terminal_value = projected.get("terminal")
        try:
            terminal = TerminalState(cast(str, terminal_value))
        except (TypeError, ValueError) as error:
            raise JournalRefusal(
                f"archive requires terminal state for {ticket}"
            ) from error
        tail = _events_after_latest_terminal(ticket, events)
        _validate_terminal_prerequisites(ticket, terminal, tail, "archive")


def _compact_archive_receipt(
    metadata: dict[str, JsonValue],
    events: list[dict[str, JsonValue]],
    projection: dict[str, JsonValue],
    final_event_sha256: JsonValue,
) -> dict[str, JsonValue]:
    """Build the prescribed audit receipt without retired executor bulk."""

    # Each ticket keeps compiled identities, routed attempts, reviews, and the
    # terminal receipt needed for audit and later knowledge closure.
    ticket_receipts: dict[str, JsonValue] = {}
    retained_references: dict[str, dict[str, JsonValue]] = {}
    projected_tickets = cast(dict[str, JsonValue], projection["tickets"])
    for ticket in cast(list[str], metadata["selection"]):
        ticket_events = [event for event in events if event["ticket"] == ticket]
        bundle = _latest_payload(ticket_events, EventType.BUNDLE_CONSUMED)
        routes: list[JsonValue] = [
            cast(dict[str, JsonValue], event["payload"])
            for event in ticket_events
            if _event_type(event) is EventType.ROUTE_RECORDED
        ]
        rehydrations: list[JsonValue] = [
            cast(dict[str, JsonValue], event["payload"])
            for event in ticket_events
            if _event_type(event) is EventType.EXECUTOR_REHYDRATED
        ]
        reviews: list[JsonValue] = [
            cast(dict[str, JsonValue], event["payload"])
            for event in ticket_events
            if _event_type(event) is EventType.REVIEW_COMPLETED
        ]
        terminal_event = next(
            (
                event
                for event in reversed(ticket_events)
                if _event_type(event)
                in {EventType.LANDED, EventType.PARKED, EventType.STRANDED}
            ),
            None,
        )
        if terminal_event is None:
            raise JournalRefusal(f"archive receipt has no terminal event for {ticket}")
        retained_patch = _retained_parked_patch(ticket_events, terminal_event)
        if retained_patch is not None:
            retained_references[cast(str, retained_patch["path"])] = retained_patch
        projected_ticket = cast(dict[str, JsonValue], projected_tickets[ticket])
        ticket_receipts[ticket] = {
            "terminal": _event_type(terminal_event).value,
            "bundle": bundle,
            "route_decisions": routes,
            "rehydrations": rehydrations,
            "continuation": projected_ticket["continuation"],
            "reviews": reviews,
            "bundle_release": _latest_payload(ticket_events, EventType.BUNDLE_RELEASED),
            "terminal_receipt": terminal_event["payload"],
            "retained_patch": retained_patch,
        }

    # Observation inputs intentionally live beside the archive for the owner's
    # separate model-selector record action.
    observations: list[JsonValue] = []
    for event in events:
        if _event_type(event) is not EventType.OBSERVATION_RECORDED:
            continue
        reference = cast(dict[str, JsonValue], event["artifacts"])["observation-input"]
        observations.append(reference)
        typed_reference = cast(dict[str, JsonValue], reference)
        retained_references[cast(str, typed_reference["path"])] = typed_reference

    return {
        "schema": SCHEMA,
        "repository": metadata["repository"],
        "integration_ref": metadata["integration_ref"],
        "opening_head": metadata["opening_head"],
        "opened_at": metadata["opened_at"],
        "run_fingerprint": metadata["run_fingerprint"],
        "invocation": metadata["invocation"],
        "instruction": metadata["instruction"],
        "selection": metadata["selection"],
        "at_once": metadata["at_once"],
        "route": metadata["route"],
        "event_count": projection["event_count"],
        "final_event_sha256": final_event_sha256,
        "tickets": ticket_receipts,
        "observations": observations,
        "retained_artifacts": cast(
            list[JsonValue],
            [retained_references[path] for path in sorted(retained_references)],
        ),
    }


def _validate_retained_artifacts(
    archive: Path, receipt: dict[str, JsonValue]
) -> set[str]:
    """Verify every retained byte against all receipt identity fields."""

    retained = receipt.get("retained_artifacts")
    tickets = receipt.get("tickets")
    observations = receipt.get("observations")
    if (
        not isinstance(retained, list)
        or not isinstance(tickets, dict)
        or not isinstance(observations, list)
    ):
        raise JournalRefusal("archive retained-artifact receipt is malformed")

    # Nested ticket and observation receipts prescribe the complete retained
    # set; the top-level list cannot silently omit or add an artifact.
    expected_by_path: dict[str, dict[str, JsonValue]] = {}

    def add_expected(reference: dict[str, JsonValue]) -> None:
        """Collect one nested reference while allowing identical deduplication."""

        path = reference.get("path")
        if not isinstance(path, str):
            raise JournalRefusal("archive retained-artifact path is malformed")
        previous = expected_by_path.setdefault(path, reference)
        if previous != reference:
            raise JournalRefusal("archive retained-artifact receipts conflict")

    for ticket_receipt in tickets.values():
        if not isinstance(ticket_receipt, dict):
            raise JournalRefusal("archive ticket receipt is malformed")
        patch = ticket_receipt.get("retained_patch")
        if patch is not None:
            if not isinstance(patch, dict):
                raise JournalRefusal("archive retained patch receipt is malformed")
            add_expected(patch)
    for observation in observations:
        if not isinstance(observation, dict):
            raise JournalRefusal("archive observation receipt is malformed")
        add_expected(observation)
    expected = [expected_by_path[path] for path in sorted(expected_by_path)]
    if retained != expected:
        raise JournalRefusal("archive retained-artifact set contradicts its receipt")

    # Validate containment, digest, and byte length before any retired bulk is
    # removed, so a missing or modified retained artifact is a clean refusal.
    paths: set[str] = set()
    for raw_reference in retained:
        if not isinstance(raw_reference, dict):
            raise JournalRefusal("archive retained-artifact entry is malformed")
        reference = raw_reference
        if set(reference) != {"path", "sha256", "byte_length"}:
            raise JournalRefusal("archive retained-artifact identity is incomplete")
        relative = reference["path"]
        digest = reference["sha256"]
        byte_length = reference["byte_length"]
        if (
            not isinstance(relative, str)
            or not relative.startswith("artifacts/")
            or not _is_relative_posix_path(relative)
            or relative in paths
            or not isinstance(digest, str)
            or not CONTENT_DIGEST_PATTERN.fullmatch(digest)
            or not isinstance(byte_length, int)
            or isinstance(byte_length, bool)
            or byte_length < 0
        ):
            raise JournalRefusal("archive retained-artifact identity is invalid")
        if not relative.endswith(digest.removeprefix("sha256:")):
            raise JournalRefusal("archive retained-artifact path contradicts digest")
        path = archive / relative
        if path.is_symlink() or not path.is_file():
            raise JournalRefusal(f"retained artifact is missing: {relative}")
        content = path.read_bytes()
        if digest != f"sha256:{sha256_hex(content)}" or byte_length != len(content):
            raise JournalRefusal(f"retained artifact identity changed: {relative}")
        paths.add(relative)
    return paths


def _latest_payload(
    events: list[dict[str, JsonValue]], event_type: EventType
) -> JsonValue:
    """Return the latest payload of one type, or null when none exists."""

    event = next(
        (event for event in reversed(events) if _event_type(event) is event_type),
        None,
    )
    return event["payload"] if event is not None else None


def _retained_parked_patch(
    events: list[dict[str, JsonValue]], terminal_event: dict[str, JsonValue]
) -> dict[str, JsonValue] | None:
    """Return only the latest patch selected by an R2 parked receipt."""

    if _event_type(terminal_event) is not EventType.PARKED:
        return None
    payload = cast(dict[str, JsonValue], terminal_event["payload"])
    sequence = payload["patch_sequence"]
    if sequence is None:
        return None
    patch = next(event for event in events if event["sequence"] == sequence)
    artifacts = cast(dict[str, JsonValue], patch["artifacts"])
    return cast(dict[str, JsonValue], artifacts["patch"])


def _read_json_object(path: Path) -> dict[str, Any]:
    """Read one command input as a JSON object."""

    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as error:
        raise JournalRefusal(f"cannot read JSON object from {path}") from error
    if not isinstance(value, dict):
        raise JournalRefusal(f"JSON input is not an object: {path}")
    return cast(dict[str, Any], value)


def _read_json_array(path: Path) -> list[dict[str, Any]]:
    """Read one command input as an array of JSON objects."""

    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as error:
        raise JournalRefusal(f"cannot read JSON array from {path}") from error
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise JournalRefusal(f"JSON input is not an object array: {path}")
    return cast(list[dict[str, Any]], value)


def _parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse the small persistence interface used by the dispatch Skill."""

    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)

    # Every operation replays the opening, which prevents a caller from
    # attaching to a branch slot under a different invocation.
    for name in ("open", "validate", "project", "record", "archive"):
        command = commands.add_parser(name)
        command.add_argument("--root", required=True, type=Path)
        command.add_argument("--opening", required=True, type=Path)

    commands.choices["project"].add_argument("--evidence", type=Path)
    commands.choices["record"].add_argument("--event", required=True, type=Path)
    return parser.parse_args(argv)


def _emit(value: Any, *, stream: Any = sys.stdout) -> None:
    """Emit one machine-readable response with a conventional trailing LF."""

    stream.buffer.write(canonical_json(value) + b"\n")


def main(argv: list[str] | None = None) -> int:
    """Execute one journal operation and return a stable process status."""

    args = _parse_args(argv if argv is not None else sys.argv[1:])
    try:
        # Opening every command makes active-slot identity one shared guard.
        opening = _read_json_object(args.opening)
        journal = Journal.open(args.root, opening)
        if args.command == "open":
            _emit({"path": str(journal.path), "metadata": journal.metadata})
        elif args.command == "validate":
            _emit(journal.validate())
        elif args.command == "project":
            evidence = _read_json_array(args.evidence) if args.evidence else None
            _emit(journal.project(git_evidence=evidence))
        elif args.command == "record":
            event = _read_json_object(args.event)
            event_type = event.get("type")
            ticket = event.get("ticket")
            payload = event.get("payload", {})
            recorded_at = event.get("recorded_at")
            artifact_paths = event.get("artifacts", {})
            if not isinstance(event_type, str):
                raise JournalRefusal("event type must be a string")
            if ticket is not None and not isinstance(ticket, str):
                raise JournalRefusal("event ticket must be a string or null")
            if not isinstance(payload, dict):
                raise JournalRefusal("event payload must be an object")
            if recorded_at is not None and not isinstance(recorded_at, str):
                raise JournalRefusal("event recorded_at must be a string or null")
            if not isinstance(artifact_paths, dict) or any(
                not isinstance(kind, str) or not isinstance(path, str)
                for kind, path in artifact_paths.items()
            ):
                raise JournalRefusal("event artifacts must map kinds to file paths")
            artifacts = {
                kind: Path(path).read_bytes() for kind, path in artifact_paths.items()
            }
            _emit(
                journal.record(
                    event_type,
                    ticket=ticket,
                    payload=payload,
                    artifacts=artifacts,
                    recorded_at=recorded_at,
                )
            )
        else:
            _emit({"archive": str(journal.archive())})
        return 0
    except (JournalRefusal, OSError) as error:
        # Refusals are data, not tracebacks; the caller owns the next action.
        _emit({"refusal": str(error)}, stream=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
