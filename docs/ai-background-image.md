# AI 背景图生成（可选步骤）

> 在工作流的「选定设计档案」之后、「生成 PPTX」之前，可选择性地为封面和章节分隔页生成 AI 背景图。
> 如果现有 design-profile 的纯色/色块方案已经足够，跳过本步骤即可。

---

## 适用场景

| 情况 | 建议 |
|------|------|
| design-profile 纯色方案已经足够 | **跳过**，直接生成 PPTX |
| 想要更强的视觉冲击力（路演封面、大赛答辩）| **使用**，生成封面背景图 |
| 需要独一无二的品牌感 | **使用**，生成与内容主题相关的抽象背景 |

---

## 只用于哪些页面

**适合使用背景图：**
- 封面（Cover）
- 章节切换页（Section Divider / Act Divider）

**不适合使用背景图：**
- 内容页（文字/图表/数据）：背景图会降低文字可读性
- 数据大字页（背景干扰数字识别）

---

## 图片类型选择

不要生成写实场景图（风景、人物、建筑），要生成**抽象纹理 / 几何光影**：

| 推荐方向 | 不推荐 |
|---------|-------|
| 抽象几何纹理 | 写实城市图 |
| 颜色渐变光晕 | 人物照片 |
| 纸张/麻布/大理石质感 | 卡通插图 |
| 极简线条构成 | 花卉、动物 |

抽象图像的优势：
- 不和文字抢视觉
- 与 design-profile 颜色系统保持一致
- 加半透明遮罩后文字对比度有保障
- 每次都能生成独一无二的版本

---

## Prompt 构造规则

根据 design-profile 自动构造图片 Prompt：

```text
Abstract [主色调描述] textured background,
[design-profile 风格关键词],
minimal, no text, no people, no faces,
suitable for presentation slide cover,
high resolution, 1920x1080
```

### 各档案对应的 Prompt 模板

**swiss-klein-blue（瑞士国际主义）**
```
Abstract deep blue geometric texture, Swiss modernist grid lines,
Klein Blue tones (#002FA7), minimal construction, no text, no people,
1920x1080 presentation cover background
```

**linear-dark（工程暗色）**
```
Abstract dark background with subtle purple grid lines,
engineering precision aesthetic, near-black (#08090a) with indigo accent,
minimal circuit-like geometry, no text, no people,
1920x1080 presentation cover background
```

**guizang-monocle（墨水经典）**
```
Warm paper texture with subtle ink wash elements,
editorial minimal, off-white (#f1efea) and ink tones,
no text, no people, soft grain texture,
1920x1080 presentation cover background
```

**guizang-indigo（靛蓝瓷）**
```
Abstract indigo porcelain texture, cool tech aesthetic,
deep blue (#0a1f3d) with subtle cerulean highlights,
minimal, no text, no people,
1920x1080 presentation cover background
```

**notion-warm（暖白极简）**
```
Warm minimal abstract background, soft cream and warm grey tones,
paper texture, gentle geometric elements,
no text, no people, clean and airy,
1920x1080 presentation cover background
```

---

## 图片生成 API 选项

| API | 质量 | 费用 | 适合 |
|-----|------|------|------|
| **DALL-E 3**（OpenAI）| ★★★★ | ~$0.04/张（1024×1024） | 你已有 API Key，推荐优先使用 |
| **Flux.1**（fal.ai）| ★★★★★ | ~$0.003–0.01/张 | 质量更高、更便宜，需注册 fal.ai |
| **Stable Diffusion**（Stability AI）| ★★★ | 有免费额度 | 最可控，适合反复测试 |

**推荐：DALL-E 3**，因为你已有 OpenAI API Key，零额外配置。

---

## 在工作流中的位置

```text
[4] 设计情报
    用 ui-ux-pro-max 查行业、风格、字体、配色
        ↓
[5] 视觉合同
    选 design-locks/<profile>.md
        ↓
[5.5] 可选：生成 AI 背景图
    ┌─ 判断：现有纯色方案是否已足够？
    │    是 → 跳过，直接到步骤 6
    │    否 → 执行以下步骤：
    │         • 构造图片 Prompt（基于 design-profile 颜色 + 风格）
    │         • 调用 DALL-E 3 / Flux API
    │         • 下载 PNG 到 assets/cover-bg.png
    │         • 在 Codex Prompt 中注明：
    │           封面和章节页使用 assets/cover-bg.png 作为背景
    │           叠加 40-60% 不透明度的遮罩（design-profile 主色）
    └─────────────────────────────────────────
        ↓
[6] Codex Presentations 生成 PPTX
```

---

## 给 Codex 的 Prompt 片段（带背景图）

```text
背景图已生成并保存在 assets/cover-bg.png。

封面页和章节切换页：
- 使用 assets/cover-bg.png 作为满铺背景图
- 叠加 50% 不透明度的遮罩，颜色使用 design-profile 的主背景色
- 文字颜色用 design-profile 的反色（浅底用深字，深底用白字）

内容页：
- 不使用背景图
- 按 design-profile 的纯色填充方案
```

---

## 注意事项

1. **遮罩必须加**：背景图直接叠文字会导致对比度不足，遮罩是保障可读性的关键
2. **尺寸要对**：PPT 幻灯片通常是 1920×1080（16:9），生成时指定分辨率
3. **图片不放 Git**：在 `.gitignore` 中加入 `assets/`，生成的图片是临时文件，不需要版本管理
4. **每次可以重新生成**：如果第一次的图不满意，重新调用 API 即可，费用极低
