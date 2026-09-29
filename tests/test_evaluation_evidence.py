"""Which committed paths are evaluation evidence, and which scans skip them (#442)."""

from __future__ import annotations

import pytest
from support.evidence import is_evaluation_evidence
from test_agents_md import reads_for_retired_name
from test_flag_grammar import reads_for_flag_grammar

EVIDENCE = (
    "docs/evaluation/editorial-400/runs/waves/x-repo.txt",
    "docs/evaluation/brief-444/fixtures/x.json",
    "docs/evaluation/redline-445/README.md",
    "docs/evaluation/regressions/401/README.md",
    "docs/evaluation/records/redline-claude-2026-09-24-398.md",
    "docs/evaluation/editorial-388/runs/x.md",
    "docs/evaluation/editorial-329/harness/baseline-prompts/article-sv-write.txt",
    "docs/evaluation/editorial-999/plan.md",
)

LIVE = (
    "docs/evaluation/protocol.md",
    "docs/evaluation/README.md",
    "docs/evaluation/record-template.md",
    "docs/evaluation/records/README.md",
    "docs/evaluation/regressions/README.md",
    "docs/evaluation/corpus/editorial-quality/README.md",
    "docs/evaluation/editorial-388/README.md",
    "docs/evaluation/editorial-388/harness/staged_run.py",
    "docs/evaluation/editorial-329/harness/run.py",
    # Outside `docs/evaluation/` altogether.
    "docs/rules/docs.md",
    "docs/adr/0001-x.md",
    "skills/kntnt/SKILL.md",
)


@pytest.mark.parametrize("path", EVIDENCE)
def test_a_packet_a_regression_packet_or_a_record_is_evidence(path: str) -> None:
    assert is_evaluation_evidence(path)


@pytest.mark.parametrize("path", LIVE)
def test_the_live_documents_and_runners_are_not_evidence(path: str) -> None:
    assert not is_evaluation_evidence(path)


@pytest.mark.parametrize("path", EVIDENCE)
def test_the_retired_name_scan_skips_evidence(path: str) -> None:
    assert not reads_for_retired_name(path)


@pytest.mark.parametrize("path", LIVE[:9] + ("docs/rules/docs.md",))
def test_the_retired_name_scan_reads_the_live_documents(path: str) -> None:
    assert reads_for_retired_name(path)


@pytest.mark.parametrize("path", [path for path in EVIDENCE if path.endswith(".md")])
def test_the_flag_scan_skips_evidence(path: str) -> None:
    assert not reads_for_flag_grammar(path)


@pytest.mark.parametrize(
    "path", [path for path in LIVE if path.endswith(".md") and path.startswith("docs/")]
)
def test_the_flag_scan_reads_the_live_markdown(path: str) -> None:
    assert reads_for_flag_grammar(path)
