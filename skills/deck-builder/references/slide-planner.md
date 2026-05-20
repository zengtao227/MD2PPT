# Slide Planner

The slide planner is the mandatory layer between raw source material and deck.md. Its job is to decide what the deck should *argue* and *show*, not what it should *contain*.

Output: `slide-plan.md`. Do not write deck.md until the user confirms the plan.

---

## What the Planner Must Decide

| Field | Description |
|-------|-------------|
| `audience` | Who will see this deck: investors, engineers, executives, examiners, internal team |
| `goal` | What decision or understanding the audience should leave with |
| `thesis` | One sentence that the entire deck must prove |
| `arc` | Narrative path from problem → insight → evidence → conclusion |
| `slide-count` | Target number of main slides (typically 8–12; appendix is separate) |

---

## Per-Slide Planning

For each slide, define:

| Field | Description |
|-------|-------------|
| `claim` | A conclusion sentence — what the audience should believe after this slide |
| `proof-object` | The one visual or data object that proves the claim: chart, diagram, table, big number, case, quote |
| `layout-family` | Rough layout intent: hero-number, two-column, full-image, timeline, comparison, architecture-diagram, table |
| `source` | Where the proof object data comes from; write "user-provided" or "missing" if unknown |
| `missing` | Any data, asset, or logo that cannot be fabricated and must be provided by the user |

---

## Slide-Plan.md Template

```markdown
# Slide Plan: <Deck Title>

## Metadata
- Audience: <who>
- Goal: <what decision or understanding>
- Thesis: <one sentence>
- Arc: <problem → ... → conclusion>
- Slide count: <N main slides + appendix>

## Main Slides

### 01 Cover
- Claim: <conclusion sentence>
- Proof object: title + one-line thesis statement
- Layout family: hero-text
- Source: user-provided
- Missing: —

### 02 <Slide Title>
- Claim:
- Proof object:
- Layout family:
- Source:
- Missing:

[continue for each slide...]

## Appendix Plan
- <What content moves to appendix or speaker notes, and why>

## Omissions
- <Data or assets that are unavailable and must not be fabricated>
```

---

## Planner Questions by Input Type

### Article / Book / Knowledge Doc

Ask before planning:
1. What is the single most important thing the audience should remember?
2. Which observations are main deck vs. background context?
3. Which structures are visualizable: timeline, comparison, framework, causal chain, taxonomy?
4. Which numbers, quotes, or cases must keep their source?
5. If only 8 slides were allowed, what would be cut?

### Engineering Project

Ask before planning:
1. What real problem does this project solve?
2. Who is the audience: technical peers, business stakeholders, evaluators, future maintainers?
3. Which diagram best explains the system: architecture, data flow, call chain, deployment, workflow?
4. What measurable results exist: performance, cost, accuracy, coverage, stability?
5. Which technical trade-offs need explanation?

### Topic Only (no source material)

Ask before planning:
1. What outcome does the user need: business pitch, technical brief, educational talk, status report?
2. What is the audience's prior knowledge level?
3. What evidence is available vs. what must be flagged as missing?

---

## Common Planning Mistakes

| Mistake | Correction |
|---------|------------|
| Slide titles are topic labels ("Market Analysis") | Every title must be a conclusion sentence ("The market grew 40% YoY driven by mobile") |
| 3+ consecutive slides with the same layout family | Vary proof objects: mix chart, diagram, table, big number |
| Proof objects without a source | Mark as "missing" — never invent |
| Main deck contains background the audience already knows | Move to appendix or speaker notes |
| Slide count exceeds 14 without clear justification | Split into main deck + appendix, or reduce scope |
