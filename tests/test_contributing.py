"""The contributor guide, and the tool names a contributor comes here to find."""

from __future__ import annotations

import json
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

# Where this repository declares which of its files are generated and what
# regenerates each. An unattended run reads it to tell a collision that carries
# a disagreement from one a command already answers (ADR-0106).
GENERATED = REPO_ROOT / ".kntnt-orchestrate" / "generated.json"

# The Catalog, and the line the guide tells a contributor to regenerate it
# with. The declaration beside it has to spell that line the same way.
CATALOG = "skills/kntnt/catalog.json"
REGENERATION = "KNTNT_SOURCE=. uv run skills/kntnt/scripts/kntnt.py catalog --write"

# The reference implementation is fetched from a subdirectory of the
# specification's own repository, so the whole of how it is obtained is in the
# one line that runs it, and the verb is the only part that varies.
INVOCATION = re.compile(
    r"uvx --from git\+https://github\.com/agentskills/agentskills"
    r"#subdirectory=skills-ref skills-ref ([a-z-]+) <skill-directory>"
)

# The Collection Library's shared modules, which need the same static checking
# locally and in CI. They are read off the shipped tree rather than listed
# here: a module named in one invocation and forgotten in the other is exactly
# what a pin holding one hardcoded path cannot see.
LIBRARY_SCRIPTS = REPO_ROOT / "skills" / "kntnt" / "library" / "scripts"


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


def test_every_shared_library_module_is_in_both_mypy_gates() -> None:
    """The Library's implementation is type-checked locally and in CI alike.

    The two invocations are written out in full in two files, so the one thing
    that can go wrong is a module reaching one of them: an engine added to the
    guide and forgotten in the workflow is checked on a contributor's machine
    and nowhere else, which is the failure a green pull request hides.
    """

    modules = sorted(LIBRARY_SCRIPTS.glob("*.py"))

    # A directory that came back empty would leave the loop below judging
    # nothing at all, which is the one outcome this check exists to catch.
    assert modules

    contributing = _contributing()
    ci = CI.read_text(encoding="utf-8")
    for module in modules:
        named = module.relative_to(REPO_ROOT).as_posix()
        for where, text in ((CONTRIBUTING, contributing), (CI, ci)):
            assert named in text, (
                f"{where.name}: {named} is a Collection Library module and is"
                f" not named in the mypy invocation there, so it is not"
                f" type-checked by both of the gates every other one is."
            )


def test_the_catalog_is_declared_generated_with_the_line_the_guide_gives() -> None:
    """The one file in this repository no hand writes says so where a run reads it.

    Every wave that merges two Skill-touching tickets collides in the Catalog,
    and always will: its bytes are a digest of the tree, so two builders who
    each regenerated it honestly cannot produce the same version. The
    declaration is what lets a run answer that with the command rather than
    with a repair (ADR-0106), and the command it names is the guide's own — a
    declaration spelling it some other way would regenerate something else.
    """

    declared = json.loads(GENERATED.read_text(encoding="utf-8"))["generated"]
    catalog = [entry for entry in declared if CATALOG in entry["files"]]

    assert catalog, (
        f"{GENERATED}: nothing declares {CATALOG} generated, so a wave that"
        f" collides in it pays a repair for what one command already knows."
        f" See ADR-0106."
    )
    assert [entry["command"] for entry in catalog] == [REGENERATION]
    assert REGENERATION in _contributing()
