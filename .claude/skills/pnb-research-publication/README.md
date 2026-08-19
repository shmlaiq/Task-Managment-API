# pnb-research-publication

Claude Code skill for writing publication-ready IEEE research papers **and**
academic/technical books/textbooks, using a 5-agent pipeline with a
convergence-gated draft-review-revise loop ("loop engineering").

## What it does

1. **Intake gate (Question 0, mandatory)** — before any writing starts, confirms
   whether the deliverable is a research paper or a book/textbook. The two have very
   different length/structure requirements, so this is a hard gate, not a suggestion.
2. **Research paper path (Variants A–D)** — regular paper, survey/review, rebuttal,
   or domain-specific (CS/AI, EE, Robotics, Comms) conventions. Default 15 pages if
   the venue isn't specified.
3. **Book path (Variant E)** — academic/technical textbook, chapter-based, default
   250–350 pages. Each chapter: Learning Objectives → body → Chapter Summary →
   Review Questions, plus glossary/references/index as back matter.
4. **5-agent workflow** — Lead → (Literature + Writing, parallel) → Lead merges →
   Fact-Checker → Editor → Lead final QA.
5. **Loop engineering** — the Fact-Checker ↔ Lead resolution loop is
   severity-gated and convergence-checked, not just "try N times":
   - Issues are tagged **Critical / Major / Minor**. Exit requires Critical=0 AND
     Major=0 — Minor issues don't block delivery.
   - Each iteration's (Critical+Major) count must **strictly decrease** from the
     last. If it doesn't, the loop stops immediately (even before the cap) and
     **escalates to the user** with the specific unresolved items — it never
     auto-clears or silently ships an unresolved draft.
   - Hard cap: **4 iterations** per section/chapter, no exceptions.
   - Every iteration's findings report is kept, not overwritten — full audit trail.
6. **5 quality pillars** — anti-hallucination, anti-plagiarism, anti-AI-detection
   (with a disclosure note — see below), humanized tone, citation integrity.
7. **Model routing** — research papers always use the strongest available model
   (Opus) throughout, given their higher reputational stakes. Books may route bulk
   drafting (Writing Agent) to a faster/cheaper model, while Fact-Checker, Editor,
   and any technically sensitive chapter stay on the strongest model.

## Important note — AI-detection pillar vs. disclosure policy

Pillar 3 (`references/anti-ai-detection.md`) targets prose *naturalness*, not
compliance. Many venues now require disclosing AI assistance regardless of how the
prose reads. **Check the target venue's current AI-use policy before submission and
disclose if required** — passing the detector-evasion targets is not the same thing
as being compliant with a disclosure requirement.

## File map

```
SKILL.md                                — entry point: intake, variants, workflow, pillars
README.md                               — this file
references/
  paper-structure.md                    — per-section requirements for research papers
  book-structure.md                     — Variant E: chapter shape, defaults, model routing
  ieee-formats.md                       — LaTeX / IEEEtran formatting rules
  writing-standards.md, writing-rules.md — prose quality rules
  agent-workflow.md                     — full 5-agent pipeline, loop engineering detail
  domain-specific.md                    — CS/AI, EE, Robotics, Comms conventions
  survey-paper.md, rebuttal.md          — Variant B, Variant C specifics
  figures-design.md, math-notation.md, visual-design.md — visual elements
  anti-hallucination.md                 — Pillar 1
  anti-plagiarism.md                    — Pillar 2
  anti-ai-detection.md                  — Pillar 3 (+ disclosure note)
  pillar4-humanized-tone.md             — Pillar 4
  pillar5-citation-integrity.md         — Pillar 5
  audit-commands.md, submission-checklist.md, grade-paper.md — final QA tools
```

All 19 reference files are cross-checked against SKILL.md's reference table — every
file listed there exists, and no file exists that isn't referenced.

## Change history

- **Base skill**: mature `research-paper` skill (5-agent workflow, IEEE rigor,
  18 reference files) — original author's work, uploaded as `research-paper.zip`.
- **v2 — book handling added**: Intake gate made mandatory-first; Variant E
  (academic textbook/book) added with its own reference file; paper-type table
  updated with book defaults (250–350 pages); model routing guidance added;
  scope boundary updated so academic/technical books are handled here instead of
  redirecting to a book-creator skill.
- **v2 — renamed**: `research-paper` → `pnb-research-publication`.
- **v3 — loop engineering strengthened**: Fact-Checker findings report changed
  from binary CLEAR/BLOCKED to severity-tagged (Critical/Major/Minor); added a
  convergence check (issue count must strictly decrease each iteration or the loop
  escalates to the user instead of continuing); hard cap kept at 4 iterations;
  added audit-trail requirement (iteration reports kept, not overwritten). Synced
  across `SKILL.md`, `references/agent-workflow.md`, and `references/book-structure.md`.
- **v4 — convergence check hardened**: was comparing each iteration only to the one
  immediately before it, which could miss an oscillating issue-count pattern
  (5 → 3 → 5) for one extra pass before escalating. Now tracks the running minimum
  across all iterations so far — each new iteration must set a new minimum or the
  loop escalates immediately, closing that gap.
