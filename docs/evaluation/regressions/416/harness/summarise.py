"""Print what one probe stream shows: the seat, each tool call in order, and the reply."""

import json
import sys
from pathlib import Path

PACKET = Path(
    "/Users/thomas/Projects/skills/.git/kntnt-orchestrate/416/docs/evaluation/regressions/416"
)


def summarise(name: str, full: bool = False) -> dict:
    events = [
        json.loads(l)
        for l in (PACKET / f"{name}.jsonl").read_text().splitlines()
        if l.strip()
    ]
    init = next(
        e for e in events if e.get("type") == "system" and e.get("subtype") == "init"
    )
    results = {}
    calls = []
    for e in events:
        if e.get("type") == "user":
            for c in (
                e.get("message", {}).get("content", [])
                if isinstance(e.get("message", {}).get("content"), list)
                else []
            ):
                if c.get("type") == "tool_result":
                    content = c.get("content")
                    if isinstance(content, list):
                        content = "\n".join(
                            x.get("text", "") for x in content if isinstance(x, dict)
                        )
                    results[c["tool_use_id"]] = {
                        "is_error": c.get("is_error", False),
                        "text": content,
                    }
    for e in events:
        if e.get("type") == "assistant":
            for c in e["message"].get("content", []):
                if c.get("type") == "tool_use":
                    calls.append(
                        {"id": c["id"], "name": c["name"], "input": c["input"]}
                    )
    for c in calls:
        r = results.get(c["id"], {})
        c["result_is_error"] = r.get("is_error")
        text = r.get("text") or ""
        c["result"] = text if full else text[:600]
    result = next((e for e in events if e.get("type") == "result"), {})
    return {
        "init_tools": init.get("tools"),
        "denied_present": sorted(
            set(init.get("tools", [])) & {"Agent", "Task", "Workflow"}
        ),
        "model": init.get("model"),
        "session_id": init.get("session_id"),
        "calls": calls,
        "reply": result.get("result"),
        "result": {
            k: result.get(k)
            for k in (
                "subtype",
                "is_error",
                "num_turns",
                "total_cost_usd",
                "duration_ms",
                "api_error_status",
            )
        },
    }


if __name__ == "__main__":
    s = summarise(sys.argv[1], full="--full" in sys.argv)
    if "--json" in sys.argv:
        print(json.dumps(s, indent=2))
    else:
        print("tools:", s["init_tools"])
        print("denied present:", s["denied_present"], "model:", s["model"])
        for i, c in enumerate(s["calls"], 1):
            print(f"--- call {i}: {c['name']} {json.dumps(c['input'])[:800]}")
            print(f"    -> error={c['result_is_error']} {c['result'][:1500]!r}")
        print("=== reply:", s["reply"])
        print("=== result:", s["result"])
