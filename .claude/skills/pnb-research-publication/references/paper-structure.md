# IEEE Paper Structure — Section-by-Section Guide

## 1. Title

**Requirements:**
- Specific and informative — describes the exact contribution
- No puns, no vague terms ("A Novel Approach to...")
- 10–15 words ideal; avoid over-long titles
- Include key terms that match your venue's scope

**Good titles:**
- "Attention Is All You Need"
- "Deep Residual Learning for Image Recognition"
- "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"

**Bad titles:**
- "A Novel and Efficient Method for Solving Hard Problems" (vague)
- "Improving Things Using Deep Learning" (no specifics)

---

## 2. Abstract (150–250 words)

The abstract must answer four questions in this order:

| Question | Typical Length | Example |
|---|---|---|
| **What problem?** | 1–2 sentences | "Training large language models requires compute that is prohibitive for most researchers." |
| **What is your approach?** | 2–3 sentences | "We propose LoRA, which freezes pretrained model weights and injects trainable rank decomposition matrices." |
| **What are the results?** | 2–3 sentences | "LoRA reduces trainable parameters by 10,000× while achieving comparable or better performance than full fine-tuning on RoBERTa, DeBERTa, and GPT-2." |
| **What is the significance?** | 1 sentence | "This enables fine-tuning of large models on a single GPU." |

**Rules:**
- No citations in abstract
- No acronyms without definition (or avoid acronyms)
- No equations or figures referenced
- Written in present tense for general statements, past tense for specific results

**Abstract ending rule:** The abstract must end with the paper's significance or contribution — what this paper establishes that no prior work established. Do NOT end with a limitations statement, a list of identified problems, or open questions. A limitations-ending abstract signals that the paper's primary finding is incompleteness.

```
WRONG — ends on limitations:
"Six specific architectural limitations are identified, including cooperative-only
scheduling, prompt-space memory constraints, and alpha-stage isolation infrastructure."

RIGHT — ends on significance:
"...Six architectural limitations are identified. The analysis establishes that
OpenClaw satisfies formal OS-level resource management guarantees—scheduled
inference cost reduction by factor N and API credential non-interference—that
no compared framework provides."
```

**Abstract acronym expansion rule:** Non-standard acronyms must be expanded on first use in the abstract, even if also expanded in the body. The abstract is read independently in databases and search engines and must be self-contained.

Standard acronyms that do NOT require expansion in abstract: CPU, GPU, OS, API, RAM, HTTP, AI, ML, LLM, NLP.

Everything else requires expansion: "Quantized Memory Distillation (QMD)", "Virtual Private Server (VPS)", "reinforcement learning from human feedback (RLHF)", "mixture of experts (MoE)".

---

## 3. Index Terms / Keywords

- 4–6 terms from the IEEE Taxonomy
- List in alphabetical order
- Format: `\begin{IEEEkeywords} keyword1, keyword2, keyword3 \end{IEEEkeywords}`
- Match your venue's scope terms

---

## 4. Introduction (~1–1.5 pages)

**Must contain (in order):**

1. **Hook**: Start with the problem or its impact — not "Deep learning has revolutionized..."
2. **Problem statement**: What specific gap or limitation exists?
3. **Motivation**: Why does solving this matter?
4. **Brief related work gap**: What have others tried and why is it insufficient? (1 paragraph)
5. **Contribution statement** (MANDATORY — explicit bulleted list):
   ```
   The contributions of this paper are as follows:
   - We propose [specific method] that achieves [specific advantage].
   - We demonstrate [specific result] on [specific datasets/benchmarks].
   - We provide [code/dataset] at [URL].
   ```
6. **Paper organization**: "The rest of this paper is organized as follows: Section II reviews..."

**What NOT to do in Introduction:**
- Do not give a tutorial on background concepts (that's Section II)
- Do not describe your results in detail (that's Sections V–VI)
- Do not have more than 4 subsections
- Do not cite every paper in your field

---

## 5. Related Work (~1 page)

**Structure by theme, not chronology:**

```
II. Related Work

A. [Theme 1 — e.g., "Efficient Transformers"]
[3–5 sentences per theme. Cite 3–6 papers. Contrast with your approach.]

B. [Theme 2 — e.g., "Knowledge Distillation"]
[...]

C. [Theme 3 — e.g., "Neural Architecture Search"]
[...]
```

**Rules:**
- Group papers by idea, not by year
- Be honest — acknowledge what works in prior methods
- Position your work clearly: "Unlike [12], which requires X, our method does Y"
- Do NOT say "to our knowledge, no prior work has..." unless you are absolutely certain
- Every cited paper must be relevant — do not cite to inflate references

**What NOT to do:**
- "Method A was proposed by [3]. Method B was proposed by [4]. Method C..." (laundry list)
- Vague comparisons: "Our method is better than previous approaches"
- Omitting competing methods — reviewers will know

**Positioning requirement:** Every Related Work subsection must contain at least one evaluative sentence identifying a specific limitation, assumption, or scope boundary of the cited work. "Existing methods have limitations" does not qualify — the limitation must name the cited paper and describe the specific gap.

**Sentence length variation:** Each subsection must contain at least one sentence under 12 words. Uniform medium-to-long sentences are a strong AI detection signal. Short sentences in Related Work should deliver critical assessments, not filler transitions.

---

## 6. Methodology (~2 pages)

**Structure:**

```
III. Proposed Method

A. Problem Formulation
[Define variables, notation. State the objective formally.]

B. [Core Component 1 — e.g., "Architecture Overview"]
[Describe with Figure 1. Reference figure inline.]

C. [Core Component 2 — e.g., "Training Objective"]
[Include equations. Number every equation.]

D. [Core Component 3 — e.g., "Inference Procedure"]
[Algorithm block if helpful.]
```

**Requirements:**
- Define all mathematical notation before use
- Number every equation: `\begin{equation}` ... `\label{eq:loss}`
- Reference every figure: "as shown in Fig. 1"

**IEEE figure inline citation rule:** Every figure must be cited by number in body prose ("as shown in Fig. 1", "Fig. 3 illustrates", "see Fig. 4") at or before the point where the figure appears. A figure caption alone does not satisfy this requirement — the caption is display text, not body argument. A figure with no body prose citation is a floating element and will be flagged during IEEE copy-editing.

Pattern to follow: introduce the figure in the sentence that motivates it — "The three-tier hierarchy is shown in Fig. 4" or "Figure 5 plots this cost ratio across N=1 to N=5." — not as an afterthought caption.

- Include an algorithm block for complex procedures:

```latex
\begin{algorithm}
\caption{Your Algorithm Name}
\begin{algorithmic}[1]
\REQUIRE Input $x$, parameter $\theta$
\ENSURE Output $y$
\STATE Initialize ...
\FOR{each epoch}
    \STATE ...
\ENDFOR
\RETURN $y$
\end{algorithmic}
\end{algorithm}
```

---

## 7. Experiments (~1.5 pages)

**Must contain:**

### A. Experimental Setup
- **Datasets**: Name, version, split sizes, source citation
- **Baselines**: List with citations — every baseline needs a `[N]` cite
- **Metrics**: Define precisely (e.g., "We report top-1 accuracy on the validation set")
- **Implementation**: Framework, hardware, training time
- **Hyperparameters**: Learning rate, batch size, epochs, etc.

### B. Main Results
- Table comparing your method vs all baselines
- Bold the best result in each column
- Include statistical significance where applicable (p-value or std dev)

```latex
\begin{table}[h]
\caption{Comparison on [Dataset]}
\label{tab:main}
\centering
\begin{tabular}{lcc}
\hline
Method & Accuracy (\%) & Params (M) \\
\hline
Baseline A [3] & 72.4 & 25.6 \\
Baseline B [7] & 74.1 & 48.2 \\
\textbf{Ours} & \textbf{76.8} & \textbf{12.3} \\
\hline
\end{tabular}
\end{table}
```

### C. Ablation Study
- Remove one component at a time
- Show why each component contributes
- Critical for top-tier venues

---

## 8. Results (~0.5 page)

Separate from Experiments if the venue expects it (journals typically do, conferences often merge with Experiments).

- State what the numbers mean
- Do not just repeat the table — interpret it
- "Table II shows that our method achieves X% improvement over baseline Y, which we attribute to..."

---

## 9. Discussion (~0.5 page)

**Must contain:**
- Analysis of WHY your method works (not just that it works)
- Failure cases: where does your method underperform? Be honest.
- Limitations: computational cost, data requirements, scope restrictions
- Do NOT claim the method works for everything

---

## 10. Conclusion (~0.25 page)

**Must contain:**
1. What was shown (past tense: "We presented...")
2. Key result (one sentence with the main number/finding)
3. Future work (2–3 specific directions, ordered by urgency — see below)

**Do NOT:**
- Repeat the abstract verbatim
- Introduce new claims not in the paper
- Be vague: "We hope this work inspires future research"
- Announce future work symmetrically: "Three limitations are the most consequential targets..." → signals AI structure

**Future work — ordering and structure:**

Order future work directions by urgency and consequence, not by symmetry. Each direction should have a different sentence length and framing — vary the approach:

```
AI-pattern (flagged):
  "Three limitations are the most consequential targets for future work.
  First, X must evolve toward Y: [one uniform sentence].
  Second, A is a fundamental constraint: [one uniform sentence].
  Third, B must reach production stability: [one uniform sentence]."

Human-pattern (correct):
  "[Most urgent item] is the most pressing gap. [Explanation of why
  it is observably a problem today, not hypothetically.] No such
  mechanism exists today, and the fix is narrower than it appears.

  [Second item] is a different category of problem: [reason why it
  differs from the first]. The right solution is [specific approach]
  — decoupling [X] from [Y], which is the correct separation of
  concerns.

  [Third item] is a binary prerequisite [for some specific use case].
  [What must happen] must reach production quality first — the
  [other quality] is sound; it is [this specific quality] that
  requires investment."
```

The key signals of human future-work writing:
- Items ordered by urgency ("most pressing," "different category," "binary prerequisite")
- Varied paragraph lengths (long, medium, long — not three matching lengths)
- Explicit framing of what is NOT the problem ("the security architecture is sound")
- Concrete observable trigger ("observable in any multi-user deployment")

---

## 11. Acknowledgments

```
This work was supported by [Grant Agency, Grant No. XXX].
The authors thank [Name] for [specific contribution].
Experiments were conducted on [HPC cluster / Cloud provider].
```

**Omit entirely in blind review submissions.**

---

## 12. References

IEEE numbered format. See `ieee-formats.md` for all citation types.

**Minimum expected references by paper type:**
- Conference paper: 25–40 references
- Journal article: 40–60+ references
- Survey/review: 80–150+ references

**Reference count realism (Variant D — Conceptual papers):**
These counts are norms, not hard requirements. IEEE Access does not reject papers for
reference count — it rejects for uncited claims. For a conceptual/proposed architecture
paper, 17 high-quality verified citations outperform 60 padded unverified ones.

Rule: Every citation must be verified. If you have 20 verified citations, submit with 20.
Note in SUBMISSION-CHECKLIST.md which reference categories could be expanded (governance
frameworks, regulatory documents, competing implementations) for the author to research
before final submission.
