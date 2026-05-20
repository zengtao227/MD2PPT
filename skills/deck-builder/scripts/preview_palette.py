#!/usr/bin/env python3
"""
Generate assets/palette-preview.html from assets/palettes.json.

Claude writes palettes.json during Step 4, then calls this script.
User opens the HTML, clicks a palette, hits confirm — selection is
auto-copied to clipboard.

palettes.json format:
[
  {
    "id": "A",
    "name": "深海科技",
    "bg":     "#0b1527",
    "text":   "#c8d5e8",
    "accent": "#5E6AD2",
    "muted":  "#7a8ba0",
    "font_zh": "思源黑体",
    "font_en": "Inter",
    "mood":   "工程感强、AI 科技、答辩专业",
    "lock":   "linear-dark"
  },
  ...
]
"""

import json
import sys
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>Step 4 — 配色方案预览</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: #eceae6;
  min-height: 100vh;
  padding: 28px 24px 48px;
  color: #1a1a1a;
}
h1 { font-size: 20px; font-weight: 700; color: #111; margin-bottom: 4px; }
.subtitle { font-size: 13px; color: #666; margin-bottom: 28px; line-height: 1.5; }

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.palette-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,.08), 0 2px 10px rgba(0,0,0,.05);
  cursor: pointer;
  transition: box-shadow .18s, transform .18s;
  user-select: none;
  border: 2px solid transparent;
}
.palette-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,.14);
  transform: translateY(-2px);
}
.palette-card.selected {
  border-color: #0061FF;
  box-shadow: 0 0 0 3px rgba(0,97,255,.15), 0 4px 20px rgba(0,0,0,.12);
  transform: translateY(-2px);
}

/* Mini slide preview */
.slide-preview {
  width: 100%;
  aspect-ratio: 16/9;
  overflow: hidden;
  position: relative;
}

/* Color swatches row */
.swatches {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background: #eee;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}
.swatch {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: white;
}
.swatch-dot {
  width: 22px;
  height: 22px;
  border-radius: 5px;
  flex-shrink: 0;
  border: 1px solid rgba(0,0,0,.08);
}
.swatch-info { min-width: 0; }
.swatch-role { font-size: 9px; color: #999; text-transform: uppercase; letter-spacing: .5px; }
.swatch-hex { font-size: 11px; font-weight: 600; color: #333; font-family: monospace; }

/* Meta section */
.meta { padding: 12px 14px 14px; }
.palette-id {
  display: inline-block;
  font-size: 10px; font-weight: 700;
  background: #f0f0ee; color: #555;
  padding: 2px 8px; border-radius: 12px;
  margin-bottom: 6px; letter-spacing: .5px;
}
.palette-name { font-size: 15px; font-weight: 700; color: #111; margin-bottom: 4px; }
.palette-font { font-size: 11px; color: #777; margin-bottom: 4px; }
.palette-mood {
  font-size: 11px; color: #444; line-height: 1.5;
  border-left: 2px solid #ddd; padding-left: 8px;
}
.lock-badge {
  display: inline-flex; align-items: center; gap: 5px;
  font-size: 10px; color: #0061FF; font-weight: 600;
  margin-top: 8px;
  background: #EEF3FF; padding: 3px 9px; border-radius: 12px;
}

.select-btn {
  display: block; width: calc(100% - 28px);
  margin: 0 14px 14px;
  padding: 9px;
  background: #f4f4f2; border: 1px solid #ddd;
  border-radius: 6px; font-size: 12px; font-weight: 600;
  color: #333; cursor: pointer; text-align: center;
  transition: background .12s;
}
.select-btn:hover { background: #eaeae8; }
.palette-card.selected .select-btn {
  background: #0061FF; color: white; border-color: #0061FF;
}

/* Bottom confirm area */
.confirm-area { display: flex; align-items: center; gap: 14px; margin-top: 8px; }
.confirm-btn {
  padding: 11px 28px; background: #0061FF; color: white;
  border: none; border-radius: 8px; font-size: 14px; font-weight: 700;
  cursor: pointer; transition: background .15s, transform .1s;
}
.confirm-btn:hover { background: #004ee0; transform: translateY(-1px); }
.confirm-btn.done { background: #16a34a; cursor: default; transform: none; }
.copied-msg {
  display: none; font-size: 13px; color: #16a34a; font-weight: 600;
  padding: 10px 14px; background: #f0fdf4; border-radius: 8px;
  border: 1px solid #bbf7d0; line-height: 1.5;
}
.copied-msg.show { display: block; }
</style>
</head>
<body>
<h1>Step 4 — 配色方案预览</h1>
<p class="subtitle">点击卡片选择配色方向，颜色均为真实渲染；确认后自动复制到剪贴板，粘贴给 Claude 继续 Step 5。</p>
<div class="grid" id="grid"></div>
<div class="confirm-area">
  <button class="confirm-btn" id="confirm-btn" onclick="confirmSelection()">确认此配色方案 →</button>
  <div class="copied-msg" id="copied-msg">
    ✓ 已复制到剪贴板！<br>粘贴到 Claude / Codex 对话框，然后继续 Step 5。
  </div>
</div>
<script>
const PALETTES = PALETTES_JSON;
let activeId = null;

function fontStack(zh, en) {
  const zhMap = {
    '思源黑体': "'Noto Sans SC'",
    '思源宋体': "'Noto Serif SC'",
    '黑体': "'Noto Sans SC'",
    '宋体': "'Noto Serif SC'",
  };
  return `${zhMap[zh] || "'Noto Sans SC'"}, '${en}', sans-serif`;
}

function buildSlide(p) {
  const fs = fontStack(p.font_zh, p.font_en);
  // Detect if background is dark
  const isDark = isDarkColor(p.bg);
  const cardBg = blendColor(p.bg, isDark ? '#ffffff' : '#000000', 0.08);
  return `
<div style="width:100%;height:100%;background:${p.bg};padding:14px 18px;display:flex;flex-direction:column;font-family:${fs};">
  <div style="width:28px;height:3px;background:${p.accent};margin-bottom:10px;"></div>
  <div style="font-size:8px;font-weight:700;color:${p.accent};letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;">SECTION 02</div>
  <div style="font-size:14px;font-weight:800;color:${p.text};line-height:1.25;margin-bottom:10px;">核心竞争力分析<br>市场份额提升 34%</div>
  <div style="height:1.5px;background:${p.accent};width:32px;margin-bottom:10px;opacity:.6;"></div>
  <div style="display:flex;gap:8px;flex:1;">
    <div style="flex:1;background:${cardBg};border-radius:3px;padding:8px;">
      <div style="font-size:7.5px;font-weight:700;color:${p.accent};margin-bottom:4px;">核心指标</div>
      <div style="font-size:7px;color:${p.text};line-height:1.6;opacity:.85;">增长率 +34%<br>市场份额 28%</div>
    </div>
    <div style="flex:1;background:${cardBg};border-radius:3px;padding:8px;">
      <div style="font-size:7.5px;font-weight:700;color:${p.accent};margin-bottom:4px;">趋势判断</div>
      <div style="font-size:7px;color:${p.text};line-height:1.6;opacity:.85;">持续上升<br>预计 Q4 加速</div>
    </div>
  </div>
  <div style="margin-top:8px;font-size:6.5px;color:${p.muted};display:flex;justify-content:space-between;">
    <span>来源：IDC 2024</span><span>03 / 12</span>
  </div>
</div>`;
}

function isDarkColor(hex) {
  const r = parseInt(hex.slice(1,3),16);
  const g = parseInt(hex.slice(3,5),16);
  const b = parseInt(hex.slice(5,7),16);
  return (r*299 + g*587 + b*114) / 1000 < 128;
}

function blendColor(hex, blend, amount) {
  const r1=parseInt(hex.slice(1,3),16), g1=parseInt(hex.slice(3,5),16), b1=parseInt(hex.slice(5,7),16);
  const r2=parseInt(blend.slice(1,3),16), g2=parseInt(blend.slice(3,5),16), b2=parseInt(blend.slice(5,7),16);
  const r=Math.round(r1*(1-amount)+r2*amount);
  const g=Math.round(g1*(1-amount)+g2*amount);
  const b=Math.round(b1*(1-amount)+b2*amount);
  return `rgb(${r},${g},${b})`;
}

function render() {
  document.getElementById('grid').innerHTML = PALETTES.map(p => `
    <div class="palette-card ${p.id === activeId ? 'selected' : ''}"
         data-id="${p.id}" onclick="selectPalette('${p.id}')">
      <div class="slide-preview">${buildSlide(p)}</div>
      <div class="swatches">
        <div class="swatch">
          <div class="swatch-dot" style="background:${p.bg}"></div>
          <div class="swatch-info">
            <div class="swatch-role">背景</div>
            <div class="swatch-hex">${p.bg}</div>
          </div>
        </div>
        <div class="swatch">
          <div class="swatch-dot" style="background:${p.text}"></div>
          <div class="swatch-info">
            <div class="swatch-role">正文</div>
            <div class="swatch-hex">${p.text}</div>
          </div>
        </div>
        <div class="swatch">
          <div class="swatch-dot" style="background:${p.accent}"></div>
          <div class="swatch-info">
            <div class="swatch-role">强调色</div>
            <div class="swatch-hex">${p.accent}</div>
          </div>
        </div>
        <div class="swatch">
          <div class="swatch-dot" style="background:${p.muted}"></div>
          <div class="swatch-info">
            <div class="swatch-role">辅助色</div>
            <div class="swatch-hex">${p.muted}</div>
          </div>
        </div>
      </div>
      <div class="meta">
        <div class="palette-id">方案 ${p.id}</div>
        <div class="palette-name">${p.name}</div>
        <div class="palette-font">字体：${p.font_zh} + ${p.font_en}</div>
        <div class="palette-mood">${p.mood}</div>
        <div class="lock-badge">→ 推荐结构层：${p.lock}</div>
      </div>
      <button class="select-btn"
              onclick="event.stopPropagation(); selectPalette('${p.id}')">
        ${p.id === activeId ? '✓ 已选择' : '选择此配色'}
      </button>
    </div>`).join('');
}

function selectPalette(id) {
  activeId = id;
  render();
  document.getElementById('confirm-btn').textContent = '确认此配色方案 →';
  document.getElementById('confirm-btn').classList.remove('done');
  document.getElementById('copied-msg').classList.remove('show');
}

function confirmSelection() {
  if (!activeId) {
    alert('请先点击选择一个配色方案');
    return;
  }
  const p = PALETTES.find(x => x.id === activeId);
  const text = `我选择方案 ${p.id} — ${p.name}`;
  navigator.clipboard.writeText(text).then(() => {
    document.getElementById('confirm-btn').textContent = '✓ 已确认';
    document.getElementById('confirm-btn').classList.add('done');
    document.getElementById('copied-msg').classList.add('show');
  }).catch(() => {
    document.getElementById('copied-msg').innerHTML =
      `请手动复制粘贴到 Claude：<br><strong>${text}</strong>`;
    document.getElementById('copied-msg').classList.add('show');
  });
}

render();
</script>
</body>
</html>"""


def main() -> None:
    repo_root = Path(__file__).parent.parent
    assets_dir = repo_root / "assets"
    palette_json = assets_dir / "palettes.json"

    if not palette_json.exists():
        print(f"✗ 找不到 {palette_json}")
        print("  Claude 需要先把配色方案写入 assets/palettes.json，再运行此脚本。")
        sys.exit(1)

    palettes = json.loads(palette_json.read_text(encoding="utf-8"))
    if not isinstance(palettes, list) or not palettes:
        print("✗ palettes.json 格式错误，应为非空数组。")
        sys.exit(1)

    out = assets_dir / "palette-preview.html"
    html = HTML_TEMPLATE.replace("PALETTES_JSON", json.dumps(palettes, ensure_ascii=False))
    out.write_text(html, encoding="utf-8")
    print(f"✓ {out}")
    print("  在浏览器中打开，点击选择配色方案后确认，选择自动复制到剪贴板。")


if __name__ == "__main__":
    main()
