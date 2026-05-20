# Layout Vocabulary

Canonical layout names used across this pipeline. Generation engines receive these names as intent; the engine mapping columns show the closest equivalent in each system.

Use these names in `slide-plan.md` under `layout-family`.

---

## Canonical Layout Names

| Canonical Name | Purpose | guizang-ppt-skill | html-ppt-skill | Codex Presentations |
|----------------|---------|-------------------|----------------|---------------------|
| `hero-text` | Cover or opener — large title, minimal body | S01 Index Cover / SWISS-COVER-ASCII | `cover` | "Full-bleed or high-contrast title slide with subtitle and metadata" |
| `hero-number` | Single dominant metric as proof object | S06 KPI Tower / S20 Stacked KPI Ledger / S21 Tech Spec Sheet | `stat-highlight` / `kpi-grid` | "Oversized number, short context, direct annotation" |
| `two-column` | Split layout — claim left, proof object right | S03 Split Statement / S08 Duo Compare | `two-column` | "Two-column layout, one side text and one side visual/proof object" |
| `three-panel` | Three parallel insights or comparison points | S05 Three Layers / S13 Three Forces | `three-column` | "Three aligned panels with equal visual weight" |
| `table` | Structured data table, decision matrix, or spec sheet | S16 Multi-card Brief / S21 Tech Spec Sheet | `table` | "Editable comparison/spec table with clear header row and compact notes" |
| `timeline` | Horizontal or vertical sequence of events | S02 Vertical Timeline + KPI / S11 Horizontal Timeline | `timeline` / `roadmap` / `gantt` | "Timeline or roadmap with 4-6 labeled milestones" |
| `architecture-diagram` | System component map — boxes, stores, connectors | S17 System Diagram | `arch-diagram` / `flow-diagram` | "Architecture diagram with editable shapes and labeled connectors" |
| `comparison` | Before/after or A vs B side-by-side contrast | S08 Duo Compare / S03 Split Statement | `comparison` / `pros-cons` / `diff` | "Two-panel comparison with mirrored structure" |
| `quote` | Pull quote or attributed statement as proof object | S09 Dot Matrix Statement / S12 Manifesto + Ink Banner | `big-quote` | "Large quote or thesis statement with attribution below" |
| `full-image` | Dominant visual — photo, screenshot, or generated image | S22 Image Hero | `image-hero` / `image-grid` | "Image-dominant slide with restrained caption or overlay" |
| `bullet-list` | Vertical list of 3-5 points | S04 Six Cells / S16 Multi-card Brief | `bullets` | "Title plus short list; no dense paragraphs" |
| `framework` | Matrix, loop, ecosystem, or multi-part model | S14 Loop Form / S15 Matrix + Hero Stat / S17 System Diagram | `mindmap` / `process-steps` | "Structured framework diagram where relationships are the proof object" |
| `data-chart` | Chart-dominant slide — bar, line, pie, radar, scatter | S07 Horizontal Bar / S06 KPI Tower / S20 Stacked KPI Ledger | `chart-bar` / `chart-line` / `chart-pie` / `chart-radar` | "Chart-first slide with direct labels and no unnecessary legend" |
| `section-opener` | Visual divider between deck sections | S09 Dot Matrix Statement / S12 Manifesto + Ink Banner | `section-divider` | "Section divider with number, title, and short transition sentence" |
| `action-close` | Closing slide — ask, next steps, contact, or takeaway | S10 Split Closing / SWISS-CLOSING-ASCII | `cta` / `thanks` | "Closing ask with next action and optional contact/details" |

---

## Engine Coverage Notes

**guizang-ppt-skill (S01–S22)**
- Full Swiss International layout library (22 layouts); confirmed design-system match with MD2PPT's 5 design profiles
- Mapping above uses the registered Swiss layout names where they are semantically close. Some concepts, such as dense tables, are represented by the nearest structured brief/spec layout rather than a literal table slide.
- Layout names in guizang follow the `S##` slot convention

**html-ppt-skill (31 named layouts)**
- 36 themes, 31 named layouts, 47 animations, BroadcastChannel presenter mode
- Layout names above use the public single-page layout names from html-ppt-skill's layout catalog.
- Use as alternative HTML engine when guizang layouts are insufficient or a non-Swiss theme is needed

**Codex Presentations**
- No fixed slot names; the engine interprets descriptive layout intent from the prompt
- Use the quoted descriptions in the table as the layout-family value in the prompt template
- Match the description to the proof object type — a chart slide gets a different description than a quote slide

**ppt-master (not mapped)**
- ppt-master uses an SVG → DrawingML native PPTX pipeline; it is not a routing target for this skill
- Tracked in ROADMAP only; do not assign canonical layout names for ppt-master until a PoC is completed

---

## How to Use in slide-plan.md

```markdown
### 05 Architecture
- Claim: The three-layer separation enables independent scaling of each service.
- Proof object: architecture diagram — three boxes (API / Core / Storage) with labeled connectors
- Layout family: architecture-diagram
- Source: project design doc
- Missing: —
```

---

## Layout Anti-Patterns

| Anti-Pattern | Canonical Fix |
|-------------|---------------|
| 3+ consecutive slides with `three-panel` | Break with `hero-number`, `data-chart`, or `comparison` |
| Proof object is a list but layout is `three-panel` | Change layout to `bullet-list` |
| Architecture diagram on a `two-column` layout | Use `architecture-diagram` — connectors need full width |
| Cover slide using `bullet-list` | Use `hero-text` |
| Data metric buried in `bullet-list` | Promote to `hero-number` |
