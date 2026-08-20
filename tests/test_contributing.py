"""The contributor guide, and the tool names a contributor comes here to find."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRIBUTING = REPO_ROOT / "CONTRIBUTING.md"
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
DEVIATION_RECORD = (
    REPO_ROOT
    / "docs"
    / "adr"
    / "0066-the-reference-validator-is-a-baseline-not-a-gate.md"
)

# The reference implementation is fetched from a subdirectory of the
# specification's own repository, so the whole of how it is obtained is in the
# one line that runs it, and the verb is the only part that varies.
INVOCATION = re.compile(
    r"uvx --from git\+https://github\.com/agentskills/agentskills"
    r"#subdirectory=skills-ref skills-ref ([a-z-]+) <skill-directory>"
)


def _contributing() -> str:
    return CONTRIBUTING.read_text(encoding="utf-8")


def test_contributing_gives_the_line_that_obtains_the_reference_validator() -> None:
    """`validate` and `read-properties`, each written as it is actually typed.

    Neither is on `PATH` and neither is reachable under the name `agentskills`
    that this repository's older tickets used, so a contributor or an agent
    that goes looking finds nothing — which is what five agents did before the
    guide named the tool (issue #64).
    """

    verbs = {match.group(1) for match in INVOCATION.finditer(_contributing())}

    assert verbs == {"validate", "read-properties"}


def test_the_guide_and_the_record_spell_the_invocation_the_same_way() -> None:
    """One command line, written in two places, and neither free to drift."""

    record = DEVIATION_RECORD.read_text(encoding="utf-8")
    validate = next(
        match.group(0)
        for match in INVOCATION.finditer(_contributing())
        if match.group(1) == "validate"
    )

    assert validate in record


def test_the_guide_points_at_the_record_that_settles_the_red_run() -> None:
    """A contributor meeting a rejection must find out here that it is expected.

    The reasoning stays in one place: the guide cites the record rather than
    restating why the two deviating fields are shipped knowingly.
    """

    assert "ADR-0066" in _contributing()
    assert DEVIATION_RECORD.exists()


def test_no_check_ci_runs_is_the_reference_validator() -> None:
    """The tool is a baseline to compare against, and a gate would be red.

    ADR-0066 reads it as a state that must not regress rather than one that
    must pass, so a CI job running it would fail every build there is.
    """

    ci = CI.read_text(encoding="utf-8")

    assert "skills-ref" not in ci
    assert "agentskills" not in ci
