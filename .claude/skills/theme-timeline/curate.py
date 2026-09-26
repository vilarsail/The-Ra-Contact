#!/usr/bin/env python3
"""Curate 68 raw milestones down to the final timeline dataset with era assignment.

Usage: python3 curate.py
Output: milestones_final.json  (list of milestones with `era` 1..5)
"""
import json
import re
from pathlib import Path

DIR = Path(__file__).resolve().parent
WS = re.compile(r"\s+")

ERAS = [
    (1, "命名与阶梯", "1–15 集", "密度先有了名字（爱、光），再被编上序号，成为一条连续递进的意识阶梯。"),
    (2, "结构定形", "16–30 集", "密度被定义成数学式的音阶结构：七个密度、七个子密度、无限细分，并可计数。"),
    (3, "色彩·身体·极化", "31–50 集", "密度长出了颜色与身体：真实颜色、七重载具、能量中心，以及只属于第三密度的极化。"),
    (4, "循环与八度", "51–71 集", "密度被放进更大的循环里：八度既是终点也是起点，而行星、高我、个体各自有其密度刻度。"),
    (5, "边界与载体", "72–106 集", "收束：第三密度是一次选择，密度之间可渗透，载具不加速成长、只允许成长。"),
]

PICKS = {
    1: ["1.1", "6.14", "6.15", "7.16", "9.14", "13.16", "13.22", "14.32"],
    2: ["16.27", "16.50", "16.51", "19.2", "27.13", "28.15", "30.1", "30.5"],
    3: ["36.12", "38.7", "39.4", "40.3", "40.6", "43.13", "47.3", "47.8", "50.7"],
    4: ["52.12", "54.4", "62.29", "63.8", "67.6", "70.9", "71.12"],
    5: ["76.16", "78.24", "82.12", "82.29", "87.6", "89.12", "90.25", "105.16"],
}

SPECIAL = {
    "16.51": lambda z: z.replace("本区间最核心的定义节点", "全书最核心的定义节点"),
    "90.25": lambda z: z.replace(
        "并首次出现「次密度」这一刻度",
        "并明确次密度之间的通讯",
    ),
}

# 该节点所聚焦的密度层级。0 = 整条阶梯／总论，1..8 = 第一至第八密度。
# 判据是「这一节点主要在谈哪一层」，而非「文本里出现过哪些数字」。
LEVELS = {
    "1.1": 0, "6.14": 4, "6.15": 3, "7.16": 0, "9.14": 2, "13.16": 1,
    "13.22": 4, "14.32": 8,
    "16.27": 0, "16.50": 4, "16.51": 0, "19.2": 2, "27.13": 4,
    "28.15": 8, "30.1": 3, "30.5": 3,
    "36.12": 6, "38.7": 4, "39.4": 7, "40.3": 0, "40.6": 0, "43.13": 4,
    "47.3": 4, "47.8": 0, "50.7": 4,
    "52.12": 0, "54.4": 0, "62.29": 4, "63.8": 4, "67.6": 5, "70.9": 6,
    "71.12": 0,
    "76.16": 3, "78.24": 6, "82.12": 4, "82.29": 4, "87.6": 0, "89.12": 6,
    "90.25": 0, "105.16": 0,
}


def clean(z: str) -> str:
    z = re.sub(r"(本区间|全区间)首次", "首次", z)
    z = re.sub(r"(本区间|全区间)", "", z)
    return WS.sub(" ", z).strip()


def main() -> int:
    raw = json.loads((DIR / "milestones_raw.json").read_text(encoding="utf-8"))
    index = {(m["session"], m["ref"]): m for m in raw}

    out = []
    missing = []
    for era, _, _, _ in ERAS:
        for ref in PICKS[era]:
            sess = int(ref.split(".")[0])
            key = (sess, ref)
            if key not in index:
                missing.append(key)
                continue
            m = dict(index[key])
            m["zh"] = clean(m["zh"])
            if ref in SPECIAL:
                m["zh"] = SPECIAL[ref](m["zh"])
            m["era"] = era
            m["level"] = LEVELS[ref]
            m["quotes"] = [{"en": WS.sub(" ", q["en"]).strip(), "zh": q["zh"]} for q in m["quotes"]]
            out.append(m)

    if missing:
        print("MISSING:", missing)
        return 1

    (DIR / "milestones_final.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    per_era = {}
    for m in out:
        per_era[m["era"]] = per_era.get(m["era"], 0) + 1
    print(f"final milestones: {len(out)}")
    print("per era:", per_era)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())