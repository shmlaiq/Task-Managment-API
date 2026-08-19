# Book / Academic Textbook Structure (Variant E)

Read this when the Intake confirms the deliverable is a book/academic textbook, not a
research paper.

## Defaults (override if the user specifies otherwise)

- **Length**: 250–350 pages (~62,500–87,500 words at ~250 words/page)
- **Subtype**: academic/textbook
- **Structure**: Units/Chapters → Sections → Subsections
- **Citation style**: confirm with the user (APA / IEEE / Chicago — subject-area
  dependent); never assume

## Front matter

- Title page
- Preface (why this book, who it's for, how to use it)
- Table of contents

## Per-chapter structure (mandatory for every chapter)

```
Chapter N: [Title]
  Learning Objectives      — 3-5 bullet points, what the reader will be able to do
  [Body sections/subsections — the actual content]
  Chapter Summary           — 1 paragraph or bullet recap
  Review Questions          — 5-10 questions testing the chapter's objectives
```

## Back matter

- Glossary (define all domain-specific terms introduced)
- References/Bibliography (same citation-integrity rules as the paper skill: every
  entry cited inline, no `and others`, DOIs verified)
- Index

## Production flow

One chapter at a time, through the same 5-agent pipeline as a paper (Lead → parallel
Literature+Writing → Fact-Checker → Editor → Lead), with the loop-engineering cap
(max 4 draft-review-revise iterations, severity-gated exit, must converge each
iteration or escalate) applied per chapter. Maintain a running
outline/table of contents across chapters so the Lead Agent's final QA pass can catch:

- Terminology/notation drift between chapters
- Repeated content across chapters
- Uneven depth (some chapters much thinner than others relative to their weight in
  the table of contents)

## Model routing

- **Writing Agent (bulk drafting)**: reasonable to route to a faster/cheaper model —
  a book is volume-heavy, not precision-heavy in the way a single paper submission is
- **Fact-Checker Agent, Editor Agent, and any chapter with technically sensitive
  claims**: keep on the strongest available model
- Do not extend this cost-saving routing to research papers (Variant A–D) — those
  stay on the strongest model throughout

## Quality pillars — same five as the paper skill, per chapter

Replace "Section" with "Chapter" in the pre-writing checklist in the main SKILL.md.
The AI-detection disclosure note (Pillar 3) applies here too — a textbook publisher's
AI-use policy is a separate question from prose-naturalness targets; check it before
relying on Pillar 3 targets as sufficient.

## What differs from a research paper

| Aspect | Research Paper | Book/Textbook |
|---|---|---|
| Length driver | Venue page limit | Reader/curriculum need, 250-350pg default |
| Section rigidity | Fixed 13-section structure | Flexible chapter count, fixed per-chapter shape |
| Empirical rigor | Every claim [N]-cited or from own experiments | Same citation rigor, but more exposition/pedagogy allowed |
| Review model | Peer review (blind) | Publisher review or self-review |
| Reader assumption | Domain expert | Depends on target audience (state it in intake) |
