#!/usr/bin/env python3
"""Build study/Ra_Density_Timeline.html — 单文件、离线、滚动驱动的密度概念演化时间机器。

Usage: python3 build_timeline.py
Input: milestones_final.json
Output: study/Ra_Density_Timeline.html
"""
import html
import json
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parent.parent.parent
OUT = ROOT / "study" / "Ra_Density_Timeline.html"

ERAS = [
    (1, "Ⅰ", "命名与阶梯", "1–15 集",
     "密度先有了名字（爱、光），再被编上序号，成为一条连续递进的意识阶梯。"),
    (2, "Ⅱ", "结构定形", "16–30 集",
     "密度被定义成数学式的音阶结构：七个密度、七个子密度、无限细分，而且可以计数。"),
    (3, "Ⅲ", "色彩·身体·极化", "31–50 集",
     "密度长出了颜色与身体：真实颜色、七重载具、能量中心，以及只属于第三密度的极化。"),
    (4, "Ⅳ", "循环与八度", "51–71 集",
     "密度被放进更大的循环：八度既是终点也是起点，而行星、高我、个体各自都有自己的密度刻度。"),
    (5, "Ⅴ", "边界与载体", "72–106 集",
     "收束：第三密度是一次选择，密度之间可以渗透，载具不加速成长、只允许成长。"),
]

LADDER = [
    (8, "第八密度", "八度／智能无限的入口"),
    (7, "第七密度", "入口密度，极性功能用尽"),
    (6, "第六密度", "合一；统一智慧与悲悯"),
    (5, "第五密度", "光／智慧"),
    (4, "第四密度", "爱／理解"),
    (3, "第三密度", "自我觉察；选择"),
    (2, "第二密度", "生长；趋向光"),
    (1, "第一密度", "觉察；矿物与水"),
]

SUBTEMES = ["密度定义", "各密度生命形态", "收割与毕业", "密度与极化",
            "光体与身体", "宇宙生成", "实体与密度"]


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def card_html(m: dict) -> str:
    lv = m["level"]
    lv_tag = "全阶 · 阶梯本身" if lv == 0 else f"聚焦 第{['','一','二','三','四','五','六','七','八'][lv]}密度"
    quotes = "\n".join(
        f'''        <blockquote class="q">
          <p class="en">{esc(q["en"])}</p>
          <p class="zh">{esc(q["zh"])}</p>
        </blockquote>''' for q in m["quotes"]
    )
    w3 = " w3" if m["weight"] == 3 else ""
    return f'''      <article class="ms{w3}" id="m-{m["session"]}-{m["ref"].replace(".", "-")}"
        data-session="{m["session"]}" data-era="{m["era"]}" data-level="{lv}"
        data-sub="{esc(m["subtheme"])}">
        <header class="ms-head">
          <span class="ms-badge" title="原文出处">{esc(m["ref"])}</span>
          <span class="ms-session">第 {m["session"]} 集</span>
          <span class="ms-dot" aria-hidden="true"></span>
        </header>
        <h3 class="ms-title">{esc(m["title"])}</h3>
        <span class="ms-read" aria-hidden="true">已读</span>
        <p class="ms-zh">{esc(m["zh"])}</p>
{quotes}
        <footer class="ms-meta">
          <span class="tag tag-sub">{esc(m["subtheme"])}</span>
          <span class="tag tag-lv">{lv_tag}</span>
        </footer>
      </article>'''


def main() -> int:
    data = json.loads((DIR / "milestones_final.json").read_text(encoding="utf-8"))

    era_sections = []
    for era, num, name, span, blurb in ERAS:
        cards = "\n".join(card_html(m) for m in data if m["era"] == era)
        era_sections.append(f'''    <section class="era" id="era{era}" data-era="{era}">
      <header class="era-head">
        <span class="era-num">{num}</span>
        <div>
          <h2>{name}</h2>
          <p class="era-span">{span}</p>
        </div>
      </header>
      <p class="era-blurb">{blurb}</p>
      <div class="era-cards">
{cards}
      </div>
    </section>''')

    ladder_rows = []
    for lv, lname, lnote in LADDER:
        n = sum(1 for m in data if m["level"] == lv)
        ladder_rows.append(f'''        <li class="rung" data-level="{lv}">
          <span class="rung-bar" aria-hidden="true"></span>
          <span class="rung-txt"><b>{lname}</b><small>{lnote}</small></span>
          <span class="rung-n">{n}</span>
        </li>''')

    n_all = sum(1 for m in data if m["level"] == 0)
    sessions_with = sorted({m["session"] for m in data})

    ticks = "".join(
        f'<i class="{"has" if s in sessions_with else ""}" data-session="{s}" '
        f'title="第 {s} 集"></i>' for s in range(1, 107)
    )

    era_chips = "".join(
        f'<button class="chip chip-era" data-era="{e}">{num} {name}<small>{span}</small></button>'
        for e, num, name, span, _ in ERAS
    )
    sub_chips = "".join(
        f'<button class="chip chip-sub" data-sub="{esc(s)}">{esc(s)}</button>' for s in SUBTEMES
    )

    doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>密度 · 概念演化时间机器 | 一的法则</title>
<style>
:root{{
  --ink:#2b2620;
  --ink-soft:#5c5348;
  --paper:#f7f3ec;
  --card:#fffdf8;
  --accent:#9a3b2e;
  --accent-soft:#f3e2dd;
  --blue:#2e4a62;
  --blue-soft:#e2eaf1;
  --gold:#8a6d1f;
  --gold-soft:#f4ecd4;
  --green:#3d6b4f;
  --green-soft:#e0eee5;
  --line:#e4dccc;
  --radius:14px;
}}
*{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{
  font-family:"Songti SC","Noto Serif SC","Source Han Serif SC",serif;
  background:var(--paper);color:var(--ink);line-height:1.85;
  -webkit-font-smoothing:antialiased;
}}
a{{color:var(--blue)}}

/* ===== 滚动进度 ===== */
#scrollbar{{position:fixed;top:0;left:0;height:3px;width:0;z-index:200;
  background:linear-gradient(90deg,var(--accent),var(--gold));transition:width .1s linear}}

/* ===== 顶部 ===== */
header.hero{{
  background:linear-gradient(135deg,#16203c 0%,#2b3560 55%,#4a3a5e 100%);
  color:#f2eee6;text-align:center;padding:72px 20px 60px;
}}
header.hero .kicker{{letter-spacing:.35em;font-size:.8rem;opacity:.72;margin-bottom:16px}}
header.hero h1{{font-size:2.15rem;font-weight:600;letter-spacing:.06em;margin-bottom:8px}}
header.hero h1 em{{font-style:normal;color:#e8c987}}
header.hero .sub{{max-width:640px;margin:18px auto 0;opacity:.86;font-size:1.02rem}}
header.hero .tagline{{
  display:inline-block;margin-top:26px;padding:9px 24px;border:1px solid rgba(242,238,230,.38);
  border-radius:999px;font-size:.9rem;letter-spacing:.1em;
}}
header.hero .stats{{margin-top:22px;font-size:.84rem;opacity:.6;letter-spacing:.08em}}

/* ===== 停靠栏 ===== */
.dock{{
  position:sticky;top:0;z-index:90;background:rgba(247,243,236,.97);
  border-bottom:1px solid var(--line);backdrop-filter:blur(8px);
}}
.dock-row{{max-width:1240px;margin:0 auto;padding:8px 16px;
  display:flex;gap:10px;align-items:center;overflow-x:auto;white-space:nowrap}}
.dock-row + .dock-row{{border-top:1px dashed var(--line);padding-top:7px;padding-bottom:9px}}
.dock-label{{font-size:.74rem;color:var(--ink-soft);opacity:.8;letter-spacing:.14em;flex-shrink:0}}
.chip{{
  font-family:inherit;font-size:.83rem;color:var(--ink-soft);cursor:pointer;
  background:transparent;border:1px solid var(--line);border-radius:999px;
  padding:4px 13px;flex-shrink:0;transition:all .18s;
}}
.chip:hover{{border-color:var(--accent);color:var(--accent)}}
.chip.on{{background:var(--accent);border-color:var(--accent);color:#fff}}
.chip-era small{{display:block;font-size:.68rem;opacity:.7;letter-spacing:.06em}}
.chip-era.on small{{opacity:.85}}

/* 集号轨 */
.track-wrap{{flex:1;display:flex;align-items:center;gap:10px;min-width:320px}}
.track{{flex:1;position:relative;display:flex;gap:1px;height:16px;align-items:flex-end;min-width:260px}}
.track i{{flex:1;height:5px;background:var(--line);border-radius:1px;transition:height .2s,background .2s}}
.track i.has{{background:#c9b48c;height:10px;cursor:pointer}}
.track i.has:hover{{background:var(--accent);height:14px}}
.track i.past{{background:var(--accent-soft);height:10px}}
.track i.cur{{background:var(--accent);height:16px}}
#ptr{{position:absolute;top:-4px;width:0;height:0;
  border-left:5px solid transparent;border-right:5px solid transparent;
  border-top:7px solid var(--accent);transform:translateX(-5px);transition:left .25s ease}}
.readout{{font-size:.78rem;color:var(--ink-soft);flex-shrink:0;min-width:132px;text-align:right}}
.readout b{{color:var(--accent)}}
#reset{{font-family:inherit;font-size:.74rem;color:var(--ink-soft);background:none;border:none;
  cursor:pointer;text-decoration:underline;opacity:.7;flex-shrink:0}}
#reset:hover{{color:var(--accent);opacity:1}}

/* ===== 主体 ===== */
.stage{{max-width:1240px;margin:0 auto;padding:0 16px 120px;
  display:grid;grid-template-columns:216px minmax(0,1fr);gap:34px;align-items:start}}

/* 左侧阶梯 */
aside.rail{{position:sticky;top:112px;padding-top:34px}}
.rail-card{{background:var(--card);border:1px solid var(--line);border-radius:var(--radius);
  padding:16px 14px 14px}}
.rail-title{{font-size:.76rem;letter-spacing:.2em;color:var(--ink-soft);
  text-align:center;margin-bottom:12px;opacity:.85}}
ol.ladder{{list-style:none;display:flex;flex-direction:column;gap:3px}}
.rung{{display:flex;align-items:center;gap:8px;padding:5px 6px;border-radius:9px;
  transition:background .25s,transform .25s}}
.rung-bar{{width:7px;border-radius:3px;background:var(--line);align-self:stretch;
  flex-shrink:0;transition:background .3s,box-shadow .3s}}
.rung-txt{{flex:1;min-width:0;line-height:1.3}}
.rung-txt b{{display:block;font-size:.82rem;font-weight:600;color:var(--ink-soft);transition:color .25s}}
.rung-txt small{{display:block;font-size:.68rem;color:var(--ink-soft);opacity:.62;
  overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.rung-n{{font-size:.68rem;color:var(--ink-soft);opacity:.5;flex-shrink:0}}
.rung.on{{background:var(--accent-soft);transform:translateX(3px)}}
.rung.on .rung-bar{{background:var(--accent);box-shadow:0 0 0 3px rgba(154,59,46,.14)}}
.rung.on .rung-txt b{{color:var(--accent)}}
.rung.on .rung-n{{color:var(--accent);opacity:.9}}
.rung.all-on{{background:var(--blue-soft)}}
.rung.all-on .rung-bar{{background:var(--blue)}}
.rail-note{{margin-top:12px;font-size:.7rem;color:var(--ink-soft);opacity:.72;
  line-height:1.6;border-top:1px dashed var(--line);padding-top:10px}}
.rail-all{{margin:10px 0 0;font-size:.72rem;text-align:center;color:var(--ink-soft);opacity:.75}}

/* 阶段 */
section.era{{padding-top:52px}}
.era-head{{display:flex;gap:14px;align-items:center;border-bottom:2px solid var(--line);
  padding-bottom:10px}}
.era-num{{font-size:2.2rem;color:var(--accent);opacity:.3;line-height:1;font-weight:700}}
.era-head h2{{font-size:1.4rem;letter-spacing:.04em}}
.era-span{{font-size:.78rem;color:var(--ink-soft);opacity:.75;letter-spacing:.1em}}
.era-blurb{{margin:14px 0 4px;color:var(--ink-soft);font-size:.95rem;max-width:660px}}
.era-cards{{position:relative;margin-top:26px;padding-left:26px}}
.era-cards::before{{content:"";position:absolute;left:7px;top:6px;bottom:6px;width:2px;
  background:linear-gradient(180deg,var(--line),rgba(228,220,204,.25))}}

/* 里程碑卡片 */
article.ms{{
  position:relative;background:var(--card);border:1px solid var(--line);
  border-radius:var(--radius);padding:20px 22px;margin-bottom:20px;
  box-shadow:0 1px 0 rgba(60,50,30,.02);
  transition:box-shadow .3s,border-color .3s,transform .3s;
}}
article.ms::before{{
  content:"";position:absolute;left:-26px;top:30px;width:14px;height:14px;border-radius:50%;
  background:var(--paper);border:2px solid var(--line);transition:all .3s;
}}
article.ms.w3::before{{border-color:#c9b48c}}
article.ms.active{{border-color:var(--accent);box-shadow:0 10px 26px rgba(60,50,30,.09)}}
article.ms.active::before{{background:var(--accent);border-color:var(--accent);
  box-shadow:0 0 0 5px rgba(154,59,46,.14)}}
article.ms.w3{{border-left:3px solid #c9b48c}}
article.ms.w3.active{{border-left-color:var(--accent)}}
.ms-head{{display:flex;align-items:center;gap:10px;margin-bottom:6px}}
.ms-badge{{font-size:.76rem;letter-spacing:.06em;color:var(--accent);background:var(--accent-soft);
  padding:1px 9px;border-radius:999px}}
.ms-session{{font-size:.76rem;color:var(--ink-soft);opacity:.7}}
.ms-dot{{flex:1;height:1px;background:repeating-linear-gradient(90deg,var(--line) 0 4px,transparent 4px 8px)}}
.ms-title{{font-size:1.14rem;color:var(--ink);margin-bottom:8px}}
.ms-zh{{font-size:.95rem;color:var(--ink-soft);margin-bottom:4px}}

blockquote.q{{margin:12px 0 0;background:var(--blue-soft);border-left:3px solid var(--blue);
  padding:12px 16px;border-radius:0 10px 10px 0}}
blockquote.q + blockquote.q{{margin-top:8px;background:#eaf0f5}}
blockquote.q .en{{font-size:.9rem;color:var(--blue);font-style:italic;line-height:1.7}}
blockquote.q .zh{{font-size:.87rem;color:var(--ink-soft);margin-top:8px;
  border-top:1px dashed rgba(46,74,98,.26);padding-top:7px}}
blockquote.q .zh::before{{content:"译 ";font-weight:700;opacity:.65;font-size:.8rem}}
.ms-meta{{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px;
  border-top:1px dashed var(--line);padding-top:10px}}
.tag{{font-size:.74rem;padding:1px 10px;border-radius:999px;border:1px solid var(--line);
  color:var(--ink-soft)}}
.tag-sub{{background:var(--green-soft);border-color:transparent;color:var(--green)}}
.tag-lv{{background:var(--gold-soft);border-color:transparent;color:var(--gold)}}

/* 已读标记 */
.ms-read{{position:absolute;right:16px;top:16px;font-size:.7rem;color:var(--green);
  opacity:0;transition:opacity .4s}}
article.ms.read .ms-read{{opacity:.85}}

/* 揭示动画（仅在 JS 健康启动时启用；任何异常都会退回全显） */
html.rv article.ms{{opacity:0;transform:translateY(16px)}}
html.rv article.ms.in{{opacity:1;transform:none;
  transition:opacity .6s ease,transform .6s ease,border-color .3s,box-shadow .3s}}
@media (prefers-reduced-motion: reduce){{
  html{{scroll-behavior:auto}}
  html.rv article.ms{{opacity:1;transform:none}}
  .track i,#ptr,#scrollbar{{transition:none}}
}}

/* 筛选 */
article.ms.hide{{display:none}}
section.era.hide{{display:none}}

/* 收尾 */
#end{{max-width:1240px;margin:0 auto;padding:40px 16px 60px;border-top:1px solid var(--line)}}
#end h2{{font-size:1.1rem;color:var(--blue);margin-bottom:8px}}
#end p{{font-size:.9rem;color:var(--ink-soft);max-width:720px}}
#end .note{{margin-top:14px;font-size:.8rem;opacity:.7}}

/* 窄屏：收起阶梯 */
@media (max-width:1080px){{
  .stage{{grid-template-columns:1fr}}
  aside.rail{{display:none}}
  .era-cards{{padding-left:22px}}
}}
@media (max-width:620px){{
  header.hero{{padding:52px 18px 44px}}
  header.hero h1{{font-size:1.6rem}}
  .dock-row{{padding:7px 12px}}
  .readout{{min-width:104px;font-size:.72rem}}
  article.ms{{padding:17px 17px}}
  .era-cards{{padding-left:16px}}
  article.ms::before{{left:-22px;width:11px;height:11px}}
}}
</style>
</head>
<body>

<div id="scrollbar" aria-hidden="true"></div>

<header class="hero">
  <p class="kicker">THE RA CONTACT</p>
  <h1>密度 · <em>一个概念如何生长</em></h1>
  <p class="sub">在 106 集问答里，「密度」最初只是两个词的称呼——「爱[密度]」「光[密度]」。
  四百页之后，它长成了七重八度、层层相套、可以渗透的宇宙结构。向下滚动，看它一层层长出来。</p>
  <span class="tagline">40 个里程碑 · 5 个阶段 · 跨 106 集</span>
  <p class="stats">滚动阅读 · 左侧阶梯随当前节点亮起 · 下方可筛选子题、点击集号跳转</p>
</header>

<div class="dock">
  <div class="dock-row">
    <span class="dock-label">阶段</span>
    {era_chips}
  </div>
  <div class="dock-row">
    <span class="dock-label">子题</span>
    <button class="chip on" id="chip-all">全部</button>
    {sub_chips}
  </div>
  <div class="dock-row">
    <span class="dock-label">集号</span>
    <div class="track-wrap">
      <div class="track" id="track">{ticks}<span id="ptr"></span></div>
      <span class="readout" id="readout">第 <b>1</b> 集<span id="roman"> · 阶段 Ⅰ</span></span>
      <button id="reset" title="清除已读记录">重置</button>
    </div>
  </div>
</div>

<div class="stage">
  <aside class="rail" aria-hidden="true">
    <div class="rail-card">
      <p class="rail-title">密 度 阶 梯</p>
      <ol class="ladder">
{chr(10).join(ladder_rows)}
      </ol>
      <p class="rail-all">另有 {n_all} 个节点谈整条阶梯</p>
      <p class="rail-note">亮起的层级＝当前节点聚焦的那一层。右侧数字是该层在本书中被聚焦的次数。</p>
    </div>
  </aside>

  <main class="flow">
{chr(10).join(era_sections)}
  </main>
</div>

<div id="end">
  <h2>这条线读完之后</h2>
  <p>密度不是一个孤立的词。它一路把人牵进极化、收割、载具、社会记忆复合体与八度循环里——
  也就是说，读完这条线，你其实已经沿着《一的法则》的骨架走了一遍。</p>
  <p class="note">全部 40 个节点的英文引文均逐字取自 <b>split/Ra_Session_XXX.md</b> 的英文原文，
  并按原文块编号（如 16.51）标注出处；中文说明与译文为本页自拟，用于辅助理解。</p>
</div>

<script>
(function(){{
  var KEY = 'ra-density-timeline';
  var root = document.documentElement;
  var CARDS = Array.prototype.slice.call(document.querySelectorAll('article.ms'));
  var ERAS  = Array.prototype.slice.call(document.querySelectorAll('section.era'));
  var RUNGS = {{}};
  Array.prototype.forEach.call(document.querySelectorAll('.rung'), function(r){{
    RUNGS[r.getAttribute('data-level')] = r;
  }});
  var track = document.getElementById('track');
  var ptr = document.getElementById('ptr');
  var readout = document.getElementById('readout');
  var readbar = document.getElementById('scrollbar');
  var romanOut = document.getElementById('roman');
  var ROMAN = {{1:'Ⅰ',2:'Ⅱ',3:'Ⅲ',4:'Ⅳ',5:'Ⅴ'}};
  var activeCard = null;

  /* ---------- 已读记录 ---------- */
  var store = {{}};
  try {{ store = JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch(e) {{ store = {{}}; }}
  function persist(){{ try {{ localStorage.setItem(KEY, JSON.stringify(store)); }} catch(e) {{}} }}
  function markRead(card){{
    card.classList.add('read');
    if(!store[card.id]){{ store[card.id] = 1; persist(); }}
  }}
  CARDS.forEach(function(c){{ if(store[c.id]) c.classList.add('read'); }});

  function setActive(card){{
    activeCard = card;
    CARDS.forEach(function(c){{ c.classList.toggle('active', c === card); }});
    var lv = card.getAttribute('data-level');
    Object.keys(RUNGS).forEach(function(k){{
      RUNGS[k].classList.toggle('on', k === lv);
      RUNGS[k].classList.toggle('all-on', lv === '0');
    }});
    var sess = parseInt(card.getAttribute('data-session'), 10);
    readout.firstChild.nodeValue = '第 ';
    readout.querySelector('b').textContent = sess;
    romanOut.textContent = ' · 阶段 ' + (ROMAN[card.getAttribute('data-era')] || '');
    movePointer(sess);
  }}

  function movePointer(sess){{
    var w = track.clientWidth;
    ptr.style.left = ((sess - 1) / 105 * (w - 2) + 1) + 'px';
    var prev = track.querySelector('i.cur');
    if(prev) prev.classList.remove('cur');
    var t = track.querySelector('i[data-session="' + sess + '"]');
    if(t) t.classList.add('cur');
  }}

  /* ---------- 揭示 + 当前节点：同一次确定性扫描 ---------- */
  function sweep(){{
    var bandY = window.innerHeight * 0.34;
    var pick = null;
    for(var i=0;i<CARDS.length;i++){{
      var c = CARDS[i];
      if(c.classList.contains('hide')) continue;
      var r = c.getBoundingClientRect();
      if(r.bottom <= -60 || r.top >= window.innerHeight + 60) continue;
      if(!c.classList.contains('in')){{ c.classList.add('in'); markRead(c); }}
      if(r.top <= bandY) pick = c; else if(!pick) pick = c;
    }}
    if(pick && pick !== activeCard) setActive(pick);
  }}

  function onScroll(){{
    var h = document.documentElement.scrollHeight - window.innerHeight;
    var p = h > 0 ? Math.min(1, Math.max(0, window.pageYOffset / h)) : 0;
    readbar.style.width = (p * 100).toFixed(2) + '%';
    /* 扫描合并到下一帧；即使 rAF 被节流，进度条也已在上面同步更新 */
    if(onScroll.pending) return;
    onScroll.pending = true;
    window.requestAnimationFrame(function(){{
      onScroll.pending = false;
      sweep();
    }});
  }}

  try {{
    root.classList.add('rv');
    if(!CARDS.length) throw new Error('no cards');

    window.addEventListener('scroll', onScroll, {{passive:true}});
    window.addEventListener('resize', onScroll);
    window.addEventListener('load', onScroll);
    window.addEventListener('hashchange', onScroll);

    sweep();
    onScroll();
    /* 收尾轮询：兜住锚点跳转、字体载入、图片载入等迟到的一次性重排 */
    var ticks = 0;
    var settle = window.setInterval(function(){{
      sweep();
      onScroll();
      if(++ticks >= 10) window.clearInterval(settle);
    }}, 150);
  }} catch (err) {{
    /* 任何异常都退回「全部可见」，绝不留下空白页面 */
    root.classList.remove('rv');
    CARDS.forEach(function(c){{ c.classList.add('in'); }});
  }}

  /* ---------- 集号轨点击 ---------- */
  track.addEventListener('click', function(e){{
    var t = e.target.closest('i[data-session]');
    if(!t) return;
    var want = parseInt(t.getAttribute('data-session'), 10);
    var best = null;
    CARDS.forEach(function(c){{
      if(c.classList.contains('hide')) return;
      var s = parseInt(c.getAttribute('data-session'), 10);
      if(s < want) return;
      if(!best || s < parseInt(best.getAttribute('data-session'), 10)) best = c;
    }});
    if(!best){{ for(var i=CARDS.length-1;i>=0;i--){{ if(!CARDS[i].classList.contains('hide')){{ best=CARDS[i]; break; }} }} }}
    if(best) best.scrollIntoView({{behavior:'smooth', block:'center'}});
  }});

  /* ---------- 阶段跳转 ---------- */
  Array.prototype.forEach.call(document.querySelectorAll('.chip-era'), function(chip){{
    chip.addEventListener('click', function(){{
      var s = document.getElementById('era' + chip.getAttribute('data-era'));
      if(s) s.scrollIntoView({{behavior:'smooth', block:'start'}});
    }});
  }});

  /* ---------- 子题筛选 ---------- */
  var subChips = Array.prototype.slice.call(document.querySelectorAll('.chip-sub'));
  var allChip = document.getElementById('chip-all');
  function applyFilter(sub){{
    CARDS.forEach(function(c){{
      c.classList.toggle('hide', !!sub && c.getAttribute('data-sub') !== sub);
    }});
    ERAS.forEach(function(sec){{
      var any = sec.querySelector('article.ms:not(.hide)');
      sec.classList.toggle('hide', !any);
    }});
    allChip.classList.toggle('on', !sub);
    subChips.forEach(function(ch){{ ch.classList.toggle('on', ch.getAttribute('data-sub') === sub); }});
  }}
  allChip.addEventListener('click', function(){{ applyFilter(null); }});
  subChips.forEach(function(ch){{
    ch.addEventListener('click', function(){{
      var sub = ch.getAttribute('data-sub');
      applyFilter(ch.classList.contains('on') ? null : sub);
    }});
  }});

  /* ---------- 重置 ---------- */
  document.getElementById('reset').addEventListener('click', function(){{
    store = {{}}; persist();
    CARDS.forEach(function(c){{ c.classList.remove('read'); }});
  }});
}})();
</script>
</body>
</html>
'''

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")
    print(f"wrote {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())