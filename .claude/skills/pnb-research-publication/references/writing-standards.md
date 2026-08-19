# Academic Writing Standards for IEEE Papers

## Core Principle

IEEE research papers require precision, not eloquence. Every sentence should carry
information. Every claim should be citable. Every number should be reproducible.

This is the opposite of book writing: no personal flair, no emotional engagement,
no anecdotes. The reader is a peer reviewer — treat them as a specialist who will
check every claim.

---

## Voice and Register

| Book Writing | IEEE Paper Writing |
|---|---|
| "I believe this approach is elegant" | "This approach reduces complexity by O(n log n)" |
| Personal opinions welcomed | Opinions require evidence |
| Emotional engagement | Precise, measurable claims |
| Varied rhythm for readability | Clarity over style |
| First-person singular ("I") | "We" (even for single author) or passive |
| Anecdotes encouraged | Evidence-based only |
| "This part is genuinely hard" | "This problem is NP-hard [N]" |

---

## Tense Rules

| Context | Tense | Example |
|---|---|---|
| General truths, principles | Present | "Neural networks learn representations." |
| Your proposed method | Present | "Our model consists of three layers." |
| Your experimental results | Past | "The model achieved 94.2% accuracy." |
| Prior work findings | Past | "He et al. [3] demonstrated that..." |
| Historical events | Past | "ResNet was introduced in 2016 [3]." |
| Future work | Future/modal | "Future work will explore..." |

---

## Passive vs Active Voice

**Active** (preferred for contributions):
- "We propose a novel attention mechanism."
- "We demonstrate that our method outperforms baselines by 3.2%."
- "We release the code at [URL]."

**Passive** (acceptable for methodology):
- "The model was trained for 100 epochs."
- "Samples were randomly split 80/10/10."
- "The learning rate was decayed by 0.1 at epochs 30 and 60."

**Avoid passive for contributions.** "A novel method is proposed" reads as evasive.

---

## Hedging — When to Use and When Not To

**Use hedging for:**
- Claims about future applicability: "This approach may generalize to..."
- Preliminary observations: "Results suggest that..."
- Comparisons without full ablation: "This appears to improve performance..."
- Claims outside your experimental scope: "We hypothesize that..."

**Never hedge for:**
- Your own reported experimental results: ~~"Our method seems to achieve..."~~ → "Our method achieves..."
- Mathematical claims you proved: ~~"The complexity appears to be O(n²)"~~ → "The complexity is O(n²)"
- Direct comparisons with baselines you measured: ~~"Our method might outperform..."~~ → "Our method outperforms..."

---

## Contribution Statement (Mandatory)

Every IEEE paper must have an explicit contribution list in the Introduction. This is
the most important paragraph in the paper — it tells reviewers exactly what to evaluate.

**Required format:**
```latex
The contributions of this paper are as follows:
\begin{itemize}
  \item We propose [specific named method] that [specific measurable advantage].
  \item We demonstrate [specific result] on [specific benchmarks/datasets].
  \item We provide [code/dataset/model] at [URL or "upon acceptance"].
\end{itemize}
```

**Good contribution statement:**
```
The contributions of this paper are as follows:
- We propose LoRA, a parameter-efficient fine-tuning method that reduces trainable
  parameters by 10,000× compared to full fine-tuning.
- We demonstrate that LoRA achieves comparable or better performance than full
  fine-tuning on GLUE, MultiNLI, and SQuAD benchmarks.
- We release the LoRA implementation at https://github.com/microsoft/LoRA.
```

**Bad contribution statement:**
```
We make the following contributions:
- A new and efficient method for the problem.  ← too vague
- Experiments showing our method works well.   ← no specifics
- Code will be released.                       ← no URL or commitment
```

---

## Related Work Writing

### What to achieve:
1. Show you know the field
2. Honestly position your work vs. prior work
3. Identify the gap your paper fills
4. Cite the right papers (not just recent ones)

### How to group:
Group by **theme** (what approach they take), not by **year** or **author**:

```
A. Efficient Transformers
[Theme 1: papers that reduce attention complexity] ... Unlike [3][7][12], 
which reduce quadratic complexity via approximation, our method avoids 
the approximation entirely by [your approach].

B. Knowledge Distillation
[Theme 2] ... While [5][9] distill knowledge into smaller models, 
they require the full teacher model at inference time.

C. Neural Architecture Search
[Theme 3] ...
```

### What NOT to write in Related Work:
- "Method A was proposed by [3]. Method B was proposed by [4]. ..." (laundry list)
- "To the best of our knowledge, no prior work has..." (unless absolutely certain)
- Vague claims: "Our method is better than all existing approaches"
- Omitting directly competing methods — reviewers will know

---

## Banned Phrases (Remove Always)

These are AI-writing signatures that will flag in editorial review:

| Banned | Replace with |
|---|---|
| "It is worth noting that..." | State it directly |
| "Interestingly, ..." | Remove preamble |
| "Notably, ..." | Remove preamble |
| "It should be noted that..." | State it directly |
| "In this section, we will present..." | Start with the content |
| "This section describes..." | Start with the content |
| "As can be seen from..." | "Table N shows..." or state the observation |
| "The proposed method" (repeatedly) | "Our method", "the method", or its name |
| "state-of-the-art" without a citation | Always follow with citation: "state-of-the-art [N]" |
| "significantly improves" without a number | Give the number: "improves by 3.2%" |
| "outperforms all baselines" | "outperforms all baselines in Table II" |

---

## Section-Specific Writing Rules

### Abstract
- Write last (after the paper is done)
- 4 sentences: problem / method / results / significance
- No citations, no undefined acronyms, no equations
- Passive voice acceptable: "A method is proposed..."

### Introduction
- Start with the problem, not the field: "Scaling transformers beyond 10B parameters requires..."
- NOT: "Deep learning has achieved remarkable success in recent years."
- Contribution list must be specific and measurable

### Methodology
- Define all notation in a "Notation" paragraph or table if > 5 variables
- Number every equation
- Reference every figure before the figure appears: "Fig. 1 illustrates..."
- Describe enough for replication

### Experiments
- Name every dataset with its version and citation
- Name every baseline with its paper citation
- Define every metric precisely (top-1 accuracy on what split?)
- State compute resources (GPU type, training time)

### Conclusion
- Start with what was shown: "We presented [method], which..."
- One sentence: the single most important result
- 2–3 specific future directions (not "we plan to explore many directions")
- Do NOT introduce new claims

---

## Reproducibility Standards (Mandatory)

Reviewers at top venues now check for reproducibility. Include:

```latex
\subsection{Implementation Details}
All experiments were conducted on a single NVIDIA A100 GPU (80GB).
We used PyTorch 2.1 \cite{pytorch} with CUDA 11.8.
Training took approximately 12 hours per run.
The learning rate was set to $10^{-4}$ with cosine annealing over 100 epochs,
batch size 256, and weight decay $10^{-4}$.
Code is available at \url{https://github.com/org/repo}.
```

**Minimum reproducibility checklist:**
- [ ] Framework and version cited
- [ ] Hardware specified
- [ ] All key hyperparameters listed (lr, batch size, epochs, optimizer, scheduler)
- [ ] Datasets: name, version, split sizes
- [ ] Baselines: all reimplemented with same settings? Or results from original papers?
- [ ] Metrics: exact definition (e.g., "top-1 accuracy on ImageNet validation set")
- [ ] Random seeds: reported or averaged over N runs with std dev
