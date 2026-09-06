"""Unattended source refresh shipped by the model-selector Skill."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import UTC, datetime
from email.message import Message
from pathlib import Path
from typing import Any, Self, cast

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
MODEL_SELECTOR: Path = REPO_ROOT / "skills" / "models" / "model-selector"
REFRESH: Path = MODEL_SELECTOR / "scripts" / "refresh.py"
CAPTURE: Path = MODEL_SELECTOR / "scripts" / "capture.py"
CADENCES: Path = MODEL_SELECTOR / "data" / "refresh-cadences.json"

NOW = datetime(2026, 9, 5, 12, 0, 0, tzinfo=UTC)

# A retrieval recent enough that a weekly cadence has not elapsed by `NOW`.
STILL_FRESH = "2026-09-04T12:00:00Z"


def _sibling(stem: str) -> Any:
    """Load one engine module under the plain name its siblings import it by."""

    if stem in sys.modules:
        return sys.modules[stem]
    spec = importlib.util.spec_from_file_location(
        stem, MODEL_SELECTOR / "scripts" / f"{stem}.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[stem] = module
    spec.loader.exec_module(module)
    return module


def _load(path: Path = REFRESH) -> Any:
    """Load one shipped module from its installed path.

    Registered under its own name before it executes, exactly as the shipped
    loader in `capture.py` does it: a module whose dataclasses declare string
    annotations has to be findable by name while its classes are being built.
    Its siblings are registered first, in dependency order, so that the plain
    imports it makes resolve to the same objects these tests hold.
    """

    for stem in ("catalogue", "profiles", "evidence", "launch"):
        _sibling(stem)

    name = f"model_selector_{path.stem}"
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _row(**overrides: Any) -> dict[str, Any]:
    """Provide one `SourceState` row in the shape `update` writes it."""

    base: dict[str, Any] = {
        "record_type": "SourceState",
        "source_key": "sha256:one",
        "uri": "https://example.invalid/models",
        "provider": "example",
        "kind": "model_release_index",
        "status": "unchanged",
        "etag": None,
        "last_modified": None,
        "content_hash": None,
        "last_checked_at": None,
        "last_retrieved_at": None,
        "last_changed_at": None,
        "parser_version": "models/1",
        "finding": "Weekly cadence. Nothing new.",
    }
    return {**base, **overrides}


def _store(tmp_path: Path, *rows: dict[str, Any]) -> Path:
    """Write one source-state store and return the data directory holding it."""

    data = tmp_path / "data"
    data.mkdir(exist_ok=True)
    text = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    (data / "source-states.jsonl").write_text(text, encoding="utf-8")
    return data


def _rows(data: Path) -> list[dict[str, Any]]:
    """Return every row the source-state store under *data* now holds."""

    text = (data / "source-states.jsonl").read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def _reached(module: Any, recorded: list[tuple[str, float]]) -> Any:
    """Provide a retrieval that records what it was asked and answers changed."""

    def retrieve(
        uri: str, etag: str | None, last_modified: str | None, timeout: float
    ) -> Any:
        recorded.append((uri, timeout))
        return module.Retrieved(
            modified=True,
            etag='W/"new"',
            last_modified=None,
            content_hash="sha256:fresh",
        )

    return retrieve


def _unreachable(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
    """Provide a retrieval that answers as a source nothing could reach."""

    return None


def _never(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
    """Provide a retrieval that fails the test if the pass ever calls it."""

    raise AssertionError(f"the pass retrieved {uri}, which it may never do")


def test_the_refresh_module_reaches_the_network_and_nothing_further() -> None:
    """What the unattended pass may do is provable from what it can reach.

    ADR-0179's hook path is narrowed in exactly one phrase: this
    module may retrieve metadata conditionally, under a budget. Everything
    else that record protects is unchanged, so a module that cannot start a
    process, cannot start a thread, and holds no waiting call cannot break it
    however it is invoked.
    """

    source = REFRESH.read_text(encoding="utf-8")

    assert "import urllib.request" in source
    for unreachable in (
        "import subprocess",
        "import threading",
        "import asyncio",
        "import socket",
        "import requests",
        "time.sleep",
        "anthropic",
        "openai",
    ):
        assert unreachable not in source, unreachable


def test_the_cadences_are_shipped_data_rather_than_prose() -> None:
    """Every documented source kind carries its cadence where code reads it."""

    shipped = json.loads(CADENCES.read_text(encoding="utf-8"))

    assert set(shipped["cadences"]) == {
        "model_release_index",
        "model_detail",
        "capability_source",
        "benchmark_release_index",
        "commercial_terms",
        "gateway_rate_card",
    }
    assert shipped["cadences"]["model_release_index"] == "P7D"
    assert shipped["cadences"]["benchmark_release_index"] == "P1M"

    # An immutable detail page is never refetched, so it never becomes due.
    assert shipped["cadences"]["model_detail"] is None


def test_the_budget_is_two_seconds_across_the_whole_pass() -> None:
    """The number the record states is the number the module carries."""

    assert _load().BUDGET_SECONDS == 2.0


def test_a_machine_with_no_source_states_writes_nothing_and_retrieves_nothing(
    tmp_path: Path,
) -> None:
    """A pass with nothing to iterate does nothing, and says so to `status`."""

    module = _load()
    data = tmp_path / "data"
    data.mkdir()

    answered = module.refresh(data, now=NOW, retrieve=_never)

    assert answered["established"] is False
    assert answered["considered"] == 0
    assert list(data.iterdir()) == []
    assert module.status(data)["established"] is False


def test_a_source_never_retrieved_is_due_whatever_its_check_says(
    tmp_path: Path,
) -> None:
    """Cadence is measured from the retrieval timestamp and from nothing else.

    Every row on a machine that has run `update` is in exactly this state:
    `last_retrieved_at` is a field this ticket adds, so it is absent, and the
    retrieval date lives only in `finding` prose nothing parses.
    """

    data = _store(
        tmp_path,
        _row(last_checked_at="2026-09-05T11:00:00Z", last_retrieved_at=None),
    )
    module = _load()
    reached: list[tuple[str, float]] = []

    module.refresh(data, now=NOW, retrieve=_reached(module, reached))

    assert [uri for uri, _ in reached] == ["https://example.invalid/models"]
    assert _rows(data)[0]["last_retrieved_at"] == "2026-09-05T12:00:00Z"


def test_a_recently_retrieved_source_is_stamped_checked_and_left_alone(
    tmp_path: Path,
) -> None:
    """A not-due source records the look, never the retrieval."""

    data = _store(
        tmp_path,
        _row(last_retrieved_at="2026-09-03T12:00:00Z", status="changed"),
    )

    _load().refresh(data, now=NOW, retrieve=_never)

    row = _rows(data)[0]
    assert row["status"] == "not_due"
    assert row["last_checked_at"] == "2026-09-05T12:00:00Z"
    assert row["last_retrieved_at"] == "2026-09-03T12:00:00Z"


def test_stamping_the_check_never_moves_the_next_due_date(tmp_path: Path) -> None:
    """The defect this ticket exists to fix is not reinstalled by its own fix.

    Cadence measured from the last look would push every source's due date
    forward at every session end, and nothing would ever become due again.
    """

    module = _load()
    data = _store(tmp_path, _row(last_retrieved_at="2026-08-25T12:00:00Z"))

    for _ in range(3):
        module.refresh(data, now=NOW, retrieve=_unreachable)

    assert _rows(data)[0]["last_checked_at"] == "2026-09-05T12:00:00Z"
    assert module.status(data, now=NOW)["counts"]["unattended_due"] == 1


def test_a_price_bearing_source_is_now_retrieved_like_any_other(
    tmp_path: Path,
) -> None:
    """The rule that a pass may learn what a model can do but never what it
    costs is reversed (ADR-0182).

    A rate card is exactly what this Skill has to be current about, and what
    bounds the pass is attribution and a budget rather than a category of fact
    it is forbidden to look at.
    """

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:terms", kind="commercial_terms"),
        _row(source_key="sha256:card", kind="gateway_rate_card"),
    )
    reached: list[tuple[str, float]] = []

    answered = module.refresh(data, now=NOW, retrieve=_reached(module, reached))

    assert len(reached) == 2
    assert answered["skipped"]["manual"] == 0
    assert [row["last_retrieved_at"] for row in _rows(data)] == [
        "2026-09-05T12:00:00Z"
    ] * 2


def test_an_unrecognised_kind_is_left_to_the_user(tmp_path: Path) -> None:
    """Fail closed, so a kind added later is safe on the day it appears."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:new", kind="provider_incident_feed"),
        _row(source_key="sha256:none", kind=None),
        _row(source_key="sha256:gone", kind="model_release_index", uri=None),
    )
    before = (data / "source-states.jsonl").read_bytes()

    answered = module.refresh(data, now=NOW, retrieve=_never)

    assert (data / "source-states.jsonl").read_bytes() == before
    assert answered["skipped"]["manual"] == 3


def test_a_uri_that_is_not_http_is_never_opened(tmp_path: Path) -> None:
    """A store a user may hand-edit cannot make this pass open a local file."""

    module = _load()
    data = _store(tmp_path, _row(uri="file:///etc/passwd"))
    before = (data / "source-states.jsonl").read_bytes()

    module.refresh(data, now=NOW, retrieve=_never)

    assert (data / "source-states.jsonl").read_bytes() == before


def test_a_source_that_could_not_be_reached_records_the_look_and_nothing_else(
    tmp_path: Path,
) -> None:
    """A failed retrieval changes no fact and leaves the source due."""

    module = _load()
    data = _store(tmp_path, _row(status="unchanged", content_hash="sha256:stale"))

    answered = module.refresh(data, now=NOW, retrieve=_unreachable)

    row = _rows(data)[0]
    assert row["last_checked_at"] == "2026-09-05T12:00:00Z"
    assert row["last_retrieved_at"] is None
    assert row["status"] == "unchanged"
    assert row["content_hash"] == "sha256:stale"
    assert answered["skipped"]["unreachable"] == 1
    assert module.status(data, now=NOW)["counts"]["unattended_due"] == 1


def test_an_unchanged_source_keeps_the_instant_its_content_last_moved(
    tmp_path: Path,
) -> None:
    """A validator that proves sameness records a retrieval and no change."""

    module = _load()
    data = _store(
        tmp_path,
        _row(etag='W/"old"', last_changed_at="2026-08-01T00:00:00Z"),
    )

    def retrieve(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
        assert etag == 'W/"old"'
        return module.Retrieved(
            modified=False, etag=None, last_modified=None, content_hash=None
        )

    module.refresh(data, now=NOW, retrieve=retrieve)

    row = _rows(data)[0]
    assert row["status"] == "unchanged"
    assert row["last_retrieved_at"] == "2026-09-05T12:00:00Z"
    assert row["last_changed_at"] == "2026-08-01T00:00:00Z"
    assert row["etag"] == 'W/"old"'


def test_a_changed_source_records_that_it_moved_and_interprets_nothing(
    tmp_path: Path,
) -> None:
    """The pass establishes that something moved; a typed `update` says what."""

    module = _load()
    data = _store(tmp_path, _row(content_hash="sha256:stale"))

    module.refresh(data, now=NOW, retrieve=_reached(module, []))

    row = _rows(data)[0]
    assert row["status"] == "changed"
    assert row["last_changed_at"] == "2026-09-05T12:00:00Z"
    assert row["content_hash"] == "sha256:fresh"

    # Nothing the pass writes is a judgement: the prose and the parser the
    # typed `update` recorded are left exactly as that pass wrote them.
    assert row["finding"] == "Weekly cadence. Nothing new."
    assert row["parser_version"] == "models/1"


def test_a_typed_updates_unresolved_diagnostic_survives_a_look(
    tmp_path: Path,
) -> None:
    """This pass reads no source, so it can clear no reading of one.

    `unreachable` and `invalid` are the typed `update`'s conclusions. A pass
    that overwrote either with `not_due` would erase, at the next session end,
    exactly the thing `status` exists to keep in front of the user.
    """

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:bad", status="invalid", last_retrieved_at=STILL_FRESH),
        _row(
            source_key="sha256:out", status="unreachable", last_retrieved_at=STILL_FRESH
        ),
    )

    module.refresh(data, now=NOW, retrieve=_never)

    rows = _rows(data)
    assert [row["status"] for row in rows] == ["invalid", "unreachable"]
    assert [row["last_checked_at"] for row in rows] == ["2026-09-05T12:00:00Z"] * 2


def test_an_unchanged_retrieval_does_not_clear_a_diagnostic_either(
    tmp_path: Path,
) -> None:
    """The same bytes a typed `update` could not read are still unreadable."""

    module = _load()
    data = _store(tmp_path, _row(status="invalid", content_hash="sha256:same"))

    def retrieve(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
        return module.Retrieved(
            modified=True, etag=None, last_modified=None, content_hash="sha256:same"
        )

    module.refresh(data, now=NOW, retrieve=retrieve)

    row = _rows(data)[0]
    assert row["status"] == "invalid"
    assert row["last_retrieved_at"] == "2026-09-05T12:00:00Z"


def test_content_that_actually_moved_supersedes_a_diagnostic(tmp_path: Path) -> None:
    """A diagnostic about content that no longer exists is answered by the move."""

    module = _load()
    data = _store(tmp_path, _row(status="invalid", content_hash="sha256:stale"))

    module.refresh(data, now=NOW, retrieve=_reached(module, []))

    assert _rows(data)[0]["status"] == "changed"


def test_the_pass_writes_source_states_and_no_other_file(tmp_path: Path) -> None:
    """No capability fact, no benchmark fact, no evidence record, no frontier."""

    module = _load()
    data = _store(tmp_path, _row())

    module.refresh(data, now=NOW, retrieve=_reached(module, []))

    assert [path.name for path in data.iterdir()] == ["source-states.jsonl"]


def test_rows_are_updated_in_place_and_nothing_is_appended(tmp_path: Path) -> None:
    """The live store holds one row per source, with no superseding history."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:one"),
        _row(source_key="sha256:two", uri="https://example.invalid/bench"),
    )

    for _ in range(3):
        module.refresh(data, now=NOW, retrieve=_reached(module, []))

    rows = _rows(data)
    assert [row["source_key"] for row in rows] == ["sha256:one", "sha256:two"]


def test_a_row_the_store_cannot_parse_is_left_alone_and_counted(
    tmp_path: Path,
) -> None:
    """An unreadable row is treated as commercial and never rewritten."""

    module = _load()
    data = _store(tmp_path, _row())
    path = data / "source-states.jsonl"
    path.write_text(path.read_text(encoding="utf-8") + "{not json\n", encoding="utf-8")

    answered = module.refresh(data, now=NOW, retrieve=_unreachable)

    # The line survives verbatim: a row this pass cannot read is a row it
    # cannot reshape by reading it and writing it back.
    assert path.read_text(encoding="utf-8").splitlines()[-1] == "{not json"
    assert answered["counts"]["unreadable"] == 1


def test_the_budget_stops_the_pass_and_leaves_the_rest_due(tmp_path: Path) -> None:
    """One connection at a time, no retries, and a total budget for the pass."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:one", uri="https://example.invalid/a"),
        _row(source_key="sha256:two", uri="https://example.invalid/b"),
        _row(source_key="sha256:three", uri="https://example.invalid/c"),
    )
    asked: list[str] = []

    def slow(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
        asked.append(uri)
        assert timeout <= 0.1
        time.sleep(0.12)
        return module.Retrieved(
            modified=True, etag=None, last_modified=None, content_hash="sha256:fresh"
        )

    answered = module.refresh(data, now=NOW, budget_seconds=0.1, retrieve=slow)

    assert asked == ["https://example.invalid/a"]
    assert answered["skipped"]["budget_exhausted"] == 2
    assert [row["last_retrieved_at"] for row in _rows(data)[1:]] == [None, None]


def test_status_names_the_command_that_resolves_a_source_it_may_not_fetch(
    tmp_path: Path,
) -> None:
    """A kind nobody has taught this pass about is not fetched; it is reported."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:new", kind="provider_incident_feed"),
        _row(source_key="sha256:ok", last_retrieved_at="2026-09-04T12:00:00Z"),
    )

    reported = module.status(data, now=NOW)

    assert reported["counts"] == {
        "known": 2,
        "unreadable": 0,
        "unattended_due": 0,
        "manual_due": 1,
    }
    assert reported["resolves"] == "/model-selector update"
    manual = [source for source in reported["sources"] if not source["unattended"]]
    assert manual[0]["reason"] == "unrecognised_kind"
    assert manual[0]["due"] is True


def test_status_says_which_of_a_machines_sources_carry_a_price(
    tmp_path: Path,
) -> None:
    """The distinction survives the reversal, because a reader wants it."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:card", kind="gateway_rate_card"),
        _row(source_key="sha256:models", kind="model_release_index"),
    )

    priced = {
        source["source_key"]: source["priced"]
        for source in module.status(data, now=NOW)["sources"]
    }

    assert priced == {"sha256:card": True, "sha256:models": False}


def test_status_retrieves_nothing_and_writes_nothing(tmp_path: Path) -> None:
    """The report surface is read-only, exactly as the rest of `status` is."""

    module = _load()
    data = _store(tmp_path, _row())
    before = (data / "source-states.jsonl").read_bytes()

    module.status(data, now=NOW)

    assert (data / "source-states.jsonl").read_bytes() == before
    assert [path.name for path in data.iterdir()] == ["source-states.jsonl"]


def test_status_reports_a_next_due_date_computed_from_the_retrieval(
    tmp_path: Path,
) -> None:
    """A monthly cadence advances a calendar month, not thirty days."""

    module = _load()
    data = _store(
        tmp_path,
        _row(
            kind="benchmark_release_index",
            last_retrieved_at="2026-08-23T12:00:00Z",
        ),
    )

    source = module.status(data, now=NOW)["sources"][0]

    assert source["cadence"] == "P1M"
    assert source["next_due_at"] == "2026-09-23T12:00:00Z"
    assert source["due"] is False


def test_the_session_end_hook_dispatches_the_refresh(tmp_path: Path) -> None:
    """The pass rides the session-end invocation the Skill already installs.

    It is dispatched from inside that one invocation rather than as a second
    registered entry, so the seam stays one owned hook per event.
    """

    capture = _load(CAPTURE)
    data = _store(tmp_path, _row(last_retrieved_at="2026-09-04T12:00:00Z"))
    capture.install(data, tmp_path / "home", ["claude-code"], ["uv", "run", "hook"])

    capture.hook(data, "SessionStart", {"session_id": "s", "harness": "claude-code"})
    answered = capture.hook(
        data, "SessionEnd", {"session_id": "s", "harness": "claude-code"}
    )

    assert answered["ok"] is True
    assert _rows(data)[0]["last_checked_at"] is not None


def test_the_session_end_hook_survives_a_refresh_that_cannot_run(
    tmp_path: Path,
) -> None:
    """Every failure in the pass is swallowed where the surrounding path's are."""

    capture = _load(CAPTURE)
    data = _store(tmp_path, _row())

    # The pass cannot write its store back through a name a directory holds,
    # so it raises where the handler has to answer for it.
    (data / "source-states.jsonl.tmp").mkdir()

    answered = capture.hook(
        data, "SessionEnd", {"session_id": "s", "harness": "claude-code"}
    )

    assert answered["ok"] is True
    assert answered["fail_open"] is False


def test_the_refresh_and_capture_agree_on_where_the_data_directory_is() -> None:
    """Two readers of one on-disk contract, pinned rather than imported."""

    assert _load().default_data() == _load(CAPTURE).default_data()


class _Answer:
    """Stand in for one HTTP response, read in chunks as a real one is.

    *pause* is how long each chunk takes to arrive, which is what a server
    that accepts a connection and then drips bytes does to a budget spent
    once per socket operation.
    """

    def __init__(
        self, body: bytes, headers: dict[str, str], pause: float = 0.0
    ) -> None:
        self.body = body
        self.headers = headers
        self.pause = pause
        self.cursor = 0

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *unused: object) -> None:
        return None

    def read(self, size: int) -> bytes:
        if self.pause:
            time.sleep(self.pause)
        chunk = self.body[self.cursor : self.cursor + size]
        self.cursor += len(chunk)
        return chunk


def test_the_shipped_retrieval_sends_the_validators_the_row_holds(
    monkeypatch: Any,
) -> None:
    """Conditional retrieval is what keeps an unattended pass cheap."""

    module = _load()
    asked: list[Any] = []

    def urlopen(request: Any, timeout: float) -> Any:
        asked.append(request)
        return _Answer(b"body", {"ETag": 'W/"next"'})

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    answer = module._retrieve("https://example.invalid/a", 'W/"old"', "Mon", 1.0)

    assert asked[0].get_header("If-none-match") == 'W/"old"'
    assert asked[0].get_header("If-modified-since") == "Mon"
    assert answer.modified is True
    assert answer.content_hash.startswith("sha256:")


def test_the_shipped_retrieval_reads_not_modified_as_a_source_that_held(
    monkeypatch: Any,
) -> None:
    """A 304 is the cheapest possible answer and the one this pass wants."""

    module = _load()

    def urlopen(request: Any, timeout: float) -> Any:
        raise urllib.error.HTTPError(
            "https://example.invalid/a", 304, "Not Modified", Message(), None
        )

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    answer = module._retrieve("https://example.invalid/a", 'W/"old"', None, 1.0)

    assert answer.modified is False
    assert answer.content_hash is None


def test_the_shipped_retrieval_abandons_a_response_it_cannot_bound(
    monkeypatch: Any,
) -> None:
    """A hash of a truncated body would report a changed page as unchanged."""

    module = _load()

    def urlopen(request: Any, timeout: float) -> Any:
        return _Answer(b"x" * (module.MAX_RESPONSE_BYTES + module.CHUNK_BYTES), {})

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    assert module._retrieve("https://example.invalid/a", None, None, 10.0) is None


def test_the_shipped_retrieval_abandons_a_body_still_arriving_at_its_deadline(
    monkeypatch: Any,
) -> None:
    """The allowance bounds the whole retrieval, not one socket operation.

    A server that accepts the connection and then drips bytes would otherwise
    spend the allowance on connecting and again on every read, and the pass's
    own budget would bound nothing.
    """

    module = _load()

    def urlopen(request: Any, timeout: float) -> Any:
        # Half the allowance goes to the socket, so no single blocking
        # operation can outlast the whole of it.
        assert timeout == 0.05
        return _Answer(b"x" * (16 * module.CHUNK_BYTES), {}, pause=0.03)

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)
    started = time.monotonic()
    answer = module._retrieve("https://example.invalid/a", None, None, 0.1)
    elapsed = time.monotonic() - started

    assert answer is None
    assert elapsed < 0.4


def test_the_shipped_retrieval_answers_every_failure_as_unreachable(
    monkeypatch: Any,
) -> None:
    """It runs inside a session teardown, where raising is the one thing forbidden."""

    module = _load()

    def urlopen(request: Any, timeout: float) -> Any:
        raise urllib.error.URLError("no route to host")

    monkeypatch.setattr(urllib.request, "urlopen", urlopen)

    assert module._retrieve("https://example.invalid/a", None, None, 1.0) is None


def _document(*models: dict[str, Any], **document: Any) -> bytes:
    """Provide one machine-readable catalogue document, as a source serves it."""

    return json.dumps({**document, "models": list(models)}).encode("utf-8")


def _serving(module: Any, body: bytes) -> Any:
    """Provide a retrieval that answers with one document that changed."""

    def retrieve(uri: str, etag: str | None, last: str | None, timeout: float) -> Any:
        return module.Retrieved(
            modified=True,
            etag=None,
            last_modified=None,
            content_hash="sha256:fresh",
            body=body,
        )

    return retrieve


def _catalogue(data: Path) -> dict[str, Any]:
    """Return the refreshed catalogue the pass wrote under *data*."""

    loaded = json.loads((data / "catalogue.json").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return cast(dict[str, Any], loaded)


def test_a_fetched_price_reaches_the_catalogue_with_its_source_and_its_date(
    tmp_path: Path,
) -> None:
    """A rate card carried with its provenance is auditable; a bare number is not."""

    module = _load()
    data = _store(
        tmp_path,
        _row(kind="gateway_rate_card", reads_as="catalogue-json"),
    )
    body = _document(
        {
            "id": "example-one",
            "provider": "example",
            "family": "one",
            "price": {"input": 3.0, "output": 15.0, "currency": "USD"},
        }
    )

    answered = module.refresh(data, now=NOW, retrieve=_serving(module, body))

    assert answered["catalogue"] == ["example-one"]
    entry = _catalogue(data)["models"][0]
    assert entry["price"]["input"] == 3.0
    assert entry["source_url"] == "https://example.invalid/models"
    assert entry["retrieved"] == "2026-09-05T12:00:00Z"


def test_a_fetched_fact_that_cannot_be_attributed_is_discarded(
    tmp_path: Path,
) -> None:
    """What the pass may never do is store a fact it cannot attribute.

    An entry claiming a source this pass cannot use is dropped rather than
    quietly re-attributed to whatever page it happened to arrive on.
    """

    module = _load()
    data = _store(tmp_path, _row(reads_as="catalogue-json"))
    body = _document(
        {"id": "kept", "provider": "example", "family": "kept"},
        {
            "id": "unattributed",
            "provider": "example",
            "family": "unattributed",
            "price": {"input": 1.0, "currency": "USD"},
            "source_url": None,
        },
    )

    answered = module.refresh(data, now=NOW, retrieve=_serving(module, body))

    assert answered["catalogue"] == ["kept"]
    assert [entry["id"] for entry in _catalogue(data)["models"]] == ["kept"]


def test_a_price_for_a_model_the_catalogue_already_knows_lands_complete(
    tmp_path: Path,
) -> None:
    """A document naming only a price is the ordinary case, and it has to load.

    The catalogue's own reader rejects an entry with no provider and no
    family, so a partial one is completed from what is already known rather
    than written in a shape nothing can read back.
    """

    module = _load()
    data = _store(tmp_path, _row(kind="gateway_rate_card", reads_as="catalogue-json"))
    seeded = _load(MODEL_SELECTOR / "scripts" / "catalogue.py")
    identifier = seeded.load(data, MODEL_SELECTOR).models[0].id
    body = _document({"id": identifier, "price": {"input": 2.0, "currency": "USD"}})

    module.refresh(data, now=NOW, retrieve=_serving(module, body))

    written = seeded.load(data, MODEL_SELECTOR)
    entry = next(model for model in written.models if model.id == identifier)
    assert entry.price is not None
    assert entry.price.input == 2.0
    assert entry.family


def test_a_model_nothing_can_place_is_not_written_to_the_catalogue(
    tmp_path: Path,
) -> None:
    """An entry the reader would silently skip is not a fact worth storing."""

    module = _load()
    data = _store(tmp_path, _row(reads_as="catalogue-json"))
    body = _document({"id": "who-knows", "price": {"input": 1.0, "currency": "USD"}})

    answered = module.refresh(data, now=NOW, retrieve=_serving(module, body))

    assert answered["catalogue"] == []
    assert not (data / "catalogue.json").exists()


def test_a_source_naming_no_reader_is_retrieved_and_never_interpreted(
    tmp_path: Path,
) -> None:
    """Every source on every machine is in this state until one is registered."""

    module = _load()
    data = _store(tmp_path, _row())
    body = _document({"id": "example-one", "provider": "example", "family": "one"})

    answered = module.refresh(data, now=NOW, retrieve=_serving(module, body))

    assert answered["catalogue"] == []
    assert not (data / "catalogue.json").exists()


def test_what_a_pass_learns_is_folded_into_what_the_catalogue_already_held(
    tmp_path: Path,
) -> None:
    """A pass that learned only a price leaves every other fact standing."""

    module = _load()
    data = _store(tmp_path, _row(reads_as="catalogue-json"))
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-08-01T00:00:00Z",
                "models": [
                    {
                        "id": "example-one",
                        "provider": "example",
                        "family": "one",
                        "capability": 0.8,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    body = _document({"id": "example-one", "price": {"input": 3.0, "currency": "USD"}})

    module.refresh(data, now=NOW, retrieve=_serving(module, body))

    entry = _catalogue(data)["models"][0]
    assert entry["capability"] == 0.8
    assert entry["price"]["input"] == 3.0


def test_forcing_the_pass_checks_every_mutable_index_now(tmp_path: Path) -> None:
    """`update --force` is what the help page advertises, so the flag does it."""

    module = _load()
    data = _store(
        tmp_path,
        _row(source_key="sha256:index", last_retrieved_at=STILL_FRESH),
        _row(
            source_key="sha256:detail",
            kind="model_detail",
            uri="https://example.invalid/detail",
            last_retrieved_at=STILL_FRESH,
        ),
    )
    reached: list[tuple[str, float]] = []

    answered = module.refresh(
        data, now=NOW, retrieve=_reached(module, reached), force=True
    )

    # The mutable index is brought forward; the immutable detail page says the
    # same thing on every reading of it, so forcing it would learn nothing.
    assert [uri for uri, _ in reached] == ["https://example.invalid/models"]
    assert answered["forced"] is True
    assert answered["outcomes"]["not_due"] == 1


def test_an_unforced_pass_still_leaves_a_fresh_source_alone(tmp_path: Path) -> None:
    """The flag is the whole of the difference, and it defaults to off."""

    module = _load()
    data = _store(tmp_path, _row(last_retrieved_at=STILL_FRESH))

    answered = module.refresh(data, now=NOW, retrieve=_never)

    assert answered["forced"] is False
    assert answered["outcomes"]["not_due"] == 1


def test_the_command_line_accepts_the_flag_the_help_page_advertises() -> None:
    """A hint that advertises an inert flag is worse than one advertising none."""

    assert _load().parse_args(["refresh", "--force"]).force is True
    assert _load().parse_args(["refresh"]).force is False


def test_status_says_what_the_user_may_want_to_answer_again(tmp_path: Path) -> None:
    """It asks nothing and stops nothing; it names `setup` and stops there."""

    module = _load()
    data = _store(tmp_path, _row())
    (data / "catalogue.json").write_text(
        json.dumps(
            {
                "generated_at": "2026-09-01T00:00:00Z",
                "models": [
                    {"id": "example-one", "provider": "example", "family": "one"}
                ],
            }
        ),
        encoding="utf-8",
    )
    (data / "profile.json").write_text(
        json.dumps(
            {
                "harnesses": ["claude-code"],
                "providers": [],
                "models": [],
                "channels": [],
                "answered_at": "2026-01-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    reported = module.status(data, now=NOW)["profile"]

    assert "example-one" in reported["adoptable"]
    assert "example" in reported["unasked_providers"]
    assert "was answered more than" in reported["says"]
    assert "never asked about" in reported["says"]
    assert "/model-selector setup" in reported["says"]


def test_status_says_nothing_where_the_profile_has_nothing_to_answer(
    tmp_path: Path,
) -> None:
    """A nudge nobody needs is a reminder that teaches people to ignore them."""

    module = _load()
    data = _store(tmp_path, _row())

    assert module.status(data, now=NOW)["profile"]["says"] is None


KIND_ROW = re.compile(r"^\| `([a-z_]+)` \|", re.MULTILINE)


def _shipped_pages() -> list[Path]:
    """Return every Markdown file the model-selector Skill ships."""

    return sorted(MODEL_SELECTOR.rglob("*.md"))


def test_no_shipped_surface_says_the_configuration_overrides_a_cadence() -> None:
    """The permission is withdrawn wherever it was written, not only where listed.

    The profile carries no cadence member, no code ever read one, and the
    override vanished from a fresh `setup` without anybody noticing — which is
    the evidence it does not carry its own weight (#247).
    """

    withdrawn = ("configured cadence", "refresh cadences", "may override these")
    for page in _shipped_pages():
        text = page.read_text(encoding="utf-8")
        for claim in withdrawn:
            assert claim not in text, f"{page.name} still says {claim!r}"


def test_the_module_and_the_shipped_cadences_carry_the_same_source_kinds() -> None:
    """One closed vocabulary, read by the pass and priced by the shipped cadences.

    The reference this used to be checked against is gone with the rest of the
    old ledger prose, and the cadence file is the better half of that pair
    anyway: it is what the pass actually reads to decide what is due, so a kind
    the module knows and the cadences do not is a kind that never becomes due.
    """

    module = _load()
    cadences = set(json.loads(CADENCES.read_text(encoding="utf-8"))["cadences"])

    assert cadences == set(module.FETCHABLE_KINDS | module.COMMERCIAL_KINDS)
