---
name: deck-builder
description: Orchestrates professional presentation creation from source materials. In Codex net-new PPTX requests, this skill MUST run Presentation Director intake, research strategy, visual inspiration, and brief confirmation before Codex Presentations. For Claude/offline/HTML paths it coordinates deck.md planning, design intelligence, visual contracts, and verified output. Do NOT trigger for small edits to existing slides, quick Marp/reveal.js previews, or requests that do not require a new deck workflow.
---

# Deck Builder

A workflow orchestration skill for building professional presentations.

In Codex, this skill is the front door for net-new PPTX requests: run `Presentation Director` first, confirm research strategy and visual inspiration, open the confirmation page, automatically wait for the click confirmation signal, then hand the confirmed brief to the Codex Presentations plugin. The user must only click in the HTML UI; do not ask them to copy/paste, report choices in chat, or reply "confirmed". Do not let Codex Presentations start from an unconfirmed prompt unless the user explicitly asks to skip the director.

Outside Codex, this skill coordinates the fuller deck.md-centered workflow: source material through slide planning, design intelligence, visual contract, and verified PPTX or HTML output.

This skill does NOT generate slides directly. It routes to the correct generation engine based on the active environment and target output format.

---

## Request Boundary Check

Before starting this pipeline, verify the request actually needs a new deck:

| Request Type | Action |
|-------------|--------|
| New PPTX from source material in Codex | **Run Presentation Director before Presentations** |
| New deck from source material outside Codex | **Proceed with deck.md-centered pipeline** |
| Slide plan review or deck.md revision | **Proceed with this pipeline** |
| Single-slide text fix in existing deck | Handle directly — skip this pipeline |
| QA pass on an existing generated deck | Handle directly — skip this pipeline |
| Quick Marp / reveal.js preview | Handle directly — skip this pipeline |
| Format-only change (color, font size) | Handle directly — skip this pipeline |

If in doubt: is this a net-new presentation from substantive source material? If yes, use this pipeline. In Codex, start with Presentation Director. Outside Codex, use the deck.md-centered path.

---

## Trigger Scope

**Use this skill when:**
- Generating a new deck from an article, book, knowledge document, or engineering project materials
- The user asks Codex to create a new PPTX / PowerPoint / presentation from source material
- The request implies slide planning, deck.md authoring, or design system selection
- The user asks for a professional, editable, or high-quality presentation
- The user mentions "Presentation Director", "slide planner", "deck.md", "design lock", or "visual contract"

**Do NOT trigger when:**
- Fixing a typo or rewriting a single slide in an existing deck
- Creating a quick Marp or reveal.js preview file
- The user only asks to change formatting in an already-generated deck
- No new deck planning is required

---

## Installation Paths

Canonical copy lives in Presentation Director; sync to global locations as needed:

```
Presentation Director/skills/deck-builder/         ← canonical source
~/.claude/skills/deck-builder/       ← Claude Code (global)
~/.codex/skills/deck-builder/        ← Codex (sync only if ~/.codex/skills/ exists)
```

VS Code agent support depends on the specific agent extension — check its skill loading config separately.

Sync command after edits to canonical:
```bash
# Run from the Presentation Director repository root.
mkdir -p "$HOME/.claude/skills" "$HOME/.codex/skills"
rm -rf "$HOME/.claude/skills/deck-builder" "$HOME/.codex/skills/deck-builder"
cp -R "$(pwd)/skills/deck-builder" "$HOME/.claude/skills/"
cp -R "$(pwd)/skills/deck-builder" "$HOME/.codex/skills/"
```

---

## Dependency Resolution

This skill is global, so do not assume Presentation Director local paths exist in every project.

Resolve dependencies in this order:

| Dependency | Resolution |
|------------|------------|
| Presentation Director | Use `scripts/presentation_director.py` in the current repo if present; otherwise use `scripts/presentation_director.py` beside this SKILL.md. In Codex net-new PPTX requests, this is the first step before Presentations unless the user explicitly skips it or a user-confirmed brief already exists. |
| `design-consultant` | Use the current repo's `skills/ui-ux-pro-max/scripts/search.py` if present; otherwise try `$HOME/.claude/skills/ui-ux-pro-max/scripts/search.py`, then `$HOME/.codex/skills/ui-ux-pro-max/scripts/search.py`. If none exists, synthesize a short design intelligence brief from the source and mark the tool as unavailable. |
| `design-locks/` | Use the current repo's `design-locks/` if present. Otherwise look for `design-locks/` inside the directory containing this SKILL.md (bundled by install.sh). If neither exists, use a lightweight visual contract written directly in `deck.md` and do not cite a missing lock file. |
| PPTX fallback | Use `skills/pptx/SKILL.md` only when it exists in the current repo. If absent, do not pretend the fallback is available. |
| HTML engines | Use `html-ppt-skill` or `guizang-ppt-skill` only when the skill/tool is available in the active environment. If neither is available, explain the missing dependency or generate only the handoff prompt. |
| Presentation Director docs | Treat `docs/pptx-master-workflow.md` and `docs/quality-gates.md` as optional project-level context. Outside Presentation Director, rely on this skill's reference files and the minimum QA checklist below instead. |

Never include file paths in a generation prompt unless those files actually exist.

---

## PPTX Workspace Rule

For any project, keep all user-facing PPT artifacts in one project-local folder:

```text
PPTX/<task-slug>/
```

Do not scatter generated brief files, intake pages, contact sheets, QA summaries, revision requests, comparison files, or final PPTX/HTML outputs across the project root, `assets/`, or unrelated folders.

Recommended structure:

```text
PPTX/<task-slug>/
  sources/                # optional copied user assets
  brief/                  # optional notes and source summaries
  intake.html
  brief-confirm.html
  brief-confirmed.json
  style-review.html
  revision-request.json
  compare.html
  final-selection.json
  v1/
    final.pptx
    slides/
      slide-001.png
      slide-002.png
    contact-sheet.png
    qa-summary.md
  v2/
    final.pptx
    slides/
    contact-sheet.png
    qa-summary.md
  final/
    <deck-title>.pptx
    <deck-title>.html
    final-report.md
```

Codex Presentations may still use its required internal scratch workspace under `outputs/<thread-id>/presentations/...`. That scratch space is not the user-facing project folder. Copy final deliverables, per-slide preview images, and key review artifacts back into `PPTX/<task-slug>/`.

Every final PPTX deliverable must also have a view-only HTML companion at `PPTX/<task-slug>/final/<deck-title>.html`, generated from rendered slide previews. This companion is for simple sharing only; edit the PPTX and regenerate the companion after changes.

Final PPTX files are the editable source of record. For small changes, use manual PowerPoint editing or Codex Presentations targeted-edit instead of regenerating the full deck. Save targeted edits as a new version folder and regenerate the HTML companion from the updated render previews.

---

## Pipeline Overview

### Codex Net-New PPTX Path

Use this path when Codex has the Presentations plugin available and the user asks for a new editable PPTX.

```
[1] Source Material
    topic / links / files / folder / existing notes
        ↓
[2] Presentation Director intake
    click-based audience, goal, source paths/URLs, research strategy, source boundary, content language, logo policy, image policy, output constraints
    UI communication language auto-detected from the current conversation; content_language remains the deck body language
        ↓
[3] Research Strategy Gate
    Codex deep web research / external Deep Research packet / hybrid / provided-only
        ↓
[4] Visual Inspiration Gate
    3 dynamic visual candidates from topic, deck type, audience, design-locks, ui-ux-pro-max, and deck UI references
        ↓
[5] Brief Confirmation Gate  ← HARD STOP
    open the confirmation page; user reviews the summarized plan and clicks "confirm"
        ↓
[6] Codex Presentations
    confirmed brief → claim spine → design system → contact-sheet plan → editable PPTX
        ↓
[7] Render QA
    previews + layout JSON + contact sheet + fix-and-rerender
        ↓
[8] Style Review
    user chooses keep/current or visual revision directions
        ↓
[9] Optional Revised Versions + Compare
        ↓
PPTX/<task-slug>/final/<deck-title>.pptx
PPTX/<task-slug>/final/<deck-title>.html
```

For this Codex path, do not pre-lock `design-locks/`, palette, or per-slide layout before v1 unless the user explicitly asks. The visual inspiration gate should select a direction, not a rigid template. The goal is to lock intent, source boundaries, research strategy, and visual target, then give Presentations room to produce a stronger first draft.

In interactive Codex sessions, the confirmation gate is a real user-action gate: the agent must not POST `/api/confirm`, write `brief-confirmed.json`, or touch `confirmed.ready` on the user's behalf. Use the local Director server, open the confirm page, wait for `confirmed.ready`, and continue only after the user clicks confirm. The only exception is an explicit user instruction to skip confirmation or generate directly.

### Claude / Offline / HTML Path

```
[1] Source Material
    Article / book / knowledge doc / engineering project / topic
        ↓
[1.5] Presentation Director / Equivalent Intake Gate
    content_language → output_constraints → research boundary → visual target
    user confirmation required before generation
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
PPTX route:
  PPTX/<task-slug>/final/<deck-title>.pptx   ← editable primary output
  PPTX/<task-slug>/final/<deck-title>.html   ← view-only share companion

HTML-deck-only route:
  PPTX/<task-slug>/final/<deck-title>.html   ← full HTML deck output
```

Skipping Step 2 produces information dumps, not presentations.

Claude Code and offline agents follow the same confirmation principle as Codex. If the Presentation Director helper is available, run its intake/confirmation flow and `guard` before generating with pptxgenjs or HTML tooling. If it is not available, present an equivalent chat/static confirmation covering `content_language`, `output_constraints`, audience, goal, slide plan, source boundary, and visual direction; stop until the user explicitly confirms.

---

## Tool Routing

| Environment | Generation Path | Notes |
|-------------|-----------------|-------|
| Codex net-new PPTX | Presentation Director → Presentations plugin **(primary PPTX)** | Intake + research strategy + visual inspiration + brief confirmation must happen before `artifact-tool presentation-jsx` |
| Codex targeted edit / confirmed brief | Presentations plugin | Direct only when not creating a new deck or when `brief-confirmed.json` already exists |
| Claude Code / offline | Presentation Director or equivalent confirmation → `skills/pptx` + pptxgenjs **(fallback PPTX)** | Same `content_language` / `output_constraints` split and user-confirmation gate apply before pptxgenjs |
| Either | HTML deck skill, when installed | `html-ppt-skill` or `guizang-ppt-skill`; secondary output for online sharing |
| Either | Marp | Quick draft / PDF only — not editable PPTX |

**Hard constraints — never misattribute these roles:**
- Presentation Director = Codex intake / confirmation / revision-choice layer, NOT a PPTX generator
- `ui-ux-pro-max` = design intelligence tool, NOT a PPTX generator
- `design-locks/` = visual contracts, NOT slide templates or generation engines
- pptxgenjs = Claude Code fallback only, NOT the Codex primary path
- html-ppt-skill / guizang-ppt-skill = HTML secondary output only, NOT a PPTX replacement
- Marp output = NOT a professional editable PPTX

---

## Execution Steps

### Codex Mode — Presentation Director First

If the environment is Codex and the user asks for a net-new PPTX, use `scripts/presentation_director.py` before running Presentations.

1. Resolve the script path:

```bash
# Prefer repo-local helper.
python3 scripts/presentation_director.py --help

# If outside MD2PPT but this skill is installed globally, use the bundled helper.
python3 <deck-builder-skill-dir>/scripts/presentation_director.py --help
```

2. Initialize the director workspace:

```bash
python3 scripts/presentation_director.py init \
  --task "<short task slug>" \
  --topic "<inferred or user-provided topic>" \
  --source "<resolved source path or URL>" \
  --conversation-text "<recent user prompt or conversation excerpt>"
```

Use `--ui-language auto` by default. The Director HTML gates (`intake`, `visual-inspiration`, `confirm`, `style-review`, and `compare`) should follow the user's current conversation language, while `content_language` controls the language of the generated slide content.

3. Start the local UI server and wait in the same command:

```bash
python3 scripts/presentation_director.py serve-wait \
  --task "<short task slug>" \
  --for confirmed
```

4. Do not ask the user to copy a URL, paste JSON, or come back to chat to say "confirmed". The intake page should open in the default browser. The user will submit intake choices, review the confirmation page, and click confirm. `serve-wait` blocks until `confirmed.ready`, then exits so the agent can continue automatically. If the page does not open, use:

```bash
python3 scripts/presentation_director.py open-page --task "<short task slug>" --page intake
```

For batch or background runs, use `--no-open`, but still pair it with `serve-wait` or `wait` so generation resumes from a file signal, not a chat reply.

5. Generate the handoff prompt:

```bash
python3 scripts/presentation_director.py prompt --task "<short task slug>" --kind initial
```

6. Only now call Codex Presentations.

After v1 is generated, render Director pages and open the style review page. Use the local Director server for click-to-submit behavior; opening `style-review.html` directly is only a static preview. Wait for `revision.ready` if the user chooses a revision, then use:

```bash
python3 scripts/presentation_director.py render --task "<short task slug>"
python3 scripts/presentation_director.py serve --task "<short task slug>" --open-page style-review
python3 scripts/presentation_director.py wait --task "<short task slug>" --for revision
python3 scripts/presentation_director.py prompt --task "<short task slug>" --kind revision
```

After revised versions are generated, render and open the comparison page:

```bash
python3 scripts/presentation_director.py render --task "<short task slug>" --open-page compare
python3 scripts/presentation_director.py wait --task "<short task slug>" --for final-selection
```

Do not bypass this flow in an interactive Codex session unless the user explicitly says to skip it. A casual "continue" after providing source material is not enough to replace the brief confirmation click.

## Claude / Offline / HTML Execution Steps

The steps below are for environments without Codex Presentations, or for HTML output. Do not run them before v1 in Codex net-new PPTX mode unless the user explicitly asks for a deck.md/design-lock workflow.

### Claude Step 1 — Classify the Input

| Input Type | Key Questions | Reference |
|------------|---------------|-----------|
| Article / book / knowledge doc | What is the central thesis? Who is the audience? | `references/source-to-deck.md` |
| Engineering project | What problem does it solve? Who are the stakeholders? | `references/engineering-project-deck.md` |
| Topic only | What outcome does the user need — pitch, brief, report? | Proceed to slide planner directly |

### Claude Step 2 — Run the Slide Planner

Read `references/slide-planner.md` for the full planner protocol.

Produce `slide-plan.md` containing:
- `audience`, `goal`, `content_language`, `output_constraints`, `thesis`, `arc`, `slide-count`
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

For net-new PPTX work, this slide-plan confirmation does not replace the Director confirmation gate when the Director helper is available. Run the helper and guard before generation, or use the equivalent chat/static confirmation only when the helper cannot be used.

### Claude Step 3 — Write deck.md

Read `references/source-to-deck.md` or `references/engineering-project-deck.md` for structure.

Rules:
- Every slide needs a `Claim` — a conclusion sentence, not a topic label
- Every slide needs one primary `Proof object` (chart, diagram, table, big number, case)
- Every number and logo needs a `Source`; write "missing" if unverifiable — never invent data

### Claude Step 4 — 颜色层 (Color Layer)

**Sub-step 4a — 行业情报查询（Industry Intelligence）**

Extract the deck topic and industry from `deck.md` thesis. Then call `search.py` with the topic:

```bash
# Path: skills/ui-ux-pro-max/scripts/search.py (or ~/.claude/skills/ui-ux-pro-max/scripts/search.py)
python3 skills/ui-ux-pro-max/scripts/search.py "[deck topic / product type]" --domain color --json --max-results 3
```

Map each result to palette format:
- `bg` ← result `Background`
- `text` ← result `Foreground`
- `accent` ← result `Primary`
- `muted` ← result `Muted Foreground`
- `mood` ← result `Notes` (trimmed to key phrase)
- `font_zh` ← assign based on mood: formal/academic→"思源宋体", tech/modern→"思源黑体"
- `font_en` ← assign based on mood: editorial→"IBM Plex Sans", modern→"Inter", elegant→"Plus Jakarta Sans"
- `lock` ← assign based on color vibe: dark bg→"linear-dark", warm/paper→"editorial", cool academic→"academic", neutral→"swiss-klein-blue" or "notion-warm"
- `id` ← generate a short slug like "industry-saas-indigo"

**Note:** Filter out search results with very dark backgrounds (`Background` starts with `#0` or `#1` and very low luminance) unless the user explicitly wants dark mode — PPT slides read best on light backgrounds in daylit rooms.

**Sub-step 4b — Write palettes.json**

Write `assets/palettes.json` using the **object format** (supports industry context display in preview):

```json
{
  "deck_industry": "[product type from search results, e.g. SaaS / Finance / Healthcare]",
  "palettes": [
    {
      "id": "industry-saas-blue",
      "name": "风格名称",
      "zh": "中文风格名",
      "category": "tech",
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
}
```

**Sub-step 4c — HTML Preview — HARD STOP:**

Run the preview script to generate the interactive palette selector:

```bash
python3 scripts/preview_palette.py
# Generates assets/palette-preview.html
# Shows: Claude's industry-matched recommendations + full 50-palette browsable library
```

Open `assets/palette-preview.html` automatically. The user should click a palette in the HTML UI; do not ask them to copy/paste the selection back into chat. If the legacy preview script cannot emit a status file, replace it with an equivalent Director-style local endpoint before using it as a primary flow.

If `scripts/preview_palette.py` is not available (outside MD2PPT repo), fall back to terminal text with `████` Unicode blocks — but always note the limitation.

**Consultation is iterative:**
- User can say "我想要更暖的色调" / "强调色换成橙色" / "更深的背景"
- Update `palettes.json` and re-run the script each iteration — the browser auto-refreshes on reload
- User can also ask for a mood board image (DALL-E 3) to preview the overall visual feel

**STOP. Do not proceed to Step 5 until the user explicitly confirms a palette through the HTML UI or an equivalent file-signal mechanism.**

The output of Step 4 is:
- Confirmed color palette (hex values, semantic roles)
- Confirmed typography direction (Chinese + Latin fonts)
- Confirmed mood and style
- Suggested design-lock for the structural layer

### Claude Step 5 — 结构层 (Structure Layer)

颜色层（Step 4）已确认。结构层提供设计的骨架：字体层级、网格比例、图表标注规则、禁用效果。

**必须先运行预览脚本，绝不跳过此步骤直接展示文字表格。**

脚本已打包在 skill 目录中。按以下顺序查找并运行：

```bash
# 优先在当前项目目录查找
python3 scripts/preview_locks.py

# 若当前目录没有，用 skill 内置版本（全局安装路径）
python3 ~/.claude/skills/deck-builder/scripts/preview_locks.py
```

运行后自动打开 `assets/locks-preview.html`。用户只应在 HTML UI 中点击确认结构层；不要要求用户把选择粘贴回聊天。如果旧预览脚本不能写入状态文件，应先补齐等价的本地端点/文件信号，再作为主流程使用。

同时给出文字推荐（作为辅助说明，不替代 HTML 预览）：

| Lock ID | 布局语法 | 适合 | 不适合 |
|---------|----------|------|--------|
| `swiss-klein-blue` | 边栏分割 · 严格栅格 · 精密层级 | 商业计划、投资人、路线图 | 文化类、叙事类 |
| `linear-dark` | 卡片边框 · 高密度 · 代码块结构 | SaaS、技术平台、工程演示 | 教学类、文化类 |
| `academic` | 双色块 · 数据表格 · 权威分割线 | 技术方案、数据报告、答辩 | 温暖叙事类 |
| `editorial` | 引言竖栏 · 长文段落 · 纵向叙事 | 路演、课程、观点类 | 纯工程类、数据密集 |
| `notion-warm` | 卡片列表 · 扁平层级 · 亲和结构 | 内部汇报、文化类、轻量演示 | 投资人演示、高强度外部 |

推荐最匹配 Step 4 配色情绪的选项，说明理由。

**STOP. 等用户从预览页面点击确认，并通过状态文件或等价机制恢复；不得要求聊天粘贴，也不得自行决定。**

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

### Claude Step 5.5 — AI Background Image (Optional) — HARD STOP

**Trigger this step only after Step 5 structure lock is confirmed.**

**HARD STOP — present this choice in the HTML UI and wait for the click/file signal before proceeding to Step 6:**

> "需要为封面和章节分隔页生成 AI 背景图吗？现有的纯色方案够用就可以跳过。"

**Do NOT proceed to Step 6 until the user clicks a choice or an equivalent file signal is present.** This step is skippable, but you must ask.

**If user says skip / no / 跳过:** proceed directly to Step 6.

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
5. Add a 遮罩 (semi-transparent overlay, 40–60% opacity, using the lock's background color) instruction to the generation prompt to ensure text readability

Hard constraints (from `docs/ai-background-image.md`):
- Abstract texture / geometry only — no scenes, people, faces, text
- Image must use the lock's primary color family
- Only cover + section-divider slides get background images; content slides do not
- Always build the full prompt internally — never pass a one-line user instruction directly to the image API

### Claude Step 6 — Generate

Read `references/prompt-templates.md` for ready-to-use prompts.

- In Codex: use Template A (Presentations plugin)
- In Claude Code: use Template B (pptxgenjs fallback)
- HTML deck (either environment): use Template C (html-ppt-skill or guizang-ppt-skill)

Before generating a net-new deck in a workspace that has Presentation Director, run:

```bash
python3 scripts/presentation_director.py --base-dir "." guard --task "<task-slug>"
```

If that guard fails, open the Director confirmation page through `serve-wait` and continue automatically after the user clicks in the HTML UI. Do not ask the user to reply in chat. Do not generate PPTX/HTML by treating a conversational "continue" as a substitute for the confirmation gate unless the user explicitly asks to skip the gate or generate directly.

### macOS PowerPoint File Access Dialogs

Prefer render/export paths that do not use Microsoft PowerPoint UI automation, such as Codex Presentations artifact-tool rendering or LibreOffice/headless renderers. If a PowerPoint-based render is unavoidable on macOS, start the watcher before the render command:

```bash
scripts/macos/powerpoint-grant-access-watcher.sh 180 &
```

The watcher clicks common Microsoft PowerPoint `Grant File Access`, `Select`, and `Grant Access` dialogs. macOS may still require one-time Accessibility permission for the terminal/Codex host process; that OS-level permission cannot be silently bypassed by project code.

### Claude Step 7 — Render QA

Full gate definitions inside Presentation Director: `docs/quality-gates.md`. If that file is unavailable, apply this minimum checklist before declaring done:

- [ ] Per-slide preview images rendered (or browser screenshot for HTML)
- [ ] Contact sheet generated (PPTX) or browser full-screen test completed (HTML)
- [ ] Layout JSON reviewed (overflow, font issues, spacing)
- [ ] No text overlaps after rendering: title/subtitle/body/footer/page number/labels/connectors are visually separated
- [ ] Long titles are safe after wrapping: wrapped titles do not cover subtitles, captions, or the body area
- [ ] At least one "find issue → fix → re-render" cycle completed
- [ ] Final output confirmed at `PPTX/<task-slug>/final/<deck-title>.pptx` or `PPTX/<task-slug>/final/<deck-title>.html`
- [ ] For PPTX output, view-only HTML companion exists at `PPTX/<task-slug>/final/<deck-title>.html`
- [ ] Completion report includes: output path, render evidence, remaining risks

---

## Out of Scope

- Marp `.md` writing → handle directly without this pipeline
- Google Slides native creation → generate PPTX first, import via Google Drive
- reveal.js from scratch (no source material) → handle directly
- Fixing individual slides in an existing deck → do it directly
