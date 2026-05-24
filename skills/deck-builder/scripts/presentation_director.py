#!/usr/bin/env python3
"""Local Presentation Director UI for Codex + Presentations workflows.

This script does not generate PPTX files. It creates a small local UI for:
1. intake choices before generation,
2. brief confirmation before calling Presentations,
3. visual revision choices after v1,
4. final version selection,
5. view-only HTML companions from rendered slide previews.
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
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
IMAGE_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg", ".webp"}
STATUS_FILES: dict[str, str] = {
    "confirmed": "confirmed.ready",
    "revision": "revision.ready",
    "final-selection": "final-selected.ready",
}
PAGE_PATHS: dict[str, str] = {
    "intake": "/intake",
    "visual-inspiration": "/visual-inspiration",
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


@dataclass(frozen=True)
class VisualCandidate:
    key: str
    name: str
    summary: str
    best_for: str
    avoid_for: str
    palette: tuple[str, str, str, str]
    background: str
    typography: str
    layout: str
    chart: str
    image_strategy: str
    inspiration: str
    risk: str


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
        key="research_strategy",
        title="资料研究策略",
        prompt="如果资料不完整，先怎么获得研究材料?",
        default="hybrid-deep-research",
        choices=(
            Choice("hybrid-deep-research", "Hybrid：外部 Deep Research + Codex 定点核验", "适合医学、产业、政策、技术趋势等资料密集主题。"),
            Choice("codex-web-deep", "Codex 深度联网研究", "由 Codex 查找、筛选、核验资料；更耗时和 token。"),
            Choice("external-deep-research", "Gemini / Perplexity Deep Research 资料包", "先用外部 Deep Research 做广覆盖，再把资料包交给 Codex 结构化。"),
            Choice("provided-materials", "只用我提供的资料", "不主动联网，缺失信息必须标注。"),
            Choice("custom", "自定义", "我有自己的研究资料策略。"),
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


def natural_sort_key(path: Path) -> list[tuple[int, int | str]]:
    parts: list[str] = re.split(r"(\d+)", path.name.lower())
    return [(0, int(part)) if part.isdigit() else (1, part) for part in parts]


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


def default_intake_value(question: Question, sources: list[str]) -> str:
    if question.key == "source_boundary":
        return "provided-only" if sources else "web-with-sources"
    if question.key == "research_strategy":
        if not sources:
            return "hybrid-deep-research"
        source_text: str = " ".join(sources).lower()
        if any(token in source_text for token in ("gemini", "perplexity", "deep-research", "deep research")):
            return "external-deep-research"
        return "provided-materials"
    return question.default


def selection_value(selections: JsonDict, key: str, default: str = "") -> str:
    item: Any = selections.get(key, {})
    if isinstance(item, dict):
        return str(item.get("value", default))
    return default


def visual_candidate_to_json(candidate: VisualCandidate) -> JsonDict:
    return {
        "key": candidate.key,
        "name": candidate.name,
        "summary": candidate.summary,
        "best_for": candidate.best_for,
        "avoid_for": candidate.avoid_for,
        "palette": list(candidate.palette),
        "background": candidate.background,
        "typography": candidate.typography,
        "layout": candidate.layout,
        "chart": candidate.chart,
        "image_strategy": candidate.image_strategy,
        "inspiration": candidate.inspiration,
        "risk": candidate.risk,
    }


def classify_visual_context(topic: str, selections: JsonDict) -> str:
    deck_type: str = selection_value(selections, "deck_type")
    audience: str = selection_value(selections, "audience")
    text: str = f"{topic} {deck_type} {audience}".lower()
    if any(token in text for token in ("体育", "足球", "篮球", "运动", "赛事", "sports", "football", "basketball", "club")):
        return "sports"
    if any(token in text for token in ("战略", "策略", "规划", "运营", "组织", "增长", "strategy", "planning", "operations")):
        return "strategy"
    if any(token in text for token in ("医学", "药", "临床", "疾病", "研究", "alzheimer", "clinical", "biotech", "medical", "research")):
        return "research"
    if deck_type in {"engineering-platform"} or any(token in text for token in ("工程", "架构", "系统", "平台", "infra", "architecture", "developer")):
        return "engineering"
    if deck_type in {"investor-pitch", "sales-product"}:
        return "market"
    return "general"


def build_visual_candidates(topic: str, selections: JsonDict) -> tuple[VisualCandidate, ...]:
    context: str = classify_visual_context(topic, selections)
    libraries: dict[str, tuple[VisualCandidate, ...]] = {
        "sports": (
            VisualCandidate(
                "broadcast-analytics",
                "Broadcast Analytics",
                "像体育转播数据大屏，节奏强、数字醒目、对比高。",
                "赛事复盘、球队经营、体育商业分析。",
                "严肃学术汇报或低调内部材料。",
                ("#07111f", "#f7f8fb", "#24d18b", "#ffcc33"),
                "深色场地感背景，少量动线和数据网格。",
                "粗标题 + 紧凑数字标签。",
                "比分板式大数字、左右对抗、关键事件时间线。",
                "排名、雷达、趋势线，直接标注而少用图例。",
                "真实赛事/训练素材优先；没有素材时使用抽象运动轨迹。",
                "sports broadcast UI + html deck theme catalog + evidence dashboard",
                "容易过于娱乐化，商业策略页需要降噪。",
            ),
            VisualCandidate(
                "performance-lab",
                "Performance Lab",
                "运动科学实验室风格，干净、精准、强调指标和方法。",
                "训练表现、运动医学、青训体系、数据分析。",
                "需要强情绪感染力的路演封面。",
                ("#f4f7f8", "#17202a", "#006b7a", "#f05a28"),
                "浅底实验室网格，局部使用测量线和坐标标尺。",
                "清晰无衬线，数字使用 tabular 风格。",
                "指标卡 + 流程图 + 对比切片。",
                "小 multiples、区间带、前后对照。",
                "真实运动员素材需来源明确；可用抽象人体运动线框。",
                "performance dashboard + scientific poster + ui-ux-pro-max chart grammar",
                "可能偏理性，封面需要额外增强视觉冲击。",
            ),
            VisualCandidate(
                "club-strategy-room",
                "Club Strategy Room",
                "俱乐部董事会/战术室风格，适合把体育主题讲成战略问题。",
                "球队战略、商业化、组织治理、赞助规划。",
                "纯技术训练分析。",
                ("#102033", "#f0eadc", "#b99855", "#e85d04"),
                "暖纸 + 深色战术线，背景像会议室白板和策略地图。",
                "稳重标题字体，正文较克制。",
                "战略地图、路径图、stakeholder matrix。",
                "瀑布图、路线图、二维象限。",
                "尽量使用真实 logo/球衣/场馆素材；无授权则不用。",
                "strategy room + editorial deck + locked visual contract",
                "如果资料很多，需要避免把每页做成咨询报告表格。",
            ),
        ),
        "strategy": (
            VisualCandidate(
                "executive-boardroom",
                "Executive Boardroom",
                "高层决策汇报风格，克制但有权威感。",
                "战略规划、预算、组织调整、董事会汇报。",
                "创意发布会或教学课程。",
                ("#0f172a", "#f8fafc", "#3b82f6", "#c8a24a"),
                "浅底为主，关键页使用深色整页强调。",
                "强层级标题，正文短句化。",
                "决策摘要、风险矩阵、路线图、经营仪表盘。",
                "waterfall、scenario matrix、milestone roadmap。",
                "少装饰，优先使用真实业务图表和图标。",
                "consulting deck + executive dashboard + design-lock discipline",
                "如果全程深色，会显得压抑；应控制深色页比例。",
            ),
            VisualCandidate(
                "consulting-roadmap",
                "Consulting Roadmap",
                "咨询公司路线图风格，结构强、阶段清楚。",
                "三年规划、转型项目、市场进入策略。",
                "需要强品牌个性的产品发布。",
                ("#ffffff", "#111827", "#2563eb", "#f97316"),
                "纯白背景，细线分区，少量高饱和强调。",
                "标题结论句化，正文像 executive memo。",
                "阶段推进、2x2、能力地图、优先级排序。",
                "矩阵、堆叠条、战略地图。",
                "不依赖图片，强调结构图和业务对象。",
                "strategy scaffold + html-ppt-skill template catalog + ui-ux-pro-max UX rules",
                "容易变成普通咨询模板，需要用主题专属 proof object 打破通用感。",
            ),
            VisualCandidate(
                "operating-model-dashboard",
                "Operating Model Dashboard",
                "运营模型仪表盘风格，适合把规划落到指标和机制。",
                "年度经营计划、组织运行、OKR、流程治理。",
                "纯品牌故事或情绪型演讲。",
                ("#eef2f6", "#1f2937", "#0f766e", "#7c3aed"),
                "浅灰工作台背景，模块边界清楚，强调可扫描。",
                "中等字号、高信息密度但留白稳定。",
                "机制图、RACI、节奏表、指标看板。",
                "KPI cards、heatmap、pipeline funnel。",
                "真实流程图/组织图优先，不用装饰性背景图。",
                "operational SaaS UI + dashboard grammar + quality gates",
                "过密时容易不适合演讲，需要 split slide。",
            ),
        ),
        "research": (
            VisualCandidate(
                "clinical-atlas",
                "Clinical Atlas",
                "研究图谱风格，适合复杂证据链和研发路径。",
                "医学、生命科学、政策研究、技术综述。",
                "销售型产品发布和强情绪路演。",
                ("#f6f8fb", "#132238", "#0f6f8f", "#d97706"),
                "浅底研究图谱，局部使用细网格、节点和证据线。",
                "学术无衬线，标题清楚，来源小字统一。",
                "证据链、pipeline、机制图、分层框架。",
                "pipeline、forest-like comparison、evidence table。",
                "真实图表和示意图优先；AI 图只作抽象章节背景。",
                "academic design-lock + evidence dashboard + source-first QA",
                "如果每页都很理性，封面和章节页需要更强视觉记忆点。",
            ),
            VisualCandidate(
                "biotech-pipeline",
                "Biotech Pipeline",
                "生物科技投资人 deck 风格，重点突出机会、管线和决策。",
                "药物研发、创新技术、融资路演、BD 汇报。",
                "纯课程教学或极保守学术答辩。",
                ("#08111f", "#f8fafc", "#4cc9f0", "#ffb703"),
                "深浅交替，封面和章节页有高对比抽象分子/路径背景。",
                "大标题 + 突出 milestone 和数据。",
                "研发管线、市场窗口、风险消减、里程碑。",
                "pipeline chart、TAM blocks、risk ladder。",
                "可生成抽象科学背景，但不能伪造实验图片或监管标志。",
                "startup pitch + clinical pipeline layout + visual preview selection",
                "容易过度路演化，需保留来源和监管谨慎语气。",
            ),
            VisualCandidate(
                "medical-editorial",
                "Medical Editorial",
                "高质量医学长文/期刊特稿风格，适合解释复杂主题。",
                "研究综述、课程讲解、公众科普、专家分享。",
                "需要强销售转化的商业 deck。",
                ("#f2efe8", "#1f2933", "#6b7c93", "#b35c1e"),
                "暖纸底、细分隔线、少量图像纹理。",
                "出版物式标题，正文段落可读性优先。",
                "定义、分层、对比、时间线、注释式图表。",
                "annotated timeline、small multiples、callout table。",
                "少量抽象背景；内容页保持干净。",
                "editorial design-lock + beautiful template contract + typography rules",
                "可能不够有冲击力，商业听众需要增加关键数字页。",
            ),
        ),
        "engineering": (
            VisualCandidate(
                "signal-system",
                "Signal System",
                "系统评审风格，清晰、工程化、数据前置。",
                "平台架构、工程汇报、技术路线、SRE/数据系统。",
                "品牌发布会或教学科普。",
                ("#f8fafc", "#111827", "#0061ff", "#16a34a"),
                "浅底工程网格，少量蓝色信号线。",
                "紧凑标题，代码/指标用等宽或 tabular 数字。",
                "架构图、数据流、模块责任、指标看板。",
                "latency charts、dependency map、before/after bars。",
                "真实截图优先，截图可美化但不重画事实。",
                "Signal design language + architecture QA + screenshot treatment rules",
                "如果不加故事节奏，容易像技术文档。",
            ),
            VisualCandidate(
                "terminal-architecture",
                "Terminal Architecture",
                "高对比开发者工具风格，适合代码和基础设施。",
                "infra、DevOps、AI agent、开发者平台。",
                "非技术高层或客户销售。",
                ("#09090b", "#fafafa", "#7dd3fc", "#a3e635"),
                "深色终端背景，细线拓扑和命令行提示。",
                "大标题清晰，代码块严格控制长度。",
                "系统拓扑、调用链、状态机、故障演练。",
                "sequence diagram、service map、error budget chart。",
                "避免假 UI；真实终端/产品截图需来源明确。",
                "Terminal design language + locked layout IDs + render QA",
                "不适合长正文，文字必须拆页。",
            ),
            VisualCandidate(
                "product-operations",
                "Product Operations",
                "产品运营工作台风格，适合把技术价值讲给业务方。",
                "产品方案、客户场景、运营效率、自动化平台。",
                "底层架构深挖。",
                ("#f4f6f8", "#1f2937", "#0ea5e9", "#f59e0b"),
                "浅灰 SaaS 工作台，但减少普通卡片堆叠。",
                "清楚的组件标题和短解释。",
                "用户旅程、功能流程、价值闭环、仪表盘。",
                "funnel、cohort trend、task flow。",
                "真实产品截图优先，必要时使用线框场景图。",
                "SaaS UI + product launch scaffold + no generic card grid rule",
                "若卡片过多会显得普通，需要开放构图页做节奏变化。",
            ),
        ),
        "market": (
            VisualCandidate(
                "studio-pitch",
                "Studio Pitch",
                "更像高质量创业路演，节奏快、对比强、视觉记忆点明显。",
                "融资、比赛、产品发布、BD。",
                "监管、医学、法务等需要克制语气的汇报。",
                ("#101828", "#ffffff", "#5b7cfa", "#ff6b35"),
                "深浅切换，大封面和章节图形成记忆点。",
                "短标题、大数字、强对比。",
                "问题-方案-证明-增长-请求。",
                "traction chart、market map、before/after。",
                "可以用抽象概念图，但不能伪造客户 logo 或产品截图。",
                "Studio design language + pitch deck scaffold + visual-led HTML previews",
                "若证据不足，强表现力会放大可信度风险。",
            ),
            VisualCandidate(
                "product-launch",
                "Product Launch",
                "产品发布会风格，突出用户场景和体验。",
                "新品发布、功能介绍、客户演示。",
                "高密度内部复盘。",
                ("#ffffff", "#0f172a", "#7c3aed", "#06b6d4"),
                "干净背景 + 大图区域 + 少量品牌渐变。",
                "标题直接，辅助文案短。",
                "场景、功能、流程、价值证明。",
                "feature matrix、workflow、adoption trend。",
                "真实产品截图优先；无截图时用抽象线框，不伪造 UI。",
                "product launch template + screenshot slot contract + ui-ux-pro-max style match",
                "如果没有真实素材，视觉会偏概念化。",
            ),
            VisualCandidate(
                "brand-narrative",
                "Brand Narrative",
                "品牌叙事风格，强调信任、愿景和故事线。",
                "品牌升级、客户提案、公益/教育项目。",
                "纯技术评审或数据审计。",
                ("#f7f2e8", "#1c1917", "#2563eb", "#c2410c"),
                "暖底、摄影/插画槽位、章节像短篇故事。",
                "叙事标题，正文强调节奏。",
                "用户故事、价值阶梯、生态地图。",
                "impact metrics、quote callout、timeline。",
                "真实人物/客户素材必须授权；否则使用抽象场景图。",
                "editorial template + brand system + visual contract depth",
                "如果目标是做决策，故事页必须配决策页。",
            ),
        ),
    }
    default_candidates: tuple[VisualCandidate, ...] = (
        VisualCandidate(
            "atlas-explanatory",
            "Atlas Explanatory",
            "结构化知识图谱风格，适合把复杂主题讲清楚。",
            "研究、课程、政策、行业分析。",
            "强销售转化或纯代码评审。",
            ("#f6f3ee", "#1f2937", "#2563eb", "#b45309"),
            "浅底、细网格、少量章节色块。",
            "稳健标题，正文强调可读性。",
            "框架图、时间线、对比表、证据链。",
            "timeline、matrix、annotated chart。",
            "抽象背景只用于封面和章节页。",
            "Atlas design language + design-lock registry + source-first planner",
            "可能偏解释型，需要在封面增强主题记忆点。",
        ),
        VisualCandidate(
            "signal-dashboard",
            "Signal Dashboard",
            "数据和机制先行，适合把主题变成可行动判断。",
            "策略、运营、工程、管理汇报。",
            "情绪型演讲或品牌故事。",
            ("#f8fafc", "#0f172a", "#0f766e", "#f59e0b"),
            "浅灰工作台背景，图表和流程为主。",
            "数字清楚，标签短。",
            "dashboard、flow、roadmap、decision matrix。",
            "KPI、trend、heatmap、funnel。",
            "少图片，多使用原生图表和形状。",
            "Signal design language + dashboard UI + quality gates",
            "容易过密，必须控制每页 proof object 数量。",
        ),
        VisualCandidate(
            "studio-visual",
            "Studio Visual",
            "更强视觉表达，适合需要第一眼吸引力的 deck。",
            "路演、发布、竞赛、客户提案。",
            "保守审计或纯学术材料。",
            ("#111827", "#ffffff", "#6366f1", "#f97316"),
            "强封面、章节视觉和深浅对比。",
            "大标题、短句、视觉锚点。",
            "hero statement、before/after、proof snapshot。",
            "大数字、对比图、简化趋势。",
            "允许抽象概念图，禁止伪造真实资产。",
            "Studio design language + 3-preview workflow + visual-led templates",
            "表现力强时更需要事实来源压住可信度。",
        ),
    )
    return libraries.get(context, default_candidates)


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
    .candidate {{ min-height: 100%; }}
    .candidate input {{ margin-right: 8px; }}
    .swatches-preview {{ display: flex; gap: 6px; margin: 12px 0; }}
    .swatch-preview {{ width: 34px; height: 22px; border-radius: 4px; border: 1px solid rgba(0,0,0,.12); }}
    .mini-slides {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 12px 0; }}
    .mini-slide {{
      aspect-ratio: 16 / 9;
      border-radius: 6px;
      padding: 10px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      border: 1px solid rgba(0,0,0,.14);
      overflow: hidden;
    }}
    .mini-slide strong {{ font-size: 12px; line-height: 1.15; }}
    .mini-slide span {{ display: block; width: 60%; height: 5px; border-radius: 99px; opacity: .9; }}
    .mini-bars {{ display: grid; gap: 4px; }}
    .mini-bars i {{ display: block; height: 5px; border-radius: 99px; opacity: .86; }}
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
    source_items: list[JsonDict] = build_source_items(sources)
    return {
        "version": "0.1",
        "task_slug": task_slug,
        "topic": topic or task_slug.replace("-", " "),
        "sources": source_items,
        "selections": {
            question.key: {
                "value": default_intake_value(question, sources),
                "label": selected_choice(question, default_intake_value(question, sources)).label,
                "source": "default",
            }
            for question in INTAKE_QUESTIONS
        },
        "risks": infer_risks(source_items),
        "confirmed": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def infer_source_type(source: str) -> str:
    lowered: str = source.lower()
    if re.match(r"https?://", source) and (
        "drive.google.com" in lowered or "docs.google.com" in lowered
    ):
        return "google-drive-url"
    if re.match(r"https?://", source):
        return "url"
    path: Path = Path(source).expanduser()
    if path.is_dir():
        return "folder"
    suffix: str = path.suffix.lower().lstrip(".")
    return suffix or "text"


def build_source_items(sources: list[str]) -> list[JsonDict]:
    return [
        {"path": source, "priority": "primary", "type": infer_source_type(source)}
        for source in sources
        if source.strip()
    ]


def source_paths_from_items(sources: Any) -> list[str]:
    if not isinstance(sources, list):
        return []
    paths: list[str] = []
    for source in sources:
        if isinstance(source, dict):
            path: str = str(source.get("path", "")).strip()
            if path:
                paths.append(path)
    return paths


def parse_sources_text(value: str) -> list[str]:
    raw_items: list[str] = re.split(r"[\n,]+", value)
    seen: set[str] = set()
    sources: list[str] = []
    for raw_item in raw_items:
        source: str = raw_item.strip()
        if not source or source in seen:
            continue
        seen.add(source)
        sources.append(source)
    return sources


def format_sources_text(sources: Any) -> str:
    return "\n".join(source_paths_from_items(sources))


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
    draft_selections: JsonDict = draft.get("selections", {})
    form_sources_text: str = first_form_value(form, "sources_text", "").strip()
    draft_sources: list[str] = source_paths_from_items(draft.get("sources", []))
    selected_sources: list[str] = parse_sources_text(form_sources_text) if form_sources_text else draft_sources
    selected_source_items: list[JsonDict] = build_source_items(selected_sources)
    for question in INTAKE_QUESTIONS:
        draft_item: Any = draft_selections.get(question.key, {})
        fallback: str = (
            str(draft_item.get("value", ""))
            if isinstance(draft_item, dict) and draft_item.get("value")
            else default_intake_value(question, selected_sources)
        )
        value: str = first_form_value(form, question.key, fallback)
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
    brief["sources"] = selected_source_items
    brief["risks"] = infer_risks(selected_source_items)
    brief["selections"] = selections
    brief["updated_at"] = datetime.now().isoformat(timespec="seconds")
    brief["confirmed"] = False
    return brief


def apply_visual_selection(selected: JsonDict, form: dict[str, list[str]]) -> JsonDict:
    topic: str = str(selected.get("topic", ""))
    selections: JsonDict = selected.get("selections", {})
    candidates: tuple[VisualCandidate, ...] = build_visual_candidates(topic, selections)
    selected_key: str = first_form_value(form, "visual_candidate", candidates[0].key)
    candidate: VisualCandidate = next((item for item in candidates if item.key == selected_key), candidates[0])
    updated: JsonDict = dict(selected)
    updated["visual_direction"] = {
        "selected_candidate": visual_candidate_to_json(candidate),
        "available_candidates": [visual_candidate_to_json(item) for item in candidates],
        "source": "user-selected",
        "notes": first_form_value(form, "visual_notes", "").strip(),
        "selected_at": datetime.now().isoformat(timespec="seconds"),
    }
    updated["updated_at"] = datetime.now().isoformat(timespec="seconds")
    updated["confirmed"] = False
    return updated


def ensure_visual_selection(selected: JsonDict) -> JsonDict:
    visual_direction: Any = selected.get("visual_direction", {})
    if isinstance(visual_direction, dict) and isinstance(visual_direction.get("selected_candidate"), dict):
        return selected
    topic: str = str(selected.get("topic", ""))
    selections: JsonDict = selected.get("selections", {})
    candidate: VisualCandidate = build_visual_candidates(topic, selections)[0]
    updated: JsonDict = dict(selected)
    updated["visual_direction"] = {
        "selected_candidate": visual_candidate_to_json(candidate),
        "available_candidates": [visual_candidate_to_json(item) for item in build_visual_candidates(topic, selections)],
        "source": "agent-recommended-default",
        "notes": "",
        "selected_at": datetime.now().isoformat(timespec="seconds"),
    }
    return updated


def first_form_value(form: dict[str, list[str]], key: str, default: str) -> str:
    values: list[str] | None = form.get(key)
    if not values:
        return default
    return values[0]


def candidate_slide_dirs(version_dir: Path) -> list[Path]:
    return [
        version_dir / "slides",
        version_dir / "preview",
        version_dir / "previews",
        version_dir / "rendered-slides",
        version_dir / "html-assets",
    ]


def collect_slide_images(version_dir: Path, explicit_dir: Path | None = None) -> list[Path]:
    search_dirs: list[Path] = [explicit_dir] if explicit_dir else candidate_slide_dirs(version_dir)
    for slide_dir in search_dirs:
        if slide_dir is None or not slide_dir.exists() or not slide_dir.is_dir():
            continue
        images: list[Path] = [
            path
            for path in slide_dir.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ]
        if images:
            return sorted(images, key=natural_sort_key)
    return []


def image_data_uri(path: Path) -> str:
    mime_type: str = mimetypes.guess_type(path.name)[0] or "image/png"
    encoded: str = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def build_share_html(title: str, slide_images: list[Path], source_pptx: Path | None = None) -> str:
    generated_at: str = datetime.now().isoformat(timespec="seconds")
    slides: list[str] = []
    for index, image_path in enumerate(slide_images, start=1):
        slides.append(
            f"""<section class="slide" id="slide-{index}">
  <div class="slide-number">{index:02d} / {len(slide_images):02d}</div>
  <img src="{image_data_uri(image_path)}" alt="Slide {index}">
</section>"""
        )
    source_note: str = (
        f"<p>Source PPTX: <code>{html.escape(str(source_pptx))}</code></p>"
        if source_pptx
        else ""
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #111;
      --panel: #1b1b1b;
      --ink: #f6f6f6;
      --muted: #aaa;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC", sans-serif;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding: 12px 20px;
      background: rgba(17, 17, 17, .92);
      border-bottom: 1px solid #2a2a2a;
      backdrop-filter: blur(8px);
    }}
    h1 {{ margin: 0; font-size: 16px; font-weight: 650; }}
    .meta {{ color: var(--muted); font-size: 12px; }}
    main {{
      display: grid;
      gap: 28px;
      padding: 24px;
      max-width: 1280px;
      margin: 0 auto;
    }}
    .slide {{
      position: relative;
      background: var(--panel);
      border: 1px solid #2a2a2a;
      box-shadow: 0 18px 60px rgba(0, 0, 0, .35);
    }}
    .slide img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .slide-number {{
      position: absolute;
      right: 10px;
      top: 8px;
      padding: 3px 7px;
      border-radius: 999px;
      background: rgba(0, 0, 0, .56);
      color: #fff;
      font-size: 11px;
    }}
    footer {{
      padding: 22px 24px 36px;
      color: var(--muted);
      font-size: 12px;
      text-align: center;
    }}
    code {{ color: #ddd; }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <div class="meta">{len(slide_images)} slides · generated {html.escape(generated_at)}</div>
  </header>
  <main>
    {''.join(slides)}
  </main>
  <footer>
    <p>View-only HTML companion generated from rendered slide previews. Edit the PPTX source, then regenerate this HTML after changes.</p>
    {source_note}
  </footer>
</body>
</html>
"""


def write_share_html(
    task_dir: Path,
    version_dir: Path,
    title: str,
    explicit_slides_dir: Path | None = None,
    output_path: Path | None = None,
) -> Path:
    slide_images: list[Path] = collect_slide_images(version_dir, explicit_slides_dir)
    if not slide_images:
        searched: str = ", ".join(str(path) for path in candidate_slide_dirs(version_dir))
        raise ValueError(f"No per-slide preview images found. Searched: {searched}")
    final_dir: Path = task_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    target: Path = output_path or final_dir / f"{slugify(title)}.html"
    source_pptx: Path = version_dir / "final.pptx"
    html_text: str = build_share_html(title, slide_images, source_pptx if source_pptx.exists() else None)
    write_text(target, html_text)
    return target


def render_intake(task_dir: Path) -> str:
    draft: JsonDict = read_json(task_dir / "brief-draft.json")
    current: JsonDict = read_json(task_dir / "intake-selection.json", draft)
    selections: JsonDict = current.get("selections", {})
    current_sources: Any = current.get("sources", draft.get("sources", []))
    source_list: str = render_sources(current_sources)
    sources_text: str = format_sources_text(current_sources)
    body: str = f"""<div class="topline">Presentation Director</div>
<h1>生成前信息收集</h1>
<p>先确认会影响 PPTX 质量的关键信息。每题都有默认推荐，也可以选择自定义。</p>
<section class="section">
  <h2>资料来源</h2>
  {source_list}
  <label>资料路径 / 网页 / Google Drive 地址
    <textarea name="sources_text" form="intake-form" placeholder="每行一个来源。例如：&#10;/Users/you/project/docs&#10;https://example.com/report&#10;https://drive.google.com/file/d/...&#10;https://docs.google.com/document/d/...">{html.escape(sources_text)}</textarea>
  </label>
  <p class="meta">可以填写本地文件夹、本地文件、普通网页 URL、Google Drive / Docs / Slides / Sheets 地址。Google Drive 地址会作为来源链接记录，后续由 agent 按权限读取或要求你授权。</p>
  <label>主题 / 标题
    <input type="text" name="topic" form="intake-form" value="{html.escape(str(current.get("topic", draft.get("topic", ""))))}">
  </label>
</section>
<form method="post" action="/api/intake" id="intake-form">
  {''.join(question_section(question, selections.get(question.key, {}).get("value", "")) for question in INTAKE_QUESTIONS)}
  <section class="section">
    <h2>额外说明</h2>
    <textarea name="notes" placeholder="例如必须保留的页面、禁用内容、特殊听众背景。">{html.escape(str(current.get("notes", "")))}</textarea>
  </section>
  <div class="actions">
    <button type="submit">下一步：视觉候选</button>
  </div>
</form>"""
    return html_page("Presentation Director Intake", body)


def render_visual_inspiration(task_dir: Path) -> str:
    draft: JsonDict = read_json(task_dir / "brief-draft.json")
    selected: JsonDict = read_json(task_dir / "intake-selection.json", draft)
    topic: str = str(selected.get("topic", draft.get("topic", "")))
    selections: JsonDict = selected.get("selections", {})
    candidates: tuple[VisualCandidate, ...] = build_visual_candidates(topic, selections)
    visual_direction: JsonDict = selected.get("visual_direction", {})
    current_key: str = str(
        visual_direction.get("selected_candidate", {}).get("key", candidates[0].key)
        if isinstance(visual_direction, dict)
        else candidates[0].key
    )
    candidate_cards: list[str] = [
        render_visual_candidate_card(candidate, current_key == candidate.key)
        for candidate in candidates
    ]
    body: str = f"""<div class="topline">Visual Inspiration Gate</div>
<h1>选择第一版视觉方向</h1>
<p>这些候选会根据主题、PPT 类型和听众动态生成。它们借鉴 design-lock、ui-ux-pro-max、HTML deck/theme catalog 的做法，但最终仍交给 Codex Presentations 生成可编辑 PPTX。</p>
<section class="section">
  <h2>当前主题</h2>
  <p><strong>{html.escape(topic)}</strong></p>
</section>
<form method="post" action="/api/visual-inspiration">
  <div class="grid">
    {''.join(candidate_cards)}
  </div>
  <section class="section">
    <h2>视觉补充要求</h2>
    <textarea name="visual_notes" placeholder="例如：更像顶级咨询公司、更少卡片、背景更有层次、适合医学研究听众。">{html.escape(str(visual_direction.get("notes", "") if isinstance(visual_direction, dict) else ""))}</textarea>
  </section>
  <div class="actions">
    <a class="button secondary" href="/intake">返回修改 intake</a>
    <button type="submit">下一步：汇总确认</button>
  </div>
</form>"""
    return html_page("Presentation Director Visual Inspiration", body)


def render_visual_candidate_card(candidate: VisualCandidate, checked: bool) -> str:
    is_checked: str = " checked" if checked else ""
    swatches: str = "".join(
        f'<span class="swatch-preview" style="background:{html.escape(color)}"></span>'
        for color in candidate.palette
    )
    bg_color: str = candidate.palette[0]
    ink_color: str = candidate.palette[1]
    accent: str = candidate.palette[2]
    accent_2: str = candidate.palette[3]
    return f"""<label class="option candidate">
  <input type="radio" name="visual_candidate" value="{html.escape(candidate.key)}"{is_checked}>
  <strong>{html.escape(candidate.name)}</strong>
  <p>{html.escape(candidate.summary)}</p>
  <div class="swatches-preview">{swatches}</div>
  <div class="mini-slides" aria-hidden="true">
    <div class="mini-slide" style="background:{html.escape(bg_color)}; color:{html.escape(ink_color)}">
      <strong>{html.escape(candidate.name)}</strong>
      <span style="background:{html.escape(accent)}"></span>
    </div>
    <div class="mini-slide" style="background:#fff; color:#1f2937">
      <strong>Evidence page</strong>
      <div class="mini-bars">
        <i style="width:86%; background:{html.escape(accent)}"></i>
        <i style="width:62%; background:{html.escape(accent_2)}"></i>
        <i style="width:74%; background:{html.escape(ink_color)}"></i>
      </div>
    </div>
  </div>
  <p><strong>适合：</strong>{html.escape(candidate.best_for)}</p>
  <p><strong>背景：</strong>{html.escape(candidate.background)}</p>
  <p><strong>图表：</strong>{html.escape(candidate.chart)}</p>
  <p><strong>借鉴：</strong>{html.escape(candidate.inspiration)}</p>
  <p class="meta"><strong>风险：</strong>{html.escape(candidate.risk)}</p>
</label>"""


def render_sources(sources: Any) -> str:
    if not isinstance(sources, list) or not sources:
        return "<p class='risk'>未记录资料来源。可以在下面粘贴本地路径、网页 URL 或 Google Drive 地址。</p>"
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
    visual_direction: JsonDict = selected.get("visual_direction", {})
    selected_candidate: JsonDict = {}
    if isinstance(visual_direction, dict):
        raw_candidate: Any = visual_direction.get("selected_candidate", {})
        if isinstance(raw_candidate, dict):
            selected_candidate = raw_candidate
    if not selected_candidate:
        topic: str = str(selected.get("topic", draft.get("topic", "")))
        candidates: tuple[VisualCandidate, ...] = build_visual_candidates(topic, selections)
        selected_candidate = visual_candidate_to_json(candidates[0])
    palette_html: str = "".join(
        f'<span class="swatch-preview" style="background:{html.escape(str(color))}"></span>'
        for color in selected_candidate.get("palette", [])
    )
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
  <h2>选定视觉方向</h2>
  <h3>{html.escape(str(selected_candidate.get("name", "")))}</h3>
  <p>{html.escape(str(selected_candidate.get("summary", "")))}</p>
  <div class="swatches-preview">{palette_html}</div>
  <p><strong>背景策略：</strong>{html.escape(str(selected_candidate.get("background", "")))}</p>
  <p><strong>版式节奏：</strong>{html.escape(str(selected_candidate.get("layout", "")))}</p>
  <p><strong>图表语法：</strong>{html.escape(str(selected_candidate.get("chart", "")))}</p>
  <p><strong>图片策略：</strong>{html.escape(str(selected_candidate.get("image_strategy", "")))}</p>
  <p><strong>风险：</strong>{html.escape(str(selected_candidate.get("risk", "")))}</p>
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
    <a class="button secondary" href="/visual-inspiration">返回修改视觉方向</a>
    <button type="submit">确认并开始生成</button>
  </div>
</form>"""
    return html_page("Presentation Director Confirm", body)


def render_style_review(task_dir: Path) -> str:
    version_name: str = latest_review_version(task_dir)
    version_dir: Path = task_dir / version_name
    contact_sheet: Path = version_dir / "contact-sheet.png"
    qa_summary: Path = version_dir / "qa-summary.md"
    pptx_path: Path = version_dir / "final.pptx"
    image_html: str = (
        f'<img class="contact-sheet" src="/static/{html.escape(version_name)}/contact-sheet.png" alt="{html.escape(version_name)} contact sheet">'
        if contact_sheet.exists()
        else f"<p class='risk'>还没有找到 <code>{html.escape(version_name)}/contact-sheet.png</code>。生成版本后刷新此页。</p>"
    )
    qa_text: str = qa_summary.read_text(encoding="utf-8") if qa_summary.exists() else "暂无 QA 摘要。"
    body: str = f"""<div class="topline">Style Review</div>
<h1>视觉复审</h1>
<p>基于当前最新版本 <strong>{html.escape(version_name)}</strong> 的 contact sheet 选择是否生成对比版本。不要复制 JSON，点击按钮即可。</p>
<section class="section">
  <h2>当前版本</h2>
  {image_html}
  <p>PPTX: <code>{html.escape(str(pptx_path))}</code></p>
  <pre>{html.escape(qa_text[:2400])}</pre>
</section>
<form method="post" action="/api/revision">
  <input type="hidden" name="base_version" value="{html.escape(version_name)}">
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
    base_version: str = first_form_value(form, "base_version", "v1").strip() or "v1"
    request: JsonDict = {
        "version": "0.1",
        "base_version": base_version,
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
    write_text(task_dir / "visual-inspiration.html", render_visual_inspiration(task_dir))
    write_text(task_dir / "brief-confirm.html", render_confirm(task_dir))
    write_text(task_dir / "style-review.html", render_style_review(task_dir))
    write_text(task_dir / "compare.html", render_compare(task_dir))


def version_number(path: Path) -> int:
    name: str = path.name
    if len(name) > 1 and name[0] == "v" and name[1:].isdigit():
        return int(name[1:])
    return -1


def latest_review_version(task_dir: Path) -> str:
    candidates: list[Path] = [
        item
        for item in task_dir.iterdir()
        if item.is_dir()
        and version_number(item) >= 1
        and (item / "contact-sheet.png").exists()
        and (item / "final.pptx").exists()
    ]
    if not candidates:
        return "v1"
    return max(candidates, key=version_number).name


def initial_prompt(task_dir: Path) -> str:
    brief: JsonDict = read_json(task_dir / "brief-confirmed.json")
    if not brief:
        return "No confirmed brief found. Confirm intake first."
    script_path: Path = Path(__file__).resolve()
    return f"""Use the Codex Presentations skill and artifact-tool presentation JSX.

Confirmed brief:
{json.dumps(brief, ensure_ascii=False, indent=2)}

Rules:
- Audience, goal, research strategy, source boundary, logo policy, image policy, selected visual direction, and output constraints are locked.
- Do not fabricate metrics, logos, customer names, screenshots, or official-looking brand assets.
- Use official or user-provided brand assets only.
- AI images are allowed only according to the confirmed image policy.
- Composition, layout rhythm, chart treatment, typography hierarchy, and visual expression should follow the selected visual candidate while still using Presentations' judgment.
- Do not use a fixed design-lock unless the confirmed brief explicitly asks for it.

Output:
- Use the Presentations internal scratch workspace as required by the plugin.
- Copy the editable PPTX to {task_dir / "v1" / "final.pptx"}.
- Copy per-slide preview PNGs to {task_dir / "v1" / "slides"}.
- Copy the contact sheet and a concise QA summary to {task_dir / "v1"}.
- Generate layout JSON and QA notes in the Presentations workspace.
- Write a concise QA summary to {task_dir / "v1" / "qa-summary.md"}.
- QA must include a rendered no-overlap check: titles, subtitles, body text, labels, footers, page numbers, and connector lines must not collide.
- Long titles must be checked after PowerPoint rendering; if a title wraps and covers the subtitle or body area, fix and re-render before handoff.
- After final selection, generate a view-only HTML companion at {task_dir / "final" / (task_dir.name + ".html")} from the selected version's per-slide previews.
- Before returning control to the user after v1 generation, regenerate Director pages and start the local Director server with the style-review page open:
  python3 "{script_path}" --base-dir "{task_dir.parent.parent}" serve --task "{task_dir.name}" --open-page style-review
- Return PPTX path, HTML companion path, contact sheet path, QA summary, and remaining risks.
"""


def revision_prompt(task_dir: Path) -> str:
    request: JsonDict = read_json(task_dir / "revision-request.json")
    if not request:
        return "No revision request found. Complete style review first."
    base_version: str = str(request.get("base_version") or "v1")
    base_pptx: Path = task_dir / base_version / "final.pptx"
    existing_versions: list[int] = [
        version_number(item)
        for item in task_dir.iterdir()
        if item.is_dir() and version_number(item) >= 1
    ]
    next_version_number: int = (max(existing_versions) if existing_versions else 1) + 1
    next_version: str = f"v{next_version_number}"
    return f"""Revise the existing {base_version} PPTX using the selected revision request.

Base version:
{base_pptx}

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
- copy revised PPTX under {task_dir / next_version / "final.pptx"} unless generating multiple versions
- copy per-slide preview PNGs into the version's `slides/` folder
- copy contact sheet and QA summary into the same version folder
- explicitly check rendered slides for text overlap, especially wrapped titles covering subtitles or body text
- fix any overlap/cropping/too-tight spacing and re-render affected slides before final selection
- compare against {base_version}
- regenerate the final view-only HTML companion from the selected version's per-slide previews after final selection
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
        elif path == "/visual-inspiration":
            self.send_html(render_visual_inspiration(self.task_dir))
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
            self.redirect("/visual-inspiration")
        elif parsed.path == "/api/visual-inspiration":
            selected: JsonDict = read_json(self.task_dir / "intake-selection.json")
            if not selected:
                selected = read_json(self.task_dir / "brief-draft.json")
            updated: JsonDict = apply_visual_selection(selected, form)
            write_json(self.task_dir / "intake-selection.json", updated)
            render_all_pages(self.task_dir)
            self.redirect("/confirm")
        elif parsed.path == "/api/confirm":
            selected: JsonDict = read_json(self.task_dir / "intake-selection.json")
            if not selected:
                selected = read_json(self.task_dir / "brief-draft.json")
            selected = ensure_visual_selection(selected)
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
            selected_version_dir: Path = self.task_dir / selected_version
            selected_pptx: Path = selected_version_dir / "final.pptx"
            final_dir: Path = self.task_dir / "final"
            final_pptx: Path = final_dir / f"{self.task_dir.name}.pptx"
            if selected_pptx.exists():
                final_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(selected_pptx, final_pptx)
            final_html: Path | None = None
            share_html_error: str = ""
            try:
                final_html = write_share_html(self.task_dir, selected_version_dir, self.task_dir.name)
            except ValueError as exc:
                share_html_error = str(exc)
            payload: JsonDict = {
                "version": "0.1",
                "selected_version": selected_version,
                "selected_pptx": str(selected_pptx),
                "final_pptx": str(final_pptx if final_pptx.exists() else selected_pptx),
                "final_html": str(final_html) if final_html else "",
                "notes": first_form_value(form, "notes", "").strip(),
                "selected_at": datetime.now().isoformat(timespec="seconds"),
            }
            if share_html_error:
                payload["share_html_error"] = share_html_error
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
  <a class="button" href="/visual-inspiration">Visual Inspiration</a>
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
    print(f"Intake:             http://{args.host}:{args.port}/intake")
    print(f"Visual inspiration: http://{args.host}:{args.port}/visual-inspiration")
    print(f"Confirm:            http://{args.host}:{args.port}/confirm")
    print(f"Style review:       http://{args.host}:{args.port}/style-review")
    print(f"Compare:            http://{args.host}:{args.port}/compare")
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


def command_share_html(args: argparse.Namespace) -> None:
    task_dir: Path = resolve_task_dir(args)
    version_dir: Path = task_dir / args.version
    slides_dir: Path | None = Path(args.slides_dir).expanduser().resolve() if args.slides_dir else None
    output_path: Path | None = Path(args.output).expanduser().resolve() if args.output else None
    title: str = args.title or task_dir.name
    target: Path = write_share_html(task_dir, version_dir, title, slides_dir, output_path)
    print(f"Share HTML written: {target}")


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

    share_parser = subparsers.add_parser("share-html", help="Build a view-only final HTML companion from per-slide preview images.")
    share_parser.add_argument("--task", required=True, help="Task slug or title.")
    share_parser.add_argument("--version", default="v1", help="Version folder under PPTX/<task-slug>/. Default: v1.")
    share_parser.add_argument("--slides-dir", help="Optional explicit directory containing per-slide PNG/JPG/WebP previews.")
    share_parser.add_argument("--title", default="", help="Optional HTML title and output filename slug.")
    share_parser.add_argument("--output", help="Optional output HTML path. Default: PPTX/<task-slug>/final/<title>.html.")
    share_parser.set_defaults(func=command_share_html)

    return parser


def main() -> None:
    parser: argparse.ArgumentParser = build_parser()
    args: argparse.Namespace = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
