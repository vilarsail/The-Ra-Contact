#!/usr/bin/env python3
"""Extract English paragraphs mentioning a concept from split/Ra_Session_*.md.

Usage: python3 extract_theme.py <concept_key> <out.json>

Output: JSON list of {session, ref, speaker, text, terms}
speaker: Q (Questioner) / Ra / - (continuation or other)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # 仓库根目录

CONCEPTS = {
    "density": [r"\bdensit(?:y|ies)\b"],
    "harvest": [r"\bharvest(?:ing|ed|able|ability)?\b"],
    "polarity": [r"\bpolarit(?:y|ies)\b", r"\bpolariz\w+\b"],
    "catalyst": [r"\bcatalysts?\b"],
}

CJK = re.compile(r"[\u4e00-\u9fff]")
BLOCK = re.compile(r"^##\s*\((\d+\.\d+)\)\s*$", re.M)
REF_PREFIX = re.compile(r"^\(\d+\.\d+\)\s*")


def is_english(par: str) -> bool:
    if CJK.search(par):
        return False
    return sum(ch.isascii() and ch.isalpha() for ch in par) >= 20


def speaker_of(par: str) -> str:
    body = REF_PREFIX.sub("", par)
    if body.startswith("Questioner"):
        return "Q"
    if body.startswith("Ra"):
        return "Ra"
    return "-"


def main() -> int:
    key, out = sys.argv[1], sys.argv[2]
    pats = [re.compile(p, re.I) for p in CONCEPTS[key]]
    hits = []
    for f in sorted(ROOT.glob("split/Ra_Session_*.md")):
        session = int(re.search(r"(\d+)", f.name).group(1))
        text = f.read_text(encoding="utf-8")
        marks = [(m.start(), m.group(1)) for m in BLOCK.finditer(text)]
        if not marks:
            continue
        marks.append((len(text), None))
        for i in range(len(marks) - 1):
            chunk = text[marks[i][0]:marks[i + 1][0]]
            ref = marks[i][1]
            for par in re.split(r"\n\s*\n", chunk):
                par = par.strip()
                if not par or not is_english(par):
                    continue
                found = [p.search(par).group(0).lower() for p in pats if p.search(par)]
                if found:
                    hits.append({
                        "session": session,
                        "ref": ref,
                        "speaker": speaker_of(par),
                        "text": par,
                        "terms": sorted(set(found)),
                    })
    Path(out).write_text(json.dumps(hits, ensure_ascii=False, indent=1), encoding="utf-8")
    per = {}
    for h in hits:
        per[h["session"]] = per.get(h["session"], 0) + 1
    print(f"paragraphs with hits: {len(hits)}")
    print(f"sessions touched: {len(per)} / 106")
    print("top sessions:", sorted(per.items(), key=lambda kv: -kv[1])[:10])
    print("zero-hit sessions:", [s for s in range(1, 107) if s not in per])
    print("Q vs Ra:", sum(1 for h in hits if h["speaker"] == "Q"), sum(1 for h in hits if h["speaker"] == "Ra"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())