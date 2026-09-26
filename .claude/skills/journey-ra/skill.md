---
name: journey-ra
description: 为《一的法则》(The Ra Contact) 的一个主题（密度、收割、极性、面纱、催化剂、疗愈、能量中心、流浪者、星际联邦、地球史、原型、死亡、造物…）生成单文件零依赖的滚动星旅沉浸页 study/journey_<topic>.html——全屏"时刻"与"左钉住主画面+右细节流"的"站点"交替推进，氛围色随旅程连续演变，跨集会收网主题讨论，英文引文逐字摘录+自拟中文。结构骨架固定，仅内容随主题变化。当用户输入 /journey-ra <主题...> 或要求"为某主题生成星旅/沉浸页/滚动叙事"时触发。
---

# 角色与目标

为《一的法则》的一个**主题**生成滚动星旅沉浸页 `study/journey_<topic>.html`：让读者像坠落/攀升一段旅程一样，轻松愉快地读完该主题在全书的核心讨论。形态基准（先看它找手感）：`study/journey_densities.html`。**生动与形象的重要性远大于表述的结构性**——这是内容是排布、不是知识清单。

# 架构

```
template.html（CSS + 固定 JS：星空/氛围色插值/显影/轨道，占位符）
        │  原样复制，替换 {{PAGE_TITLE}} {{STAGES}} {{FOOTER_NOTE}} @@CUSTOM_JS@@
        ▼
study/journey_<topic>.html
        │
        ▼
check_journey.py（确定性校验：结构数量、占位符、data-c、引文按出处逐字核验）
```

- 内容规范：`.claude/skills/journey-ra/AGENT_INSTRUCTIONS.md`——**写内容前必须先读它**。
- **不做音乐/声音**（用户明确去掉）；模板与校验都不含声音按钮。

# 命名规则与主题注册表

文件名统一为 `study/journey_<topic>.html`，topic 为小写英文 kebab 词。已规划/已建的主题：

| topic | 主题 | 状态 |
|---|---|---|
| densities | 密度与八度音程 | ✓ 已建（形态基准） |
| harvest | 收割与毕业 | ✓ 已建 |
| polarity | 极性与两种道路 | ✓ 已建 |
| veil | 遗忘面纱 | ✓ 已建 |
| catalyst | 催化剂 | ✓ 已建 |
| healing | 疗愈 | ✓ 已建 |
| ray | 七个能量中心与光芒 | ✓ 已建 |
| wanderer | 流浪者 | ✓ 已建 |
| confederation | 星际联邦与守护 | ✓ 已建 |
| history | 地球的史诗（火星/马尔戴克/亚特兰蒂斯/埃及） | ✓ 已建 |
| archetype | 原型心智与塔罗 | ✓ 已建 |
| death | 死亡、中阴与转世 | ✓ 已建 |
| creation | 造物、逻各斯与智能无限 | ✓ 已建 |

新主题先在此表登记再生成；索引页 `study/journeys.html` 随之更新。

# 工作流

## 步骤一：准备

确认主题与文件名（上表登记）；`mkdir -p study`（已存在则跳过）。

## 步骤二：生成（LLM 全书收网后撰写）

单主题主代理直做：grep 全书检索主题相关句段 → 通读 → Read `template.html` 与 `AGENT_INSTRUCTIONS.md` → Write `study/journey_<topic>.html`。

多主题（≥4 个）：每主题派发一个子 Agent（`subagent_type: general-purpose`），同一轮消息并行派发。prompt 模板：

```
读取 .claude/skills/journey-ra/AGENT_INSTRUCTIONS.md 获取滚动星旅内容撰写规范，严格按其要求执行。

主题：<主题中文名>（topic: <kebab>）—— 收网范围提示：<建议的 grep 关键词>
输入：split/Ra_Session_*.md（全书检索，英文为准）
模板：.claude/skills/journey-ra/template.html（骨架原样复制，只替换 {{PAGE_TITLE}} {{STAGES}} {{FOOTER_NOTE}} @@CUSTOM_JS@@）
输出：study/journey_<kebab>.html
```

子 Agent 只写 HTML，不跑校验——校验由步骤三完成。

## 步骤三：校验（确定性脚本）

```
python3 .claude/skills/journey-ra/check_journey.py <topic> [<topic> ...]
```

校验项：文件存在、无占位符/quiz/声音按钮、场景+站点 ≥8、站点 ≥4、细节卡 ≥12、开场 `id="s0"`、终章 `id="sLast"`、`id="again"` 已绑定、每区块有 data-c、**每条英文引文按其标注的 SESSION 出处逐字核验**、篇幅 ≥20 KB。

## 步骤四：修正轮

校验 exit 1 时逐条修复（引文不忠实 → 回源文件复制精确英文，截断用 ` … `；数量不足 → 补细节卡）。同一文件最多两轮修正，仍失败则报告用户。

## 步骤五：索引与交付

- 更新索引页 `study/journeys.html`（所有主题的入口，卡片式链接）。
- 报告：主题、文件路径、校验结果；单主题可 `open` 预览（先询问或按用户习惯）。

# 注意事项

- **跨集收网，宁精勿滥**：先用多组关键词 grep 全书，把该主题的核心讨论都摸清，再挑最值得停留的句子；细节卡标题要有画面感。
- **引文可机验**：引文与其标注的 SESSION 出处必须对应，脚本逐字核验。
- **中文一律自拟**，不照抄译文行（与译文解耦；译文修正不影响星旅）。
- **Ra 的拒答与限定也是内容**，如实收录。
- **重跑幂等**：整文件重写；固定 JS 不得改动（星空/氛围色/显影/轨道），定制交互写 `@@CUSTOM_JS@@`。
