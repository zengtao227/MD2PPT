#!/usr/bin/env python3
"""
Generate assets/locks-preview.html — structural comparison of all design-locks.
Shows a representative content slide for each lock, demonstrating layout grammar,
typography hierarchy, and structural elements — NOT colors (colors are Step 4).

Usage:
    python3 scripts/preview_locks.py
    # then open: assets/locks-preview.html
"""

from pathlib import Path

# Each lock entry defines: default colors (for structural demo only),
# and the structural HTML that goes inside the slide mockup.
# Fonts are loaded from Google Fonts for authentic rendering.

LOCKS = [
    {
        "id": "swiss-klein-blue",
        "name": "Swiss · Klein Blue",
        "zh": "瑞士国际主义",
        "structure_desc": "权威 · 精准 · 高对比",
        "suitable": ["商业计划", "产品路线图", "投资人演示", "执行报告"],
        "avoid": ["文化类", "叙事性演示"],
        "cover_html": """
<div style="display:flex; height:100%; gap:0; background:#fafaf8;">
  <div style="width:6px; background:#002FA7; flex-shrink:0;"></div>
  <div style="flex:1; padding:22px 28px; display:flex; flex-direction:column; justify-content:space-between;">
    <div style="font-size:7.5px; font-weight:700; letter-spacing:2.5px; color:#002FA7; text-transform:uppercase;">STRATEGY REPORT 2024</div>
    <div>
      <div style="font-size:22px; font-weight:800; line-height:1.15; color:#0a0a0a; font-family:'Inter',sans-serif; margin-bottom:14px;">AI 基础设施<br>行业全景报告</div>
      <div style="height:2px; background:#002FA7; width:48px; margin-bottom:12px;"></div>
      <div style="font-size:9px; color:#6b6b6b;">中国 AI 产业研究院 · 2024.Q4</div>
    </div>
    <div style="font-size:7px; color:#bbb;">01 / 18</div>
  </div>
</div>""",
        "slide_html": """
<div style="display:flex; height:100%; gap:0;">
  <div style="width:6px; background:#002FA7; flex-shrink:0;"></div>
  <div style="flex:1; padding:20px 24px; display:flex; flex-direction:column; gap:0;">
    <div style="font-size:8px; font-weight:700; letter-spacing:2px; color:#002FA7; text-transform:uppercase; margin-bottom:6px;">SECTION 02</div>
    <div style="font-size:18px; font-weight:800; line-height:1.15; color:#0a0a0a; margin-bottom:14px; font-family:'Inter',sans-serif;">市场规模已达 2,400 亿<br>年增速维持 34%</div>
    <div style="height:2px; background:#0a0a0a; width:40px; margin-bottom:14px;"></div>
    <div style="display:flex; gap:14px; flex:1;">
      <div style="flex:1; background:#f0f0ee; padding:10px; border-radius:2px;">
        <div style="font-size:9px; font-weight:700; color:#002FA7; margin-bottom:4px;">核心驱动</div>
        <div style="font-size:8px; color:#1a1a1a; line-height:1.6;">企业数字化转型加速<br>AI 基础设施投入翻倍<br>政策支持持续加码</div>
      </div>
      <div style="flex:1; background:#f0f0ee; padding:10px; border-radius:2px;">
        <div style="font-size:9px; font-weight:700; color:#002FA7; margin-bottom:4px;">竞争格局</div>
        <div style="font-size:8px; color:#1a1a1a; line-height:1.6;">头部集中度提升<br>垂直赛道分化明显<br>海外扩张窗口开启</div>
      </div>
    </div>
    <div style="margin-top:10px; font-size:7px; color:#6b6b6b; display:flex; justify-content:space-between;">
      <span>来源：IDC 2024</span><span>02 / 10</span>
    </div>
  </div>
</div>""",
    },
    {
        "id": "linear-dark",
        "name": "Linear Dark",
        "zh": "工程深色",
        "structure_desc": "工程精密 · 现代科技 · 暗色",
        "suitable": ["SaaS 产品", "技术平台", "工程演示", "投资人（技术背景）"],
        "avoid": ["教学类", "文化类"],
        "cover_html": """
<div style="height:100%; padding:24px 28px; display:flex; flex-direction:column; justify-content:space-between; background:#08090a;">
  <div style="display:flex; align-items:center; gap:8px;">
    <div style="width:8px; height:8px; border-radius:50%; background:#5e6ad2;"></div>
    <div style="font-size:7.5px; font-weight:600; color:#8a8f98; letter-spacing:1.5px; text-transform:uppercase; font-family:monospace;">Product · Engineering · 2024</div>
  </div>
  <div>
    <div style="font-size:21px; font-weight:700; color:#f7f8f8; line-height:1.2; font-family:'Inter',sans-serif; margin-bottom:10px;">重新定义<br>云原生部署流水线</div>
    <div style="font-size:9px; color:#5e6ad2; font-family:monospace;">v3.0 Architecture Deep Dive</div>
  </div>
  <div style="display:flex; justify-content:space-between; font-size:7px; color:#3a3f47; font-family:monospace;">
    <span>Internal · Confidential</span><span style="color:#5e6ad2;">01 / 12</span>
  </div>
</div>""",
        "slide_html": """
<div style="height:100%; padding:18px 22px; display:flex; flex-direction:column; gap:0; background:#08090a;">
  <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
    <div style="width:8px; height:8px; border-radius:50%; background:#5e6ad2;"></div>
    <div style="font-size:8px; font-weight:600; color:#8a8f98; letter-spacing:1.5px; text-transform:uppercase;">Architecture Overview</div>
  </div>
  <div style="font-size:16px; font-weight:700; color:#f7f8f8; line-height:1.2; margin-bottom:16px; font-family:'Inter',sans-serif;">三层解耦架构将部署时间<br>从 4 小时压缩至 11 分钟</div>
  <div style="display:flex; gap:8px; flex:1;">
    <div style="flex:1; border:1px solid #23252a; border-radius:4px; padding:10px;">
      <div style="font-size:8px; font-weight:600; color:#5e6ad2; margin-bottom:6px; font-family:monospace;">API Layer</div>
      <div style="font-size:7.5px; color:#d0d6e0; line-height:1.7; font-family:monospace;">rate-limit: 10k/min<br>auth: JWT + mTLS<br>cache: Redis L1</div>
    </div>
    <div style="flex:1; border:1px solid #23252a; border-radius:4px; padding:10px; background:#0f1011;">
      <div style="font-size:8px; font-weight:600; color:#5e6ad2; margin-bottom:6px; font-family:monospace;">Core Engine</div>
      <div style="font-size:7.5px; color:#d0d6e0; line-height:1.7; font-family:monospace;">workers: 32 goroutines<br>queue: Kafka<br>latency: p99 &lt; 40ms</div>
    </div>
    <div style="flex:1; border:1px solid #23252a; border-radius:4px; padding:10px;">
      <div style="font-size:8px; font-weight:600; color:#5e6ad2; margin-bottom:6px; font-family:monospace;">Storage</div>
      <div style="font-size:7.5px; color:#d0d6e0; line-height:1.7; font-family:monospace;">pg: write-primary<br>s3: cold archive<br>ttl: 90d policy</div>
    </div>
  </div>
  <div style="margin-top:10px; font-size:7px; color:#62666d; display:flex; justify-content:space-between;">
    <span>Internal · Confidential</span><span style="color:#5e6ad2;">05 / 12</span>
  </div>
</div>""",
    },
    {
        "id": "guizang-indigo",
        "name": "Academic Indigo",
        "zh": "学术靛蓝",
        "structure_desc": "冷调学术 · 信息密度高 · 研究感",
        "suitable": ["技术方案", "数据报告", "竞赛答辩", "学术研究"],
        "avoid": ["温暖叙事类", "消费者品牌"],
        "cover_html": """
<div style="height:100%; display:flex; flex-direction:column; background:#f1f3f5;">
  <div style="background:#0a1f3d; flex:2.2; padding:20px 26px; display:flex; flex-direction:column; justify-content:flex-end;">
    <div style="font-size:7.5px; color:rgba(241,243,245,.45); letter-spacing:1.5px; margin-bottom:10px; font-family:'Noto Serif SC',serif;">研究报告 · 2024</div>
    <div style="font-size:20px; font-weight:700; color:#f1f3f5; line-height:1.3; font-family:'Noto Serif SC',serif;">AI 企业采用率<br>深度调研报告</div>
  </div>
  <div style="flex:1; padding:12px 26px; display:flex; align-items:center; justify-content:space-between; border-top:2px solid #0a1f3d;">
    <div style="font-size:9px; color:#0a1f3d; font-family:'Noto Serif SC',serif;">中国信通院 · 产业研究部</div>
    <div style="font-size:7.5px; color:#4a6080;">01 / 09</div>
  </div>
</div>""",
        "slide_html": """
<div style="height:100%; display:flex; flex-direction:column; background:#f1f3f5;">
  <div style="background:#0a1f3d; padding:12px 22px 10px; display:flex; align-items:baseline; gap:12px;">
    <div style="font-size:16px; font-weight:700; color:#f1f3f5; font-family:'Noto Serif SC',serif; line-height:1.2;">数据显示：三类企业占据<br>行业 78% 的 AI 研发投入</div>
    <div style="font-size:7px; color:rgba(241,243,245,.55); align-self:flex-end; white-space:nowrap;">图 3-2</div>
  </div>
  <div style="flex:1; padding:12px 22px; display:flex; gap:14px;">
    <div style="flex:2;">
      <div style="font-size:7.5px; font-weight:600; color:#4a6080; letter-spacing:1px; text-transform:uppercase; margin-bottom:7px;">企业类型分布（N=847）</div>
      <div style="border-top:1.5px solid #0a1f3d;">
        <div style="display:flex; padding:5px 0; border-bottom:1px solid #d0d7df; font-size:8px;">
          <div style="flex:2; font-weight:600; color:#0a1f3d; font-family:'Noto Serif SC',serif;">大型国央企</div>
          <div style="flex:1; text-align:right; color:#0a1f3d;">43.2%</div>
          <div style="flex:1; text-align:right; color:#4a6080;">↑ 6.1pp</div>
        </div>
        <div style="display:flex; padding:5px 0; border-bottom:1px solid #d0d7df; font-size:8px; background:#e4e8ec;">
          <div style="flex:2; font-weight:600; color:#0a1f3d; font-family:'Noto Serif SC',serif;">科技独角兽</div>
          <div style="flex:1; text-align:right; color:#0a1f3d;">22.7%</div>
          <div style="flex:1; text-align:right; color:#4a6080;">↑ 3.4pp</div>
        </div>
        <div style="display:flex; padding:5px 0; border-bottom:1px solid #d0d7df; font-size:8px;">
          <div style="flex:2; font-weight:600; color:#0a1f3d; font-family:'Noto Serif SC',serif;">专精特新企业</div>
          <div style="flex:1; text-align:right; color:#0a1f3d;">12.1%</div>
          <div style="flex:1; text-align:right; color:#4a6080;">↑ 1.8pp</div>
        </div>
      </div>
    </div>
    <div style="flex:1; border-left:2px solid #0a1f3d; padding-left:10px;">
      <div style="font-size:8px; font-weight:700; color:#0a1f3d; margin-bottom:5px; font-family:'Noto Serif SC',serif;">研究方法</div>
      <div style="font-size:7.5px; color:#4a6080; line-height:1.65;">问卷+访谈混合<br>置信区间 95%<br>抽样误差 ±3.2%</div>
    </div>
  </div>
  <div style="padding:4px 22px 7px; font-size:6.5px; color:#4a6080; border-top:1px solid #c8d0da;">
    资料来源：中国信通院《2024年企业AI采用率报告》第三章 &nbsp;|&nbsp; 03 / 09
  </div>
</div>""",
    },
    {
        "id": "guizang-monocle",
        "name": "Warm Paper",
        "zh": "暖纸叙事",
        "structure_desc": "叙事 · 温暖纸感 · 编辑感",
        "suitable": ["路演", "课程汇报", "观点类演示", "项目方案"],
        "avoid": ["纯工程类", "数据密集报告"],
        "cover_html": """
<div style="height:100%; padding:22px 32px 18px; display:flex; flex-direction:column; justify-content:space-between; background:#f1efea;">
  <div style="font-size:7.5px; letter-spacing:2.5px; color:#5a5650; text-transform:uppercase;">演讲 · 2024</div>
  <div>
    <div style="font-size:22px; font-weight:700; color:#0a0a0b; line-height:1.25; font-family:'Noto Serif SC',serif; margin-bottom:12px;">为什么大多数<br>产品创新都在白费力气</div>
    <div style="border-left:3px solid #0a0a0b; padding-left:10px; font-size:9px; font-style:italic; color:#5a5650; font-family:'Noto Serif SC',serif; line-height:1.6;">一个关于用户价值的深度观察</div>
  </div>
  <div style="font-size:7.5px; color:#8a8580;">张明 · 产品副总裁 &nbsp;|&nbsp; 01 / 11</div>
</div>""",
        "slide_html": """
<div style="height:100%; padding:18px 28px 14px 28px; display:flex; flex-direction:column; background:#f1efea;">
  <div style="font-size:7.5px; letter-spacing:2px; color:#5a5650; text-transform:uppercase; margin-bottom:8px;">洞察 · 03</div>
  <div style="font-size:17px; font-weight:700; line-height:1.25; color:#0a0a0b; margin-bottom:12px; font-family:'Noto Serif SC',serif; max-width:80%;">用户不是不愿付费，<br>而是还没看到值得付费的东西</div>
  <div style="border-left:3px solid #0a0a0b; padding-left:12px; margin-bottom:12px;">
    <div style="font-size:10px; font-style:italic; color:#0a0a0b; line-height:1.6; font-family:'Noto Serif SC',serif;">"我们访谈了 200 位流失用户，89% 给出的理由不是价格，而是「功能没用到」。"</div>
    <div style="font-size:7.5px; color:#5a5650; margin-top:4px;">— 用户研究报告，2024.Q3</div>
  </div>
  <div style="font-size:8.5px; color:#2a2a2b; line-height:1.75; font-family:'Noto Serif SC',serif; flex:1;">
    付费转化率低的核心原因在于价值感知缺口。当产品的核心功能与用户实际工作流高度契合时，付费意愿显著提升——平均溢价接受度达到免费版的 3.4 倍。
  </div>
  <div style="font-size:7px; color:#8a8580; margin-top:8px;">04 / 11</div>
</div>""",
    },
    {
        "id": "notion-warm",
        "name": "Notion Warm",
        "zh": "Notion 暖白",
        "structure_desc": "亲和 · 极简 · 文档感",
        "suitable": ["内部汇报", "文化类", "课程讲义", "轻量演示"],
        "avoid": ["投资人演示", "高强度外部场合"],
        "cover_html": """
<div style="height:100%; padding:24px 30px; display:flex; flex-direction:column; justify-content:space-between; background:#ffffff;">
  <div style="font-size:8px; color:#615d59; font-weight:500; letter-spacing:.5px;">2024 Q3 · 内部复盘</div>
  <div>
    <div style="font-size:21px; font-weight:700; color:#0d0d0d; line-height:1.3; font-family:'Inter',sans-serif; margin-bottom:10px;">产品团队<br>季度总结</div>
    <div style="font-size:9.5px; color:#615d59; line-height:1.7;">三个值得关注的结构性变化<br>以及下季度的重点方向</div>
  </div>
  <div style="display:flex; align-items:center; gap:10px;">
    <div style="width:18px; height:18px; background:#0d0d0d; border-radius:3px;"></div>
    <div style="font-size:9px; color:#9c9894;">产品团队 &nbsp;·&nbsp; 01 / 08</div>
  </div>
</div>""",
        "slide_html": """
<div style="height:100%; padding:20px 26px; display:flex; flex-direction:column; gap:0; background:#ffffff;">
  <div style="font-size:15px; font-weight:700; color:#0d0d0d; margin-bottom:6px; font-family:'Inter',sans-serif;">本季度三个值得关注的变化</div>
  <div style="font-size:8.5px; color:#615d59; margin-bottom:16px;">2024 Q3 内部复盘 · 产品团队</div>
  <div style="display:flex; flex-direction:column; gap:8px; flex:1;">
    <div style="background:#f6f5f4; border-radius:6px; padding:10px 12px; display:flex; gap:10px; align-items:flex-start;">
      <div style="width:20px; height:20px; background:#0d0d0d; border-radius:4px; flex-shrink:0; display:flex; align-items:center; justify-content:center;">
        <div style="width:8px; height:1.5px; background:white;"></div>
      </div>
      <div>
        <div style="font-size:9px; font-weight:600; color:#0d0d0d; margin-bottom:2px;">日活增长放缓，但留存显著改善</div>
        <div style="font-size:7.5px; color:#615d59; line-height:1.6;">次日留存从 38% 升至 51%，7日留存从 19% 升至 27%</div>
      </div>
    </div>
    <div style="background:#f6f5f4; border-radius:6px; padding:10px 12px; display:flex; gap:10px; align-items:flex-start;">
      <div style="width:20px; height:20px; background:#0d0d0d; border-radius:4px; flex-shrink:0; display:flex; align-items:center; justify-content:center;">
        <div style="width:8px; height:1.5px; background:white;"></div>
      </div>
      <div>
        <div style="font-size:9px; font-weight:600; color:#0d0d0d; margin-bottom:2px;">移动端使用比例超过桌面端</div>
        <div style="font-size:7.5px; color:#615d59; line-height:1.6;">移动占比 54%，较上季度 +11pp，催生新的导航需求</div>
      </div>
    </div>
    <div style="background:#f6f5f4; border-radius:6px; padding:10px 12px; display:flex; gap:10px; align-items:flex-start;">
      <div style="width:20px; height:20px; background:#0d0d0d; border-radius:4px; flex-shrink:0; display:flex; align-items:center; justify-content:center;">
        <div style="width:8px; height:1.5px; background:white;"></div>
      </div>
      <div>
        <div style="font-size:9px; font-weight:600; color:#0d0d0d; margin-bottom:2px;">NPS 从 32 跃升至 48</div>
        <div style="font-size:7.5px; color:#615d59; line-height:1.6;">主要驱动因素为新版编辑器和搜索速度提升</div>
      </div>
    </div>
  </div>
  <div style="font-size:7px; color:#9c9894; margin-top:10px; text-align:right;">03 / 08</div>
</div>""",
    },
]

import json as _json

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Design Locks — 结构层预览</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #eceae6;
  min-height: 100vh;
  padding: 28px 24px 48px;
  color: #1a1a1a;
}}
h1 {{ font-size: 20px; font-weight: 700; color: #111; margin-bottom: 4px; }}
.subtitle {{ font-size: 13px; color: #666; margin-bottom: 24px; line-height: 1.5; }}
.layout {{ display: flex; gap: 20px; max-width: 1100px; align-items: flex-start; }}

/* Left sidebar */
.sidebar {{
  width: 188px; flex-shrink: 0;
  background: white; border-radius: 12px; padding: 8px;
  box-shadow: 0 1px 4px rgba(0,0,0,.08);
}}
.sidebar-item {{
  padding: 10px 12px; border-radius: 8px; cursor: pointer;
  transition: background .12s; margin-bottom: 2px; user-select: none;
}}
.sidebar-item:hover {{ background: #f4f4f2; }}
.sidebar-item.active {{
  background: #EEF3FF; border-left: 3px solid #0061FF; padding-left: 9px;
}}
.sidebar-name {{ font-size: 13px; font-weight: 700; color: #111; line-height: 1.3; }}
.sidebar-item.active .sidebar-name {{ color: #0061FF; }}
.sidebar-zh {{ font-size: 11px; color: #888; margin-top: 1px; }}

/* Right detail pane */
.detail {{ flex: 1; min-width: 0; }}

/* Two slides side by side */
.slides-row {{
  display: flex; gap: 12px; margin-bottom: 14px;
}}
.slide-col {{ flex: 1; min-width: 0; }}
.slide-label {{
  font-size: 10px; font-weight: 600; color: #888; letter-spacing: .5px;
  text-transform: uppercase; margin-bottom: 5px;
}}
.slide-frame {{
  width: 100%; aspect-ratio: 16/9;
  border-radius: 8px; overflow: hidden;
  box-shadow: 0 3px 14px rgba(0,0,0,.13);
}}

/* Description box */
.desc-box {{
  background: white; border-radius: 10px; padding: 14px 18px;
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
  display: flex; gap: 24px;
}}
.desc-left {{ flex: 1; min-width: 0; }}
.desc-title {{ font-size: 15px; font-weight: 700; color: #111; margin-bottom: 2px; }}
.desc-zh {{ font-size: 12px; color: #888; margin-bottom: 8px; }}
.desc-tags {{
  font-size: 12px; color: #444; line-height: 1.6;
  border-left: 2px solid #ddd; padding-left: 10px;
}}
.desc-right {{ width: 200px; flex-shrink: 0; }}
.use-section {{ margin-bottom: 10px; }}
.use-label {{
  font-size: 10px; font-weight: 700; letter-spacing: .8px;
  text-transform: uppercase; margin-bottom: 5px;
}}
.use-label.good {{ color: #16a34a; }}
.use-label.bad {{ color: #dc2626; }}
.use-tags {{ display: flex; flex-wrap: wrap; gap: 4px; }}
.tag {{
  font-size: 11px; padding: 3px 8px; border-radius: 20px; line-height: 1.4;
}}
.tag.good {{ background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }}
.tag.bad {{ background: #fff1f2; color: #be123c; border: 1px solid #fecdd3; }}

/* Confirm area */
.confirm-area {{ margin-top: 14px; display: flex; align-items: center; gap: 14px; }}
.confirm-btn {{
  padding: 11px 26px; background: #0061FF; color: white;
  border: none; border-radius: 8px; font-size: 14px; font-weight: 700;
  cursor: pointer; transition: background .15s, transform .1s; letter-spacing: .2px;
}}
.confirm-btn:hover {{ background: #004ee0; transform: translateY(-1px); }}
.confirm-btn:active {{ transform: translateY(0); }}
.confirm-btn.done {{ background: #16a34a; cursor: default; transform: none; }}
.copied-msg {{
  display: none; font-size: 13px; color: #16a34a; font-weight: 600;
  padding: 10px 14px; background: #f0fdf4; border-radius: 8px;
  border: 1px solid #bbf7d0; line-height: 1.5;
}}
.copied-msg.show {{ display: block; }}
</style>
</head>
<body>
<h1>结构层预览 — Design Locks</h1>
<p class="subtitle">点击左侧选项查看封面和内页结构；颜色仅用于呈现风格，Step 4 确认的配色在生成时覆盖。</p>
<div class="layout">
  <div class="sidebar" id="sidebar"></div>
  <div class="detail">
    <div class="slides-row">
      <div class="slide-col">
        <div class="slide-label">封面</div>
        <div class="slide-frame" id="cover-frame"></div>
      </div>
      <div class="slide-col">
        <div class="slide-label">内页</div>
        <div class="slide-frame" id="content-frame"></div>
      </div>
    </div>
    <div class="desc-box">
      <div class="desc-left">
        <div class="desc-title" id="desc-title"></div>
        <div class="desc-zh" id="desc-zh"></div>
        <div class="desc-tags" id="desc-tags"></div>
      </div>
      <div class="desc-right">
        <div class="use-section">
          <div class="use-label good">✓ 适合</div>
          <div class="use-tags" id="suitable-tags"></div>
        </div>
        <div class="use-section">
          <div class="use-label bad">✗ 不适合</div>
          <div class="use-tags" id="avoid-tags"></div>
        </div>
      </div>
    </div>
    <div class="confirm-area">
      <button class="confirm-btn" id="confirm-btn" onclick="confirmSelection()">确认此结构层 →</button>
      <div class="copied-msg" id="copied-msg">
        ✓ 已复制到剪贴板！<br>粘贴到 Claude / Codex 对话框，然后继续 Step 5。
      </div>
    </div>
  </div>
</div>
<script>
const LOCKS = {locks_json};
let activeId = LOCKS[0].id;

function render() {{
  const lock = LOCKS.find(l => l.id === activeId);
  document.getElementById('sidebar').innerHTML = LOCKS.map(l => `
    <div class="sidebar-item ${{l.id === activeId ? 'active' : ''}}" onclick="selectLock('${{l.id}}')">
      <div class="sidebar-name">${{l.name}}</div>
      <div class="sidebar-zh">${{l.zh}}</div>
    </div>`).join('');
  document.getElementById('cover-frame').innerHTML = lock.cover_html;
  document.getElementById('content-frame').innerHTML = lock.slide_html;
  document.getElementById('desc-title').textContent = lock.name;
  document.getElementById('desc-zh').textContent = lock.zh;
  document.getElementById('desc-tags').textContent = lock.structure_desc;
  document.getElementById('suitable-tags').innerHTML =
    lock.suitable.map(t => `<span class="tag good">${{t}}</span>`).join('');
  document.getElementById('avoid-tags').innerHTML =
    lock.avoid.map(t => `<span class="tag bad">${{t}}</span>`).join('');
  const btn = document.getElementById('confirm-btn');
  btn.textContent = '确认此结构层 →';
  btn.classList.remove('done');
  document.getElementById('copied-msg').classList.remove('show');
}}

function selectLock(id) {{ activeId = id; render(); }}

function confirmSelection() {{
  const text = `我选择 ${{activeId}}`;
  navigator.clipboard.writeText(text).then(() => {{
    document.getElementById('confirm-btn').textContent = '✓ 已确认';
    document.getElementById('confirm-btn').classList.add('done');
    document.getElementById('copied-msg').classList.add('show');
  }}).catch(() => {{
    document.getElementById('copied-msg').innerHTML =
      `请手动复制粘贴到 Claude：<br><strong>${{text}}</strong>`;
    document.getElementById('copied-msg').classList.add('show');
  }});
}}

render();
</script>
</body>
</html>"""


def main() -> None:
    repo_root = Path(__file__).parent.parent
    assets_dir = repo_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    out = assets_dir / "locks-preview.html"

    locks_data = [
        {k: v for k, v in lock.items()
         if k in ("id", "name", "zh", "structure_desc", "slide_html")}
        for lock in LOCKS
    ]
    html = HTML_TEMPLATE.format(locks_json=_json.dumps(locks_data, ensure_ascii=False))
    out.write_text(html, encoding="utf-8")
    print(f"✓ {out}")
    print("  Open in browser: click a lock on the left, then click '确认此结构层 →'.")
    print("  The selection is auto-copied to clipboard — paste into Claude to continue.")


if __name__ == "__main__":
    main()
