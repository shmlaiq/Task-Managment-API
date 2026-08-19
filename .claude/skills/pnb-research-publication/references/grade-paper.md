# /grade-paper Command

Grade any paper (`paper.md` + `references.bib`) on a 100-point scale and
**automatically fix every warning found** before delivering the report.

---

## Execution Protocol

```
1. Run bash audit (all 17 commands) → collect raw findings
2. Score each category (0–100) using rubric below
3. Identify BLOCKERS (must stop delivery) and WARNINGS (fixable)
4. Auto-fix all warnings in paper.md (banned phrases, missing failure cases, etc.)
5. Re-run bash audit to confirm fixes → update scores
6. Deliver final grading report
```

---

## Grading Rubric (100 points total)

| # | Category | Weight | How to Score |
|---|---|---|---|
| 1 | **Hallucination Check** | 20% | Start 100; deduct per trigger table below |
| 2 | **Plagiarism Compliance** | 15% | 100 if read-close-write evident + no echo patterns; −10 per flagged pattern |
| 3 | **Anti-AI / Human Tone** | 15% | Run banned phrase grep; check burstiness; GPTZero result if available |
| 4 | **Fact & Citation Integrity** | 15% | Verify author names vs BibTeX; check DOIs; −5 per mismatch |
| 5 | **Technical Contribution** | 20% | Novelty + depth + correctness of proposed idea (manual judgment) |
| 6 | **Writing Quality & Clarity** | 10% | Structure, abstract quality, section completeness (manual judgment) |
| 7 | **Experimental Rigor** | 5% | Baselines named+cited, metrics defined, ablation present or justified N/A |

**Hallucination deduction triggers (Category 1):**

| Trigger | Penalty |
|---|---|
| Any `%` without `[N]` citation | −5 per instance |
| Unverified / placeholder arXiv ID | −10 per instance |
| `[CITE NEEDED]` / `[Unverified]` remaining | −15 per instance (delivery blocker) |
| Empirical claim stated without evidence | −8 per instance |
| Wrong author name on a citation | −5 per instance |
| Mathematical bound cited to wrong primary source (Rule L) | −8 per instance |
| `and others` in any BibTeX entry (Rule M) | −5 per entry |
| Derived estimate misattributed to a source (Rule N) | −5 per instance |
| Near-verbatim vendor documentation (Rule P) | −8 per paragraph |
| Distinctive abstract phrase echoed verbatim in body (Rule O) | −3 per phrase |

---

## Grade Scale

| Score | Grade |
|---|---|
| 95–100 | A+ |
| 90–94 | A |
| 85–89 | A- |
| 80–84 | B+ |
| 75–79 | B |
| Below 75 | Needs revision |

---

## Auto-Fix Protocol (run after scoring, before final report)

When warnings are found, fix them directly in `paper.md`:

| Warning Type | Auto-Fix Action |
|---|---|
| Banned phrase found | Replace with direct, specific alternative |
| Sentence burstiness violation | Split or merge sentences to vary length |
| `%` from prior work without `[N]` | Add `[N]` citation — every external % needs one |
| `%` from mathematical derivation | Replace with a ratio or multiplier (e.g., "25× reduction") — derivation-based percentages must not appear as bare `NN%` |
| Missing failure case in Discussion | Add a concrete limitation paragraph |
| Author name mismatch | Correct inline name to match BibTeX first author |
| Vague claim without concrete detail | Add specific technical detail or example |
| Formula parameter with no default | Add default value + recommended range per workload type (e.g., α = 0.6; low α ≈ 0.3 for planning, high α ≈ 0.8 for conversation) |
| Source phrasing too close to original | Rewrite with different sentence structure AND different vocabulary — synonym substitution is not enough; the new sentence must be unrecognisable from the source without the citation |
| Mechanism with incomplete escalation path | Specify the full sequence: trigger condition → step 1 → step 2 → fallback (HITL or human review) — no mechanism may end with "not fully specified" |
| Conceptual paper missing Theoretical Analysis | Add a §Theoretical Analysis subsection to §V with: (1) complexity analysis of core algorithm, (2) formal property proof or dominance argument for the proposed approach vs. baseline, (3) at least one quantitative bound derived from the architecture's parameters |

After auto-fixing, re-run the bash audit and update category scores accordingly.

---

## Report Format

```
PAPER GRADING REPORT
════════════════════════════════════════
Paper:  [Title]
Author: [Name]
Date:   [Date]

CATEGORY SCORES
───────────────────────────────────────
1. Hallucination Check     (20%)   NN/100  → NN.N
2. Plagiarism Compliance   (15%)   NN/100  → NN.N
3. Anti-AI / Human Tone    (15%)   NN/100  → NN.N
4. Fact & Citation Integrity(15%)  NN/100  → NN.N
5. Technical Contribution  (20%)   NN/100  → NN.N
6. Writing Quality         (10%)   NN/100  → NN.N
7. Experimental Rigor       (5%)   NN/100  → NN.N

TOTAL SCORE:  NN.N / 100
GRADE:        [A+ / A / A- / B+ / B / Needs revision]
───────────────────────────────────────
BLOCKERS (must fix before submission):
  [list or "✅ None found"]

WARNINGS:
  ⚠ [section/category]: [issue description]
  ⚠ [section/category]: [issue description]

FIXES APPLIED:
  ✔ [what was changed and where]
```
