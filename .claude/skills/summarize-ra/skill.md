---
name: summarize-ra
description: 把《一的法则》(The Ra Contact) 某一次集会（split/Ra_Session_XXX.md）的内容概括为层级列表式笔记 output/Ra_Session_XXX_summary.md。笔记全文只包含列表格式（无标题、无段落），第一条为概括整集的「全篇总括」，其下按本集问答脉络逐层展开。语言为现代白话（英文只作点缀），一级主题点明问题、优先讲组织公式，「器皿状态与例行问答」一两条带过。只读英文原文（脚本先剔除中文译段），与正文译文解耦。格式校验由确定性脚本完成，LLM 只做内容概括。当用户输入 /summarize-ra <编号...> 或要求"总结第 X-Y 集内容笔记"、"生成第 X-Y 集的层级概要"时触发。
---

# 角色与目标

你是《一的法则》内容总结 Agent。任务是为 `split/` 目录下的每一次集会（`Ra_Session_001.md` ~ `Ra_Session_106.md`）产出一份**层级列表式内容笔记**：

- 输出文件：`output/Ra_Session_XXX_summary.md`
- 全文**只包含列表格式**——没有标题（#）、没有普通段落，每个非空行都是一个列表项
- 第一条列表项为 `- **全篇总括**：…`，用一段话概括整集内容
- 其下按本集的问答脉络与逻辑推进逐层展开，形成层级列表

**只读英文原文，不读中文译文**——译文是同一流水线的下游产物且可能被修正，不携带独立信息（与 study-ra 同一原则）。

# 架构设计（重要）

**LLM 只做内容概括，不做格式校验。** 流水线：

```
prepare_reading.py（split 英中对照 → 剔除中文译段 → output/reading_Ra_Session_XXX_en.txt）→ [LLM] → output/Ra_Session_XXX_summary.md → verify_summary.py（格式校验）
```

- `prepare_reading.py`：从 `split/Ra_Session_XXX.md` 提取英文-only 紧凑文本（剔除含 CJK 字符的行）
- LLM：通读英文原文，直接写 `output/Ra_Session_XXX_summary.md`（格式要求见 `AGENT_INSTRUCTIONS.md`）
- `verify_summary.py`：校验「全文只有列表项」「首条为全篇总括」「层级缩进规整」，并打印条目统计

# 自动化执行工作流

## 步骤一：准备（确定性脚本）

```
python3 .claude/skills/summarize-ra/prepare_reading.py 5-12
```

生成 `output/reading_Ra_Session_XXX_en.txt`（LLM 的输入）。参数接受单集、区间（`A-B`）或列举。若该文件已存在，直接复用即可，不必重跑。

## 步骤二：LLM 生成 summary.md

### 小范围（≤5 集）：主代理直接处理

在一个 turn 内逐集处理：Read `output/reading_Ra_Session_XXX_en.txt` → Write `output/Ra_Session_XXX_summary.md` → 一行状态。不需要子代理。

### 大范围（≥6 集）：并行子 Agent

对每集派发一个子 Agent（`subagent_type: general-purpose`），**所有子 Agent 在同一轮消息中并行派发**。prompt 精简（指令在 AGENT_INSTRUCTIONS.md，子 Agent Read 一次命中缓存）：

```
读取 .claude/skills/summarize-ra/AGENT_INSTRUCTIONS.md 获取层级列表笔记生成指令，按其要求撰写。

输入文件：output/reading_Ra_Session_XXX_en.txt
输出文件：output/Ra_Session_XXX_summary.md
```

子 Agent 直接写 `output/Ra_Session_XXX_summary.md`，不自行校验——格式校验由脚本完成。

## 步骤三：校验（确定性脚本）

```
python3 .claude/skills/summarize-ra/verify_summary.py 5-12
```

- 校验：每个非空行都是列表项；首条为顶层 `- **全篇总括**：`；缩进按每层 2 空格规整递进；统计总条目数与层级数
- ⚠ 类警告（条目过少/一级主题过少/层级过深）不阻断；✗ 类错误（非列表行、缺总括条、缩进错乱、跳层）exit 1

## 步骤四：修正轮

`verify_summary.py` 报错（exit 1）时，按打印的错误行修改对应的 `output/Ra_Session_XXX_summary.md`：
- **「第 X 行不是列表项」** → 把该行并入上一条列表项，或改为子列表项；
- **「首条不是全篇总括」** → 在文件开头补写 `- **全篇总括**：…` 一句话概括；
- **「缩进错乱」/「跳层」** → 统一为每层 2 空格、逐层递进。

修完重跑校验。同一文件最多两轮修正，仍失败则报告用户，不要无限重试。

## 步骤五：清理

成功后删除临时文件 `output/reading_Ra_Session_XXX_en.txt`（若该文件是本 skill 为此轮新生成的；若其他流程还在用，则保留）。

# 注意事项

- **只读英文**：输入只有 `output/reading_Ra_Session_XXX_en.txt`，不读 `split/` 里的中文译段，也不读 `output/Ra_Session_XXX.md`。
- **白话优先**：条目默认现代白话，英文只作点缀；术语首现带英文原词与白话定义；一级主题点明问题；组织公式优先于平铺清单。详见 `AGENT_INSTRUCTIONS.md`。
- **问答脉络是主线**：一级主题 = 本集的议题块；「器皿状态与例行问答」一两条带过；Ra 的拒答/限定/反问要如实记录。
- **风格参考**：若 `study/Ra_Session_XXX_study.html` 存在，LLM 可参考其章节划分与口吻，但内容以英文原文为准。
- **重跑幂等**：`summary.md` 每次由 LLM 全量重写，不叠加。
- **条目数与层级**：由脚本打印统计，仅为参考信息；内容完整覆盖整集（从开场致意到 `Adonai` 收尾）比条目数更重要，脚本对条目数只警告不阻断。
- **与其他产物的关系**：`summary.md` 是独立笔记文件，不写入 `split/` 或 `output/Ra_Session_XXX.md`，不影响翻译/校对/导读/学习网页流水线；它是 mindmap-ra 的唯一输入。

# 交互反馈

- 启动时，简要确认要处理的集会范围。
- ≥6 集时告知将并行派发 N 个子 Agent。
- 处理中保持静默高效。
- 结束后输出简明报告：集数、每集条目数/一级主题数/层级数、校验结果（全部 ✓ / 有 ✗ 需修正）。
