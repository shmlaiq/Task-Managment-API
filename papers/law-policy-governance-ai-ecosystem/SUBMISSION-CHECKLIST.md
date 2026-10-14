# Submission Checklist — "Law, Policy, and Governance of the AI Ecosystem for Human Control: The Human-Centric AI Governance and Continuous Oversight Framework (HACOF)"

Target venue: **IEEE Access** (open access journal, single-blind review).
IEEE Access guidelines last verified live: **2026-10-10** (re-verify immediately before upload).
Status as of **2026-10-12 (final audit)**: **32 pages, 79 references, 15 tables, 6 figures, abstract 250 words. Final grade A (91.2/100).** A complete whole-paper audit by an independent Fact-Checker and Editor found 20 Major issues: 12 claim-source mismatches in the older sections and 8 prose/layout issues. All are fixed, and both re-verification passes are CLEAR on Critical/Major. Remaining items: 5 bib entries without URLs (openai2026funding, anthropic2026funding, nvidia2026marketcap, imf2025pakistangdp, sbp2026itexports); small float gap below Table XII; Kish 1965 / Sha 2001 primary-source confirmation. **2026-10-12 prose pass:** 'rather than' cut from 72 to 18 and em-dashes from 211 to 93 (mostly paired asides turned into parentheses, commas or colons); no content or citations removed; abstract still 250 words. Independent Editor re-score: Tone 89 (was 87), Writing 90; overall **A (91.5)**. The 3 Majors the pass introduced (double colon L116, stronger hedge L159, nested parentheses L122) and 9 minor regressions are fixed. **Round 3 done (2026-10-12):** ~15 long sentences split, 22 explanatory colons made into sentences; punctuation density 23.5→21.4 per 1k words, sentences >60 words 22→16. Independent Editor final score: **Tone 92, Writing 91 → overall A (92.1)**; its 1 Major (L390 grammar) and 12 minors are fixed (after the score, not re-scored). Next tone items if wanted: 'real' (26) / 'genuine' (11) / 'entirely' (10); remaining closers L135, L1452. **Round 2 done (2026-10-12):** contrast family 117→~62, 'exactly'/'actually' 25→8, longest sentences split; Editor re-score Tone 91, Writing 90 → overall **A (91.8)**; the 6 slips round 2 introduced (L918 hedge, L279 aphorism, L1313 grammar, L1091, L341, L304) are fixed and the 5 longest sentences split after that score (not re-scored). Still open for tone: semicolon/colon/parenthesis density (~25 per 1k words); ~65 sentences >45 words; closer at L1247 kept on purpose. Earlier round-2 notes: the contrast habit moved to ', not' (39→51) and 'instead of' (3→10); 'exactly'/'actually' (13/11); aphoristic paragraph closers; 90 sentences >45 words (L120, L1313, L341).

> **Revision note (2026-10-11).** The paper was restructured around HACOF as its central contribution, per the author's direction. The changes:
> - **New sections and figures:** a new title subtitle, abstract, Introduction opening (Proposition box), Section V (HACOF, subsections A–L), Section VII (evaluation protocol plus staged-deployment roadmap), and a new Related Work subsection on runtime oversight of AI agents. Fig. 2 is the HACOF flow and Fig. 3 is the lifecycle loop.
> - **Removed material:** the Nigeria/Bangladesh comparison and the Gulf, Peru and PECA material (7 bib entries dropped).
> - **References:** grew from 50 to 78 (28 newly verified).
> - **Factual corrections in pre-existing text:** the EU AI Act's high-risk obligations are now dated per the Digital Omnibus, Reg. (EU) 2026/1744 (2 Dec 2027 / 2 Aug 2028); the Pakistan audit-provision claim is corrected; and the labor-market claim, previously cited to a study using only US data, is reframed.

---

## 0. Session 2026-10-14: IEEE Access port, link check, length inquiry
- [x] **Template port done:** `access/` holds the official IEEE Access LaTeX template (ACCESS_latex_template_20260513, downloaded from ieeeaccess.ieee.org). The port is `access/main.tex` and builds to `access/main.pdf`: **33 pages, 0 errors, 0 undefined, 0 BibTeX warnings**, every page visually inspected. **Upload `access/main.tex` + `access/main.pdf`**, not the root IEEEtran files, which are kept as a backup (32 pp, also rebuilt clean).
  - Port fixes: (1) `ieeeaccess.cls` redefines `\year`, which breaks PGF's RNG seed (240 errors plus a blank page after every page), so the TeX primitive is restored while TikZ/pgfplots load; (2) the class's PANTONE spot `accessblue` is invisible under `xcolor`, so it is redefined in CMYK with the same ink values; (3) the class's `\textbf` breaks nested `\textcolor` in the 4 box titles, so they use `\bfseries` inside the color instead; (4) the class owns heading colors, so the per-heading `\textcolor` wrappers were removed; (5) keywords are in alphabetical order (template rule). **No text cut.**
  - Placeholders left as IEEE fills them: `\history`, `\doi`, "VOLUME 11, 2023" footer.
- [x] **Live link check (66 links): 0 dead.** 46 OK, 17 bot-blocked but confirmed live, 3 redirects. Basel URL updated to the new BIS PDF.
- [x] **5 URL-less refs fixed and verified against sources by the Lead:** Anthropic (official post), OpenAI (SiliconANGLE; openai.com returns 403 to automated fetches, so its URL is given in the note), NVIDIA (CompaniesMarketCap; Forbes attribution was unsupported and removed), IMF (DataMapper), SBP (primary PDF, row 9: 3,814 / 4,600).
- [x] **Fact correction:** Pakistan's 2025 GDP changed from $407.8B to **$408.2B** (current IMF WEO data) in the text, bib and paper.md.
- [x] **EIC length inquiry drafted:** `EIC-LENGTH-INQUIRY.md`. **Send it and wait for permission before uploading.**
- [ ] **Author biography + photo:** the IEEE Access template ends with `IEEEbiography` blocks. Supply a short bio (and photo, or use `IEEEbiographynophoto`). Not added, because no placeholder content is used without the author's approval.
- [ ] **Abstract wording:** the template says the abstract must be "without abbreviations". The current abstract defines AI, HACOF and HITL in parentheses. This is common in published IEEE Access abstracts, but the author decides.
- [ ] **Portal keywords:** pick 3 to 10 at upload.

## 1. Formatting & Structure

> **Live IEEE Access check, 2026-10-14** (ieeeaccess.ieee.org submission guidelines, APC and preparing-your-article pages):
> - **[BLOCKER] Template:** the IEEE Access template is *required at initial submission* ("using a required IEEE Access template"). Upload both a LaTeX/Word source and a PDF, 40 MB max. Plain `[journal]{IEEEtran}` is not enough. Port to `ieeeaccess.cls` before upload.
> - **[BLOCKER] Length:** "Authors who have a special reason to submit a paper over 20 pages must first make a **pre-submission inquiry** to seek permission from the EIC." Permission comes *before* submission, so a cover-letter request alone is not enough. No contact address is published; ask through the Author Portal or the editorial office.
> - **APC:** $2,160 with no page limit and no over-length charge. IEEE members get 5% off; IEEE Society members get 20% off; discounts do not combine.
> - **AI disclosure** wording is unchanged and still belongs in the Acknowledgments.
> - **Keywords:** select 3 to 10 in the portal. The paper's 13 Index Terms are separate from that selection.
> - **Code:** IEEE endorses Code Ocean for code, and it can be added at submission, revision or after acceptance. A ZIP supplement for review is also acceptable.
> - **Review model:** single-anonymized, so no anonymization is needed. Portal: https://ieee.atyponrex.com/journal/ieee-access
- [x] **[BLOCKER]** `\documentclass[journal]{IEEEtran}`
- [ ] **[ACTION — page length]** **DECIDED 2026-10-14: keep full length (Option A); Sir Faisal: "don't decrease the pages." Request EIC pre-approval in the cover letter; do not move material to supplementary.** **32 pages.** IEEE Access guidance as cached on 2026-10-10: stay under ~20 pages for a standard review, and anything over 20 needs **Editor-in-Chief pre-approval**. Length was explicitly accepted by the author ("it doesn't matter how lengthy it is"). Before upload, either (a) request EIC pre-approval, or (b) move parts of Section V (e.g., V.E per-agent paragraphs, V.K formal bounds, Table XII roadmap) to supplementary material. Also check the live page for any over-length charges; this was not verified.
- [x] References on unlimited pages
- [x] Two-column layout verified on the rendered PDF (Check 19). Page 1 template, Fig. 2, Fig. 3 and the bibliography pages were inspected. No column overflow (`xurl` added). The only overfull box is 0.7pt.
- [x] No global font or margin reduction
- [x] `\IEEEPARstart` on the first Introduction paragraph

## 2. Content — Required Sections
- [x] **[BLOCKER]** Abstract 250 words (≤250; recounted 2026-10-14). No citations. AI, HACOF and HITL are expanded. It ends on significance and carries the author's core HACOF statement.
- [x] **[BLOCKER]** Index Terms: 13 terms (the author's 10 plus 3 retained)
- [x] Contributions list: HACOF first, then the pillars, the major-power map and the Pakistan case
- [x] Variant D structure: Background → Pillars (IV) → HACOF (V) → Case (VI) → Evaluation protocol (VII, **no results reported, stated explicitly**) → Limitations (VIII) → Conclusion (IX)
- [x] **Coverage:** 49 of 49 items from the author's HACOF source text are present, per the Editor's coverage audit. The one partial item (plane contents) has since been fixed.
- [x] Three author-required distinctions explicit in V.B and the Introduction: safety vs. policing, detection vs. prevention, oversight vs. surveillance
- [x] **[BLOCKER]** Acknowledgments: no external funding, plus the AI-disclosure statement (Sections I–IX)

## 3. Citations
- [x] **[BLOCKER]** IEEE `[N]` format. 79 entries (79 `\bibitem`s in main.bbl, recounted 2026-10-14), 0 orphans, 0 missing (checked by script against `main.aux`).
- [x] **[BLOCKER]** No placeholders: no `NEWCITE`, `[PAK-…]` or `[HACOF-EXPANSION]`
- [x] **[BLOCKER]** No `and others` / `et al.` authors. The CAC entry now lists all 7 issuing agencies.
- [x] Title case protected in all bib titles (acronyms render correctly)
- [x] **Novelty positioned honestly.** No "novel/first/central innovation" claims. Prior art is cited: guard agents (GuardAgent, ShieldAgent), Sentinel Agents, AgentSpec, GaaS, MI9, the Swiss-cheese architecture, Koch 2026, IMDA, Simplex/shielding, zero trust and the NIST AI RMF.
- [x] **Name check:** no prior use of "HACOF" or the full name in AI or governance. The only hit is a food-chemistry paper. Trademark databases were not searched.
- [ ] **Recommended before upload:**
  - Open the paywalled Sha 2001 (Simplex) on IEEE Xplore to confirm the paraphrase; it was checked via secondary descriptions.
  - Optionally cite Kish (1965) for the design-effect form in V.K. No primary source was reachable online, so the formula is currently labelled "an illustrative approximation" without citation.
- [ ] **Live link-check** of all URLs immediately before upload. Most fragile: the Pakistan MoITT policy PDF, the Chambers guide, the OMB memos (not rescinded as of the Sep 2026 listing), the IMDA PDF.

## 4. Visual Design (Rule Q)
- [x] Colored title, purple italic author line, abstract box, keywords box (kept unsplit with `nobreak=true`)
- [x] Proposition box (Intro), Foundational Principles box (V.C), Key Principle box (V.I), Key Finding box (VI)
- [x] Colored section and subsection headings. Tables use `[!t]` floats; supervisors table is full-width.
- [ ] Optional: the title is 22 words over 4 lines. IEEE Access favors shorter titles (author's call).

## 5. Figures and Tables
- [x] 4 TikZ figures, 0 placeholders. Every figure and table is referenced in the text.
- [x] Fig. 2, Table VI (supervisors) and the text agree: Agents A, D, E in-path; B, C, F, G out-of-path

## 6. Ethics & Compliance
- [x] **[BLOCKER]** AI-use disclosure in Acknowledgments (IEEE Access policy, verified 2026-10-10)
- [x] No human subjects or datasets
- [x] Design defaults (appeal deadlines, the worked authorization profile) are labelled as proposed or hypothetical, not empirical

## 7. Build
- [x] pdflatex → bibtex → pdflatex ×2: 0 errors, 0 undefined citations/references, 0 `??`
- [x] `paper.md` regenerated from `main.tex` + `main.bbl` (citation numbering is one-way from main.tex per Rule H)

## 8. Still Outstanding (Human Action Items)
0. **Supplementary material:** `HACOF-supplementary.zip` built 2026-10-14 (10 files, 15 KB, no `__pycache__`; selftest 9/9 pass). Upload it with the manuscript. Originally: upload `prototype/` (hacof_sim.py, make_tex.py, README.md, results/) as a supplementary ZIP, or host it at a public repository and cite the URL in VII.D.
1. **Page-length decision:** EIC pre-approval or move material to supplementary (see §1).
2. **Cover letter:** update to the HACOF framing. Template:
   ```
   Dear Editor-in-Chief,
   We submit "Law, Policy, and Governance of the AI Ecosystem for Human Control:
   The Human-Centric AI Governance and Continuous Oversight Framework (HACOF)"
   for consideration in IEEE Access. The paper proposes HACOF, a policy-oriented
   reference model that places runtime enforcement, independent supervisory AI
   agents, real-time monitoring, automated containment and accountable human
   governance under legal authority, adds a governance regime for the supervisors
   themselves, and maps the framework onto four pillars of state governance
   capacity, with Pakistan's 2025 National AI Policy as a case study. The
   manuscript is 32 pages; we request pre-approval for its length. It has not
   been submitted elsewhere.
   Sincerely, Muhammad Faisal Laiq
   ```
3. Final live link-check; Simplex/Kish primary-source confirmation (see §3).
4. Portal: account, subject areas (AI governance / technology policy / AI safety), ORCID linkage.

Portal: https://ieee.atyponrex.com/journal/ieee-access (verified live 2026-10-10)
