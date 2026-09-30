# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Read the profile's choices against the local catalogue, without selection."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import catalogue
import profiles

# The Maker names used by the setup interview, with unknown ids kept verbatim.
MAKER_NAMES: dict[str, str] = {
    "anthropic": "Claude",
    "openai": "GPT",
    "spacexai": "Grok",
}


def read(data_dir: Path, here: Path) -> str:
    """List only profile choices, taking one current release per selected series."""

    cat = catalogue.load(data_dir, here)
    profile = profiles.load(data_dir, cat)
    if profile.source != "file":
        return f"No configured models can be listed: {profile.problem}"

    # Membership and release order belong to the existing shared contracts.
    releases: dict[tuple[str, str], str] = {}
    for model in catalogue.newest_first(cat.models):
        if profiles.allows(profile, model):
            releases.setdefault((model.provider, model.family.lower()), model.id)

    # Retain explicit choices even when the local catalogue has no release.
    for provider, names in profile.families.items():
        for family in names:
            releases.setdefault((provider, family), "no catalogue release")

    lines = [
        "Harnesses:",
        *(f"  {h}" for h in sorted(set(profile.harnesses))),
        "Models:",
    ]
    for provider in sorted(profile.makers, key=lambda p: (MAKER_NAMES.get(p, p), p)):
        lines.append(f"  {MAKER_NAMES.get(provider, provider)}:")
        for (maker, family), identifier in sorted(releases.items()):
            if maker == provider:
                lines.append(f"    {family}: {identifier}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    """Print the local inventory, with the same data directory as other readers."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(catalogue.default_data()))
    args = parser.parse_args(argv)
    print(read(Path(args.data).expanduser(), Path(__file__).resolve().parent.parent))
    return 0


if __name__ == "__main__":
    sys.exit(main())
