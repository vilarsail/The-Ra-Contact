# journey-ra 滚动星旅 · 内容撰写规范

你的任务：为《一的法则》（The Ra Contact）的**一个主题**生成一个**单文件、零依赖的滚动星旅沉浸页**（scrollytelling），输出到 `study/journey_<topic>.html`。目标：让读者像坠入一段旅程一样读完这个主题在全书里的核心讨论——**生动与形象远比结构罗列重要**。已完成样例（本 skill 的形态基准）：`study/journey_densities.html`。

## 输入与输出

- 输入：`split/Ra_Session_*.md`（全书 106 集，英中逐段对照）。**先用 grep 在全书范围内检索主题相关句段，通读后再动笔**——星旅的内容必须来自跨集会的收网，不是单集摘要。
- 语言原则（与 study-ra 一致）：英文原文是唯一依据；引文必须是**英文原文的逐字子串**（含原标点、弯引号、方括号注；句中截断用 `…` 且省略号两侧留一个空格，不要自行补句号）；页面中文一律**自拟**，不得照抄译文行。
- 骨架模板：`.claude/skills/journey-ra/template.html`——CSS 与固定 JS（星空画布 / 氛围色插值 / 显影 / 进度轨道）**原样复制一字不改**，只替换 `{{PAGE_TITLE}}`、`{{STAGES}}`、`{{FOOTER_NOTE}}` 与 `@@CUSTOM_JS@@`。
- **不做音乐/声音**：模板无声音按钮，也不要自行添加。

## 页面结构

页面由两种区块组成，按旅程顺序排列：

### 时刻（scene，全屏居中）

```html
<section class="scene" id="sK" data-c="#f5efe2">
  <div class="stage">
    <p class="kicker">小节名</p>
    <p class="narr">自拟叙事（可用 <br> 分行，短句成诗）</p>
    <p class="en">"英文原句…"</p>
    <p class="zh">自拟中文释义</p>
    <p class="ref">—— SESSION NNN · (N.Y)</p>
  </div>
</section>
```

- **开场必须是 scene**（id="s0"）：一个钩子，把读者拉进旅程；末行可加 `<p class="hint">向下滚动 · … ▾</p>`。
- **终章必须是 scene**（id="sLast"）：旅程收束 + 本主题最核心的一句原书宣告；末尾加 `<button class="again" id="again">回到…</button>`（CUSTOM_JS 里绑定 `scrollTo({top:0,behavior:'smooth'})`）。
- 中间可穿插 1-2 个演出时刻（见「演出组件」）。

### 站点（station，左钉住 + 右细节流）

```html
<section class="station" id="sK" data-c="#c94b3a">
  <div class="pin"><div class="stage">
    <p class="kicker">站点名</p>
    <p class="narr">…</p>
    <p class="en">"主引文…"</p><p class="zh">…</p><p class="ref">…</p>
  </div></div>
  <div class="detail">
    <div class="frag">
      <p class="f-k">细节标题（2-8 字）</p>
      <p class="f-en">"英文原句…"</p>
      <p class="f-zh">自拟中文（一两句，精炼）</p>
      <p class="f-ref">—— SESSION NNN · (N.Y)</p>
    </div>
    …
  </div>
</section>
```

- 站点是主题的一个「章」：主画面钉在左侧，细节卡随滚动从右侧流过。
- 每站 **2-6 张细节卡**；全页 **细节卡 ≥12**。
- 细节卡的标题要**有画面感**（「两亿年的一堂课」「一锅浓汤」「没有学历要求」），不要用名词标签（「定义」「背景」）。

## 数量与覆盖

- 全页 **场景 + 站点 ≥8**，其中 **站点 ≥4**。
- **覆盖全书**：先用多个关键词 grep 全书（如主题为收割：`harvest / graduation / violet ray / ripe / fourth density`），把 Ra 关于该主题的**核心讨论都收进来**，然后精炼——宁缺毋滥，每张卡都必须值得停留。
- 引文总量一般在 25-50 处；每处都能在出处集会中逐字找到。

## 氛围色（data-c）

- 每个场景/站点必须写 `data-c`（十六进制色）。固定 JS 会在滚动时对全页氛围色做连续插值——**颜色弧线就是旅程的情绪线**。
- 惯例：开场与终章用暖白 `#f5efe2`；中间站点按主题选一条有意义的三至七段色弧（如密度页的彩虹弧、面纱页的灰白—深蓝弧）。

## 演出组件（可选，CUSTOM_JS）

每页最多 2 个，必须优雅降级（触屏/无鼠标时不影响阅读）：

| 组件 | 适用 | 用法 |
|---|---|---|
| **CSS 显形动画** | 概念的可视化（如棱镜分光） | 纯 CSS：`.demo` 内放几何元素，`.scene.on` 触发 transition；参考样例页的 `.prism/.ray` 写法 |
| **模糊显影** | 遗忘/隐藏类主题 | 给 `.narr` 加 class，在 CSS 中写 `blur(14px)→0` 的过渡（参考样例页 `#s5 .veiled`） |
| **对比路径** | 二元选择（服务他人/自我、正/负极性） | `.paths` + 两个 `.path.a/.b`，CUSTOM_JS 绑定 mouseenter/click 切换 `p-a/p-b` 类（参考 study-ra 样例） |
| **时间轴** | 历史叙事 | `.timeline` + `.tl-item`（模板已带样式），3-7 个节点 |

定制 JS 写在 `/* @@CUSTOM_JS@@ */` 处；不与保留名冲突：`size/frame/scenes/rail/io/ioFrag`。

## 忠实性规则

- 所有义理以 `split/` 英文段落为准；不引入原书没有的内容，不做宗派比较。
- **Ra 的拒答、限定、反问也是内容**，如实收录。
- 每条引文都能在 `f-ref`/`.ref` 所标 SESSION 的源文件中逐字找到（校验脚本会按出处核验，引文与出处必须对应，不许张冠李戴）。
- 术语首现给自拟白话定义；页面自足，未读过原书的读者也能看懂。

## 质量自检（写完后逐项过）

1. 无 `{{`、无 `@@CUSTOM_JS@@` 残留；无 soundBtn/音乐；无 quiz 字样。
2. 场景+站点 ≥8、站点 ≥4、细节卡 ≥12；开场为 `id="s0"` 的 scene，终章为 `id="sLast"` 的 scene。
3. 每个场景/站点有 `data-c`；颜色弧线有意义。
4. 每张细节卡有 f-k + f-en（逐字）+ f-zh（自拟）+ f-ref（SESSION 编号）。
5. 全部引文在各自出处集会中逐字可寻。
6. CUSTOM_JS 与模板保留名不冲突；id="again" 已绑定。
7. JS 括号配对；`node --check` 自查。
