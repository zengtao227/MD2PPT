# MD2PPT 项目上下文

## 项目定位

MD2PPT 是一个把主题、文章、知识文稿、书籍摘要或工程项目资料转成高质量演示文稿的工作流仓库。

当前首选目标不是“快速导出一份能放映的幻灯片”，而是生成：

- 内容逻辑清晰
- 设计语言统一
- 可在 PowerPoint 中继续编辑
- 有渲染预览和 QA 证据的 `.pptx`

同时，`deck-builder` 已把 HTML deck 纳入正式的 secondary 输出路径：当用户需要在线分享、网页演示或 presenter mode，而不是 PowerPoint 可编辑性时，可以路由到 HTML 演示方案。

## 主要术语

### Source Material

原始材料。可以是一个主题、一篇文章、一本书的章节、访谈稿、产品文档、代码仓库、工程项目说明、数据表或已有 PPTX。

### PPTX Slide Planner

从原始材料到 `deck.md` 之间的规划层。它不负责画幻灯片，也不直接生成 `.pptx`，而是输出每一页的演示蓝图：

- 这份 deck 给谁看
- 要推动什么决定或理解
- 整体 thesis 和叙事弧线
- 每页的 claim
- 每页的 proof object
- 每页适合的 layout family
- 需要的数据、截图、图表、架构图或引用
- 缺失信息和不可编造项

### deck.md

最终交给生成层的内容源。它应该包含 thesis、audience、slide list、claim、proof object、source 和 omission notes，不应该混入大量样式代码。

### Design Intelligence

由 `skills/ui-ux-pro-max` 生成的设计情报。新版优先使用 `--design-system` 聚合输出，再按需补查 `style`、`typography`、`google-fonts`、`color`、`chart`、`ux`。

### Visual Contract

由 `design-profiles/` 提供的视觉合同。它把 Open Design 风格落成可执行约束：颜色、字体、字号层级、版式语法、禁用项和页码/脚注规则。

### Codex Presentations

Codex 中生成专业可编辑 PPTX 的主路径。它应使用 artifact-tool `presentation-jsx`，并执行 claim spine、design system、contact-sheet plan、render QA、导出 PPTX。

### Fallback PPTX Path

本地 `skills/pptx` + pptxgenjs 路径。用于 Claude Code 或没有 Codex `Presentations` 能力时的备用方案。

## 当前推荐路径

```text
Source Material
    ↓
PPTX Slide Planner
    ↓
deck.md
    ↓
ui-ux-pro-max Design Intelligence
    ↓
design-profiles Visual Contract
    ↓
Codex Presentations
    ↓
render QA / contact sheet / layout JSON
    ↓
outputs/<deck-title>.pptx
```

如果目标是在线分享而非 PowerPoint 编辑，生成层可以改走 HTML 路由：

```text
deck.md
    ↓
design-profiles Visual Contract
    ↓
guizang-ppt-skill primary HTML / html-ppt-skill alternative HTML
    ↓
browser QA
    ↓
outputs/<deck-title>.html
```

## 当前研究记录

- `docs/deck-builder-review-and-external-research.md`：记录 `deck-builder` 首轮审查发现，以及对 `ppt-master`、`frontend-slides`、`guizang-ppt-skill`、`html-ppt-skill`、`beautiful-html-templates` 的外部方案分析和后续路线图。

## 常见输入模式

### 知识文稿 / 文章 / 书

核心任务是“提炼与重组”，不是逐段搬运。

优先提取：

- 中心论点
- 3 到 5 个关键观点
- 支撑观点的证据、案例、数据、引用
- 适合视觉化的结构：时间线、对比、框架、流程、分类、因果链
- 不适合放进主 deck 的细节，放入 appendix 或 notes

### 工程项目介绍

核心任务是“让听众快速理解项目价值和实现方式”。

优先提取：

- 项目要解决的问题
- 使用者或业务场景
- 系统边界和核心模块
- 架构图、数据流、工作流、接口关系
- 关键技术选择及原因
- 当前进展、效果指标、风险和下一步

## 沟通约定

- 默认用中文沟通。
- 优先用 `PPTX slide planner`、`deck.md`、`design intelligence`、`visual contract`、`Codex Presentations` 这些术语描述流程。
- 不把 Marp PPTX 称为可细编辑 PPTX；Marp 更适合快速写作、预览、PDF 和放映版输出。
- 不把 `ui-ux-pro-max` 或 Open Design 称为 PPTX 生成器；它们分别是设计情报和视觉合同来源。
