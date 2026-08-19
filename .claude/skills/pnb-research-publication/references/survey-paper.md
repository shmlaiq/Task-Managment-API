# Survey / Review Paper Guide

## Survey vs Research Paper — Key Differences

| Feature | Research Paper | Survey Paper |
|---|---|---|
| Contribution | New method/result | Comprehensive coverage + taxonomy |
| Sections | Methodology + Experiments | Taxonomy + Analysis + Challenges |
| Length | 6–8 pages (conf) | 15–30+ pages (journal) |
| Citations | 25–50 | 80–200+ |
| Novelty | New algorithm/dataset | New organization + insights |
| Experiments | Your own results | Comparison of existing results |

---

## Survey Paper Structure (Mandatory)

```
1.  Title              — "A Survey of X" or "X: A Comprehensive Review"
2.  Authors + Affiliations
3.  Abstract           — scope, methodology, key findings, 250 words max
4.  Index Terms        — 4–6 keywords covering the survey domain
5.  Introduction       — motivation for survey, scope definition, contributions
6.  Background         — foundational concepts readers must know
7.  Taxonomy           — your classification framework (the core contribution)
8.  Coverage Sections  — one section per taxonomy category (most of the paper)
9.  Benchmark Datasets — overview of common evaluation datasets
10. Evaluation Metrics — metrics used across the field, when each is appropriate
11. Comparison Tables  — systematic comparison of methods
12. Open Challenges    — what the field has not solved yet
13. Future Directions  — specific, concrete research opportunities
14. Conclusion
15. References         — IEEE [N] format, 80–200+ entries
```

---

## Section 5 — Introduction for Surveys

A survey introduction must answer:
1. **Why now?** Why is a survey of this topic needed at this moment?
2. **What scope?** What is included and what is explicitly excluded?
3. **How is it organized?** What is the taxonomy structure?
4. **What is new vs prior surveys?** How does this survey differ from existing ones?

```latex
\section{Introduction}

[Opening: state the field and why it has grown to the point of needing a survey]

Several surveys have examined related topics: [N] covers X but excludes Y;
[N] focuses on Z but predates the emergence of [recent development].
This survey differs in three ways:
\begin{itemize}
  \item We cover [specific scope] from [year] to [year].
  \item We introduce a new taxonomy based on [criterion].
  \item We include [N] methods, compared to [M] in the most recent prior survey [N].
\end{itemize}

The rest of this survey is organized as follows...
```

---

## Section 7 — Taxonomy (Core Contribution)

The taxonomy IS the intellectual contribution of a survey. A bad taxonomy = a bad survey.

### Taxonomy design principles:
1. **Mutually exclusive**: a method should fit in exactly one category (or clearly explained if it spans)
2. **Collectively exhaustive**: the taxonomy should cover all known methods in scope
3. **Principled criterion**: based on architectural choice, learning paradigm, application, or problem formulation
4. **Hierarchical**: top-level categories, then subcategories

### How to present the taxonomy:

```latex
\section{Taxonomy}

We classify existing methods along two axes: (1) [criterion A], and (2) [criterion B].
This yields four categories, illustrated in Fig.~\ref{fig:taxonomy}:

\begin{itemize}
  \item \textbf{Category A1-B1}: Methods that [description]. Representative works: [N][N][N].
  \item \textbf{Category A1-B2}: Methods that [description]. Representative works: [N][N].
  \item ...
\end{itemize}
```

Include a taxonomy figure (tree diagram or 2D grid) — it is the most-cited part of any survey.

---

## Section 8 — Coverage Sections

Each coverage section = one taxonomy category. Structure per section:

```
A. [Category Name]

[Opening: what unifies the methods in this category]

A.1 [Subcategory]
[3–5 representative papers, described with their key ideas — NOT a laundry list]
[Compare them: what do they share? Where do they differ?]

A.2 [Subcategory]
[...]

[Closing: what are the limitations of this entire category?]
```

**Anti-pattern to avoid** (laundry list):
```
Method A [N] does X. Method B [N] does Y. Method C [N] does Z.
```

**Correct pattern** (comparative analysis):
```
Category A methods share a common assumption: [X]. This allows them to [advantage],
but limits them to [scope]. Within this category, methods diverge on [dimension]:
[N] uses approach P, which excels at [strength] but fails when [condition].
[N] instead uses approach Q, trading [cost] for [benefit].
```

---

## Section 11 — Comparison Tables

The comparison table is the most practically useful section of any survey.

```latex
\begin{table*}[t]
\caption{Comparison of Representative Methods on [Benchmark]}
\label{tab:comparison}
\centering
\begin{tabular}{llccccl}
\toprule
Method & Year & Venue & [Metric 1] & [Metric 2] & [Metric 3] & Key Feature \\
\midrule
Method A [3]  & 2019 & CVPR & 72.4 & 45.1 & 120ms & [what makes it unique] \\
Method B [7]  & 2021 & NeurIPS & 78.1 & 51.3 & 95ms  & [what makes it unique] \\
Method C [12] & 2023 & ICCV & 83.5 & 58.7 & 67ms  & [what makes it unique] \\
\bottomrule
\end{tabular}
\vspace{2pt}
{\small Results reproduced from original papers. All methods evaluated on [Dataset] [N].}
\end{table*}
```

**Rules for comparison tables:**
- Every number must come from the original paper — cite the source
- Use the same dataset/split for all comparisons when possible
- If different splits are used, note explicitly: "(†) evaluated on full val set"
- Do NOT include your own new results in a survey (this is a research paper contribution)

---

## Section 12 — Open Challenges

This section distinguishes a good survey from a great one. Reviewers look for genuine insight.

**Good challenge format:**
```
C1. [Challenge Name]: [precise description of what is unsolved and why it is hard]
    Current best: [what has been tried and how far it gets]
    Why it persists: [fundamental difficulty — not just "more data needed"]
    Progress indicators: [how we would know when it is solved]
```

**Bad challenge format:**
```
"More efficient methods are needed." (too vague)
"Better datasets would help." (not actionable)
```

---

## Literature Agent Rules for Surveys

The Literature Agent must:
1. Find papers from **multiple time periods** — not just recent ones
2. Cover all **major sub-communities** working on the topic
3. Include **foundational/seminal papers** (even if old)
4. Note papers that were **influential but superseded**
5. Find **benchmark papers** (dataset papers, evaluation frameworks)
6. Look for **prior surveys** to cite and differentiate from

Minimum coverage: 80 papers for a focused survey, 150+ for a broad survey.

---

## Pre-Submission Survey Checklist

- [ ] Taxonomy is original — not just repeating a prior survey's categories
- [ ] All methods in scope are covered (no significant omissions)
- [ ] Comparison table has ≥10 methods with cited numbers
- [ ] Open challenges are specific and insightful (not generic)
- [ ] Future directions are concrete (not "more research is needed")
- [ ] Prior surveys are cited and differentiated from
- [ ] iThenticate < 15% (surveys are high-risk for plagiarism due to volume of paraphrasing)
- [ ] References: 80+ entries, all verified
- [ ] No placeholder arXiv IDs
