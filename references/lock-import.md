# Design Lock 导入：从 PPTX 模板提取设计系统

把一个现有 PPTX 模板变成 design-lock 的流程。完成后这个 lock 和内置的 5 个完全等价，可以在 Step 5 中选择。

---

## 什么可以自动提取，什么需要人工填写

| 信息 | 来源 | 方式 |
|------|------|------|
| 颜色 | `ppt/theme/theme1.xml` — `<a:clrScheme>` | **自动提取** |
| 字体 | `ppt/theme/theme1.xml` — `<a:fontScheme>` | **自动提取** |
| 背景色 | 幻灯片母版 XML | **自动提取** |
| 布局名称 | `ppt/slideLayouts/` 目录 | **自动列出** |
| 网格/间距规则 | 幻灯片母版占位符坐标 | 半自动（Claude 推断） |
| 图表标注风格 | 无法从文件提取 | **人工描述** |
| 禁用规则 | 无法从文件提取 | **人工描述** |
| 情绪/适用场景 | 无法从文件提取 | **人工描述** |

---

## 提取步骤

### 1. 运行提取脚本

```bash
python3 scripts/extract_lock.py path/to/your-template.pptx --name my-brand
# 输出：design-locks/my-brand.md（草稿，含 TODO 占位符）
```

### 2. 查看草稿，填写 TODO

脚本会提取颜色和字体，但以下内容需要你补充：

```markdown
## 结构规则（TODO：人工填写）
- 标题字号：__
- 正文字号：__
- 网格边距：__
- 允许哪些 layout 类型：__

## 图表规范（TODO：人工填写）
- 图表标注方式：直接标注 / 图例
- 允许的图表类型：__

## 禁用规则（TODO：人工填写）
- 不允许渐变：是/否
- 不允许投影：是/否

## 情绪与适用场景（TODO：人工填写）
- tone: __
- suitable_for: __
- avoid_for: __
```

### 3. 运行完成后同步

```bash
bash install.sh   # 将新 lock 同步到全局 skill 目录
```

新 lock 会在下次 Step 5 的对比表和 `locks-preview.html` 中出现。

---

## 换模板（生成后重新套用）

PPTX 已生成后，想换一套结构层：

1. 重新走 Step 5 — 选不同的 lock
2. 用 Step 4 确认的颜色层 + 新的结构层，重新生成 Design Contract
3. 用新 Design Contract 重跑 Step 6（重新生成 PPTX）

注意：这是**重新生成**，不是在现有 PPTX 上套用模板。PPTX 格式不支持程序化的母版替换。

---

## scripts/extract_lock.py（待实现）

占位脚本，提取逻辑待补全。当前版本仅解析主题颜色和字体：

```bash
python3 scripts/extract_lock.py <input.pptx> --name <lock-name>
```

优先级：有真实需求时实现，当前用人工填写 design-locks 文件替代。
