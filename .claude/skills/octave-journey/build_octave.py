#!/usr/bin/env python3
"""Build study/Ra_Octave_Journey.html —— 单文件、离线、滚动驱动的沉浸式「八度之旅」原型。

读者是第一人称的意识本身：向下滚动 = 沿密度阶梯演化，一屏一幕，画面讲故事，
文字只做旁白。所有文字写死在 DOM 里，canvas 只负责氛围，JS 失效时文字全可见。

Usage: python3 build_octave.py
Output: study/Ra_Octave_Journey.html
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SPLIT = ROOT / "split"
OUT = ROOT / "study" / "Ra_Octave_Journey.html"

WS = re.compile(r"\s+")

# ---------------------------------------------------------------- 引文（英文必须是
# split 原文的精确有序子串；中文一律自拟，非 split 中译段）
QUOTES = {
    0: (6, "The Law of One states simply that all things are one, that all beings are one.",
        "一的法则只说了这一件事：万物是一，众生是一。"),
    1: (13, "the first density of awareness, or consciousness, of planetary entities.",
        "行星存有们最初的觉察密度——也就是意识的那一层。"),
    2: (13, "The second density strives towards the third density, which is the density of self-consciousness, or self-awareness.",
        "第二密度奋力走向第三密度，而第三密度就是自我意识、自我觉察的密度。"),
    3: (76, "The third density is a choice.",
        "第三密度，就是一次选择。"),
    4: (16, "That which fourth density is not: it is not of words, unless chosen.",
        "第四密度不是什么：它不属于言语——除非你自己选择用言语。"),
    5: (25, "The fifth density is the density of light, or wisdom.",
        "第五密度是光之密度，或者说，智慧之密度。"),
    6: (59, "The work of sixth density is to unify wisdom and compassion.",
        "第六密度的功课，是把智慧与悲悯合而为一。"),
    7: (41, "The seventh density is a density of completion and the turning towards timelessness, or foreverness.",
        "第七密度是完成之密度，也是转身朝向无时间、朝向永远的那一刻。"),
    8: (28, "However, it is well to perceive that the eighth density functions also as the beginning density, or first density—in its latter stages—of the next octave of densities.",
        "但有一点值得看清：第八密度同时也充当起始密度——在它的后期阶段，它就是下一个八度的第一密度。"),
}

# ---------------------------------------------------------------- 十幕旁白
SCENES = [
    dict(kicker="起初", lead="一切万有，本是一个。",
         sub="光从中心涌出，又向中心收回。你是被抛出去的那一粒——去经历一次漫长的遗忘。"),
    dict(kicker="第一密度 · 觉察", lead="尘埃落定，水与石开始记得自己。",
         sub="还没有「我」，只有存在本身，在黑暗里缓慢地结晶。"),
    dict(kicker="第二密度 · 生长", lead="从土里抬头，向光伸去。",
         sub="活着的第一个愿望，是想要更多的光。"),
    dict(kicker="第三密度 · 选择", lead="镜子碎了，你第一次看见两个方向。",
         sub="从此每件事都要选：向光，还是背光。这是这一密度唯一的功课。"),
    dict(kicker="第四密度 · 爱／理解", lead="懂得了「我」，才可能懂得「我们」。",
         sub="光开始穿过彼此，不再被挡住——这就是理解。"),
    dict(kicker="第五密度 · 光／智慧", lead="形体熔去，只剩光的几何。",
         sub="看得足够清楚，本身也是一种自由。"),
    dict(kicker="第六密度 · 合一／悲悯", lead="智慧与悲悯缠在一起，分不开。",
         sub="它们从来不是两条路，而是同一条路的两股。"),
    dict(kicker="第七密度 · 入口", lead="极性用尽了，万物向内消融。",
         sub="只剩中心一点，仍在，还在。门就在这一点上。"),
    dict(kicker="第八密度 · 八度", lead="光走到了尽头，翻过去。",
         sub="又是一粒光被抛出去——同一个故事，下一个八度。"),
    dict(kicker="收束", lead="这本书没有结尾。",
         sub="只有一圈又一圈的起点，而每一圈里，都等着一场你自己的选择。"),
]

N = len(SCENES)
INK = ["ink-light", "ink-light", "ink-light", "ink-light", "ink-light",
       "ink-light", "ink-light", "ink-dark", "ink-light", "ink-light"]

CSS = """
:root{
  --paper:#f7f3ec;
  --gold:#d8b366;
  --gold-deep:#8a6d1f;
  --serif:"Songti SC","Noto Serif SC","Source Han Serif SC","STSong",serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html{background:#06080f}
body{
  background:#06080f;color:#f4efe4;overflow-x:hidden;
  font-family:var(--serif);line-height:1.8;
  -webkit-font-smoothing:antialiased;
}
#sky{position:fixed;left:0;top:0;z-index:0;display:block;pointer-events:none}
#rail{position:fixed;right:16px;top:50%;transform:translateY(-50%);z-index:30;
  display:flex;flex-direction:column;gap:12px}
#rail button{
  width:7px;height:7px;padding:0;border:none;border-radius:50%;cursor:pointer;
  background:rgba(244,239,228,.22);
  transition:background .3s,transform .3s,box-shadow .3s;
}
#rail button:hover{background:rgba(244,239,228,.6)}
#rail button.on{background:var(--gold);transform:scale(1.55);
  box-shadow:0 0 12px rgba(216,179,102,.85)}
#hint{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);z-index:30;
  font-size:.70rem;letter-spacing:.42em;color:rgba(244,239,228,.6);
  pointer-events:none;animation:bob 2.6s ease-in-out infinite}
@keyframes bob{
  0%,100%{transform:translate(-50%,0);opacity:.45}
  50%{transform:translate(-50%,7px);opacity:.95}
}
#mark{position:fixed;left:22px;top:20px;z-index:30;pointer-events:none;
  font-size:.70rem;letter-spacing:.34em;color:#fff;opacity:.30;
  mix-blend-mode:difference}
#track{position:relative;z-index:10}
.scene{height:100vh;position:relative;overflow:hidden}
#tail{height:100vh}

/* ---- 旁白（默认静态可见；js 模式下改为固定层，由滚动驱动淡入淡出） ---- */
.copy{
  position:absolute;left:5.5vw;bottom:8vh;width:min(660px,84vw);
  z-index:20;opacity:1;
}
html.js .copy{position:fixed;z-index:20;opacity:0}
.copy .kicker{
  font-size:.70rem;letter-spacing:.40em;margin-bottom:.75em;
}
.copy .lead{
  font-size:clamp(1.32rem,2.9vw,2.02rem);font-weight:500;
  letter-spacing:.035em;line-height:1.52;margin-bottom:.5em;
}
.copy .sub{
  font-size:clamp(.85rem,1.45vw,.98rem);line-height:2.0;max-width:34em;
}
.copy.ink-light{color:#f4efe4;
  text-shadow:0 1px 18px rgba(2,4,10,.9),0 0 52px rgba(2,4,10,.6)}
.copy.ink-light .kicker{color:var(--gold)}
.copy.ink-light .sub{opacity:.74}
.copy.ink-dark{color:#2b251d;
  text-shadow:0 1px 20px rgba(255,255,255,.92)}
.copy.ink-dark .kicker{color:var(--gold-deep)}
.copy.ink-dark .sub{opacity:.76}

/* ---- Ra 原话抽屉（默认折叠，不打扰画面） ---- */
.copy .quote{
  margin-top:1.05em;padding-top:.72em;font-size:.80rem;max-width:42em;
  border-top:1px solid rgba(244,239,228,.22);
}
.copy.ink-dark .quote{border-top-color:rgba(43,37,29,.20)}
.copy .quote summary{
  list-style:none;cursor:pointer;display:inline-block;pointer-events:auto;
  font-size:.72rem;letter-spacing:.18em;opacity:.66;transition:opacity .2s;
}
.copy .quote summary::-webkit-details-marker{display:none}
.copy .quote summary:hover{opacity:1}
.copy .quote summary::after{content:"\\25BE";margin-left:.5em;font-size:.7em}
.copy .quote[open] summary::after{content:"\\25B4"}
.copy .quote blockquote{
  margin-top:.75em;padding-left:.95em;
  border-left:2px solid rgba(216,179,102,.55);
}
.copy .en{
  font-family:Georgia,"Times New Roman",serif;font-style:italic;
  font-size:.79rem;line-height:1.78;opacity:.86;
}
.copy .zh{font-size:.79rem;line-height:1.88;margin-top:.38em}
.copy .src{font-size:.66rem;letter-spacing:.2em;opacity:.5;margin-top:.5em}

@media (prefers-reduced-motion: reduce){
  #hint{animation:none;opacity:.5}
  html{scroll-behavior:auto}
}
"""

JS = r"""
(function(){
  var TAU = Math.PI * 2;
  var cv = document.getElementById('sky');
  var ctx = cv.getContext('2d');
  var N = 10;
  var W = 0, H = 0, DPR = 1, T = 0, SA = 1;
  var REDUCED = false;
  var copies = [], dots = [];
  var cache = {};

  /* ---------- 小工具 ---------- */
  function cl(v,a,b){ return v<a?a:(v>b?b:v); }
  function lp(a,b,t){ return a+(b-a)*t; }
  function ease(t){ t = cl(t,0,1); return t*t*(3-2*t); }
  function rgba(c,a){ return 'rgba('+(c[0]|0)+','+(c[1]|0)+','+(c[2]|0)+','+a+')'; }
  function mix(c1,c2,t){ return [lp(c1[0],c2[0],t),lp(c1[1],c2[1],t),lp(c1[2],c2[2],t)]; }
  function ga(a){ ctx.globalAlpha = cl(a*SA,0,1); }
  function mulberry32(a){
    return function(){
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      var t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function state(k, fn){ if(!cache[k]) cache[k] = fn(mulberry32(9781 + k.length * 7919)); return cache[k]; }
  function qbez(p0,p1,p2,u){
    var m = 1-u;
    return { x: m*m*p0.x + 2*m*u*p1.x + u*u*p2.x,
             y: m*m*p0.y + 2*m*u*p1.y + u*u*p2.y };
  }
  function glow(x,y,r,c,a){
    if(r <= 0.6 || a <= 0.002) return;
    var g = ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0, rgba(c,a));
    g.addColorStop(0.34, rgba(c,a*0.42));
    g.addColorStop(0.68, rgba(c,a*0.11));
    g.addColorStop(1, rgba(c,0));
    ga(1); ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(x,y,r,0,TAU); ctx.fill();
  }
  function disc(x,y,r,c,a){
    ga(a); ctx.fillStyle = rgba(c,1);
    ctx.beginPath(); ctx.arc(x,y,Math.max(0.4,r),0,TAU); ctx.fill();
  }
  function ring(x,y,rx,ry,c,a,lw){
    ga(a); ctx.strokeStyle = rgba(c,1); ctx.lineWidth = lw || 1;
    ctx.beginPath(); ctx.ellipse(x,y,Math.max(0.5,rx),Math.max(0.5,ry),0,0,TAU); ctx.stroke();
  }
  function bgRadial(cx,cy,innerR,inner,outer,sharp){
    var g = ctx.createRadialGradient(cx,cy,0,cx,cy,Math.max(1,innerR));
    if(sharp){
      g.addColorStop(0, rgba(inner,1));
      g.addColorStop(0.16, rgba(mix(inner,outer,0.32),1));
      g.addColorStop(0.42, rgba(mix(inner,outer,0.68),1));
      g.addColorStop(0.72, rgba(mix(inner,outer,0.90),1));
      g.addColorStop(1, rgba(outer,1));
    } else {
      g.addColorStop(0, rgba(inner,1));
      g.addColorStop(0.5, rgba(mix(inner,outer,0.5),1));
      g.addColorStop(1, rgba(outer,1));
    }
    ga(1); ctx.fillStyle = g; ctx.fillRect(-2,-2,W+4,H+4);
  }
  function scrim(mode){
    var g = ctx.createLinearGradient(0,H*0.36,0,H);
    if(mode === 'light'){
      g.addColorStop(0,'rgba(250,248,242,0)');
      g.addColorStop(0.5,'rgba(250,248,242,0.62)');
      g.addColorStop(1,'rgba(250,248,242,0.95)');
    } else {
      g.addColorStop(0,'rgba(5,8,18,0)');
      g.addColorStop(0.5,'rgba(5,8,18,0.52)');
      g.addColorStop(1,'rgba(3,5,13,0.92)');
    }
    ga(1); ctx.fillStyle = g; ctx.fillRect(-2,-2,W+4,H+4);
  }
  function leaf(x,y,rot,len,a){
    ctx.save(); ctx.translate(x,y); ctx.rotate(rot);
    ga(a); ctx.fillStyle = rgba([92,156,92],1);
    ctx.beginPath(); ctx.moveTo(0,0);
    ctx.quadraticCurveTo(len*0.55,-len*0.42,len,0);
    ctx.quadraticCurveTo(len*0.55,len*0.42,0,0);
    ctx.fill();
    ga(a*0.75); ctx.strokeStyle = rgba([198,222,152],1); ctx.lineWidth = 0.8;
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(len,0); ctx.stroke();
    ctx.restore();
  }
  function hexCell(x,y,r,rot){
    ctx.beginPath();
    for(var i=0;i<=6;i++){
      var a = rot + i/6*TAU;
      var px = x + Math.cos(a)*r, py = y + Math.sin(a)*r*0.86;
      if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
    }
    ctx.stroke();
    for(var j=0;j<3;j++){
      var a2 = rot + j/3*Math.PI;
      ctx.beginPath();
      ctx.moveTo(x-Math.cos(a2)*r, y-Math.sin(a2)*r*0.86);
      ctx.lineTo(x+Math.cos(a2)*r, y+Math.sin(a2)*r*0.86);
      ctx.stroke();
    }
  }
  function beam(x,c,a,hf){
    ctx.save();
    ctx.translate(x, H*0.5);
    ctx.scale(1, (hf||0.98)*H/(W*0.20));
    var g = ctx.createRadialGradient(0,0,0,0,0,W*0.20);
    g.addColorStop(0, rgba(c,a));
    g.addColorStop(0.42, rgba(c,a*0.5));
    g.addColorStop(1, rgba(c,0));
    ga(1); ctx.fillStyle = g;
    ctx.beginPath(); ctx.arc(0,0,W*0.20,0,TAU); ctx.fill();
    ctx.restore();
  }
  function drawCube(cx,cy,r,ry,rx,a,col){
    var v = [[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]];
    var e = [[0,1],[1,2],[2,3],[3,0],[4,5],[5,6],[6,7],[7,4],[0,4],[1,5],[2,6],[3,7]];
    var p = [], i;
    for(i=0;i<8;i++){
      var x = v[i][0], y = v[i][1], z = v[i][2];
      var x1 = x*Math.cos(ry) - z*Math.sin(ry);
      var z1 = x*Math.sin(ry) + z*Math.cos(ry);
      var y1 = y*Math.cos(rx) - z1*Math.sin(rx);
      var z2 = y*Math.sin(rx) + z1*Math.cos(rx);
      var d = 4/(4 + z2);
      p.push([cx + x1*r*d, cy + y1*r*d]);
    }
    ga(a); ctx.strokeStyle = rgba(col,1); ctx.lineWidth = 1.15;
    for(i=0;i<e.length;i++){
      ctx.beginPath();
      ctx.moveTo(p[e[i][0]][0], p[e[i][0]][1]);
      ctx.lineTo(p[e[i][1]][0], p[e[i][1]][1]);
      ctx.stroke();
    }
  }
  function drawOcta(cx,cy,r,ry,rx,a,col){
    var v = [[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
    var e = [[0,2],[2,1],[1,3],[3,0],[0,4],[4,1],[1,5],[5,0],[2,4],[4,3],[3,5],[5,2]];
    var p = [], i;
    for(i=0;i<6;i++){
      var x = v[i][0], y = v[i][1], z = v[i][2];
      var x1 = x*Math.cos(ry) - z*Math.sin(ry);
      var z1 = x*Math.sin(ry) + z*Math.cos(ry);
      var y1 = y*Math.cos(rx) - z1*Math.sin(rx);
      var z2 = y*Math.sin(rx) + z1*Math.cos(rx);
      var d = 4/(4 + z2);
      p.push([cx + x1*r*d, cy + y1*r*d]);
    }
    ga(a); ctx.strokeStyle = rgba(col,1); ctx.lineWidth = 1;
    for(i=0;i<e.length;i++){
      ctx.beginPath();
      ctx.moveTo(p[e[i][0]][0], p[e[i][0]][1]);
      ctx.lineTo(p[e[i][1]][0], p[e[i][1]][1]);
      ctx.stroke();
    }
  }

  /* ---------- 幕 0 · 造物者的光 ---------- */
  function scene0(t,Tx){
    var S = state('s0', function(r){
      var d = [], i, n = 210;
      for(i=0;i<n;i++) d.push({a:r()*TAU, rr:0.14+r()*1.02, sp:0.5+r()*1.1,
                               sz:0.5+r()*1.8, ph:r()});
      return {d:d};
    });
    var core = [255,250,232], night = [7,10,24];
    var Diag = Math.hypot(W,H), cx = W*0.5, cy = H*0.44;
    var k = Math.pow(cl(t,0,1),0.42);
    var innerR = lp(Diag*0.72, Diag*0.14, k);
    bgRadial(cx,cy,innerR,
             mix(core,[64,72,108],k),
             mix([192,194,212],night,Math.pow(cl(t,0,1),0.45)),
             true);

    var br = 0.72 + 0.28*Math.sin(Tx*1.15);
    for(var i=0;i<60;i++){
      var ang = i/60*TAU + Tx*0.04;
      var len = Diag*0.55*(0.5+0.5*br)*(0.55+0.45*Math.abs(Math.sin(i*2.3+Tx*0.5)));
      var x2 = cx+Math.cos(ang)*len, y2 = cy+Math.sin(ang)*len;
      var lg = ctx.createLinearGradient(cx,cy,x2,y2);
      lg.addColorStop(0, rgba([255,251,238], 0.26*br*(1-k*0.55)));
      lg.addColorStop(0.55, rgba([255,246,222], 0.09*br*(1-k*0.65)));
      lg.addColorStop(1, rgba([255,246,222], 0));
      ga(1); ctx.strokeStyle = lg; ctx.lineWidth = 1 + 2.2*br;
      ctx.beginPath(); ctx.moveTo(cx,cy); ctx.lineTo(x2,y2); ctx.stroke();
    }

    glow(cx,cy, Diag*0.30*br*(1-k*0.4), [255,251,235], 0.50*(1-k*0.45));

    var R0 = Diag*0.56;
    var env = cl(t*5,0,1) * (1 - cl((t-0.42)/0.48,0,1)*0.93);
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for(i=0;i<S.d.length;i++){
      var d = S.d[i];
      var u = (d.ph + Tx*0.055) % 1;
      var rr = d.rr * R0 * (1 - u*0.93);
      var ang2 = d.a + Tx*0.03*d.sp;
      var x = cx + Math.cos(ang2)*rr, y = cy + Math.sin(ang2)*rr*0.90;
      ga(0.50*(1-u)*env);
      ctx.fillStyle = rgba([255,244,214],1);
      ctx.beginPath(); ctx.arc(x,y,d.sz,0,TAU); ctx.fill();
    }
    ctx.restore();

    var sp = cl((t-0.50)/0.50,0,1);
    if(sp > 0){
      var e = ease(sp);
      ctx.save(); ctx.translate(cx,cy); ctx.rotate(-0.44); ctx.scale(1, 0.12+0.55*e);
      var gd = ctx.createRadialGradient(0,0,0,0,0,Math.max(1,W*0.50*e));
      gd.addColorStop(0, rgba(night, 0.95*e));
      gd.addColorStop(0.55, rgba(night, 0.50*e));
      gd.addColorStop(1, rgba(night, 0));
      ga(1); ctx.fillStyle = gd;
      ctx.beginPath(); ctx.arc(0,0,Math.max(1,W*0.50*e),0,TAU); ctx.fill();
      ctx.restore();
    }

    scrim('dark');

    if(sp > 0){
      var m = ease(cl((t-0.60)/0.40,0,1));
      var mx = lp(cx, W*0.79, m), my = lp(cy, H*0.795, m);
      var br2 = 0.8 + 0.2*Math.sin(Tx*2.6);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(mx,my, 22+16*br2, [255,242,210], 0.85);
      disc(mx,my, 3.0+0.8*br2, [255,253,246], 1);
      ctx.restore();
    }
  }

  /* ---------- 幕 1 · 第一密度 · 觉察 ---------- */
  function scene1(t,Tx){
    var cols = 9, rows = 6;
    var S = state('s1', function(r){
      var d = [], i;
      for(i=0;i<cols*rows;i++){
        var gx = i % cols, gy = (i/cols)|0;
        d.push({
          sx: r()*W, sy: H*0.06 + r()*H*0.86,
          tx: W*0.5 + (gx/(cols-1)-0.5)*W*0.34 + (r()-0.5)*W*0.04,
          ty: H*0.30 + (gy/(rows-1)-0.5)*H*0.34 + (r()-0.5)*H*0.04,
          sz: 0.5 + r()*1.5
        });
      }
      return {d:d};
    });
    var Diag = Math.hypot(W,H);
    bgRadial(W*0.5,H*0.5,Diag*0.70,[13,17,36],[3,5,13]);

    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for(var q=0;q<3;q++){
      ga(0.10 - 0.028*q);
      ctx.strokeStyle = rgba([104,146,186],1); ctx.lineWidth = 1;
      ctx.beginPath();
      for(var x=0;x<=W;x+=7){
        var y = H*0.84 + q*8 + Math.sin(x*0.011 + Tx*0.75 + q*1.3)*4.5
                + Math.sin(x*0.028 - Tx*0.5)*2;
        if(x===0) ctx.moveTo(x,y); else ctx.lineTo(x,y);
      }
      ctx.stroke();
    }
    ctx.restore();

    var env = cl(t*6,0,1) * (0.08 + 0.92*cl((1.06-t)/0.42,0,1));
    var mv = ease(cl(t/0.70,0,1));
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for(var i=0;i<S.d.length;i++){
      var d = S.d[i];
      var x2 = lp(d.sx,d.tx,mv), y2 = lp(d.sy,d.ty,mv);
      ga((0.10 + 0.55*mv)*env);
      ctx.fillStyle = rgba(mix([150,170,200],[255,236,196],mv),1);
      ctx.beginPath(); ctx.arc(x2,y2,d.sz,0,TAU); ctx.fill();
    }
    ctx.restore();

    var cr = cl((t-0.60)/0.32,0,1);
    if(cr > 0){
      var sites = [[0,0],[-1,0],[1,0],[0,-1],[0,1],[-1,-1],[1,1]];
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for(var s=0;s<sites.length;s++){
        var sx = W*0.5 + sites[s][0]*W*0.115;
        var sy = H*0.46 + sites[s][1]*H*0.115;
        var rad = Math.min(W,H)*(0.045 + 0.012*Math.sin(Tx*0.9 + s));
        ga(0.42*cr*env);
        ctx.strokeStyle = rgba([226,190,112],1); ctx.lineWidth = 1;
        hexCell(sx,sy,rad, Tx*0.18 + s*0.3);
      }
      ctx.restore();
    }

    var fp = cl((t-0.72)/0.28,0,1);
    if(fp > 0){
      var b = 0.5 + 0.5*Math.sin(Tx*1.25);
      glow(W*0.5,H*0.47, 90 + 60*b, [176,196,224], 0.11*fp*(0.5+0.7*b));
    }
    scrim('dark');
  }

  /* ---------- 幕 2 · 第二密度 · 生长 ---------- */
  function scene2(t,Tx){
    var base = {x:W*0.36, y:H*0.95}, light = {x:W*0.70, y:H*0.13};
    bgRadial(light.x, light.y, Math.hypot(W,H)*0.75, [17,19,30], [5,6,14]);
    var lk = cl(t/0.85,0,1);
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    glow(light.x, light.y, Math.min(W,H)*0.55, [255,238,198], 0.12 + 0.30*lk);
    ctx.restore();

    var grow = ease(cl(t/0.76,0,1));
    if(grow > 0.004){
      var bend = cl(t/0.9,0,1);
      var P0 = {x:base.x, y:base.y};
      var P2 = {x: base.x + (light.x-base.x)*(0.26+0.44*bend),
                y: base.y - H*(0.60+0.16*bend)};
      var P1 = {x: base.x + W*0.05 + W*0.09*bend, y: base.y - H*0.22};
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      ctx.lineCap = 'round';
      var steps = 72, upto = Math.max(1, Math.round(grow*steps));
      for(var i=0;i<=upto;i++){
        var p = qbez(P0,P1,P2, i/steps);
        var q = qbez(P0,P1,P2, Math.min(1,(i+1)/steps));
        var u = i/steps;
        ga(0.85);
        ctx.strokeStyle = rgba(mix([116,138,92],[210,186,126],u),1);
        ctx.lineWidth = lp(4.4,1.0,Math.pow(u,0.7))*cl(t*5,0,1);
        ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(q.x,q.y); ctx.stroke();
        if(i % 8 === 0) glow(p.x,p.y, 11, [200,214,140], 0.045);
      }
      var brs = [[0.30,1],[0.50,-1],[0.68,1],[0.84,-1]];
      for(var b2=0;b2<brs.length;b2++){
        var ub = brs[b2][0], sgn = brs[b2][1];
        var bg = cl((grow-ub)/0.22,0,1);
        if(bg <= 0) continue;
        var e2 = ease(bg);
        var pb = qbez(P0,P1,P2,ub);
        var L = Math.min(W,H)*0.13*e2;
        var tx2 = pb.x + sgn*L*0.9, ty2 = pb.y - L*0.85;
        ga(0.72); ctx.strokeStyle = rgba([168,182,120],1); ctx.lineWidth = 1.6;
        ctx.beginPath(); ctx.moveTo(pb.x,pb.y);
        ctx.quadraticCurveTo(pb.x + sgn*L*0.5, pb.y + L*0.06, tx2, ty2);
        ctx.stroke();
        leaf(tx2, ty2, Math.atan2(ty2-pb.y, tx2-pb.x), 12*e2, 0.85*e2);
        leaf(lp(pb.x,tx2,0.55), lp(pb.y,ty2,0.55),
             Math.atan2(ty2-pb.y, tx2-pb.x), 9*e2, 0.6*e2);
      }
      ctx.restore();
    }
    scrim('dark');
  }

  /* ---------- 幕 3 · 第三密度 · 选择 ---------- */
  function scene3(t,Tx){
    var BRK = 0.44;
    var Diag = Math.hypot(W,H);
    bgRadial(W*0.5,H*0.48,Diag*0.72,[19,17,28],[4,5,13]);
    var colL = W*0.19, colR = W*0.81;
    var pulse = 0.5 + 0.5*Math.sin(Tx*0.85);
    var S = state('s3', function(r){
      var sh = [], ps = [], i;
      for(i=0;i<34;i++) sh.push({a:r()*TAU, sp:0.22+r()*1.0, w:6+r()*22, h:14+r()*54,
                                 rot:r()*TAU, vr:(r()-0.5)*1.6});
      for(i=0;i<280;i++) ps.push({side:(i%2), d:r(), off:(r()-0.5)*H*0.62,
                                  sz:0.6+r()*1.5});
      return {sh:sh, ps:ps};
    });

    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    beam(colL, [214,166,92], 0.24 + 0.11*pulse);
    beam(colR, [104,152,214], 0.24 + 0.11*(1-pulse));
    ctx.restore();

    if(t < BRK + 0.07){
      var a0 = cl((BRK + 0.07 - t)/0.11, 0, 1);
      ctx.save(); ctx.translate(W*0.5, H*0.5);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      var mg = ctx.createLinearGradient(0,-H*0.34,0,H*0.34);
      mg.addColorStop(0,'rgba(190,205,225,0)');
      mg.addColorStop(0.5,'rgba(232,240,250,'+(0.55*a0)+')');
      mg.addColorStop(1,'rgba(190,205,225,0)');
      ga(1); ctx.fillStyle = mg;
      ctx.beginPath(); ctx.ellipse(0,0,W*0.020,H*0.33,0,0,TAU); ctx.fill();
      glow(0, Math.sin(Tx*0.8)*H*0.15, W*0.07, [255,255,255], 0.28*a0);
      ctx.restore(); ctx.restore();
    }

    var bp = cl((t-BRK)/0.28,0,1);
    if(bp > 0){
      var e = ease(bp), fade = cl(1 - bp*1.05, 0, 1);
      for(var i=0;i<S.sh.length;i++){
        var s = S.sh[i];
        var dd = Math.pow(e,0.8)*s.sp;
        var x = W*0.5 + Math.cos(s.a)*dd*W*0.52;
        var y = H*0.5 + Math.sin(s.a)*dd*H*0.55;
        var aa = 0.72*fade;
        ctx.save(); ctx.translate(x,y); ctx.rotate(s.rot + s.vr*e*2.4);
        var g = ctx.createLinearGradient(-s.w/2,-s.h/2,s.w/2,s.h/2);
        g.addColorStop(0,'rgba(226,238,250,'+aa+')');
        g.addColorStop(0.5,'rgba(158,180,208,'+(aa*0.55)+')');
        g.addColorStop(1,'rgba(226,238,252,'+(aa*0.85)+')');
        ga(1); ctx.fillStyle = g;
        ctx.beginPath();
        ctx.moveTo(-s.w/2,-s.h/2); ctx.lineTo(s.w/2,-s.h*0.35);
        ctx.lineTo(s.w*0.35,s.h/2); ctx.lineTo(-s.w*0.42,s.h*0.4);
        ctx.closePath(); ctx.fill();
        ga(aa*0.85); ctx.strokeStyle = 'rgba(255,255,255,1)';
        ctx.lineWidth = 0.7; ctx.stroke();
        ctx.restore();
      }
    }

    var sp2 = cl((t-0.66)/0.34,0,1);
    if(sp2 > 0){
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      for(var j=0;j<S.ps.length;j++){
        var p = S.ps[j];
        var u2 = ease(cl((sp2 - p.d*0.32)/(1 - p.d*0.32),0,1));
        var tgt = p.side ? colR : colL;
        var x2 = lp(W*0.5, tgt, u2*0.96);
        var y2 = lp(H*0.5, H*0.44, u2) + p.off*(1-u2);
        ga(0.26 + 0.50*u2);
        ctx.fillStyle = rgba(p.side ? [150,196,246] : [248,214,142], 1);
        ctx.beginPath(); ctx.arc(x2,y2,p.sz*(0.6+u2*0.6),0,TAU); ctx.fill();
      }
      ctx.restore();
    }
    scrim('dark');
  }

  /* ---------- 幕 4 · 第四密度 · 爱／理解 ---------- */
  function scene4(t,Tx){
    var Diag = Math.hypot(W,H);
    bgRadial(W*0.5,H*0.44,Diag*0.70,[28,19,42],[6,6,16]);
    var S = state('s4', function(r){
      var sp = [], i, n = 9;
      for(i=0;i<n;i++) sp.push({a:i/n*TAU + (r()-0.5)*0.14, sz:0.052+r()*0.036,
                                ph:r()*TAU, bob:0.6+r()*0.8});
      return {sp:sp};
    });
    var cx = W*0.5, cy = H*0.42, rad = Math.min(W,H)*0.30;
    var inA = cl(t/0.5,0,1);
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for(var i=0;i<S.sp.length;i++){
      var s = S.sp[i], a = s.a + Tx*0.055;
      var x = cx + Math.cos(a)*rad;
      var y = cy + Math.sin(a)*rad*0.60 + Math.sin(Tx*s.bob + s.ph)*8;
      var sr = Math.min(W,H)*s.sz*(1 + 0.07*Math.sin(Tx*1.1 + s.ph))*inA;
      glow(x,y,sr*3.6,[242,196,138],0.20);
      disc(x,y,sr,[255,238,208],0.10*inA);
      ring(x,y,sr,sr,[255,242,220],0.40*inA,1);
      ring(x,y,sr*0.62,sr*0.62,[250,206,150],0.22*inA,1);
    }
    var beat = 0.5 + 0.5*Math.sin(Tx*1.5);
    glow(cx,cy, Math.min(W,H)*0.30*(0.8+0.3*beat), [228,104,110], 0.15 + 0.16*beat);
    for(var k=0;k<4;k++){
      var rr2 = (Tx*0.20 + k/4) % 1;
      ring(cx,cy, rad*rr2*1.45 + 2, rad*0.60*rr2*1.45 + 2,
           [242,150,138], 0.26*(1-rr2)*(1-rr2)*inA, 1.6);
    }
    disc(cx,cy, 5 + 3*beat, [255,216,200], 0.72);
    ctx.restore();
    scrim('dark');
  }

  /* ---------- 幕 5 · 第五密度 · 光／智慧 ---------- */
  function scene5(t,Tx){
    var k = ease(cl(t,0,1));
    var Diag = Math.hypot(W,H);
    bgRadial(W*0.5,H*0.44, lp(Diag*0.30, Diag*0.95, k),
             mix([20,24,38],[206,230,238],k),
             mix([5,7,16],[46,96,116],k*0.85));
    var vp = {x:W*0.5, y:H*0.44};
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    ga(0.06 + 0.10*k); ctx.strokeStyle = rgba([226,190,116],1); ctx.lineWidth = 1;
    for(var i=-9;i<=9;i++){
      ctx.beginPath();
      ctx.moveTo(vp.x + i*W*0.055, H*1.06);
      ctx.lineTo(vp.x + i*W*0.016, vp.y + 6);
      ctx.stroke();
    }
    for(var j=1;j<=10;j++){
      var yy = vp.y + Math.pow(j/10, 2.2)*(H*1.06 - vp.y);
      ctx.beginPath(); ctx.moveTo(0,yy); ctx.lineTo(W,yy); ctx.stroke();
    }
    var r0 = Math.min(W,H)*0.19;
    glow(W*0.5,H*0.44, r0*3.2, mix([120,150,180],[255,252,244],k), 0.08 + 0.18*k);
    drawCube(W*0.5,H*0.44, r0,      Tx*0.32,  Tx*0.19, 0.14 + 0.55*k, [236,246,252]);
    drawCube(W*0.5,H*0.44, r0*0.62, -Tx*0.46, Tx*0.27, 0.12 + 0.50*k, [232,206,150]);
    drawOcta(W*0.5,H*0.44, r0*1.42,  Tx*0.22, Tx*0.14, 0.08 + 0.34*k, [180,220,232]);
    ctx.restore();
    scrim('dark');
  }

  /* ---------- 幕 6 · 第六密度 · 合一／悲悯 ---------- */
  function scene6(t,Tx){
    var Diag = Math.hypot(W,H);
    var tw = Math.sin(cl(t,0,1)*Math.PI);
    var cx = W*0.5;
    bgRadial(cx,H*0.44,Diag*0.72, mix([22,18,34],[40,36,48],tw*0.5), [5,5,14]);
    var top = H*0.10, bot = H*0.92, NP = 120, amp = W*0.115*tw;
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for(var s=0;s<2;s++){
      var col = s === 0 ? [246,208,132] : [140,204,226];
      var colw = mix(col, [255,252,246], cl(1 - tw*1.1, 0, 1));
      for(var i=0;i<=NP;i++){
        var u = i/NP;
        var y = lp(top,bot,u);
        var ang = u*Math.PI*3.6 + s*Math.PI + Tx*0.45;
        var x = cx + Math.cos(ang)*amp;
        var z = Math.sin(ang)*amp;
        var sc = 1 + z/(Math.max(amp,1)*3.2);
        ga(0.10 + 0.30*(0.5 + 0.5*sc));
        ctx.fillStyle = rgba(colw,1);
        ctx.beginPath(); ctx.arc(x,y, 1.2 + 2.4*Math.max(0, sc-0.3), 0, TAU); ctx.fill();
        if(i % 6 === 0) glow(x,y, 11, colw, 0.045);
      }
    }
    var beat = 0.5 + 0.5*Math.sin(Tx*0.9);
    var merge = cl((t-0.45)/0.55,0,1);
    glow(cx,H*0.44, Math.min(W,H)*(0.10 + 0.16*merge)*(0.85 + 0.25*beat),
         [255,246,226], 0.20 + 0.26*merge);
    disc(cx,H*0.44, 3 + 4*beat + 3*merge, [255,252,244], 0.6 + 0.35*merge);
    ctx.restore();
    scrim('dark');
  }

  /* ---------- 幕 7 · 第七密度 · 入口 ---------- */
  function scene7(t,Tx){
    var Diag = Math.hypot(W,H);
    var k = ease(cl(t,0,1));
    bgRadial(W*0.5,H*0.44, Diag*0.95,
             mix([246,242,232],[255,253,247],k),
             mix([222,214,196],[248,244,236],k));
    var S = state('s7', function(r){
      var d = [], i;
      for(i=0;i<150;i++) d.push({a:r()*TAU, rr:0.18+r()*1.0, ph:r(), sz:0.5+r()*1.5});
      return {d:d};
    });
    var R0 = Diag*0.55;
    for(var i=0;i<S.d.length;i++){
      var d = S.d[i];
      var u = (d.ph + Tx*0.045) % 1;
      var rr = d.rr * R0 * (1 - u*0.95);
      var x = W*0.5 + Math.cos(d.a)*rr, y = H*0.44 + Math.sin(d.a)*rr*0.86;
      ga(0.30*(1-u)*(1 - k*0.65));
      ctx.fillStyle = rgba([150,140,118],1);
      ctx.beginPath(); ctx.arc(x,y,d.sz*0.9,0,TAU); ctx.fill();
    }
    var pa = cl(1 - t*1.7, 0, 1)*0.5;
    if(pa > 0.01){
      var sx = W*0.29, sy = H*0.30, sr = Math.min(W,H)*0.030;
      ga(pa); ctx.strokeStyle = rgba([176,132,44],1); ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(sx,sy,sr,0,TAU); ctx.stroke();
      for(var q=0;q<12;q++){
        var aq = q/12*TAU;
        ctx.beginPath();
        ctx.moveTo(sx + Math.cos(aq)*sr*1.3, sy + Math.sin(aq)*sr*1.3);
        ctx.lineTo(sx + Math.cos(aq)*sr*1.9, sy + Math.sin(aq)*sr*1.9);
        ctx.stroke();
      }
      var mx = W*0.71, my = H*0.30, mr = Math.min(W,H)*0.034;
      ga(pa); ctx.fillStyle = rgba([86,124,168],1);
      ctx.beginPath(); ctx.arc(mx,my,mr,0,TAU); ctx.fill();
      ga(1); ctx.fillStyle = rgba([250,247,240],1);
      ctx.beginPath(); ctx.arc(mx + mr*0.55, my - mr*0.22, mr*0.86, 0, TAU); ctx.fill();
    }
    var ck = cl((t-0.35)/0.65,0,1);
    if(ck > 0.01){
      glow(W*0.5,H*0.44, Math.min(W,H)*(0.05 + 0.05*ck), [186,148,64], 0.30*ck);
      disc(W*0.5,H*0.44, 2.2 + 1.2*ck, [150,112,40], 0.85*ck);
    }
    scrim('light');
  }

  /* ---------- 幕 8 · 第八密度 · 八度 ---------- */
  function scene8(t,Tx){
    var Diag = Math.hypot(W,H);
    var k = cl(t,0,1);
    var night = cl((k-0.26)/0.55, 0, 1);
    var white = cl((0.18-k)/0.18, 0, 1);
    var fl = Math.exp(-Math.pow((k-0.20)/0.05, 2));
    var inner = mix(mix([246,242,230],[9,12,28],night), [255,255,255], fl);
    var outer = mix(mix([224,218,200],[5,7,18],night), [255,255,255], white*0.8 + fl*0.2);
    bgRadial(W*0.5,H*0.46, lp(Diag*0.95, Diag*0.35, night*0.9)*lp(1,0.5,white), inner, outer);

    var rg = cl((k-0.18)/0.30, 0, 1);
    if(rg > 0 && rg < 1){
      ring(W*0.5,H*0.46, Diag*0.75*ease(rg), Diag*0.62*ease(rg),
           [255,255,255], 0.35*(1-rg), 2.5);
    }
    if(white > 0.02){
      glow(W*0.5,H*0.46, Math.min(W,H)*0.55, [255,250,232], 0.25*white);
    }
    scrim('dark');
    var m = ease(cl((k-0.40)/0.52,0,1));
    if(m > 0.01){
      var x = lp(W*0.5, W*0.80, m), y = lp(H*0.46, H*0.80, m);
      var br = 0.8 + 0.2*Math.sin(Tx*2.4);
      ctx.save(); ctx.globalCompositeOperation = 'lighter';
      glow(x,y, 22 + 16*br, [255,242,210], 0.80);
      disc(x,y, 2.8 + 0.8*br, [255,253,246], 1);
      ctx.restore();
    }
  }

  /* ---------- 幕 9 · 收束 ---------- */
  function scene9(t,Tx){
    var Diag = Math.hypot(W,H);
    bgRadial(W*0.5,H*0.44,Diag*0.55,[10,12,24],[2,3,9]);
    var S = state('s9', function(r){
      var s = [], i;
      for(i=0;i<130;i++) s.push({x:r(), y:r()*0.8, sz:0.3+r()*1.0,
                                 ph:r()*TAU, sp:0.5+r()});
      return {s:s};
    });
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    var fade = cl(t*3,0,1);
    for(var i=0;i<S.s.length;i++){
      var s = S.s[i];
      var a = (0.10 + 0.30*(0.5 + 0.5*Math.sin(Tx*0.5*s.sp + s.ph)))*fade;
      ga(a);
      ctx.fillStyle = rgba([236,240,250],1);
      ctx.beginPath(); ctx.arc(s.x*W, s.y*H, s.sz, 0, TAU); ctx.fill();
    }
    var b = 0.5 + 0.5*Math.sin(Tx*0.7);
    glow(W*0.5,H*0.44, Math.min(W,H)*(0.10 + 0.06*b), [255,246,220], 0.14 + 0.20*b);
    disc(W*0.5,H*0.44, 2.4 + 1.6*b, [255,252,244], 0.7 + 0.3*b);
    ctx.restore();
    scrim('dark');
  }

  var SCENES = [scene0,scene1,scene2,scene3,scene4,scene5,scene6,scene7,scene8,scene9];

  /* ---------- 引擎 ---------- */
  function resize(){
    W = window.innerWidth; H = window.innerHeight;
    DPR = Math.min(1.75, window.devicePixelRatio || 1);
    cv.width = Math.round(W*DPR); cv.height = Math.round(H*DPR);
    cv.style.width = W + 'px'; cv.style.height = H + 'px';
    ctx.setTransform(DPR,0,0,DPR,0,0);
  }
  function drawScene(i,t,Tx,a){
    SA = a; SCENES[i](t,Tx); SA = 1;
  }
  function frame(){
    var raw = window.scrollY / H;
    var i = Math.floor(raw);
    if(i < 0) i = 0;
    if(i > N-1) i = N-1;
    var t = cl(raw - i, 0, 1);
    var Tx = REDUCED ? 0 : T;
    if(REDUCED) t = 0.5;

    ctx.setTransform(DPR,0,0,DPR,0,0);
    ctx.clearRect(0,0,W,H);
    drawScene(i, t, Tx, 1);
    if(!REDUCED && t > 0.78 && i < N-1){
      drawScene(i+1, 0.02, Tx, (t-0.78)/0.22);
    }
    updateCopies(raw);
    updateDots(i);
  }
  function updateCopies(raw){
    var idx = Math.min(raw, N - 1 + 0.999);
    for(var k=0;k<copies.length;k++){
      var el = copies[k];
      var p = idx - k;
      var a, dy;
      if(REDUCED){
        a = (p >= 0 && p < 1) ? 1 : 0; dy = 0;
      } else if(p >= 0 && p < 1){
        var ain = cl(p/0.12, 0, 1);
        a = (k < N-1) ? ain*cl((1-p)/0.16, 0, 1) : ain;
        dy = lp(20, 0, ain);
      } else { a = 0; dy = 0; }
      el.style.opacity = a;
      el.style.transform = 'translateY(' + dy.toFixed(1) + 'px)';
      el.style.pointerEvents = a > 0.05 ? 'auto' : 'none';
    }
  }
  function updateDots(i){
    for(var k=0;k<dots.length;k++){
      if(k === i) dots[k].classList.add('on');
      else dots[k].classList.remove('on');
    }
    if(hint) hint.style.opacity = (i === 0 ? cl(1 - T*0.35, 0, 1) : 0);
  }

  var hint = document.getElementById('hint');
  function tick(){
    try{
      if(!REDUCED) T += 0.016;
      frame();
    } catch(err){
      document.documentElement.className = '';
      for(var k=0;k<copies.length;k++) copies[k].style.cssText = '';
      return;
    }
    requestAnimationFrame(tick);
  }

  function boot(){
    copies = [].slice.call(document.querySelectorAll('.copy'));
    dots = [].slice.call(document.querySelectorAll('#rail button'));
    REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    resize();
    window.addEventListener('resize', function(){ resize(); });
    for(var k=0;k<dots.length;k++){
      (function(kk){
        dots[kk].addEventListener('click', function(){
          window.scrollTo({ top: kk*window.innerHeight, behavior: 'smooth' });
        });
      })(k);
    }
    frame();
    requestAnimationFrame(tick);
  }
  boot();
})();
"""


def verify_quotes() -> int:
    cache = {}
    bad = []
    for scene, (sess, en, _zh) in sorted(QUOTES.items()):
        if sess not in cache:
            cache[sess] = WS.sub(" ", (SPLIT / f"Ra_Session_{sess:03d}.md").read_text(encoding="utf-8")).strip()
        if WS.sub(" ", en).strip() not in cache[sess]:
            bad.append((scene, sess, en))
    if bad:
        for scene, sess, en in bad:
            print(f"FAIL 幕{scene} s{sess}: {en[:100]!r}", file=sys.stderr)
        return 1
    print(f"引文核验通过：{len(QUOTES)}/{len(QUOTES)}")
    return 0


def scene_html(i: int) -> str:
    s = SCENES[i]
    q = QUOTES.get(i)
    drawer = ""
    if q:
        sess, en, zh = q
        drawer = f"""
      <details class="quote">
        <summary>看 Ra 原话</summary>
        <blockquote>
          <p class="en">{html.escape(en, quote=True)}</p>
          <p class="zh">{html.escape(zh, quote=True)}</p>
          <p class="src">第 {sess:03d} 集</p>
        </blockquote>
      </details>"""
    return f"""  <section class="scene" id="scene-{i}">
    <div class="copy {INK[i]}">
      <p class="kicker">{html.escape(s["kicker"])}</p>
      <h2 class="lead">{html.escape(s["lead"])}</h2>
      <p class="sub">{html.escape(s["sub"])}</p>{drawer}
    </div>
  </section>"""


def build() -> str:
    sections = "\n".join(scene_html(i) for i in range(N))
    dots = "".join(f'\n  <button type="button" aria-label="第 {i+1} 幕"></button>'
                   for i in range(N))
    return f"""<!DOCTYPE html>
<html lang="zh-CN" class="nojs">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="dark">
<title>八度之旅 · 一的法则</title>
<style>{CSS}</style>
<script>document.documentElement.className='js';</script>
<noscript><style>#rail,#hint{{display:none}}</style></noscript>
</head>
<body>
<canvas id="sky" aria-hidden="true"></canvas>
<div id="mark" aria-hidden="true">八度之旅</div>
<nav id="rail" aria-hidden="true">{dots}
</nav>
<div id="hint" aria-hidden="true">向下滚动</div>
<main id="track">
{sections}
  <div id="tail" aria-hidden="true"></div>
</main>
<script>{JS}</script>
</body>
</html>
"""


def main() -> int:
    if verify_quotes():
        return 1
    doc = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc, encoding="utf-8")

    checks = [
        ("外链数量为 0", "http://" not in doc and "https://" not in doc),
        (f"幕数 = {N}", doc.count('class="scene"') == N),
        ("引文抽屉 = 9", doc.count('<details class="quote">') == len(QUOTES)),
        ("无占位符残留", "__" not in doc.split("<style>")[0] and "{{" not in doc),
    ]
    for label, ok in checks:
        print(("  OK  " if ok else " FAIL ") + label)
    print(f"输出 {OUT}  ({len(doc.encode('utf-8'))/1024:.1f} KB)")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())