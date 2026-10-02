# /// script
# requires-python = ">=3.12"
# ///
"""Expose a packet through neutral file names over the native MCP boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def serve(root: Path, report: str, log: Path) -> None:
    """Read only staged materials and write only the designated reader report."""

    # Map public names explicitly; neither traversal nor host paths are accepted.
    paths = {
        "/run/" + str(path.relative_to(root)): path
        for path in root.rglob("*")
        if path.is_file()
    }
    destination = "/run/" + report
    tools = [
        {
            "name": "read_file",
            "description": "Read a named file in the run directory.",
            "inputSchema": {
                "type": "object",
                "properties": {"path": {"type": "string", "enum": list(paths)}},
                "required": ["path"],
                "additionalProperties": False,
            },
        },
        {
            "name": "write_file",
            "description": "Write the designated report in the run directory.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "enum": [destination]},
                    "contents": {"type": "string"},
                },
                "required": ["path", "contents"],
                "additionalProperties": False,
            },
        },
    ]

    # Keep RPC requests attributable outside the reader's visible namespace.
    with log.open("a") as ledger:
        for line in sys.stdin:
            message = json.loads(line)
            ledger.write(json.dumps(message, ensure_ascii=False) + "\n")
            ledger.flush()
            if "id" not in message:
                continue
            method = message["method"]
            result: dict[str, Any]
            if method == "initialize":
                result = {
                    "protocolVersion": message["params"]["protocolVersion"],
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": "materials", "version": "1.0.0"},
                }
            elif method == "tools/list":
                result = {"tools": tools}
            elif method == "tools/call":
                params = message["params"]
                arguments = params["arguments"]
                path = arguments.get("path")
                if params["name"] == "read_file" and path in paths:
                    result = {
                        "content": [{"type": "text", "text": paths[path].read_text()}]
                    }
                elif params["name"] == "write_file" and path == destination:
                    (root / report).write_text(arguments["contents"])
                    result = {
                        "content": [{"type": "text", "text": f"Written: {destination}"}]
                    }
                else:
                    result = {
                        "isError": True,
                        "content": [
                            {"type": "text", "text": "Use a designated run file."}
                        ],
                    }
            else:
                result = {}
            print(
                json.dumps(
                    {"jsonrpc": "2.0", "id": message["id"], "result": result},
                    ensure_ascii=False,
                ),
                flush=True,
            )


def main() -> None:
    """Start the packet-specific adapter without exposing host configuration."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--log", type=Path, required=True)
    args = parser.parse_args()
    serve(args.root, args.report, args.log)


if __name__ == "__main__":
    main()
