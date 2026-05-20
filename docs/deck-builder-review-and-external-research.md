# Deck Builder Review and External Project Research

Date: 2026-05-20

## 1. Current `deck-builder` Review Findings

### Status

The first version of `deck-builder` is structurally sound and usable as a global orchestration skill.

Verified:

- Canonical copy under `skills/deck-builder/` matches the synced copies under `~/.claude/skills/deck-builder/` and `~/.codex/skills/deck-builder/`.
- `quick_validate.py` reports the skill is valid.
- Frontmatter and backtick reference syntax are valid.
- The skill correctly separates responsibilities:
  - `ui-ux-pro-max` is design intelligence.
  - `design-profiles/` are visual contracts.
  - Codex `Presentations` is the primary editable PPTX generation path.
  - `pptxgenjs` is the fallback path for Claude Code or offline use.

### Resolved Portability and Boundary Findings

#### P1. Global skill still assumes MD2PPT-local paths

The skill is intended to work outside MD2PPT, but several references still assume local repo paths such as:

- `skills/ui-ux-pro-max`
- `design-profiles/`
- `docs/pptx-master-workflow.md`
- `skills/pptx/SKILL.md`
- `skills/pptx/scripts/thumbnail.py`

This will break or mislead agents when the skill is triggered from another repository.

Implemented fix:

- Add a `Dependency Resolution` section.
- Resolve dependencies in this order:
  1. Current project local files.
  2. Global skill locations such as `~/.codex/skills` and `~/.claude/skills`.
  3. Inline minimal visual contracts or handoff prompts when a dependency is unavailable.
- Do not cite paths that do not exist in the active project.

#### P2. Slide-plan confirmation needs environment awareness

The slide-plan approval gate is valuable in interactive sessions because it prevents the agent from turning raw material directly into slides without user review.

The issue was not the confirmation itself, but making it unconditional in every environment.

Implemented fix:

- Interactive session: present `slide-plan.md` and wait for approval before writing `deck.md`.
- Batch / automated / non-interactive context: write `slide-plan.md`, log that execution is proceeding without user confirmation, then continue.

#### P3. reveal.js out-of-scope reference was invalid

The Out of Scope section pointed reveal.js work to a skill that is not present in the current Codex skill list.

Implemented fix:

- Replace the reference with a generic rule:
  - Use the current project's reveal.js or Marp workflow if present.
  - If no such workflow exists, handle directly or explain that it is outside the PPTX pipeline.

#### P4. Request boundary needs an explicit self-check

Implemented fix:

- Add a `Request Boundary Check` table at the top of `SKILL.md`.
- Single-slide edits, existing-deck QA, formatting-only changes, and quick preview requests are handled directly without running the full pipeline.

### Good Decisions to Keep

- The trigger scope excludes small slide edits and quick preview workflows.
- The skill is an orchestrator, not another PPTX generator.
- The reference files are split by responsibility and support progressive disclosure.
- The workflow preserves the key planning layer: source material -> `slide-plan.md` -> `deck.md` -> design intelligence -> visual contract -> PPTX generation -> QA.

## 2. External Projects to Research

Target repositories:

- `hugohe3/ppt-master`
- `zarazhangrui/frontend-slides`
- `op7418/guizang-ppt-skill`
- `lewislulu/html-ppt-skill`
- `zarazhangrui/beautiful-html-templates`

Research questions:

- What output format does each project optimize for: editable PPTX, HTML slides, screenshots, PDF, or hybrid?
- What part of our pipeline can it improve: planning, design language, template library, rendering QA, export, or automation?
- Does it solve a current weakness in `deck-builder`?
- Can it be integrated as a dependency, reference pattern, optional path, or only as inspiration?

## 3. External Project Snapshot

Research snapshot:

| Project | Latest inspected commit | Primary output | Core idea |
| --- | --- | --- | --- |
| `hugohe3/ppt-master` | `f40fcf5` · 2026-05-19 | Native editable `.pptx` | Source -> Markdown -> design spec -> SVG pages -> SVG quality gate -> DrawingML PPTX |
| `zarazhangrui/frontend-slides` | `8dca834` · 2026-04-08 | Single-file HTML slides | Visual style discovery with 3 previews, strong viewport-fitting rules |
| `op7418/guizang-ppt-skill` | `6bfa520` · 2026-05-19 | Single-file HTML slides and covers | Two locked visual systems, strict layout IDs, validator and real-world QA checklist |
| `lewislulu/html-ppt-skill` | `f3a8435` · 2026-04-26 | Static HTML slides, PNG/PDF export | Large tokenized theme/layout/runtime library, presenter mode and render script |
| `zarazhangrui/beautiful-html-templates` | `68ae471` · 2026-05-18 | HTML template library | Template metadata registry, 3-candidate preview workflow, detailed `design.md` contracts |

Public sources:

- https://github.com/hugohe3/ppt-master
- https://github.com/zarazhangrui/frontend-slides
- https://github.com/op7418/guizang-ppt-skill
- https://github.com/lewislulu/html-ppt-skill
- https://github.com/zarazhangrui/beautiful-html-templates

## 4. Project-by-Project Analysis

### 4.1 `hugohe3/ppt-master`

#### What it is

`ppt-master` is the most relevant project for our editable PPTX requirement. It does not treat HTML as the final deck. Its core architecture is:

```text
source document
  -> source_to_md conversion
  -> project directory
  -> strategist phase
  -> design_spec.md + spec_lock.md
  -> per-page SVG authoring
  -> svg_quality_checker.py
  -> finalize_svg.py
  -> svg_to_pptx.py
  -> native-shape PPTX
```

The important point: SVG is an intermediate representation that the agent can visually author and debug, then the scripts translate SVG into native PowerPoint DrawingML shapes. This is materially different from embedding screenshots or SVG images into a deck.

#### What we should borrow

1. **Source intake layer**

   `ppt-master` has practical converters for PDF, DOCX/HTML/EPUB/IPYNB, Excel, existing PPTX, and web pages. Our current workflow mostly assumes the source has already been normalized into text. For books, reports, old decks, and URLs, this source intake layer is a real gap.

2. **Two design artifacts: human spec + machine lock**

   - `design_spec.md`: readable rationale, audience, style, color, typography, layout and content outline.
   - `spec_lock.md`: exact execution contract for colors, fonts, icons, images, page rhythm, chart choices, forbidden features.

   This directly maps to our `Visual Contract`, but is stricter and more automation-friendly. We should introduce a `visual-contract.yaml` or `spec-lock.md` equivalent for `deck-builder`.

3. **Single blocking confirmation point**

   The project asks for a bundled design confirmation once, then runs the rest of the pipeline without repeated interruption. This is better than our current "confirm `slide-plan.md` before deck.md" rule, which can block automation too early and too often.

4. **Anti-drift discipline**

   `ppt-master` forces the executor to re-read `spec_lock.md` per page. The purpose is to stop long decks from drifting in color, typography, icon style, page rhythm, and image treatment. We should adapt the same concept even when using Codex `Presentations`: generation prompts should explicitly re-assert the visual contract and forbid per-slide invention.

5. **Quality gate before export**

   Its SVG checker catches unsupported SVG features before PPTX conversion. We may not need the exact checker for Codex `Presentations`, but we need the same concept:

   - contract compliance check
   - render/contact-sheet check
   - overflow and font-size check
   - source/proof-object check
   - at least one fix-and-reverify loop

6. **Project artifact structure**

   `ppt-master` keeps sources, generated SVGs, exports, backups, notes, and specs separated. Our workflow should similarly define a repeatable deck work directory, rather than dropping `deck.md`, renders, and outputs loosely into the repo.

#### What not to copy blindly

- It is a heavy, strict serial pipeline. That is useful for high-value decks, but too much ceremony for quick PPTX drafts.
- It forbids batch/script generation of SVG pages. That makes sense for its SVG authoring model, but we should not impose that rule on Codex `Presentations`.
- Its skill is repo-specific. Until MD2PPT has a working proof of concept, treat it as a design and QA reference, not as a committed routing target.

#### Recommended role in our system

`ppt-master` should remain a **design reference candidate** for now.

Use it to inform:

- source normalization ideas
- `design_spec.md` + `spec_lock.md` separation
- SVG QA gate thinking
- anti-drift visual contracts
- repeatable deck project directories

Do not put `ppt-master` in the active Tool Routing table until a local PoC proves the adapter path.

### 4.2 `zarazhangrui/frontend-slides`

#### What it is

`frontend-slides` is an HTML presentation skill. It produces single-file, browser-run slides with strong animation and visual exploration. It is not an editable PPTX solution.

#### What we should borrow

1. **Show, don't tell style discovery**

   Instead of asking the user to describe a style in abstract words, it generates 3 visual previews and lets the user pick. This is useful for our visual contract selection stage.

2. **Viewport fitting rules**

   It has strict density and viewport rules: one slide equals one viewport, no scroll, split overflow content into multiple slides, constrain images, and use responsive sizing. For PPTX, the equivalent is: one slide equals one canvas, no overflow, split dense content, constrain proof objects, and inspect thumbnails.

3. **Content density limits**

   Its per-slide limits are a useful planner constraint. Our `PPTX Slide Planner` should add density warnings such as "this claim needs two slides" or "this proof object cannot share space with six bullets."

4. **Style preview folder**

   We can add an optional `previews/` stage where three title/section-page previews are generated before full PPTX generation. This is especially useful when the user cares about design language but cannot name a style.

#### What not to copy blindly

- Its output is HTML, not editable `.pptx`.
- It asks several user questions. In our global skill, those questions should be conditional rather than mandatory.
- It recommends web fonts and rich CSS motion; these do not map directly to PowerPoint editability.

#### Recommended role in our system

Use it as a **visual exploration and HTML prototype path**, not as the main PPTX path.

### 4.3 `op7418/guizang-ppt-skill`

#### What it is

`guizang-ppt-skill` is a strongly opinionated HTML deck skill with two visual systems:

- editorial magazine / electronic ink
- Swiss international style

Its strongest contribution is not breadth. It is discipline: locked layout IDs, style-specific checklists, image slot rules, and an actual validator for the Swiss mode.

#### What we should borrow

1. **Locked visual systems**

   The Swiss mode does not say "make it Swiss-ish." It requires a registered `data-layout="Sxx"` from a fixed layout set. This is exactly what many AI-generated slide workflows lack: a hard grammar.

   Our `design-profiles/` should evolve from loose style descriptions into executable contracts:

   - allowed layout families
   - required page chrome
   - typography hierarchy
   - image slot ratios
   - forbidden shortcuts
   - QA checks

2. **Validator mindset**

   Its validator checks layout IDs, experimental structures, text alignment traps, SVG text misuse, image-slot binding, and specific image cropping issues. We should build a comparable QA checklist for PPTX generation, even if some checks remain manual at first.

3. **Image slot contract**

   It decides image ratio and placement before image generation. This is important for our workflow:

   ```text
   slide claim -> proof object -> layout family -> image slot ratio -> image prompt or asset treatment
   ```

   Images should not be generated first and then squeezed into arbitrary slots.

4. **Screenshot treatment rules**

   It distinguishes screenshot preservation, screenshot beautification, screenshot redesign, and UI scenario images. This is useful for engineering project decks, where screenshots are common and should not be casually redrawn.

5. **Real QA checklist**

   The checklist records concrete failures: tiny fonts, navigation safety zones, over-centered titles, wrong image containers, SVG text labels, class names missing from templates. We should model our QA docs after this level of specificity.

#### What not to copy blindly

- It is HTML-first and not suitable as the default editable PPTX route.
- It has project-local personal paths in its golden-source notes. Those cannot be used as-is in a portable skill.
- Its style set is intentionally narrow. We should borrow the contract structure, not force every deck into its two styles.

#### Recommended role in our system

Use it as a **design-profile discipline reference** and an optional HTML/social-cover path.

### 4.4 `lewislulu/html-ppt-skill`

#### What it is

`html-ppt-skill` is a broad static HTML slide studio:

- 36 themes
- 31 single-page layouts
- 15 full-deck templates
- 27 CSS animations
- 20 canvas FX
- keyboard runtime
- presenter mode with current/next/script/timer
- headless Chrome PNG rendering

#### What we should borrow

1. **Tokenized theme/layout catalog**

   It separates base tokens, themes, layouts, runtime, and full-deck templates. This is a good model for organizing our design profiles and prompt templates.

2. **Presenter script support**

   It treats speaker notes and presenter mode as first-class. Our planner should ask whether the user needs:

   - slide-only deck
   - deck + speaker notes
   - deck + full talk script

3. **Scenario scaffolds**

   Full-deck templates such as pitch deck, product launch, tech sharing, weekly report, and course module are useful analogs for our `PPTX Slide Planner` presets.

4. **Render-to-PNG script**

   Its headless Chrome script is simple but effective for HTML. The principle applies to our PPTX route: always produce render previews or contact sheets, not only the final file.

#### What not to copy blindly

- Its trigger scope is broad and would conflict with our `deck-builder` unless routed carefully.
- HTML animations and presenter runtime do not translate to editable PPTX.
- It optimizes for web delivery, not PowerPoint-native editing.

#### Recommended role in our system

Use it as a **layout/theme catalog reference** and a **speaker-notes workflow reference**.

### 4.5 `zarazhangrui/beautiful-html-templates`

#### What it is

This is a template library rather than a deck generation engine. It has:

- `index.json` with template metadata
- one folder per visual system
- `template.json` for matching
- `design.md` for detailed visual contract
- screenshots for quick visual inspection
- an agent workflow that picks 3 candidates and generates title-slide previews

#### What we should borrow

1. **Template registry schema**

   Its `index.json` fields are exactly the kind of metadata our `design-profiles/` currently lack:

   - `mood`
   - `occasion`
   - `tone`
   - `formality`
   - `density`
   - `scheme`
   - `best_for`
   - `avoid_for`
   - `slide_count`

   We should add YAML frontmatter to each profile first. A generated index can come later if the profile library grows.

2. **3-candidate style preview**

   The workflow produces three title-slide previews with the user's real title before committing to a full deck. This is a strong improvement over asking users to choose from prose descriptions.

3. **Design contract depth**

   Its `design.md` files include palette, typography, spacing, components, layout grammar, and constraints. This is closer to what our `Visual Contract` should become.

4. **Preserve then extend**

   When a template lacks a needed slide, the agent must extend the same visual system rather than mixing in a different template. This rule should become part of our design profile contract.

#### What not to copy blindly

- It is HTML-only.
- It always asks the user to pick. For fully automated PPTX generation, we should allow the agent to choose a default when the user has not requested visual review.
- It is a template library, not a content planning system.

#### Recommended role in our system

Use it as the model for a **design-profile registry** and **visual preview selection layer**.

## 5. Synthesis: What This Means for MD2PPT

The external projects cluster into three categories:

| Category | Projects | Usefulness for us |
| --- | --- | --- |
| Native editable PPTX reference | `ppt-master` | High as design reference and future candidate; not an active route yet |
| HTML deck skills | `frontend-slides`, `guizang-ppt-skill`, `html-ppt-skill` | Medium. Strong design workflow and QA ideas, but not final editable PPTX |
| Visual template registry | `beautiful-html-templates` | High. Strong model for design profile indexing, preview selection, and contract depth |

The biggest lesson: our workflow should not be a single linear "Markdown -> PPTX" script. It should be a router with a shared planning/design layer and multiple output engines.

Shared core:

```text
Source Material
  -> Source Normalization
  -> PPTX Slide Planner
  -> deck.md
  -> Design Intelligence
  -> Visual Contract / spec lock
  -> Route to output engine
  -> Render QA
```

Output engines:

```text
Codex Presentations      -> primary editable PPTX
pptxgenjs               -> simple deterministic fallback
guizang-ppt-skill       -> primary HTML deck path for online sharing
html-ppt-skill          -> alternative HTML deck path for richer layouts / presenter mode
Marp                    -> quick draft / PDF path
```

## 6. Proposed Workflow Improvement

### 6.1 Add a repeatable deck project directory

For each real deck, create a working directory:

```text
deck-work/<slug>/
  sources/
  source.md
  slide-plan.md
  deck.md
  design-brief.md
  visual-contract.md
  spec-lock.yaml
  assets/
  previews/
  renders/
  qa.md
  outputs/
```

This makes each deck reproducible and lets other agents resume the work without reading the whole chat.

### 6.2 Add source normalization before slide planning

Borrow from `ppt-master`:

| Input | Normalization |
| --- | --- |
| PDF/book/report | convert/extract to Markdown, keep extracted images |
| DOCX/HTML/EPUB | convert to Markdown |
| Existing PPTX | extract text, images, notes |
| Web article | fetch to Markdown |
| Code repository | summarize README, architecture docs, key modules, screenshots |
| User-pasted text | write directly to `source.md` |

The planner should operate on `source.md`, not on raw fragmented inputs.

### 6.3 Upgrade `Visual Contract` into `spec-lock`

Current:

```text
design-profiles/<profile>.md
```

Recommended:

```text
design-profiles/<profile>.md
deck-work/<slug>/visual-contract.md
deck-work/<slug>/spec-lock.yaml
```

`spec-lock.yaml` should include:

```yaml
canvas:
  ratio: "16:9"
palette:
  background: "#..."
  text: "#..."
  primary: "#..."
  accent: "#..."
typography:
  title: "..."
  body: "..."
layout:
  density: "medium"
  allowed_families:
    - cover
    - claim-proof
    - comparison
    - architecture
    - timeline
images:
  policy: "preserve-user-screenshots"
  slots:
    - slide: 5
      ratio: "16:10"
      treatment: "screenshot-framing"
qa:
  forbidden:
    - invented metrics
    - generic card grid
    - unsupported logos
```

### 6.4 Add optional 3-preview design selection

When design quality matters and the user has not specified a visual profile:

1. Query `ui-ux-pro-max`.
2. Match 3 candidate design profiles using metadata.
3. Generate 3 lightweight previews:
   - title slide
   - one content slide
   - optional architecture/data slide
4. Let the user choose or let the agent pick if the user requested full automation.

This borrows from `frontend-slides` and `beautiful-html-templates`, but keeps our final route as editable PPTX.

### 6.5 Add route selection to the global skill

`deck-builder` should explicitly decide:

| User need | Route |
| --- | --- |
| "editable PPTX", Codex available | Codex `Presentations` |
| "editable PPTX", no Codex Presentations | `pptxgenjs` fallback when local `skills/pptx` exists |
| "web slides", "single HTML", "presenter mode" | HTML deck route |
| "social cover", "公众号头图", "小红书图文" | HTML/image route inspired by Guizang |
| "quick draft" | Marp or simple HTML |

### 6.6 Add QA levels

Define three QA levels:

| Level | When | Checks |
| --- | --- | --- |
| L1 quick | draft/internal | file opens, no missing slides, no obvious overflow |
| L2 standard | normal deliverable | contact sheet, per-slide preview, visual contract check, source check |
| L3 strict | client/high-stakes | L2 + data/source audit + accessibility/readability + one explicit fix-and-rerender cycle |

The global skill should default to L2 for professional PPTX.

## 7. Current `deck-builder` Implementation Status

### Implemented in the current revision

1. Rename the previous PPTX-only skill to `deck-builder` in canonical and global skill locations.
2. Add dependency resolution so the global skill works outside MD2PPT.
3. Keep slide-plan approval in interactive sessions and continue automatically only in batch/non-interactive contexts.
4. Remove the invalid reveal.js skill reference.
5. Add Request Boundary Check to avoid triggering the full pipeline for small existing-deck edits.
6. Add Output Router with PPTX primary, HTML secondary, and Marp quick-draft routes.
7. Add Template C for HTML deck generation.
8. Add `references/layout-vocabulary.md` with canonical layout names and partial engine mappings.
9. Add YAML frontmatter metadata to the five design profiles.

### Still future work

1. Add source normalization step before slide planning.
2. Add `spec-lock` / machine visual contract concept.
3. Add optional 3-preview design selection.
4. Add image-slot planning before any image generation.
5. Add QA levels and a reusable `qa.md` checklist.
6. Explore a `ppt-master` adapter only after a working local PoC exists.

## 8. Proposed Roadmap

### Phase 1: Stabilize the global skill

Goal: make `deck-builder` safe to trigger from any project.

Deliverables:

- dependency resolution rules
- corrected trigger and route table
- conditional confirmation rule
- valid fallback references
- sync canonical copy to global Claude/Codex skill directories

### Phase 2: Improve the design contract layer

Goal: make visual decisions searchable, repeatable, and enforceable.

Deliverables:

- metadata/frontmatter for each profile
- `spec-lock.yaml` template
- 3-candidate style preview protocol
- image-slot contract template

### Phase 3: Add source normalization

Goal: handle articles, books, PDFs, existing PPTX, and engineering repos consistently.

Deliverables:

- source normalization doc
- source normalization ideas from `ppt-master` converters or local equivalents
- `source.md` conventions
- engineering repo intake checklist

### Phase 4: Add optional output route docs

Goal: route to the best output engine without confusing the user.

Deliverables:

- Codex `Presentations` prompt update
- `pptxgenjs` fallback doc cleanup
- HTML deck route doc for web-only deliverables
- `ppt-master` PoC notes only if a working adapter exists

### Phase 5: Build QA automation

Goal: make "good-looking" and "editable" verifiable.

Deliverables:

- `qa.md` template
- contact-sheet requirements
- render preview checklist
- visual contract checklist
- data/source audit checklist

## 9. Current Recommendation

Do not replace our workflow with any one external project.

Recommended architecture:

```text
deck-builder = global orchestrator
ui-ux-pro-max = design intelligence
design-profiles + spec-lock = visual contract
Codex Presentations = primary editable PPTX engine
pptxgenjs = fallback editable PPTX path when available
guizang-ppt-skill = primary HTML deck path
html-ppt-skill = alternative HTML deck path
ppt-master = design reference candidate / future PoC
```

The strongest immediate improvement is to make our design profiles behave more like `beautiful-html-templates` metadata plus `ppt-master` `spec_lock.md`. That gives us better style matching, less drift, and a cleaner bridge to Codex `Presentations`, pptxgenjs, or HTML deck engines.
