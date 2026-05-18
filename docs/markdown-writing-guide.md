# Markdown 写作与排版规范

这份规范的目标是让 Markdown 在 VS Code Preview、HTML、PDF、PPTX 中尽量一致。

## 页面结构

每页保持一个明确主题：

```markdown
---

# 页面标题

一句核心观点

<div class="grid2">
...
</div>
```

建议每页最多：

- 1 个主标题
- 1 个副标题或解释句
- 1 个主视觉区
- 3 到 5 个信息块

## 布局规则

优先使用稳定布局：

```css
.grid2 {
  display: table;
  width: 100%;
  table-layout: fixed;
}
.grid2 > * {
  display: table-cell;
  width: 50%;
  vertical-align: top;
}
```

谨慎使用：

- `display: grid`
- 页面主结构上的 `display: flex`
- `position: absolute`
- `height: auto` 依赖内容撑开的复杂卡片

尽量不用：

- `filter: drop-shadow(...)`
- `backdrop-filter`
- 大面积半透明叠加
- 复杂 SVG filter
- 依赖浏览器滚动的长页面

判断标准很简单：如果这个 CSS 决定了页面主结构，就尽量使用保守写法；如果只是局部小标签、小按钮的装饰，可以适度使用现代 CSS。

## 字体与字号

建议固定字号，不用 `vw` 做响应式字号。

```css
h1 { font-size: 2.1em; }
h2 { font-size: 1.2em; }
.card { font-size: 0.9em; }
```

不要让一页里出现太多字号层级。常用层级：

- 主标题
- 小标题
- 正文
- 注释
- 数字强调

## 卡片设计

卡片适合表达并列信息，不适合层层嵌套。

推荐：

```html
<div class="card card-blue">
  <h3>关键结论</h3>
  <p>一句话说明。</p>
</div>
```

不推荐：

```html
<div class="card">
  <div class="card">
    嵌套卡片容易让边距和高度失控
  </div>
</div>
```

## 表格

表格是 Marp 导出里相对稳定的结构，适合：

- 对比
- 清单
- 时间线
- 参数说明

建议给表格指定固定列宽：

```css
.compare-table table {
  table-layout: fixed;
  width: 100%;
}
.compare-table th:first-child,
.compare-table td:first-child {
  width: 45%;
}
```

## 图片

图片建议放在 `assets/`，并固定尺寸：

```html
<img src="assets/demo.png" class="screen-shot">
```

```css
.screen-shot {
  width: 100%;
  max-height: 360px;
  object-fit: contain;
}
```

Logo 建议额外限制：

```css
.logo {
  max-width: 150px;
  height: auto;
  display: inline-block;
}
```

不要依赖 `filter: drop-shadow(...)` 做 logo 关键效果，导出时可能和浏览器显示不一致。

## 内容长度

每页先写结论，再补证据。导出稳定性最高的写法是短句、短行、少层级。

经验值：

- 标题不超过 18 个汉字
- 卡片正文每行不超过 18 到 22 个汉字
- 单页列表不超过 5 条
- 单张表格不超过 6 行

## 多版本管理

建议保留多个入口文件：

```text
deck-main.md
deck-short.md
deck-chatflow.md
```

共用同一套 CSS 和 assets。这样可以快速导出多个版本，且视觉风格一致。

## 导出变形时怎么修

优先级如下：

1. 先检查是否使用了 Grid/Flex 做主布局。
2. 把主布局改成 table-like 结构。
3. 给日期、标签、数字列固定宽度。
4. 给卡片设置 `min-height` 和 `box-sizing:border-box`。
5. 缩短文案或调整列宽。
6. 最后才考虑缩小字号。

不要一上来调很多字号。字号变小只会暂时塞下内容，但根因通常是布局不稳定或承载空间不足。
