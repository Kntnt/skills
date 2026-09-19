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


def header(name: str, skill: str, wave: str) -> list[str]:
    """Identify immutable instructions and retain the prior wave as history."""
    return [
        f"# {skill.title()} — GPT — {wave} candidate verification",
        "",
        f"- **record** — `{name}`",
        "- **date** — `2026-09-19`",
        "- **ticket** — #329, #349, #352, #353, #354, #355",
        f"- **skill** — `{skill}`",
        "- **provider family** — `gpt`",
        "- **model** — `gpt-6-astra`, inherited `high`, checked in native parent/child traces",
        "- **harness** — Codex CLI 0.155.1",
        f"- **instruction commit** — `{'82db4393' if wave == 'second' else '7b86144d'}`",
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


def controls(wave: str) -> None:
    """Write the selected wave's controls with every declared criterion."""
    name = f"redline-gpt-2026-09-19-354-{wave}-controls"
    notes = json.loads((FOLLOW / f"reviews/{wave}-control-judgements.json").read_text())
    lines = header(name, "redline", wave)
    if wave == "second":
        lines.extend(
            [
                "The timetable input repeats the full earlier artifact byte-for-byte. Two of three reviews still demand an unsupported rationale for an expressly qualified eight-week request (#354). The contrasting certainty control detects and removes the actual unsupported promise, with a removed-claim account. All three destination controls satisfy the repaired delivery contract (#353); their deliberately contradictory source remains a reported quality problem because max=0 forbids substantive correction. These expected remaining input defects are not new Skill defects.",
                "",
                "In-place preservation is established by identical bytes, nanosecond mtime and inode before and after. Separate-file output was captured before literal-path root cleanup; its bytes equal the input and it is the sole created non-Harness file. No response duplicates that separate artifact. Every control ran one final installed Proofread, on the resolved locale. Encrypted correction dispatch remains a limit on direct inspection of its exact payload; actual fresh settings, identity, resource loads and returned text are preserved.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "All three exact-input timetable controls preserve the qualified eight-week request without requiring an unsupported interval rationale. The contrasting certainty control removes only the actual unsupported guarantee, explicitly accounts for the removed claim and preserves the proposed deferral. Earlier failed observations remain in their records; this is repeated observed repair, not a reliability guarantee.",
                "",
                "Every control reads the complete selected review scope and performs one final installed Proofread. One mechanical child retries a command rejected before execution; it does not repeat a completed mechanical pass. Encrypted dispatch limits exact instruction-payload inspection. All four roots are absent after literal-path cleanup, and all-root inventories show no surviving Skill files or source changes.",
                "",
            ]
        )
    for case in notes:
        lines.extend(
            entry(
                case,
                FOLLOW / f"probes/{wave}-controls" / case / "run",
                notes[case],
                [*QUALITY, "T1", "R1", "R2", "O1"],
            )
        )
    (RECORDS / f"{name}.md").write_text("\n".join(lines))


def pipelines(stage: str, wave: str) -> None:
    """Render complete source and pipeline judgements from the manual record."""
    name = f"{stage}-gpt-2026-09-19-355-{wave}-new"
    all_notes = json.loads((FOLLOW / f"reviews/{wave}-new-judgements.json").read_text())
    lines = header(name, stage, wave)
    if wave == "second":
        lines.extend(
            [
                "Both Bellwick opinion repetitions fail independent F1: the article turns the supplied package's unknown consent status into a claim about the complete referenced submission. The source checker approves that extra scope; both paired source-blind Redline runs preserve it. This is [#355](https://github.com/Kntnt/skills/issues/355), not a duty for Redline to recover an unseen source. The unknown/absent distinction itself remains present, and a new document-content assertion is the failure.",
                "",
                "Actual source and complete delivered prose are visible in the final checker file reads; only resolved metadata and outer delivery separators are excluded from prose comparison. Encrypted dispatch still prevents direct inspection of every instruction in that message. Transport/process observations and independent semantic judgements remain separate. A disputed conservative removal of an optional author evaluation is retained as a limitation, not counted as a proven factual repair.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "The third matrix retains the same semantic criteria and full source packages. Each delivered artifact is judged independently, including optional positive-control coverage. A source-check approval establishes process completion only; exact observed draft transport and final source fidelity are recorded separately. Failed gates or skipped pairs, if any, are explicit in their entries.",
                "",
            ]
        )
    for case, original in all_notes.items():
        run = FOLLOW / f"runs/{wave}-candidate" / case / stage
        notes = dict(original)
        if stage == "write":
            notes.setdefault(
                "T1",
                "pass — Formal genre/locale and default none match metadata and actual selected resource loads; no technique inferred.",
            )
            notes.setdefault(
                "R2",
                "pass — Complete selected composition contract loaded; no editorial review half or peer editorial/mechanical pass. Source comparison remains its separate bounded task.",
            )
            notes.setdefault(
                "O1",
                "pass — Complete response and truthful account; all-root inventories show unchanged source/resources and no surviving Skill work/scratch files.",
            )
            criteria = ["F1", *QUALITY, "T1", "R2", "O1", "S1"]
        else:
            notes.update(original["redline"])
            notes["coverage"] = (
                "Source-aware pipeline judgement: " + notes["pipeline_F1"]
            )
            criteria = [*QUALITY, "T1", "R1", "R2", "O1", "S1"]
        lines.extend(entry(case, run, notes, criteria))
    (RECORDS / f"{name}.md").write_text("\n".join(lines))


def main() -> None:
    """Render only the explicitly requested independently completed record."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=["controls", "write", "redline"])
    parser.add_argument("--wave", choices=["second", "third"], default="second")
    args = parser.parse_args()
    if args.kind == "controls":
        controls(args.wave)
    else:
        pipelines(args.kind, args.wave)


if __name__ == "__main__":
    main()
