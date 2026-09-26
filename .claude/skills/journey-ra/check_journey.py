#!/usr/bin/env python3
"""校验 study/journey_<topic>.html 的结构完整性与引文忠实性。

用法:
    python3 .claude/skills/journey-ra/check_journey.py densities
    python3 .claude/skills/journey-ra/check_journey.py harvest polarity veil

exit 0 = 全部通过; exit 1 = 有失败项（逐条打印）。

校验项:
- 无 {{ / @@CUSTOM_JS@@ 残留、无 quiz 字样、无声音按钮（soundBtn）
- 场景+站点 ≥8、站点 ≥4、细节卡 ≥12
- 开场为 id="s0" 的 scene；终章存在 id="sLast" 的 scene；id="again" 已绑定
- 每个场景/站点有 data-c 十六进制色
- 细节卡含 f-en 引文与 f-ref 出处（SESSION 编号）
- 引文忠实性：按各区块标注的 SESSION 出处，逐字核验英文引文为源文件的有序子串
- 篇幅 ≥20 KB
"""
import html
import os
import re
import sys

MIN_SECTIONS = 8
MIN_STATIONS = 4
MIN_FRAGS = 12
MIN_KB = 20

CJK_RE = re.compile(r'[㐀-鿿　-〿＀-￯]')
_DASHES = {'“': '"', '”': '"', '‘': "'", '’': "'",
           '–': '-', '—': '-', '−': '-', ' ': ' '}


def norm(s: str) -> str:
    s = html.unescape(re.sub(r'<[^>]+>', '', s))
    for a, b in _DASHES.items():
        s = s.replace(a, b)
    s = re.sub(r'\.\s*\.\s*\.', '...', s)
    s = s.replace('…', '...')
    return re.sub(r'\s+', ' ', s).strip()


_src_cache = {}


def session_text(n: str) -> str:
    if n not in _src_cache:
        p = f'split/Ra_Session_{n}.md'
        if not os.path.exists(p):
            _src_cache[n] = None
        else:
            lines = [l.strip() for l in open(p, encoding='utf-8')
                     if l.strip() and not CJK_RE.search(l)]
            _src_cache[n] = norm(' '.join(lines))
    return _src_cache[n]


def check_quotes(section: str, tag: str, errs: list) -> int:
    refs = set(re.findall(r'SESSION (\d{3})', section))
    quotes = re.findall(r'class="(?:f-)?en">(.*?)</p>', section, re.S)
    n_checked = 0
    for q in quotes:
        if not refs:
            errs.append(f'{tag}: 引文区块缺少 SESSION 出处标注: {norm(q)[:50]!r}')
            continue
        frags = [f.strip() for f in norm(q).strip('"').split('...') if f.strip()]
        for f in frags:
            if len(f) < 6:
                continue
            n_checked += 1
            if not any(session_text(r) and f in session_text(r) for r in refs):
                errs.append(f'{tag}: 引文非原文逐字摘录（出处 {sorted(refs)}）: {f[:70]!r}')
    return n_checked


def check(topic: str) -> list:
    topic = topic.removeprefix('journey_').removesuffix('.html')
    path = f'study/journey_{topic}.html'
    errs = []
    if not os.path.exists(path):
        print(f'[{topic}] ✗ 文件不存在: {path}')
        return [f'文件不存在: {path}']

    with open(path, encoding='utf-8') as f:
        s = f.read()

    for needle, desc in [('{{', '未替换的占位符'), ('@@CUSTOM_JS@@', '定制 JS 占位符（应已被替换）'),
                         ('quiz', '测验区块'), ('soundBtn', '声音按钮（本 skill 不做音乐）')]:
        if needle in s:
            errs.append(f'不应出现: {desc} ({needle})')

    n_scene = len(re.findall(r'<section class="scene"', s))
    n_station = len(re.findall(r'<section class="station"', s))
    n_frag = s.count('class="frag"')
    if n_scene + n_station < MIN_SECTIONS:
        errs.append(f'场景+站点仅 {n_scene + n_station} 个，要求 ≥{MIN_SECTIONS}')
    if n_station < MIN_STATIONS:
        errs.append(f'站点仅 {n_station} 个，要求 ≥{MIN_STATIONS}')
    if n_frag < MIN_FRAGS:
        errs.append(f'细节卡仅 {n_frag} 张，要求 ≥{MIN_FRAGS}')

    if 'id="s0"' not in s:
        errs.append('缺少开场 id="s0"')
    if 'id="sLast"' not in s:
        errs.append('缺少终章 id="sLast"')
    if 'id="again"' not in s or "getElementById('again')" not in s:
        errs.append('id="again" 未绑定回卷事件')

    for m in re.finditer(r'<section class="(?:scene|station)"[^>]*>', s):
        if 'data-c="#' not in m.group(0):
            errs.append(f'场景/站点缺少 data-c 颜色: {m.group(0)[:60]}')

    n_quotes = 0
    for m in re.finditer(r'<section class="(?:scene|station)".*?</section>', s, re.S):
        tag = re.search(r'id="(s\w+)"', m.group(0))
        n_quotes += check_quotes(m.group(0), tag.group(1) if tag else '?', errs)

    kb = len(s.encode('utf-8')) / 1024
    if kb < MIN_KB:
        errs.append(f'篇幅过短（{kb:.0f} KB < {MIN_KB} KB）')

    if not errs:
        print(f'[{topic}] ✓ {path} ({kb:.0f} KB, 场景 {n_scene}, 站点 {n_station}, '
              f'细节卡 {n_frag}, 引文 {n_quotes} 处逐字核验通过)')
    else:
        print(f'[{topic}] ✗ {path}')
        for e in errs:
            print(f'   - {e}')
    return errs


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    failed = False
    for t in sys.argv[1:]:
        if check(t):
            failed = True
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
