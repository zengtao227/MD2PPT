# MD2PPT

一套稳定的 Markdown 写 PPT 方案：用 Markdown 作为唯一源文件，在 VS Code 里实时预览，用 Marp CLI 导出 HTML、PDF 和 PPTX。

这个仓库的重点不是“把复杂 HTML 无损转 PPTX”，而是从一开始就用适合导出的 Markdown/CSS 写法，尽量保证 Preview、HTML、PDF、PPTX 之间不发生大的版式变形。

## 推荐工作流

1. 安装 VS Code 插件：`Marp for VS Code`
2. 复制或修改根目录的 `deck.md`
3. 在 VS Code 里打开 `deck.md`，使用 Marp Preview 实时检查
4. 导出文件：

```bash
npm install
npm run export:all
```

导出结果在 `outputs/`：

- `outputs/deck.html`
- `outputs/deck.pdf`
- `outputs/deck.pptx`

## 核心原则

- 只改 `.md`，不要手改导出的 HTML/PDF/PPTX。
- 每一页用 `---` 分隔，单页内容不要依赖浏览器滚动。
- 复杂布局优先使用 table-like CSS，不优先使用 CSS Grid/Flex。
- 尽量避免 `filter`、`backdrop-filter`、复杂 `box-shadow`、复杂透明叠加。
- 图片提前压缩并固定尺寸，避免导出时重新排版。
- PPTX 导出通常更适合提交和放映，不适合逐字编辑。

## 文档

- [专业可编辑 PPTX 主流程](docs/pptx-master-workflow.md)
- [PPTX 生成方案对比](docs/pptx-generation-schemes.md)
- [Open Design 集成说明](docs/workflow-with-open-design.md)
- [导出流程](docs/export-workflow.md)
- [Markdown 写作与排版规范](docs/markdown-writing-guide.md)
- [预览与导出一致性指南](docs/preview-export-consistency.md)
- [导出稳定性检查清单](docs/checklist.md)
- [UI/UX Pro Max 设计支持](docs/design-skill.md)

## 设计支持

仓库内置了 `skills/ui-ux-pro-max` 作为本地设计知识库。做路演、比赛答辩、项目方案类 PPT 前，先用它检索合适的产品类型、视觉风格、字体、配色和 UX 检查项，再进入 Markdown 或 PPTX 生成。

如果目标是专业、可编辑的 `.pptx`，优先按 [专业可编辑 PPTX 主流程](docs/pptx-master-workflow.md) 使用 Codex `Presentations` 插件。Marp 仍适合快速写作、预览、PDF 和放映版 PPTX；本地 `skills/pptx` + pptxgenjs 作为 Claude Code / 离线备用路径。

常用命令示例：

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "AI SaaS investor pitch" --design-system --format markdown --project-name "Demo Deck"
python3 skills/ui-ux-pro-max/scripts/search.py "professional education service" --domain product
python3 skills/ui-ux-pro-max/scripts/search.py "minimal professional editorial" --domain style
python3 skills/ui-ux-pro-max/scripts/search.py "professional modern" --domain typography
python3 skills/ui-ux-pro-max/scripts/search.py "Noto Sans SC Chinese presentation" --domain google-fonts
python3 skills/ui-ux-pro-max/scripts/search.py "service education" --domain color
python3 skills/ui-ux-pro-max/scripts/search.py "accessibility layout spacing contrast" --domain ux
```

## 适合场景

- 路演 PPT
- 比赛答辩
- 课程汇报
- 项目方案
- 需要快速迭代多个版本的演示稿

## 不适合场景

- 需要在 PowerPoint 里逐个编辑文本框和图形的商业模板
- 依赖大量动画、母版、SmartArt 的传统 PPT
- 复杂网页 HTML 直接无损转 PPTX

## 最重要的经验

不要把 Markdown PPT 当成网页来写。浏览器打开 HTML 属于显示模式渲染，CSS 支持最完整；Marp 导出 PDF/PPTX 会进入 Chromium 打印/截图相关链路，部分 CSS 在分页、缩放、`section` 容器里会出现差异。

为了让 Preview、PDF、PPTX 尽量一致，建议从一开始就采用“导出友好”的写法：

- 并排布局用 `display: table`，不要依赖复杂 Grid/Flex。
- 页面居中用固定 padding、`text-align`、稳定高度，不依赖 `section { display:flex }`。
- 时间线、三列卡片、截图并排都用 table-like 结构。
- logo 和图片统一加 `max-width`、`height:auto`、`object-fit:contain`。
- 少用透明叠加、filter、backdrop-filter、复杂阴影。

完整说明见 [预览与导出一致性指南](docs/preview-export-consistency.md)。
