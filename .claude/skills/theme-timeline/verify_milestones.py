#!/usr/bin/env python3
"""Verify each milestone quote `en` is an exact ordered substring of split/Ra_Session_XXX.md.

Usage: python3 verify_milestones.py <milestones.json>

Exits 0 if all quotes verify, 1 otherwise.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # 仓库根目录
WS = re.compile(r"\s+")


def norm(s: str) -> str:
    return WS.sub(" ", s).strip()


def main() -> int:
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    cache = {}
    bad = []
    total = 0
    for m in data:
        s = m["session"]
        if s not in cache:
            cache[s] = norm((ROOT / f"split/Ra_Session_{s:03d}.md").read_text(encoding="utf-8"))
        hay = cache[s]
        for q in m["quotes"]:
            total += 1
            en = q["en"]
            probe = en[:-1].rstrip() if en.endswith("…") else en
            probe = norm(probe)
            if probe not in hay:
                bad.append((s, m["ref"], m["title"], en[:90]))

    # duplicate session+ref check
    seen = {}
    for m in data:
        k = (m["session"], m["ref"])
        seen[k] = seen.get(k, 0) + 1

    print(f"milestones: {len(data)}  quotes: {total}")
    sessions = sorted(set(m["session"] for m in data))
    print(f"sessions covered: {len(sessions)}  {sessions}")
    from collections import Counter
    print("subthemes:", dict(Counter(m["subtheme"] for m in data)))
    print("weights:", dict(Counter(m["weight"] for m in data)))
    dup = {k: v for k, v in seen.items() if v > 1}
    if dup:
        print("DUPLICATE session/ref:", dup)
    if bad:
        print(f"FAILED quotes: {len(bad)}")
        for s, ref, title, frag in bad:
            print(f"  s{s} {ref} [{title}] {frag!r}")
        return 1
    print("all quotes verified as exact substrings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())