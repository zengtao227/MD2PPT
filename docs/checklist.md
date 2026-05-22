# 导出稳定性检查清单

写完或改完 Markdown 后，按这个顺序检查。

## 预览检查

- VS Code Marp Preview 每页都没有滚动条
- 标题没有压到 logo 或页脚
- 卡片里的长词没有溢出
- 表格没有被挤出页面
- 图片没有变形或遮挡文字

## CSS 检查

- 并列布局优先用 table-like CSS
- 没有大面积使用 Grid/Flex
- `section.title`、`section.chapter`、`section.ending` 不依赖 Flex 居中
- 流程图、三图并排、版本时间线使用稳定列宽
- 没有依赖 `filter: drop-shadow(...)`
- 没有使用复杂 `backdrop-filter`
- 关键数字、按钮、标签都有固定尺寸或稳定行高
- logo 有 `max-width` 和 `height:auto`

## 导出检查

```bash
npm run export:all
```

然后确认：

- HTML 能打开
- PDF 页数正确
- PPTX 幻灯片数正确
- 关键页视觉和 Preview 基本一致

## 提交前检查

建议只提交：

- Markdown 源文件
- 文档
- assets
- package.json

不建议提交：

- `PPTX/`
- 临时截图
- 本地缓存
