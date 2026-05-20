---
profile: swiss-klein-blue
suitable_for:
  - Business plan
  - Product roadmap
  - Competition defense
  - Execution report
  - Investor pitch
tone: authoritative, precise, professional
formality: high
density: medium
color_scheme: Klein Blue accent (002FA7) on warm white (fafaf8) — high contrast, two-color minimal palette
avoid_for:
  - Culture decks or casual internal reports
  - Warm editorial / narrative presentations
  - Decks where the brand color is not blue
---

# 瑞士国际主义 · Klein Blue（Swiss International IKB）

> 来源：nexu-io/open-design · deck-swiss-international
> 风格：商业 / AI / 设计 / 产品分析
> 适用：商业计划、产品路线图、方案分析、执行报告

---

## 色板（hex 值锁死，不许改动）

| 角色 | 色值 | 用途 |
|------|------|------|
| accent（主强调色）| `002FA7` | CTA 块、关键数字、封面背景 |
| paper（底色）| `fafaf8` | 幻灯片主背景 |
| ink（文字色）| `0a0a0a` | 所有正文文字 |
| white | `ffffff` | accent 块上的反白文字 |
| gray-light | `f0f0ee` | 卡片背景、次要区域 |
| gray-mid | `6b6b6b` | 次要文字、注释 |

**生成工具颜色参数**（去掉 # 号）：
- 背景：`fafaf8`
- 主标题文字：`0a0a0a`
- 正文文字：`1a1a1a`
- 次要文字：`6b6b6b`
- Accent 块背景：`002FA7`（文字用 `ffffff`）
- 卡片背景：`f0f0ee`

---

## 字体规范

| 角色 | 字体（英文）| 字体（中文）|
|------|------------|------------|
| Display 标题 | `Inter Tight` | `Noto Sans SC` |
| Body 正文 | `Inter` | `Noto Sans SC` |
| 数据 / 编号 | `JetBrains Mono` | `Noto Sans SC` |

**关键**：严禁衬线字体、严禁装饰字体，全程无衬线。

---

## 字号与层级

| 层级 | 尺寸 | 字重 | 特殊处理 |
|------|------|------|---------|
| Cover 超大字 | 54–64pt | 700 | charSpacing: -1，全大写可选 |
| 幻灯片标题 | 32–40pt | 600 | — |
| 章节 kicker | 11pt | 400 | uppercase，charSpacing: 2 |
| 正文 | 14–16pt | 400 | — |
| 数据大字 | 48–60pt | 700 | JetBrains Mono |
| 注释 / 标签 | 10–11pt | 400 | uppercase，gray-mid 色 |

---

## 22 种版式参考（对应可编辑 PPTX 布局）

| 编号 | 版式名 | 适用内容 |
|------|--------|---------|
| S01 | Cover | 封面：全屏 accent 背景 + 反白大字 |
| S02 | Vertical Timeline | 左侧时间轴 + 右侧节点 |
| S03 | Statement | 超大居中宣言字 |
| S04 | Six Cells | 2×3 网格，图标+编号+描述 |
| S05 | Three Sub-cards | 左 hero + 右 3 张横向卡 |
| S06 | KPI Tower | 4 列变高柱状 + 数字 |
| S07 | H-Bar Chart | 水平排名横条图 |
| S08 | Duo Compare | 左 Before / 右 After |
| S09 | Closing Manifesto | 左 accent 块 + 右白底要点 |
| S11 | Horizontal Timeline | 顶部 headline + 中部时间轴 |
| S13 | Three Forces Cards | 左 ink hero + 右 3 卡 |
| S18 | Why Now | 3 列分析，末列 accent 高亮 |
| S19 | Four Cards | 4 张等宽卡 |
| S20 | Stacked KPI Ledger | 垂直行，大数字+标签 |

---

## 设计铁律

- **只用直角**：全程 `borderRadius: 0`
- **1px 细线分割**，accent 色或 ink 色，严禁阴影 / 渐变
- **16 列网格意识**：内容区域要有对齐感
- **极端字号反差**：cover 用 54pt+，body 14–16pt
- 角标固定：`№N / N` 右下，topic 标签左下

---

## JS token 快速参数模板

```javascript
const SWISS_IKB = {
  bg: "fafaf8",
  accent: "002FA7",
  ink: "0a0a0a",
  white: "ffffff",
  grayLight: "f0f0ee",
  grayMid: "6b6b6b",
  fontDisplay: "Noto Sans SC",  // 或 Inter Tight（英文）
  fontBody: "Noto Sans SC",     // 或 Inter（英文）
  fontMono: "JetBrains Mono",
};
```
