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
from pathlib import Path
from typing import Any, Final, cast

type JsonValue = None | bool | int | str | list[JsonValue] | dict[str, JsonValue]

SCHEMA: Final = "kntnt.dispatch-journal/v1"
SAFE_INTEGER_LIMIT: Final = 9_007_199_254_740_991
OPENING_KEYS: Final = {
    "repository",
    "integration_ref",
    "opening_head",
    "invocation",
    "instruction",
    "selection",
    "at_once",
    "route",
}
EVENT_TYPES: Final = frozenset(
    {
        "selection-recorded",
        "bundle-consumed",
        "bundle-released",
        "route-recorded",
        "ticket-assigned",
        "attempt-started",
        "attempt-returned",
        "patch-captured",
        "dispatcher-write-recorded",
        "review-completed",
        "revise-requested",
        "rebuild-requested",
        "owner-answered",
        "landing-started",
        "human-conflict",
        "landed",
        "parked",
        "stranded",
        "tracker-transition-planned",
        "tracker-transition-completed",
        "bundle-retired",
        "resource-cleaned",
        "observation-recorded",
        "run-completed",
    }
)
TRANSITION_IDS: Final = frozenset({"T-LAND", "T-PARK-INFO", "T-PARK-HUMAN"})
TERMINAL_TYPES: Final = frozenset({"landed", "parked", "stranded"})
ARTIFACT_KIND = re.compile(r"^[a-z][a-z0-9-]*$")
TICKET = re.compile(r"^#[1-9][0-9]*$")
OBJECT_ID = re.compile(r"^[0-9a-f]{40,64}$")
UTC_INSTANT = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?Z$"
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
    if not isinstance(opening["opening_head"], str) or not OBJECT_ID.fullmatch(
        opening["opening_head"]
    ):
        raise JournalRefusal("opening opening_head must be a full lowercase object ID")

    # Keep selection and concurrency mechanically unambiguous.
    selection = opening["selection"]
    if not isinstance(selection, list) or not selection:
        raise JournalRefusal("opening selection must be a non-empty ordered array")
    if any(
        not isinstance(ticket, str) or not TICKET.fullmatch(ticket)
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

    if not UTC_INSTANT.fullmatch(value):
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

    def __init__(self, root: Path, path: Path, metadata: dict[str, JsonValue]) -> None:
        """Bind an already published active slot to its immutable metadata."""

        self.root = root
        self.path = path
        self.metadata = metadata

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
    def _load(cls, root: Path, slot: Path) -> Journal:
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
        return cls(root, slot, cast(dict[str, JsonValue], value))

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
        if event_type not in EVENT_TYPES:
            raise JournalRefusal(f"unknown event type: {event_type}")
        if ticket is not None and not TICKET.fullmatch(ticket):
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
                event_type, ticket, normalized_payload, prior_events
            )
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
                "type": event_type,
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
        self, *, evidence: Mapping[str, Any] | None = None
    ) -> dict[str, JsonValue]:
        """Project run and ticket recovery state without mutating the journal.

        Raises:
            JournalRefusal: Supplied external evidence contradicts a durable fact.
        """

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

        # External tools stay outside this module; exact observations may only
        # confirm the requirements durable events already carry.
        if evidence is not None:
            normalized_evidence = _normalize_json(dict(evidence), "$.evidence", set())
            for ticket, projection in tickets.items():
                required = cast(dict[str, JsonValue], projection["required_evidence"])
                for key, expected in required.items():
                    if (
                        not isinstance(normalized_evidence, dict)
                        or normalized_evidence.get(key) != expected
                    ):
                        raise JournalRefusal(
                            f"contradictory external evidence for {ticket}: {key}"
                        )

        # Recovery actions depend only on durable milestones, never chronology
        # remembered by the invoking session.
        for projection in tickets.values():
            projection["recovery_action"] = _recovery_action(projection)

        # Completion is contradictory until every selected ticket is terminal.
        completed = any(event["type"] == "run-completed" for event in events)
        if completed and any(
            projection["terminal"] not in TERMINAL_TYPES
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
        """Atomically replace a completed active slot with its archive."""

        with _exclusive_lock(self.path / ".write.lock"):
            # Completion must already be durable and every selected ticket must
            # have an exact terminal state before the active name can vanish.
            state = self._read_validated()
            events = cast(list[dict[str, JsonValue]], state["events"])
            if not events or events[-1]["type"] != "run-completed":
                raise JournalRefusal("archive requires a final run-completed event")
            projection = self.project()
            tickets = cast(dict[str, dict[str, JsonValue]], projection["tickets"])
            if any(
                ticket["terminal"] not in TERMINAL_TYPES for ticket in tickets.values()
            ):
                raise JournalRefusal(
                    "archive requires every selected ticket to be terminal"
                )

            # The receipt preserves audit identities without asking path digests
            # or the retired executor bundle to explain the completed run.
            receipt: dict[str, JsonValue] = {
                "schema": SCHEMA,
                "repository": self.metadata["repository"],
                "integration_ref": self.metadata["integration_ref"],
                "opening_head": self.metadata["opening_head"],
                "opened_at": self.metadata["opened_at"],
                "run_fingerprint": self.metadata["run_fingerprint"],
                "invocation": self.metadata["invocation"],
                "instruction": self.metadata["instruction"],
                "selection": self.metadata["selection"],
                "at_once": self.metadata["at_once"],
                "route": self.metadata["route"],
                "event_count": projection["event_count"],
                "final_event_sha256": state["last_event_sha256"],
                "tickets": cast(dict[str, JsonValue], tickets),
            }
            _atomic_publish(self.path / "receipt.json", canonical_json(receipt))

            # Path punctuation is removed while the fingerprint remains exact.
            opened = cast(str, self.metadata["opened_at"])
            archive_name = f"{opened.replace('-', '').replace(':', '')}-{cast(str, self.metadata['run_fingerprint']).removeprefix('sha256:')}"
            archive = self.root / "archive" / archive_name
            if archive.exists():
                raise JournalRefusal("archive destination already exists")
            os.replace(self.path, archive)
            _flush_directory(self.path.parent)
            _flush_directory(archive.parent)
            return archive

    def _store_artifact(self, kind: str, content: bytes) -> dict[str, JsonValue]:
        """Publish one content-addressed artifact and return its receipt."""

        if not ARTIFACT_KIND.fullmatch(kind):
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
            if event["type"] == "selection-recorded":
                payload = cast(dict[str, JsonValue], event["payload"])
                if payload.get("tickets") != metadata["selection"]:
                    raise JournalRefusal("selection event contradicts opening metadata")
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
            if not ARTIFACT_KIND.fullmatch(kind) or not isinstance(value, dict):
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
    if not isinstance(event["type"], str) or event["type"] not in EVENT_TYPES:
        raise JournalRefusal(f"event {sequence} has an unknown type")
    if not isinstance(event["recorded_at"], str):
        raise JournalRefusal(f"event {sequence} has no recorded instant")
    _validate_instant(event["recorded_at"], f"event {sequence} recorded_at")
    if event["ticket"] is not None and (
        not isinstance(event["ticket"], str) or not TICKET.fullmatch(event["ticket"])
    ):
        raise JournalRefusal(f"event {sequence} has an invalid ticket")
    if not isinstance(event["payload"], dict):
        raise JournalRefusal(f"event {sequence} payload is not an object")
    _validate_event_payload(
        event["type"], event["ticket"], event["payload"], prior_events
    )


def _validate_event_payload(
    event_type: str,
    ticket: str | None,
    payload: dict[str, JsonValue],
    prior_events: list[dict[str, JsonValue]],
) -> None:
    """Validate the receipts whose exact fields affect safe recovery."""

    # Run-wide events are the only events allowed to omit a ticket identity.
    if event_type not in {"selection-recorded", "run-completed"} and ticket is None:
        raise JournalRefusal(f"{event_type} requires a ticket")
    if any(event["type"] == "run-completed" for event in prior_events):
        raise JournalRefusal("no event may follow run-completed")

    if event_type == "tracker-transition-planned":
        _validate_transition_plan(ticket, payload)
        expected_terminal = (
            "landed" if payload["transition_id"] == "T-LAND" else "parked"
        )
        if not any(
            event["ticket"] == ticket and event["type"] == expected_terminal
            for event in prior_events
        ):
            raise JournalRefusal(
                f"tracker transition requires prior {expected_terminal} state"
            )
    elif event_type == "tracker-transition-completed":
        _validate_transition_completion(ticket, payload, prior_events)
    elif event_type == "bundle-retired" and not any(
        event["ticket"] == ticket and event["type"] == "tracker-transition-completed"
        for event in prior_events
    ):
        raise JournalRefusal("bundle retirement requires tracker completion")


def _validate_transition_plan(
    ticket: str | None, payload: dict[str, JsonValue]
) -> None:
    """Validate a concrete pre-mutation tracker transition receipt."""

    if set(payload) != {"transition_id", "resolution", "pre_projection"}:
        raise JournalRefusal("tracker-transition-planned has incomplete fields")
    transition_id = payload["transition_id"]
    resolution = payload["resolution"]
    pre = payload["pre_projection"]
    if (
        not isinstance(transition_id, str)
        or transition_id not in TRANSITION_IDS
        or not isinstance(resolution, dict)
        or not isinstance(pre, dict)
    ):
        raise JournalRefusal("tracker-transition-planned has invalid field types")
    _validate_resolution(transition_id, resolution, pre)


def _validate_resolution(
    transition_id: str,
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
    if transition_id == "T-LAND":
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
    if planned["type"] != "tracker-transition-planned" or planned["ticket"] != ticket:
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
        "bundle_consumed": False,
        "route_recorded": False,
        "assigned": False,
        "attempt_started": False,
        "patch_captured": False,
        "review_completed": False,
        "revision_requested": False,
        "rebuild_requested": False,
        "landing_started": False,
        "human_conflict": False,
        "tracker_transition_completed": False,
        "bundle_retired": False,
        "resource_cleaned": False,
        "required_evidence": {},
        "receipts": {},
        "recovery_action": "start-ticket",
    }


def _apply_event(projection: dict[str, JsonValue], event: dict[str, JsonValue]) -> None:
    """Apply one validated event to a ticket's recovery projection."""

    event_type = cast(str, event["type"])
    projection["last_event"] = event_type
    receipts = cast(dict[str, JsonValue], projection["receipts"])
    event_receipts = cast(list[JsonValue], receipts.setdefault(event_type, []))
    event_receipts.append(
        {
            "sequence": event["sequence"],
            "payload": event["payload"],
            "artifacts": event["artifacts"],
        }
    )
    flags = {
        "bundle-consumed": "bundle_consumed",
        "route-recorded": "route_recorded",
        "ticket-assigned": "assigned",
        "attempt-started": "attempt_started",
        "patch-captured": "patch_captured",
        "review-completed": "review_completed",
        "revise-requested": "revision_requested",
        "rebuild-requested": "rebuild_requested",
        "landing-started": "landing_started",
        "human-conflict": "human_conflict",
        "tracker-transition-completed": "tracker_transition_completed",
        "bundle-retired": "bundle_retired",
        "resource-cleaned": "resource_cleaned",
    }
    if event_type in flags:
        projection[flags[event_type]] = True
    if event_type in TERMINAL_TYPES and projection["terminal"] not in {
        None,
        event_type,
    }:
        raise JournalRefusal("ticket has contradictory terminal events")
    if event_type in TERMINAL_TYPES:
        projection["terminal"] = event_type
    payload = cast(dict[str, JsonValue], event["payload"])
    required = payload.get("required_evidence")
    if required is not None:
        if not isinstance(required, dict):
            raise JournalRefusal(f"{event_type} required_evidence is not an object")
        cast(dict[str, JsonValue], projection["required_evidence"]).update(required)


def _recovery_action(projection: dict[str, JsonValue]) -> str:
    """Map durable ticket milestones to one approved recovery action."""

    terminal = projection["terminal"]
    if terminal == "stranded" and not projection["resource_cleaned"]:
        return "clean-stranded"
    if (
        terminal in {"landed", "parked"}
        and not projection["tracker_transition_completed"]
    ):
        return "complete-tracker-transition"
    if projection["tracker_transition_completed"] and (
        not projection["bundle_retired"] or not projection["resource_cleaned"]
    ):
        return "retire-and-clean"
    if projection["human_conflict"] and terminal is None:
        return "resume-human-conflict"
    if projection["rebuild_requested"] and terminal is None:
        return "await-recompile"
    if projection["landing_started"] and terminal is None:
        return "reconcile-landing"
    if projection["revision_requested"] and terminal is None:
        return "resume-revision"
    if projection["patch_captured"] and not projection["review_completed"]:
        return "review-patch"
    if projection["attempt_started"] and not projection["patch_captured"]:
        return "replay-attempt"
    if terminal is not None:
        return "complete"
    if projection["bundle_consumed"]:
        return "continue-ticket"
    return "start-ticket"


def _read_json_object(path: Path) -> dict[str, Any]:
    """Read one command input as a JSON object."""

    try:
        value = json.loads(path.read_bytes())
    except (OSError, json.JSONDecodeError) as error:
        raise JournalRefusal(f"cannot read JSON object from {path}") from error
    if not isinstance(value, dict):
        raise JournalRefusal(f"JSON input is not an object: {path}")
    return cast(dict[str, Any], value)


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
            evidence = _read_json_object(args.evidence) if args.evidence else None
            _emit(journal.project(evidence=evidence))
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
