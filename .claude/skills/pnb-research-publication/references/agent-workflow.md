# 5-Agent Research Paper Production Workflow

## Architecture Overview

```
Phase 1 — Lead Agent     → Paper Brief + task assignment
Phase 2 — Literature Agent } parallel
          Writing Agent    }
Phase 3 — Lead Agent     → merge citations into drafts
Phase 4 — Fact-Checker Agent → findings report (CLEAR / BLOCKED)
Phase 5 — Editor Agent   → IEEE style + word count enforcement
Phase 6 — Lead Agent     → final QA + delivery
```

---

## Agent 1 — Lead Agent

### Phase 1: Paper Brief

**Inputs:** User requirements (topic, paper type, venue, contributions, materials)

**Output: Paper Brief** — passed to both Literature and Writing Agents

```
PAPER BRIEF
───────────
Paper type    : [Conference / Journal / arXiv / Workshop]
Target venue  : [e.g., IEEE CVPR 2025]
Page limit    : [e.g., 8 pages + unlimited references]
Abstract limit: [e.g., 250 words max]
Review type   : [Double-blind / Single-blind / None]

Title (working): [Working title]
Core problem   : [One-sentence problem statement]

Contributions (user-stated):
  1. [contribution 1]
  2. [contribution 2]
  3. [contribution 3]

Sections to produce:
  I.   Introduction       — [scope: motivation, gap, contributions]
  II.  Related Work       — [themes: list 3-4 thematic clusters to cover]
  III. Methodology        — [scope: what to describe, key equations/figures]
  IV.  Experiments        — [datasets, baselines, metrics to compare]
  V.   Results            — [tables/figures needed]
  VI.  Discussion         — [analysis points, known limitations]
  VII. Conclusion         — [what was shown, future work]

Literature priorities (for Literature Agent):
  - [specific papers user mentioned or seminal papers to find]
  - [baseline methods to cite]
  - [benchmark datasets to reference]
  - [any claimed improvements that need comparison papers]

Writing notes (for Writing Agent):
  - [audience level: expert, mixed, interdisciplinary]
  - [sections that need heavy math vs. conceptual explanation]
  - [any user-provided data/results to incorporate]
```

### Phase 3: Merge

- Inject Literature Agent's verified `[N]` citations into Writing Agent's `[CITE: description]` placeholders
- Match citations to claims by description
- Mark any unmatched claim with `[Unverified: no primary source found]`
- Assign sequential citation numbers [1], [2], [3]...

### Phase 6: Final QA

Before delivery, verify:
- [ ] All `[Unverified]` markers resolved
- [ ] No placeholder arXiv IDs
- [ ] Abstract word count within limit
- [ ] Page count within venue limit
- [ ] Contribution statement present in Introduction
- [ ] All figures/tables referenced inline
- [ ] Acknowledgments removed (if blind review)
- [ ] Self-citations anonymized (if double-blind)

---

## Agent 2 — Literature Agent

### Role
The only agent authorized to make citation claims. Runs in parallel with Writing Agent. Returns structured literature packets — never drafts prose.

### Inputs
- Paper Brief (literature priorities + section scopes)
- Access to: Google Scholar, Semantic Scholar, arXiv, IEEE Xplore, ACM DL

### Output: Literature Packet

```markdown
## Literature Packet — [Section Name]

### Core Papers (must cite)
| Paper | Year | Venue | Key Claim Relevant to Us | Quoted Source Text | IEEE Citation |
|-------|------|-------|--------------------------|---------------------|---------------|
| [Title] | 2024 | CVPR | [what it shows / why we cite it] | "[exact sentence or clause from the source, via WebFetch, that supports the claim in the previous column — not a paraphrase]" | [N] A. Author... |

### Baseline Methods (for Experiments section)
| Method | Paper | Why it's a relevant baseline |
|--------|-------|------------------------------|
| [Name] | [N]   | [brief justification] |

### Datasets Cited in Literature
| Dataset | Paper | Standard Split/Metric |
|---------|-------|-----------------------|
| [Name]  | [N]   | [train/val/test sizes] |

### Research Gap (for Introduction/Related Work)
[2–3 sentences describing what prior work lacks that this paper addresses]

### Unresolvable Citations
| Claim | Why unresolvable | Recommendation |
|-------|-----------------|----------------|
| [claim] | [no primary source / conflicting papers] | [remove / qualify / use secondary] |
```

### Literature Agent Rules

1. **Primary sources only.** Peer-reviewed papers from IEEE Xplore, ACM DL, arXiv (real IDs only), DBLP. Blog posts and documentation are not citable primary sources for claims.

2. **Verify arXiv IDs.** Every arXiv citation must have a real, verifiable ID that resolves at `https://arxiv.org/abs/XXXX.XXXXX`. Never fabricate an ID.

3. **Seminal papers.** For any established method (e.g., ResNet, BERT, Transformer), find and cite the original paper — not a follow-up or summary.

4. **Recency.** For fast-moving fields (LLMs, diffusion models), include papers from the last 2 years. For mature fields, include foundational papers regardless of age.

5. **Flag unresolvable.** If a claim in the Paper Brief cannot be supported by a real primary source, return it in "Unresolvable Citations" — never invent a citation.

6. **Quote the source, don't just cite it.** For every row in "Core Papers," WebFetch the actual source and copy the exact sentence or clause that supports the "Key Claim" column into "Quoted Source Text" — do not write the packet from memory or from the citation's title/abstract alone. A citation that resolves (real DOI/arXiv ID, matching title and authors) is not the same as a citation that actually says what you're about to attribute to it — verifying the source *exists* and verifying the source *supports this specific claim* are two different checks, and only the second one prevents a fabricated statistic from surviving into the merged draft. (This rule exists because a real, resolvable source was cited for a growth statistic it did not actually contain, on the 2026-08-20 FDE paper — the citation checked out, the number attached to it didn't.)

---

## Agent 3 — Writing Agent

### Role
Drafts all sections except References. Runs in parallel with Literature Agent. Uses `[CITE: description]` placeholders — no actual citation numbers yet. Academic voice only.

### Inputs
- Paper Brief (section scopes + audience notes)
- `writing-standards.md` (fully binding)
- User-provided data, results tables, experimental details (if any)

### Output: Section Drafts

```
## I. Introduction

[Prose draft — academic voice. Use [CITE: description of what to cite] where citations needed.]

The contributions of this paper are as follows:
\begin{itemize}
  \item We propose [specific method] that [specific advantage].
  \item We demonstrate [specific result].
  \item We release [code/dataset] at [CITE: own repo URL].
\end{itemize}

## II. Related Work

### A. [Theme 1]
[Prose. Use [CITE: paper that does X] placeholders.]

...
```

### Writing Agent Academic Style Contract

| Rule | Requirement |
|---|---|
| **Voice** | Formal, objective, third-person or "we". No first-person opinion ("I believe...") |
| **Contribution statement** | Must use exact format: "The contributions of this paper are as follows:" with \begin{itemize} list |
| **Tense** | Present for general truths and system descriptions. Past for specific experimental results. |
| **Passive voice** | Acceptable for methodology ("The model was trained..."). Active preferred for contributions ("We propose...") |
| **Hedging** | Use for unproven claims: "suggests", "indicates", "appears to". Banned for your own proven results. |
| **Math** | Every variable must be defined. Every equation must be numbered. |
| **Figures** | Write "as shown in Fig.~\ref{fig:N}" even before figure files exist — the Editor will verify |
| **No filler** | Remove: "It is worth noting that...", "Interestingly,...", "Notably,...", "In this section, we..." |

---

## Agent 4 — Fact-Checker Agent

### Role
Accuracy and reproducibility enforcement layer. Receives merged draft. Outputs structured findings report — never rewrites prose.

### Output: Fact-Checker Findings Report

```markdown
## Fact-Checker Findings Report — Iteration [N] of max 4

### Summary
Claims verified    : N
Claims flagged     : N (Critical: N | Major: N | Minor: N)
Reproducibility    : PASS / FAIL
Delivery blocker   : YES / NO
Issue count vs. running minimum : [this iteration: N | lowest so far: N] (must set a new minimum or loop escalates — see below)

### Verified Claims
| Section | Claim | Citation | Status |
|---------|-------|----------|--------|
| II.A | [claim text] | [N] | VERIFIED |

### Flagged Claims (severity-tagged)
| Section | Claim | Severity | Issue | Recommendation |
|---------|-------|----------|-------|----------------|
| III.B | [claim] | Critical | [hallucinated stat / fake citation] | [cite / remove / qualify] |
| IV.C | [claim] | Major | [weak/indirect source for a load-bearing claim] | [strengthen citation] |
| V.A | [claim] | Minor | [phrasing could overclaim] | [hedge language] |

**Severity definitions:**
- **Critical** — hallucinated statistic, fake/unverifiable citation, unnamed dataset/baseline. Always blocks delivery, no exceptions.
- **Major** — a real but weak/indirect source for a claim doing heavy lifting in the argument; reproducibility gap on a secondary detail.
- **Minor** — phrasing/hedging issues, stylistic overclaiming that doesn't change the substance.

### Reproducibility Check
| Item | Status | Note |
|------|--------|------|
| Datasets named with version | PASS / FAIL | |
| Baselines cited with papers | PASS / FAIL | |
| Metrics precisely defined | PASS / FAIL | |
| Hyperparameters reported | PASS / FAIL | |
| Code/model availability stated | PASS / FAIL | |

### Citation Audit
- [ ] No placeholder arXiv IDs (arXiv:XXXX.XXXXX pattern absent)
- [ ] No [CITE NEEDED] markers remaining in draft
- [ ] All [Unverified: ...] markers listed in Flagged Claims above
- [ ] No citations to Wikipedia, blog posts, or press releases as primary evidence
- [ ] For every load-bearing numeric/statistical claim, the Literature Packet's "Quoted Source Text" actually supports the number as written in the merged draft — a resolvable citation with a fabricated or drifted number attached is a Critical finding, not a Minor one, even though the citation itself checks out

### Delivery Recommendation
[ ] CLEAR — zero Critical, zero Major issues remaining → pass to Editor Agent
[ ] BLOCKED — Critical and/or Major issues remain → Lead Agent must resolve first
[ ] ESCALATE — see convergence rule below
```

### Fact-Checker Hard Rules

1. **Hallucinated statistics = hard block (Critical).** Any numerical claim with no citation is flagged as "hallucinated stat."
2. **Fake arXiv IDs = delivery blocker (Critical).** Any `arXiv:XXXX.XXXXX` pattern must be verified.
3. **Reproducibility = mandatory (Critical).** If datasets or baselines are unnamed, it is a BLOCKED finding.
4. **Delivery recommendation is binding.** Lead Agent must not pass a BLOCKED draft to Editor. Minor-only findings do not block — flag and pass, don't loop over style nitpicks.
5. **Exit criteria is Critical=0 AND Major=0**, not "fewer issues than before." Minor issues can ship; Critical/Major cannot.

### Loop Engineering — Convergence & Escalation Rules

This is the draft-review-revise loop (Fact-Checker → Lead resolves → re-check). It exists to
fix real problems fast, not to iterate indefinitely chasing diminishing returns.

- **Hard cap: 4 iterations per section/chapter.** No exceptions, no "one more pass."
- **Convergence check every iteration:** track the (Critical+Major) count from
  every iteration so far, not just the last one. Each new iteration's count must
  be **strictly lower than the lowest count seen in any prior iteration** (not
  just lower than the immediately preceding one — this also catches an
  oscillating pattern like 5 → 3 → 5, which a prior-iteration-only comparison
  would miss for one extra pass). If the new count isn't a new minimum, **stop
  looping immediately** and escalate; another identical-strength pass will not
  fix what hasn't already been fixed.
- **Escalate means:** the Fact-Checker's report is handed to the user directly with the specific
  Critical/Major items still open, plus a one-line note on why the automated loop couldn't
  resolve them (e.g., "no primary source exists for this claim — needs author's own data or the
  claim must be removed"). Never auto-mark a section "CLEAR" or silently ship it to the Editor
  just because the cap was reached.
- **Audit trail:** each iteration's findings report is kept (not overwritten) so the Lead Agent's
  final QA and the user can see the resolution history, not just the last state.

---

## Agent 5 — Editor Agent

### Role
IEEE style compliance, word count enforcement, clarity, and removal of AI-writing patterns. Receives only CLEARED drafts. Does not alter factual content or citations.

### Editor Checklist

**IEEE Style:**
- [ ] All citations use `[N]` format — no `(Author, Year)` anywhere
- [ ] Figures captioned above (tables) or below (figures) — IEEE standard
- [ ] Section headings use Roman numerals (I, II, III)
- [ ] Subsection headings use letters (A, B, C)
- [ ] No subsection has only one item (merge or remove)
- [ ] `\IEEEPARstart` used for first paragraph of Introduction

**Word/Page Count:**
- [ ] Abstract within venue limit (150–250 words typically)
- [ ] Total page count within venue limit
- [ ] If over limit: identify longest paragraphs for tightening

**Clarity:**
- [ ] Every acronym defined on first use
- [ ] Every mathematical symbol defined before or at first use
- [ ] No sentence > 40 words without restructuring
- [ ] No paragraph > 8 lines without a break

**AI-Writing Patterns (remove all):**
- [ ] "It is worth noting that..." → state directly
- [ ] "Interestingly,..." → remove preamble
- [ ] "In this section, we will..." → remove meta-commentary
- [ ] "The proposed method is..." → "Our method..."
- [ ] Generic section openings ("This section presents...") → content-first

### What the Editor Must NOT Do
- Change any cited statistic or experimental result
- Add new claims not in the merged draft
- Remove `[Unverified]` markers — those are Lead Agent decisions
- Alter citation numbers

---

## Handoff Schema

```
Lead Agent
  └─► Paper Brief
        ├─► Literature Agent → Literature Packet
        └─► Writing Agent    → Section Drafts
              │
Lead Agent ◄──┘ (merge: inject [N] citations, mark [Unverified])
  └─► Merged Draft
        └─► Fact-Checker Agent → Findings Report (Iteration 1)
              │
              ├── Critical/Major = 0 → CLEAR
              │       └─► Editor Agent → Polished Paper
              │
              └── Critical/Major > 0 → BLOCKED
                    └─► Lead Agent resolves → Fact-Checker re-checks (Iteration 2)
                          │
                          ├── issue count decreased → loop continues (max iteration 4)
                          └── issue count flat/worse → ESCALATE to user, stop looping
                                (do not auto-clear; do not silently ship)

Lead Agent ◄──────────────┘ (final QA — includes checking no ESCALATE items were bypassed)
  └─► Delivered Paper (main.tex + paper.md + references.bib)
```

---

## Paper Production Log (per paper)

```markdown
# Paper Production Log — [Paper Title]

## Lead Agent — Phase 1
- [ ] Paper Brief created
- [ ] Target venue and limits confirmed
- [ ] Literature priorities defined

## Phase 2 (parallel)
- [ ] Literature Agent complete — N citations returned, N unresolvable
- [ ] Writing Agent complete — N section drafts returned

## Lead Agent — Phase 3
- [ ] Merge complete — N citations injected, N [Unverified] markers

## Fact-Checker — Phase 4 (loop, max 4 iterations)
- [ ] Iteration 1: N verified, N flagged (Critical N / Major N / Minor N), reproducibility PASS/FAIL
- [ ] Delivery: CLEAR / BLOCKED / ESCALATE
- [ ] If BLOCKED: iteration 2 resolved on [date] — issue count [before → after], must have decreased
- [ ] If ESCALATE: reason logged, user notified, not auto-shipped

## Editor — Phase 5
- [ ] IEEE style compliance confirmed
- [ ] Word/page count within limits

## Lead Agent — Phase 6
- [ ] Final QA passed
- [ ] Blind review prep complete (if applicable)
- [ ] Paper delivered on [date]
```
