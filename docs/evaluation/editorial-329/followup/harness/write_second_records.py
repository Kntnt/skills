# /// script
# requires-python = ">=3.12"
# ///
"""Render independently authored second-wave judgements as evaluation records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT: Path = Path("/Users/thomas/Projects/skills")
FOLLOW: Path = ROOT / "docs/evaluation/editorial-329/followup"
RECORDS: Path = ROOT / "docs/evaluation/records"
QUALITY: tuple[str, ...] = ("G1", "G2", "P1", "W1", "L1", "L2")


def header(name: str, skill: str) -> list[str]:
    """Identify immutable instructions and retain the prior wave as history."""
    return [
        f"# {skill.title()} — GPT — second candidate, new/general verification",
        "",
        f"- **record** — `{name}`",
        "- **date** — `2026-09-19`",
        "- **ticket** — #329, #349, #352, #353, #354, #355",
        f"- **skill** — `{skill}`",
        "- **provider family** — `gpt`",
        "- **model** — `gpt-6-astra`, inherited `high`, checked in native parent/child traces",
        "- **harness** — Codex CLI0.155.1",
        "- **instruction commit** — `82db4393`",
        "- **corpus commit** — original `6e531f5`; supplemental `bf14dc2`; second controls `20de1df7`",
        "",
        "All criteria were frozen before these runs. The independent evaluator read each complete input and output before assigning the judgements below. No prior failed attempt is replaced. Full native sessions, responses, inventories, input stat, evaluator-extracted artifacts and cleanup receipts remain in each linked run directory. Checker approval is never the independent F1 judgement.",
        "",
    ]


def entry(
    case: str, run: Path, notes: dict[str, Any], criteria: list[str]
) -> list[str]:
    """Render recorded evidence without deriving semantic scores from prose."""

    # Run facts supply provenance; all criterion text comes from manual judging.
    relative = "../editorial-329/followup/" + str(run.relative_to(FOLLOW))
    invocation = (run / "invocation.txt").read_text().strip()
    result = json.loads((run / "result.json").read_text())
    target = (
        "in-place"
        if "--in-place" in invocation
        else "result.md"
        if "--output=result.md" in invocation
        else "response"
    )
    changes = json.loads((run / "native-audit.json").read_text())[
        "outside_native_home_changes"
    ]
    effects = {kind: list(paths) for kind, paths in changes.items()}
    lines = [
        f"## `{case}`",
        "",
        f"- **fixture** — `{case}`",
        f"- **invocation** — `{invocation}`",
        "- **contextual instruction** — none",
        f"- **output target** — {target}",
        f"- **observed delivery** — {notes.get('delivery', notes.get('outcome', 'Complete draft and separate account'))}. [Response]({relative}/response.txt), [artifact]({relative}/artifact.md), [account]({relative}/account.md), [input]({relative}/supplied-input.md).",
        f"- **side effects** — Skill-visible differences outside native Harness state: `{json.dumps(effects)}`. [Inventory differences]({relative}/filesystem-changes.json), [native audit]({relative}/native-audit.json), [cleanup]({relative}/cleanup.json).",
        "- **criteria** —",
    ]
    lines.extend(f"  - {criterion} — {notes[criterion]}" for criterion in criteria)
    lines.extend(
        [
            f"- **unresolved findings** — {notes.get('unresolved', 'none delivered')}",
            f"- **defects filed** — {notes.get('defect', notes.get('issue', 'none'))}",
            f"- **notes** — {notes.get('coverage', '')} {notes.get('repair', '')} {notes.get('artifact_source', '')} Native return code {result['returncode']}; duration {result['duration_seconds']} seconds.",
            "",
        ]
    )
    return lines


def controls() -> None:
    """Write the seven supplemental controls with every declared criterion."""
    name = "redline-gpt-2026-09-19-354-second-controls"
    notes = json.loads((FOLLOW / "reviews/second-control-judgements.json").read_text())
    lines = header(name, "redline")
    lines.extend(
        [
            "The timetable input repeats the full earlier artifact byte-for-byte. Two of three reviews still demand an unsupported rationale for an expressly qualified eight-week request (#354). The contrasting certainty control detects and removes the actual unsupported promise, with a removed-claim account. All three destination controls satisfy the repaired delivery contract (#353); their deliberately contradictory source remains a reported quality problem because max=0 forbids substantive correction. These expected remaining input defects are not new Skill defects.",
            "",
            "In-place preservation is established by identical bytes, nanosecond mtime and inode before and after. Separate-file output was captured before literal-path root cleanup; its bytes equal the input and it is the sole created non-Harness file. No response duplicates that separate artifact. Every control ran one final installed Proofread, on the resolved locale. Encrypted correction dispatch remains a limit on direct inspection of its exact payload; actual fresh settings, identity, resource loads and returned text are preserved.",
            "",
        ]
    )
    for case in (
        "timetable-r1",
        "timetable-r2",
        "timetable-r3",
        "certainty-r1",
        "delivery-response",
        "delivery-in-place",
        "delivery-file",
    ):
        lines.extend(
            entry(
                case,
                FOLLOW / "probes/second-controls" / case / "run",
                notes[case],
                [*QUALITY, "T1", "R1", "R2", "O1"],
            )
        )
    (RECORDS / f"{name}.md").write_text("\n".join(lines))


def main() -> None:
    """Render only the explicitly requested independently completed record."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["controls"])
    parser.parse_args()
    controls()


if __name__ == "__main__":
    main()
