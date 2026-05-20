---
name: deck-builder
description: Orchestrates a full-pipeline workflow for creating professional presentation decks from source materials — editable PPTX as the primary output, HTML deck as a secondary online-sharing output. This skill should be used when the task involves generating a new presentation deck from an article, book, knowledge document, engineering project materials, or any substantive source — specifically when slide planning (deck.md), design intelligence, visual contract, and verified output are needed. Do NOT trigger for small edits to existing slides (typo fixes, minor text changes), quick Marp/reveal.js previews, or requests that do not require a full deck planning and design workflow.
---

# Deck Builder

A workflow orchestration skill for building professional presentations. It enforces the full pipeline — from source material through slide planning, design intelligence, visual contract, to verified PPTX or HTML output.

This skill does NOT generate slides directly. It routes to the correct generation engine based on the active environment and target output format.

---

## Request Boundary Check

Before starting this pipeline, verify the request actually needs a new deck:

| Request Type | Action |
|-------------|--------|
| New deck from source material | **Proceed with this pipeline** |
| Slide plan review or deck.md revision | **Proceed with this pipeline** |
| Single-slide text fix in existing deck | Handle directly — skip this pipeline |
| QA pass on an existing generated deck | Handle directly — skip this pipeline |
| Quick Marp / reveal.js preview | Handle directly — skip this pipeline |
| Format-only change (color, font size) | Handle directly — skip this pipeline |

If in doubt: does the request require producing or revising a `slide-plan.md` or `deck.md`? If yes, use this pipeline. If no, handle directly.

---

## Trigger Scope

**Use this skill when:**
- Generating a new deck from an article, book, knowledge document, or engineering project materials
- The request implies slide planning, deck.md authoring, or design system selection
- The user asks for a professional, editable, or high-quality presentation
- The user mentions "slide planner", "deck.md", "design profile", or "visual contract"

**Do NOT trigger when:**
- Fixing a typo or rewriting a single slide in an existing deck
- Creating a quick Marp or reveal.js preview file
- The user only asks to change formatting in an already-generated deck
- No new deck planning is required

---

## Installation Paths

Canonical copy lives in MD2PPT; sync to global locations as needed:

```
MD2PPT/skills/deck-builder/         ← canonical source
~/.claude/skills/deck-builder/       ← Claude Code (global)
~/.codex/skills/deck-builder/        ← Codex (sync only if ~/.codex/skills/ exists)
```

VS Code agent support depends on the specific agent extension — check its skill loading config separately.

Sync command after edits to canonical:
```bash
# Run from the MD2PPT repository root.
mkdir -p "$HOME/.claude/skills" "$HOME/.codex/skills"
rm -rf "$HOME/.claude/skills/deck-builder" "$HOME/.codex/skills/deck-builder"
cp -R "$(pwd)/skills/deck-builder" "$HOME/.claude/skills/"
cp -R "$(pwd)/skills/deck-builder" "$HOME/.codex/skills/"
```

---

## Dependency Resolution

This skill is global, so do not assume MD2PPT-local paths exist in every project.

Resolve dependencies in this order:

| Dependency | Resolution |
|------------|------------|
| `design-consultant` | Use the current repo's `skills/ui-ux-pro-max/scripts/search.py` if present; otherwise try `$HOME/.claude/skills/ui-ux-pro-max/scripts/search.py`, then `$HOME/.codex/skills/ui-ux-pro-max/scripts/search.py`. If none exists, synthesize a short design intelligence brief from the source and mark the tool as unavailable. |
| `design-locks/` | Use the current repo's `design-locks/` if present. Otherwise look for `design-locks/` inside the directory containing this SKILL.md (bundled by install.sh). If neither exists, use a lightweight visual contract written directly in `deck.md` and do not cite a missing profile file. |
| PPTX fallback | Use `skills/pptx/SKILL.md` only when it exists in the current repo. If absent, do not pretend the fallback is available. |
| HTML engines | Use `guizang-ppt-skill` or `html-ppt-skill` only when the skill/tool is available in the active environment. If neither is available, explain the missing dependency or generate only the handoff prompt. |
| MD2PPT docs | Treat `docs/pptx-master-workflow.md` and `docs/quality-gates.md` as optional project-level context. Outside MD2PPT, rely on this skill's reference files and the minimum QA checklist below instead. |

Never include file paths in a generation prompt unless those files actually exist.

---

## Pipeline Overview

```
[1] Source Material
    Article / book / knowledge doc / engineering project / topic
        ↓
[2] Slide Planner  ← NEVER skip this step
    audience → thesis → arc → slide claims → proof objects → omissions
    Output: slide-plan.md
        ↓
[3] deck.md
    Thesis, audience, per-slide: claim + proof object + source
        ↓
[4] 颜色层 (Color Layer)
    design-consultant → 2-3 套配色方案（可视色块）→ 迭代调整 → 用户确认
        ↓
[5] 结构层 (Structure Layer)
    展示全部 5 个 design-locks → 用户选择 → 记录颜色覆盖 → 两层都确认后才 lock
        ↓
[6] Generation  (environment-dependent — see Tool Routing)
        ↓
[7] Render QA
    Contact sheet + layout JSON + at least one fix-and-reverify cycle
        ↓
outputs/<deck-title>.pptx   ← primary
outputs/<deck-title>.html   ← secondary (HTML deck, when requested)
```

Skipping Step 2 produces information dumps, not presentations.

---

## Tool Routing

| Environment | Generation Path | Notes |
|-------------|-----------------|-------|
| Codex | Presentations plugin **(primary PPTX)** | `artifact-tool presentation-jsx` |
| Claude Code / offline | `skills/pptx` + pptxgenjs **(fallback PPTX)** | pptxgenjs |
| Either | **guizang-ppt-skill** (primary HTML) | Reveal.js-based HTML deck — secondary output for online sharing |
| Either | **html-ppt-skill** (alternative HTML) | 36 themes / 31 layouts / presenter mode — use when richer HTML layouts are needed |
| Either | Marp | Quick draft / PDF only — not editable PPTX |

**Hard constraints — never misattribute these roles:**
- `ui-ux-pro-max` = design intelligence tool, NOT a PPTX generator
- `design-locks/` = visual contracts, NOT slide templates or generation engines
- pptxgenjs = Claude Code fallback only, NOT the Codex primary path
- guizang-ppt-skill / html-ppt-skill = HTML secondary output only, NOT a PPTX replacement
- Marp output = NOT a professional editable PPTX

---

## Execution Steps

### Step 1 — Classify the Input

| Input Type | Key Questions | Reference |
|------------|---------------|-----------|
| Article / book / knowledge doc | What is the central thesis? Who is the audience? | `references/source-to-deck.md` |
| Engineering project | What problem does it solve? Who are the stakeholders? | `references/engineering-project-deck.md` |
| Topic only | What outcome does the user need — pitch, brief, report? | Proceed to slide planner directly |

### Step 2 — Run the Slide Planner

Read `references/slide-planner.md` for the full planner protocol.

Produce `slide-plan.md` containing:
- `audience`, `goal`, `thesis`, `arc`, `slide-count`
- Per-slide: `claim`, `proof-object`, `layout-family`, `source`, `missing`
- `appendix-plan`: what moves to notes or appendix, not the main deck

**Confirmation behavior — HARD STOP in interactive sessions:**

In an interactive session (human is present):
1. Present the slide plan as a readable list: slide number, title, one-line claim, layout intent
2. Ask explicitly: "这个大纲符合你的想法吗？有需要调整的幻灯片顺序、数量或重点吗？确认后我继续下一步。"
3. **STOP. Do not write deck.md, do not run ui-ux-pro-max, do not call any tool until the user replies.**
4. Only proceed to Step 3 after the user sends an explicit confirmation (e.g., "好的"、"继续"、"looks good", or change instructions).

Rationale: skipping this confirmation forces an expensive full-rerun if the structure is wrong. The cost of pausing here is near zero.

In a batch / automated / non-interactive context: write `slide-plan.md`, log "slide-plan.md written — proceeding to deck.md", then continue without waiting.

### Step 3 — Write deck.md

Read `references/source-to-deck.md` or `references/engineering-project-deck.md` for structure.

Rules:
- Every slide needs a `Claim` — a conclusion sentence, not a topic label
- Every slide needs one primary `Proof object` (chart, diagram, table, big number, case)
- Every number and logo needs a `Source`; write "missing" if unverifiable — never invent data

### Step 4 — 颜色层 (Color Layer)

Run `design-consultant` (scripts: `skills/ui-ux-pro-max/scripts/search.py`). Read `references/design-workflow.md` for query protocol.

**Present 2–3 palette options via HTML preview — HARD STOP:**

After running design-consultant, do NOT present palettes as terminal text only. Instead:

1. Write `assets/palettes.json` with the 2–3 options in this exact format:
```json
[
  {
    "id": "A",
    "name": "风格名称",
    "bg": "#hex",
    "text": "#hex",
    "accent": "#hex",
    "muted": "#hex",
    "font_zh": "思源黑体",
    "font_en": "Inter",
    "mood": "情绪描述",
    "lock": "recommended-lock-id"
  }
]
```

2. Run the preview script:
```bash
python3 scripts/preview_palette.py
# 生成 assets/palette-preview.html
```

3. Tell the user: **"配色方案预览已生成，请在浏览器中打开 `assets/palette-preview.html` 查看真实色彩效果，选择后点击「确认此配色方案」，将确认内容粘贴回来继续。"**

If `scripts/preview_palette.py` is not available (outside MD2PPT repo), fall back to terminal text with `████` Unicode blocks — but always note the limitation.

**Consultation is iterative:**
- User can say "我想要更暖的色调" / "强调色换成橙色" / "更深的背景"
- Update `palettes.json` and re-run the script each iteration — the browser auto-refreshes on reload
- User can also ask for a mood board image (DALL-E 3) to preview the overall visual feel

**STOP. Do not proceed to Step 5 until user explicitly confirms a palette by pasting their selection.**

The output of Step 4 is:
- Confirmed color palette (hex values, semantic roles)
- Confirmed typography direction (Chinese + Latin fonts)
- Confirmed mood and style
- Suggested design-lock for the structural layer

### Step 5 — 结构层 (Structure Layer)

颜色层（Step 4）已确认。结构层提供设计的骨架：字体层级、网格比例、图表标注规则、禁用效果。

**必须先运行预览脚本，绝不跳过此步骤直接展示文字表格。**

脚本已打包在 skill 目录中。按以下顺序查找并运行：

```bash
# 优先在当前项目目录查找
python3 scripts/preview_locks.py

# 若当前目录没有，用 skill 内置版本（全局安装路径）
python3 ~/.claude/skills/deck-builder/scripts/preview_locks.py
```

运行后告知用户：**"结构层预览已生成，请在浏览器中打开 `assets/locks-preview.html`，点击左侧选项查看封面和内页结构，选好后点「确认此结构层 →」，将选择粘贴回来继续。"**

同时给出文字推荐（作为辅助说明，不替代 HTML 预览）：

| 方案 | 风格 | 适合 | 不适合 |
|------|------|------|--------|
| Swiss · Klein Blue | 权威 · 精准 · 高对比 | 商业计划、投资人、路线图 | 文化类、叙事类 |
| Linear Dark | 工程精密 · 现代科技 · 暗色 | SaaS、技术平台、工程演示 | 教学类、文化类 |
| Academic Indigo | 冷调学术 · 信息密度高 | 技术方案、数据报告、答辩 | 温暖叙事类 |
| Warm Paper | 叙事 · 温暖纸感 · 编辑感 | 路演、课程、观点类 | 纯工程类、数据密集 |
| Notion Warm | 亲和 · 极简 · 文档感 | 内部汇报、文化类、轻量演示 | 投资人演示、高强度外部 |

（选择时请用 lock ID：`swiss-klein-blue` / `linear-dark` / `guizang-indigo` / `guizang-monocle` / `notion-warm`）

推荐最匹配 Step 4 配色情绪的选项，说明理由。

**STOP. 等用户从预览页面选择并粘贴确认，不得自行决定。**

两层都确认之后，才写入 `deck.md` 的 Design Contract：

```markdown
## Design Contract
- Structure lock: design-locks/<lock>.md
- Color layer (from Step 4):
  - background: #[hex]
  - primary text: #[hex]
  - accent: #[hex]
  - muted: #[hex]
  - _(只列与 lock 默认值不同的颜色)_
- Typography: [中文字体] + [西文字体]（来自 Step 4 确认）
- Must keep: lock 的字体层级、网格语法、图表标注规则
- May adapt: layout families to match proof objects
- Must avoid: gradients, generic card grids, invented logos, unsupported metrics
```

**这是真正的 lock 时刻。** 颜色层 + 结构层都由用户明确选定后，生成过程不得引入任何未在 Design Contract 中声明的颜色、字体或效果。

### Step 5.5 — AI Background Image (Optional)

**Trigger this step only after the profile is confirmed.**

Ask the user one question:
> "需要为封面和章节分隔页生成 AI 背景图吗？现有的纯色方案够用就可以跳过。"

**If user says skip / no:** proceed directly to Step 6.

**If user says yes:** read `docs/ai-background-image.md` for the full protocol, then:
1. **Auto-construct the image prompt** — do NOT pass the user's raw instruction to the API. Build a rich DALL-E 3 prompt by combining:
   - Primary color family from the Design Contract (e.g. "deep indigo blue tones, #0a1f3d")
   - Mood/style from the confirmed structure lock (e.g. "scholarly, cold-tech aesthetic")
   - Deck theme/topic extracted from `deck.md` thesis (e.g. "AI infrastructure growth in enterprise")
   - Fixed technical constraints: "abstract texture, no people, no faces, no text, suitable for 16:9 presentation slide background, high contrast areas reserved for title placement, 1920×1080"
   - Overlay note: "semi-transparent overlay will be applied — background should be rich in texture but not distracting"
2. Call DALL-E 3 via OpenAI images API (or Flux/SD if user specifies) — only for cover and section-divider slides
3. Save generated images to `assets/` in the current project folder
4. Note image paths — they will be referenced in Step 6 generation prompts
5. Add a 遮罩 (semi-transparent overlay, 40–60% opacity, using the profile's background color) instruction to the generation prompt to ensure text readability

Hard constraints (from `docs/ai-background-image.md`):
- Abstract texture / geometry only — no scenes, people, faces, text
- Image must use the profile's primary color family
- Only cover + section-divider slides get background images; content slides do not
- Always build the full prompt internally — never pass a one-line user instruction directly to the image API

### Step 6 — Generate

Read `references/prompt-templates.md` for ready-to-use prompts.

- In Codex: use Template A (Presentations plugin)
- In Claude Code: use Template B (pptxgenjs fallback)
- HTML deck (either environment): use Template C (guizang-ppt-skill or html-ppt-skill)

### Step 7 — Render QA

Full gate definitions inside MD2PPT: `docs/quality-gates.md`. If that file is unavailable, apply this minimum checklist before declaring done:

- [ ] Per-slide preview images rendered (or browser screenshot for HTML)
- [ ] Contact sheet generated (PPTX) or browser full-screen test completed (HTML)
- [ ] Layout JSON reviewed (overflow, font issues, spacing)
- [ ] At least one "find issue → fix → re-render" cycle completed
- [ ] Final output confirmed at `outputs/<deck-title>.pptx` or `outputs/<deck-title>.html`
- [ ] Completion report includes: output path, render evidence, remaining risks

---

## Out of Scope

- Marp `.md` writing → handle directly without this pipeline
- Google Slides native creation → generate PPTX first, import via Google Drive
- reveal.js from scratch (no source material) → handle directly
- Fixing individual slides in an existing deck → do it directly
