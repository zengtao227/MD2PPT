# Engineering Project Deck

Use this reference when the source material is a project README, design doc, code repository, architecture document, or technical specification.

The goal is to help the audience quickly understand **why the project exists, what it does, how it works, and what it has achieved** — not to document every implementation detail.

---

## Core Principle

An engineering deck is NOT a README on slides. It is a narrative that earns the audience's trust in the project's value and execution.

Before planning, answer:
1. What real problem does this project solve?
2. Who is the audience: engineers, business stakeholders, investors, evaluators, future maintainers?
3. What is the single most impressive thing about this project?

The answer to (3) should be the thesis.

---

## Audience Calibration

| Audience | Emphasis | What to Minimize |
|----------|----------|-----------------|
| Engineers / peers | Architecture, data flow, technical trade-offs, code quality | Business context, ROI language |
| Business stakeholders | Problem, user impact, metrics, timeline, risks | Implementation details, stack choices |
| Investors | Market problem, differentiation, traction, roadmap | Low-level architecture |
| Evaluators / competition judges | Innovation, methodology, results, completeness | Obvious choices |
| Future maintainers | System boundaries, data model, key decisions, known risks | Marketing narrative |

---

## Extraction Checklist

From the project materials, extract:

- **Problem statement**: the specific pain point or gap that motivated the project
- **User / stakeholder**: who benefits and how
- **System boundary**: what is inside and outside this project
- **Core modules**: 3–6 main components and their relationships
- **Key data flows**: how data enters, transforms, and exits the system
- **Critical technical decisions**: architectural choices and their trade-offs
- **Measurable outcomes**: performance, cost, accuracy, coverage, stability, latency, throughput
- **Risks and limitations**: known constraints or open problems
- **Next steps**: what comes after current state

For diagrams, identify which type best explains the system:

| Diagram Type | Best For |
|-------------|----------|
| Architecture diagram | Component relationships, system boundaries |
| Data flow diagram | How data moves through the system |
| Sequence / call chain | Request lifecycle, API interactions |
| Deployment diagram | Infrastructure, environments, scaling |
| Workflow / state machine | Process logic, decision paths |

---

## Recommended Deck Structure

| Slide | Role |
|-------|------|
| 01 | Cover: project name + value proposition in one line |
| 02 | Problem: why this needed to be built |
| 03 | User / use case: who uses it and in what scenario |
| 04 | Solution overview: how it addresses the problem |
| 05 | System architecture: the diagram that best explains the whole |
| 06 | Core workflow / data flow: how it actually runs |
| 07 | Key technical decisions and trade-offs |
| 08 | Results / metrics / demo evidence |
| 09 | Risks, limitations, and next steps |
| 10 | Decision ask / collaboration / Q&A |

Adjust for audience: for engineers, expand slides 05–07; for business stakeholders, expand slides 02–04 and 08; for investors, expand 02 and 10.

---

## deck.md Structure for Engineering Decks

```markdown
# <Project Name>

## Metadata
- Audience: <engineers / stakeholders / investors / evaluators>
- Goal: <what the audience should understand or decide>
- Length: <N slides>
- Tone: <technical / strategic / pitch>

## Thesis
<One sentence — the most important claim about what this project achieves>

## Slides

### 01 Cover
- Claim: <value proposition in one sentence>
- Proof object: project name + thesis line
- Source: user-provided

### 02 Problem
- Claim: <why the status quo is insufficient and this problem matters>
- Proof object: one data point, failure case, or before-state description
- Source: <cite or "user-provided">

### 03 Use Case
- Claim: <who uses this and what they can now do that they couldn't before>
- Proof object: user journey or scenario description
- Source: user-provided

### 04 Solution Overview
- Claim: <how this project directly resolves the problem>
- Proof object: high-level solution diagram or 3-part mechanism
- Source: derived from project

### 05 Architecture
- Claim: <what architectural principle or boundary makes this system robust>
- Proof object: architecture diagram (editable shapes, not screenshot)
- Source: project design docs / user-provided

### 06 Core Workflow
- Claim: <what makes the core execution path reliable or efficient>
- Proof object: data flow or sequence diagram
- Source: project codebase / docs

### 07 Technical Decisions
- Claim: <why the key trade-offs made here were the right calls>
- Proof object: comparison table or decision matrix
- Source: derived / user-provided rationale

### 08 Results
- Claim: <what measurable improvement this project delivered>
- Proof object: metrics table or big-number layout (performance, cost, accuracy, etc.)
- Source: <measurement methodology and data source>

### 09 Risks and Next Steps
- Claim: <what is known to be incomplete or uncertain, and what happens next>
- Proof object: risk list + roadmap items
- Source: derived

### 10 Decision / Q&A
- Claim: <what the audience needs to decide or do>
- Proof object: ask statement or contact / repo link
- Source: user-provided

## Appendix Plan
- <Detailed data tables, extended architecture sub-diagrams, codebase structure>

## Omissions
- <Metrics not yet measured, features not yet built, risks not yet quantified>
```

---

## Diagram Guidelines

When requesting diagrams from the generation engine:

- All diagrams must use **editable shapes and connectors**, not embedded screenshots or images
- Connection lines must carry semantic meaning — do not use decorative arrows
- Label every node and every arrow that carries a meaningful relationship
- Limit nodes per diagram to 8–10 for readability; split complex systems across two slides
- Use consistent shape conventions within a deck: boxes = services, cylinders = storage, diamonds = decisions

---

## Quality Gates Before Handing to Generation

- [ ] Every slide title is a conclusion sentence, not a section label
- [ ] The architecture/flow diagram is specified as editable shapes (not a screenshot request)
- [ ] Every metric has a stated source and measurement method
- [ ] Unavailable data is marked "missing" — not fabricated
- [ ] Audience calibration is reflected in which slides receive more depth
