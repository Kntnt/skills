"""The landed-change Interface shared across the pipeline."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

import pytest  # type: ignore[import-not-found]  # CI's mypy command omits pytest.

REPO_ROOT: Path = Path(__file__).resolve().parent.parent
CONTRACT: Path = (
    REPO_ROOT / "skills" / "kntnt" / "library" / "references" / "landed-change.md"
)
PIPELINE_RULES: Path = REPO_ROOT / "docs" / "rules" / "pipeline.md"
STANDARD: str = "docs/rules/skills.md"
TICKET_TRAILER: str = "Kntnt-Ticket"
PLAN_TRAILER: str = "Kntnt-Plan"
PLAN_FINGERPRINT: str = f"sha256:{'a' * 64}"
PLAN_FINGERPRINT_PATTERN: re.Pattern[str] = re.compile(r"sha256:[0-9a-f]{64}")


def _git(repository: Path, *arguments: str) -> str:
    """Keep fixture Git failures visible.

    Partial histories cannot satisfy this contract.
    """

    return subprocess.run(
        ["git", *arguments],
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _commit(
    repository: Path,
    subject: str,
    *,
    ticket: str | None = None,
    fingerprint: str = PLAN_FINGERPRINT,
) -> str:
    """Advance fixture history through Git's own trailer handling."""

    # Let Git parse the optional trailer block while advancing fixture history.
    message = subject
    if ticket is not None:
        message += f"\n\n{TICKET_TRAILER}: {ticket}\n{PLAN_TRAILER}: {fingerprint}"
    _git(repository, "commit", "--allow-empty", "-m", message)

    return _git(repository, "rev-parse", "HEAD")


@pytest.fixture  # type: ignore[untyped-decorator]
def repository(tmp_path: Path) -> Path:
    """Keep fixtures isolated from the developer's repository and identity."""

    # Initialise only the repository state each history fixture needs.
    _git(tmp_path, "init", "--initial-branch=integration")
    _git(tmp_path, "config", "user.name", "Contract Test")
    _git(tmp_path, "config", "user.email", "contract@example.invalid")
    _commit(tmp_path, "base")

    return tmp_path


def _reachable_matches(
    repository: Path, tip: str, ticket: str
) -> list[tuple[str, str]]:
    """Derive candidates from ancestry and Git's native trailer parser."""

    # Reachability comes from the named history, never from all object refs.
    matches: list[tuple[str, str]] = []
    for commit in _git(repository, "rev-list", tip).splitlines():
        trailers = _git(repository, "show", "-s", "--format=%(trailers:only)", commit)
        ticket_values = re.findall(rf"^{TICKET_TRAILER}: (.+)$", trailers, re.MULTILINE)
        plan_values = re.findall(rf"^{PLAN_TRAILER}: (.+)$", trailers, re.MULTILINE)
        if (
            ticket_values == [ticket]
            and len(plan_values) == 1
            and PLAN_FINGERPRINT_PATTERN.fullmatch(plan_values[0])
        ):
            matches.append((commit, plan_values[0]))

    return matches


def test_the_collection_library_carries_the_landed_change_interface() -> None:
    """The producer and both consumers share one durable Git contract."""

    assert CONTRACT.is_file(), (
        f"{CONTRACT}: `/dispatch`, `/compile`, and `/land` need one shared"
        f" landed-change Interface in the Collection Library. See {STANDARD}."
    )

    # Pin the commit contents, fixed trailers, and scratch-history boundary.
    text = CONTRACT.read_text(encoding="utf-8")
    for promise in (
        "one dispatcher-authored landing commit",
        "implementation patch",
        "exact compiler-owned tests",
        "every dispatcher-owned shared write",
        "Kntnt-Ticket: #<ticket>",
        "Kntnt-Plan: sha256:<bundle-fingerprint>",
        "Executor scratch commits",
        "do not land",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is part of the durable commit shape."
            f" See {STANDARD}."
        )


@pytest.mark.parametrize(  # type: ignore[untyped-decorator]
    ("history", "expected_count"),
    (
        ("none", 0),
        ("reachable", 1),
        ("off-history", 0),
        ("duplicate", 2),
        ("malformed-plan", 0),
        ("repeated-ticket-trailer", 0),
    ),
)
def test_selection_counts_only_matching_commits_reachable_from_the_evaluated_tip(
    repository: Path,
    history: str,
    expected_count: int,
) -> None:
    """Zero, off-history, and duplicate matches never become one baton."""

    # Construct the requested graph before observing only integration history.
    base = _git(repository, "rev-parse", "HEAD")
    if history == "reachable":
        _commit(repository, "land #185", ticket="#185")
    elif history == "off-history":
        _git(repository, "switch", "-c", "other")
        _commit(repository, "land #185 elsewhere", ticket="#185")
        _git(repository, "switch", "integration")
    elif history == "duplicate":
        _commit(repository, "first land #185", ticket="#185")
        _commit(repository, "second land #185", ticket="#185")
    elif history == "malformed-plan":
        _commit(
            repository, "malformed land #185", ticket="#185", fingerprint="sha256:no"
        )
    elif history == "repeated-ticket-trailer":
        message = (
            "repeated ticket trailer\n\n"
            f"{TICKET_TRAILER}: #185\n"
            f"{TICKET_TRAILER}: #185\n"
            f"{PLAN_TRAILER}: {PLAN_FINGERPRINT}"
        )
        _git(repository, "commit", "--allow-empty", "-m", message)

    # A selected baton exists only for the single-match fixture.
    tip = _git(repository, "rev-parse", "integration")
    matches = _reachable_matches(repository, tip, "#185")
    assert len(matches) == expected_count
    assert (len(matches) == 1) is (history == "reachable")
    assert _git(repository, "merge-base", "--is-ancestor", base, tip) == ""


def test_selected_baton_exposes_the_implementation_vantage_and_plan_fingerprint(
    repository: Path,
) -> None:
    """Land can recover both consumer inputs from Git alone."""

    landing_commit = _commit(repository, "land #185", ticket="#185")

    # The selected pair is the implementation commit and exact plan identity.
    matches = _reachable_matches(repository, "integration", "#185")
    assert matches == [(landing_commit, PLAN_FINGERPRINT)]


def test_contract_pins_blockers_lifecycle_compilation_and_journal_boundaries() -> None:
    """Every consumer interprets the same selected baton consistently."""

    # Pin every promise shared by the baton consumers.
    text = CONTRACT.read_text(encoding="utf-8")
    for promise in (
        "exactly one matching landing commit",
        "reachable from the integration history being evaluated",
        "reachable from the current integration tip",
        "Issue closure alone",
        "remains open",
        "knowledge and tracker closure",
        "not compiled again",
        "executable-ready label drift",
        "implementation vantage",
        "plan fingerprint",
        "without consulting a dispatch journal",
        "recovery and audit evidence",
        "not a portable or durable substitute",
    ):
        assert promise in text, (
            f"{CONTRACT}: `{promise}` is required by a baton consumer. See {STANDARD}."
        )

    # Tracker drift is a contract fixture because no consumer exists in S3.
    fixture = "| The issue is closed or its labels drift in any of the histories above | Unchanged | Preserve the Git result; tracker state neither creates nor removes a baton |"
    assert fixture in text, (
        f"{CONTRACT}: the tracker-drift fixture no longer pins Git selection."
        f" See {STANDARD}."
    )


def test_every_local_reference_from_the_shared_contract_resolves() -> None:
    """Every consumer can follow the Interface's exposed references."""

    # Resolve every local Markdown destination from the contract's directory.
    text = CONTRACT.read_text(encoding="utf-8")
    destinations = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    local_destinations = [
        destination.split("#", maxsplit=1)[0]
        for destination in destinations
        if "://" not in destination
    ]
    assert local_destinations, (
        f"{CONTRACT}: the shared Interface exposes no local contract pointer."
        f" See {STANDARD}."
    )

    # Report all broken addresses together for one corrective pass.
    missing = [
        destination
        for destination in local_destinations
        if not (CONTRACT.parent / destination).resolve().exists()
    ]
    assert missing == [], (
        f"{CONTRACT}: these local references resolve nowhere: {missing}."
        f" See {STANDARD}."
    )


def test_pipeline_rules_route_every_consumer_to_the_runtime_interface() -> None:
    """Keep current law reachable without copying the runtime contract."""

    # Pin the producer, consumers, and selection boundary at the rules seam.
    text = PIPELINE_RULES.read_text(encoding="utf-8")
    for promise in (
        "landed-change.md",
        "`/dispatch` authors",
        "`/compile` and `/land` consume",
        "exactly one matching landing commit",
        "Blocker completion",
        "defensive compilation guard",
        "remains open",
    ):
        assert promise in text, (
            f"{PIPELINE_RULES}: `{promise}` must route the shared baton rule"
            " to its runtime Interface. See docs/rules/docs.md."
        )
