#!/usr/bin/env python3
"""
Generate assets/locks-preview.html — visual comparison of all design-locks.

Usage:
    python3 scripts/preview_locks.py
    # then open: assets/locks-preview.html
"""

import os
from pathlib import Path

LOCKS = [
    {
        "id": "swiss-klein-blue",
        "name": "Swiss · Klein Blue",
        "zh": "瑞士国际主义",
        "bg": "#fafaf8",
        "card": "#f0f0ee",
        "text": "#0a0a0a",
        "text_muted": "#6b6b6b",
        "accent": "#002FA7",
        "accent_text": "#ffffff",
        "font_zh": "Source Han Sans",
        "font_en": "Inter",
        "tone": "权威 · 精准 · 高对比",
        "density": "中",
        "suitable": ["商业计划", "产品路线图", "投资人演示", "执行报告"],
        "avoid": ["文化类", "叙事性演示"],
    },
    {
        "id": "linear-dark",
        "name": "Linear Dark",
        "zh": "工程深色",
        "bg": "#08090a",
        "card": "#0f1011",
        "text": "#f7f8f8",
        "text_muted": "#8a8f98",
        "accent": "#5e6ad2",
        "accent_text": "#ffffff",
        "font_zh": "Source Han Sans",
        "font_en": "Inter",
        "tone": "工程精密 · 现代科技 · 暗色",
        "density": "中高",
        "suitable": ["SaaS 产品", "技术平台", "工程演示", "投资人（技术背景）"],
        "avoid": ["教学类", "文化类", "非技术商务场合"],
    },
    {
        "id": "guizang-indigo",
        "name": "Guizang Indigo",
        "zh": "归藏靛蓝瓷",
        "bg": "#f1f3f5",
        "card": "#e4e8ec",
        "text": "#0a1f3d",
        "text_muted": "#4a6080",
        "accent": "#0a1f3d",
        "accent_text": "#f1f3f5",
        "font_zh": "Source Han Serif",
        "font_en": "IBM Plex Sans",
        "tone": "学术 · 冷调 · 信息密度高",
        "density": "高",
        "suitable": ["技术方案", "数据报告", "AI/ML 项目", "竞赛答辩"],
        "avoid": ["温暖叙事类", "消费品牌类"],
    },
    {
        "id": "guizang-monocle",
        "name": "Guizang Monocle",
        "zh": "归藏墨水经典",
        "bg": "#f1efea",
        "card": "#e8e5de",
        "text": "#0a0a0b",
        "text_muted": "#5a5650",
        "accent": "#0a0a0b",
        "accent_text": "#f1efea",
        "font_zh": "Source Han Serif",
        "font_en": "Spectral",
        "tone": "叙事 · 温暖纸感 · 编辑感",
        "density": "中",
        "suitable": ["路演", "课程汇报", "观点类演示", "项目方案"],
        "avoid": ["纯工程类", "数据密集报告"],
    },
    {
        "id": "notion-warm",
        "name": "Notion Warm",
        "zh": "Notion 暖白",
        "bg": "#ffffff",
        "card": "#f6f5f4",
        "text": "#0d0d0d",
        "text_muted": "#615d59",
        "accent": "#37352f",
        "accent_text": "#ffffff",
        "font_zh": "Source Han Sans",
        "font_en": "Inter",
        "tone": "亲和 · 极简 · 文档感",
        "density": "低",
        "suitable": ["内部汇报", "文化类", "课程讲义", "轻量演示"],
        "avoid": ["投资人演示", "高强度外部场合"],
    },
]

CARD_HTML = """
<div class="lock-card" onclick="select('{id}')">
  <div class="slide-mock" style="background:{bg}; border: 1px solid {card};">
    <div class="slide-header" style="background:{accent}; color:{accent_text};">
      <span class="slide-title">{name}</span>
      <span class="slide-sub">{zh}</span>
    </div>
    <div class="slide-body" style="color:{text};">
      <div class="body-line" style="background:{text}; opacity:0.8; width:72%; height:8px; border-radius:2px; margin-bottom:8px;"></div>
      <div class="body-line" style="background:{text_muted}; opacity:0.5; width:55%; height:6px; border-radius:2px; margin-bottom:5px;"></div>
      <div class="body-line" style="background:{text_muted}; opacity:0.4; width:63%; height:6px; border-radius:2px; margin-bottom:14px;"></div>
      <div style="display:flex; gap:6px;">
        <div style="flex:1; background:{card}; border-radius:3px; height:36px;"></div>
        <div style="flex:1; background:{card}; border-radius:3px; height:36px;"></div>
        <div style="flex:1; background:{card}; border-radius:3px; height:36px;"></div>
      </div>
    </div>
    <div class="slide-footer" style="color:{text_muted};">
      <span style="font-family:monospace; font-size:9px;">{font_zh} + {font_en}</span>
      <span style="font-size:9px;">密度 {density}</span>
    </div>
  </div>
  <div class="swatches">
    <div class="swatch" style="background:{bg}; border:1px solid #ccc;" title="背景 {bg}"></div>
    <div class="swatch" style="background:{text};" title="正文 {text}"></div>
    <div class="swatch" style="background:{accent};" title="强调 {accent}"></div>
    <div class="swatch" style="background:{card}; border:1px solid #ccc;" title="卡片 {card}"></div>
    <div class="swatch" style="background:{text_muted};" title="辅助 {text_muted}"></div>
  </div>
  <div class="meta">
    <div class="tone">{tone}</div>
    <div class="tags">
      {''.join(f'<span class="tag suitable">{s}</span>' for s in suitable)}
    </div>
    <div class="tags" style="margin-top:4px;">
      {''.join(f'<span class="tag avoid">✗ {a}</span>' for a in avoid)}
    </div>
  </div>
</div>
"""

HTML = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Design Locks — Visual Preview</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f2f2f0;
    padding: 32px 24px;
    color: #1a1a1a;
  }}
  h1 {{
    font-size: 18px; font-weight: 600; margin-bottom: 6px;
  }}
  .subtitle {{
    font-size: 13px; color: #666; margin-bottom: 28px;
  }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 20px;
  }}
  .lock-card {{
    background: white;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,.08);
    overflow: hidden;
    cursor: pointer;
    transition: box-shadow .15s, transform .15s;
  }}
  .lock-card:hover {{ box-shadow: 0 4px 16px rgba(0,0,0,.14); transform: translateY(-2px); }}
  .lock-card.selected {{ box-shadow: 0 0 0 3px #007AFF, 0 4px 16px rgba(0,0,0,.12); transform: translateY(-2px); }}

  .slide-mock {{
    width: 100%;
    aspect-ratio: 16/9;
    display: flex;
    flex-direction: column;
    border-radius: 6px 6px 0 0;
    overflow: hidden;
  }}
  .slide-header {{
    padding: 10px 12px 8px;
    display: flex;
    flex-direction: column;
    gap: 2px;
  }}
  .slide-title {{ font-size: 12px; font-weight: 700; letter-spacing: .3px; }}
  .slide-sub {{ font-size: 9px; opacity: .75; }}
  .slide-body {{ flex: 1; padding: 10px 12px; }}
  .slide-footer {{
    display: flex;
    justify-content: space-between;
    padding: 5px 10px;
    border-top: 1px solid rgba(128,128,128,.12);
    background: rgba(255,255,255,.05);
  }}

  .swatches {{
    display: flex;
    gap: 4px;
    padding: 8px 10px;
    background: #fafafa;
    border-top: 1px solid #eee;
  }}
  .swatch {{
    width: 20px; height: 20px;
    border-radius: 4px;
    flex-shrink: 0;
  }}

  .meta {{ padding: 10px 12px 14px; }}
  .tone {{ font-size: 11px; color: #444; margin-bottom: 7px; font-style: italic; }}
  .tags {{ display: flex; flex-wrap: wrap; gap: 4px; }}
  .tag {{
    font-size: 10px; padding: 2px 7px;
    border-radius: 99px;
    line-height: 1.5;
  }}
  .tag.suitable {{ background: #e8f4fd; color: #0969a2; }}
  .tag.avoid {{ background: #fdf0f0; color: #c0392b; }}

  #selection-bar {{
    display: none;
    margin-top: 28px;
    padding: 16px 20px;
    background: #007AFF;
    color: white;
    border-radius: 10px;
    font-size: 14px;
  }}
  #selection-bar code {{
    background: rgba(255,255,255,.2);
    padding: 2px 8px; border-radius: 4px;
    font-family: monospace;
  }}
</style>
</head>
<body>
<h1>Design Locks — 结构层预览</h1>
<p class="subtitle">点击选择一个结构层 lock。颜色层已在 Step 4 确认，此处颜色仅供参考结构风格。</p>
<div class="grid">
{cards}
</div>
<div id="selection-bar">
  已选择：<code id="sel-name"></code> — 告诉 Claude "<b>选 <span id="sel-id"></span></b>" 继续下一步。
</div>
<script>
function select(id) {{
  document.querySelectorAll('.lock-card').forEach(c => c.classList.remove('selected'));
  const card = document.querySelector(`[onclick="select('${{id}}')"]`);
  card.classList.add('selected');
  const bar = document.getElementById('selection-bar');
  bar.style.display = 'block';
  document.getElementById('sel-name').textContent = card.querySelector('.slide-title').textContent;
  document.getElementById('sel-id').textContent = id;
}}
</script>
</body>
</html>
"""

def render_card(lock):
    suitable_tags = "".join(f'<span class="tag suitable">{s}</span>' for s in lock["suitable"])
    avoid_tags = "".join(f'<span class="tag avoid">✗ {a}</span>' for a in lock["avoid"])
    return f"""
<div class="lock-card" onclick="select('{lock["id"]}')">
  <div class="slide-mock" style="background:{lock['bg']};">
    <div class="slide-header" style="background:{lock['accent']}; color:{lock['accent_text']};">
      <span class="slide-title">{lock['name']}</span>
      <span class="slide-sub">{lock['zh']}</span>
    </div>
    <div class="slide-body" style="color:{lock['text']};">
      <div style="background:{lock['text']}; opacity:0.8; width:72%; height:8px; border-radius:2px; margin-bottom:8px;"></div>
      <div style="background:{lock['text_muted']}; opacity:0.5; width:55%; height:6px; border-radius:2px; margin-bottom:5px;"></div>
      <div style="background:{lock['text_muted']}; opacity:0.4; width:63%; height:6px; border-radius:2px; margin-bottom:14px;"></div>
      <div style="display:flex; gap:6px;">
        <div style="flex:1; background:{lock['card']}; border-radius:3px; height:36px;"></div>
        <div style="flex:1; background:{lock['card']}; border-radius:3px; height:36px;"></div>
        <div style="flex:1; background:{lock['card']}; border-radius:3px; height:36px;"></div>
      </div>
    </div>
    <div class="slide-footer" style="color:{lock['text_muted']}; font-size:9px; display:flex; justify-content:space-between; padding:5px 10px; border-top:1px solid rgba(128,128,128,.15);">
      <span style="font-family:monospace;">{lock['font_zh']} + {lock['font_en']}</span>
      <span>密度 {lock['density']}</span>
    </div>
  </div>
  <div class="swatches">
    <div class="swatch" style="background:{lock['bg']}; border:1px solid #ccc;" title="背景 {lock['bg']}"></div>
    <div class="swatch" style="background:{lock['text']};" title="正文 {lock['text']}"></div>
    <div class="swatch" style="background:{lock['accent']};" title="强调 {lock['accent']}"></div>
    <div class="swatch" style="background:{lock['card']}; border:1px solid #ccc;" title="卡片 {lock['card']}"></div>
    <div class="swatch" style="background:{lock['text_muted']};" title="辅助 {lock['text_muted']}"></div>
  </div>
  <div class="meta">
    <div class="tone">{lock['tone']}</div>
    <div class="tags">{suitable_tags}</div>
    <div class="tags" style="margin-top:4px;">{avoid_tags}</div>
  </div>
</div>"""


def main():
    repo_root = Path(__file__).parent.parent
    assets_dir = repo_root / "assets"
    assets_dir.mkdir(exist_ok=True)
    out = assets_dir / "locks-preview.html"

    cards = "\n".join(render_card(lock) for lock in LOCKS)
    html = HTML.format(cards=cards)
    out.write_text(html, encoding="utf-8")
    print(f"✓ {out}")
    print("  Open in browser to compare design-locks visually.")
    print("  Click a card to select it — the page shows the lock ID to confirm with Claude.")


if __name__ == "__main__":
    main()
