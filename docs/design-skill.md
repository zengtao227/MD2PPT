# UI/UX Pro Max 设计支持

`skills/ui-ux-pro-max` 是本仓库用于 PPT 和可视化页面设计的本地 skill。它不是自动生成 PPT 的工具，而是一个可搜索的设计参考库，可以在确定视觉方向时提供配色、字体、布局、图表和 UX 检查建议。

## 适用场景

- 路演 PPT 视觉重做
- 比赛答辩 PPT 版式优化
- Markdown PPT 的配色与字体方案选择
- 图表页、时间线页、对比页的表达方式选择
- 导出前的可读性、对比度、留白检查

## 推荐检索顺序

```bash
python3 skills/ui-ux-pro-max/scripts/search.py "<项目类型>" --domain product
python3 skills/ui-ux-pro-max/scripts/search.py "<风格关键词>" --domain style
python3 skills/ui-ux-pro-max/scripts/search.py "<字体气质>" --domain typography
python3 skills/ui-ux-pro-max/scripts/search.py "<行业或场景>" --domain color
python3 skills/ui-ux-pro-max/scripts/search.py "<图表类型>" --domain chart
python3 skills/ui-ux-pro-max/scripts/search.py "accessibility layout spacing contrast" --domain ux
```

## 路演 PPT 建议默认方向

对于高校竞赛、酒店服务、AI 应用路演这类材料，优先采用：

- 风格：Swiss Modernism 2.0 / Trust & Authority / Minimalism
- 配色：浅色背景、深色正文、蓝绿双主色，少量金色作为强调
- 字体：现代专业型无衬线字体，中文优先保证可读性和稳定导出
- 版式：12 栏网格、充足留白、少装饰、少大面积暗色
- 检查：标题不被线条穿过，正文不低对比，卡片不拥挤，句末标点不破坏标题观感

## 使用原则

设计建议必须服务于内容表达。涉及比赛名称、项目定义、评分权重、学校名称和团队信息时，以项目资料和官方规则为准，不用设计 skill 改写事实。
