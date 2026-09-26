#!/usr/bin/env python3
"""校验 output/Ra_Session_XXX_summary.md 的层级列表格式。

校验项：
- 每个非空行都必须是列表项（"- " 开头，可缩进）
- 首条为顶层「- **全篇总括**：」
- 缩进按每层 2 空格规整递进（不跳层、不用 Tab）
- 统计：总条目数、最大层级、一级主题数

✗ 类错误 -> exit 1；⚠ 类警告仅提示。

用法：
    python3 verify_summary.py 5            # 单集
    python3 verify_summary.py 5-12         # 区间
    python3 verify_summary.py 5 12 88      # 列举
"""

from __future__ import annotations
import re
import sys
from pathlib import Path

OUTPUT_DIR = Path('output')
ITEM_RE = re.compile(r'^( *)- ')
TOP_SUMMARY_RE = re.compile(r'^- \*\*全篇总括\*\*')

MIN_ITEMS = 8
MAX_DEPTH = 5


def verify(n: int) -> bool:
    xxx = f'{n:03d}'
    path = OUTPUT_DIR / f'Ra_Session_{xxx}_summary.md'
    if not path.exists():
        print(f'  [{xxx}] ✗ {path} 不存在')
        return False

    ok = True
    first_seen = False
    prev_depth = -1
    items = 0
    topics = 0  # 一级主题数：总括（第0层）之下的直接子条目（第1层）
    max_depth = 0
    top_level_extra = 0  # 首条（总括）之后仍写在顶层的条目数（应为 0）

    for lineno, line in enumerate(path.read_text(encoding='utf-8').split('\n'), 1):
        if not line.strip():
            continue
        m = ITEM_RE.match(line)
        if not m:
            print(f'  [{xxx}] ✗ 第{lineno}行不是列表项: {line.strip()[:40]}')
            ok = False
            continue

        indent = len(m.group(1))
        if '\t' in line[:indent + 2]:
            print(f'  [{xxx}] ✗ 第{lineno}行使用了 Tab 缩进')
            ok = False
        if indent % 2 != 0:
            print(f'  [{xxx}] ✗ 第{lineno}行缩进为奇数空格({indent})，层级错乱')
            ok = False
            continue
        depth = indent // 2

        if not first_seen:
            first_seen = True
            if depth != 0:
                print(f'  [{xxx}] ✗ 首条列表项不在顶层（缩进 {indent} 空格）')
                ok = False
            elif not TOP_SUMMARY_RE.match(line):
                print(f'  [{xxx}] ✗ 首条不是「- **全篇总括**：」: {line.strip()[:40]}')
                ok = False
        elif depth > prev_depth + 1:
            print(f'  [{xxx}] ✗ 第{lineno}行跳层：从第{prev_depth}层直接到第{depth}层')
            ok = False
        elif depth == 0:
            top_level_extra += 1

        prev_depth = depth
        items += 1
        max_depth = max(max_depth, depth)
        if depth == 1:
            topics += 1

    if not first_seen:
        print(f'  [{xxx}] ✗ 文件为空或没有任何列表项')
        return False

    warn = []
    if items < MIN_ITEMS:
        warn.append(f'条目过少（{items} < {MIN_ITEMS}），覆盖可能不足')
    if topics < 3:
        warn.append(f'一级主题过少（{topics}），可能未按问答脉络展开')
    if max_depth + 1 > MAX_DEPTH:
        warn.append(f'层级过深（{max_depth + 1} 层 > {MAX_DEPTH} 层）')
    if top_level_extra:
        warn.append(f'有 {top_level_extra} 条列表项写在顶层——议题条应缩进为「全篇总括」的子层级'
                    f'（导图脚本虽会容错合并，但不符合规范格式）')

    detail = f'条目={items}, 一级主题={topics}, 最大层级={max_depth + 1}'
    if ok:
        status = '✓' if not warn else '⚠'
        print(f'  [{xxx}] {status} {detail}')
        for w in warn:
            print(f'        ⚠ {w}')
    else:
        print(f'  [{xxx}] ✗ {detail}')
    return ok


def parse_args(argv):
    ns = []
    for a in argv:
        m = re.fullmatch(r'(\d+)-(\d+)', a)
        if m:
            ns.extend(range(int(m.group(1)), int(m.group(2)) + 1))
        else:
            ns.append(int(a))
    return ns


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ns = parse_args(sys.argv[1:])
    print('=' * 60)
    print(f'verify_summary (Ra): 共 {len(ns)} 集')
    print('=' * 60)
    all_ok = True
    for n in ns:
        if not verify(n):
            all_ok = False
    print('')
    print('全部通过 ✓' if all_ok else '存在 ✗ 错误，需修正后重跑')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main())
