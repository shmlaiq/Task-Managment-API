# Rebuttal Writing Guide

## What a Rebuttal Is

A rebuttal (also called author response) is a 500–1000 word response to peer review
comments submitted during the review period of a conference or journal. It is your
only chance to correct factual errors and address reviewer concerns before the final
decision.

**What a rebuttal can do:**
- Correct factual misunderstandings about your method
- Provide missing experimental results (if you can run them in time)
- Clarify unclear writing
- Point out errors in the reviewer's reasoning (carefully)

**What a rebuttal cannot do:**
- Rewrite your paper (reviewers read the original, not the rebuttal)
- Change a weak paper into a strong one
- Argue that the reviewer is wrong about their taste or standards

---

## Rebuttal Structure (500 words max for most venues)

```
[Opening — 1 sentence]
We thank the reviewers for their careful reading and constructive comments.

[Per-reviewer responses, ordered by reviewer ID]

## Response to Reviewer 1

**R1.1 [Concern title — paraphrase the reviewer's point]**
[Your response — 2–4 sentences]

**R1.2 [Next concern]**
[Response]

## Response to Reviewer 2
...

[Optional closing — 1 sentence if space allows]
We will incorporate all suggestions into the final revision.
```

---

## Classify Each Comment Before Responding

Before writing, classify every reviewer comment into one of four types:

| Type | Description | How to Respond |
|---|---|---|
| **Factual error** | Reviewer misread your method or misunderstood a number | Politely correct with exact quote from paper + section number |
| **Missing experiment** | Reviewer wants an additional ablation, baseline, or analysis | Run it if possible; describe the result; commit to including it |
| **Unclear writing** | Reviewer was confused by your explanation | Clarify; thank them; commit to revising that section |
| **Opinion / taste** | Reviewer thinks your problem is not important enough | Acknowledge perspective; reinforce motivation with citations |

---

## Response Templates

### Type 1: Factual Error (reviewer misread the paper)

```
**R1.2 [Claim about X]**
We respectfully note that our paper reports Y (not X as the reviewer states).
Specifically, Table 2, row 3, column "Accuracy" shows Y = 83.5%.
The reviewer may be referring to our baseline result of 79.1%, which appears in
the same table in row 1. We will clarify this distinction more prominently in
the revised manuscript.
```

**Rules:**
- Never say "the reviewer is wrong" — say "we respectfully note..."
- Always give the section number or table number
- Always commit to clarifying in revision

### Type 2: Missing Experiment (reviewer wants more results)

```
**R2.1 [Request for ablation on component X]**
We appreciate this suggestion. We ran the requested ablation over the review period:

| Config | Accuracy | F1 |
|--------|----------|-----|
| Full model | 83.5% | 81.2 |
| w/o Component X | 79.8% | 77.4 |
| w/o Component Y | 81.1% | 79.0 |

The results confirm that Component X contributes +3.7% accuracy, validating
our design choice. We will include this ablation in Table 3 of the revised paper.
```

**Rules:**
- If you ran it: give the exact numbers in a mini-table
- If you cannot run it: explain why (compute cost, dataset access) and offer a proxy
- Always commit to including it in revision

### Type 3: Unclear Writing

```
**R3.1 [Confusion about the training procedure]**
We agree that Section III.B was unclear. To clarify: the model is first pre-trained
on Dataset A (Stage 1, 50 epochs), then fine-tuned on Dataset B (Stage 2, 10 epochs).
The reviewer's interpretation (that both stages use Dataset B) is incorrect.
We will rewrite Section III.B with an explicit two-stage training diagram (Fig. 2
will be updated to show both stages separately).
```

### Type 4: Scope / Importance Disagreement

```
**R1.1 [Concern that the problem setting is too narrow]**
We appreciate the reviewer's perspective. The [specific setting] addressed in this
paper affects [specific real-world scenario] — for example, [concrete instance] [N].
While broader settings are valuable research directions, addressing them requires
[specific capability] not yet available, as noted in our limitations (Section VI.B).
We will add [citation] to strengthen the motivation in Section I.
```

---

## Tone Rules (Critical)

| Do | Don't |
|---|---|
| "We respectfully note..." | "The reviewer is incorrect..." |
| "We agree that Section X was unclear" | "We already stated this clearly in Section X" |
| "Thank you for this suggestion" | Ignoring a comment entirely |
| Be specific with numbers and section refs | Vague: "As described in our paper..." |
| Acknowledge limitations honestly | Over-promise: "We will fix all issues" |
| Match reviewer's formality level | Overly casual or defensive |

---

## Rebuttal Strategy

### Prioritize by impact on decision:

1. **Correctional responses first** — fix factual errors; these change reviewer scores
2. **Missing experiments second** — if you can run them, they change scores
3. **Clarifications third** — useful but rarely change scores
4. **Acknowledgments last** — "we will revise X" takes no space; put these at the end

### When a reviewer is clearly wrong:

Correct them once, clearly, with evidence. Do not argue further. Reviewers who feel
attacked dig in. Your goal is to give the Area Chair/Editor enough information to
recognize the error — not to win a debate.

### When a reviewer raises a valid point you missed:

Acknowledge it honestly. "The reviewer raises a valid concern. We investigated and
found [result]." This builds credibility and often recovers a low score.

### What to skip:

Do not respond to every minor comment. Prioritize comments that affected the reviewer's
recommendation score. If Reviewer 2 has 8 comments but only 2 seem to have driven
the "reject" recommendation, focus on those 2 in depth.

---

## Venue-Specific Rebuttal Limits

| Venue | Word Limit | Format |
|---|---|---|
| IEEE CVPR / ICCV | 500 words | Plain text or Markdown |
| NeurIPS | 500 words | LaTeX allowed |
| ICML | 500 words | Plain text |
| IEEE Transactions | 2 pages | PDF (formal letter format) |
| IEEE Letters | 1 page | PDF |
| AAAI | 200 words | Plain text |

Always check the current year's author instructions — limits change.

---

## Pre-Submission Rebuttal Checklist

- [ ] Every major concern addressed (nothing ignored)
- [ ] Factual errors corrected with exact section/table references
- [ ] New experimental results provided as mini-tables (not prose)
- [ ] Word count within venue limit
- [ ] Tone: respectful throughout — no defensive or confrontational phrasing
- [ ] Every response ends with a commitment to revise ("We will add/clarify/include...")
- [ ] Reviewers addressed by ID (R1, R2, R3) — not "Reviewer A" or "the first reviewer"
- [ ] No new claims introduced that were not in the original paper
