"""Write each probe's record into the packet, from its run record and its stream."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from summarise import PACKET, summarise

S = Path(__file__).parent
DENIED = {"Agent", "Task", "Workflow"}
HARNESS_PREFIXES = (
    ".claude/.claude.json",
    ".claude/.last-cleanup",
    ".claude/backups",
    ".claude/plugins",
    ".claude/projects",
    ".claude/session-env",
    ".claude/sessions",
    ".claude/shell-snapshots",
    ".claude/skills/synced",
)


def changed_by(call: dict) -> str:
    if call["name"] == "ToolSearch":
        return "nothing: a lookup among the session's deferred tools"
    command = call["input"].get("command", "")
    if call["name"] == "Bash" and "scripts/invoke.py" in command:
        return "nothing: the shim call, which reads the invocation and prints the reading sheet"
    return "UNCLASSIFIED"


def diff(before: dict, after: dict) -> dict:
    return {
        "created": sorted(set(after) - set(before)),
        "removed": sorted(set(before) - set(after)),
        "changed": sorted(p for p in set(before) & set(after) if before[p] != after[p]),
    }


for skill in ("orchestrate", "ready-for-agent-check", "delegation"):
    for n in ("1", "2", "3"):
        name = f"{skill}-{n}"
        run = json.loads((S / f"{name}.record.json").read_text())
        s = summarise(name, full=True)
        calls = [
            {
                "order": i,
                "tool": c["name"],
                "input": c["input"],
                "result_is_error": c["result_is_error"],
                "result": c["result"],
                "changed": changed_by(c),
            }
            for i, c in enumerate(s["calls"], 1)
        ]
        record = {
            "skill": skill,
            "probe": int(n),
            "void": False,
            "command_line": run["argv"],
            "working_directory": run["working_directory"],
            "environment": run["environment"],
            "harness": run["harness"],
            "base_commit": run["base_commit"],
            "stream": f"{name}.jsonl",
            "session_id": s["session_id"],
            "init_model": s["model"],
            "init_tools": s["init_tools"],
            "init_tools_denied_present": sorted(set(s["init_tools"]) & DENIED),
            "tool_calls": calls,
            "reply": s["reply"],
            "harness_result": s["result"],
            "process": run["outcome"],
        }
        if skill == "delegation":
            before, after = run["listing_before"], run["listing_after"]
            record["credential_source"] = run["credential_source"]
            record["listing_before"] = before
            record["listing_after"] = after
            record["listing_diff"] = {k: diff(before[k], after[k]) for k in before}
            home = record["listing_diff"]["home"]
            record["listing_diff_outside_harness_state"] = {
                "repo": record["listing_diff"]["repo"],
                "home": {
                    k: [p for p in v if not p.startswith(HARNESS_PREFIXES)]
                    for k, v in home.items()
                },
            }
        else:
            record["git_status_porcelain_before"] = run["git_before"][
                "status_porcelain"
            ]
            record["git_status_porcelain_after"] = run["git_after"]["status_porcelain"]
            record["worktree_list_unchanged"] = (
                run["git_before"]["worktrees"] == run["git_after"]["worktrees"]
            )
        (PACKET / f"{name}.record.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n"
        )
        print(
            name,
            [c["tool"] for c in calls],
            [c["changed"][:8] for c in calls],
            record["init_tools_denied_present"],
            record.get("listing_diff_outside_harness_state")
            or (
                record["git_status_porcelain_before"]
                == record["git_status_porcelain_after"],
                record["worktree_list_unchanged"],
            ),
        )
