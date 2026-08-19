# Anti-AI-Detection for Research Papers

## The Academic AI Detection Problem

IEEE reviewers and journal editors now use AI detection tools. More importantly,
experienced reviewers can identify AI-generated academic prose by its specific
failure patterns — even without tools.

AI-generated research writing fails in predictable ways:
- **Vague claims** — no specific numbers, datasets, or failure modes
- **Generic methodology** — describes the approach conceptually without real implementation detail
- **Uniform hedging** — everything is "may", "could", "suggests"
- **No failures** — AI never acknowledges what doesn't work
- **Template prose** — every section follows the same rhythm

The goal is not to "fool" detectors — the goal is to write the way expert
researchers actually write. That writing naturally passes detection.

---

## AI Detection Tools Used in Academia

| Tool | What It Detects | Access | Threshold |
|---|---|---|---|
| **Turnitin AI Writing** | AI-generated prose (GPT-style) | Institutional only | 0% in submitted work |
| **GPTZero** | Perplexity + burstiness | **Requires paid API key** | < 20% AI probability |
| **Originality.ai** | AI + plagiarism combined | Paid subscription | < 20% AI probability |
| **Copyleaks** | AI detection + plagiarism | Paid subscription | < 20% AI probability |
| **iThenticate AI** | IEEE/Elsevier journals | Institutional / web portal | < 20% AI probability |
| **Hello-SimpleAI/chatgpt-detector-roberta** | ChatGPT-style prose | **Free, runs offline** | < 20% AI probability |

**IEEE Policy (2023+):** AI cannot be listed as an author. AI-assisted writing must
be disclosed in some venues. Check the specific venue's policy.

---

## Free Local AI Detection — No API Key Required

GPTZero returns 401 without a paid API key. ZeroGPT returns 403 ("Please make a
purchase"). GPT-2 perplexity scoring is unreliable for academic text — it was never
trained on LaTeX or math notation and assigns false-high AI probabilities to correctly
written equations and technical terminology.

**Use this instead — runs fully offline, section-by-section:**

```bash
pip install transformers torch
```

```python
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

detector = pipeline(
    "text-classification",
    model="Hello-SimpleAI/chatgpt-detector-roberta",
    device=-1  # CPU; change to 0 for GPU
)

sections = {
    "Abstract":     "...",
    "Introduction": "...",
    "Section III":  "...",
    # add each section's text
}

print(f"{'Section':<30} {'Label':<10} {'AI%':>5}  {'Status'}")
print("-" * 55)
for name, text in sections.items():
    result = detector(text[:512], truncation=True)[0]
    label = result["label"]
    score = result["score"]
    ai_pct = round((1 - score)*100, 1) if label == "Human" else round(score*100, 1)
    status = "✅ PASS" if ai_pct < 20 else "❌ REWRITE"
    print(f"{name:<30} {label:<10} {ai_pct:>4.1f}%  {status}")
```

**Target:** every section < 20% AI probability. Any section ≥ 20% → apply
specificity + burstiness fixes and re-scan.

**Important:** The model's 512-token window covers approximately 350–400 words.
Split sections longer than 400 words and scan each half independently.

---

---

## How AI Detectors Work (So You Can Write Better)

AI detectors measure two things:

**1. Perplexity** — how "surprising" or unpredictable each word choice is.
- AI tends to pick the statistically most likely next word → low perplexity
- Expert human writing uses domain-specific, precise terms that are statistically rare → higher perplexity

**2. Burstiness** — variation in sentence length.
- AI produces uniformly structured sentences of similar length
- Human experts mix short punchy sentences with long technical ones

**3. Specificity** — AI writes vague generalities; humans cite specifics.

---

## Banned AI-Writing Patterns in Research Papers

These patterns reliably trigger AI detection AND signal poor academic writing:

### Banned opening patterns:
```
× "Deep learning has revolutionized the field of X."
× "In recent years, X has gained significant attention."
× "The rapid advancement of Y has led to..."
× "With the proliferation of Z, there is a growing need for..."
× "This paper presents a novel approach to..."
× "We propose a framework that leverages..."
```

**Replace with**: Start with the specific technical problem or a concrete observation.
```
✓ "Standard self-attention scales as O(n²) in sequence length, making it
   prohibitive for documents exceeding 4,096 tokens on a single A100 GPU."
✓ "Existing methods for X fail on benchmark Y because they assume Z —
   an assumption that breaks on 23% of real-world inputs [3]."
```

### Banned filler phrases (remove entirely):
```
× "It is worth noting that..."          → state it directly
× "Notably, ..."                        → remove preamble
× "Importantly, ..."                    → remove preamble
× "It should be noted that..."          → state it directly
× "The proposed method leverages..."    → "Our method uses..."
× "We leverage the power of..."         → "We use..."
× "state-of-the-art performance"        → give the actual number
× "significant improvement"            → give the actual percentage
× "Our method outperforms baselines"   → "Our method achieves 3.2% higher accuracy"
× "as can be seen in Fig. X"           → "Fig. X shows that [specific observation]"
× "which demonstrates the effectiveness" → state what was demonstrated specifically
```

### Banned conclusion patterns:
```
× "In this paper, we have presented..."       → starts with recap
× "We hope this work will inspire..."         → vague aspiration
× "There are many avenues for future work..." → non-specific
× "The results demonstrate the potential..."  → vague
```

---

## Writing Techniques That Beat AI Detection

### Technique 1: Specificity Over Generality

AI writes generalities. Humans write specifics.

```
AI style:    "Our method is efficient and scalable."
Human style: "Our method processes 512-token sequences in 12ms on an A100 GPU,
              compared to 47ms for the vanilla attention baseline."
```

### Technique 2: Acknowledge Failures

AI never admits what doesn't work. A real researcher does.

```
AI style:    "Our method achieves strong results across all benchmarks."
Human style: "Our method underperforms on long-context tasks (>2048 tokens) —
              we attribute this to the fixed window size in our attention pattern,
              a limitation we discuss in Section VI."
```

Including a genuine failure case increases credibility AND lowers AI probability score.

### Technique 3: Engineer Sentence Length Variation (Burstiness)

```
AI style (uniform):
"We propose a novel attention mechanism. The mechanism reduces complexity. It also
maintains performance. Results show improvement over baselines. The method is efficient."

Human style (varied):
"Standard attention is O(n²). Our mechanism replaces exact computation with a
linear-time approximation via random feature maps — a trade-off that costs 0.3%
accuracy on average while reducing memory from 40GB to 6GB per batch, making
fine-tuning feasible on consumer hardware."
```

Rule: At least one sentence < 8 words AND one sentence > 30 words per section.

### Technique 4: Domain-Specific Precise Vocabulary

AI uses safe, common words. Expert writers use precise technical terms.

```
AI: "We use a neural network to process the input data."
Expert: "We apply a bidirectional LSTM encoder over subword tokens, pooling the
         final hidden states via mean-pooling before projection."
```

### Technique 5: Take a Position

AI hedges everything. Researchers take positions on trade-offs.

```
AI: "Both approaches have advantages and disadvantages."
Human: "The approximation-based approach is the right default for sequences
        over 512 tokens. If your task requires exact attention over short
        sequences, the vanilla implementation is preferable."
```

### Technique 6: Specific Implementation Details

AI methodology sections are abstract. Real papers give concrete details.

```
AI: "The model was trained using standard optimization techniques."
Human: "We trained for 50 epochs using AdamW [N] with β₁=0.9, β₂=0.999,
        weight decay 0.01, and a learning rate of 2×10⁻⁴ with linear
        warmup over the first 5% of steps. All experiments used a batch
        size of 32 per GPU across 4 A100s."
```

---

## Editor Agent Anti-AI Transformation Protocol

The Editor Agent applies this transformation checklist on every section:

### Pass 1 — Specificity audit
For each sentence:
- Does it contain a number? If yes, is it real? (→ Fact-Checker verifies)
- Does it make a general claim? Replace with specific: "X improves Y by Z% on dataset D"
- Does it describe a method vaguely? Add implementation detail.

### Pass 2 — Banned phrase removal
Run grep and remove/replace all banned phrases:
```bash
grep -n "worth noting\|It should be noted\|leverage\|proliferation\
         \|significant improvement\|demonstrates the effectiveness\
         \|state-of-the-art performance\|in recent years\|gained attention" paper.md
```
Every match must be rewritten.

### Pass 3 — Burstiness check
For each paragraph:
- Count sentence lengths (approximate word count per sentence)
- If 3+ consecutive sentences are similar length: rewrite one to be short (<8 words) and one to be long (>30 words)
- Minimum variation: shortest sentence in paragraph ≤ half the length of longest sentence

### Pass 4 — Position and failure check
For each section:
- Is there at least one limitation or failure case? (Experiments and Discussion must have this)
- Is there at least one direct technical position (not just hedged observation)?

---

## Pre-Submission AI Detection Audit

### Run the scanner suite:

```
1. Hello-SimpleAI/chatgpt-detector-roberta [FREE, offline — run this first]
   → See "Free Local AI Detection" section above
   → Target: < 20% AI probability per section
   → Advantage: no API key, no rate limits, no purchase required

2. GPTZero (https://gptzero.me) [requires paid API key]
   → API: POST to https://api.gptzero.me/v2/predict/text with Bearer token
   → Without API key: returns 401 Unauthorized — cannot be used
   → Alternative: use the web UI manually (free tier allows limited uploads)

3. Originality.ai (paid, more accurate)
   → Full document scan
   → Target: < 20% AI score

4. Turnitin AI (if your institution has access)
   → Target: 0 AI-flagged passages
```

### If a section scores > 20% AI probability:

Step 1: Identify which paragraph triggered it (GPTZero highlights at sentence level)
Step 2: Apply specificity technique — add concrete numbers, datasets, implementation details
Step 3: Apply burstiness — break up uniform sentence lengths
Step 4: Add one genuine limitation or position statement
Step 5: Re-scan

### Sections most commonly flagged:
1. **Introduction** — generic motivation language
2. **Related Work** — formulaic "X proposed Y which achieves Z" structure
3. **Conclusion** — template recap and future work language
4. **Abstract** — high-level language with no specifics
5. **Installation Manual (multi-subsection)** — uniform paragraph rhythm across subsections (see below)

These sections need the most human rewriting effort.

---

## Installation Manual — Structural Anti-Pattern

When a paper includes a multi-subsection installation guide (≥5 platforms), all subsections tend to converge on the same rhythm:

```
AI-pattern (flagged):
  Subsection B: one-line context → bash block → notes
  Subsection C: one-line context → bash block → notes
  Subsection D: one-line context → bash block → notes
  Subsection E: one-line context → bash block → notes
```

This structural uniformity triggers AI detection even when individual sentences are humanized. Fix: vary the paragraph *structure* — not just word choice — across at least 3 of N subsections.

**Safe variation patterns:**

```
Option A — Lead with the platform distinction before code:
  "Linux differs from macOS in one critical way: daemon lifetime. The
  systemd user service stops on logout unless linger is enabled with
  loginctl enable-linger $USER — skipping this is the most common
  Linux setup error. [code block] [notes]"

Option B — Lead with the decision criterion:
  "Choose NemoClaw over standard Docker when your deployment is
  customer-facing or compliance-audited. The $10/month premium over
  Docker Compose covers kernel-level isolation. [code block] [notes]"

Option C — Lead with the failure mode:
  "WSL2 is required, not optional. Several native plugins depend on
  POSIX syscalls unavailable on Windows natively; browser automation
  fails silently on the Windows path. [code block] [notes]"
```

**Check**: After writing all subsections, scan their first sentences. If 3+ start with "[Platform] installation" or with a bash block, restructure those subsections.

---

## AI Disclosure Policy (IEEE)

As of 2023, IEEE policy requires:
- AI **cannot be listed as an author** (it cannot take responsibility for the work)
- Use of AI tools for **writing assistance** must be disclosed in some venues
- Use of AI for **data generation or analysis** must be disclosed and validated

Check your specific venue's author instructions. When in doubt, add a disclosure:

```
\section*{Author Contributions}
The authors used [tool name] to assist with grammar checking.
All scientific content, experimental design, and conclusions are
the sole responsibility of the authors.
```

---

## Conclusion Section — Paragraph-Level Uniformity (AI Signal)

The Conclusion section is the most commonly AI-flagged section after Related Work. A specific failure pattern is **mechanical paragraph uniformity**: all future-work paragraphs containing exactly 3 sentences and 55–75 words. GPTZero measures burstiness at the paragraph level, not just the sentence level.

**Required:** At least one conclusion paragraph must be 1–2 sentences (< 40 words) and at least one must be 5+ sentences (> 100 words). Do not target symmetry — target natural emphasis gradation where urgency drives length.

```
AI-flagged pattern (avoid):
Para 3: "X is the most pressing gap. [1 long sentence]. [1 medium sentence]." — 3 sentences, 65 words
Para 4: "Y is a different category. [1 long sentence]. [1 medium sentence]." — 3 sentences, 68 words
Para 5: "Z is a prerequisite. [1 long sentence]. [1 medium sentence]."     — 3 sentences, 62 words

Human-varied pattern (correct):
Para 3: "X is the most pressing gap. It is a missing mechanism — adding one does not require redesigning the architecture." — 2 sentences, 30 words
Para 4: "Y is a different category of problem entirely... [4-sentence explanation of why] ...which is the correct separation of concerns." — 5 sentences, 90 words
Para 5: "Z is a binary prerequisite. [2-sentence explanation]." — 3 sentences, 55 words
```

**Pass 3 burstiness check — add to Conclusion section scan:**
```bash
# Extract conclusion section and approximate paragraph word counts
awk '/^## (Conclusion|VIII\.|VII\.)/,/^---/' paper.md | \
  awk 'BEGIN{RS=""; p=0} {p++; n=split($0,a," "); print p": ~"n" words"}' | head -10
# If 3+ consecutive paragraphs show 55–80 words: rewrite one short, one long
```

---

## Related Work — Specific AI Detection Failure Modes

Related Work is the second most AI-flagged section. Two independent failure modes both require fixes.

### Failure Mode 1: Uniform Sentence Length

AI-generated Related Work consists exclusively of medium-to-long sentences (15–35 words), creating a flat rhythmic profile that GPTZero flags as high AI probability.

**Required:** Each Related Work subsection must contain at least one sentence under 12 words that delivers a direct critical assessment. Short sentences in Related Work should carry weight, not filler.

```
AI-flagged (all medium/long — avoid):
"AIOS [3] introduces a layered abstraction that separates storage, execution,
and tool access, demonstrating improved throughput in multi-agent benchmarks,
though no security architecture is specified."

Human-varied (correct — short punch included):
"AIOS [3] separates storage, execution, and tool access in a layered abstraction,
demonstrating throughput gains in multi-agent benchmarks.
Neither the security model nor deployment configuration is addressed.
No production security architecture exists in the current release."
```

**Audit command:**
```bash
# Find all sentences under 12 words in Related Work section
awk '/^## (II\.|Related Work)/,/^## (III\.|Background)/' paper.md | \
  grep -o '[^.!?]*[.!?]' | awk 'NF < 12 {print NR": "$0}' | head -20
# If no output: zero short sentences in Related Work = AI flag — add at least 1 per subsection
```

### Failure Mode 2: Descriptive Catalogue — No Evaluative Positions

IEEE reviewers evaluate Related Work on two criteria: (1) coverage and (2) positioning. A Related Work section that describes prior work without critiquing it fails criterion 2.

**Required:** Every Related Work subsection must contain at least one evaluative sentence that identifies a specific limitation, assumption, or scope boundary of the cited work. Generic statements ("existing methods have limitations") do not qualify.

```
Catalogue style (insufficient — avoid):
"AIOS [3] proposes a layered architecture. AutoGen [5] provides multi-agent
conversation. AgentBench [7] introduces an evaluation benchmark."

Positioned style (required):
"AIOS [3] proposes a layered architecture that separates tool access from
execution, but assumes single-machine deployment — multi-node coordination
is outside its current scope. AutoGen [5] supports multi-agent conversation
but delegates scheduling to the application layer, producing inconsistent
behavior under concurrent load. Neither system ships a security architecture."
```

**Audit command:**
```bash
# Look for evaluative/critical language in Related Work section
awk '/^## (II\.|Related Work)/,/^## (III\.|Background)/' paper.md | \
  grep -in "however\|but \|limitation\|fails\|lacks\|does not\|unable\|constraint\|assumes\|restricted\|cannot\|weakness\|gap\|outside its"
# If no output for a subsection: that subsection is purely descriptive = flag
```
