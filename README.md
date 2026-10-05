# The Ra Contact ·《一的法则》中文翻译与学习项目

《一的法则》（The Law of One / The Ra Contact）是 L/L Research 记录的 Ra 群体传讯合集。坊间中文译本较为拗口，本项目借助 AI 工程化的思路，完成了全书 106 次集会（Session）的英文翻译，并在此基础上生成了导读、思维导图、交互式学习模块、沉浸式主题探索等一系列学习资料，全部开源免费，方便后来者阅读与学习。

## 成品下载

- [The_Ra_Contact.epub](./The_Ra_Contact.epub) — 全书 EPUB 电子书（导读 + 正文交替编排）
- [The_Ra_Contact.pdf](./The_Ra_Contact.pdf) — PDF 版本

## 项目地址

- GitHub: https://github.com/vilarsail/The-Ra-Contact
- Gitee: https://gitee.com/vilarsail/The-Ra-Contact

## 目录结构

```
The-Ra-Contact/
├── origin/
│   └── ra_en.txt              # 英文原文
├── split/                     # 106 次集会，英中对照正文（Ra_Session_001.md ~ 106）
├── output/                    # 译文产物与派生内容（每集 5 类文件 + 前言 0.md）
│   ├── 0.md                   # 前言
│   ├── Ra_Session_XXX.md      # 该集英中对照译文
│   ├── Ra_Session_XXX_review.md  # 审校报告（评估结论 + 问题清单）
│   ├── Ra_Session_XXX_fix.md     # 修复日志（采纳/拒绝的修正项）
│   ├── Ra_Session_XXX_guide.md   # 单章导读（核心议题 + 结构脉络）
│   └── Ra_Session_XXX_summary.md # 层级列表式内容笔记（供思维导图使用）
├── study/                     # 交互式学习产物（均为单文件、零依赖 HTML）
│   ├── Ra_Session_XXX_study.html    # 每集交互式学习模块
│   ├── Ra_Session_XXX_mindmap.html  # 每集思维导图（幕布风格，可折叠/缩放）
│   ├── journey_<主题>.html          # 主题沉浸式探索（密度、收割、极性、面纱、催化剂等 13 个主题）
│   ├── journeys.html                # 主题旅程索引页
│   └── Ra_Octave_Journey.html       # 八度音程之旅
├── do_translate.py            # 翻译回填脚本（将译文替换占位符）
├── translate_fix.py           # 残余占位符修复脚本（智能引号归一化匹配）
├── build_epub.sh              # 用 pandoc 打包 EPUB（前言 + 导读 + 正文交替）
└── The_Ra_Contact.epub / .pdf # 打包成品
```

## 学习资料说明

| 资料 | 内容 | 适合场景 |
|------|------|----------|
| 导读 (`_guide`) | 单章核心议题、结构脉络、背景梳理 | 阅读正文前的指引 |
| 笔记 (`_summary`) | 层级列表式概要，首条为全篇总括 | 快速回顾集会脉络 |
| 思维导图 | 幕布风格版式，支持节点折叠/展开、缩放、平移 | 可视化梳理全章结构 |
| 学习模块 | 按问答脉络分议题的学习路径、核心概念四件套（英文原句 + 中译 + 一句话 + 比喻）、生活案例与交互组件 | 系统学习单章内容 |
| 主题旅程 | 跨集会收网单一主题（密度、收割、极性、面纱、催化剂、疗愈、能量中心、流浪者、星际联邦、地球史、原型、死亡、造物、光线）的沉浸式滚动叙事 | 按主题深入理解 |

浏览器直接打开 `study/` 下的 HTML 文件即可使用，无需任何服务或依赖。

## 翻译与制作流程

1. **切分**：将英文原文（`origin/ra_en.txt`）按集会切分为 106 个文件；
2. **翻译**：逐段翻译，通过 `do_translate.py` / `translate_fix.py` 将译文回填到英中对照格式；
3. **审校**：用脚本校验原文、译文、内容对称、字符等问题，并对重点章节进行 AI 审校（`_review`）与修复（`_fix`）；
4. **派生**：基于译文生成导读、笔记、思维导图、学习模块与主题旅程；
5. **打包**：`./build_epub.sh` 按「前言 → 导读 001 → 正文 001 → …」顺序打包为 EPUB。

## 参与贡献

欢迎通过 MR / PR 参与校对或提出修改意见，也可直接邮件联系：[vilarsail@163.com](mailto:vilarsail@163.com)。

## 版权声明

原版英文书籍版权归原作者所有（L/L Research），本项目翻译内容及其他资料仅作为个人学习使用。

---

**版本：V1.0**
**整理人：君言**
**辅助 AI：Deepseek-v4 / GLM5.3**
