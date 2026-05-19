# 工作流：Open Design + Anthropic pptx skill + VS Code

## 核心思路

```
MD 内容（你写）
    ↓
选择设计档案（design-profiles/）
    ↓
Claude Code 调用 pptx skill（pptxgenjs）
按设计档案规范生成 PPTX
    ↓
VS Code 用 thumbnail.py 预览缩略图
或直接打开 PowerPoint 检查
    ↓
不满意 → 告诉 Claude 改哪页 → 重新生成
    ↓
最终输出：可编辑 .pptx
```

---

## 三层分工

| 层 | 工具 | 作用 |
|----|------|------|
| 内容层 | Marp MD / 普通 MD | 写内容大纲、文字、数据 |
| 设计层 | `design-profiles/` | 确定配色、字体、版式语言 |
| 生成层 | pptx skill + pptxgenjs | 生成可编辑 PPTX |

---

## 可用设计档案

| 文件 | 风格 | 适合场景 |
|------|------|---------|
| `guizang-monocle.md` | 墨水经典，暖纸色底 | 通用商业、科技、路演 |
| `guizang-indigo.md` | 靛蓝瓷，冷调科技感 | 技术方案、数据报告、竞赛 |
| `swiss-klein-blue.md` | 瑞士国际主义，Klein Blue | 商业计划、产品路线、执行报告 |
| `linear-dark.md` | Linear 暗色，工程精准感 | SaaS 产品、投资人 deck |
| `notion-warm.md` | Notion 暖白，亲和极简 | 课程汇报、内部文档、文化类 |

---

## 具体操作步骤

### 第一步：准备内容

在 VS Code 里写好内容 MD，包括：
- 每页的主标题
- 正文要点
- 需要展示的数据/图表
- 演讲者备注（可选）

不需要考虑格式，只管内容。

### 第二步：选择设计档案

根据演示场景选一个档案，记下档案名（比如 `swiss-klein-blue`）。

### 第三步：给 Claude Code 的 Prompt

```
使用 pptx skill 帮我生成一个演示文稿。

设计档案：[档案名，比如 swiss-klein-blue]
参考文件：design-profiles/swiss-klein-blue.md

内容如下：
[粘贴你的 MD 内容]

要求：
- 严格按照设计档案的配色、字体、版式铁律
- 使用 pptxgenjs 生成
- 生成后用 thumbnail.py 预览，检查排版问题
- 至少完成一次 fix-and-verify 循环
- 输出文件保存为 outputs/deck.pptx
```

### 第四步：预览

```bash
# 生成缩略图（需要 LibreOffice + Poppler）
python skills/pptx/scripts/thumbnail.py outputs/deck.pptx

# 或直接用 VS Code 打开查看（需要 Office Viewer 插件）
```

### 第五步：迭代修改

告诉 Claude：
- "第 3 页的数字太小，改成 48pt"
- "封面背景换成深色反白"
- "KPI 那页改成 3 列而不是 4 列"

Claude 会修改对应页的 pptxgenjs 代码并重新生成。

---

## 安装 pptx skill 依赖

```bash
# Python 依赖
pip install "markitdown[pptx]" Pillow

# Node.js 依赖
npm install -g pptxgenjs

# macOS 安装 LibreOffice（用于预览转换）
brew install --cask libreoffice

# macOS 安装 Poppler（用于 PDF→图片）
brew install poppler
```

---

## 与 Marp 的关系

| 用途 | 推荐工具 |
|------|---------|
| 快速写作 + 结构检查 | Marp MD + VS Code Preview |
| 提交用 PDF（视觉最佳）| `npm run export:pdf` |
| 可编辑 PPTX（需要对方修改）| pptx skill + Open Design 档案 |
| 特别漂亮的 HTML 演示 | guizang / swiss HTML 模板（直接 prompt Claude）|

---

## 参考资源

- Anthropic pptx skill: `skills/pptx/SKILL.md`
- pptxgenjs 用法: `skills/pptx/pptxgenjs.md`
- 编辑现有 PPTX: `skills/pptx/editing.md`
- Open Design 原始仓库: https://github.com/nexu-io/open-design
