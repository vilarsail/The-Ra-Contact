#!/usr/bin/env python3
"""校验 study/Ra_Session_XXX_study.html 的结构完整性与内容规范。

用法:
    python3 .claude/skills/study-ra/check_study.py 5            # 单集
    python3 .claude/skills/study-ra/check_study.py 5-12         # 区间
    python3 .claude/skills/study-ra/check_study.py 5 12 88      # 列举

exit 0 = 全部通过; exit 1 = 有失败项（逐条打印）。

校验项:
- 组件齐全（hero / path-box / toc / script / initStepper / initSorter / renderPath）
- 无 {{ 占位符残留、@@CUSTOM_JS@@ 已替换、无 quiz 区块
- 导航锚点与 data-target 均有对应 id="sK"
- 章节数 4-8；案例块 ≥ max(8, 2×章节数)；.quote 数 ≥ 章节数
- 英文引文忠实性：每条 <p class="en"> 逐字核验为 split/Ra_Session_XXX.md 英文文本的有序子串
- 交互调用 ≥3（且必须有 initStepper 调用）
- localStorage key 为 ra{XXX}-study-progress；篇幅 ≥18 KB
"""
import html
import os
import re
import sys

MIN_CHAPTERS, MAX_CHAPTERS = 4, 8
MIN_CASES_ABS = 8
MIN_KB = 18
MIN_QUOTE_CHARS = 12

REQUIRED = [
    ('class="hero"', "hero 头部"),
    ('path-box', "学习路径区块"),
    ('id="toc"', "导航"),
    ('<script>', "脚本"),
    ('function initStepper(', "流程推演/问答推进组件定义"),
    ('function initSorter(', "归类练习组件定义"),
    ('renderPath();', "进度初始化调用"),
]
FORBIDDEN = [
    ('{{', "未替换的占位符"),
    ('@@CUSTOM_JS@@', "定制 JS 占位符（应已被替换）"),
    ('quiz', "测验区块/链接（本 skill 不产出）"),
]

CJK_RE = re.compile(r'[㐀-鿿　-〿＀-￯]')
EN_QUOTE_RE = re.compile(r'<p class="en">(.*?)</p>', re.S)

_DASHES = {'“': '"', '”': '"', '‘': "'", '’': "'",
           '–': '-', '—': '-', '−': '-', ' ': ' '}


def norm(s: str) -> str:
    """归一化文本，供引文忠实性比对：剥标签/反转义/统一引号破折号/折叠空白。"""
    s = html.unescape(s)
    s = re.sub(r'<[^>]+>', '', s)
    for a, b in _DASHES.items():
        s = s.replace(a, b)
    s = re.sub(r'\.\s*\.\s*\.', '...', s)   # ". . ." -> "..."
    s = s.replace('…', '...')          # "…" -> "..."
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def english_text(path: str) -> str:
    """抽取 split/Ra_Session_XXX.md 的英文-only 文本（剔除含 CJK 的译文行）。"""
    lines = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip() and not CJK_RE.search(line):
                lines.append(line.strip())
    return norm(' '.join(lines))


def verify_quotes(s: str, src: str, tag: str) -> list:
    """核验每条英文引文为源文本的有序子串（按 ... 切分片段）。"""
    errs = []
    for m in EN_QUOTE_RE.finditer(s):
        q = norm(m.group(1))
        if len(q) < MIN_QUOTE_CHARS:
            errs.append(f"引文过短/为空（{len(q)} 字符）: {q[:40]!r}")
            continue
        pos, bad = 0, None
        for frag in [f.strip() for f in q.split('...') if f.strip()]:
            if len(frag) < 6:
                continue
            hit = src.find(frag, pos)
            if hit < 0:
                bad = frag
                break
            pos = hit + len(frag)
        if bad:
            errs.append(f"{tag} 引文非原文逐字摘录（找不到片段）: {bad[:70]!r}")
    return errs


def check(n: int) -> list:
    xxx = f'{n:03d}'
    path = f"study/Ra_Session_{xxx}_study.html"
    src_path = f"split/Ra_Session_{xxx}.md"
    errs = []
    if not os.path.exists(path):
        print(f"[{xxx}] ✗ 文件不存在: {path}")
        return [f"文件不存在: {path}"]

    with open(path, encoding='utf-8') as f:
        s = f.read()

    for needle, desc in REQUIRED:
        if needle not in s:
            errs.append(f"缺少组件: {desc} ({needle})")

    for needle, desc in FORBIDDEN:
        if needle in s:
            errs.append(f"不应出现: {desc} ({needle})")

    # 导航锚点 / 路径步骤 data-target 对应章节 id
    for m in re.finditer(r'href="#(s\d+)"', s):
        if f'id="{m.group(1)}"' not in s:
            errs.append(f"导航锚点 #{m.group(1)} 无对应章节")
    for m in re.finditer(r'data-target="#(s\d+)"', s):
        if f'id="{m.group(1)}"' not in s:
            errs.append(f"路径步骤 data-target #{m.group(1)} 无对应章节")

    # 章节数 / 案例数 / 引文数
    chapters = len(re.findall(r'<section class="chapter"', s))
    cases = s.count('class="case"')
    quotes = s.count('class="quote"')
    min_cases = max(MIN_CASES_ABS, 2 * chapters)
    if not (MIN_CHAPTERS <= chapters <= MAX_CHAPTERS):
        errs.append(f"章节数 {chapters} 不在 {MIN_CHAPTERS}-{MAX_CHAPTERS} 范围内")
    if cases < min_cases:
        errs.append(f"案例块仅 {cases} 个，要求 ≥{min_cases}（max({MIN_CASES_ABS}, 2×{chapters})）")
    if quotes < chapters:
        errs.append(f"引文块仅 {quotes} 个，要求 ≥章节数 {chapters}（每章至少 1 条）")

    # 交互调用（排除函数定义本身）
    n_stepper = len(re.findall(r'(?<!function )initStepper\(', s))
    n_sorter = len(re.findall(r'(?<!function )initSorter\(', s))
    n_fncard = len(re.findall(r"classList\.toggle\(['\"]open['\"]\)", s))
    interactive = n_stepper + n_sorter + n_fncard
    if interactive < 3:
        errs.append(f"交互调用仅 {interactive} 处，要求 ≥3（initStepper/initSorter/fn-card 展开）")
    if n_stepper < 1:
        errs.append("缺少问答推进器调用 initStepper(...)")

    # localStorage key
    if f"ra{xxx}-study-progress" not in s:
        errs.append(f"localStorage key 应为 ra{xxx}-study-progress")

    # 英文引文忠实性
    n_quotes = 0
    if not os.path.exists(src_path):
        errs.append(f"源文件不存在，无法核验引文: {src_path}")
    else:
        src = english_text(src_path)
        n_quotes = len(EN_QUOTE_RE.findall(s))
        for e in verify_quotes(s, src, "英文"):
            errs.append(e)

    kb = len(s.encode('utf-8')) / 1024
    if kb < MIN_KB:
        errs.append(f"篇幅过短（{kb:.0f} KB < {MIN_KB} KB）")

    if not errs:
        print(f"[{xxx}] ✓ {path} ({kb:.0f} KB, 章节 {chapters}, 案例 {cases}, "
              f"引文 {n_quotes} 全部逐字核验通过, 交互调用 {interactive})")
    else:
        print(f"[{xxx}] ✗ {path}")
        for e in errs:
            print(f"   - {e}")
    return errs


def parse_args(argv: list) -> list:
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
        return 1
    failed = False
    for n in parse_args(sys.argv[1:]):
        if check(n):
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
