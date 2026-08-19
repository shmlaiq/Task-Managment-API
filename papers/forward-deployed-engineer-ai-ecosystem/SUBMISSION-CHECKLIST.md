# Submission Checklist — "Forward Deployed Engineer (FDE) in the AI Ecosystem"

Paper type: Conceptual / Proposed-Framework paper (Variant D — no empirical experiments)
Target venue: IEEE Access
Author: Muhammad Faisal Laiq (no institutional affiliation) — shmlaiq@gmail.com — ORCID 0009-0007-5779-9836

## 1. Formatting & Structure
- [x] `\documentclass[journal]{IEEEtran}` — IEEE Access uses the journal class
- [x] Compiles cleanly: `pdflatex → bibtex → pdflatex → pdflatex`, 8 pages, zero errors, zero undefined references
- [x] Section headings I–VII with lettered subsections (A, B, C...); no subsection has only one item
- [x] `\IEEEPARstart{J}{ob}` used on the Introduction's first paragraph
- [x] Abstract 150–250 words (delivered: ~230 words), no citations, no undefined acronyms inside the abstract itself
- [x] Index Terms present (5 terms)

## 2. Content
- [x] Contribution statement present in Introduction, exact IEEE phrasing + itemized list
- [x] All 7 sections present per Variant D structure (Intro, Related Work, Background, Proposed Framework, Case Analysis, Limitations, Conclusion)
- [x] 5 named limitations in Section VI, ordered by severity
- [x] Future work in Section VII ordered by urgency, not by count/symmetry

## 3. Citations — IEEE Format
- [x] All inline citations use `\cite{}` / `[N]` — never `(Author, Year)`
- [x] Citation numbering strictly follows order of first appearance (verified against compiled `main.bbl`)
- [x] 17 references, all cited at least once, zero orphaned `.bib` entries
- [x] Zero `and others` in any BibTeX author list
- [x] All 3 arXiv IDs independently verified live (2507.21504, 2511.17676, 2504.20119)
- [x] All company careers-page / blog citations independently verified (or explicitly hedged where re-verification wasn't possible — see Known Gaps below)

## 4. Visual Design (Rule Q)
- [x] Colored title (`darkblue`)
- [x] Styled author block (`slateblue`, italic)
- [x] mdframed colored Abstract box
- [x] mdframed colored Index Terms box
- [x] Fig. 1 (TikZ engagement-lifecycle loop) uses the darkblue/ambercolor convention, not monochrome

## 5. Figures and Tables
- [x] Fig. 1 is a real TikZ diagram in main.tex — zero `\figplaceholder` calls
- [x] Table I and Table II use `booktabs`, captions above, referenced inline as "Table~\ref{}"
- [x] Both tables fit within `\textwidth` after `p{}`-column + `\footnotesize` fix (initial overfull-hbox issue resolved)

## 6. Blind Review
- N/A — IEEE Access is single-blind; author block is intentionally not anonymized.

## 7. Ethics & Compliance
- [x] No human-subjects data, no primary data collection — paper is explicit about this in Section VI (Limitation #4)
- [x] No AI-use disclosure statement included. **Action for author before submission:** check IEEE Access's current AI-assistance disclosure policy at submission time and add a disclosure statement if required — this paper was produced with AI-assisted drafting and research under human direction, review, and fact-checking, and IEEE Access's policy on disclosing that may have changed since this checklist was written.

## 8. Final Build Check
- [x] `pdflatex -interaction=nonstopmode main.tex && bibtex main && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex` — clean, 8 pages
- [x] `grep -c "^\\bibitem" main.bbl` → 17 (matches references.bib entry count)
- [x] No "Citation undefined" or "Reference undefined" warnings in final log

## 9. Known Gaps / Recommended Author Review Before Submission
These are honest, flagged limitations from the fact-checking pass — not blockers, but worth a final human read before you submit:

1. **Scale AI case study (Section V.D)** is explicitly hedged as lower-confidence than the other three companies — the live job posting could not be independently re-fetched (dynamically loaded content, standard bot protection). If you have direct access to the current Scale AI FDE posting, a quick manual re-check would strengthen this subsection.
2. **Palantir's exact FDE founding year** is stated as "early 2010s" based on the single best-available secondary source (The Pragmatic Engineer). No primary Palantir source with an exact date was found. This is stated as a hedge, not a hard date, and should stay that way unless you find a primary source.
3. **AI-use disclosure** (see Section 7 above) — confirm IEEE Access's current policy before submission.
4. This paper makes no causal claims and collected no primary survey/interview data — that is a deliberate, load-bearing limitation (Section VI), not a gap to "fix" before submission. Do not let a reviewer push you into overclaiming here.

## 10. Submission
IEEE Access submits through IEEE Author Portal / ScholarOne. See https://ieeeaccess.ieee.org for current author guidelines and article processing charge information before submitting — venue requirements can change; verify against the live CFP at submission time.
