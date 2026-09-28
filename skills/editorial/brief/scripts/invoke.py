# /// script
# requires-python = ">=3.12"
# ///
"""Hand this Skill's invocation to the Manager's engine, wherever the Manager is.

A body cannot say where the Manager is, because nothing has found it yet when
the body is read: it is beside this Skill when both were Enabled at one layer,
and under a Global harness skills directory when the Skill was Enabled for a
Project and the Manager for the machine. Finding it is deterministic, so a
script does it and the body says one sentence — run this, on stdin, and do what
it prints. The engine's three answers pass through untouched: the exit status
is its, stdout is its, and this script adds a line of its own only where the
engine could not answer at all, no Manager being found or the one found
predating the engine.

Every Skill of the collection carries this file byte for byte, because the
Library that would hold one copy is what this file exists to find. The Global
list is the Manager's `harness-paths.json` read into a tuple, and the suite
holds the two equal.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
MANAGER = "kntnt"
ENGINE = Path("scripts") / "kntnt.py"

# The Global skills directory of every Harness the Manager knows, from its
# `harness-paths.json`; `~` is the home the Manager itself resolves against.
GLOBAL_SKILLS = (
    "~/.adal/skills",
    "~/.agents/skills",
    "~/.aider-desk/skills",
    "~/.astrbot/data/skills",
    "~/.augment/skills",
    "~/.autohand/skills",
    "~/.bob/skills",
    "~/.claude/skills",
    "~/.codeartsdoer/skills",
    "~/.codebuddy/skills",
    "~/.codeium/windsurf/skills",
    "~/.codemaker/skills",
    "~/.codestudio/skills",
    "~/.codex/skills",
    "~/.commandcode/skills",
    "~/.config/agents/skills",
    "~/.config/crush/skills",
    "~/.config/devin/skills",
    "~/.config/goose/skills",
    "~/.config/kimchi/harness/skills",
    "~/.config/opencode/skills",
    "~/.continue/skills",
    "~/.copilot/skills",
    "~/.cursor/skills",
    "~/.deepagents/agent/skills",
    "~/.factory/skills",
    "~/.firebender/skills",
    "~/.forge/skills",
    "~/.gemini/antigravity-cli/skills",
    "~/.gemini/antigravity/skills",
    "~/.gemini/skills",
    "~/.grok/skills",
    "~/.hermes/skills",
    "~/.iflow/skills",
    "~/.inferencesh/skills",
    "~/.jazz/skills",
    "~/.junie/skills",
    "~/.kilocode/skills",
    "~/.kiro/skills",
    "~/.kode/skills",
    "~/.lingma/skills",
    "~/.mcpjam/skills",
    "~/.minimax/skills",
    "~/.moxby/skills",
    "~/.mux/skills",
    "~/.neovate/skills",
    "~/.ona/skills",
    "~/.openclaw/skills",
    "~/.openhands/skills",
    "~/.pi/agent/skills",
    "~/.pochi/skills",
    "~/.qoder-cn/skills",
    "~/.qoder/skills",
    "~/.qwen/skills",
    "~/.reasonix/skills",
    "~/.roo/skills",
    "~/.rovodev/skills",
    "~/.snowflake/cortex/skills",
    "~/.tabnine/agent/skills",
    "~/.terramind/skills",
    "~/.tinycloud/skills",
    "~/.trae-cn/skills",
    "~/.trae/skills",
    "~/.vibe/skills",
    "~/.zcode/skills",
    "~/.zencoder/skills",
)

NO_MANAGER = (
    "No Manager was found beside this Skill or under a Global harness skills"
    " directory. Install it with `npx skills add Kntnt/skills`, then invoke the"
    " Skill again."
)
OUTDATED_MANAGER = (
    "The installed Manager predates the invocation engine. Run `/kntnt update`,"
    " then invoke the Skill again."
)


def home() -> Path:
    """The home Global paths resolve against, as the Manager resolves it."""

    return Path(os.environ.get("KNTNT_HOME", str(Path.home())))


def manager() -> Path | None:
    """The first Manager directory that holds an engine: beside this Skill, else Global."""

    candidates = (
        HERE.parent / MANAGER,
        *(
            home() / directory.removeprefix("~/") / MANAGER
            for directory in GLOBAL_SKILLS
        ),
    )
    return next((c for c in candidates if (c / ENGINE).is_file()), None)


def main() -> int:
    """Run the engine on stdin and answer as it answered."""

    found = manager()
    if found is None:
        print(NO_MANAGER)
        return 2

    # The engine reads the Project layer off the working directory the user
    # stands in, so the call inherits the caller's working directory.
    result = subprocess.run(
        ["uv", "run", "--quiet", str(found / ENGINE), "invoke", f"--here={HERE}"],
        stdin=sys.stdin,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    # An older Manager has no `invoke` verb; argparse says so on stderr, and
    # the fix is the Manager's own Update rather than that message.
    if result.returncode != 0 and "invalid choice: 'invoke'" in result.stderr:
        print(OUTDATED_MANAGER)
        return 2
    sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
