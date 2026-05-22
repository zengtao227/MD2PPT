#!/usr/bin/env python3
"""Local Presentation Director UI for Codex + Presentations workflows.

This script does not generate PPTX files. It creates a small local UI for:
1. intake choices before generation,
2. brief confirmation before calling Presentations,
3. visual revision choices after v1,
4. final version selection.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import sys
import time
import webbrowser
from dataclasses import dataclass
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse


JsonDict = dict[str, Any]

DEFAULT_PORT: int = 8765
DEFAULT_HOST: str = "127.0.0.1"
STATUS_FILES: dict[str, str] = {
    "confirmed": "confirmed.ready",
    "revision": "revision.ready",
    "final-selection": "final-selected.ready",
}
PAGE_PATHS: dict[str, str] = {
    "intake": "/intake",
    "confirm": "/confirm",
    "style-review": "/style-review",
    "compare": "/compare",
}


@dataclass(frozen=True)
class Choice:
    value: str
    label: str
    description: str


@dataclass(frozen=True)
class Question:
    key: str
    title: str
    prompt: str
    choices: tuple[Choice, ...]
    default: str


INTAKE_QUESTIONS: tuple[Question, ...] = (
    Question(
        key="deck_type",
        title="PPT 类型",
        prompt="你要做哪类 PPT?",
        default="engineering-platform",
        choices=(
            Choice("project-report", "项目汇报", "说明进展、结果、风险和下一步。"),
            Choice("engineering-platform", "工程 / 技术方案介绍", "解释系统价值、架构和实现路径。"),
            Choice("investor-pitch", "投资人 / 路演 deck", "突出机会、增长、证明和决策请求。"),
            Choice("knowledge-teaching", "学术 / 课程 / 知识讲解", "把复杂材料重组成清晰知识结构。"),
            Choice("sales-product", "客户销售 / 产品介绍", "展示痛点、方案、demo 和价值证明。"),
            Choice("custom", "自定义", "我有自己的类型描述。"),
        ),
    ),
    Question(
        key="audience",
        title="听众",
        prompt="这份 PPT 主要给谁看?",
        default="technical-leaders",
        choices=(
            Choice("executives", "高层 / 老板 / 决策者", "更重结论、风险和决策请求。"),
            Choice("investors-reviewers", "投资人 / 评委 / 路演对象", "更重可信证明、市场和增长叙事。"),
            Choice("technical-leaders", "技术团队 / 工程评审", "更重架构、实现、指标和 tradeoff。"),
            Choice("customers-sales", "客户 / 销售对象", "更重痛点、方案、案例和转化。"),
            Choice("teachers-researchers", "学生 / 老师 / 研究者", "更重解释、引用和知识结构。"),
            Choice("custom", "自定义", "我有自己的听众描述。"),
        ),
    ),
    Question(
        key="goal",
        title="目标",
        prompt="这份 PPT 的主要目标是什么?",
        default="explain-value",
        choices=(
            Choice("understand-topic", "让对方快速理解一个主题", "强调清晰解释和结构化。"),
            Choice("decision", "说服对方做决定", "强调证据、取舍和行动请求。"),
            Choice("progress-risk", "汇报进展、成果和风险", "强调状态、指标、风险和下一步。"),
            Choice("teaching", "教学讲解 / 知识传达", "强调概念、例子和学习路径。"),
            Choice("explain-value", "展示产品 / 项目价值", "强调问题、方案、价值和证明。"),
            Choice("custom", "自定义", "我有自己的目标描述。"),
        ),
    ),
    Question(
        key="source_boundary",
        title="资料边界",
        prompt="资料应该怎么使用?",
        default="provided-only",
        choices=(
            Choice("provided-only", "严格只用我提供的材料", "缺失信息必须标注，不联网补全。"),
            Choice("web-with-sources", "可以联网补充，但必须标注来源", "适合需要最新资料或外部事实。"),
            Choice("existing-doc", "以已有 PPT / 文档为内容基础", "继承已有内容结构并改进表达。"),
            Choice("reference-quality", "以参考 deck 作为质量和风格标杆", "参考是质量 bar，不盲目复制。"),
            Choice("custom", "自定义", "我有自己的资料使用规则。"),
        ),
    ),
    Question(
        key="output_constraints",
        title="输出限制",
        prompt="输出限制是什么?",
        default="zh-10-12",
        choices=(
            Choice("zh-10-12", "中文，10-12 页，适合 10-15 分钟演讲", "默认推荐。"),
            Choice("zh-15-20", "中文，15-20 页，适合详细汇报", "适合内部评审或长汇报。"),
            Choice("en-10-12", "英文，10-12 页", "适合英文演示。"),
            Choice("bilingual-flex", "中英双语，页数由内容决定", "适合跨语言材料。"),
            Choice("custom", "自定义", "我有自己的页数、语言或格式要求。"),
        ),
    ),
    Question(
        key="logo_policy",
        title="Logo / 品牌素材",
        prompt="Logo 和品牌素材怎么处理?",
        default="provided-only",
        choices=(
            Choice("none", "不使用 logo", "避免品牌资产风险。"),
            Choice("provided-only", "只使用我提供的 logo / 图片", "最安全。"),
            Choice("official-sources", "可以查找官方 logo 和官方素材", "需要记录来源。"),
            Choice("cover-final-only", "只在封面和结束页使用 logo", "弱品牌露出。"),
            Choice("custom", "自定义", "我有自己的品牌素材规则。"),
        ),
    ),
    Question(
        key="image_policy",
        title="AI 生图",
        prompt="是否允许使用 AI 生图?",
        default="ask-before-use",
        choices=(
            Choice("none", "不使用 AI 生成图片", "只用文字、图表、真实素材。"),
            Choice("abstract-only", "只允许生成抽象背景 / 概念图", "不伪造真实对象。"),
            Choice("cover-section", "允许生成封面和章节图", "用于增强视觉表现。"),
            Choice("ask-before-use", "每次生图前先问我", "默认安全策略。"),
            Choice("custom", "自定义", "我有自己的图片策略。"),
        ),
    ),
    Question(
        key="visual_freedom",
        title="第一版视觉方向",
        prompt="第一版视觉方向怎么处理?",
        default="delegate",
        choices=(
            Choice("delegate", "交给 Presentations 自由发挥", "最大化插件表现力。"),
            Choice("restrained", "更正式克制", "适合严肃汇报。"),
            Choice("technical", "更科技 / 工程感", "适合技术方案和架构解释。"),
            Choice("investor", "更投资人路演 / 高对比", "适合 pitch 或评审。"),
            Choice("academic-editorial", "更学术 / 编辑风", "适合知识讲解和研究。"),
            Choice("custom", "自定义", "我有自己的视觉方向。"),
        ),
    ),
    Question(
        key="reference_deck",
        title="参考 deck",
        prompt="是否有参考 deck 或风格样张?",
        default="none",
        choices=(
            Choice("none", "没有参考，按内容生成", "由 Presentations 自主设计。"),
            Choice("quality-only", "有参考，但只作为质量标杆", "beat reference, do not clone。"),
            Choice("visual-style", "有参考，需要接近其视觉风格", "继承风格但不盲目复制。"),
            Choice("existing-ppt", "有已有 PPT，需要在它基础上改", "作为 source/template。"),
            Choice("custom", "自定义", "我有自己的参考使用规则。"),
        ),
    ),
)

REVISION_GROUPS: tuple[Question, ...] = (
    Question(
        key="palette_direction",
        title="配色方向",
        prompt="是否要改变配色方向?",
        default="keep",
        choices=(
            Choice("keep", "保持当前", "不改 v1 配色。"),
            Choice("warm-editorial", "暖色纸感 / 编辑风", "更像高质量长文和研究报告。"),
            Choice("engineering-blue-gray", "工程蓝灰 / 技术风", "更冷静、系统、技术。"),
            Choice("high-contrast-pitch", "高对比 / 路演风", "更强冲击力。"),
            Choice("brand-boost", "强化品牌色", "更明显使用品牌色。"),
            Choice("custom", "自定义", "我有自己的配色方向。"),
        ),
    ),
    Question(
        key="structure_direction",
        title="结构节奏",
        prompt="是否要改变结构节奏?",
        default="keep",
        choices=(
            Choice("keep", "保持当前", "不改整体节奏。"),
            Choice("stronger-story", "更强故事节奏", "章节推进更明显。"),
            Choice("more-analytical", "更数据分析", "更多 evidence-led 页面。"),
            Choice("more-architecture", "更架构 / 系统图", "强化系统图和流程图。"),
            Choice("more-product-demo", "更产品发布 / demo 感", "更像产品展示。"),
            Choice("denser-internal", "更高密度内部汇报", "更适合内部评审。"),
            Choice("custom", "自定义", "我有自己的结构方向。"),
        ),
    ),
    Question(
        key="visual_expression",
        title="视觉表现力",
        prompt="是否要改变视觉表现力?",
        default="keep",
        choices=(
            Choice("keep", "保持当前", "不改表现力。"),
            Choice("more-premium", "更高级 / 更有设计感", "提高整体 polished 感。"),
            Choice("more-restrained", "更克制 / 更少装饰", "减少视觉噪音。"),
            Choice("less-cards", "更少卡片，更开放构图", "避免 generic SaaS card grid。"),
            Choice("stronger-evidence", "更强图表和 evidence-led storytelling", "让证据更直接证明标题。"),
            Choice("custom", "自定义", "我有自己的表现力要求。"),
        ),
    ),
    Question(
        key="image_strategy",
        title="图片策略",
        prompt="图片和视觉素材怎么调整?",
        default="keep",
        choices=(
            Choice("keep", "保持当前", "不改图片策略。"),
            Choice("fewer-decorative", "减少装饰图", "更依赖图表和文字。"),
            Choice("more-ai-concept", "增加 AI 概念图", "只用于已授权场景。"),
            Choice("official-only", "只用真实截图 / 官方素材", "避免 AI 和不明来源素材。"),
            Choice("stronger-cover-section", "增强封面或章节视觉", "提升第一印象。"),
            Choice("custom", "自定义", "我有自己的图片策略。"),
        ),
    ),
    Question(
        key="logo_strategy",
        title="Logo / 品牌露出",
        prompt="Logo 和品牌露出怎么调整?",
        default="keep",
        choices=(
            Choice("keep", "保持当前", "不改品牌露出。"),
            Choice("cover-final-only", "只保留封面和结束页", "降低干扰。"),
            Choice("footer-brand", "增强页脚品牌感", "每页轻品牌提示。"),
            Choice("partner-logo-page", "增加合作方 / 学校 / 企业 logo 页", "适合展示生态或背书。"),
            Choice("remove-all", "移除所有 logo", "避免品牌资产风险。"),
            Choice("custom", "自定义", "我有自己的品牌策略。"),
        ),
    ),
)


def slugify(value: str) -> str:
    cleaned: str = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip().lower()).strip("-")
    if cleaned:
        return cleaned[:80]
    return f"presentation-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


def now_id() -> str:
    return datetime.now().strftime("manual-%Y%m%d-%H%M%S")


def workspace_root(base_dir: Path, thread_id: str, task_slug: str) -> Path:
    # `thread_id` is kept for command compatibility. User-facing PPT assets
    # should live together under one project-local folder.
    return base_dir / "PPTX" / task_slug


def status_dir(task_dir: Path) -> Path:
    return task_dir / "status"


def read_json(path: Path, default: JsonDict | None = None) -> JsonDict:
    if not path.exists():
        return {} if default is None else default
    with path.open("r", encoding="utf-8") as handle:
        value: Any = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"Expected object JSON at {path}")
    return value


def write_json(path: Path, data: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def touch_status(task_dir: Path, status_name: str) -> Path:
    filename: str | None = STATUS_FILES.get(status_name)
    if filename is None:
        raise ValueError(f"Unknown status: {status_name}")
    path: Path = status_dir(task_dir) / filename
    write_text(path, datetime.now().isoformat(timespec="seconds") + "\n")
    return path


def selected_choice(question: Question, value: str) -> Choice:
    for choice in question.choices:
        if choice.value == value:
            return choice
    return next(choice for choice in question.choices if choice.value == question.default)


def html_page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --bg: #f7f4ee;
      --panel: #ffffff;
      --ink: #161616;
      --muted: #626262;
      --line: #d8d2c7;
      --accent: #274c77;
      --accent-2: #c75000;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif;
      line-height: 1.5;
    }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 40px 24px 72px; }}
    h1 {{ font-size: 32px; margin: 0 0 8px; letter-spacing: 0; }}
    h2 {{ font-size: 22px; margin: 28px 0 12px; }}
    h3 {{ font-size: 17px; margin: 0 0 8px; }}
    p {{ color: var(--muted); margin: 0 0 16px; }}
    .topline {{ text-transform: uppercase; letter-spacing: .08em; color: var(--accent-2); font-size: 12px; font-weight: 700; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }}
    .card, .section {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
      box-shadow: 0 1px 0 rgba(0,0,0,.03);
    }}
    .section {{ margin-top: 18px; }}
    label.option {{
      display: block;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      cursor: pointer;
      background: #fff;
      min-height: 112px;
    }}
    label.option:has(input:checked) {{
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(39, 76, 119, .16);
    }}
    input[type="radio"] {{ margin-right: 8px; }}
    input[type="text"], textarea {{
      width: 100%;
      margin-top: 8px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      font: inherit;
    }}
    textarea {{ min-height: 88px; resize: vertical; }}
    .actions {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 28px; }}
    button, .button {{
      appearance: none;
      border: 0;
      background: var(--accent);
      color: #fff;
      padding: 12px 18px;
      border-radius: 6px;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      display: inline-block;
    }}
    button.secondary, .button.secondary {{ background: #545454; }}
    button.warning {{ background: var(--accent-2); }}
    .meta {{ color: var(--muted); font-size: 13px; }}
    .source-tag {{ display: inline-block; padding: 2px 7px; border-radius: 999px; background: #ebe3d5; font-size: 12px; color: #554; }}
    .risk {{ border-left: 4px solid var(--accent-2); padding-left: 12px; }}
    .contact-sheet {{
      width: 100%;
      max-height: 520px;
      object-fit: contain;
      border: 1px solid var(--line);
      background: #eee;
      border-radius: 8px;
    }}
    code {{ background: #eee7da; padding: 2px 5px; border-radius: 4px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--panel); }}
    th, td {{ border: 1px solid var(--line); padding: 10px; text-align: left; vertical-align: top; }}
    th {{ background: #efe8dc; }}
  </style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def question_section(question: Question, current: str = "") -> str:
    current_value: str = current or question.default
    cards: list[str] = []
    for choice in question.choices:
        checked: str = " checked" if choice.value == current_value else ""
        custom_input: str = ""
        if choice.value == "custom":
            custom_input = (
                f'<input type="text" name="{question.key}__custom" '
                f'placeholder="输入你的自定义说明">'
            )
        cards.append(
            f"""<label class="option">
  <input type="radio" name="{question.key}" value="{html.escape(choice.value)}"{checked}>
  <strong>{html.escape(choice.label)}</strong>
  <p>{html.escape(choice.description)}</p>
  {custom_input}
</label>"""
        )
    return f"""<section class="section">
  <h2>{html.escape(question.title)}</h2>
  <p>{html.escape(question.prompt)}</p>
  <div class="grid">
    {''.join(cards)}
  </div>
</section>"""


def build_draft_brief(task_slug: str, topic: str, sources: list[str]) -> JsonDict:
    source_items: list[JsonDict] = [
        {"path": source, "priority": "primary", "type": infer_source_type(source)}
        for source in sources
    ]
    return {
        "version": "0.1",
        "task_slug": task_slug,
        "topic": topic or task_slug.replace("-", " "),
        "sources": source_items,
        "selections": {
            question.key: {
                "value": question.default,
                "label": selected_choice(question, question.default).label,
                "source": "default",
            }
            for question in INTAKE_QUESTIONS
        },
        "risks": infer_risks(source_items),
        "confirmed": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def infer_source_type(source: str) -> str:
    if re.match(r"https?://", source):
        return "url"
    path: Path = Path(source).expanduser()
    if path.is_dir():
        return "folder"
    suffix: str = path.suffix.lower().lstrip(".")
    return suffix or "text"


def infer_risks(sources: list[JsonDict]) -> list[str]:
    risks: list[str] = []
    source_text: str = " ".join(str(item.get("path", "")) for item in sources).lower()
    if "logo" not in source_text:
        risks.append("未发现明确 logo 文件；如需使用 logo，必须由用户提供或使用官方来源。")
    if not any(token in source_text for token in ("metric", "data", "csv", "xlsx", "指标", "数据")):
        risks.append("未发现明确量化数据文件；第一版可能需要用定性证明或标注缺失指标。")
    if not sources:
        risks.append("未提供具体资料路径；需要在生成前补充 source material。")
    return risks


def apply_intake_selection(draft: JsonDict, form: dict[str, list[str]]) -> JsonDict:
    selections: JsonDict = {}
    for question in INTAKE_QUESTIONS:
        value: str = first_form_value(form, question.key, question.default)
        choice: Choice = selected_choice(question, value)
        custom: str = first_form_value(form, f"{question.key}__custom", "").strip()
        selections[question.key] = {
            "value": value,
            "label": custom if value == "custom" and custom else choice.label,
            "source": "user-selected",
            "description": choice.description,
        }
        if custom:
            selections[question.key]["custom"] = custom

    brief: JsonDict = dict(draft)
    brief["selections"] = selections
    brief["updated_at"] = datetime.now().isoformat(timespec="seconds")
    brief["confirmed"] = False
    return brief


def first_form_value(form: dict[str, list[str]], key: str, default: str) -> str:
    values: list[str] | None = form.get(key)
    if not values:
        return default
    return values[0]


def render_intake(task_dir: Path) -> str:
    draft: JsonDict = read_json(task_dir / "brief-draft.json")
    current: JsonDict = read_json(task_dir / "intake-selection.json", draft)
    selections: JsonDict = current.get("selections", {})
    source_list: str = render_sources(draft.get("sources", []))
    body: str = f"""<div class="topline">Presentation Director</div>
<h1>生成前信息收集</h1>
<p>先确认会影响 PPTX 质量的关键信息。每题都有默认推荐，也可以选择自定义。</p>
<section class="section">
  <h2>资料来源</h2>
  {source_list}
  <label>主题 / 标题
    <input type="text" name="topic" form="intake-form" value="{html.escape(str(draft.get("topic", "")))}">
  </label>
</section>
<form method="post" action="/api/intake" id="intake-form">
  {''.join(question_section(question, selections.get(question.key, {}).get("value", "")) for question in INTAKE_QUESTIONS)}
  <section class="section">
    <h2>额外说明</h2>
    <textarea name="notes" placeholder="例如必须保留的页面、禁用内容、特殊听众背景。">{html.escape(str(current.get("notes", "")))}</textarea>
  </section>
  <div class="actions">
    <button type="submit">下一步：汇总确认</button>
  </div>
</form>"""
    return html_page("Presentation Director Intake", body)


def render_sources(sources: Any) -> str:
    if not isinstance(sources, list) or not sources:
        return "<p class='risk'>未记录资料来源。请在启动脚本时用 <code>--source</code> 传入。</p>"
    items: list[str] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        path: str = str(source.get("path", ""))
        source_type: str = str(source.get("type", "unknown"))
        items.append(f"<li><code>{html.escape(path)}</code> <span class='source-tag'>{html.escape(source_type)}</span></li>")
    return f"<ul>{''.join(items)}</ul>"


def render_confirm(task_dir: Path) -> str:
    draft: JsonDict = read_json(task_dir / "brief-draft.json")
    selected: JsonDict = read_json(task_dir / "intake-selection.json", draft)
    rows: list[str] = []
    selections: JsonDict = selected.get("selections", {})
    for question in INTAKE_QUESTIONS:
        item: JsonDict = selections.get(question.key, {})
        rows.append(
            "<tr>"
            f"<th>{html.escape(question.title)}</th>"
            f"<td>{html.escape(str(item.get('label', '')))}</td>"
            f"<td><span class='source-tag'>{html.escape(str(item.get('source', 'unknown')))}</span></td>"
            "</tr>"
        )
    risks: list[str] = selected.get("risks", draft.get("risks", []))
    risk_html: str = "".join(f"<li>{html.escape(str(risk))}</li>" for risk in risks) or "<li>未发现明显风险。</li>"
    body: str = f"""<div class="topline">Brief Confirmation Gate</div>
<h1>确认生成简报</h1>
<p>请最后确认一次。只有点击“确认并开始生成”后，agent 才应调用 Codex Presentations plugin。</p>
<section class="section">
  <h2>主题</h2>
  <p><strong>{html.escape(str(selected.get("topic", draft.get("topic", ""))))}</strong></p>
</section>
<section class="section">
  <h2>资料来源</h2>
  {render_sources(selected.get("sources", draft.get("sources", [])))}
</section>
<section class="section">
  <h2>选择汇总</h2>
  <table>
    <thead><tr><th>项目</th><th>选择</th><th>来源</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
</section>
<section class="section">
  <h2>生成前风险</h2>
  <ul>{risk_html}</ul>
</section>
<section class="section">
  <h2>生成策略</h2>
  <p>先生成 v1 PPTX 和 contact sheet，并集中保存到 <code>{html.escape(str(task_dir))}</code>，然后打开 style-review.html 供选择是否重绘。</p>
</section>
<form method="post" action="/api/confirm">
  <div class="actions">
    <a class="button secondary" href="/intake">返回修改</a>
    <button type="submit">确认并开始生成</button>
  </div>
</form>"""
    return html_page("Presentation Director Confirm", body)


def render_style_review(task_dir: Path) -> str:
    contact_sheet: Path = task_dir / "v1" / "contact-sheet.png"
    qa_summary: Path = task_dir / "v1" / "qa-summary.md"
    pptx_path: Path = task_dir / "v1" / "final.pptx"
    image_html: str = (
        '<img class="contact-sheet" src="/static/v1/contact-sheet.png" alt="v1 contact sheet">'
        if contact_sheet.exists()
        else "<p class='risk'>还没有找到 <code>v1/contact-sheet.png</code>。生成 v1 后刷新此页。</p>"
    )
    qa_text: str = qa_summary.read_text(encoding="utf-8") if qa_summary.exists() else "暂无 QA 摘要。"
    body: str = f"""<div class="topline">Style Review</div>
<h1>第一版视觉复审</h1>
<p>基于 v1 contact sheet 选择是否生成对比版本。不要复制 JSON，点击按钮即可。</p>
<section class="section">
  <h2>当前版本</h2>
  {image_html}
  <p>PPTX: <code>{html.escape(str(pptx_path))}</code></p>
  <pre>{html.escape(qa_text[:2400])}</pre>
</section>
<form method="post" action="/api/revision">
  {''.join(question_section(group) for group in REVISION_GROUPS)}
  <section class="section">
    <h2>生成几个对比版本?</h2>
    <label class="option"><input type="radio" name="revision_count" value="0"> 保持 v1，进入最终选择</label>
    <label class="option"><input type="radio" name="revision_count" value="1" checked> 生成一个对比版本</label>
    <label class="option"><input type="radio" name="revision_count" value="2"> 生成两个对比版本</label>
    <textarea name="notes" placeholder="补充说明，例如：第 5 页架构图需要更清楚。"></textarea>
  </section>
  <div class="actions">
    <button type="submit">确认视觉选择</button>
  </div>
</form>"""
    return html_page("Presentation Director Style Review", body)


def apply_revision_request(form: dict[str, list[str]]) -> JsonDict:
    request: JsonDict = {
        "version": "0.1",
        "base_version": "v1",
        "revision_count": int(first_form_value(form, "revision_count", "1")),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "preserve": [
            "factual content",
            "slide claims",
            "source attribution",
            "official asset policy",
            "imagegen policy",
        ],
    }
    for group in REVISION_GROUPS:
        value: str = first_form_value(form, group.key, group.default)
        choice: Choice = selected_choice(group, value)
        custom: str = first_form_value(form, f"{group.key}__custom", "").strip()
        request[group.key] = custom if value == "custom" and custom else value
        request[f"{group.key}_label"] = custom if value == "custom" and custom else choice.label
    request["notes"] = first_form_value(form, "notes", "").strip()
    return request


def render_compare(task_dir: Path) -> str:
    version_cards: list[str] = []
    for version in ("v1", "v2", "v3"):
        version_dir: Path = task_dir / version
        if not version_dir.exists():
            continue
        contact_sheet: Path = version_dir / "contact-sheet.png"
        qa_summary: Path = version_dir / "qa-summary.md"
        pptx_path: Path = version_dir / "final.pptx"
        image_html: str = (
            f'<img class="contact-sheet" src="/static/{version}/contact-sheet.png" alt="{version} contact sheet">'
            if contact_sheet.exists()
            else "<p class='risk'>没有 contact sheet。</p>"
        )
        qa_text: str = qa_summary.read_text(encoding="utf-8") if qa_summary.exists() else "暂无 QA 摘要。"
        version_cards.append(
            f"""<section class="section">
  <h2>{html.escape(version.upper())}</h2>
  {image_html}
  <p>PPTX: <code>{html.escape(str(pptx_path))}</code></p>
  <pre>{html.escape(qa_text[:1600])}</pre>
  <label class="option"><input type="radio" name="selected_version" value="{html.escape(version)}"> 选择 {html.escape(version.upper())}</label>
</section>"""
        )
    if not version_cards:
        version_cards.append("<p class='risk'>还没有可比较版本。请先生成 v1。</p>")
    body: str = f"""<div class="topline">Version Compare</div>
<h1>选择最终版本</h1>
<form method="post" action="/api/final-selection">
  {''.join(version_cards)}
  <section class="section">
    <h2>选择后动作</h2>
    <textarea name="notes" placeholder="最终选择理由或仍需注意的问题。"></textarea>
  </section>
  <div class="actions">
    <button type="submit">确认最终版本</button>
    <a class="button secondary" href="/style-review">继续修改</a>
  </div>
</form>"""
    return html_page("Presentation Director Compare", body)


def render_all_pages(task_dir: Path) -> None:
    write_text(task_dir / "intake.html", render_intake(task_dir))
    write_text(task_dir / "brief-confirm.html", render_confirm(task_dir))
    write_text(task_dir / "style-review.html", render_style_review(task_dir))
    write_text(task_dir / "compare.html", render_compare(task_dir))


def initial_prompt(task_dir: Path) -> str:
    brief: JsonDict = read_json(task_dir / "brief-confirmed.json")
    if not brief:
        return "No confirmed brief found. Confirm intake first."
    return f"""Use the Codex Presentations skill and artifact-tool presentation JSX.

Confirmed brief:
{json.dumps(brief, ensure_ascii=False, indent=2)}

Rules:
- Audience, goal, source boundary, logo policy, image policy, and output constraints are locked.
- Do not fabricate metrics, logos, customer names, screenshots, or official-looking brand assets.
- Use official or user-provided brand assets only.
- AI images are allowed only according to the confirmed image policy.
- Composition, layout rhythm, chart treatment, typography hierarchy, and visual expression are delegated to Presentations.
- Do not use a fixed design-lock unless the confirmed brief explicitly asks for it.

Output:
- Use the Presentations internal scratch workspace as required by the plugin.
- Copy the editable PPTX to {task_dir / "v1" / "final.pptx"}.
- Copy the contact sheet and a concise QA summary to {task_dir / "v1"}.
- Generate layout JSON and QA notes in the Presentations workspace.
- Write a concise QA summary to {task_dir / "v1" / "qa-summary.md"}.
- Return PPTX path, contact sheet path, QA summary, and remaining risks.
"""


def revision_prompt(task_dir: Path) -> str:
    request: JsonDict = read_json(task_dir / "revision-request.json")
    if not request:
        return "No revision request found. Complete style review first."
    return f"""Revise the existing v1 PPTX using the selected revision request.

Base version:
{task_dir / "v1" / "final.pptx"}

Revision request:
{json.dumps(request, ensure_ascii=False, indent=2)}

Preserve:
- factual content
- slide claims
- sources and omission notes
- official asset policy
- imagegen policy

Change only the selected visual directions:
- palette direction
- structure rhythm
- visual expression
- image/logo treatment

Render and QA:
- use the Presentations internal scratch workspace as required by the plugin
- copy revised PPTX under {task_dir / "v2" / "final.pptx"} unless generating multiple versions
- copy contact sheet and QA summary into the same version folder
- compare against v1
- document what changed and remaining risks
"""


class DirectorHandler(BaseHTTPRequestHandler):
    task_dir: Path

    def log_message(self, format_text: str, *args: Any) -> None:
        sys.stderr.write("[presentation-director] " + format_text % args + "\n")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path: str = parsed.path
        if path in ("/", "/intake"):
            self.send_html(render_intake(self.task_dir))
        elif path == "/confirm":
            self.send_html(render_confirm(self.task_dir))
        elif path == "/style-review":
            self.send_html(render_style_review(self.task_dir))
        elif path == "/compare":
            self.send_html(render_compare(self.task_dir))
        elif path.startswith("/static/"):
            self.send_static(path.removeprefix("/static/"))
        elif path == "/confirmed":
            self.send_html(message_page("Brief confirmed", "可以回到 Codex，agent 会检测 confirmed.ready 并开始生成。"))
        elif path == "/revision-saved":
            self.send_html(message_page("Revision saved", "可以回到 Codex，agent 会检测 revision.ready 并生成对比版本。"))
        elif path == "/final-selected":
            self.send_html(message_page("Final version selected", "可以回到 Codex，agent 会检测 final-selected.ready 并做最终交付。"))
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        form: dict[str, list[str]] = self.read_form()
        if parsed.path == "/api/intake":
            draft: JsonDict = read_json(self.task_dir / "brief-draft.json")
            brief: JsonDict = apply_intake_selection(draft, form)
            topic: str = first_form_value(form, "topic", "").strip()
            if topic:
                brief["topic"] = topic
            brief["notes"] = first_form_value(form, "notes", "").strip()
            write_json(self.task_dir / "intake-selection.json", brief)
            render_all_pages(self.task_dir)
            self.redirect("/confirm")
        elif parsed.path == "/api/confirm":
            selected: JsonDict = read_json(self.task_dir / "intake-selection.json")
            if not selected:
                selected = read_json(self.task_dir / "brief-draft.json")
            selected["confirmed"] = True
            selected["confirmed_at"] = datetime.now().isoformat(timespec="seconds")
            write_json(self.task_dir / "brief-confirmed.json", selected)
            touch_status(self.task_dir, "confirmed")
            render_all_pages(self.task_dir)
            self.redirect("/confirmed")
        elif parsed.path == "/api/revision":
            request: JsonDict = apply_revision_request(form)
            write_json(self.task_dir / "revision-request.json", request)
            touch_status(self.task_dir, "revision")
            render_all_pages(self.task_dir)
            self.redirect("/revision-saved")
        elif parsed.path == "/api/final-selection":
            selected_version: str = first_form_value(form, "selected_version", "v1")
            selected_pptx: Path = self.task_dir / selected_version / "final.pptx"
            final_dir: Path = self.task_dir / "final"
            final_pptx: Path = final_dir / f"{self.task_dir.name}.pptx"
            if selected_pptx.exists():
                final_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(selected_pptx, final_pptx)
            payload: JsonDict = {
                "version": "0.1",
                "selected_version": selected_version,
                "selected_pptx": str(selected_pptx),
                "final_pptx": str(final_pptx if final_pptx.exists() else selected_pptx),
                "notes": first_form_value(form, "notes", "").strip(),
                "selected_at": datetime.now().isoformat(timespec="seconds"),
            }
            write_json(self.task_dir / "final-selection.json", payload)
            touch_status(self.task_dir, "final-selection")
            self.redirect("/final-selected")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def read_form(self) -> dict[str, list[str]]:
        length: int = int(self.headers.get("Content-Length", "0"))
        body: bytes = self.rfile.read(length)
        return parse_qs(body.decode("utf-8"), keep_blank_values=True)

    def send_html(self, content: str) -> None:
        body: bytes = content.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_static(self, raw_path: str) -> None:
        relative: Path = Path(unquote(raw_path))
        if relative.is_absolute() or ".." in relative.parts:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return
        path: Path = self.task_dir / relative
        if not path.exists() or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content_type: str = "application/octet-stream"
        if path.suffix.lower() == ".png":
            content_type = "image/png"
        elif path.suffix.lower() == ".jpg" or path.suffix.lower() == ".jpeg":
            content_type = "image/jpeg"
        elif path.suffix.lower() == ".md":
            content_type = "text/plain; charset=utf-8"
        data: bytes = path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, target: str) -> None:
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", target)
        self.end_headers()


def message_page(title: str, message: str) -> str:
    body: str = f"""<div class="topline">Presentation Director</div>
<h1>{html.escape(title)}</h1>
<section class="section"><p>{html.escape(message)}</p></section>
<div class="actions">
  <a class="button" href="/intake">Intake</a>
  <a class="button" href="/style-review">Style Review</a>
  <a class="button" href="/compare">Compare</a>
</div>"""
    return html_page(title, body)


def resolve_task_dir(args: argparse.Namespace) -> Path:
    base_dir: Path = Path(args.base_dir).expanduser().resolve()
    thread_id: str = args.thread_id or os.environ.get("CODEX_THREAD_ID") or now_id()
    task_slug: str = slugify(args.task)
    return workspace_root(base_dir, thread_id, task_slug)


def command_init(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    task_dir.mkdir(parents=True, exist_ok=True)
    brief: JsonDict = build_draft_brief(slugify(args.task), args.topic or args.task, args.source or [])
    write_json(task_dir / "brief-draft.json", brief)
    render_all_pages(task_dir)
    print(f"Presentation Director task created: {task_dir}")
    print(f"Open intake page: {task_dir / 'intake.html'}")
    print("For click-to-submit flow, run:")
    print(f"  python3 scripts/presentation_director.py serve --task {slugify(args.task)}")


def command_render(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    render_all_pages(task_dir)
    print(f"Rendered pages in {task_dir}")
    if args.open_page:
        open_director_page(args.host, args.port, args.open_page)


def open_director_page(host: str, port: int, page: str) -> str:
    path: str | None = PAGE_PATHS.get(page)
    if path is None:
        raise SystemExit(f"Unknown page: {page}")
    url: str = f"http://{host}:{port}{path}"
    webbrowser.open(url)
    print(f"Opened {url}")
    return url


def command_serve(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    if not (task_dir / "brief-draft.json").exists():
        print(f"Missing brief-draft.json in {task_dir}. Run init first.", file=sys.stderr)
        raise SystemExit(1)
    handler_class: type[DirectorHandler] = type(
        "BoundDirectorHandler",
        (DirectorHandler,),
        {"task_dir": task_dir},
    )
    server: ThreadingHTTPServer = ThreadingHTTPServer((args.host, args.port), handler_class)
    print(f"Serving Presentation Director for {task_dir}")
    print(f"Intake:       http://{args.host}:{args.port}/intake")
    print(f"Confirm:      http://{args.host}:{args.port}/confirm")
    print(f"Style review: http://{args.host}:{args.port}/style-review")
    print(f"Compare:      http://{args.host}:{args.port}/compare")
    if not args.no_open and args.open_page:
        open_director_page(args.host, args.port, args.open_page)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


def command_wait(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    filename: str | None = STATUS_FILES.get(args.for_status)
    if filename is None:
        raise SystemExit(f"Unknown status: {args.for_status}")
    target: Path = status_dir(task_dir) / filename
    started: float = time.time()
    while True:
        if target.exists():
            print(f"Ready: {target}")
            return
        if args.timeout > 0 and time.time() - started > args.timeout:
            raise SystemExit(f"Timed out waiting for {target}")
        time.sleep(args.interval)


def command_prompt(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    if args.kind == "initial":
        print(initial_prompt(task_dir))
    elif args.kind == "revision":
        print(revision_prompt(task_dir))
    else:
        raise SystemExit(f"Unknown prompt kind: {args.kind}")


def command_open_page(args: argparse.Namespace) -> None:
    resolve_task_dir(args)
    open_director_page(args.host, args.port, args.page)


def build_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Presentation Director helper for Codex + Presentations workflows."
    )
    parser.add_argument("--base-dir", default=".", help="Repository/workspace root. Default: current directory.")
    parser.add_argument("--thread-id", default=None, help="Deprecated compatibility option; user-facing files now live in PPTX/<task-slug>/.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create a director workspace and render initial pages.")
    init_parser.add_argument("--task", required=True, help="Task slug or title.")
    init_parser.add_argument("--topic", default="", help="Optional topic/title shown in the brief.")
    init_parser.add_argument("--source", action="append", default=[], help="Source path or URL. Repeatable.")
    init_parser.set_defaults(func=command_init)

    render_parser = subparsers.add_parser("render", help="Regenerate HTML pages from current JSON.")
    render_parser.add_argument("--task", required=True, help="Task slug or title.")
    render_parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host for optional browser open. Default: {DEFAULT_HOST}")
    render_parser.add_argument("--port", default=DEFAULT_PORT, type=int, help=f"Port for optional browser open. Default: {DEFAULT_PORT}")
    render_parser.add_argument("--open-page", choices=sorted(PAGE_PATHS.keys()), help="Open a Director page in the default browser after rendering.")
    render_parser.set_defaults(func=command_render)

    serve_parser = subparsers.add_parser("serve", help="Run local click-to-submit UI server.")
    serve_parser.add_argument("--task", required=True, help="Task slug or title.")
    serve_parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host. Default: {DEFAULT_HOST}")
    serve_parser.add_argument("--port", default=DEFAULT_PORT, type=int, help=f"Port. Default: {DEFAULT_PORT}")
    serve_parser.add_argument(
        "--open-page",
        choices=sorted(PAGE_PATHS.keys()),
        default="intake",
        help="Open a Director page in the default browser once the server starts. Default: intake.",
    )
    serve_parser.add_argument("--no-open", action="store_true", help="Do not open a browser page after the server starts.")
    serve_parser.set_defaults(func=command_serve)

    wait_parser = subparsers.add_parser("wait", help="Wait for a ready status file.")
    wait_parser.add_argument("--task", required=True, help="Task slug or title.")
    wait_parser.add_argument("--for", dest="for_status", choices=sorted(STATUS_FILES.keys()), required=True)
    wait_parser.add_argument("--timeout", type=float, default=0.0, help="Seconds before timeout. 0 means no timeout.")
    wait_parser.add_argument("--interval", type=float, default=1.0, help="Polling interval seconds.")
    wait_parser.set_defaults(func=command_wait)

    prompt_parser = subparsers.add_parser("prompt", help="Print Presentations handoff prompt.")
    prompt_parser.add_argument("--task", required=True, help="Task slug or title.")
    prompt_parser.add_argument("--kind", choices=("initial", "revision"), required=True)
    prompt_parser.set_defaults(func=command_prompt)

    open_parser = subparsers.add_parser("open-page", help="Open a running Director page in the default browser.")
    open_parser.add_argument("--task", required=True, help="Task slug or title.")
    open_parser.add_argument("--page", choices=sorted(PAGE_PATHS.keys()), required=True)
    open_parser.add_argument("--host", default=DEFAULT_HOST, help=f"Host. Default: {DEFAULT_HOST}")
    open_parser.add_argument("--port", default=DEFAULT_PORT, type=int, help=f"Port. Default: {DEFAULT_PORT}")
    open_parser.set_defaults(func=command_open_page)

    return parser


def main() -> None:
    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
