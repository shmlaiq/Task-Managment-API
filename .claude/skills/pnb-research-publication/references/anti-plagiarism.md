# Academic Plagiarism Prevention for Research Papers

## Pre-Delivery Plagiarism Self-Assessment (Run Before iThenticate)

Before running any external scanner, do a section-by-section risk rating:

| Section | Typical Risk | Why |
|---|---|---|
| Abstract | Very Low | Original summary of your own work |
| Introduction | Very Low | Original problem framing |
| Related Work | **Medium — Highest Risk Zone** | Describes prior papers; shares field terminology |
| Methodology / Architecture | Very Low | Your original contribution |
| Results / Analysis | Very Low | Your own numbers and interpretation |
| Limitations / Discussion | Very Low | Original critical assessment |
| Conclusion | Low | Some field-standard phrasing is unavoidable |
| References | **Excluded** | iThenticate excludes reference lists by default |

**Estimated safe iThenticate score for a well-written paper: 8–12% overall**
- ~3–5% from Related Work (shared terminology, cited numbers from primary sources)
- ~2–3% from common domain vocabulary (unavoidable in any field)
- ~0% from original contribution sections (Methodology, Architecture, Analysis)

**Delivery blocker:** Any single section exceeding 20% similarity → rewrite that section.

---

## What Counts as Plagiarism in Academia

Academic plagiarism is broader than most people realize. It includes:

| Type | Example | Risk |
|---|---|---|
| **Verbatim copying** | Copy-pasting sentences from another paper without quotes | Desk rejection / retraction |
| **Near-verbatim paraphrase** | Same sentence, just synonyms swapped | Turnitin flags this |
| **Idea theft** | Presenting someone else's method as your own | Career-ending |
| **Self-plagiarism** | Copying your own prior published paper without citation | Journal policy violation |
| **Partial citation** | Paraphrasing a paper but not citing it | Plagiarism |
| **Mosaic plagiarism** | Stitching sentences from multiple papers | Still plagiarism |
| **Data fabrication** | Reporting fake experimental results | Retraction + ban |

---

## Related Work — High-Risk Patterns to Fix Before Submission

These patterns consistently trigger iThenticate even in properly cited papers:

### Pattern 1: Echoing a Paper's Own Metaphor
When a cited paper introduced a memorable phrase or analogy, using their exact words
in your Related Work — even with a citation — can flag as similarity.

```
RISKY (mirrors MemGPT abstract verbatim):
"the context window is main memory; long-term storage is disk [3]"

SAFE (same meaning, your own sentence structure):
"the active context window functions as working memory, while external
 persistent storage acts as the disk equivalent [3]"
```

**Rule:** If the original paper coined the phrase, rephrase it. Cite the concept, not the words.

### Pattern 2: Author Name Mismatch
When you write "Smith et al. [N] demonstrate..." — verify the actual first author of [N]
matches "Smith." This is a factual error AND can flag inconsistency during review.

```
WRONG: "Zhan et al. [16] demonstrate that injection attacks can cause..."
       (if reference [16] is actually Liu et al.)

RIGHT: Check the BibTeX `author` field for [16] — use that last name inline.
```

**Rule:** Before delivery, grep for every "et al." in the paper and cross-check each
against the corresponding BibTeX entry author field.

```bash
# Find all inline author references
grep -n "et al\." paper.md

# Cross-check each against references.bib
grep "author" references.bib
```

### Pattern 3: Cited Numbers That Mirror Abstracts
Performance numbers from prior papers (e.g., "achieves 85.9% Pass@1") are lifted
directly from their abstracts. They must be cited — but iThenticate may still flag
the sentence because the number + metric + paper name creates a near-verbatim match.

**Fix:** Embed the number in your own analytical sentence, not a restatement:
```
RISKY:  "MetaGPT achieves 85.9% Pass@1 on HumanEval [5]."
SAFER:  "On HumanEval code generation, role-based SOPs in MetaGPT [5] yield
         85.9% Pass@1 — a gain attributed to structured inter-agent verification."
```

### Pattern 4: Vendor / Official Documentation Near-Verbatim (Rule P)

Product pages, technical documentation, and marketing copy from companies like
Microsoft, Google, IBM, and NVIDIA use precise, distinctive phrasing that is
indexed on thousands of web pages. Writing a description of their products while
the documentation is open in front of you produces near-verbatim matches that
iThenticate will flag.

**Examples of dangerous vendor phrases:**
- "a domain-specific language for quantum computation" (Microsoft Q# docs)
- "enables seamless collaboration between" (generic marketing phrase, highly indexed)
- "purpose-built for quantum" (product marketing boilerplate)

**The read-close-write method applies equally here:**
1. Read the vendor documentation to understand the factual content
2. Close the documentation
3. Write your characterization using your own analytical framing
4. Add the citation
5. Never describe what a vendor product does using the vendor's own marketing language

```
RISKY (near-verbatim from Microsoft Q# page):
"Q# is a domain-specific language for quantum computation and the Quantum
 Development Kit (QDK) is the surrounding tooling."

SAFE (same facts, original framing):
"Q# is a functional language built around reversible-computation semantics,
 with quantum gate operations as first-class constructs; the Quantum Development
 Kit (QDK) is the surrounding compiler and tooling ecosystem."
```

### Pattern 5: Abstract-Body Phrase Echo (Rule O)

When a paper is written body-first, then an abstract is composed from the body,
it is easy to lift a distinctive phrase from a section and paste it into the
abstract. The result: the same 5+ word phrase appears both in the abstract and
in the body. Reviewers who read both will notice this structural laziness.

**Detection:**
```bash
# After finishing the abstract, pick 3 distinctive phrases (5+ words):
grep -n "most geographically distributed" main.tex
# Should appear at MOST once (in the abstract). A second hit in the body = echo.
```

**Fix:** Rewrite the BODY occurrence with the same facts but different words. The
abstract should crystallise the finding; the body should elaborate it with
different phrasing. If they sound identical, one of them is redundant.

```
ECHO (abstract):  "the most geographically distributed quantum OS deployment"
ECHO (body §III): "the most geographically distributed quantum OS deployment"

FIXED (body §III): "a deployment scale no comparable academic prototype approaches:
                    339,000+ jobs across 145 countries"
```

---

## The Read-Close-Write Method (Mandatory for Literature Review)

This is the only safe method for writing about prior work:

```
Step 1: READ the original paper thoroughly
Step 2: CLOSE the paper (do not look at it)
Step 3: WRITE your summary from memory
Step 4: CITE — add the [N] citation
Step 5: CHECK — compare your summary to the original to verify accuracy
         (but do NOT copy phrases even during this check)
```

**Why this works**: Writing from memory forces you to understand and rephrase,
not copy. The final check catches factual errors without enabling verbatim copying.

**What NOT to do:**
- Read a sentence, then write a "synonym version" of it → mosaic plagiarism
- Copy the abstract and lightly edit it → verbatim plagiarism
- Describe an algorithm by changing variable names → plagiarism

---

## Paraphrase Rules

### A legitimate paraphrase must differ in BOTH sentence structure AND vocabulary:

```
Original: "We propose a lightweight attention mechanism that reduces the quadratic
           complexity of self-attention to linear complexity by approximating the
           attention matrix using random features."

BAD (synonym substitution — still plagiarism):
"They introduce a compact attention approach that decreases the quadratic cost of
 self-attention to linear cost by estimating the attention matrix via random features."

GOOD (structural + vocabulary change):
"The method addresses the O(n²) bottleneck of standard self-attention by replacing
 exact attention computation with a linear-time approximation based on random
 feature maps [N]."
```

### Test for a legitimate paraphrase:
- Different sentence structure? ✓
- Different vocabulary (not just synonyms)? ✓
- Same factual meaning? ✓
- Citation present? ✓

---

## Self-Plagiarism (Duplicate Publication)

### What counts:
- Reusing a paragraph from your own conference paper in a journal extension without disclosure
- Submitting the same paper to two venues simultaneously
- Publishing data already published in a prior paper without noting it

### What is acceptable:
- Quoting your own prior work with citation: "As we showed in [N], ..."
- Extending a prior short paper: disclose in the submission ("This is an extended version of [N]")
- Reusing your own experimental setup description (method section prose) with self-citation

### IEEE policy on dual submission:
IEEE prohibits submitting a paper currently under review elsewhere. Check each venue's policy.

---

## Code and Algorithm Plagiarism

**Rule**: All code examples must be original implementations.

```python
# WRONG — copy-pasted from a GitHub repo (even if modified):
# Original: https://github.com/huggingface/transformers/blob/main/src/...
def forward(self, hidden_states, attention_mask=None):
    query_layer = self.transpose_for_scores(self.query(hidden_states))
    ...

# RIGHT — your own implementation with attribution:
# Based on the attention formulation in [N], we implement:
def forward(self, x, mask=None):
    Q = self.W_q(x)   # [B, T, d_k]
    K = self.W_k(x)
    ...
```

If you adapt code from a published paper's official repo, you MUST:
1. State this in the paper: "We adapt the official implementation of [N]"
2. Check the repo's license (MIT/Apache = OK with attribution; GPL = complex)
3. Not claim the implementation as original

---

## Figures and Tables from Other Papers

**Never reproduce a figure from another paper** without permission and citation.

### Alternatives:
1. **Redraw the figure** in your own style (with citation: "adapted from [N]")
2. **Reference the figure** without reproducing: "as shown in Fig. 3 of [N]"
3. **Request permission** from the publisher (IEEE: use IEEE permissions portal)

### Tables from other papers:
- You CAN report numbers from another paper's table (with citation)
- You CANNOT reproduce the entire table layout without permission
- If recreating a comparison table with published numbers, note: "Results for [Method] from [N]"

---

## Academic Plagiarism Scanners

### Tools and thresholds:

| Tool | Type | Threshold | Notes |
|---|---|---|---|
| **iThenticate** | Text similarity | < 15% total, < 5% from any single source | Used by most IEEE journals |
| **Turnitin** | Text similarity | < 15% | Also detects AI writing |
| **Copyscape** | Web content | 0% verbatim | For web-published content |
| **CrossCheck** | CrossRef network | < 15% | IEEE standard |

### What these tools flag:
- Verbatim and near-verbatim matches (even in quotes)
- Your own prior publications (self-plagiarism)
- Common phrases in the field (false positives — reviewers must judge)
- Reference list matches (not a concern — references are expected to match)

### What they don't catch:
- Translated plagiarism (from non-English papers)
- Idea theft without text copying
- Data fabrication

---

## Fact Packet Citation Integrity (Literature Agent Rule)

The Literature Agent must follow this protocol for every citation:

```
1. Find the ORIGINAL primary source (not a blog, not a secondary citation)
2. Read the relevant section of the original paper
3. Extract the exact claim or number
4. Formulate the citation in IEEE format
5. Return to Writing Agent as: claim + citation (not sentence to copy)

The Writing Agent then writes its own sentence about this fact.
The Literature Agent NEVER provides sentences to copy — only facts and citations.
```

---

## Pre-Submission Plagiarism Checklist

- [ ] Every paragraph in Related Work was written using the read-close-write method
- [ ] No sentence is a verbatim or near-verbatim copy of any source
- [ ] All direct quotes use quotation marks + `[N]` citation
- [ ] Self-citations present for any reused content from prior own work
- [ ] All code is original or explicitly attributed
- [ ] All figures are original, redrawn, or used with permission + citation
- [ ] All table data from other papers has `[N]` source attribution per row
- [ ] iThenticate or Turnitin similarity < 15% (run before submission)
- [ ] No single-source similarity > 5%
- [ ] Reference list excluded from similarity count (standard practice)

---

## Running iThenticate / Turnitin

**IMPORTANT: iThenticate cannot be run from the CLI or automated.** It is a
web-only portal requiring institutional or paid access. There is no public API.
Attempting to automate it via curl or scripts will fail. Run the local pre-scan
below first, then upload manually.

### Step 1 — Local n-gram pre-scan (run from CLI before uploading)

This identifies your highest-risk phrases before you pay for a scan:

```python
import re
from collections import Counter

with open("paper.md") as f:
    raw = f.read()

# Strip headers, reference list, math, citations
body = re.sub(r'^##.*$', '', raw, flags=re.MULTILINE)
body = re.sub(r'^\[[\d]+\].*$', '', body, flags=re.MULTILINE)
body = re.sub(r'\[[\d,\s]+\]', '', body)
body = re.sub(r'\$.*?\$', '', body)
body = re.sub(r'\s+', ' ', body).strip()

words = body.lower().split()
ngrams = [' '.join(words[i:i+8]) for i in range(len(words)-7)]

# Known high-risk patterns (report title phrases, proper nouns, cited doc names)
risk_patterns = [
    r'\b(your institution|org name|report title keywords)\b',
    # add patterns specific to your paper's source documents
]

flagged = [ng for ng in ngrams if any(
    re.search(pat, ng, re.I) for pat in risk_patterns)]

print(f"Scanned: {len(ngrams)} 8-grams | Flagged: {len(flagged)} | Density: {len(flagged)/len(ngrams)*100:.1f}%")
```

**What counts as a benign flag** (iThenticate will flag these but they do not reduce your score meaningfully):
- Document/report titles in italics with a citation ("IEA's *Energy and AI* report")
- Proper nouns that are government initiative names ("East Data, West Computing")
- Direct quotes in quotation marks with citation
- Domain terminology shared across all papers in the field

**What counts as a real risk** (requires rewriting):
- 8+ word phrases from a cited paper's body text appearing in your body text
- Any sentence in your Related Work that matches a source abstract near-verbatim
- Paper titles used as descriptive prose (not as citations)

### Step 2 — Manual upload to iThenticate

```
1. Export paper to PDF (references section last)
2. Upload to iThenticate (institutional access required — web portal only)
3. Set "Exclude bibliography" = YES
4. Set "Exclude quotes" = NO (quotes must be attributed)
5. Review similarity report:
   - Blue = quoted text (acceptable if cited)
   - Orange = paraphrase match (review carefully)
   - Red = verbatim match (rewrite unless it is a direct quote)
6. Target: overall < 15%, no single-source > 5%
```

**If you do not have institutional iThenticate access:**
- IEEE Access provides one free similarity check through the editorial system after
  submission — the editor sees the score, not you. A well-written paper predicts
  8–13% similarity; this will pass their threshold.
- Use Copyscape (https://www.copyscape.com) for web content check
- Manual check: paste suspicious sentences into Google in quotes

**Predicted similarity by paper type:**
- Survey / environmental analysis papers: 10–14% (report titles + domain terms)
- Systems / architecture papers: 7–10% (fewer shared proper nouns)
- Papers with Chinese gov policy sections (EDWC, etc.): add ~1–2% from policy names

**Free manual audit workflow:**
```bash
# Step 1: Extract all sentences about prior work
grep -n "et al\.\|proposed\|demonstrate\|achieve\|introduce\|present" paper.md

# Step 2: For each sentence, search Google:
#   "[first 8 words of sentence]"
# If the exact phrase appears in a paper abstract → rephrase

# Step 3: Verify every "AuthorName et al." matches references.bib
grep -n "et al\." paper.md       # list all inline author references
grep "author.*=" references.bib  # list all bib author fields
# Every name used inline must match the first author in the corresponding entry
```
