---
name: mindmap-ra
description: 把已生成的层级列表笔记 output/Ra_Session_XXX_summary.md 转成单文件思维导图 study/Ra_Session_XXX_mindmap.html——幕布风格版式（无框文字节点、肘形灰线、加粗小标题富文本、胶囊根节点），零依赖 SVG，支持节点折叠/展开、双指滚动平移、捏合缩放、拖拽平移、复位按钮。当用户输入 /mindmap-ra <编号...> 或要求"把第 X-Y 集笔记转成思维导图"、"生成第 X-Y 集思维导图"时触发。
---

# 角色与目标

把 `output/Ra_Session_XXX_summary.md`（summarize-ra 产出的层级列表笔记）转换为**单文件零依赖思维导图** `study/Ra_Session_XXX_mindmap.html`。纯确定性转换，**不需要 LLM 参与内容生成**。

# 架构

```
output/Ra_Session_XXX_summary.md（层级列表笔记，唯一输入）
        │
        ▼
build_mindmap.py（确定性转换：解析列表 → 计算布局 → 渲染 SVG HTML）
        │
        ▼
study/Ra_Session_XXX_mindmap.html
```

- 版式：幕布（mubu）风格——节点为无框纯文字，仅根节点为朱红胶囊（白色文字）；层级靠细灰肘形连接线；`**加粗小标题**：说明` 渲染为深墨加粗+灰色正文；子节点跟随父节点宽度阶梯推进。
- 交互：单击节点折叠/展开（折叠显示子节点数徽章）、双指滚动平移、捏合缩放（Chrome ctrlKey+wheel / Safari gesture 事件均兼容）、拖拽平移、顶栏「复位」按钮、打开自动适配视图。
- 列表缩进 2 空格 = 一层；根节点标题取自 `split/Ra_Session_XXX.md` 的 `# § Ra Session_XXX` 行；其下第一层固定为「全篇总括」条目（由 summarize-ra 的格式保证）。

# 工作流

1. 前置检查：确认 `output/Ra_Session_XXX_summary.md` 存在；不存在则提示先运行 `/summarize-ra`，经用户同意后先执行总结流程。
2. 转换：
   ```
   python3 .claude/skills/mindmap-ra/build_mindmap.py 5 12 88
   ```
   参数接受单集、区间（`A-B`）或列举。
3. 交付：脚本打印每集节点数与画布尺寸；✗ 表示对应 summary.md 缺失或无法解析。单集时可 `open study/Ra_Session_XXX_mindmap.html` 预览（先询问或按用户习惯）。

# 注意事项

- **零依赖**：HTML 不引用任何外部资源，可离线打开、直接分享。
- **重跑幂等**：每次全量重写，重复运行不叠加。
- **样式调整集中在脚本顶部常量**：`FONT`（字号）、`LINE_H`（行高）、`MAX_CHARS`（普通节点每行字符数）、`H_GAP`/`V_GAP`（间距）、颜色常量（INK/BODY/LINE_C/ACCENT）。改后重跑脚本即可。
- **不改动输入**：脚本只读 `output/Ra_Session_XXX_summary.md`，不写回。
- 与 study-ra 的产物同放 `study/` 目录，文件名 `Ra_Session_XXX_mindmap.html` 不冲突。

# 交互反馈

- 转换完成后报告：集数、每集节点数、输出路径。
- 批量时保持静默高效，结束给一行汇总即可。
