# Writing Rules A–P (Full Enforcement Detail)

These rules address issues that caused grade deductions in prior papers. Read this file
before writing Section I. Each rule is ON from the first sentence — no deferral.

---

## Rule A — Formula parameters must be fully specified

Every parameter in any equation must have: (1) its domain stated (e.g., α ∈ [0,1]),
(2) a concrete default value for the general case, and (3) recommended values for at
least two specific workload types. Never leave a parameter as "tunable" without
specifying what to tune it to.

---

## Rule B — Source rephrasing must be structurally unrecognisable

A safe paraphrase differs in both sentence structure AND vocabulary. After writing a
sentence about prior work, ask: "Could a reader identify this as paraphrased from
[Source] without the citation?" If yes — rewrite.

Changing "context window is RAM, storage is disk" to "context window functions as
working memory, storage is the disk equivalent" is NOT safe. A safe version inverts the
sentence order, uses different nouns, and draws the analogy from a different angle.

---

## Rule C — Every mechanism must have a complete escalation path

Any protocol, policy, or mechanism described in the paper must specify: normal path,
error/conflict path, and fallback (HITL or operator action). The phrase "is not fully
specified" or "is left for future work" is a grading deduction. If a full specification
is genuinely out of scope, state explicitly what the trigger condition is and what the
fallback action is — even if the middle steps are TBD.

---

## Rule D — Conceptual papers require a Theoretical Analysis subsection

Every Variant D paper (proposed architecture, no implementation) must include a
Theoretical Analysis subsection in Section V (Analysis / Discussion) containing:
(1) complexity analysis of the core algorithm or policy,
(2) a formal dominance argument or proof sketch showing the proposed approach improves
    on the baseline under stated conditions,
(3) at least one quantitative bound derived directly from the architecture's parameters.

Use multipliers and ratios (e.g., 25×, O(n log n)) rather than bare percentages to
avoid citation audit failures on derived numbers.

---

## Rule E — Multi-platform installation sections must vary paragraph rhythm

When a paper includes an installation manual with ≥5 platform subsections, all
subsections must NOT follow the same opening structure. Identical rhythm (context
sentence → bash block → notes) triggers AI detection even when individual sentences
are humanized.

Required: vary the opening strategy in at least 3 of N subsections:
- Lead with the platform's key behavioral difference vs. the previous platform
- Lead with the decision criterion for choosing this path
- Lead with the most common failure mode
- Lead with a constraint or prerequisite specific to this platform

After writing all subsections, scan their first sentences. If 3+ start with
"[Platform] installation" or directly with a code block — restructure.

---

## Rule F — Conclusion future work must be ordered by urgency, not by symmetry

AI-generated future work announces a fixed count ("Three limitations...") then presents
them as uniform-length items. Human researchers order by urgency and write each item at
a different length with different framing.

Required pattern:
- Item 1: Most pressing/observable gap. Short setup sentence + concrete trigger.
  State that no mechanism exists today.
- Item 2: Structurally different category. Explain why it differs from Item 1.
- Item 3: Binary prerequisite. Frame as "X is a prerequisite for Y use case."

Never use: "Three/Four/Five limitations are the most consequential targets for future
work." This is a grading deduction trigger.

See `references/paper-structure.md` for the full pattern.

---

## Rule G — Every reference in references.bib must be cited inline in the body

Adding a reference to the bibliography but not citing it in the body is an IEEE rule
violation. It is also a quality signal that the reference was padded rather than used.

This error is easy to miss: paper.md uses `[N]` numbers and a written-out list — uncited
entries look like cited ones. In main.tex, BibTeX includes uncited entries silently.

Detection: run audit command 6 before every delivery. Any key returned is uncited and
must either:
- Be given a natural inline citation where it genuinely strengthens the argument, OR
- Be removed from references.bib entirely

Never add inline citations in awkward positions just to force a reference to appear cited.

---

## Rule H — paper.md and main.tex must stay in sync throughout writing

Both files are canonical: paper.md is the review copy, main.tex is the submission copy.
Editing one without updating the other creates a silent version split.

Sync discipline:
- After ANY edit to paper.md, immediately update the corresponding paragraph in main.tex.
- After ANY edit to main.tex, verify the change is reflected in paper.md.
- Before final delivery, run audit check 7: pick 3 paragraphs (Abstract, Architecture,
  Conclusion) and confirm the same facts and numbers appear in both files.
- High-risk sections for drift: installation subsections, conclusion, any section with
  equations or numbers.

Sync drift caught in prior work: Linux installation section, Remote Access section, and
Conclusion were all edited in paper.md but main.tex was not updated — 3 sections out of
sync at delivery.

---

## Rule I — External factual claims must be cited or removed

External factual claims include: named events and their dates, named third-party product
features, hardware specifications, benchmark results from prior work, pricing, rate
limits, and code comments that assert factual details.

| Claim Type | Example | Treatment |
|---|---|---|
| Named public event | "announced at GTC 2026" | Cite the press release or primary source |
| Named third-party product feature | "NVIDIA's OpenShell sandbox framework" | Cite official docs, or remove if unverifiable |
| Third-party spec (rate limits, pricing) | "Gemini: 15 RPM free tier" | Cite official API docs at time of writing |
| Hardware specifications | "Pi 4 draws approximately 3–5W" | Cite datasheet, or describe capability not wattage |
| Code block factual claims | `# Hetzner CX11 at ~$5/month` | Remove dollar amount; use "budget provider" |
| BibTeX venue type | `@inproceedings` vs `@article` | Must match how the paper appears in paper.md |

**Why:** Claims that cannot be cited make the paper unfalsifiable. Reviewers who follow
citations and find wrong or missing information lose trust in all other numbers.

**How to apply:** Before writing any sentence that asserts an external fact, ask:
"Is this cited?" If not — add the citation or rewrite to remove the assertion.

---

## Rule J — The abstract must be self-contained and end on significance

The abstract is read independently of the body. Four requirements — all mandatory:

1. **Ends with significance, not limitations.** The final sentence must state the paper's
   contribution or impact. Wrong: "This work is limited to single-user deployments."
   Right: "This analysis establishes a formal OS-layer foundation for the emerging class
   of personal AI employee platforms."

2. **All non-standard acronyms expanded on first use.** Standard exemptions: AI, ML, OS,
   API, CPU, GPU, RAM. Must always expand: LLM, MCP, RAG, HITL, ACP, VPS, QMD, WSL,
   K3s, CoT — and any others first used in abstract.

3. **Factual lists match the body exactly.** If the abstract says "sponsored by OpenAI,
   GitHub, and NVIDIA" but the body lists six sponsors — that is a factual contradiction.
   Count items. Match them.

4. **No citations in the abstract.** IEEE style prohibits inline `[N]` citations.
   Any cited fact must be phrased as a design claim or moved to the Introduction.

---

## Rule K — Figures must be actual TikZ diagrams in main.tex — never placeholders

A `\figplaceholder`, gray shaded box, or `[INSERT FIGURE HERE]` note is a delivery
blocker in every draft, not only the final submission.

Every figure must exist as working TikZ/pgfplots code in main.tex before delivery.
Seven canonical templates in `references/figures-design.md`:

| Figure Type | TikZ Approach |
|---|---|
| Taxonomy tree | Rounded nodes, `arrows.meta` stealth tips, 3-level hierarchy |
| Architecture stack | `darkblue` header + `blue!18` modules + `gray!28` HAL |
| Enhanced architecture | Core center + flanking dashed-border additions |
| Bar chart | `pgfplots` `ybar` with `symbolic x coords`, legend at bottom |
| Heatmap | Manual `\fill[color]` rectangle grid + `\foreach` gridlines |
| Hybrid flow loop | `to[bend left/right]` arrows forming a cycle |
| Two-branch taxonomy | Root → two `blue!20` branch nodes → `gray!10` leaf nodes |

**Required preamble packages:**
```latex
\usepackage{tikz}
\usepackage{pgfplots}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,calc,backgrounds}
\pgfplotsset{compat=1.18}
```

**LaTeX safety rule:** Never use `sed` to insert backslash sequences into a `.tex` file.
The shell double-expands backslashes — `sed 's/foo/\\bar/'` writes `\bar`, but
`sed 's/foo/\\\\begin/'` writes `\\begin` (double backslash) causing cascade errors.
Always use the Edit tool directly for any `.tex` modification.

---

## Rule L — Mathematical bounds must be cited to their primary source

When citing a formula, regret bound, or theorem, the citation must point to the paper
that *proved* that result — not one that merely uses it in a related application.

Ask: "Who proved this bound first?" Common primary sources:
- UCB / bandit bounds → Auer et al. (2002), Abbasi-Yadkori et al. (NeurIPS 2011)
- Attention complexity → Vaswani et al. (2017)
- Graph complexity → cite the original algorithmic paper or algorithmics textbook

---

## Rule M — BibTeX author lists must be complete — never use `and others`

`and others` truncates the author list in the formatted IEEE reference. IEEE requires
full author lists. Truncated lists are citation integrity failures and deduction triggers.

Before writing any `@article` or `@inproceedings` entry: fetch the paper's title page
(`https://arxiv.org/abs/ID` for arXiv; publisher page for journals) and list every author.

```bash
grep -n "and others" references.bib   # Must return zero before delivery
```

---

## Rule N — Derived estimates must be framed as derived

A range computed by applying a formula described in the paper is a *derived* value.
Citing the paper whose formula was used does NOT mean that paper states your derived
range — implying it does is misattribution (−5 per instance).

Safe: "...falls in the 30–70% range — derived from the σ²/S scaling applied to
typical VQA gradient norm ratios; see [N] for the underlying scaling framework."

Unsafe: "...falls in the 30–70% range~\cite{cerezo2021vqa}" (implies Cerezo 2021
states this range).

---

## Rule O — No distinctive phrase from the abstract may appear verbatim in body sections

A phrase that appears verbatim in both abstract and body signals the abstract was
assembled rather than independently written.

Self-similarity check before delivery: identify 3 distinctive phrases (5+ contiguous
words, specific to this paper) in the abstract. Grep for each in the body. If any
appears verbatim outside the abstract, rewrite the body occurrence.

```bash
# Replace PHRASE with 5+ word abstract excerpt:
grep -n "PHRASE" main.tex  # Must return at most one hit (the abstract itself)
```

---

## Rule P — Vendor and official documentation requires read-close-write

The read-close-write method applies equally to vendor documentation, product pages,
official technical specs, and marketing copy. Official docs contain precise phrasing
that iThenticate and Turnitin flag as similarity.

Process: read the vendor doc; close it; write your own characterization using your own
sentence structure, analytical framing, and vocabulary. Then add the citation.

Audit signal: "enables seamless collaboration" or "purpose-built for" in descriptions
of vendor products = flag that read-close-write was not applied.
