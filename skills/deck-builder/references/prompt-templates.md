# Prompt Templates

Ready-to-use generation prompts for the three supported output paths. Fill in `<...>` placeholders before sending.

Before using any template, resolve file paths from the active project. Do not include a file in the prompt unless it exists. Outside MD2PPT, omit `docs/pptx-master-workflow.md` and rely on this skill's references instead.

---

## Template A — Codex Presentations (Primary Path)

Use this when working inside Codex with the Presentations plugin available.

```
I want to generate a high-quality, editable PowerPoint deck.

Use the Codex Presentations skill / plugin as the primary workflow.
Generation engine: artifact-tool presentation JSX.
Do NOT use pptxgenjs, Marp, or Google Slides as the primary generation path.

[Input Files]
- Content source: <resolved path to deck.md>
- Design profile: <resolved design profile path, or inline visual contract if no profile file exists>
- Workflow reference: <optional resolved docs/pptx-master-workflow.md when working inside MD2PPT>

[Output Target]
- Final PPTX: outputs/<deck-title>.pptx
- Scratch / preview / layout / QA files: keep inside Presentations workspace
- Only the deliverable PPTX goes into outputs/

[Narrative Requirements]
- First, write a claim spine from deck.md: thesis, audience, one-line arc, per-slide claim, proof object, source
- Every slide title must be a conclusion sentence — not a topic label
- Do not fabricate numbers, clients, sources, logos, or brand assets
- Missing data must be noted in source notes or omission notes

[Design Requirements]
- Read the design profile; apply its hex values, typography, layout rules as hard constraints
- Apply ui-ux-pro-max design intelligence to select chart types and layout families
- Build a design system: background, fonts, palette, chart grammar, page numbers, footnotes, kicker, layout families
- Do not use the same major layout on 3 or more consecutive slides
- Avoid generic SaaS card grids; give each slide a distinct proof object

[Build Requirements]
- Use editable text, shapes, lines, tables, and charts throughout
- Charts must use direct annotation — minimize or eliminate legends
- Architecture and flow diagrams must use semantic connectors, not decorative arrows
- Every node and every labeled connector must be editable

[QA Requirements]
- Render per-slide preview images
- Generate a contact sheet (thumbnail grid)
- Generate layout JSON; review for overflow, font issues, spacing
- Use the Presentations comeback rubric for self-assessment
- Complete at least one "find issue → fix → re-render" cycle
- Final reply must include: PPTX absolute path, QA evidence, remaining risks for human review
```

---

## Template B — Claude Code / pptxgenjs (Fallback Path)

Use this when Codex Presentations is not available — e.g., in Claude Code or offline.

```
Use this repository's skills/pptx/SKILL.md pptxgenjs workflow to generate an editable PPTX.

[Input Files]
- Content source: <resolved path to deck.md>
- Design profile: <resolved design profile path, or inline visual contract if no profile file exists>

[Output Target]
- Final PPTX: outputs/<deck-title>.pptx

[Narrative Requirements]
- Before writing any pptxgenjs code, produce a claim spine:
  thesis / audience / one-line arc / per-slide claim / proof object / source
- Every slide title must be a conclusion sentence — not a topic label
- Do not fabricate numbers, clients, logos, or missing data

[Design Requirements]
- Read the design profile; apply hex values, font names, and layout rules as hard constraints
- Do not introduce colors, fonts, or gradients not present in the profile
- Vary layout families across slides — do not repeat the same layout 3 times in a row

[Build Requirements]
- Use editable pptxgenjs text boxes, shapes, lines, and tables throughout
- No embedded screenshots as proof objects unless user explicitly provides image files
- Keep chart code compact; use direct data labels instead of chart legends where possible

[QA Requirements]
- After generating the PPTX, run the local thumbnail script only if it exists: `python3 skills/pptx/scripts/thumbnail.py outputs/<deck-title>.pptx`
- Review thumbnails for: text overflow, font substitution, layout collision, color violations
- Fix at least one identified issue and regenerate before declaring done
- Final reply must include: PPTX absolute path, thumbnail path, remaining risks for human review
```

---

## Template C — HTML Deck (guizang-ppt-skill / html-ppt-skill)

Use this when the target output is an HTML presentation for online sharing — not when an editable PPTX is required.

**Primary engine:** guizang-ppt-skill (same design system as the 5 MD2PPT profiles, S01–S22 Swiss layouts)
**Alternative engine:** html-ppt-skill (36 themes, 31 named layouts, BroadcastChannel presenter mode)

Use html-ppt-skill when the deck needs: richer layout variety beyond S01–S22, a specific non-Swiss theme, or live presenter mode.

```
Use [guizang-ppt-skill / html-ppt-skill] to generate an HTML presentation deck.

[Input Files]
- Content source: <resolved path to deck.md>
- Design profile: <resolved design profile path, or inline visual contract if no profile file exists>

[Output Target]
- Final HTML: outputs/<deck-title>.html

[Narrative Requirements]
- Before writing any HTML, produce a claim spine:
  thesis / audience / one-line arc / per-slide claim / proof object / source
- Every slide title must be a conclusion sentence — not a topic label
- Do not fabricate numbers, clients, logos, or missing data

[Design Requirements]
- guizang-ppt-skill: select layouts from S01–S22 library; apply design profile colors as CSS variables; maintain Swiss grid grammar
- html-ppt-skill: select from 31 named layouts; choose the closest matching theme from 36 available; apply profile accent color
- Vary layout families — do not repeat the same layout 3 times in a row
- Do not introduce colors not in the design profile

[Build Requirements]
- All slides must be self-contained in the output HTML file
- Include speaker notes in the slide notes area where applicable
- html-ppt-skill: enable presenter mode (BroadcastChannel) if the deck will be presented to a live audience

[QA Requirements]
- Open the HTML file in a browser and verify all slides render at 16:9 aspect ratio
- Check for text overflow and layout collisions in full-screen mode
- Verify consistent visual rhythm across slides — no abrupt style break
- Final reply must include: HTML absolute path, engine used, any layout risks for human review
```

---

## Iteration Feedback Templates

Use these when the generated deck needs revision. Specify page number and expected outcome — do not use vague requests like "make it better."

| Problem | Feedback Template |
|---------|------------------|
| Title is a topic label | `Slide <N> title: change to a conclusion sentence that states why <topic> matters.` |
| Repeated layout | `Slides <N> and <M> both use three-card layout. Keep slide <N>, change slide <M> to <timeline / comparison / big-number / diagram>.` |
| Weak data slide | `Slide <N>: make the primary metric the proof object — <N>pt number, two lines of context on the right. Remove the four small cards.` |
| Too much text | `Slide <N>: compress body to 3 sentences, max 16 Chinese characters per line.` |
| Unclear chart | `Slide <N>: remove the chart legend, apply direct annotation. Reduce x-axis labels to 4 values.` |
| Profile violation | `Slide <N> introduced a gradient not in the design profile. Return to <profile name>'s flat color system.` |
| Invented data | `Slide <N> contains a metric with no cited source. Replace with "pending measurement" or remove.` |

---

## Render QA Checklist

After generation, verify all of the following:

**Contact Sheet**
- [ ] All slides visible as thumbnails
- [ ] Consistent visual rhythm — no abrupt style break between slides
- [ ] Section openers visually distinct from content slides

**Full-Size Preview**
- [ ] No title text wraps awkwardly onto a third line
- [ ] No body text overflows its container
- [ ] Charts and diagrams are legible at slide scale
- [ ] Footer and page number do not collide with content

**PowerPoint File**
- [ ] All text boxes are editable
- [ ] All shapes and connectors are native objects (not images)
- [ ] Chinese fonts render correctly or have a documented fallback

**Content**
- [ ] No fabricated numbers, company names, or logos
- [ ] All "missing" items are explicitly flagged
- [ ] Thesis claim appears on slide 01 or 02

---

## Generation Engine Quick Reference

| Environment | Primary Engine | Fallback | Quick Draft / PDF |
|-------------|----------------|----------|-------------------|
| Codex | Presentations + artifact-tool presentation-jsx | — | Marp (not editable PPTX) |
| Claude Code | skills/pptx + pptxgenjs | — | Marp |
| Offline / local | skills/pptx + pptxgenjs | — | Marp |
| HTML online sharing | guizang-ppt-skill | html-ppt-skill | Browser print / PDF export |
| Need Google Slides | Generate PPTX first → import via Google Drive | — | — |
