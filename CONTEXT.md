# Presentation Director 项目上下文

## 项目定位

Presentation Director 是一个把主题、文章、知识文稿、书籍摘要或工程项目资料转成高质量演示文稿的工作流仓库。仓库早期名为 MD2PPT；以后统一用 Presentation Director 指代这个项目和流程。

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

由 `design-locks/` 提供的视觉合同。它把 Open Design 风格落成可执行约束：颜色、字体、字号层级、版式语法、禁用项和页码/脚注规则。

### Codex Presentations

Codex 中生成专业可编辑 PPTX 的主路径。它应使用 artifact-tool `presentation-jsx`，并执行 claim spine、design system、contact-sheet plan、render QA、导出 PPTX。

### Presentation Director

Codex 环境下创建全新 PPTX 前的交互增强层。它不生成 PPTX，而是先用点击式 intake 收集听众、目标、资料边界、logo/品牌素材、AI 生图许可和输出限制，再通过 brief confirmation gate 让用户确认，之后才把确认后的 brief 交给 Codex Presentations。

Director 交互页应自动打开，不要让用户复制本地 URL。`serve` 默认打开 `intake`；用户点“下一步”后进入确认页。批处理或后台运行可显式传 `--no-open`。`style-review` 和 `compare` 可用 `presentation_director.py open-page` 或 `render --open-page ...` 打开。

对于 Codex 里的 net-new PPTX 请求，默认路径必须先走 Presentation Director，不应直接调用 Presentations 生成。只有以下情况可以跳过：

- 用户明确要求跳过 intake / director
- 已经存在用户确认过的 `brief-confirmed.json`
- 任务是现有 PPTX 的小改、QA 或 targeted edit

### PPTX Workspace

在任何项目中生成 PPT 时，用户可见的所有相关文件都应集中放到项目内 `PPTX/<task-slug>/`，不要散落在根目录、`assets/` 或多个临时目录里。推荐结构：

```text
PPTX/<task-slug>/
  brief/
  sources/
  intake.html
  brief-confirm.html
  brief-confirmed.json
  style-review.html
  revision-request.json
  compare.html
  final-selection.json
  v1/
    final.pptx
    slides/
      slide-001.png
      slide-002.png
    contact-sheet.png
    qa-summary.md
  v2/
    final.pptx
    slides/
    contact-sheet.png
    qa-summary.md
  final/
    <deck-title>.pptx
    <deck-title>.html
    final-report.md
```

Codex Presentations 插件内部可能仍按插件规则使用 `outputs/<thread-id>/presentations/...` 作为 scratch workspace；但交给用户看的 brief、版本、逐页预览图、contact sheet、QA 摘要、最终 PPTX 和最终 HTML 分享版必须复制或保存到 `PPTX/<task-slug>/`。

### Layout QA / No Overlap Gate

任何 PPTX 生成或 targeted edit 都必须通过渲染级排版检查，而不是只通过代码、XML 或包结构检查：

- 必须生成逐页预览图和 contact sheet，并把它们放入对应版本目录。
- 必须检查标题、副标题、正文、页脚、页码、图表标签、连接线和卡片之间是否互相重叠或裁切。
- 长标题必须预留换行高度；标题换行后不得压住副标题、小字说明或页面主体。
- 发现重叠后必须修复并重新渲染受影响页面；QA summary 中要写明修复前问题、修复动作和复检结果。
- 没有渲染证据和 no-overlap 检查结果时，不得把 PPTX 标记为完成。

### HTML Companion

最终 `.pptx` 的只读分享版。它由最终版本的逐页渲染图生成，保存为 `PPTX/<task-slug>/final/<deck-title>.html`，方便浏览器打开或简单分享。它不是编辑源，也不是 HTML deck 引擎的替代品；如果 PPTX 内容被修改，应从修改后的 PPTX 或重新渲染的逐页预览图再生成一次 HTML companion。

### PPTX Editability

最终 `.pptx` 是主要可编辑交付物。小改不需要重新生成整套 deck：文字替换、元素左右移动、颜色微调、替换图片、添加少量图片或图表，都应优先作为 PowerPoint 手工编辑或 Codex `Presentations` targeted-edit 处理。为了保留可回退历史，agent 修改现有 PPTX 时应复制成新版本，例如 `PPTX/<task-slug>/v2/final.pptx`，再重新生成 HTML companion。

如果某个元素被做成了截图或整页图片，它只能整体移动/裁剪，不能编辑内部文字、连接线或数据。需要可细编辑时，应要求 agent 把该页重建为原生文本框、形状、连接器、表格或图表。

### Fallback PPTX Path

本地 `skills/pptx` + pptxgenjs 路径。用于 Claude Code 或没有 Codex `Presentations` 能力时的备用方案。

## 当前推荐路径

```text
Source Material
    ↓
Presentation Director intake + brief confirmation (Codex net-new PPTX)
    ↓
Codex Presentations
    ↓
render QA / contact sheet / layout JSON
    ↓
style-review / optional revised versions
    ↓
final comparison and selection
    ↓
PPTX/<task-slug>/final/<deck-title>.pptx
PPTX/<task-slug>/final/<deck-title>.html
```

在 Codex 环境中，`deck.md`、`design-locks` 和 `ui-ux-pro-max` 都可以作为可选的中间资料或风格约束，但不再是全新 PPTX 第一版生成前的硬性步骤。第一版应优先让 Presentations plugin 根据 confirmed brief 自主完成内容组织、设计系统、contact sheet rhythm 和渲染 QA。

如果目标是在线分享而非 PowerPoint 编辑，生成层可以改走完整 HTML deck 路由。注意这不同于每个 PPTX 最终都会附带的只读 HTML companion；HTML deck 路由是把 HTML 作为主输出。

```text
deck.md
    ↓
design-locks Visual Contract
    ↓
available HTML deck engine
    (html-ppt-skill or guizang-ppt-skill, only when installed)
    ↓
browser QA
    ↓
PPTX/<task-slug>/final/<deck-title>.html
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
- 优先用 `Presentation Director`、`brief confirmation`、`Codex Presentations`、`style-review`、`deck.md`、`design intelligence`、`visual contract` 这些术语描述流程。
- 在 Codex 全新 PPTX 请求中，先走 Presentation Director；不要直接启动 Presentations，除非用户明确跳过或已有 confirmed brief。
- 不把 Marp PPTX 称为可细编辑 PPTX；Marp 更适合快速写作、预览、PDF 和放映版输出。
- 不把 `ui-ux-pro-max` 或 Open Design 称为 PPTX 生成器；它们分别是设计情报和视觉合同来源。
