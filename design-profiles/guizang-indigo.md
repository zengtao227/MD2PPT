---
profile: guizang-indigo
suitable_for:
  - Technical proposal or specification
  - Data report or analytics deck
  - AI / ML project introduction
  - Competition defense or thesis defense
  - Research presentation
tone: technical, research-oriented, data-driven, scholarly
formality: medium-high
density: high
color_scheme: Deep navy ink (0a1f3d) on cool paper (f1f3f5) — cold, academic, high-information density
avoid_for:
  - Warm narrative or editorial decks
  - Consumer-facing or brand content
  - Casual internal presentations
  - Decks where approachability is the primary goal
---

# 归藏靛蓝瓷（Guizang Indigo Porcelain）

> 来源：nexu-io/open-design · deck-guizang-editorial
> 风格：科技 / 研究 / 数据
> 适用：技术方案、数据报告、竞赛答辩、AI 产品介绍

---

## 色板（hex 值锁死，不许改动）

| 角色 | 色值 | 用途 |
|------|------|------|
| ink（主色）| `0a1f3d` | 深色背景、反白区域 |
| paper（底色）| `f1f3f5` | 幻灯片主背景 |
| paper-tint | `e4e8ec` | 卡片背景、次要区域 |
| ink-tint | `152a4a` | 深色辅助块 |

**生成工具颜色参数**（去掉 # 号）：
- 背景：`f1f3f5`
- 主标题文字：`0a1f3d`
- 正文文字：`152a4a`
- 次要文字：`4a6080`
- 深色 accent 块：`0a1f3d`（反白用 `f1f3f5` 文字）

---

## 字体规范

| 角色 | 字体（英文）| 字体（中文）|
|------|------------|------------|
| Display 标题 | `Playfair Display` | `Noto Serif SC` |
| Body 正文 | `Inter` | `Noto Sans SC` |
| 数据数字 | `Playfair Display Italic` | — |

---

## 字号与层级

| 层级 | 尺寸 | 字重 |
|------|------|------|
| Hero 封面大字 | 48–60pt | 700 |
| 幻灯片标题 | 32–40pt | 600 |
| kicker 章节标 | 11pt uppercase | 400 |
| 正文 | 14–16pt | 400 |
| 数据大字 | 48–64pt | 700 |
| 注释 | 10–11pt | 300 |

---

## 版式参考

| 版式 | 适用内容 |
|------|---------|
| L01 Hero Cover | 封面，深色背景反白 |
| L03 Big Numbers Grid | 技术指标、数据结果 |
| L06 Pipeline | 系统架构、工作流程 |
| L05 Image Grid | 截图、对比效果图 |
| L04 Quote + Image | 用户反馈、案例 |
| L02 Act Divider | 技术章节切换 |

---

## JS token 快速参数模板

```javascript
const INDIGO = {
  bg: "f1f3f5",
  ink: "0a1f3d",
  inkTint: "152a4a",
  paperTint: "e4e8ec",
  muted: "4a6080",
  fontDisplay: "Noto Serif SC",
  fontBody: "Noto Sans SC",
};
```
