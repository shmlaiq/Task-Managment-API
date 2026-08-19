# Pillar 4 — Humanized Language Tone

Writing that sounds like an expert wrote it rather than a language model. Apply from
the first sentence. This pillar overlaps with Pillar 3 (anti-AI detection) — the
difference is that Pillar 3 focuses on statistical detection signals; Pillar 4 focuses
on intellectual authenticity.

---

## What Humanized Tone Means

| Authentic Expert Writing | Template / AI Tone |
|---|---|
| Names the specific obstacle: "The 12.7% variance at N=500 broke our assumption" | Hedges vaguely: "Limitations may affect results in some cases" |
| Takes a position: "We argue this trade-off favors latency over accuracy for mobile" | Avoids commitment: "Both approaches have merits depending on the use case" |
| Uses precise domain vocabulary: "Bayesian regret bound", "HITL escalation rate" | Uses generic vocabulary: "good performance", "improved results" |
| Structures around insights, not sections: "The surprising result is…" | Structures around headings: "This section presents the methodology" |
| Shows reasoning under uncertainty: "We chose α=0.6 because pilot runs at 0.3 produced…" | Asserts without trace: "We set α=0.6 for optimal performance" |

---

## Six Techniques for Humanized Tone

### Technique 1 — Specific Vocabulary Over Generic

Replace general technical words with the most precise term in the domain.

| Generic | Domain-Specific Replacement |
|---|---|
| "better performance" | "7.3% lower P99 latency at 2,000 concurrent requests" |
| "handles errors" | "falls back to HITL escalation within 400 ms" |
| "large dataset" | "1.2M token context traces from 847 production sessions" |
| "state-of-the-art" | [forbidden — always cite the method name + its metric] |

**Rule:** Every adjective (fast, robust, efficient, accurate) must be replaced with a
number, a method name, or a structural property. Bare adjectives without evidence
are Pillar 3 (AI detection) AND Pillar 4 (authenticity) failures.

---

### Technique 2 — Take a Position

AI-generated prose avoids commitment. Expert prose makes claims and defends them.

**Pattern to apply once per major section:**
```
We argue / We claim / We find / Our analysis shows
[one-sentence claim]
because [evidence or reasoning].
```

**Bad (neutral, non-committal):**
> "The choice between federation and centralization presents trade-offs. Researchers
> may select the approach that best fits their requirements."

**Good (position-taking):**
> "We argue federation is the wrong default for latency-critical pipelines: the two
> additional network hops add 38–65 ms under congestion, exceeding the 50 ms budget
> of real-time inference applications."

---

### Technique 3 — Name Failures and Limitations Explicitly

A paper without a credible failure story reads as promotional. Name:
- Conditions under which the approach breaks
- Cases that were excluded from evaluation and why
- Metrics that declined while other metrics improved
- Implementation difficulties that caused design compromises

**Placement:** At least one failure/limitation paragraph in:
- Discussion section (mandatory)
- Results section where applicable (when a result was unexpected or negative)

**Pattern:**
```
[Method] fails (or degrades) when [condition].
We observed [specific magnitude] degradation at [threshold].
No mitigation was attempted because [reason].
```

---

### Technique 4 — Vary Sentence Rhythm (Burstiness)

This also serves Pillar 3. For Pillar 4 framing: natural expert writing reflects
cognitive rhythm — short sentences punctuate; long sentences build.

**Check at end of every section:**
1. Count sentences < 8 words and > 28 words.
2. If all sentences are 15–22 words → AI-uniform rhythm → restructure.
3. Target: ≥ 2 sentences under 8 words AND ≥ 2 sentences over 28 words per section.

---

### Technique 5 — Show Reasoning, Not Just Conclusions

Expert prose shows the path. AI prose shows only the destination.

**Bad:**
> "We selected transformer-based encoding for its superior context retention."

**Good:**
> "We evaluated BiLSTM, GRU, and transformer-based encoding across 12 session
> length buckets. At lengths < 512 tokens, all three performed within 1.2% of each
> other. At 2,048+ tokens, transformer encoding held 94.3% recall while GRU dropped
> to 78.1% — that gap drove the architecture choice."

---

### Technique 6 — No Filler Transitions or Meta-Commentary

These phrases describe the paper's structure rather than advancing the argument.
They are both Pillar 3 and Pillar 4 failures.

| Filler Phrase | Human Alternative |
|---|---|
| "In this section, we describe…" | [Just describe it — no meta-announcement] |
| "As mentioned earlier," | [Re-state the fact in one clause if needed] |
| "It is worth noting that" | [Start the sentence with the observation itself] |
| "This paper makes the following contributions:" | "The contributions of this paper are:" followed by a precise list |
| "Overall, the results demonstrate that" | [State the actual conclusion] |
| "Future work will explore" | [State what trigger or threshold would make this the next priority] |

---

## Tone Self-Assessment (Run Before Delivery)

For each major section (Abstract, Introduction, Methodology, Results, Discussion,
Conclusion), ask:

1. **Expert vocabulary test**: Does every adjective have a number, method name, or
   structural qualifier behind it? If not — add specificity.

2. **Position test**: Is there at least one sentence that takes a clear side, argues
   for a design choice, or states a finding as a claim? If not — add a position statement.

3. **Failure test**: Is there at least one limitation, exception, or degradation case
   named with a concrete condition? If only in the Discussion — acceptable. If nowhere
   — add one.

4. **Rhythm test**: Are there sentences both < 8 words and > 28 words in this section?
   If all sentences cluster in the 14–20 word range — restructure.

5. **Filler test**: Grep for meta-commentary patterns:
   ```bash
   grep -in "in this section\|as mentioned\|worth noting\|it should be noted\|this paper presents\|overall.*results.*demonstrate" paper.md
   # Each match = rewrite candidate
   ```

---

## Relation to Other Pillars

| Pillar | Overlap with Pillar 4 |
|---|---|
| Pillar 3 (Anti-AI) | Burstiness, filler phrases, specificity — same technical fixes; Pillar 4 frames them as *authenticity*, Pillar 3 frames them as *detector evasion* |
| Pillar 1 (No Hallucinations) | "Named failures" (Technique 3) must cite real experimental results, not fabricated ones |
| Pillar 5 (Fact Integrity) | "Show reasoning" (Technique 5) must cite every external data point used |

The quickest path to Pillar 4 compliance is fully applying the anti-ai-detection.md
transformation protocol (Pillar 3), then adding one position statement and one named
failure per section that were not already required by Pillar 3.
