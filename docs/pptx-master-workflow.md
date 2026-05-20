# 从主题到专业 PPTX：完整工作流

> 适用场景：你有一个主题，或者已经有了文字内容，想做成设计专业、逻辑清晰的 PPTX。

---

## 总览

```
[阶段一] 内容准备
   写 deck.md（结构 + 文字 + 数据）
       ↓
[阶段二] 设计选型
   用 ui-ux-pro-max 查配色/字体风格建议
   → 选 design-profiles/ 中对应的设计档案
       ↓
[阶段三] 生成 PPTX
   Codex / Claude 读取 deck.md + design-profile
   → 调用 pptxgenjs（presentation skill）
   → 输出可编辑 .pptx
       ↓
[阶段四] 预览 & 迭代
   打开 .pptx 检查
   → 告诉 AI 改哪里 → 重新生成
       ↓
[最终] 提交 / 分享
```

---

## 阶段一：内容准备

### 1.1 写 `deck.md`

不需要任何格式指令，只写**内容骨架**：

```markdown
# 演示主题（会成为封面标题）

## 演示背景
- 项目名称、日期、演讲人

## 问题 / 机会
- 核心问题是什么
- 市场规模 / 数据支撑

## 解决方案
- 我们做了什么
- 核心差异点（3 个以内）

## 成果 / 数据
- 关键指标（数字要精确，不要编造）

## 下一步
- 请求 / 行动项

## 附录（可选）
- 详细数据、技术细节
```

### 1.2 确认页数规划

| 演示类型 | 建议页数 |
|---------|---------|
| 投资人路演 | 10–12 页 |
| 竞赛答辩 | 8–15 页 |
| 项目汇报 | 6–10 页 |
| 课程展示 | 5–8 页 |

---

## 阶段二：设计选型

### 2.1 用 ui-ux-pro-max 获取设计建议

运行以下搜索（在项目根目录执行）：

```bash
# 1. 按行业查配色方案
python3 skills/ui-ux-pro-max/scripts/search.py "SaaS tech startup" --domain color

# 2. 查字体搭配风格
python3 skills/ui-ux-pro-max/scripts/search.py "professional elegant" --domain typography

# 3. 查 UI 风格定位
python3 skills/ui-ux-pro-max/scripts/search.py "minimalism dark mode" --domain style
```

**常用行业关键词：**

| 场景 | 搜索词 |
|------|-------|
| 科技 / SaaS | `saas tech startup` |
| 金融 / 投资 | `fintech investment finance` |
| 医疗 / 健康 | `healthcare medical` |
| 教育 | `education learning` |
| 品牌 / 消费品 | `brand consumer beauty` |
| 竞赛答辩 | `competition academic professional` |

### 2.2 选择 design-profile

根据 ui-ux-pro-max 建议 + 场景，从 `design-profiles/` 选一个：

| 档案 | 风格 | 适合 |
|------|------|------|
| `guizang-monocle` | 暖纸色 + 衬线，叙事感 | 通用商业、路演、课程汇报 |
| `guizang-indigo` | 靛蓝 + 冷调科技 | 技术方案、数据报告、竞赛 |
| `swiss-klein-blue` | Klein Blue + 瑞士风 | 商业计划、执行报告、产品路线 |
| `linear-dark` | 暗色 + 精准工程感 | SaaS 产品、投资人 deck |
| `notion-warm` | 暖白 + 亲和极简 | 内部文档、文化类、轻量展示 |

**决策参考：**
- 要说服投资人 → `swiss-klein-blue` 或 `linear-dark`
- 要参加比赛 → `guizang-indigo` 或 `swiss-klein-blue`
- 要做课程展示 → `guizang-monocle` 或 `notion-warm`
- 对方需要可编辑中文 PPTX → 任选，注意字体替换（见阶段四）

---

## 阶段三：生成 PPTX

### 3.1 使用 Codex（推荐）

在 Codex 或 VS Code 终端中，给 AI 以下 Prompt：

```
我要做一个演示文稿。

[设计档案]
请读取 design-profiles/<档案名>.md，严格按照其中的：
- 配色（hex 值锁死，不能改）
- 字体（display/body 字体对应中英文）
- 版式规则（直角、禁渐变等铁律）

[内容文件]
请读取 deck.md，按其结构生成幻灯片，逻辑顺序不变。

[生成要求]
- 使用 pptxgenjs 生成可编辑 .pptx
- 根据 skills/pptx/SKILL.md 的工作流执行
- 封面用 L01 Hero Cover 版式
- 章节切换用 L02 Act Divider
- 数据页用 L03 Big Numbers Grid
- 流程页用 L06 Pipeline
- 页码格式：右下角 01 / N
- 严禁编造数字，所有数据来自 deck.md
- 输出保存为 outputs/<主题名>.pptx

生成完成后，用 thumbnail.py 生成预览缩略图供检查。
```

### 3.2 使用 Claude Code（备用）

```bash
# 在项目目录中，给 Claude 同样的指令
# 参考上方 Prompt，替换档案名和主题名即可
```

### 3.3 关键设计约束（所有档案通用）

- **禁止渐变**：pptxgenjs 所有填充用纯色（`fill: {color: "hex"}`）
- **禁止圆角**：`borderRadius: 0`
- **禁止外部图片 URL**：用色块/形状代替
- **页码**：每页右下角 `01 / N`
- **分割线**：1px hairline，用主色，不用粗线

---

## 阶段四：预览与迭代

### 4.1 预览方式

```bash
# 生成缩略图（需要 LibreOffice + Poppler）
python skills/pptx/scripts/thumbnail.py outputs/<文件名>.pptx

# 或直接用 PowerPoint / Keynote 打开检查
```

### 4.2 常见迭代指令

| 问题 | 给 AI 的指令 |
|------|------------|
| 某页文字太多 | "第 N 页正文超过 5 行，提炼成 3 个要点" |
| 数据页看不清 | "第 N 页数字改为 64pt，标签改为 11pt uppercase" |
| 封面需要副标题 | "封面加副标题：XXX，字号 20pt，muted 颜色" |
| 章节太多/少 | "在第 N 页后插入一个 Act Divider，标题：XXX" |
| 颜色不对 | "第 N 页背景换成设计档案的 paper-tint 色" |

### 4.3 中文字体替换（手动）

pptxgenjs 生成后，用 PowerPoint 手动替换：

1. `编辑` → `查找/替换` → `替换字体`
2. 将 `Inter` 替换为 `微软雅黑` 或 `苹方`（视平台）
3. 将 `Noto Serif SC` 替换为 `宋体` 或 `思源宋体`

---

## 快速参考卡

```
有主题 → 写 deck.md（只管内容，不管格式）
         ↓
选设计 → python3 skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain color
         查结果 → 对照 design-profiles/ 选档案
         ↓
生成   → 给 Codex/Claude 的 Prompt：
         "读取 design-profiles/<档案>.md + deck.md，
          用 pptxgenjs 生成 outputs/deck.pptx"
         ↓
检查   → 打开 .pptx 预览，列出要改的点
         告诉 AI：重新生成对应页
         ↓
完成   → 手动替换中文字体（如需要）→ 导出分享
```

---

## 三层工具分工

| 层 | 工具 | 职责 |
|----|------|------|
| **设计情报** | `skills/ui-ux-pro-max` | 查行业配色、字体风格、UI 趋势 |
| **设计约束** | `design-profiles/` | 锁死 hex 值、字体、版式铁律 |
| **生成引擎** | pptxgenjs + pptx skill | 按约束生成可编辑 .pptx |

这三层相互独立，也相互补充：
- 没有 ui-ux-pro-max：不知道该选哪种风格
- 没有 design-profiles：AI 会自由发挥，配色字体不一致
- 没有 pptx skill：只能生成截图 PPTX，无法编辑

---

## 本项目文件索引

```
MD2PPT/
├── deck.md                          # 你的内容（从这里开始）
├── design-profiles/                 # 选一个设计档案
│   ├── guizang-monocle.md
│   ├── guizang-indigo.md
│   ├── swiss-klein-blue.md
│   ├── linear-dark.md
│   └── notion-warm.md
├── skills/
│   ├── pptx/                        # Anthropic pptx skill（生成引擎）
│   │   ├── SKILL.md
│   │   ├── pptxgenjs.md
│   │   └── scripts/thumbnail.py
│   └── ui-ux-pro-max/               # 设计情报数据库
│       ├── SKILL.md
│       ├── data/                    # CSV 数据库（配色、字体、风格等）
│       └── scripts/search.py
├── docs/
│   ├── pptx-master-workflow.md      # 本文件
│   ├── workflow-with-open-design.md # 详细步骤说明
│   └── pptx-generation-schemes.md  # 方案对比
└── outputs/                         # 生成的 PPTX 放这里（gitignore）
```
