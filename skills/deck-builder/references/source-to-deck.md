# Source-to-Deck: Article / Book / Knowledge Document

Use this reference when the source material is an article, book chapter, research paper, interview transcript, or any knowledge-driven text.

The key task is **extraction and restructuring**, not compression or summarization. The output should argue a thesis, not recap the source.

---

## Core Principle

A knowledge deck is NOT a summary of the source. It is a persuasive argument built from the source's best evidence.

Before writing anything, identify:
1. The source's central claim or finding
2. The 3–5 supporting observations or insights that are genuinely worth communicating
3. The evidence, data, cases, or quotes that make those insights credible
4. The structures that can be visualized: timelines, comparisons, frameworks, causal chains, taxonomies, hierarchies

---

## Extraction Checklist

Work through the source and extract:

- **Central thesis**: one sentence
- **Key insights**: 3–5 observations (not summaries of sections)
- **Evidence objects**: data points, statistics, case studies, quotes with attribution
- **Visualizable structures**: any list, sequence, comparison, or relationship that can become a chart or diagram
- **What to cut**: background knowledge the audience already has; methodology details that don't affect conclusions; tangential examples

---

## Recommended Deck Structure

| Slide | Role |
|-------|------|
| 01 | Cover: topic + one-line thesis |
| 02 | Why this topic matters now (problem / context) |
| 03 | Framework or structure (but title must be a conclusion, not a label) |
| 04–07 | Key insights, one per slide: claim + proof object |
| 08 | Synthesis model, methodology summary, or "so what" diagram |
| 09 | Implications or action recommendations for the audience |
| 10+ | Appendix: source quotes, detailed data, extended reading |

Adjust slide count to the source's density. A short article may need only 6 slides. A full book summary may need 12–14.

---

## deck.md Structure for Knowledge Decks

```markdown
# <Deck Title>

## Metadata
- Audience: <who>
- Goal: <what the audience should understand or decide>
- Length: <N slides>
- Tone: <professional / educational / pitch / internal>

## Thesis
<One sentence — the most important claim this deck makes>

## Slides

### 01 Cover
- Claim: <thesis in one punchy sentence>
- Proof object: title + thesis line
- Source: original work title / author

### 02 Why This Matters
- Claim: <why the audience should care about this topic>
- Proof object: one data point, trend, or problem statement
- Source: <cite>

### 03 <Framework / Structure Slide>
- Claim: <conclusion the framework illustrates — not just "here are 4 things">
- Proof object: framework diagram or structured list with visual hierarchy
- Source: <cite or "derived from source">

### 04 <Key Insight 1>
- Claim: <what the audience should believe after this slide>
- Proof object: <chart / quote / case / number>
- Source: <cite>

[repeat 04 pattern for each key insight...]

### 08 Synthesis
- Claim: <what all the evidence together implies>
- Proof object: model diagram / summary framework / before-after
- Source: derived

### 09 Implications
- Claim: <what the audience should do or think differently>
- Proof object: action list or decision matrix
- Source: derived

## Appendix Plan
- <What moves to appendix: raw data, full quotes, methodology, extended examples>

## Omissions
- <Data or claims that could not be verified from the source>
```

---

## Translation Rules: Web/UI → Deck Language

When using `ui-ux-pro-max` design output for a knowledge deck, translate as follows:

| ui-ux-pro-max output | Deck equivalent |
|----------------------|-----------------|
| Hero section / large headline | Cover slide or section opener |
| Feature cards grid | Parallel insights layout (avoid 3-up card grids — use claim-focused layouts instead) |
| CTA button | Call-to-action slide / action recommendation |
| Scroll animation / motion | Slide transition pacing / section rhythm |
| Sidebar navigation | Appendix or progress indicator |
| Dashboard metrics | Data slide with big-number proof objects |

---

## Quality Gates Before Handing to Generation

- [ ] Every slide title is a conclusion sentence, not a topic label
- [ ] No slide contains more than one primary proof object
- [ ] Every number, quote, or case has an attributed source (or is marked "missing")
- [ ] No data has been invented to fill gaps
- [ ] Appendix plan captures what was deliberately excluded from the main deck
