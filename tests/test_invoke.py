"""The engine that reads every Skill's invocation, `kntnt.py invoke`."""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
from support.contract import STANDARD

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS = REPO_ROOT / "skills"
MANAGER_DIR = SKILLS / "kntnt"
KNTNT_PY = MANAGER_DIR / "scripts" / "kntnt.py"
ENVELOPE = MANAGER_DIR / "library" / "references" / "invocation-envelope.md"
UV_CACHE = Path(os.environ.get("UV_CACHE_DIR") or Path.home() / ".cache" / "uv")

# The record settling that the grammar is executed by one engine rather than
# read by the model per invocation, cited by every failure below.
RECORD = "ADR-0181"

# The three answers the engine gives, told apart by exit status so that a
# body can treat the two non-zero ones alike — print stdout and stop — while a
# test can tell a page from a refusal.
EXIT_VALID = 0
EXIT_REFUSED = 2
EXIT_HELP = 3


def _engine() -> Any:
    """Load the Manager's script so the grammar reader can be called in-process.

    The shipped Skills declare binaries and peer Skills a test machine may not
    hold, and the dependency check runs before the grammar is read, so the
    sweep over every shipped grammar reaches the reader directly rather than
    through a subprocess whose first answer would be about `pdftotext`.
    """

    spec = importlib.util.spec_from_file_location("kntnt_invoke", KNTNT_PY)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _skill_md(
    name: str,
    hint: str,
    *,
    binaries: list[str] | None = None,
    capabilities: list[str] | None = None,
) -> str:
    """A SKILL.md in the shape the collection ships, with the given hint."""

    lists = {
        "binaries": binaries or [],
        "skills": [],
        "externals": [],
        "capabilities": capabilities or [],
    }
    lines = [
        "---",
        f"name: {name}",
        "description: A collection skill.",
        "disable-model-invocation: true",
        f"argument-hint: {json.dumps(hint)}",
        "metadata:",
        '  kntnt.internal: "true"',
        *(f'  kntnt.{key}: "{" ".join(values)}"' for key, values in lists.items()),
        "---",
        "",
        f"# {name}",
        "",
    ]
    return "\n".join(lines)


def _page(name: str, path: str, synopsis: list[str], options: list[str]) -> str:
    """A manpage carrying the two grammar sections the engine reads."""

    title = " ".join([name, *path.split()]) if path else name
    body = [
        f"# {title}",
        "",
        "## NAME",
        "",
        f"{title} - a fixture",
        "",
        "## SYNOPSIS",
        "",
    ]
    for form in synopsis:
        body.extend([form, ""])
    body.extend(["## DESCRIPTION", "", f"The {title} page.", ""])
    if options:
        body.extend(["## OPTIONS", ""])
        for term in options:
            body.extend([term, "", "What it does.", ""])
    body.extend(
        [
            "## DEPENDENCIES",
            "",
            "None",
            "",
            "## SEE ALSO",
            "",
            f"**/{name} --help**",
            "",
        ]
    )
    return "\n".join(body)


def _fixture(
    root: Path,
    name: str,
    hint: str,
    synopsis: list[str],
    options: list[str] | None = None,
    pages: dict[str, tuple[list[str], list[str]]] | None = None,
    *,
    binaries: list[str] | None = None,
    capabilities: list[str] | None = None,
) -> Path:
    """Write one fixture Skill under *root* and return its directory."""

    directory = root / name
    _write(
        directory / "SKILL.md",
        _skill_md(name, hint, binaries=binaries, capabilities=capabilities),
    )
    _write(directory / "help.md", _page(name, "", synopsis, options or []))
    for path, (forms, terms) in (pages or {}).items():
        _write(
            directory / "help" / (path.replace(" ", "/") + ".md"),
            _page(name, path, forms, terms),
        )
    return directory


def _force_skill(
    root: Path,
    *,
    binaries: list[str] | None = None,
    capabilities: list[str] | None = None,
) -> Path:
    """The schematic `/skill --force` the worked-cases table is written for."""

    return _fixture(
        root,
        "skill",
        "[--force] [-- <instruction>]",
        ["**/skill** [**--force**] [**--** *INSTRUCTION*]"],
        ["**--force**"],
        binaries=binaries,
        capabilities=capabilities,
    )


def _invoke(
    directory: Path, payload: str, tmp_path: Path
) -> subprocess.CompletedProcess[str]:
    """Run the shipped engine against *directory* with *payload* on stdin."""

    home = tmp_path / "home"
    project = tmp_path / "proj"
    home.mkdir(exist_ok=True)
    project.mkdir(exist_ok=True)
    env = os.environ.copy()
    env["HOME"] = str(home)
    env["UV_CACHE_DIR"] = str(UV_CACHE)
    env["KNTNT_HOME"] = str(home)
    env["KNTNT_PROJECT"] = str(project)
    return subprocess.run(
        ["uv", "run", "--quiet", str(KNTNT_PY), "invoke", f"--here={directory}"],
        input=payload,
        cwd=project,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def _synopsis(page: Path) -> str:
    text = page.read_text(encoding="utf-8")
    return text.partition("\n## SYNOPSIS\n")[2].partition("\n## ")[0].strip("\n")


# --- The worked cases of the Library file -----------------------------------


def _cell(text: str) -> str | None:
    """Read one table cell: a code span, possibly double-fenced, or a dash."""

    text = text.strip()
    if text == "—":
        return None
    if text.startswith("``") and text.endswith("``"):
        text = text[2:-2].strip()
    elif text.startswith("`") and text.endswith("`"):
        text = text[1:-1]
    return text.replace("\\n\\n", "\n\n")


def _worked_cases() -> list[tuple[str, str, str, str | None, str]]:
    """Read the worked-cases table off the Library file, row by row."""

    rows: list[tuple[str, str, str, str | None, str]] = []
    text = ENVELOPE.read_text(encoding="utf-8")
    table = text.partition("## Worked cases")[2]
    for line in table.splitlines():
        if not line.startswith("| ") or line.startswith(("| Case", "| ---")):
            continue
        cells = [part for part in re.split(r"(?<!\\)\|", line)[1:-1]]
        case, envelope, formal, instruction, outcome = (
            cells[0].strip(),
            _cell(cells[1]),
            _cell(cells[2]),
            _cell(cells[3]),
            cells[4].strip(),
        )
        assert envelope is not None and formal is not None
        rows.append((case, envelope, formal, instruction, outcome))
    return rows


def _after_name(text: str) -> str:
    """Strip the schematic `/skill` the table writes in front of every payload."""

    assert text.startswith("/skill")
    return text[len("/skill") :].lstrip(" ") if text != "/skill" else ""


def test_the_envelope_split_matches_every_worked_case_row_by_row() -> None:
    """The table that pinned the split as prose is now the engine's own test."""

    engine = _engine()
    rows = _worked_cases()

    # A table the scan could not read would leave this judging nothing.
    assert len(rows) == 7

    for case, envelope, formal, instruction, outcome in rows:
        split_formal, split_instruction = engine.split_envelope(_after_name(envelope))

        assert split_formal == _after_name(formal), (
            f"{case}: the Formal Invocation of {envelope!r} is {formal!r}"
            f" ({RECORD}). See {STANDARD}."
        )
        if outcome == "Syntax refusal":
            assert split_instruction == "", (
                f"{case}: an empty suffix is told from no separator ({RECORD})."
            )
        else:
            assert split_instruction == instruction, (
                f"{case}: the Contextual Instruction of {envelope!r} is"
                f" {instruction!r} ({RECORD}). See {STANDARD}."
            )


def test_every_worked_case_reaches_the_outcome_the_table_names(tmp_path: Path) -> None:
    """The split is followed by the outcome each row says comes next."""

    engine = _engine()
    skill = _force_skill(tmp_path)
    page = (skill / "help.md").read_text(encoding="utf-8").rstrip("\n")

    for case, envelope, _formal, _instruction, outcome in _worked_cases():
        reading = engine.read_invocation(skill, _after_name(envelope))

        if outcome == "Envelope valid; formal grammar next":
            assert reading.status == EXIT_VALID, (case, reading.text)
        elif outcome == "Syntax refusal":
            assert reading.status == EXIT_REFUSED, case
            assert _synopsis(skill / "help.md") in reading.text, case
            assert "see '/skill --help'" in reading.text, case
        elif outcome == "Context refusal; render nothing":
            assert reading.status == EXIT_REFUSED, case
            assert page not in reading.text, f"{case}: the page was rendered."
            assert "Explain this page" in reading.text, case
            assert "SYNOPSIS" not in reading.text, (
                f"{case}: a context refusal prints no synopsis."
            )
        else:
            # "No split; formal grammar decides": the schematic grammar takes no
            # operand, so the whole payload reaching the grammar is what refuses it.
            assert outcome == "No split; formal grammar decides", case
            assert reading.status == EXIT_REFUSED, case
            assert not reading.invocation, case


# --- The three answers, end to end ------------------------------------------


def test_a_valid_form_answers_with_json_and_the_dependency_payload(
    tmp_path: Path,
) -> None:
    skill = _force_skill(tmp_path, capabilities=["subagents"])

    result = _invoke(skill, "--force -- Preserve deployment facts", tmp_path)

    assert result.returncode == EXIT_VALID, result.stderr
    assert result.stderr == ""
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["path"] == []
    assert payload["flags"] == {"--force": True}
    assert payload["operands"] == []
    assert payload["instruction"] == "Preserve deployment facts"
    dependencies = payload["dependencies"]
    assert dependencies["ok"] is True
    assert dependencies["unsatisfied"] == []
    assert dependencies["capabilities"][0]["name"] == "subagents"
    assert dependencies["capabilities"][0]["confirm"]


def test_a_multi_line_instruction_with_quotes_survives_stdin(tmp_path: Path) -> None:
    """The payload reaches the engine as text, however many lines it runs to."""

    skill = _force_skill(tmp_path)
    instruction = (
        'Keep the "deployment" facts.\n\nDon\'t touch the -- second paragraph.'
    )

    result = _invoke(skill, f"--force --\n\n{instruction}\n", tmp_path)

    assert result.returncode == EXIT_VALID, result.stderr
    assert json.loads(result.stdout)["instruction"] == instruction


def test_an_exact_help_form_prints_the_addressed_page_on_its_own_status(
    tmp_path: Path,
) -> None:
    skill = _fixture(
        tmp_path,
        "tool",
        "(on|off) [-- <instruction>]",
        ["**/tool** (**on**|**off**) [**--** *INSTRUCTION*]"],
        pages={
            "on": (["**/tool on** [**--** *INSTRUCTION*]"], []),
            "off": (["**/tool off** [**--** *INSTRUCTION*]"], []),
        },
    )
    root = (skill / "help.md").read_text(encoding="utf-8").rstrip("\n")
    on = (skill / "help" / "on.md").read_text(encoding="utf-8").rstrip("\n")

    for payload in ("--help", "-h", "help"):
        result = _invoke(skill, payload, tmp_path)
        assert result.returncode == EXIT_HELP, (payload, result.stderr)
        assert result.stdout.rstrip("\n") == root, payload
        assert result.stderr == ""

    for payload in ("on --help", "on -h"):
        result = _invoke(skill, payload, tmp_path)
        assert result.returncode == EXIT_HELP, (payload, result.stderr)
        assert result.stdout.rstrip("\n") == on, payload


def test_a_help_form_beside_an_instruction_is_refused_without_the_page(
    tmp_path: Path,
) -> None:
    skill = _force_skill(tmp_path)
    page = (skill / "help.md").read_text(encoding="utf-8").rstrip("\n")

    result = _invoke(skill, "--help -- Explain this page", tmp_path)

    assert result.returncode == EXIT_REFUSED
    assert page not in result.stdout
    assert "Explain this page" in result.stdout
    assert result.stderr == ""


def test_an_invalid_form_is_refused_in_the_collections_shape(tmp_path: Path) -> None:
    """One line, the addressed SYNOPSIS verbatim, that page's own help route."""

    skill = _force_skill(tmp_path)

    result = _invoke(skill, "--bogus", tmp_path)

    assert result.returncode == EXIT_REFUSED
    assert result.stderr == ""
    first, _, rest = result.stdout.partition("\n\n")
    assert "--bogus" in first
    assert "\n" not in first.strip()
    assert rest.startswith(_synopsis(skill / "help.md"))
    assert rest.rstrip("\n").endswith("see '/skill --help'")


def test_an_unsatisfied_dependency_refuses_with_the_checkers_payload(
    tmp_path: Path,
) -> None:
    skill = _force_skill(tmp_path, binaries=["definitely-not-a-binary-kntnt"])

    result = _invoke(skill, "--force", tmp_path)

    assert result.returncode == EXIT_REFUSED
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["unsatisfied"][0]["name"] == "definitely-not-a-binary-kntnt"
    assert payload["unsatisfied"][0]["kind"] == "binary"
    assert payload["capabilities"] == []


def test_a_declaration_the_engine_cannot_read_is_refused_like_the_checker(
    tmp_path: Path,
) -> None:
    skill = _force_skill(tmp_path)
    _write(
        skill / "SKILL.md",
        "---\nname: skill\ndescription: A skill.\nargument-hint: '[--force]'\n---\n\n# skill\n",
    )

    result = _invoke(skill, "--force", tmp_path)

    assert result.returncode == EXIT_REFUSED
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["unsatisfied"][0]["kind"] == "declaration"


def test_an_empty_payload_is_the_bare_form(tmp_path: Path) -> None:
    """Valid exactly where the SYNOPSIS admits a form with nothing after the name."""

    admits = _force_skill(tmp_path)
    refuses = _fixture(
        tmp_path,
        "tool",
        "(on|off) [-- <instruction>]",
        ["**/tool** (**on**|**off**) [**--** *INSTRUCTION*]"],
        pages={
            "on": (["**/tool on** [**--** *INSTRUCTION*]"], []),
            "off": (["**/tool off** [**--** *INSTRUCTION*]"], []),
        },
    )

    accepted = _invoke(admits, "", tmp_path)
    assert accepted.returncode == EXIT_VALID, accepted.stderr
    payload = json.loads(accepted.stdout)
    assert (payload["path"], payload["flags"], payload["operands"]) == ([], {}, [])
    assert payload["instruction"] is None

    refused = _invoke(refuses, "", tmp_path)
    assert refused.returncode == EXIT_REFUSED
    assert _synopsis(refuses / "help.md") in refused.stdout
    assert "see '/tool --help'" in refused.stdout


def test_a_subcommand_refusal_addresses_the_most_specific_page(tmp_path: Path) -> None:
    skill = _fixture(
        tmp_path,
        "tool",
        "(on|off) [--yes] [-- <instruction>]",
        ["**/tool** (**on**|**off**) [**--yes**] [**--** *INSTRUCTION*]"],
        ["**--yes**"],
        pages={
            "on": (["**/tool on** [**--yes**] [**--** *INSTRUCTION*]"], ["**--yes**"]),
            "off": (["**/tool off** [**--** *INSTRUCTION*]"], []),
        },
    )

    result = _invoke(skill, "off --yes", tmp_path)

    assert result.returncode == EXIT_REFUSED
    assert _synopsis(skill / "help" / "off.md") in result.stdout
    assert _synopsis(skill / "help.md") not in result.stdout
    assert "see '/tool off --help'" in result.stdout


def test_the_engine_reads_no_grammar_through_the_library_module() -> None:
    """The strict order is what `argument_grammar.split` was written not to enforce."""

    source = KNTNT_PY.read_text(encoding="utf-8")

    assert "argument_grammar" not in source, (
        f"{KNTNT_PY.relative_to(REPO_ROOT)}: the engine reads a Skill's grammar"
        f" from its shipped surfaces itself; `library/scripts/argument_grammar.py`"
        f" belongs to the two engines that refuse in JSON ({RECORD}). See"
        f" {STANDARD}."
    )


# --- Every shipped Skill's grammar ------------------------------------------


def _shipped_skills() -> list[Path]:
    return sorted(SKILLS.glob("*/*/SKILL.md")) + [MANAGER_DIR / "SKILL.md"]


def test_every_shipped_grammar_surface_is_one_the_engine_can_read() -> None:
    """A page the engine cannot read is a Skill whose invocations it cannot judge."""

    engine = _engine()
    pages = [
        page
        for body in _shipped_skills()
        for page in [
            body.parent / "help.md",
            *sorted((body.parent / "help").rglob("*.md")),
        ]
        if page.exists()
    ]

    assert pages

    for page in pages:
        skill_dir = next(
            parent for parent in page.parents if (parent / "SKILL.md").exists()
        )
        grammar = engine.page_grammar(skill_dir, page)
        assert grammar.forms, f"{page.relative_to(REPO_ROOT)}: no form read ({RECORD})."


# Per Skill: the forms its SYNOPSIS admits, with what the engine reads off
# them, and the forms its DIAGNOSTICS refuses. `None` as the expectation means
# refused; a dict is compared as a subset of the reading.
Case = tuple[str, dict[str, Any] | None]

SHIPPED_CASES: dict[str, list[Case]] = {
    "agents/agents-md": [
        ("", {"path": [], "flags": {}, "operands": []}),
        ("--force", {"flags": {"--force": True}}),
        (
            "--force --yes docs/",
            {"flags": {"--force": True, "--yes": True}, "operands": ["docs/"]},
        ),
        ("-- keep it short", {"instruction": "keep it short", "operands": []}),
        ("--bogus", None),
        ("--force=on", None),
        ("--yes --yes", None),
    ],
    "agents/brief": [
        ("on", {"path": ["on"], "operands": []}),
        ("off", {"path": ["off"]}),
        ("status", {"path": ["status"]}),
        (
            "on -- keep the security part",
            {"path": ["on"], "instruction": "keep the security part"},
        ),
        ("", None),
        ("--yes", None),
        ("on off", None),
        ("on the security part", None),
        ("toggle", None),
    ],
    "agents/delegation": [
        ("", {"path": [], "flags": {}}),
        ("on", {"path": ["on"]}),
        (
            "off --project --yes",
            {"path": ["off"], "flags": {"--project": True, "--yes": True}},
        ),
        ("status --user", {"path": ["status"], "flags": {"--user": True}}),
        ("--yes", None),
        ("status --yes", None),
        ("on --project --user", None),
        ("on extra", None),
        ("toggle", None),
    ],
    "agents/tldr": [
        ("", {"operands": []}),
        (
            "bara säkerhetsdelen",
            {"operands": ["bara säkerhetsdelen"], "instruction": None},
        ),
        (
            "-- bara säkerhetsdelen",
            {"operands": [], "instruction": "bara säkerhetsdelen"},
        ),
        ("--only the security part", {"operands": ["--only the security part"]}),
        ("--  ", None),
    ],
    "code/commit": [
        ("", {"flags": {}, "operands": []}),
        ("--yes", {"flags": {"--yes": True}, "operands": []}),
        ("fix the --yes bug", None),
        ("fix the --legacy path", {"flags": {}, "operands": ["fix the --legacy path"]}),
        ("--yes fix it", {"flags": {"--yes": True}, "operands": ["fix it"]}),
        ('"fix the parser"', {"operands": ['"fix the parser"']}),
        ("--bogus fix it", None),
        ("--yes=on", None),
    ],
    "code/push": [
        ("--yes ship it", {"flags": {"--yes": True}, "operands": ["ship it"]}),
        ("--force", None),
    ],
    "code/orchestrate": [
        ("", {"path": [], "operands": []}),
        ("--dry-run", {"flags": {"--dry-run": True}}),
        (
            "--at-once=2 --yes #12 #13",
            {"flags": {"--at-once": "2", "--yes": True}, "operands": ["#12", "#13"]},
        ),
        ("#12", {"operands": ["#12"]}),
        ("reconcile #12", {"path": ["reconcile"], "operands": ["#12"]}),
        (
            "reconcile --commit=abc --yes #12",
            {"path": ["reconcile"], "flags": {"--commit": "abc", "--yes": True}},
        ),
        ("--at-once", None),
        ("reconcile", None),
        ("reconcile --dry-run #12", None),
        ("--bogus", None),
        ("--yes --yes", None),
        # A declared flag after an operand is out of order on the root form too,
        # where the grammar also has command paths (ADR-0176).
        ("#12 --yes", None),
        ("#12 --dry-run", None),
    ],
    "code/ready-for-agent-check": [
        ("", {"operands": []}),
        ("#12 #13", {"operands": ["#12", "#13"]}),
        # No flag and no command path: a dash-prefixed token is a reference the
        # Skill's own step resolves and refuses, never an option (ADR-0176).
        ("--bogus-flag", {"flags": {}, "operands": ["--bogus-flag"]}),
        ("#12 --yes", {"flags": {}, "operands": ["#12", "--yes"]}),
        ("--  ", None),
    ],
    "code/release": [
        ("", {"operands": []}),
        (
            "--no-build --yes minor",
            {"flags": {"--no-build": True, "--yes": True}, "operands": ["minor"]},
        ),
        ("1.2.3", {"operands": ["1.2.3"]}),
        ("--bogus", None),
        ("--yes=on", None),
    ],
    "editorial/proofread": [
        ("", {"flags": {}, "operands": []}),
        (
            "--language=sv report.md",
            {"flags": {"--language": "sv"}, "operands": ["report.md"]},
        ),
        (
            "--in-place report.md",
            {"flags": {"--in-place": True}, "operands": ["report.md"]},
        ),
        ("--in-place=off report.md", {"flags": {"--in-place": "off"}}),
        (
            "--output=out.md Some inline text",
            {"flags": {"--output": "out.md"}, "operands": ["Some inline text"]},
        ),
        (
            "Här är en text att korrekturläsa.",
            {"operands": ["Här är en text att korrekturläsa."]},
        ),
        ("--language", None),
        ("--in-place", None),
        ("--in-place --output=out.md report.md", None),
        ("--language=sv --language=en report.md", None),
    ],
    "editorial/redline": [
        (
            "--genre=essay --max=2 report.md",
            {"flags": {"--genre": "essay", "--max": "2"}},
        ),
        ("--in-place report.md", {"flags": {"--in-place": True}}),
        ("--max", None),
        ("--in-place", None),
        ("--in-place --output=x report.md", None),
    ],
    "editorial/unslop": [
        (
            "--language=sv --max=0 report.md",
            {"flags": {"--language": "sv", "--max": "0"}},
        ),
        ("--in-place=on report.md", {"flags": {"--in-place": "on"}}),
        ("--genre=essay report.md", None),
        ("--in-place", None),
    ],
    "editorial/write": [
        ("", {"operands": []}),
        (
            "--genre=essay --frontmatter=no brief.md",
            {
                "flags": {"--genre": "essay", "--frontmatter": "no"},
                "operands": ["brief.md"],
            },
        ),
        ("Write me a letter", {"operands": ["Write me a letter"]}),
        ("--in-place brief.md", None),
        ("--genre", None),
    ],
    "kntnt": [
        ("", {"path": [], "flags": {}, "operands": []}),
        ("help select", {"path": ["help"], "operands": ["select"]}),
        ("select", {"path": ["select"], "flags": {}}),
        (
            "select --on=a --on=b --yes",
            {"path": ["select"], "flags": {"--on": ["a", "b"], "--yes": True}},
        ),
        ("select --project", {"path": ["select"], "flags": {"--project": True}}),
        (
            "select --project=on --dry-run",
            {"flags": {"--project": "on", "--dry-run": True}},
        ),
        ("select --off=a --yes", {"flags": {"--off": ["a"], "--yes": True}}),
        ("update --yes", {"path": ["update"], "flags": {"--yes": True}}),
        ("update --project=off", {"flags": {"--project": "off"}}),
        (
            "uninstall --yes --dry-run",
            {"path": ["uninstall"], "flags": {"--yes": True, "--dry-run": True}},
        ),
        ("--yes", None),
        ("help --yes", None),
        ("help select --yes", None),
        ("select --force", None),
        ("uninstall --project", None),
        ("updat --yes", None),
        ("select --on", None),
        ("select a", None),
    ],
    "models/model-selector": [
        ("", {"path": [], "operands": []}),
        ("my workload", {"path": [], "operands": ["my workload"]}),
        (
            "--json --kind=implement --scope=callable",
            {
                "path": [],
                "flags": {
                    "--json": True,
                    "--kind": "implement",
                    "--scope": "callable",
                },
            },
        ),
        (
            "--scope=all --data=/x rewrite the parser",
            {
                "flags": {"--scope": "all", "--data": "/x"},
                "operands": ["rewrite the parser"],
            },
        ),
        ("setup", {"path": ["setup"]}),
        ("setup --data=/x", {"path": ["setup"], "flags": {"--data": "/x"}}),
        ("status", {"path": ["status"]}),
        ("update", {"path": ["update"], "flags": {}}),
        ("evidence", {"path": ["evidence"], "operands": []}),
        ("evidence implement", {"path": ["evidence"], "operands": ["implement"]}),
        ("reset", {"path": ["reset"], "flags": {}}),
        (
            "reset --evidence --yes",
            {"path": ["reset"], "flags": {"--evidence": True, "--yes": True}},
        ),
        ("recommend", {"path": [], "operands": ["recommend"]}),
        ("route path", {"path": [], "operands": ["route path"]}),
        ("setup --force", None),
        ("update --force", None),
        ("status extra", None),
        ("update --evidence", None),
        ("reset --json", None),
        ("my workload --yes", None),
    ],
    "producivity/rename-invoices": [
        ("--type=invoice", {"flags": {"--type": "invoice"}, "operands": []}),
        (
            "--folder=/x --type=invoice --locale=sv --locale=en --yes",
            {
                "flags": {
                    "--folder": "/x",
                    "--type": "invoice",
                    "--locale": ["sv", "en"],
                    "--yes": True,
                }
            },
        ),
        (
            "--type=x --no-config --locale=sv --dry-run",
            {
                "flags": {
                    "--type": "x",
                    "--no-config": True,
                    "--locale": ["sv"],
                    "--dry-run": True,
                }
            },
        ),
        (
            "--type=x --counterparty-source=issuer",
            {"flags": {"--type": "x", "--counterparty-source": "issuer"}},
        ),
        ("", None),
        ("--type=x --yes --dry-run", None),
        ("--type=x --config=a --no-config", None),
        ("--type", None),
    ],
}


def test_the_case_table_covers_every_shipped_skill() -> None:
    """A Skill added without a row here is a grammar the engine is never held to."""

    shipped = {str(body.parent.relative_to(SKILLS)) for body in _shipped_skills()}

    assert shipped == set(SHIPPED_CASES)


def _subset(expected: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(key) == value for key, value in expected.items())


def test_every_shipped_skills_documented_forms_are_read_as_its_pages_state_them() -> (
    None
):
    """Valid forms accepted, DIAGNOSTICS refusals refused, on the real shipped pages."""

    engine = _engine()

    for relative, cases in SHIPPED_CASES.items():
        directory = SKILLS / relative
        for payload, expected in cases:
            reading = engine.read_invocation(directory, payload)
            if expected is None:
                assert reading.status == EXIT_REFUSED, (
                    f"/{directory.name} {payload!r}: the page refuses this form"
                    f" and the engine accepted it ({RECORD}). See {STANDARD}."
                )
                assert "see '/" in reading.text, (relative, payload, reading.text)
                assert "--help'" in reading.text, (relative, payload, reading.text)
            else:
                assert reading.status == EXIT_VALID, (
                    f"/{directory.name} {payload!r}: the SYNOPSIS admits this"
                    f" form and the engine refused it: {reading.text}"
                    f" ({RECORD}). See {STANDARD}."
                )
                assert reading.invocation is not None
                assert _subset(expected, reading.invocation), (
                    relative,
                    payload,
                    reading.invocation,
                )


def test_every_shipped_skill_routes_its_help_forms_to_its_pages() -> None:
    """Root help forms print `help.md`; a command path's help form prints its page."""

    engine = _engine()

    for body in _shipped_skills():
        directory = body.parent
        root = (directory / "help.md").read_text(encoding="utf-8").rstrip("\n")
        for payload in ("--help", "-h", "help"):
            reading = engine.read_invocation(directory, payload)
            assert reading.status == EXIT_HELP, (directory.name, payload)
            assert reading.text.rstrip("\n") == root, (directory.name, payload)

        for page in sorted((directory / "help").rglob("*.md")):
            path = " ".join(page.relative_to(directory / "help").with_suffix("").parts)
            reading = engine.read_invocation(directory, f"{path} --help")
            assert reading.status == EXIT_HELP, (directory.name, path)
            assert reading.text.rstrip("\n") == page.read_text(encoding="utf-8").rstrip(
                "\n"
            )


def test_a_refusal_quotes_the_addressed_pages_own_synopsis_and_route() -> None:
    """The Manager uses the common engine refusal for its addressed page."""

    engine = _engine()

    reading = engine.read_invocation(MANAGER_DIR, "select --force")

    assert reading.status == EXIT_REFUSED
    assert reading.text.startswith("'/kntnt select' takes no '--force'\n\n")
    assert _synopsis(MANAGER_DIR / "help" / "select.md") in reading.text
    assert reading.text.rstrip("\n").endswith("see '/kntnt select --help'")

    reading = engine.read_invocation(MANAGER_DIR, "updat --yes")

    assert reading.status == EXIT_REFUSED
    assert reading.text.startswith("unknown command 'updat'\n\n")
    assert _synopsis(MANAGER_DIR / "help.md") in reading.text
    assert reading.text.rstrip("\n").endswith("see '/kntnt --help'")


# --- The Manager on the engine -----------------------------------------------


def test_the_managers_own_directory_passes_the_dependency_gate(tmp_path: Path) -> None:
    """`invoke --here=<manager>` answers, although the Manager carries no marker.

    The Manager is no Catalog entry and the sweep must never read it as one,
    so its `SKILL.md` carries no `kntnt.` key — the one shape the gate
    otherwise refuses as an unreadable declaration (ADR-0175). Asked about
    itself it declares nothing: `uv`, its one dependency, is what runs the
    check, and a body that calls the engine has no other preamble to make.
    """

    result = _invoke(MANAGER_DIR, "", tmp_path)

    assert result.returncode == EXIT_VALID, (result.stdout, result.stderr)
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["path"] == []
    assert payload["dependencies"] == {
        "ok": True,
        "unsatisfied": [],
        "capabilities": [],
    }

    result = _invoke(MANAGER_DIR, "select --help", tmp_path)

    assert result.returncode == EXIT_HELP, (result.stdout, result.stderr)
    assert result.stdout.rstrip("\n") == (
        (MANAGER_DIR / "help" / "select.md").read_text(encoding="utf-8").rstrip("\n")
    )


def test_manager_refusals_use_the_engine_diagnostics_and_route(tmp_path: Path) -> None:
    """Manager refusals use the addressed page's common engine contract."""

    cases = (
        (
            "help --yes",
            "'/kntnt help' takes no '--yes'",
            MANAGER_DIR / "help" / "help.md",
            "/kntnt help --help",
        ),
        (
            "help select --yes",
            "'/kntnt help' takes no '--yes'",
            MANAGER_DIR / "help" / "help.md",
            "/kntnt help --help",
        ),
        ("sel", "unknown command 'sel'", MANAGER_DIR / "help.md", "/kntnt --help"),
        (
            "select --force",
            "'/kntnt select' takes no '--force'",
            MANAGER_DIR / "help" / "select.md",
            "/kntnt select --help",
        ),
        (
            "uninstall --project",
            "'/kntnt uninstall' takes no '--project'",
            MANAGER_DIR / "help" / "uninstall.md",
            "/kntnt uninstall --help",
        ),
        (
            "update --on=foo",
            "'/kntnt update' takes no '--on'",
            MANAGER_DIR / "help" / "update.md",
            "/kntnt update --help",
        ),
    )

    for payload, problem, page, route in cases:
        result = _invoke(MANAGER_DIR, payload, tmp_path)

        expected = f"{problem}\n\n{_synopsis(page)}\n\nsee '{route}'\n"
        assert result.returncode == EXIT_REFUSED, payload
        assert result.stdout == expected, payload
        assert result.stderr == "", payload


def test_manager_refusals_name_what_the_script_named_before_the_move() -> None:
    """Every documented Manager refusal keeps its substance across the move.

    Before the body moved onto the engine each of these forms reached the
    script, whose refusal named the stray flag, quoted the addressed verb's
    SYNOPSIS and pointed at its page. The engine's refusal names the same
    flag and quotes the same SYNOPSIS. Only the spelling is the engine's —
    `'/kntnt select' takes no '--force'` and `see '/kntnt select --help'`
    where the script wrote `select takes no '--force'` and `see '/kntnt help
    select'` — which is the one contract ADR-0181 gives every Skill, on
    stdout, and the two routes open the same page.
    """

    engine = _engine()
    cases = (
        ("select --force", ["plan", "select", "--force"], "--force"),
        ("uninstall --project", ["plan", "uninstall", "--project"], "--project"),
        ("update --on=foo", ["apply", "update", "--on=foo"], "--on"),
        ("help --yes", ["help", "--yes"], "--yes"),
        ("help select --yes", ["help", "select", "--yes"], "--yes"),
    )

    for payload, argv, flag in cases:
        reading = engine.read_invocation(MANAGER_DIR, payload)
        with pytest.raises(engine.ManagerError) as refused:
            engine.parse_args(argv)
        before = str(refused.value)

        assert reading.status == EXIT_REFUSED, payload
        assert refused.value.code == EXIT_REFUSED, payload
        engine_first, _, engine_rest = reading.text.partition("\n\n")
        script_first, _, script_rest = before.partition("\n\n")
        assert f"'{flag}" in engine_first and f"'{flag}" in script_first, payload
        engine_synopsis = engine_rest.rpartition("\n\nsee '")[0]
        script_synopsis = script_rest.rpartition("\n\nsee '")[0]
        assert engine_synopsis == script_synopsis, payload
        assert reading.text.rstrip("\n").endswith("--help'"), payload


# --- The record and the rule --------------------------------------------------


def test_the_record_and_the_rule_state_the_engine() -> None:
    records = sorted((REPO_ROOT / "docs" / "adr").glob("0181-*.md"))
    assert len(records) == 1, "one record at the next free number"
    record = records[0].read_text(encoding="utf-8")
    assert "invoke" in record
    assert "ADR-0176" in record and "ADR-0177" in record

    rule = (REPO_ROOT / STANDARD).read_text(encoding="utf-8")
    assert 'invoke --here="$HERE"' in rule
    assert "stdin" in rule
    assert RECORD in rule
    for key in ("`path`", "`flags`", "`operands`", "`instruction`", "`dependencies`"):
        assert key in rule, f"{STANDARD} states the JSON shape: {key}"
