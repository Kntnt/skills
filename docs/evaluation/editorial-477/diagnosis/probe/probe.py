"""A neutral diagnostic probe of one saved state of a Redline run (#477).

It is not a Redline run. It hands a fresh top-level session the state the
historical run stood in once its reply checker returned: the two texts, the
drafted reply the checker read, the checker's return, and the instructions a
run follows with that return, in one of two wordings. It asks for the reply
the run now delivers. Nothing else of the run is replayed.

The two texts, the drafted reply and the checker's return are read from
`../historical/`, written there by `../../runs/states.py` from #475's packet
`post-control-case-study-clean`. `--wording` is the revision whose
`reply-check.md` supplies the instructions: `fb169087`, where the build
started, or `51777db2`, the candidate. Each run's `prompt.txt` holds the whole
prompt it was sent.
"""

import argparse
import json
import subprocess
import sys
import uuid
from pathlib import Path

HARNESS = Path(
    "/Users/thomas/Projects/skills/.git/kntnt-orchestrate/477/docs/evaluation/editorial-388/harness"
)
sys.path.insert(0, str(HARNESS))
import staged_run

HERE = Path(__file__).resolve().parent.parent / "historical"
REPOSITORY = Path(__file__).resolve().parents[4]


def at(revision: str, path: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{revision}:{path}"], cwd=REPOSITORY, text=True
    )


def truth() -> str:
    delivery = at("fb169087", "skills/kntnt/library/references/delivery.md")
    start = delivery.index("## The truth of a report about the text")
    end = delivery.index("\n## ", start + 1)
    return delivery[start : end + 1]


def section(brief: str) -> str:
    parent = brief.split("\n---\n", 1)[0]
    start = parent.index("**What you do with what it returns.**")
    return parent[start:].strip()


def prompt(wording: str) -> str:
    read = lambda name: (HERE / name).read_text(encoding="utf-8")
    return f"""You are the reviewing run that reviewed the text below, corrected it in one round, ran the closing proofreading pass, and drafted the reply below. Before delivering anything you started a fresh checker on the two texts and your drafted reply. The checker has now returned. The run was aimed at the response: `input.md` is untouched, and every private file of the run has been removed.

These are your instructions for what follows the check, word for word:

> Once the reply is drafted, and before anything is delivered, have that check made by a fresh subagent started from `reply-check.md`, filled in and delivered as that brief says, and correct only the reply from what it returns.

{section(at(wording, "skills/editorial/redline/references/reply-check.md"))}

`$LIBRARY/references/delivery.md` says this in the section it names:

{truth()}

**The text as it arrived.**

````markdown
{read("received.md")}````

**The text as delivered** (the final Text Artifact; it is delivered after the reply, inside one fenced code block, and is not yours to change):

````markdown
{read("delivered.md")}````

**The reply as you drafted it**, which is what the checker read:

````markdown
{read("draft-reply.md")}````

**What the checker returned:**

{read("check-return.md")}

Write the reply you now deliver, whole, in the language of the text, exactly as it will reach the reader, and nothing else: no preamble, no note on what you changed, and not the delivered text itself, which follows it unchanged.
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wording", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    text = prompt(args.wording)
    (out / "prompt.txt").write_text(text, encoding="utf-8")
    with staged_run.private_root(out) as root:
        home = root / "home" / ".claude"
        home.mkdir(parents=True)
        (root / "scratch" / "tmp").mkdir(parents=True)
        (root / "work").mkdir()
        source = staged_run.install_credential(home / staged_run.CREDENTIALS)
        command = [
            "claude",
            "--print",
            "--session-id",
            str(uuid.uuid4()),
            "--model",
            "claude-opus-5-5",
            "--effort",
            "high",
            "--tools",
            "",
            "--strict-mcp-config",
            "--output-format",
            "json",
        ]
        done = subprocess.run(
            command,
            input=text,
            capture_output=True,
            text=True,
            cwd=root / "work",
            env=staged_run.environment(root),
            timeout=1800,
            check=False,
        )
    (out / "stderr.txt").write_text(done.stderr, encoding="utf-8")
    result = json.loads(done.stdout)
    (out / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "reply.md").write_text(result.get("result", ""), encoding="utf-8")
    (out / "run.json").write_text(
        json.dumps(
            {
                "wording": args.wording,
                "command": command,
                "credential_source": source,
                "exit": done.returncode,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return done.returncode


if __name__ == "__main__":
    raise SystemExit(main())
