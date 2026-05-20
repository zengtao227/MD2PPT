# 后续开发路线图

> 来源：竞品分析（pi.inc / pi.deepvinci.tech）+ 实际使用痛点
> 状态：规划中，按优先级排列

---

## 优先级 1：立即可加入工作流

### ~~1.1 多输入方式~~ — N/A，已被模型原生能力覆盖

**结论（2026-05-20）：** Claude 和 Codex 原生就能读取 URL（WebFetch）、处理粘贴文本、解析 PDF/Word。用户直接把原始材料提供给模型，说"帮我做一个 PPT"，模型会自动提炼并进入 deck-builder 流程，不需要专门实现输入解析层。

删除此条。无需开发。

---

### 1.2 先出大纲供确认，再生成完整 PPTX

**来源：** pi.inc 在生成前让用户看到并确认结构（页数 + 主标题），避免生成 20 页后发现结构不对。

**现状：** 当前 Prompt 直接生成完整 PPTX，如果叙事结构不对就要大改。

**改进方案：**
在 Codex Prompt 里分两步执行：

```text
Step 1（你批准前不继续）：
生成 claim spine，格式：
  01 / 封面：<一句话 claim>
  02 / 问题：<一句话 claim>
  03 / 解决方案：<一句话 claim>
  ...
列出页数、每页主张、建议版式，等待确认。

Step 2（你确认后执行）：
按确认后的 claim spine，执行完整 PPTX 生成流程。
```

**实现成本：** 低。加入 Prompt 模板即可。

---

### 1.3 长图导出 —— 适合社交媒体 / 微信分享

**来源：** pi.inc 和 DeepVinci 都支持将完整演示导出为一张竖版长图，便于微信、LinkedIn 等平台分享，接收方不需要打开 PPT 文件。

**现状：** md2ppt 只支持 PPTX / PDF / HTML 输出。

**改进方案：**
在 PPTX 导出后，追加一步长图合成：

```bash
# 将 PPTX 每页转为 PNG，再纵向拼接
python3 scripts/export-longimage.py outputs/deck.pptx outputs/deck-longimage.png
```

依赖：LibreOffice（PPTX → PDF）、Poppler（PDF → PNG）、Pillow（拼接）。

实现细节见：`scripts/export-longimage.py`（待开发）。

---

## 优先级 2：中期改进

### 2.1 AI 背景图生成（可选步骤）

**场景：** 当现有 design-profile 的纯色方案不够视觉冲击力时，可以为封面和章节分隔页生成独一无二的 AI 背景图。

**详见：** `docs/ai-background-image.md`

---

### 2.2 从个人笔记 / Obsidian / Notion 直接生成 deck.md

**场景：** 笔记库里已有大量内容，想快速把某个主题的笔记整理成演示稿。

**实现方向：**
- 指定笔记文件夹或 URL，Claude 提炼 claim spine
- 与 1.1（多输入方式）共用同一个提炼 Prompt

---

### 2.3 品牌模板档案

**场景：** 有固定的企业/个人品牌色，每次不需要选 design-profile，直接用品牌模板。

**实现：** 新建 `design-profiles/<brand-name>.md`，把品牌色写死，视为专属 profile 使用。

---

## 优先级 3：长期探索

### 3.1 查看数据分析

**来源：** DeepVinci 支持分享链接后查看每页被阅读的时长和次数。

**实现方向：** 导出为 HTML 部署后，接入 Plausible 或类似轻量统计。

### 3.2 多人协作

**场景：** 两人以上共同编辑同一份 deck。  
**现实建议：** 用 Google Slides 协作流程（见 `docs/pptx-generation-schemes.md`），不需要在本项目里另行实现。

---

## 不打算实现的功能

| 功能 | 原因 |
|------|------|
| 自动设计系统（AI 随意选主题）| 你需要精确控制设计语言，这是 md2ppt 的核心优势，不应该交给 AI 随机决定 |
| 内置 GUI 编辑器 | VS Code + PowerPoint 已经够用，不需要重复造轮子 |
| 所有页面都生成背景图 | 内容页有背景图时文字可读性差，只封面+章节页适合 |
