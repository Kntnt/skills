"""Share of a drafted reply's sentences that reach the delivered reply verbatim."""

import re
import sys
from pathlib import Path


def sentences(text: str) -> list[str]:
    text = re.sub(r"[*`]", "", text)
    parts = re.split(r"(?<=[.!?:])\s+|\n+", text)
    return [p.strip(" -–") for p in parts if len(p.strip(" -–").split()) >= 4]


draft, final = (Path(p).read_text(encoding="utf-8") for p in sys.argv[1:3])
flagged = [q for q in sys.argv[3:]]
flat = re.sub(r"[*`]", "", final)
flat = re.sub(r"\s+", " ", flat)
kept = changed = 0
for s in sentences(draft):
    if any(q in s for q in flagged):
        continue
    if re.sub(r"\s+", " ", s) in flat:
        kept += 1
    else:
        changed += 1
        print("CHANGED:", s)
print(f"unflagged sentences kept verbatim: {kept} of {kept + changed}")
