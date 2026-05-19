# Linear 深色（Linear Dark）

> 来源：nexu-io/open-design · design-systems/linear-app
> 风格：极简暗色 / 精准工程感 / 科技产品
> 适用：SaaS 产品介绍、技术路线图、投资人 deck

---

## 色板

| 角色 | 色值 | 用途 |
|------|------|------|
| bg-deep | `08090a` | 主背景（近纯黑，略带冷调）|
| bg-panel | `0f1011` | 卡片/面板背景 |
| bg-elevated | `191a1b` | 高亮卡片 |
| bg-secondary | `28282c` | hover 状态、浅层背景 |
| text-primary | `f7f8f8` | 主文字（近白，略暖）|
| text-secondary | `d0d6e0` | 正文、描述 |
| text-muted | `8a8f98` | 次要信息、metadata |
| text-faint | `62666d` | 时间戳、禁用态 |
| accent | `7170ff` | 交互元素、链接、强调 |
| accent-bg | `5e6ad2` | CTA 按钮背景 |
| border | `23252a` | 主分割线 |
| border-subtle | `rgba(255,255,255,0.05)` → `1a1b1d` | 超细分割线近似 |
| success | `27a644` | 状态指示 |

**pptxgenjs 颜色参数**（去掉 # 号）：
- 幻灯片背景：`08090a`
- 主标题：`f7f8f8`
- 正文：`d0d6e0`
- 次要文字：`8a8f98`
- Accent 高亮：`7170ff`
- 卡片背景：`0f1011` 或 `191a1b`
- 分割线：`23252a`

---

## 字体规范

| 角色 | 字体 |
|------|------|
| 主字体 | `Inter` |
| 数字 / 代码 | `Berkeley Mono`（备选 `JetBrains Mono`）|
| 中文 | `Noto Sans SC` |

---

## 字号与层级

| 层级 | 尺寸 | 字重 | 特殊处理 |
|------|------|------|---------|
| Display 超大 | 48–60pt | 510（介于 400-500） | charSpacing: -1 |
| 幻灯片标题 | 32–40pt | 600 | charSpacing: -0.5 |
| 正文 | 14–16pt | 400 | — |
| 标签 / kicker | 11pt | 400 | uppercase |
| 数据大字 | 48pt+ | 700 | 用 Berkeley Mono |
| 注释 | 10–11pt | 300 | text-muted 色 |

---

## 布局风格

- **深色 sandwich**：封面全黑背景+反白，内容页卡片用 bg-panel
- **卡片用微透明边框**：`23252a` 1px 实线
- **强调色克制使用**：accent 只用于关键数字、CTA、选中态
- **无装饰**：无渐变、无阴影、无圆角（或极小圆角 2–4pt）

---

## pptxgenjs 快速参数模板

```javascript
const LINEAR_DARK = {
  bg: "08090a",
  bgPanel: "0f1011",
  bgElevated: "191a1b",
  textPrimary: "f7f8f8",
  textSecondary: "d0d6e0",
  textMuted: "8a8f98",
  accent: "7170ff",
  accentBg: "5e6ad2",
  border: "23252a",
  fontDisplay: "Inter",
  fontBody: "Inter",
  fontMono: "JetBrains Mono",
  fontChinese: "Noto Sans SC",
};
```
