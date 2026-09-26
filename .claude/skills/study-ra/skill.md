---
name: study-ra
description: 为《一的法则》(The Ra Contact) 某一次集会（split/Ra_Session_XXX.md 英中对照）生成单文件交互式学习网页 study/Ra_Session_XXX_study.html——按问答脉络分议题的学习路径、核心概念四件套（英文原句引用+自拟中译+一句话+比喻/案例）、丰富的生活案例、问答推进/术语卡/归类练习/条件模拟/历史时间轴等交互组件，例行问答收进折叠区。结构骨架与模板固定，仅内容随集会变化。无测验区。当用户输入 /study-ra <编号...> 或要求"生成第 X-Y 集的交互学习网页/学习模块"时触发。
---

# 角色与目标

为 `split/Ra_Session_XXX.md`（英中逐段对照，`## (N.Y)` 分块的问答实录）生成**交互式学习网页** `study/Ra_Session_XXX_study.html`：让对 Ra 资料不熟的中文读者，不逐句啃英文也能弄懂这一集 Ra 与发问者谈了什么、在体系中的位置、以及为什么重要。已完成样例：`study/Ra_Session_005_study.html`。

# 架构

**结构与交互骨架 100% 固定，只有内容变化。**

```
template.html（CSS + 固定 JS + HTML 外壳，占位符）
        │  原样复制，替换占位符
        ▼
study/Ra_Session_XXX_study.html
        │
        ▼
check_study.py（确定性校验：组件齐全、无占位符残留、案例数达标、英文引文逐字核验等）
```

- 骨架来源：`.claude/skills/study-ra/template.html`——CSS、进度条 JS、initStepper、initSorter **一字不改**。
- 内容规范：`.claude/skills/study-ra/AGENT_INSTRUCTIONS.md`——占位符表、章节划分（按问答脉络）、四件套、案例要求、交互组件选型、忠实性规则、自检清单。**写内容前必须先读它。**
- 校验：`.claude/skills/study-ra/check_study.py`。

# 工作流

## 步骤一：准备

```
mkdir -p study
```

## 步骤二：生成（LLM 全文通读 split/Ra_Session_XXX.md 后撰写）

### 小范围（≤5 集）：主代理直接处理

逐集处理：Read `split/Ra_Session_XXX.md` 全文 → Read `template.html` 与 `AGENT_INSTRUCTIONS.md` → Write `study/Ra_Session_XXX_study.html`。

### 大范围（≥6 集）：并行子 Agent

对每集派发一个子 Agent（`subagent_type: general-purpose`），**所有子 Agent 在同一轮消息中并行派发**。prompt：

```
读取 .claude/skills/study-ra/AGENT_INSTRUCTIONS.md 获取交互学习网页的内容撰写规范，严格按其要求执行。

输入：split/Ra_Session_XXX.md（通读全文，英文为准）
模板：.claude/skills/study-ra/template.html（骨架原样复制，替换占位符）
输出：study/Ra_Session_XXX_study.html
```

子 Agent 只写 HTML，不跑校验——校验由步骤三完成。

## 步骤三：校验（确定性脚本）

```
python3 .claude/skills/study-ra/check_study.py 5-12
python3 .claude/skills/study-ra/check_study.py 5 12 88
```

参数接受单集、区间（`A-B`）或列举。

校验项：文件存在、组件齐全（hero/path-box/toc/script/initStepper/initSorter/renderPath）、无占位符残留、无 quiz、导航锚点与 data-target 对应、章节数 4-8、案例 ≥ max(8, 2×章节数)、每章至少 1 条引文、**每条英文引文逐字核验为 split/ 英文文本的有序子串**、交互调用 ≥3 且含 initStepper、localStorage key 为 `ra{XXX}-study-progress`、篇幅 ≥18 KB。

## 步骤四：修正轮

校验 exit 1 时，按打印的错误逐条修复：
- 缺组件 → 检查是否遗漏模板区块；
- 案例不足 → 在对应章节补 `.case` 块（每章 ≥2）；
- **引文非原文子串** → 回到 `split/Ra_Session_XXX.md` 复制精确英文；句中截断处不要补句号，改用 `…` 收尾；
- 交互未初始化 → 在 `{{CUSTOM_JS}}` 位置补调用；
- 锚点不对应 → 核对 `id="sK"` 与 nav/data-target；
- 章节数越界 → 合并或拆分议题章节。

修完重跑 `check_study.py`。同一文件最多两轮修正，仍失败则报告用户（列出失败项），不要无限重试。

## 步骤五：交付

- 报告：集数、每集文件路径、校验结果。
- 单集时可 `open study/Ra_Session_XXX_study.html` 在浏览器中打开（先询问或按用户习惯）。

# 注意事项

- **忠实性**：所有义理以 `split/Ra_Session_XXX.md` 的**英文段落**为准，不引入本集没有的内容（不引用其他集会、不引用社区二手解读）。中文译段仅作理解辅助，**不得照抄进页面**——页面中文一律自拟，以便与将来可能修正的正文译文解耦。
- **引文可机验**：英文引文必须是原文精确子串，脚本会逐条核验（这是本 skill 与瑜伽版的主要差异点之一）。
- **比喻边界**：比喻只作理解辅助，映射必须准确；拿不准的义理直接用释义，不用比喻。
- **Ra 的拒答也是内容**：Ra 常以「我们不谈论 X」「这无关紧要」或反问作答，这些体现自由意志法则，要如实写入，不要为了讲完整而补 Ra 没说过的内容。
- **例行问答折叠**：器皿状态、个人/后勤问答收进开篇章节的 `details.dict`，一句话带过，不占正文章节。
- **无测验**：不产出任何 quiz/自测区；测试类交互只有嵌在章节内的「归类练习」(initSorter)。
- **重跑幂等**：整文件重写，不存在叠加问题；localStorage key 含集会编号，互不干扰。
