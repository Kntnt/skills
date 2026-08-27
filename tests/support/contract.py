"""Shared assertions for a Skill's distributed prose contract."""

from pathlib import Path

# The rules module stating each of those rules once, with the record carrying
# its reasoning cited beside it. Every assertion enforcing one of them points
# here, so a contributor whose check has just gone red is given the rule and its
# reason in the message and the whole of it at this path (issue #69).
STANDARD = "docs/rules/skills.md"


def assert_contract_markers(
    path: Path,
    markers: tuple[str, ...],
    consequence: str,
) -> str:
    """Return an agent document after holding its required contract markers."""

    # Read the public prose seam once for every marker in this contract.
    text = path.read_text(encoding="utf-8")

    # Report the behavioural consequence of whichever obligation disappears.
    for marker in markers:
        assert marker in text, (
            f"{path}: the contract must state `{marker}`. {consequence} See {STANDARD}."
        )

    return text
