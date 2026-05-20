# Design Workflow: Intelligence → Visual Contract

This reference covers Steps 4 and 5 of the pipeline: running `ui-ux-pro-max` to generate design intelligence, then selecting and applying a design profile from `design-locks/`.

---

## Layer Roles (Do Not Confuse)

| Layer | Tool / File | Role | What It Is NOT |
|-------|-------------|------|----------------|
| Design Intelligence | `skills/ui-ux-pro-max` | Generates design direction: style, palette, typography, chart grammar, UX risks | NOT a PPTX generator |
| Visual Contract | `design-locks/*.md` | Locks the chosen visual language as hard constraints: hex values, fonts, layout rules | NOT a slide template or generation engine |
| Generation | Codex Presentations / pptxgenjs / HTML engine | Produces the actual PPTX or HTML deck using the above as constraints | Takes both as input |

---

## Dependency Resolution

Before running commands, resolve the `ui-ux-pro-max` search script:

```bash
if [ -f "skills/ui-ux-pro-max/scripts/search.py" ]; then
  UIUX_SEARCH="skills/ui-ux-pro-max/scripts/search.py"
elif [ -f "$HOME/.codex/skills/ui-ux-pro-max/scripts/search.py" ]; then
  UIUX_SEARCH="$HOME/.codex/skills/ui-ux-pro-max/scripts/search.py"
elif [ -f "$HOME/.claude/skills/ui-ux-pro-max/scripts/search.py" ]; then
  UIUX_SEARCH="$HOME/.claude/skills/ui-ux-pro-max/scripts/search.py"
else
  UIUX_SEARCH=""
fi
```

If `UIUX_SEARCH` is empty, skip tool execution and write a concise design intelligence brief from the source material. Explicitly note that `ui-ux-pro-max` was unavailable.

For visual contracts, use `design-locks/` only when it exists in the active project. If it does not exist, write a minimal `## Design Contract` block directly in `deck.md` with palette, typography, layout grammar, and forbidden items.

---

## Step 4 — Running Design Intelligence

### Primary Query (run when `UIUX_SEARCH` is available)

Use `--design-system` to get a consolidated brief across all domains:

```bash
python3 "$UIUX_SEARCH" "<industry + deck type + audience>" \
  --design-system \
  --format markdown \
  --project-name "<deck title>"
```

### Supplemental Queries (run as needed)

```bash
python3 "$UIUX_SEARCH" "<industry>" --domain product
python3 "$UIUX_SEARCH" "<visual tone>" --domain style
python3 "$UIUX_SEARCH" "<font character>" --domain typography
python3 "$UIUX_SEARCH" "<Chinese or Latin font>" --domain google-fonts
python3 "$UIUX_SEARCH" "<industry/scenario>" --domain color
python3 "$UIUX_SEARCH" "<chart type>" --domain chart
python3 "$UIUX_SEARCH" "layout spacing contrast accessibility" --domain ux
```

### Common Search Terms by Deck Type

| Deck Type | Search Term |
|-----------|-------------|
| Tech / SaaS / startup | `saas tech startup product` |
| Finance / investment | `fintech investment finance` |
| AI / data / research | `ai data research analytics` |
| Healthcare | `healthcare medical clinical` |
| Education / competition | `education competition academic professional` |
| Consumer brand | `brand consumer beauty retail` |
| Internal / culture | `corporate internal culture communication` |
| Data report | `trend comparison metrics dashboard timeline` |

### Translating ui-ux-pro-max Output to Deck Language

The tool's output is calibrated for Web/UI contexts. For PPTX, apply these translations:

| ui-ux-pro-max Output | PPTX Equivalent |
|----------------------|-----------------|
| Hero section / large headline | Cover or section opener slide |
| Feature cards grid | Parallel insights layout — avoid generic 3-up card grids |
| Scroll animation / motion-driven design | Section rhythm, transition pacing, chapter openers |
| CTA button | Action recommendation slide |
| Dashboard metrics | Big-number slide with inline annotations |
| Sidebar / nav | Appendix indicator or progress bar |
| Micro-interactions | Reserved for Codex Presentations render quality |

### Design Intelligence Brief Format

Distill the query output into this 5-field brief (append to deck.md or keep in workspace):

```markdown
## Design Intelligence
- Style: <Swiss Modernism / Editorial / Linear dark / Warm minimal / ...>
- Palette direction: primary / accent / background / foreground / muted / border (as semantic roles)
- Typography: <Chinese font> + <Latin font> — rationale
- Chart grammar: trend → line, ranking → horizontal bar, comparison → before/after or table
- UX risks: <contrast issues, title overflow, card clutter, footer collision — specific to this deck>
```

---

## Step 5 — Selecting the Visual Contract

### Available Design Profiles

| Profile File | Style | Best For |
|-------------|-------|----------|
| `swiss-klein-blue.md` | Swiss International, Klein Blue accent | Business plan, product roadmap, competition defense, execution report |
| `linear-dark.md` | Dark background, engineering precision | SaaS product, technical platform, investor deck |
| `guizang-indigo.md` | Indigo, cold tech / research feel | Technical proposal, data report, AI project introduction |
| `guizang-monocle.md` | Warm paper, editorial narrative | Business pitch, course presentation, opinion-driven deck |
| `notion-warm.md` | Warm white, approachable minimal | Internal report, culture deck, lightweight presentation |

### Selection Rules

| Situation | Profile |
|-----------|---------|
| Investor / business decision-maker audience | `swiss-klein-blue` or `linear-dark` |
| Technical, AI, data, or competition | `guizang-indigo` or `swiss-klein-blue` |
| Course, internal, culture, or explanatory | `guizang-monocle` or `notion-warm` |
| Client has a brand color | Pick the closest profile, use brand color as limited accent — do not rewrite the full visual system |

### Design Contract Block

After selecting a profile, append this block to deck.md:

```markdown
## Design Contract
- Profile: design-locks/<profile-name>.md
- Must keep: profile hex values, typography hierarchy, straight-edge grid grammar
- May adapt: layout families to match content proof objects
- Must avoid: gradients, generic card grids, invented logos, unsupported metrics
```

### Handling Mismatch Between Intelligence and Profile

If `ui-ux-pro-max` suggests a direction that conflicts with the selected profile:

1. Keep the profile as the hard constraint — it is the visual contract
2. Use the intelligence output to inform proof object choices (chart type, data density, visual hierarchy)
3. Translate dynamic Web suggestions (motion, scroll) into structural deck choices (pacing, section dividers, varied layouts)

Do not override a profile's hex values or typography hierarchy based on intelligence output alone.

---

## Anti-Patterns to Enforce

| Anti-Pattern | Rule |
|-------------|------|
| 3+ consecutive slides with the same layout | Enforce layout variety: mix hero-number, two-column, diagram, table |
| Generic SaaS card grid (3 items in boxes) | Replace with claim-focused layout tied to the specific proof object |
| Gradients or shadows not in the profile | Refuse — return to flat, profile-defined color system |
| New colors introduced mid-deck | Flag as profile violation — lock to existing palette roles |
| Low-contrast text on background | Enforce WCAG AA minimum (4.5:1 for body text) |
| Title that is a noun phrase | Replace with a conclusion sentence |
