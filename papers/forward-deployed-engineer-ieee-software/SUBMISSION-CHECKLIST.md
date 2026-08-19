# Submission Checklist — "Forward Deployed Engineer (FDE) in the AI Ecosystem" (IEEE Software)

Author: Muhammad Faisal Laiq (no institutional affiliation) — shmlaiq@gmail.com — ORCID 0009-0007-5779-9836
Venue: IEEE Software (practitioner magazine feature article)

## 1. Format Requirements (verified against current CFP, computer.org/digital-library/magazines/so/cfp-ieee-software)
- [x] Article ≤4,200 words including 250 words per figure/table — delivered ≈2,130 total (1,519 body + 111 insights box + 128 abstract + 250 figure + 250 table charge, well under cap)
- [x] Abstract ≤150 words — delivered 128
- [x] ≤15 references — delivered 10
- [x] "Three Actionable Insights" bullet box present
- [x] Uses IEEE Software's IEEEtran-based template (same journal-class scaffold as the companion IEEE Access paper — reused, not rebuilt)
- [ ] **Author photo — required by the CFP, not something I can produce.** You'll need to supply a headshot before submission.

## 2. What Changed From the IEEE Access Version
This is a condensation, not a copy — cut from ~6,600 words to ~1,750, dropped 7 of 17 references (kept only the load-bearing ones), removed the formal Related Work literature review and the theoretical/combinatorics subsection (not appropriate for a practitioner magazine), and rewrote toward a problem/insight-first structure instead of a thesis-defense structure. Both versions live in `papers/` as separate directories — this one does not replace the IEEE Access draft.

## 3. Fact-Checker Pass (Condensation-Specific)
A second independent Fact-Checker audit ran specifically to catch compression errors — a real risk when cutting a paper this hard, since a hedge or nuance can get lost in the trim even when the underlying citation is sound. It found and I fixed two issues before delivery:
- **Fixed (Major):** the Scale AI case-study hedge ("this analysis holds it with less confidence than the other three") was dropped during condensation, leaving an unhedged claim on weaker evidence than the sentences around it. Restored.
- **Fixed (Minor):** an unsupported "within the year" timeframe had been added to the OpenAI team-growth stat during rewriting; the source doesn't state that timeframe. Removed.

Everything else — citation numbering, the core stats (22/311, Delta codename, 25% travel, <15% real-time integration), and word/reference limits — checked out clean on re-audit.

## 4. Before You Submit
1. **Query the editor first.** IEEE Software's CFP lists Editor-in-Chief Sigrid Eldh (sigrid.eldh@ieee.org) as a contact for discussing fit before submitting — for a magazine venue (vs. a blind-reviewed research journal), a short pitch email is normal practice and can save a review cycle if the piece isn't what they're looking for right now.
2. **Supply an author photo.**
3. Submission portal: https://ieee.atyponrex.com/journal/sw-cs — reconfirm current requirements there, since magazine CFPs can change between when this was drafted and when you submit.
4. Unlike the IEEE Access version, this is a single-author opinion/practice piece for a magazine audience, not a peer-reviewed research claim — the tone is deliberately more direct and less hedged throughout the body text than the academic version. The Limitations section still carries the same honest caveats (descriptive not causal, no primary survey data, source bias) in compressed form.

## 5. Companion Version
The full academic treatment — formal taxonomy justification, complete case analysis, 5 named limitations, 17 references — remains available at `papers/forward-deployed-engineer-ai-ecosystem/` if a reviewer or reader wants the deeper version.
