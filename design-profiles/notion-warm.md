---
profile: notion-warm
suitable_for:
  - Internal report or status update
  - Culture deck or team communication
  - Lightweight presentation or course handout
  - Casual brief where approachability matters
tone: approachable, clean, document-like, minimal
formality: low-medium
density: low
color_scheme: Warm white (ffffff) with soft warm surface (f6f5f4) — gentle, paper-like, no strong accent
avoid_for:
  - Investor pitches or competitive defense
  - High-stakes external presentations
  - Decks requiring a strong visual impact or brand statement
  - Engineering or data-heavy content (low density will feel sparse)
---

# Notion 暖白（Notion Warm Minimal）

> 来源：nexu-io/open-design · design-systems/notion
> 风格：温暖极简 / 纸张质感 / 亲和力强
> 适用：课程汇报、内部文档、通用演示、文化类内容

---

## 色板

| 角色 | 色值 | 用途 |
|------|------|------|
| bg | `ffffff` | 幻灯片主背景 |
| surface | `f6f5f4` | 卡片背景（暖白，略带黄棕）|
| fg | `000000f2` → `0d0d0d` | 主文字（近黑，非纯黑）|
| fg-warm | `31302e` | 深表面上的标题文字 |
| muted | `615d59` | 次要文字（暖灰）|
| meta | `a39e98` | 注释、占位文字 |
| accent | `0075de` | 链接、CTA、强调 |
| accent-dark | `213183` | 深色强调区域 |
| border | `1a` → `e6e6e6` | 分割线（rgba近似）|
| warm-dark | `31302e` | 深色背景块（用于封面/章节）|

**生成工具颜色参数**（去掉 # 号）：
- 背景：`ffffff`
- 主标题：`0d0d0d`
- 正文：`31302e`
- 次要文字：`615d59`
- 注释：`a39e98`
- Accent：`0075de`
- 卡片背景：`f6f5f4`
- 深色块背景：`31302e`（反白用 `ffffff`）

---

## 字体规范

| 角色 | 字体 |
|------|------|
| 主字体 | `Inter`（或系统字体）|
| 中文 | `Noto Sans SC` |
| 显示级标题 | Inter，负字间距 |

---

## 字号与层级

| 层级 | 尺寸 | 字重 | 特殊处理 |
|------|------|------|---------|
| 封面大字 | 48–60pt | 700 | charSpacing: -1 |
| 幻灯片标题 | 32–36pt | 600 | charSpacing: -0.5 |
| 正文 | 14–16pt | 400 | — |
| 标签 | 11pt | 500 | — |
| 数据大字 | 48pt+ | 700 | — |
| 注释 | 10–11pt | 400 | meta 色 |

---

## 设计风格

- **温暖感**：背景用 `f6f5f4` 暖白，不用纯白 `ffffff`（封面或强调页可用纯白）
- **边框轻盈**：1px `e6e6e6` 分割线，近乎隐形
- **阴影极克制**：小卡片可用极轻阴影（不超过 4% 透明度）
- **Accent 单点使用**：`0075de` 只用于关键 CTA 和链接文字
- **圆角**：`borderRadius: 4–8pt`（Notion 允许小圆角）

---

## JS token 快速参数模板

```javascript
const NOTION_WARM = {
  bg: "ffffff",
  surface: "f6f5f4",
  fg: "0d0d0d",
  fgWarm: "31302e",
  muted: "615d59",
  meta: "a39e98",
  accent: "0075de",
  darkBg: "31302e",
  border: "e6e6e6",
  fontDisplay: "Inter",
  fontBody: "Inter",
  fontChinese: "Noto Sans SC",
};
```
