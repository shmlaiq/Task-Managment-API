---
name: pnb-research-publication
allowed-tools: WebSearch, WebFetch, Read, Write, Edit, Bash
metadata:
  model: opus
description: |
  Use when users ask to write a research paper, IEEE paper, conference/journal
  submission, survey, rebuttal, or an academic/technical book or textbook — e.g.
  "write a paper about X", "help me publish my research", or a book/paper writing
  offer. ALWAYS run Intake first to confirm paper vs. book before writing — they
  differ hugely in length/structure. Produces publication-ready IEEE papers
  (Abstract through References, verified citations, LaTeX/IEEEtran output) or
  chapter-based academic books (250-350 pages default). Optional 5-agent team
  (Lead, Literature, Writing, Fact-Checker, Editor) = the draft-review-revise
  "loop engineering" cycle: severity-tagged (Critical/Major/Minor), must converge
  each iteration or it escalates to the user, hard-capped at 4 iterations. Covers
  domain conventions (CS/AI, EE, Robotics, Comms), word/page limits, citation
  integrity, reproducibility, anti-hallucination, plagiarism-free prose, and
  AI-detection posture subject to the venue's disclosure policy.
---

# Research Paper & Book Writer

Write complete, publication-ready IEEE standard research papers — from first draft
to submission-ready LaTeX output — or complete academic/technical books, with full
rigor and quality enforcement. Always starts with an Intake step that confirms which
of the two is being written.

## Scope Boundaries

Handled by this skill: research papers (all variants below) AND academic/technical
books/textbooks (Variant E). Redirect and stop if the task is outside even that:
- **Patent drafting** → patent-writer skill
- **Grant proposals** → grant-writer skill
- **Thesis/dissertation** → thesis-writer skill (multi-chapter, committee review)
- **Fiction / trade non-fiction book** → book-creator skill (this skill covers
  academic/technical books only)

---

## Before Implementation

| Source | Gather |
|--------|--------|
| **Conversation** | Paper topic, type, venue, contributions, author name, email |
| **Skill References** | Domain conventions, IEEE patterns from `references/` |
| **Codebase** | Existing `paper.md` / `main.tex` if improving a draft |

Ask only questions 1–4 from Step 0 on the first message. Use conversation context to skip already-answered questions. Do not ask for domain knowledge — that is embedded in `references/`.

---

## Step 0: Gather Requirements

**Before asking:** scan the user's message for already-stated answers — if they mentioned the venue, topic, or paper type, skip those questions. Never ask more than 4 questions in a single message.

**Question 0 — MANDATORY, always asked first, hard gate:** "Is this a research paper (conference/journal/arXiv/survey/rebuttal) or a book/academic textbook?" Do not proceed to any other question, outline, or writing until this is answered — the two deliverables have very different length and structure requirements (see Paper Type Reference table below, which now includes the book/textbook row). If the answer is "book/textbook," skip straight to the **Book / Academic Textbook Variant** section and its own intake questions instead of questions 1–7 below.

Ask questions 1–4 first (always required for the research-paper path). Ask 5–7 only if not already clear from context.

1. **Author name**: "What is your full name? (appears on the paper)" — ALWAYS ask, never skip.
2. **Research topic**: "What is your paper about? What problem does it solve?"
3. **Paper type**: "Conference, journal, arXiv preprint, survey paper, or rebuttal?"
4. **Target venue**: "Which conference or journal? (e.g., IEEE CVPR, IEEE TPAMI, ICLR)"
5. **Contributions**: "What are the 2–3 main contributions?"
6. **Materials available**: "Do you have results/data, or is this a proposed approach?"
7. **Contact details**: "Your email address, and optionally ORCID iD?" — needed for the author block in main.tex. Collect at Step 0 so the final LaTeX is complete at first delivery, not as a late patch.

**If 5–7 go unanswered:** proceed with safe defaults — conference format, 6–8 pages, contributions inferred from the topic description. Note any gaps in SUBMISSION-CHECKLIST.md for the author to fill before submission.

**Author block formatting rule** (apply immediately when writing main.tex):

| Has institutional affiliation? | LaTeX pattern |
|---|---|
| Yes (university / company) | `\IEEEauthorblockN{Name}` + `\IEEEauthorblockA{Institution \\ City \\ Email \quad ORCID}` |
| No affiliation provided | `\IEEEauthorblockN{Name \qquad Email:~x \qquad ORCID:~x}` — single line, NO `\IEEEauthorblockA` |

**Critical:** Never use `\IEEEauthorblockA` with a placeholder value (`[Your Affiliation]`, empty, or `Independent Researcher` without the author's consent) — it renders as a visible blank or wrong line in the PDF. If affiliation is unknown, use the no-affiliation single-line pattern above and note the gap in SUBMISSION-CHECKLIST.md.

### Paper Type Reference

| Type | Page Limit | Abstract | Review |
|---|---|---|---|
| IEEE Conference | 6–8 pages + unlimited refs | 150–250 words | Double-blind |
| IEEE Transactions | 8–15+ pages | 250 words max | Single-blind |
| IEEE Letters | 4–5 pages | 150 words max | Single-blind |
| arXiv Preprint | No limit | 150–250 words | None |
| Workshop Paper | 4–6 pages | 150 words | Double-blind |
| Survey / Review | 15–30+ pages | 250 words | Single-blind |
| Rebuttal | 1 page (500 words) | None | N/A |
| Academic Textbook / Book | **250–350 pages (default)** | N/A (per-chapter summary instead) | Publisher/self-review |

**Defaults when venue/type not specified by the user:** research paper → 15 pages
(~7,500 words); book/textbook → 250–350 pages, academic/textbook subtype. State the
assumed default back to the user in the confirmation brief so they can override it.

---

## Step 1: Detect Domain

Before writing, identify the research domain — it affects citation norms, writing
conventions, expected baselines, and section emphasis.

| Domain | Key Signals | Special Conventions |
|---|---|---|
| **CS / AI / ML** | Neural networks, datasets, benchmarks, accuracy/F1 | Ablation study mandatory; code release expected |
| **Electrical Engineering** | Circuits, signals, hardware, FPGA, power | Simulation results + hardware validation both required |
| **Robotics** | Physical systems, kinematics, ROS, SLAM, manipulation | Real-world experiments required; sim-to-real gap addressed |
| **Communications / Networks** | Throughput, latency, protocol, channel model | Mathematical analysis + simulation results |
| **Computer Vision** | Images, detection, segmentation, 3D | Qualitative figure results + quantitative tables |
| **NLP / LLM** | Language models, BLEU, perplexity, fine-tuning | Human evaluation + automatic metrics |
| **Interdisciplinary** | Mixed signals from above | Follow the primary venue's domain conventions |

Read `references/domain-specific.md` for domain-by-domain writing conventions.

---

## Step 2: Identify Paper Variant

### Variant A — Regular Research Paper
Standard 13-section structure. See **Paper Structure** section below.

### Variant B — Survey / Review Paper
Different structure: Taxonomy + Coverage + Analysis instead of Methodology + Experiments.
Read `references/survey-paper.md` for complete survey paper guidance.

### Variant C — Rebuttal
Response to peer review comments. 500 words, structured per-reviewer.
Read `references/rebuttal.md` for complete rebuttal writing guide.

### Variant D — Conceptual / Proposed Architecture Paper
No empirical experiments exist. The author proposes a new framework, system design,
or architectural model grounded in prior literature. Common in systems, AI infrastructure,
and interdisciplinary venue papers.

**Key difference from Variant A:** Replace Experiments + Results sections with:
- **Architecture Analysis** — component interaction lifecycle, design trade-offs table
- **Comparison Table** — side-by-side vs. existing systems across all proposed pillars/dimensions

**Section structure for Variant D:**
```
I.    Introduction          — hook + gap + explicit contribution list
II.   Related Work          — 3–5 themed subsections; honest positioning
III.  Background            — mapping prior concepts to new domain (e.g., OS → agents)
IV.   Proposed Architecture — N subsections, one per pillar/component; equations welcome
V.    Architecture Analysis — lifecycle walkthrough + design trade-offs + comparison table
VI.   Limitations           — ≥5 named failure modes; include implementation gap
VII.  Conclusion            — what was specified + future research agenda (specific)
```

### Variant E — Academic Textbook / Book

No page-limit-per-section constraint like a paper; instead a chapter-based structure
scaled to 250–350 pages (default) or whatever the user overrides.

**Intake questions specific to this variant (ask instead of paper Q1-7):**
1. Subject/topic of the book
2. Target length (default: 250–350 pages academic/textbook — confirm or override)
3. Target audience (undergrad/grad/professional) — affects depth and prerequisite assumptions
4. Publisher or self-publish, and citation style (APA/IEEE/Chicago — confirm, don't assume)

**Book structure (default academic/textbook):**
```
Front matter    — title page, preface, table of contents
Units/Chapters  — each chapter: learning objectives → body sections/subsections →
                   chapter summary → review questions
Back matter     — glossary, references/bibliography, index
```

**Production flow — one chapter at a time, through the same 5-agent pipeline below**
(Lead → Literature+Writing parallel → Fact-Checker → Editor → Lead), with the loop
engineering cap in "Execution Protocol" applied per chapter, not per whole book. Track
a running outline/table of contents across chapters so the Lead Agent's final QA pass
can check cross-chapter consistency (terminology, notation, no repeated content).

**Model routing for books (cost vs. precision):** because a book is volume-heavy
(250–350 pages) rather than precision-heavy like a paper, it is reasonable to route
the Writing Agent (bulk drafting) to a faster/cheaper model while keeping the
Fact-Checker Agent, Editor Agent, and any technically sensitive chapter on the
strongest available model. Do not apply the same cost-saving routing to research
papers — those stay on the strongest model throughout, given the higher
reputational stakes of formal submission and peer review.

Same five quality pillars below apply per chapter (hallucination, plagiarism,
AI-detection posture per Pillar 3's disclosure note, humanized tone, citation
integrity) — just replace "Section" with "Chapter" in the pre-writing checklist.

---

**Anti-hallucination rule for Variant D:**
- Architectural design choices (e.g., "the ACR header uses 512 tokens by default") do NOT need citations — they are your design
- Claims about prior systems' performance DO need citations (e.g., "AIOS achieves 2.1× speedup [N]")
- Design equations (paging policies, allocation formulas) do NOT need citations — they are your contribution
- Any numbers attributed to prior work MUST be cited to the primary source

**Reference count for Variant D:**
17 high-quality verified citations outperform 60 padded unverified ones. IEEE Access
does not reject papers for low reference counts — it rejects papers for uncited claims.
Prioritize verification over volume. Note in SUBMISSION-CHECKLIST.md if count is below
venue typical range and recommend additional citations the author can verify.

---

## Paper Structure (Regular Research Paper — Mandatory)

```
1.  Title              — specific, informative, 10–15 words, no puns
2.  Authors + Affiliations — anonymized for double-blind review
3.  Abstract           — 150–250 words: problem → method → results → significance
4.  Index Terms        — 4–6 IEEE taxonomy keywords
5.  Introduction       — motivation → gap → contributions (explicit list) → organization
6.  Related Work       — grouped by theme, honest positioning
7.  Methodology        — problem formulation, architecture, numbered equations
8.  Experiments        — setup, datasets (named+cited), baselines (named+cited), metrics
9.  Results            — tables (bold best), figures, ablation study
10. Discussion         — analysis + ≥1 failure case/limitation
11. Conclusion         — what was shown + key result + 2–3 future directions
12. Acknowledgments    — funding, compute, data (omit in blind review)
13. References         — IEEE [N] format
    [Appendix]         — optional: proofs, extended results, extra tables
    [Supplementary]    — optional: uploaded separately, not in page count
```

See `references/paper-structure.md` for section-by-section depth guidance.

---

## 5-Agent Production Workflow

> **ACTIVATION REQUIRED — this workflow does NOT run automatically.**
> The default system behavior suppresses sub-agent spawning unless the user explicitly
> requests it. To activate the full 5-agent workflow, the user must say something like:
> - "use the 5-agent workflow"
> - "spawn sub-agents for this paper"
> - "use the full agent pipeline"
>
> Without explicit activation, the main assistant handles all five roles inline in a
> single context. This is faster but sacrifices true parallelism, independent
> fact-checking, and a genuinely fresh editorial pass. For long or high-stakes papers,
> always ask: **"Should I use the 5-agent workflow for better quality, or write inline
> for speed?"**

```
┌─────────────────────────────────────────┐
│              LEAD AGENT                 │
│  Plans structure, assigns tasks, merges │
└──────────────┬──────────────────────────┘
               │ spawns in parallel
       ┌───────┴────────┐
       ▼                ▼
┌─────────────┐  ┌─────────────┐
│  LITERATURE │  │   WRITING   │
│    AGENT    │  │    AGENT    │
│ Lit search  │  │ Drafts per  │
│ IEEE cites  │  │ IEEE + domain│
│ gap analysis│  │ conventions │
└──────┬──────┘  └──────┬──────┘
       └────────┬────────┘
                ▼
       ┌────────────────┐
       │  FACT-CHECKER  │  ← verifies numbers, arXiv IDs,
       │     AGENT      │    math, reproducibility
       └───────┬────────┘
               ▼ CLEAR
       ┌────────────────┐
       │    EDITOR      │  ← IEEE style, word count,
       │     AGENT      │    anti-AI transformation
       └───────┬────────┘
               ▼
       ┌────────────────┐
       │  LEAD AGENT    │  ← final QA + delivery
       └────────────────┘
```

| Agent | Runs | Responsibility |
|---|---|---|
| **Lead Agent** | Phase 1 + 6 | Paper Brief; parallel dispatch; citation merge; final QA |
| **Literature Agent** | Phase 2 (parallel) | Academic database search; IEEE citations; gap analysis; baselines |
| **Writing Agent** | Phase 2 (parallel) | All section drafts; `[CITE: description]` placeholders; domain voice |
| **Fact-Checker Agent** | Phase 4 | Every number verified; arXiv IDs checked; math validated; reproducibility confirmed; CLEAR / BLOCKED |
| **Editor Agent** | Phase 5 | IEEE style; word count; anti-AI transformation; banned phrase removal |

**Why the 5-agent workflow produces better output than inline:**
- Literature Agent + Writing Agent run in true parallel — faster for long papers
- Fact-Checker Agent has no memory of what the Writing Agent wrote — catches self-deceptions the writer cannot see
- Editor Agent reads the draft cold — catches AI-pattern prose the writer normalised during drafting
- Inline (single context) collapses all five roles, which introduces reviewer bias and cannot genuinely parallelise

See `references/agent-workflow.md` for full prompts and handoff schemas.

---

## Execution Protocol

```
1  Lead Agent → Paper Brief (structure + domain + research priorities)
2  Parallel: Literature Agent + Writing Agent
3  Lead Agent → merge (inject [N] citations, mark [Unverified] gaps)
4  Fact-Checker Agent → CLEAR or BLOCKED report
5  (if BLOCKED) Lead resolves → re-check
6  Editor Agent → IEEE style + anti-AI transformation
7  Lead Agent → final QA → deliver
```

**Loop engineering rule (strengthened):** steps 4–5 (Fact-Checker → Lead resolves → re-check)
are a draft-review-revise loop with real exit criteria, not a fixed number of passes.

- Fact-Checker tags every issue **Critical / Major / Minor**. Exit (CLEAR) requires
  Critical=0 AND Major=0 — Minor issues don't block delivery.
- **Convergence check every iteration:** the Critical+Major count must strictly decrease
  from the prior iteration. If it doesn't, stop looping immediately — even before the cap —
  and **escalate to the user** with the specific unresolved items and why the loop couldn't
  fix them, rather than spending another identical-strength pass on it.
- **Hard cap: 4 iterations per section/chapter** regardless.
- Never auto-mark a section CLEAR or silently pass it to the Editor because the cap was
  reached — an unresolved Critical/Major item at the cap is a human decision, not an
  automated one.
- Keep every iteration's findings report (don't overwrite) so there's an audit trail of what
  was flagged and how it was resolved. Full detail: `references/agent-workflow.md`.

---

## Five Quality Pillars (Non-Negotiable — Enforce FROM THE FIRST SENTENCE)

These are not post-writing checks. They are active writing constraints that apply
from the moment the first word is written. Never skip, never defer to "fix later."

**Before writing Section I, confirm all active:**
- [ ] Hallucination guard ON — I will verify every stat/arXiv ID; no fabricated claims
- [ ] Plagiarism guard ON — I will rephrase all prior work, not echo it
- [ ] Anti-AI guard ON — I will vary sentence lengths, take positions, include failures
- [ ] Humanized tone ON — I will write as a domain expert, not as a template filler
- [ ] Fact integrity ON — I will cross-check every author name and citation before delivery
- [ ] Rule A ON — every formula parameter will have domain + default + workload values
- [ ] Rule B ON — every source paraphrase will be structurally unrecognisable
- [ ] Rule C ON — every mechanism will have a complete escalation path (no "not fully specified")
- [ ] Rule D ON — derived numbers will use ratios/multipliers, not bare `NN%`
- [ ] Rule E ON — installation subsections will vary paragraph structure (no uniform rhythm)
- [ ] Rule F ON — conclusion future work ordered by urgency, not by count or symmetry
- [ ] Rule G ON — I will only add .bib entries I will actually cite in body text
- [ ] Rule H ON — every edit to paper.md will be immediately mirrored in main.tex
- [ ] Rule I ON — all external factual claims (events, named products, specs, prices, hardware) will be cited or removed
- [ ] Rule J ON — abstract will be self-contained: ends with significance, all non-standard acronyms expanded, all factual lists match the body
- [ ] Rule K ON — all figures are actual TikZ/pgfplots code in main.tex; zero \figplaceholder calls in any delivered draft; TikZ packages in preamble
- [ ] Rule L ON — every mathematical bound/theorem cites the paper that proved it, not a paper that uses it
- [ ] Rule M ON — zero `and others` in references.bib; every BibTeX author list is complete
- [ ] Rule N ON — derived estimates are labeled as derived and not attributed to sources that don't state them
- [ ] Rule O ON — no distinctive 5+ word phrase from the abstract appears verbatim in body sections
- [ ] Rule P ON — vendor/official documentation written with read-close-write method, same as academic papers
- [ ] Rule Q ON — paper is colorful and visually attractive; first page has colored title, styled author, colored abstract box, colored keywords box; all figures use resource-coded colors; heatmaps use diverging scale — read `references/visual-design.md` before writing main.tex

**Before delivering ANY draft, run the 17-check pre-delivery audit in `references/audit-commands.md`.** Checks 1, 2, 4, 5, 13, 14, 15 are delivery blockers.

Read the corresponding reference file BEFORE any content is generated.

### Pillar 1 — No Hallucinations
→ `references/anti-hallucination.md`

- Zero fabricated statistics — every number is from your experiments OR has `[N]` citation
- Zero fabricated arXiv IDs — verify every ID at `arxiv.org/abs/XXXX.XXXXX` before inclusion
- Zero fabricated baselines or author names
- Distinguish design choices (no citation needed) from empirical claims (citation required)
- Delivery blockers: any placeholder arXiv ID, `[CITE NEEDED]`, `[Unverified]`

Full deduction scale for `/grade-paper`: see `references/grade-paper.md`.

### Pillar 2 — Plagiarism Free
→ `references/anti-plagiarism.md`

- All Related Work: **read-close-write method** (never copy-then-paraphrase)
- iThenticate/Turnitin: **< 15% overall**, **< 5% per single source**
- Self-plagiarism: prior own work must be cited
- Code: original implementation; figures: original or redrawn with permission

### Pillar 3 — Zero Detectable AI Involvement
→ `references/anti-ai-detection.md`

**Disclosure note (check before relying on this pillar):** these targets govern prose
*quality and naturalness* (varied sentence rhythm, concrete specificity, no template
filler) — they are not a substitute for the target venue's AI-use disclosure policy.
Many venues now require disclosing AI assistance in a cover letter or acknowledgments
regardless of how "human" the prose reads. Check the venue's current policy before
submission and disclose if required — passing these scanner targets and being
compliant with disclosure rules are two separate things; do not treat one as covering
the other.

| Scanner | Target |
|---|---|
| GPTZero | < 20% AI probability per section |
| Originality.ai | < 20% AI probability |
| Turnitin AI | 0 flagged passages |

Editor Agent transformation (mandatory before delivery):
- Remove banned phrases: "It is worth noting", "Interestingly,", "state-of-the-art performance" (no number), "significant improvement" (no %)
- Burstiness: sentences < 8 words AND > 30 words mixed per section
- Specificity: every vague claim replaced with concrete number/detail
- Failures: ≥1 limitation/failure case in Discussion section

### Pillar 4 — Humanized Language Tone
→ `references/pillar4-humanized-tone.md`

- Write as a domain expert: specific vocabulary, concrete details, honest limitations named explicitly
- No uniform hedging, no template prose, no filler transitions
- At least one genuine opinion per section; at least one failure story per paper

### Pillar 5 — Fact & Citation Integrity
→ `references/pillar5-citation-integrity.md`

- Every "Author et al." name cross-checked against the BibTeX `author` field
- Every DOI confirmed live on the publisher's site
- Every URL verified accessible at time of writing
- Zero placeholder citations of any form
- BibTeX author lists complete — zero `and others` entries (Rule M)
- For deployment statistics appearing in multiple source documents: cite ALL supporting sources, not just the primary one — a single citation where two exist is a partial attribution failure

Deep deduction scale for external event claims, product attribution, third-party specs,
BibTeX venue consistency, and Rules L/M/N: `references/anti-hallucination.md` Categories 6–12.

### Writing Rules A–P — Prevent Recurring Issues

Read `references/writing-rules.md` **before writing Section I**. Full enforcement details and safe/unsafe examples are in that file. Summaries below for quick reference:

| Rule | Enforcement Summary |
|---|---|
| **A — Formula params** | Every parameter needs: domain, concrete default, ≥2 workload values. Never "tunable" without specifying values. |
| **B — Paraphrase** | Must differ in both structure AND vocabulary. Test: "Identifiable without citation?" → rewrite. |
| **C — Escalation path** | Every mechanism needs: normal path + error path + fallback (HITL/operator). "Not fully specified" = deduction. |
| **D — Theoretical Analysis** | Variant D papers: add Theoretical Analysis subsection (complexity + dominance argument + quantitative bound). Use ratios, not bare %. |
| **E — Install rhythm** | ≥5 platform subsections: vary opening strategy across subsections. Check: 3+ identical openings → restructure. |
| **F — Future work order** | Order by urgency, not symmetry. Never "Three limitations are the most consequential..." → deduction trigger. |
| **G — Orphaned refs** | Every `.bib` entry must be cited inline. Run audit check 6 before delivery. |
| **H — File sync** | paper.md ↔ main.tex must stay in sync. Every edit to one triggers an update to the other. |
| **I — External claims** | Events, product features, specs, pricing, hardware = citation required or remove. Pre-write: "Is this cited?" |
| **J — Abstract** | Ends on significance; all non-standard acronyms expanded (LLM, MCP, RAG, HITL, ACP, VPS, QMD); factual lists match body; no `[N]` citations. |
| **K — Figures** | TikZ/pgfplots in main.tex before delivery. Preamble: `tikz`, `pgfplots`, `arrows.meta,positioning,shapes.geometric,fit,calc,backgrounds`, `compat=1.18`. Never `sed` on `.tex`. 7 templates in `references/figures-design.md`. |
| **L — Theorem source** | Cite paper that *proved* the result, not one that merely uses it. Ask "Who proved this first?" |
| **M — Author lists** | Complete BibTeX author lists always. `grep -n "and others" references.bib` must return zero. |
| **N — Derived estimates** | Label derived ranges as derived; do not imply the formula's source states your range. |
| **O — Abstract echo** | No 5+ word abstract phrase verbatim in body. Grep 3 phrases; each must return ≤1 hit. |
| **P — Vendor docs** | read-close-write applies to vendor docs equally. Never write with product page open. |
| **Q — Visual design** | First page: colored title (`\textcolor{darkblue}`), **dark purple italic author** (`\textcolor{slateblue}{\itshape ...}`), mdframed abstract box (darkblue border + light fill), mdframed keywords box. Figures: resource-coded colors, diverging heatmap scale, colored branch taxonomy. IEEEtran abstract label: suppress via `\makeatletter` redefine — `\renewcommand` alone does NOT remove the hardcoded `---`. Full spec: `references/visual-design.md`. |

---

## IEEE Citation Rules (Mandatory)

All inline citations: `[N]` format only — never `(Author, Year)`.

```
Journal:  [N] A. Author, "Title," Abbrev. J., vol. X, no. Y, pp. ZZ–ZZ, Year.
Conf:     [N] A. Author, "Title," in Proc. CONF, City, Year, pp. ZZ–ZZ.
Book:     [N] A. Author, Title, Nth ed. City: Publisher, Year.
Online:   [N] A. Author, "Title," [Online]. Available: https://url. [Accessed: Date].
arXiv:    [N] A. Author, "Title," arXiv:XXXX.XXXXX, Year. [verified IDs only]
```

See `references/ieee-formats.md` for full BibTeX formats and LaTeX templates.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| LaTeX + IEEEtran | `pdflatex` + `bibtex`; `IEEEtran.cls`/`.bst` not in TeX Live — download from https://ctan.org/pkg/ieeetran and place in paper directory |
| Python 3 | For `generate_pdf.py` quick review builds only |
| WebSearch / WebFetch | Required for citation verification (Citation Verification Protocol) |

**Version awareness:** IEEEtran template versions and venue page limits change annually.
Before any submission, re-check the CFP for current formatting requirements.

**Official Documentation Resources:**

| Resource | URL | Use For |
|---|---|---|
| IEEEtran official | https://www.ieeetran.com | Template changelog, LaTeX class options |
| CTAN IEEEtran | https://ctan.org/pkg/ieeetran | Download `.cls`/`.bst` files |
| IEEE Author Center | https://journals.ieeeauthorcenter.ieee.org | Submission guidelines, ethics, formatting rules |
| IEEE Manuscript Tools | https://ieee-author-tools.ieee.org | PDF checker, accessibility checker |
| arXiv abstract page | https://arxiv.org/abs/[ID] | arXiv ID + author verification |

For LaTeX patterns not listed in `references/ieee-formats.md`, consult the IEEEtran official site or the IEEE Author Center above.

---

## Output Delivered

```
paper-title/
├── main.tex                ← LaTeX source (IEEEtran)
├── paper.md                ← Markdown for review
├── references.bib          ← BibTeX entries
├── generate_pdf.py         ← Quick PDF generator (no LaTeX install needed)
├── figures/                ← Figure files (PDF/PNG)
└── SUBMISSION-CHECKLIST.md ← Venue-specific pre-submission checklist
```

LaTeX class:
- Conference: `\documentclass[conference]{IEEEtran}`
- Journal/Transactions: `\documentclass[journal]{IEEEtran}`

Quick PDF (for review only, not IEEE two-column):
```bash
python3 generate_pdf.py
```

Official IEEE two-column PDF (for submission):
```bash
pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
```

---

## Citation Verification Protocol (Run After Writing)

Batch 5 WebSearch calls per message: query format `Author "Title" Venue Year`.

For each result: (1) confirm arXiv ID in URL (`arxiv.org/abs/XXXX.XXXXX`); (2) match title and authors; (3) verify DOI on publisher site — DOIs can be wrong even when title/year are correct; (4) verify URLs live; (5) mark ✅ in SUBMISSION-CHECKLIST.md.

Tag user-provided current events as `[CITE-USER]` with a note to replace before submission. DOI mismatches are the most common error — always verify on the journal site, not just from search results.

### Replacing [CITE-USER] Tags (Current Events Protocol)

Run WebSearch per claim. Match source to claim type: conflict/leadership → BBC, Reuters, Britannica; military incidents → Air & Space Forces, Breaking Defense; economic → Federal Reserve, IMF; civilian casualties → HRW, Amnesty; government statements → Al Jazeera, NPR; proxy activity → Soufan Center, ACLED; military analysis → RAND, IISS.

**Re-verify numbers** against the replacement source — user-provided figures often differ from verified counts. Update body text to match the verified source.

---

## How to Submit to IEEE

See `references/submission-checklist.md` Section 10 for portal URLs, cover letter template, and upload steps.

---

## /grade-paper Command

See `references/grade-paper.md` for the full grading rubric, auto-fix protocol, and report format template.

---

## Reference Files

| File | Read When |
|---|---|
| `references/paper-structure.md` | Drafting any research-paper section — detailed requirements per section |
| `references/book-structure.md` | Variant E — book/academic textbook: chapter shape, defaults, model routing |
| `references/ieee-formats.md` | LaTeX template, all BibTeX types, figure/table code |
| `references/writing-standards.md` | Academic voice, hedging, contribution statement, reproducibility |
| `references/writing-rules.md` | **Before writing** — full text of Rules A–P with safe/unsafe examples |
| `references/agent-workflow.md` | Agent prompts, Paper Brief template, Fact-Checker report format |
| `references/domain-specific.md` | Domain detected (CS/AI, EE, Robotics, Comms, NLP) |
| `references/survey-paper.md` | Variant B — survey/review paper structure |
| `references/rebuttal.md` | Variant C — responding to reviewer comments |
| `references/figures-design.md` | Designing effective figures, architecture diagrams, result plots |
| `references/math-notation.md` | Theorems, proofs, algorithm blocks, notation consistency |
| `references/anti-hallucination.md` | **Before writing** — stat verification, arXiv protocol |
| `references/anti-plagiarism.md` | **Before writing** — read-close-write, scanner thresholds |
| `references/anti-ai-detection.md` | **Before writing** — banned phrases, burstiness, scanner suite |
| `references/audit-commands.md` | **Before delivering** — 17 bash checks, fix actions |
| `references/submission-checklist.md` | Pre-submission + blind review + ethics statement + submission portals |
| `references/grade-paper.md` | `/grade-paper` command — grading rubric, auto-fix protocol, report format |

**Quick access for large files (>300 lines):**
- `figures-design.md` (552 lines): grep for `Taxonomy tree\|Architecture stack\|Bar chart\|Heatmap\|Hybrid flow\|Two-branch`
- `agent-workflow.md` (331 lines): grep for `Agent 1\|Agent 2\|Agent 3\|Agent 4\|Agent 5\|Paper Brief`
- `anti-ai-detection.md` (384 lines): grep for `Banned phrases\|Burstiness\|Scanner suite`
- `anti-plagiarism.md` (353 lines): grep for `read-close-write\|Self-plagiarism\|Mosaic`
- `writing-rules.md`: grep for `Rule A\|Rule B\|Rule C...` to jump to specific rule
