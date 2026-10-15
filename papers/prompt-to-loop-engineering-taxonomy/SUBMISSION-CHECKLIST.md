# Submission Checklist — "From Prompt Engineering to Loop Engineering: A Five-Layer Taxonomy for Evaluating AI Systems Engineering Practice"

Target venue: IEEE Access (assumed at intake; confirm with Sir Faisal before submission — this checklist was not re-verified against a live venue re-check).

## Author Block
- [x] Author confirmed: Muhammad Faisal Laiq, shmlaiq@gmail.com, ORCID 0009-0007-5779-9836
- [x] No institutional affiliation — independent researcher. Author block uses the
      no-affiliation single-line pattern (`\IEEEauthorblockN{Name \qquad Email \qquad ORCID}`,
      no `\IEEEauthorblockA`) in main.tex.

## Citations — Complete
- [x] **2026-08-21/22 deep-research expansion:** all 5 Related Work subsections
      (II-A through II-E) substantially deepened per Sir Faisal's explicit request for
      more technical-depth citations. 3 parallel Literature Agent forks produced
      dossiers (`LITERATURE-DOSSIER-PROMPT-CONTEXT.md`, `-HARNESS-AGENT.md`,
      `-LOOP.md`) totaling 47 candidate citations; 45 were integrated (2 deduped —
      Ouyang/InstructGPT and Wang/Self-Consistency each already covered one layer and
      were reused via `\cite{}` in the second, not re-added as duplicate `.bib` keys).
      References grew from 27 to **72 total**, all verified via direct WebFetch of
      arXiv/publisher abstract pages by the Literature Agent forks, cross-checked for
      consistency at integration time.
- [x] `references.bib` built; `pdflatex → bibtex → pdflatex → pdflatex` compiles clean;
      citation numbering in `paper.md` transcribed from the compiled `main.bbl`
      order-of-first-appearance (Rule H) via a safe two-pass old→temp-tag→new Python
      remap, not hand-incremented.
- [x] Rule M: `grep "and others" references.bib` → zero hits (all 72 entries, including
      the 45 new ones, carry complete author lists).
- [x] Rule G: all 72 `.bib` entries are cited in `main.tex`; zero orphans in either
      direction (verified via `main.aux` cross-check, re-run 2026-08-22 post-expansion).
- [x] One citation (Lin et al. 2026, "Agentic Harness Engineering") was independently
      re-verified by the Lead via direct WebFetch to arxiv.org/abs/2604.25850 before
      trusting the sub-agent's report, given how load-bearing it was for the paper's
      framing of "harness engineering" as an emerging vs. established term.
- [x] Check 3 (et al. name spot-check) re-run post-expansion on all 4 "et al." mentions
      in prose (Lin, Huang, Kamoi, Christiano) — each matches its `references.bib`
      author field exactly.

## Figures — Complete
- [x] Fig. 1: five-layer maturity-stack diagram (TikZ, color-coded, "increasing
      autonomy & state" side annotation) in `main.tex`.
- [x] Fig. 2: evaluation-framework mapping diagram (TikZ, `figure*`, full-width,
      same color coding as Fig. 1) in `main.tex`.
- [x] Table I: per-layer diagnostic metrics table (`booktabs`).
- [x] Zero `\figplaceholder` calls anywhere in the delivered draft (Rule K, verified by
      grep).

## Visual Design (Rule Q) — Complete, one real bug found and fixed post-delivery
- [x] Colored title (`\textcolor{darkblue}`), slateblue italic author line.
- [x] Colored Abstract and Index Terms boxes (mdframed, darkblue border/fill).
- [x] **Known-good bug fix applied:** the first delivered version used
      `\IEEEtitleabstractindextext` to hold the abstract/keywords, following an
      incorrect assumption that this was the standard journal-mode pattern — it
      silently dropped all its content on compile (confirmed by visually reading the
      rendered PDF, not caught by any text-based grep check). Replaced with the
      standard `\begin{abstract}`/`\begin{IEEEkeywords}` environments plus a
      `\makeatletter` override of IEEEtran's hardcoded label, per
      `references/visual-design.md`'s documented tested pattern. Re-verified by
      reading the recompiled PDF directly.
- [x] A duplicated Acknowledgments/AI-disclosure paragraph (introduced during an
      earlier merge) was also found by the same visual read-through and fixed in both
      `main.tex` and `paper.md`.
- [x] **Lesson:** grep-based audit checks on `paper.md` cannot catch LaTeX-macro
      rendering failures or duplication bugs that only exist in `main.tex`'s compiled
      output — reading the actual rendered PDF is a required step, not optional, before
      calling a LaTeX-heavy delivery done.

## Structure / Content
- [x] Contribution type stated explicitly and early (Introduction): taxonomy/
      perspective paper with grounded case studies, not a controlled experiment.
- [x] Explicit 5-item contribution list (Introduction), including the Section VIII
      traditional-antecedents mapping added after initial delivery per user request.
- [x] Limitations section states all required framings: illustrative not experimental,
      author framing-bias risk, non-sharp layer boundaries, unvalidated metrics.
- [x] Discussion names the under-diagnosed loop-layer failure mode plainly.
- [x] Future work in Conclusion ordered by urgency, not symmetry/count (Rule F).
- [x] Acknowledgments section present: no external funding, IEEE generative-AI
      disclosure statement (tool described as "an AI-LLM" since 2026-10-15; scope of AI assistance, human
      verification and accountability statement). Live IEEE Access AI-disclosure
      policy text re-verified via WebFetch against `ieeeaccess.ieee.org/authors/
      submission-guidelines/` at delivery time — matched cached reference exactly.
- [x] Section VIII ("Traditional Programming Antecedents") added post-initial-delivery
      per explicit user request, mapping each layer to a pre-LLM SE discipline (Design
      by Contract, twelve-factor config, containerization, actor model, continuous
      delivery) — inserted as the second-to-last section specifically to avoid
      renumbering earlier hardcoded `Section~N` cross-references throughout the body.
- [x] Case studies (Section V) verified twice against the actual live source files
      (docker-deployment SKILL.md, global CLAUDE.md/Viper charter,
      pnb-research-publication SKILL.md) — once by the Writing Agent at draft time,
      once independently by the Fact-Checker Agent, which caught and the Lead fixed
      one internal inconsistency ("sixteen" vs. "seventeen" non-negotiable principles
      — sixteen is correct).
- [x] No fabricated statistics or citation numbers anywhere in the draft.

## Anti-AI-Detection — Complete, scanner-verified (not just proxy checks)
- [x] Ran the skill's documented free/offline scanner (`Hello-SimpleAI/chatgpt-detector-roberta`
      via `transformers`, no API key) against every section, chunked to the model's
      ~380-word window. Result: 28/28 chunks scored effectively 0% AI probability,
      target was <20% — real measured result, not an estimate. Re-run after the
      deep-research expansion against the full 40-chunk expanded text: 40/40 chunks,
      0% AI probability, 0 flagged.
- [x] Related Work Failure Mode 1 (uniform sentence length) and Failure Mode 2
      (descriptive catalogue, no evaluative positions) — both explicitly checked
      per-subsection (not just aggregate); found 0 short (<12-word) sentences and 2
      of 5 subsections with zero evaluative language on first pass; fixed by adding
      one short critical sentence pair to each of the 5 subsections.
- [x] Conclusion paragraph-uniformity check (skill's specific rule: at least one
      paragraph <40 words/1-2 sentences, at least one >100 words/5+ sentences) —
      found both original paragraphs were 3-sentence/~130-145-word (uniform);
      restructured into a 27-word 1-sentence paragraph and a 166-word 5-sentence
      paragraph.
- [x] Rule D (conceptual paper missing Theoretical Analysis) — added a Theoretical
      Analysis subsection to Section IV: O(L) complexity bound for layer-sequential
      diagnosis, an exchange-argument optimality proof for cost/probability-ratio
      layer ordering, and a derived quantitative cost bound (Eq. 1) — self-contained
      design/derivation content, no fabricated data, no citation needed per
      anti-hallucination guidance on original design contributions.

## Compilation
- [x] `pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex`
      compiles with zero errors, zero undefined references, zero `??` cross-reference
      failures. Current output: **14 pages** (grew from 9 pages after the deep-research
      Related Work expansion). Re-verified 2026-08-22.
- [x] `paper.md` and `main.tex` verified in sync after every content/citation change
      (Rule H) — spot-checked repeatedly across the whole editing session, and again
      post-expansion (Abstract exact-text diff, Conclusion opening sentence, and the
      Huang/Kamoi Related Work paragraph all confirmed identical content and matching
      `[N]` numbers in both files).
- [x] Check 19 (compiled-PDF visual verification) run twice post-expansion: full
      14-page PDF read confirms title/author colors, Abstract/Index Terms boxes,
      all `\textcolor{darkblue}` section headings, Fig. 1, Table I, Fig. 2, Equation 1,
      all three Key Finding callout boxes (red/orange/blue), and the References list
      (72 entries, IEEE format, full author lists) all render correctly with no
      duplication and nothing dropped.

## Outstanding Before Actual Submission (author action items, not something an agent can complete)
- [ ] **Re-verify the IEEE Access venue choice and current CFP/page-limit/reference-cap
      numbers live** immediately before submitting — this checklist's venue assumption
      was set at intake and not independently re-confirmed against IEEE Access's
      *current* guidelines on this pass (only the AI-disclosure policy text specifically
      was live-checked).
- [ ] Decide whether to keep "independent researcher" as the permanent author framing
      or add an institutional affiliation, and update the author block accordingly if so.
- [ ] Final proofread by the author — an LLM-assisted paper about LLM-era engineering
      failure modes should get the same independent human read any paper does before
      submission.
- [ ] Confirm iThenticate/plagiarism-scan and any *institutional* GPTZero-style scan
      IEEE Access itself requires at formal submission — this session ran the skill's
      own free/offline `Hello-SimpleAI/chatgpt-detector-roberta` scanner (0% AI
      probability, 40/40 chunks) as a pre-delivery proxy check, not a substitute for
      whatever scan IEEE Access's submission portal runs independently.

## 2026-10-15 Update
- [x] **Author biography + photo added:** canonical bio from `papers/AUTHOR-BIO.md`, photo `author.jpg`. Email stays on page 1 only.
- [x] **AI-use disclosure reworded:** "Claude (Anthropic)" replaced with "an AI-LLM" in main.tex and paper.md, per the author's standing rule. Scope, accountability and no-AI-author statements unchanged.
- [ ] **AI-disclosure compliance risk (author's choice):** the disclosure names the tool only as "an AI-LLM". IEEE says "the AI system used shall be identified", so an editor may ask for the system name.
- [x] Rebuilt: 0 errors, 14 pages.
