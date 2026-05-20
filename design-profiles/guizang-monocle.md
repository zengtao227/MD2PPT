---
profile: guizang-monocle
suitable_for:
  - Business pitch or roadshow
  - Course presentation or academic defense
  - Opinion-driven or argument-led deck
  - Project proposal with narrative arc
  - Mixed technical + business audience
tone: narrative, editorial, warm-intellectual
formality: medium
density: medium
color_scheme: Near-black ink (0a0a0b) on warm paper (f1efea) — editorial warmth, strong text-on-paper contrast
avoid_for:
  - Pure engineering or data-heavy decks (use guizang-indigo instead)
  - Dark-mode preference audiences
  - Decks requiring a strong brand accent color
---

# 归藏墨水经典（Guizang Monocle）

> 来源：nexu-io/open-design · deck-guizang-editorial
> 风格：叙事 / 观点 / 通用商业 / 科技
> 适用：路演、比赛答辩、项目方案、课程汇报

---

## 色板（hex 值锁死，不许改动）

| 角色 | 色值 | 用途 |
|------|------|------|
| ink（主色）| `0a0a0b` | 背景、深色块、反白区域 |
| paper（底色）| `f1efea` | 幻灯片主背景 |
| paper-tint（辅助底色）| `e8e5de` | 卡片背景、次要区域 |
| ink-tint（深辅色）| `18181a` | 深色辅助块 |

**生成工具颜色参数**（去掉 # 号）：
- 背景：`f1efea`
- 主标题文字：`0a0a0b`
- 正文文字：`18181a`
- 次要文字：`4a4a4b`（墨水 60% 透明度近似）
- 深色 accent 块：`0a0a0b`（反白用 `f1efea` 文字）

---

## 字体规范

| 角色 | 字体（英文）| 字体（中文）| 备注 |
|------|------------|------------|------|
| Display 标题 | `Playfair Display` | `Noto Serif SC` | 衬线，叙事感 |
| Body 正文 | `Inter` | `Noto Sans SC` | 无衬线，清晰 |
| 数字 / 编号 | `Playfair Display Italic` | — | 斜体衬线数字 |

**fontFace 建议**：
- 标题（中文内容）：`"Noto Serif SC"`，英文内容：`"Playfair Display"`
- 正文：`"Noto Sans SC"` / `"Inter"`

---

## 字号与层级

| 层级 | 尺寸 | 字重 | 间距 |
|------|------|------|------|
| Hero 封面大字 | 48–60pt | 700 | charSpacing: -1 |
| 幻灯片标题 | 32–40pt | 600 | charSpacing: 0 |
| 章节小标题（kicker）| 11pt | 400 | charSpacing: 2（uppercase） |
| 正文 | 14–16pt | 400 | 默认 |
| 数据大字 | 48–64pt | 700 | italic 衬线 |
| 注释 / 脚注 | 10–11pt | 300 | 淡色 |

---

## 版式参考（对应可编辑 PPTX 布局）

| 版式 | 描述 | 适用内容 |
|------|------|---------|
| L01 Hero Cover | 居中大字 + 副标题 + 底部元数据 | 封面 |
| L02 Act Divider | 巨大 headline + 一句引言，可反色 | 章节切换 |
| L03 Big Numbers Grid | 3×2 数据卡（标签/大数字/注释）| 数据展示 |
| L04 Quote + Image | 左文右图，基线对齐 | 案例/引言 |
| L06 Pipeline | 横向编号步骤 | 流程/方法论 |
| L08 Big Quote | 巨大衬线引文 + 署名 | 金句/观点 |
| L09 Before / After | 左旧右新对比，左侧 55% 透明 | 对比分析 |

---

## 设计铁律（不许违反）

- **禁止**：渐变、drop-shadow、圆角、blur、emoji 装饰
- **只用直角**：`borderRadius: 0`，所有形状全直角
- **分页编号**：右下角 `01 / N` 格式
- **细分割线**：1px hairline，用 ink 色，不用粗线
- **图片**：不能用外部 URL，用纯色块或内联形状代替
- **数据**：严禁编造，所有数字来自用户输入

---

## JS token 快速参数模板

```javascript
// 封面页
const MONOCLE = {
  bg: "f1efea",
  ink: "0a0a0b",
  inkTint: "18181a",
  paperTint: "e8e5de",
  muted: "6b6b6c",
  fontDisplay: "Noto Serif SC",  // 或 Playfair Display（英文）
  fontBody: "Noto Sans SC",      // 或 Inter（英文）
};
```
