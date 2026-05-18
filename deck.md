---
marp: true
theme: default
paginate: true
size: 16:9
footer: "MD2PPT · Markdown to Presentation"
style: |
  section {
    font-family: "Inter", "PingFang SC", "Microsoft YaHei", sans-serif;
    background: #0f172a;
    color: #e5e7eb;
    padding: 52px 64px;
  }
  h1 {
    font-size: 2.2em;
    letter-spacing: 0;
    margin: 0 0 20px;
  }
  h2 {
    font-size: 1.15em;
    color: #93c5fd;
    margin: 0 0 18px;
  }
  p, li {
    line-height: 1.55;
  }
  .lead {
    font-size: 1.1em;
    color: #cbd5e1;
  }
  .grid2 {
    display: table;
    width: 100%;
    table-layout: fixed;
    margin-top: 24px;
  }
  .grid2 > * {
    display: table-cell;
    width: 50%;
    vertical-align: top;
  }
  .grid2 > * + * {
    padding-left: 18px;
  }
  .grid3 {
    display: table;
    width: 100%;
    table-layout: fixed;
    margin-top: 24px;
  }
  .grid3 > * {
    display: table-cell;
    width: 33.33%;
    vertical-align: top;
  }
  .grid3 > * + * {
    padding-left: 16px;
  }
  .card {
    border: 1px solid rgba(147,197,253,0.35);
    background: rgba(30,41,59,0.78);
    border-radius: 8px;
    padding: 18px 20px;
    min-height: 130px;
    box-sizing: border-box;
  }
  .card h3 {
    margin: 0 0 10px;
    color: #7dd3fc;
  }
  .metric {
    display: block;
    font-size: 2.8em;
    line-height: 1;
    font-weight: 900;
    color: #38bdf8;
  }
  .muted {
    color: rgba(226,232,240,0.58);
    font-size: 0.86em;
  }
---

# Markdown 写 PPT

<p class="lead">用 Markdown 快速写内容，用稳定 CSS 控制版式，用 Marp 导出 HTML / PDF / PPTX。</p>

---

# 为什么用这套方案

<div class="grid3">
<div>
<div class="card">
<h3>快</h3>
从大纲到成稿都在 Markdown 里完成，适合频繁修改。
</div>
</div>
<div>
<div class="card">
<h3>稳</h3>
使用保守布局，减少 Preview 和导出之间的版式差异。
</div>
</div>
<div>
<div class="card">
<h3>可复用</h3>
同一套 CSS、组件和导出命令可以服务多个 PPT。
</div>
</div>
</div>

---

# 两列布局示例

<div class="grid2">
<div>
<div class="card">
<h3>写作建议</h3>

- 一页一个观点
- 短句优先
- 控制表格行数
</div>
</div>
<div>
<div class="card">
<h3>导出建议</h3>

- 先看 Preview
- 再导出 PDF
- 最后检查 PPTX
</div>
</div>
</div>

---

# 数字页示例

<div class="grid2">
<div>
<div class="card">
<span class="metric">80%</span>
<p>把重点数字单独成行，使用稳定字号和行高。</p>
</div>
</div>
<div>
<div class="card">
<span class="metric">3 min</span>
<p>数字和说明分层，导出到 PDF/PPTX 后更不容易错位。</p>
</div>
</div>
</div>

---

# 收尾页

## 谢谢观看

<p class="muted">MD2PPT · 2026</p>

