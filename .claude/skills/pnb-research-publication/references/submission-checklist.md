# Pre-Submission Checklist

Use this checklist before submitting to any IEEE conference or journal.
All items must pass. Items marked [BLOCKER] will cause desk rejection.

---

## 1. Formatting & Structure

- [ ] **[BLOCKER]** Paper uses `\documentclass{IEEEtran}` (conference) or `\documentclass[journal]{IEEEtran}`
- [ ] **[BLOCKER]** Page count within venue limit (conference: typically 8 pages; check CFP)
- [ ] References on separate unlimited pages (IEEE conferences allow unlimited reference pages)
- [ ] Two-column layout renders correctly (no text overflow, no broken tables)
- [ ] Font size not manually reduced to fit more text (10pt minimum)
- [ ] Margins not manually reduced
- [ ] `\IEEEPARstart` used for first paragraph of Introduction

---

## 2. Content — Required Sections

- [ ] **[BLOCKER]** Abstract present (150–250 words, no citations, no undefined acronyms)
- [ ] **[BLOCKER]** Abstract ends with a significance/contribution statement — NOT with a limitations statement or open question
- [ ] **[BLOCKER]** All non-standard acronyms expanded on first use in abstract (QMD, VPS, RLHF, etc. — not CPU/GPU/OS/API/RAM/HTTP/AI/ML/LLM)
- [ ] **[BLOCKER]** Index Terms / Keywords present (4–6 terms)
- [ ] Introduction with explicit contribution statement ("The contributions of this paper are:")
- [ ] Related Work section (grouped by theme, not chronology)
- [ ] Methodology section (problem formulation + proposed approach)
- [ ] Experiments section (setup, datasets, baselines, metrics)
- [ ] Results section (tables, figures, ablation study)
- [ ] Conclusion (what was shown, future work — no new claims)
- [ ] **[BLOCKER]** Acknowledgments section present between Conclusion and References — IEEE requires funding disclosure and conflict-of-interest statement. A minimal one-sentence placeholder is sufficient for solo authors with no funding: "The author thanks [community/colleagues]. No external funding was received for this work."
- [ ] References section

---

## 3. Citations — IEEE Format

- [ ] **[BLOCKER]** All citations use `[N]` format — no `(Author, Year)` anywhere
- [ ] **[BLOCKER]** No placeholder arXiv IDs (`arXiv:XXXX.XXXXX` pattern absent)
- [ ] No `[CITE NEEDED]` or `[Unverified]` markers remaining
- [ ] Every `[N]` in body has a corresponding References entry
- [ ] **[BLOCKER]** Every reference in `.bib` is cited at least once in the body — run:
  ```bash
  comm -23 \
    <(grep -o '@[a-z]*{[^,]*' references.bib | sed 's/@[a-z]*{//' | sort) \
    <(grep -o '\\cite{[^}]*}' main.tex | sed 's/\\cite{//;s/}//' | tr ',' '\n' | sort -u)
  # Must return empty. Any key listed = uncited reference = IEEE violation.
  ```
- [ ] **[BLOCKER]** paper.md and main.tex are in sync — spot-check 3 paragraphs:
  pick one from Abstract, one from Architecture/Methodology, one from Conclusion;
  verify same facts, numbers, and claims appear in both files.
- [ ] **[BLOCKER]** BibTeX entry type matches paper.md reference display format — arXiv preprints must use `@misc`/`@article` with `archivePrefix = {arXiv}`; conference papers must use `@inproceedings` with correct `booktitle`. Compiled LaTeX derives format from `.bib` — a mismatch means the PDF shows a different venue than paper.md.
- [ ] No citations to Wikipedia, blog posts, or press releases as primary evidence
- [ ] External event claims cited ("announced at GTC 2026" requires a citation to official source)
- [ ] Named third-party products cited ("NVIDIA's OpenShell framework" requires official documentation citation)
- [ ] Third-party product specs cited (rate limits, pricing tiers, hardware wattage — cite vendor's official docs or remove specific figures)
- [ ] No dollar amounts or hardware specs in code block comments without a prose citation nearby
- [ ] Seminal papers in the field cited (reviewers expect foundational works)
- [ ] All arXiv IDs verified at `https://arxiv.org/abs/XXXX.XXXXX`

---

## 4. Visual Design (Rule Q — Mandatory)

See full spec: `references/visual-design.md`

- [ ] **[BLOCKER]** Title uses `\textcolor{darkblue}{...}` — not black default
- [ ] **[BLOCKER]** Author block uses `\textcolor{slateblue}{\itshape ...}` — italic + dark purple (`RGB{90,80,160}`)
- [ ] Abstract: mdframed box INSIDE `\begin{abstract}` (never the reverse — breaks column spanning)
- [ ] Abstract label: custom bold darkblue "Abstract---" inside mdframed box; IEEEtran's hardcoded label suppressed via `\makeatletter\def\abstract{...}\makeatother` in preamble
- [ ] IEEEkeywords: mdframed box INSIDE `\begin{IEEEkeywords}` with custom "Index Terms---" label
- [ ] `\usepackage{mdframed}` in preamble
- [ ] All 7 colors defined: `darkblue`, `midgreen`, `deepred`, `steelblue`, `tealcolor`, `ambercolor`, `slateblue`
- [ ] `\hypersetup{colorlinks=true,linkcolor=darkblue,...}` set
- [ ] Page 1 rendered to PNG and visually verified before delivery
- [ ] No blank page 1 (symptom of `\IEEEspecialpapernotice` misuse — see visual-design.md)

---

## 5. Figures and Tables

- [ ] **[BLOCKER]** Every figure cited by number in body prose ("as shown in Fig. 1", "Fig. 3 illustrates", "see Fig. 4") at or before the figure placement — caption alone does not satisfy IEEE inline citation requirement
- [ ] Every table referenced inline: "as shown in Table~\ref{tab:X}"
- [ ] Figure captions are below figures (`\caption` after `\includegraphics`)
- [ ] Table captions are above tables (`\caption` before `\tabular`)
- [ ] Best result in each table column is **bold**
- [ ] No figure placeholder text or broken `\ref` references
- [ ] All figures use resource-coded colors (not monochrome) — see `references/visual-design.md`
- [ ] Heatmaps use diverging color scale (gray→yellow→orange→red), not all-blue
- [ ] Taxonomy/tree diagrams have color-coded branches
- [ ] Matrix figures have colored column headers and bold dominant cells
- [ ] All figures are readable in grayscale (for printed proceedings)
- [ ] Figure file formats: PDF or high-res PNG (minimum 300 DPI)
- [ ] All figures have alt-text equivalent in caption

---

## 5. Reproducibility

- [ ] All datasets named with version and citation
- [ ] All baselines named with paper citations
- [ ] All metrics precisely defined (what split? what metric variant?)
- [ ] Key hyperparameters reported (learning rate, batch size, optimizer, scheduler, epochs)
- [ ] Hardware and training time reported
- [ ] Code/model/dataset availability stated (URL or "upon acceptance")
- [ ] Random seed(s) reported, or results averaged over N runs with std dev

---

## 6. Blind Review Preparation (if double-blind)

- [ ] **[BLOCKER]** Author names and affiliations removed from paper
- [ ] **[BLOCKER]** `\author{Anonymous Authors}` or equivalent
- [ ] Acknowledgments section removed entirely
- [ ] Self-citations anonymized: "In our prior work [ANON]" or removed
- [ ] GitHub URLs do not reveal author org (fork to anonymous repo)
- [ ] No identifying information in paper metadata (PDF title, author field)
- [ ] Supplementary material also anonymized

**To check PDF metadata:**
```bash
pdfinfo paper.pdf | grep -E "Author|Creator|Producer"
# Author field must be empty or "Anonymous"
```

---

## 7. Ethics & Compliance

- [ ] Ethics statement included if required by venue (human subjects, sensitive data, AI-generated content disclosure)
- [ ] Dataset licenses confirmed (you are allowed to use the data)
- [ ] No copyright violations (all quoted text properly attributed)
- [ ] Potential negative societal impacts discussed (required by NeurIPS, ICML, and others)
- [ ] Funding/conflict of interest disclosed in Acknowledgments (or noted as none)

---

## 8. Final Build Check

### 8a — Pre-flight: Download IEEEtran class files (not in TeX Live)

IEEEtran.cls and IEEEtran.bst are NOT included in any TeX Live distribution.
Download them into the paper directory before the first build.

```bash
# IEEEtran LaTeX class (document formatting)
curl -sL "https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.cls" -o IEEEtran.cls
wc -c IEEEtran.cls   # must be ~270KB. If <10KB: got an HTML redirect — see note below.

# IEEEtran BibTeX style (reference formatting)
# CRITICAL: use the /bibtex/ subdirectory path — the root path returns an HTML redirect
curl -sL "https://mirrors.ctan.org/macros/latex/contrib/IEEEtran/bibtex/IEEEtran.bst" -o IEEEtran.bst
wc -c IEEEtran.bst   # must be ~57KB. If <1KB: got an HTML page — use the path above exactly.

# Verify both files are valid LaTeX/BibTeX (not HTML)
head -2 IEEEtran.cls   # should start with "% IEEEtran.cls"
head -2 IEEEtran.bst   # should start with "%%"
```

**CTAN redirect pitfall:** `mirrors.ctan.org/macros/latex/contrib/IEEEtran/IEEEtran.bst`
(without `/bibtex/`) returns an HTML page, not the .bst file. Always use the
`/bibtex/IEEEtran.bst` path shown above.

### 8b — Correct build order (ORDER MATTERS)

```bash
# WRONG order (bibtex before pdflatex): bibtex reads stale .aux → new \cite{} keys undefined
# CORRECT order: pdflatex first to generate .aux, then bibtex reads fresh .aux

pdflatex -interaction=nonstopmode main.tex   # pass 1: generates .aux with all \cite{} keys
bibtex main                                   # reads .aux, generates .bbl from references.bib
pdflatex -interaction=nonstopmode main.tex   # pass 2: inserts bibliography
pdflatex -interaction=nonstopmode main.tex   # pass 3: resolves cross-references

# Verify build succeeded
grep "undefined\|Warning" main.log | grep -v "Font\|Redefin\|Info" | head -10
# Must return empty. Any "Citation undefined" = a \cite{key} whose key is not in .bib

# Check for undefined references
grep "??" main.log   # should be empty

# Count pages
pdfinfo main.pdf | grep Pages

# Word count (approximate)
pdftotext main.pdf - | wc -w
```

---

## 9. Submission Portal

- [ ] PDF compiled without errors or warnings
- [ ] File size within venue limit (usually 10–20 MB)
- [ ] Title in submission portal matches title in PDF
- [ ] Author list in portal matches paper (if not blind review)
- [ ] Abstract in portal matches paper abstract exactly
- [ ] Correct track/area/topic selected
- [ ] Supplementary material uploaded separately (if applicable)
- [ ] Submission confirmed with confirmation email received

---

## Venue-Specific Page Limits Quick Reference

| Venue | Main Paper | References | Notes |
|---|---|---|---|
| IEEE CVPR | 8 pages | Unlimited | Double-blind |
| IEEE ICCV | 8 pages | Unlimited | Double-blind |
| IEEE ICRA | 6 pages | 1 page (7 total) | Single-blind |
| IEEE IROS | 6 pages | 1 page (7 total) | Single-blind |
| IEEE Transactions (most) | No hard limit | Included | Single-blind |
| IEEE Letters | 4–5 pages | Included | Single-blind |
| NeurIPS | 9 pages | Unlimited | Double-blind |
| ICML | 8 pages | Unlimited | Double-blind |

**Always check the current CFP** — limits change between years.

---

## 10. How to Submit to IEEE

| Journal | Submission URL |
|---|---|
| IEEE Transactions on Technology and Society | mc.manuscriptcentral.com/t-ts |
| IEEE Transactions on Neural Networks | mc.manuscriptcentral.com/tnnls |
| IEEE Access | ieee.atyponrex.com/journal/access |
| IEEE Security & Privacy | mc.manuscriptcentral.com/ieeessp |

Steps:
1. Create account at ScholarOne
2. Upload: `main.tex` + `references.bib` + cover letter (1 page)
3. Select subject areas, confirm no dual submission
4. Submit — expect desk review in 2–4 weeks

**Cover letter template:**
```
Dear Editor-in-Chief,

We submit "[Title]" for consideration in [Journal Name].

[2-sentence paper summary: problem + contribution]

The manuscript addresses [specific gap] that no existing work covers.
It has not been submitted elsewhere.

Sincerely,
[Author Name]
```
