"""Reproduce prose-load accounting for the immutable editorial revisions."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
BASELINE = "8ae4c21c203fa44f9782c3c0db2c85a5d805c3a6"
CANDIDATE = "93758f4"
LIBRARY = "skills/kntnt/library/references/"
GENRES = ("article", "case-study", "column", "opinion", "web-copy")
LOCALES = ("sv", "en_GB", "en_US")


def read(revision: str, path: str) -> str:
    """Read committed resource bytes; absent new support files cost zero before."""
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        if revision == BASELINE and "web-craft" in path:
            return ""
        raise RuntimeError(result.stderr)
    return result.stdout


def words(revision: str, path: str) -> int:
    """Count whitespace-separated words, including headings and frontmatter."""
    return len(read(revision, path).split())


def scope(revision: str, locale: str, heading: str) -> int:
    """Count only a resolver scope's body, excluding its heading and metadata."""
    text = read(revision, f"{LIBRARY}languages/{locale}.md")
    match = re.search(
        rf"^## {heading}\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    if match is None:
        raise ValueError(f"Missing scope {locale}/{heading}")
    return len(match[1].split())


def contract(revision: str, genre: str, locale: str, review: bool) -> int:
    """Count each stage's full contract, including conditional ordinary arc."""
    paths = ["editorial/base.md", f"editorial/genres/{genre}.md"]
    if revision == BASELINE:
        paths.append("editorial/techniques/abt.md")
    else:
        paths.append("editorial/web-craft.md")
    if review:
        paths += [path.replace(".md", ".review.md") for path in paths[:]]
        paths.append("editorial/anti-slop.md")
    scopes = ["Composition", "Review", "Anti-slop"] if review else ["Composition"]
    return sum(words(revision, LIBRARY + path) for path in paths) + sum(
        scope(revision, locale, name) for name in scopes
    )


def main() -> None:
    """Write accounting as evidence, never as a normative resource."""
    revisions = (BASELINE, CANDIDATE)
    resources = ["base.md", "base.review.md", "web-craft.md", "web-craft.review.md"]
    resources += [
        f"genres/{g}{suffix}" for g in GENRES for suffix in (".md", ".review.md")
    ]
    resources += [
        f"techniques/{t}{suffix}"
        for t in ("abt", "pac")
        for suffix in (".md", ".review.md")
    ]
    lines = [
        "# Reading load — #331–337",
        "",
        (
            f"Whitespace-delimited words: baseline `{BASELINE}` versus candidate `{CANDIDATE}`. "
            "These are context costs, not quality targets or new rules. "
            "Reproduce with `python3 docs/evaluation/editorial-329/harness/reading_load.py`. "
            "The three language resources supply all scopes directly; scope counts match "
            "the resolver's body-only output. JSON wrappers, invocation results, supplied "
            "texts and findings are excluded because their lengths vary by run."
        ),
        "",
        "## Authored editorial resources",
        "",
        "| Resource | Before | After |",
        "|---|---:|---:|",
    ]
    for path in resources:
        counts = [words(r, LIBRARY + "editorial/" + path) for r in revisions]
        lines.append(f"| editorial/{path} | {counts[0]} | {counts[1]} |")
    lines += [
        "",
        "## Complete ordinary editorial contracts",
        "",
        (
            "Write includes base, selected genre, language composition and ordinary "
            "ABT before / shared web-craft without a technique after. Review and correction "
            "also include every applicable review half, shared anti-slop and language "
            "review/anti-slop. No rule has been moved into this report."
        ),
        "",
        "| Genre / locale | Write before | Write after | Review/correction before | Review/correction after |",
        "|---|---:|---:|---:|---:|",
    ]
    for genre in GENRES:
        for locale in LOCALES:
            counts = [
                contract(r, genre, locale, review)
                for review in (False, True)
                for r in revisions
            ]
            lines.append(
                f"| {genre} / {locale} | " + " | ".join(map(str, counts)) + " |"
            )
    operations = [
        "skills/editorial/write/SKILL.md",
        "skills/editorial/redline/SKILL.md",
        "skills/editorial/redline/references/correction.md",
        "skills/editorial/proofread/SKILL.md",
        LIBRARY + "delivery.md",
        LIBRARY + "editorial/mechanics.md",
        LIBRARY + "invocation-envelope.md",
        "skills/editorial/write/references/quotations.md",
    ]
    lines += [
        "",
        "## Operational instructions and full stage costs",
        "",
        (
            "The editorial contract alone is not the full invocation. Write and review "
            "each add their SKILL.md and delivery contract. Each correction adds its "
            "complete correction brief. The final installed Proofread adds its SKILL.md, "
            "delivery, shared mechanics and the selected language's mechanics. "
            "Reads are counted again at each stage/agent boundary; incidental duplicate "
            "reads inside a stage are not contractual requirements and actual traces "
            "remain authoritative about run-specific overreads."
        ),
        "",
        "| File | Before | After |",
        "|---|---:|---:|",
    ]
    for path in operations:
        counts = [words(r, path) for r in revisions]
        lines.append(f"| {path} | {counts[0]} | {counts[1]} |")
    totals: dict[str, dict[str, list[int]]] = {}
    for revision in revisions:
        tally: dict[str, list[int]] = {
            name: [] for name in ("Write", "Review", "Correction", "Pipeline")
        }
        delivery = words(revision, LIBRARY + "delivery.md")
        for genre in GENRES:
            for locale in LOCALES:
                write = (
                    contract(revision, genre, locale, False)
                    + words(revision, operations[0])
                    + delivery
                )
                review = (
                    contract(revision, genre, locale, True)
                    + words(revision, operations[1])
                    + delivery
                )
                correction = contract(revision, genre, locale, True) + words(
                    revision, operations[2]
                )
                proofread = (
                    words(revision, operations[3])
                    + delivery
                    + words(revision, operations[5])
                    + scope(revision, locale, "Mechanics")
                )
                for name, value in (
                    ("Write", write),
                    ("Review", review),
                    ("Correction", correction),
                    ("Pipeline", write + review + proofread),
                ):
                    tally[name].append(value)
        totals[revision] = tally
    lines += [
        "",
        "| Complete stage / pipeline | Before range | After range |",
        "|---|---:|---:|",
    ]
    for name in ("Write", "Review", "Correction", "Pipeline"):
        ranges = [f"{min(totals[r][name])}–{max(totals[r][name])}" for r in revisions]
        lines.append(f"| {name} | {ranges[0]} | {ranges[1]} |")
    lines += ["", "| Final Proofread | Before | After |", "|---|---:|---:|"]
    for locale in LOCALES:
        counts = [
            sum(words(r, p) for p in (operations[3], operations[4], operations[5]))
            + scope(r, locale, "Mechanics")
            for r in revisions
        ]
        lines.append(f"| {locale} | {counts[0]} | {counts[1]} |")
    lines += [
        "",
        (
            "Pipeline means ordinary Write → Redline review → one Proofread, before "
            "any correction rounds. Add the complete Correction cost for each actual "
            "round. Conditional quotation guidance and invocation-envelope guidance "
            "are listed above, not hidden in an ordinary no-quotation/no-context total. "
            "A quoted Write adds its quotation guidance. An invocation with contextual "
            "instructions adds the envelope. Explicit ABT/PAC adds its base to Write "
            "and base/review pair to review and correction; exact deltas are in the "
            "resource table. Inference may read installed genre openings only when "
            "the genre is unresolved. Help is outside these invocation paths."
        ),
        "",
        (
            "The reductions concern instruction volume, not proof of better prose. "
            "Operational and language contracts still account for much of the load. "
            "The evaluation records distinguish expected paths from observed failures "
            "such as the unnecessary genre-opening scan in #350."
        ),
        "",
    ]
    (ROOT / "docs/evaluation/editorial-329/reading-load.md").write_text(
        "\n".join(lines)
    )


if __name__ == "__main__":
    main()
