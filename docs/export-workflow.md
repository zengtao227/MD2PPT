# Marp 快速导出流程（轻量备用）

> 这不是 Presentation Director 的主工作流。主路径见 `docs/pptx-master-workflow.md`；只有在你明确选择 VS Code + Marp 快速草稿路由时，才使用本页流程。

## 1. 环境准备

如果你选择 Marp 这条轻量路由，需要安装 Node.js。然后在仓库根目录执行：

```bash
npm install
```

VS Code 推荐安装：

- `Marp for VS Code`

## 2. 实时预览

打开 `deck.md`，使用 VS Code 的 Marp Preview。

如果你走的是 Marp 快速路径，建议只以 Preview 作为排版基准，因为 PDF/PPTX 导出基本会沿用 Marp Preview 的渲染模型。

## 3. 导出全部格式

```bash
npm run export:all
```

`npm run export:all` 默认输出到仓库根目录的 `outputs/`。如果你是在 Presentation Director 的任务里交付，下面是建议的 Marp 目标路径示例：

```bash
npx marp deck.md --html --allow-local-files -o PPTX/<task-slug>/marp/deck.html
npx marp deck.md --pdf --allow-local-files -o PPTX/<task-slug>/marp/deck.pdf
npx marp deck.md --pptx --allow-local-files -o PPTX/<task-slug>/marp/deck.pptx
```

如果当前任务属于 Presentation Director，建议把 Marp 导出文件放进该项目的 `PPTX/<task-slug>/marp/`；个人草稿场景可以先留在 `outputs/`。

## 4. 检查导出结果

优先检查：

- PDF 页数是否正确
- PPTX 幻灯片数是否正确
- 关键页是否有文字溢出、遮挡、换行异常
- 深色背景、图片、logo 是否正常显示

macOS 上可以用：

```bash
pdfinfo PPTX/<task-slug>/marp/deck.pdf | grep Pages
```

## 5. 常见问题

### PPTX 里的文字不能单独编辑

这是正常现象。Marp 的 PPTX 导出更接近“每页视觉成品”，适合提交和放映；如果要完全可编辑，应该走 Codex `Presentations` 主路径或用 PowerPoint 原生方式重新制作。

### HTML 看起来对，PPTX/PDF 不对

通常是 CSS 使用了导出链路不稳定的能力，例如复杂 Grid/Flex、filter、透明叠加、动态高度。解决办法是改成更保守的固定布局。

### PDF 比 PPTX 更稳定

一般是的。最终提交如果允许 PDF，PDF 通常最接近预览效果。PPTX 可作为比赛要求的补充格式。
