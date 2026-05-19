# PPT 生成方案研究与选型（2026-05）

## 核心需求

- 所见即所得：预览效果 = 最终导出效果
- 导出 PPTX 可在 PowerPoint 里直接编辑文字
- 尽量免费，支持中文内容

---

## 方案对比总览

| 方案 | 预览方式 | PPTX 可编辑 | 中文字体 | 费用 | 推荐度 |
|------|----------|------------|---------|------|--------|
| Marp CLI 直接导出 | VS Code Marp Preview | ❌ 截图/不可编辑 | ✅ 完整 | 免费 | 内容定稿后提交用 |
| Office-PowerPoint-MCP-Server | 无内置预览 | ✅ | ✅ | 免费 | ⭐⭐ |
| pptx-generator-mcp | 无内置预览 | ✅ | ✅ | 免费 | ⭐⭐ |
| Google Slides MCP（matteoantoci） | 浏览器 Google Slides | ✅ | ⚠️ 字体替换 | 免费 | ⭐⭐⭐⭐ **当前选用** |
| Google Slides MCP（Composio） | 浏览器 Google Slides | ✅ | ⚠️ 字体替换 | 免费额度有限 | ⭐⭐⭐ |
| Alai MCP | Alai 在线编辑器 | ✅（需付费） | ✅ | $16/月起 | ⭐⭐⭐⭐⭐（付费首选） |

---

## 各方案详细说明

### 1. Marp CLI 直接导出（现有工作流）

**工作流：** VS Code 写 Marp MD → Marp Preview 实时预览 → `npm run export:all` 导出

**优点：**
- 预览与导出高度一致（Chromium 渲染，CSS 完整保留）
- 支持中文字体（本地渲染）
- 完全免费，无需配置

**缺点：**
- PPTX 不可编辑（每页是渲染截图贴入 PPT）
- 复杂 CSS 布局在 PDF/PPTX 导出时可能有偏差

**适合场景：** 内容已定稿，需要提交或放映用的 PDF/PPTX，不需要对方再次编辑。

---

### 2. Office-PowerPoint-MCP-Server（GongRzhe）

**GitHub：** `GongRzhe/Office-PowerPoint-MCP-Server`

**工作流：** Claude/Codex CLI 读取 MD → 调用 MCP 工具逐步构建幻灯片 → 生成 .pptx

**优点：**
- 32 个工具，功能最完整（文字、图片、表格、图表、模板）
- PPTX 完全可编辑
- 基于 python-pptx，免费

**缺点：**
- 无内置预览，每次改完需手动打开 PowerPoint 查看
- AI 需要重新解读内容，Marp CSS 样式完全丢失
- 视觉效果与 Marp 预览差距大

---

### 3. pptx-generator-mcp（dmytro-ustynov）

**GitHub：** `dmytro-ustynov/pptx-generator-mcp`

**工作流：** Claude/Codex CLI 读取 MD 文件 → MCP 解析结构 → 生成 .pptx

**优点：**
- 专门针对 MD → PPTX 场景
- 支持代码块、表格、自定义品牌配置
- 内容结构（标题、列表）对应关系比方案 2 更直接
- 免费

**缺点：**
- 无内置预览
- CSS 样式丢失，视觉与 Marp 差距大
- 项目为个人维护，更新频率不确定

---

### 4. Google Slides MCP（matteoantoci）⭐ 当前选用方案

**GitHub：** `matteoantoci/google-slides-mcp`

**工作流：**
```
Claude CLI 调用 MCP → 写入 Google Slides
        ↓
浏览器打开 Google Slides = 实时预览（所见即所得）
        ↓
不满意 → 告诉 Claude 改 → 刷新浏览器
        ↓
满意 → 文件 → 下载 → PPTX（完全可编辑）
        ↓
导出后检查中文字体，必要时手动替换一次
```

**优点：**
- 浏览器里的 Google Slides 就是最终效果，真正所见即所得
- PPTX 完全可编辑
- 完全免费（自部署，需一次性配置 Google API）
- Claude CLI 和 Codex CLI 均可使用

**缺点：**
- **中文字体问题**：导出 PPTX 时宋体/黑体会被替换为 Noto Sans 或 Arial，需导出后手动检查并替换字体
- 需要一次性配置：Google Cloud 项目 + 开启 Slides API + OAuth 凭据
- 复杂图表导出为图片（非原生 PPT 图表对象），不能在 PPT 里修改数据

**配置步骤（一次性）：**
1. 前往 Google Cloud Console，新建项目
2. 开启 Google Slides API
3. 创建 OAuth 2.0 凭据，下载 `credentials.json`
4. 克隆 `matteoantoci/google-slides-mcp`，配置到 Claude/Codex CLI 的 MCP 设置中
5. 首次运行时浏览器弹出授权页，点击允许

**已知问题与处理：**
- 导出 PPTX 后，打开 PowerPoint → 全选 → 字体替换 → 将 Arial/Noto Sans 换成目标中文字体（如微软雅黑、黑体）

---

### 5. Google Slides MCP（Composio）

**工作流与方案 4 相同，区别在于认证方式**

**优点：**
- 无需自己配置 Google Cloud，Composio 托管 OAuth
- 支持 Claude Code、Codex、Cursor 全覆盖

**缺点：**
- 有免费额度限制，重度使用需付费
- 中文字体问题同方案 4

---

### 6. Alai MCP（付费时的最优方案）

**GitHub：** `getalai/alai-mcp-server`

**工作流：** Claude/Codex CLI → Alai MCP → Alai 在线编辑器（浏览器预览 + 编辑）→ 导出 PPTX/PDF

**优点：**
- 有自己的浏览器编辑器，所见即所得
- 无需 Google 账号，无中文字体替换问题
- 导出 PPTX 无需手动调字体
- 可与 Notion、Stripe 等 MCP 联动，从多数据源生成 deck

**缺点：**
- **免费版只能导出 PDF，PPTX 导出需付费**（$16/月起）
- 免费版仅 200-300 AI credits，数量有限

**适合场景：** 愿意每月 $16，追求最干净工作流且不想处理字体问题。

---

## 当前推荐工作流

```
VS Code 写 Marp MD（内容草稿 + 结构）
        ↓
Claude CLI + matteoantoci Google Slides MCP
把 MD 内容转入 Google Slides
        ↓
浏览器预览、迭代修改（告诉 Claude 改 → 刷新）
        ↓
满意 → Google Slides 下载 PPTX
        ↓
PowerPoint 打开 → 字体替换（宋体/黑体/微软雅黑）
        ↓
完成：可编辑 PPTX ✅
```

---

## 未来升级路径

- 如中文字体替换太麻烦，切换到 **Alai MCP 付费版**
- 如需要纯离线生成，考虑改进 **GongRzhe MCP** 的 prompt 模板，预设固定样式风格
