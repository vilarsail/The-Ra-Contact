#!/usr/bin/env python3
"""从 split/Ra_Session_XXX.md 提取「英文-only」紧凑文本，供 summarize-ra 的 LLM 通读。

原文是英中逐段对照：英文段落后紧跟同义的中文译段（含 `[两分钟停顿。]` 这类中文方括号注）。
中文行可通过「含 CJK 字符」可靠识别并剔除——这样总结只依赖英文原文，与正文译文解耦
（译文将来怎么修正都不影响总结输入）。

保留：`# § Ra Session_XXX` 标题行、英文日期行、`## (N.Y)` 问答块标题、英文段落、
      英文方括号注（如 `[Two-minute pause.]`）。
剔除：含 CJK 字符的所有行（中文译段、中文方括号注、中文日期）。

用法：
    python3 .claude/skills/summarize-ra/prepare_reading.py 5
    python3 .claude/skills/summarize-ra/prepare_reading.py 5-12
    python3 .claude/skills/summarize-ra/prepare_reading.py 5 12 88

输出：output/reading_Ra_Session_XXX_en.txt
"""
import re
import sys
from pathlib import Path

SPLIT_DIR = Path('split')
OUT_DIR = Path('output')
CJK_RE = re.compile(r'[㐀-鿿　-〿＀-￯]')


def extract(n: int) -> bool:
    xxx = f'{n:03d}'
    src = SPLIT_DIR / f'Ra_Session_{xxx}.md'
    if not src.exists():
        print(f'  [{xxx}] ✗ 源文件不存在: {src}')
        return False

    kept, dropped = [], 0
    for line in src.read_text(encoding='utf-8').split('\n'):
        s = line.strip()
        if not s:
            continue
        if CJK_RE.search(s):
            dropped += 1
            continue
        kept.append(s)

    OUT_DIR.mkdir(exist_ok=True)
    dst = OUT_DIR / f'reading_Ra_Session_{xxx}_en.txt'
    dst.write_text('\n'.join(kept) + '\n', encoding='utf-8')
    blocks = sum(1 for s in kept if s.startswith('## ('))
    print(f'  [{xxx}] ✓ {dst.name}：保留 {len(kept)} 行（问答块 {blocks}），剔除中文行 {dropped}')
    return True


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
    return 0 if all(extract(n) for n in parse_args(sys.argv[1:])) else 1


if __name__ == '__main__':
    sys.exit(main())
