# 预览与导出一致性指南

这份文档总结的是一个普适原则：如果最终目标是 PDF/PPTX，就不要只按“浏览器网页效果”来写 Markdown PPT。应该按 Marp Preview 和 Chromium 导出链路都稳定支持的方式来写。

## 为什么 Preview、HTML、PDF、PPTX 会不同

同一个 Markdown 文件可能经历几种渲染路径：

| 场景 | 渲染模式 | 特点 |
|:---|:---|:---|
| 浏览器直接打开 HTML | screen/display | CSS 支持最完整，很多网页布局都正常 |
| VS Code Marp Preview | Marp 预览容器 | 接近最终导出，但仍是编辑器预览 |
| Marp 导出 PDF | Chromium print pipeline | 会应用打印分页、缩放、`@media print` 相关逻辑 |
| Marp 导出 PPTX | Marp + Chromium/图片化页面 | 视觉接近 PDF，但可编辑性有限 |

最常见的问题不是 Markdown 内容错了，而是某些网页 CSS 在打印/导出模式下行为不同。

## 优先采用的稳定写法

### 1. 页面级居中

不要依赖：

```css
section.title {
  display: flex;
  align-items: center;
  justify-content: center;
}
```

更稳的写法：

```css
section.title {
  padding: 90px 72px 56px;
  text-align: center;
}
```

原因：`section` 是 Marp 的分页容器，在打印链路里再叠加 Flex 居中，容易出现缩放、垂直位置和内容高度判断差异。

### 2. 两列/三列布局

不要优先写：

```css
.grid2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}
```

推荐写：

```css
.grid2 {
  display: table;
  width: 100%;
  table-layout: fixed;
  border-collapse: collapse;
}
.grid2 > * {
  display: table-cell;
  width: 50%;
  vertical-align: top;
}
.grid2 > * + * {
  padding-left: 18px;
}
```

三列同理：

```css
.grid3 {
  display: table;
  width: 100%;
  table-layout: fixed;
}
.grid3 > * {
  display: table-cell;
  width: 33.33%;
  vertical-align: top;
}
.grid3 > * + * {
  padding-left: 16px;
}
```

### 3. 不等宽布局

如果某一列文字更长，不要强行三等分，可以显式设置列宽：

```css
.thanks-three {
  display: table;
  width: 100%;
  table-layout: fixed;
}
.thanks-three > *:first-child { width: 39%; }
.thanks-three > *:nth-child(2) { width: 30%; }
.thanks-three > *:nth-child(3) { width: 31%; }
```

这比临时调字号更稳，因为它先解决内容承载空间不足的问题。

### 4. 流程图和横向节点

不要用复杂 Flex 自动分布。推荐使用 inline-block 或 table。

```css
.flow-row {
  display: block;
  text-align: center;
  white-space: nowrap;
}
.flow-step {
  display: inline-block;
  width: 132px;
  vertical-align: middle;
}
.flow-arrow {
  display: inline-block;
  width: 28px;
  text-align: center;
}
```

如果节点很多，用表格结构更稳定。

### 5. 多图并排

三张截图并排时，不建议用 `display:flex`。用 table：

```html
<div class="grid3 image-row">
  <div><img src="assets/step1.png"></div>
  <div><img src="assets/step2.png"></div>
  <div><img src="assets/step3.png"></div>
</div>
```

```css
.image-row img {
  width: 100%;
  height: auto;
  max-height: 360px;
  object-fit: contain;
  display: block;
}
```

### 6. Logo 和图片

所有 logo 和图片都应该限制尺寸：

```html
<img src="assets/logo.png" class="logo">
```

```css
.logo {
  max-width: 150px;
  height: auto;
  display: inline-block;
}
```

避免只写 `height` 或只写 `width`，也避免用 `filter: drop-shadow(...)` 做关键视觉。

## 尽量少用的 CSS

这些 CSS 在普通浏览器里常常没问题，但在导出链路里更容易出差异：

- `display: grid`
- 页面主结构上的 `display: flex`
- `position: absolute` 大量定位
- `filter: drop-shadow(...)`
- `backdrop-filter`
- 复杂 `box-shadow`
- 大面积半透明叠加
- `vh` / `vw` 驱动字号
- 依赖内容自动撑高的长卡片

不是绝对不能用，而是不要把它们放在关键结构上。关键结构包括：整页居中、两列/三列布局、截图并排、页脚、封面 logo、流程图。

## 推荐的写作顺序

1. 先写纯 Markdown 内容，只确认每页讲什么。
2. 再把每页内容压缩到一屏内。
3. 最后加 CSS 布局，优先 table-like 结构。
4. 在 VS Code Marp Preview 中检查。
5. 导出 PDF/PPTX 检查关键页。
6. 如果导出变形，优先改布局结构，不优先调小字号。

## 常见问题与修改方案

| 问题 | 常见原因 | 推荐修改 |
|:---|:---|:---|
| Preview 对，PDF/PPTX 变形 | 使用了 Grid/Flex/复杂定位 | 改为 table-like 布局 |
| 封面 logo 丢失或阴影异常 | `filter` 或图片尺寸不固定 | 去掉 filter，设置 `max-width` 与 `height:auto` |
| 卡片高度不一致 | 内容长度不同且未固定最小高度 | 设置 `min-height`、列宽或删减文字 |
| 日期/标签不对齐 | 同一行元素自由流动 | 拆成 table-cell，给日期列固定宽度和 `text-align:right` |
| 长句频繁换行 | 列宽不足或字体过大 | 优先调整列宽，其次缩短文案 |
| 最后一页不正式 | 信息过多、emoji 过多 | 只保留标题、团队、成员、日期 |

## 适合复用的 CSS 模板

```css
.card {
  border: 1px solid rgba(147,197,253,0.35);
  background: rgba(30,41,59,0.78);
  border-radius: 8px;
  padding: 18px 20px;
  box-sizing: border-box;
}

.grid2,
.grid3 {
  display: table;
  width: 100%;
  table-layout: fixed;
}

.grid2 > *,
.grid3 > * {
  display: table-cell;
  vertical-align: top;
}

.grid2 > * { width: 50%; }
.grid3 > * { width: 33.33%; }

.grid2 > * + *,
.grid3 > * + * {
  padding-left: 16px;
}
```

这套写法不如现代网页 CSS 灵活，但它的优势是导出稳定，适合比赛、路演、汇报这种需要快速迭代和可靠提交的 PPT。

