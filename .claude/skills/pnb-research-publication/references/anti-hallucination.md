# Anti-Hallucination Protocol for Research Papers

## Why This Matters

In a research paper, a hallucinated statistic is not just a quality issue — it is
academic fraud. A fake benchmark number or fabricated citation can be detected by
any reviewer who checks the primary source. It will result in immediate rejection,
and if published, retraction.

The Fact-Checker Agent enforces this file on every draft before delivery.

---

## Conceptual / Proposed Architecture Papers (Variant D)

For papers with no empirical experiments, the anti-hallucination rules are the same
but the boundary between "your claim" and "cited claim" differs:

| Claim type | Citation required? |
|---|---|
| Your own architectural design choices | NO — this is your contribution |
| Your own equations and formulas | NO — this is your contribution |
| Performance numbers about PRIOR systems | YES — cite the primary source |
| Comparative claims about prior systems | YES — e.g., "AIOS achieves 2.1× speedup [N]" |
| General background facts about LLMs | YES — cite a foundational paper |
| Claims about industry adoption or standards | YES — cite official source |

**Common mistake in conceptual papers:**
Inventing a performance number as a "design target" and presenting it as a fact.
```
WRONG: "Our scheduler reduces latency by 40%."
       (You have no implementation — this number is fabricated)

RIGHT: "We expect the scheduler to reduce latency in proportion to agent count,
        consistent with the 2.1× throughput gain observed in AIOS [N] under
        similar scheduling conditions."
```

If no implementation exists: state this honestly in Section VI Limitations.
Write "We propose" and "we expect" — not "we achieve" and "our system reduces."

---

## Category 1: Hallucinated Statistics (Hard Block)

### What counts as a hallucinated statistic:
- Any percentage, accuracy number, F1 score, BLEU score, or metric value with no citation
- Any claim like "X% of researchers use..." without a cited survey
- Any market size, growth rate, or adoption figure without a cited industry report
- Any "X times faster" or "X% improvement" claim not directly from your own experiments

### Detection rule:
Every number in the paper must satisfy one of:
1. It comes from your own experiments (reported in your Experiments/Results section)
2. It has an inline `[N]` citation pointing to a peer-reviewed primary source

```bash
# Audit command — find numbers without nearby citations
# Run on your paper.md before submission
grep -n "[0-9]\+\(\.[0-9]\+\)\?%" paper.md | grep -v "\[" | head -20
# Any line with a percentage and no [N] near it = potential hallucination
```

### Hard rules:
- **Never copy a number from memory.** Look it up in the original paper.
- **Never round benchmark numbers.** 94.2% ≠ 94% — the exact number matters.
- **Never cite a blog post for a benchmark number.** Cite the original paper.
- **Never use "approximately X%" without citing the source of the approximation.**

### Common hallucination patterns in CS/AI papers:

| Hallucination Type | Example | Fix |
|---|---|---|
| Benchmark without source | "ResNet-50 achieves 76% top-1 accuracy" (no cite) | Add `\cite{he2016resnet}` |
| Market figure without source | "The AI market is worth $200B" (no cite) | Cite the analyst report or remove |
| Performance claim about baselines | "BERT achieves 88.5 on GLUE" (no cite) | Cite the BERT paper |
| "Recent studies show X%" (no cite) | "Recent studies show 73% adoption rate" | Cite the study or remove |
| Comparative claim | "Our method is 3× faster than Baseline A" | Only from YOUR experiments |

---

## Category 2: Fabricated or Placeholder Citations (Delivery Blocker)

### Zero tolerance policy:
Any of these patterns in the delivered paper = **immediate delivery block**:

```
arXiv:XXXX.XXXXX         ← placeholder arXiv ID
arXiv:2024.XXXXX         ← partial arXiv ID
[CITE NEEDED]            ← unresolved placeholder
[N] A. Author, "TBD"     ← incomplete reference
doi: 10.XXXX/XXXXXXX     ← placeholder DOI
```

### Verification protocol (Literature Agent must do this):

```
For every arXiv citation:
  → Verify at https://arxiv.org/abs/XXXX.XXXXX
  → Paper title and authors must match what you're citing
  → If you can't verify: use Option A/B/C below

Option A: Find a different real paper that supports the same claim
Option B: Remove the claim entirely if not load-bearing
Option C: Describe as "unpublished work" only if you are certain it exists
```

### How to find real arXiv IDs:
- Search Semantic Scholar: `https://api.semanticscholar.org/graph/v1/paper/search?query=...`
- Search arXiv directly: `https://arxiv.org/search/?searchtype=all&query=...`
- Search Google Scholar for the paper title

---

## Category 3: Unverifiable Claims About Prior Work

### The problem:
It is easy to misremember what a cited paper actually claimed.
Example: Citing paper [3] as showing "X achieves 95% accuracy" when it actually shows 89%.

### Rule: Every claim about prior work must be verified against the actual paper.

```
WRONG: "Smith et al. [3] demonstrate that their method achieves 95% accuracy."
       (if you haven't actually checked the number)

RIGHT: Check the paper, then write the exact number with the citation:
       "Smith et al. [3] report 89.3% top-1 accuracy on ImageNet."
```

### Claims that frequently get hallucinated:
- The exact dataset split sizes of a benchmark
- The number of parameters in a baseline model
- The training time of a baseline
- The year a dataset was introduced
- The institution that proposed a method

**Rule**: If you are not certain, write `[Unverified: check primary source]` and resolve before delivery.

---

## Category 4: Your Own Experimental Claims

### Never fabricate or round your own results.

```
WRONG: "Our method achieves approximately 94% accuracy."
       (if the actual number was 93.7%)

RIGHT: "Our method achieves 93.7% accuracy on the test set."
```

### Ablation study integrity:
- Never report an ablation you did not actually run
- If compute was limited, state this: "Due to compute constraints, we report results on a 10% subset"
- Statistical significance: if you ran only one seed, say so — don't imply stability

---

## Fact-Checker Anti-Hallucination Protocol

The Fact-Checker Agent must run these checks on every section:

### For each number in the paper:
```
Is this number from our experiments?
  → YES: verify it matches the results table exactly
  → NO: does it have a [N] citation?
      → YES: does the citation reference the correct paper for this number?
             (not a blog about the paper, but the original paper)
      → NO: BLOCKED — hallucinated stat
```

### For each arXiv citation:
```
Does arXiv:XXXX.XXXXX resolve at arxiv.org/abs/XXXX.XXXXX?
  → YES: title and authors match what we're citing? → VERIFIED
  → NO: BLOCKED — placeholder or fabricated ID
```

### For each claim about baseline performance:
```
Does the cited paper actually report this exact number?
  → YES: on the same dataset and split? → VERIFIED
  → NO: flag as [Unverified: number not found in cited paper]
```

---

## Pre-Submission Audit

```bash
# 1. Find all numbers — check each has a citation
grep -n "[0-9]\+\.[0-9]\+" paper.md

# 2. Find placeholder citations
grep -n "XXXX\|CITE NEEDED\|TBD\|Unverified" paper.md

# 3. Find all arXiv IDs for manual verification
grep -n "arXiv:[0-9]" paper.md

# 4. Cross-check results table vs. text claims
# Every number mentioned in text must match the table exactly
```

All three commands must return **zero matches** before submission.

---

## Category 5: Cross-Section Factual Consistency

Any enumerated factual list in the abstract (e.g., sponsors, partners, system components) must exactly match every corresponding list in the body. If the body names 6 sponsors, the abstract must name all 6 or use a tested quantifier ("six sponsors, including X and Y"). Mismatched counts between abstract and body are a hallucination by omission — the abstract implicitly claims the short list is complete.

**Audit command:**
```bash
# Find list-like enumerations — compare abstract vs body manually
grep -n "sponsored by\|supported by\|partnered with\|including.*and\b" paper.md | head -10
# Every such line must list the same entities. If counts differ, it is a violation.
```

---

## Category 6: External Event and Product Attribution Claims

### 6a — Event Attribution Claims
Claims that attribute a specific announcement, launch, or disclosure to a named venue ("announced at GTC 2026", "unveiled at WWDC", "released at NeurIPS 2024") are external factual claims requiring a citation. The event name alone is not evidence. Acceptable citation types: official press release URL, official event proceedings page, or verifiable news wire source. If no citation can be provided, rewrite as a general statement without the event attribution.

**Audit command:**
```bash
grep -in "announced at\|unveiled at\|released at\|presented at\|demonstrated at\|revealed at" paper.md | grep -v "\["
# Any match with no [N] on the same line = uncited event claim
```

### 6b — Named Third-Party Product Attribution
Naming a specific product, framework, or SDK owned by a third party (e.g., "NVIDIA's OpenShell sandbox framework") implies that product exists and has the described properties. This is a factual claim requiring a citation to the product's official documentation, announcement page, or technical whitepaper. If the product cannot be verified with a citable source, the specific product name must be removed and replaced with a generic description ("a GPU-vendor sandbox framework").

**Audit command:**
```bash
grep -n "'s [A-Z][a-zA-Z]\+\b" paper.md | grep -v "\["
# Catches patterns like "NVIDIA's OpenShell" or "Google's Gemini" without a citation
```

---

## Category 7: Third-Party Specification Claims

Third-party product specifications — including API rate limits, pricing tiers, hardware consumption figures, storage quotas, and SLA values — are external claims that change over time. They require a citation to the vendor's official documentation, pricing page, or technical spec sheet at the time of writing. Do not cite secondary sources (blog posts, tutorials) for these figures — cite the vendor's primary documentation directly. If the spec cannot be traced to an official primary source, remove the specific figure and describe the property qualitatively.

This applies equally to hardware manufacturer specs: power consumption, memory bandwidth, storage I/O, and clock speed figures must be cited to the manufacturer's official product page or datasheet. "Approximately X watts" is not a qualifier that waives the citation requirement.

### 7a — Consumer vs. Data Center GPU Pages Are Different Citations

An NVIDIA consumer GPU (RTX series) and a data center GPU (H100, A100) live on
separate product pages and must use separate BibTeX keys. Do not cite the RTX 4090
consumer page as evidence for H100 TDP, or vice versa.

| Product | Correct citation target |
|---|---|
| NVIDIA H100 SXM5 (700W) | nvidia.com/en-us/data-center/h100/ |
| NVIDIA A100 SXM4 (400W) | nvidia.com/en-us/data-center/a100/ |
| NVIDIA RTX 4090 (450W) | nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/ |

### 7b — Vendor Specs With No Primary Datasheet → Qualitative Only

Some hardware vendors — particularly for AI chips manufactured under export-controlled
conditions — publish no official product datasheet. When no primary source exists:

1. Do NOT use secondary tech blog figures (e.g., "approximately X watts — Unite.AI")
2. Do NOT cite a secondary source as if it were a primary specification
3. REMOVE the specific watt figure entirely
4. Replace with qualitative language: "at a lower thermal footprint than the H100's
   700-watt ceiling [cite NVIDIA]" or "at materially reduced power draw"

**Known cases (as of mid-2026) with no official primary datasheet:**
- Huawei Ascend 910C — secondary sources cite ~310W; Huawei has published no spec sheet
- Huawei Ascend 910B — ~400W cited in press; no official datasheet URL available
- Any Chinese AI chip where "specifications" appear only in news articles or analyst reports

### 7c — Institutional Projection Claims Need Primary Source From That Institution

A claim attributed to a specific body ("OPEC projects X", "the UN says Y") must come
from a document that body actually published — not from news reporting about it.

**Verification protocol:**
1. Identify the institution (e.g., OPEC, IEA, World Bank, UN, NDRC)
2. Navigate to that institution's official publications page
3. Confirm the specific figure (percentage, projection year, multiplier) appears
   in a primary document from that institution — not in a news article that paraphrases them
4. If the figure cannot be located in a primary document: **do not use it**
5. Offer the user a verified alternative from a different primary source

**Why this matters:** OPEC publishes World Oil Outlooks. IEA publishes energy reports.
These documents may or may not contain specific AI/data center projections. A news
article saying "OPEC projects AI will consume 8% of global electricity by 2050" does not
mean OPEC's document says this — it may be a journalist's extrapolation. Using it as a
cited fact from OPEC constitutes misattribution, even if the underlying concern is valid.

**Verified alternatives when institutional primary source is not findable:**
- IEA World Energy Outlook (authoritative, fully public): iea.org/reports/world-energy-outlook
- Lawrence Berkeley National Laboratory data center reports: eta-publications.lbl.gov
- IRENA energy reports: irena.org/publications
- These are primary sources with citable PDFs and verified page numbers.

**Audit commands:**
```bash
# Third-party product specs without citation
grep -n "requests/minute\|requests/day\|rate limit\|free tier\|per month\b\|GB/s\|TB/month" paper.md | grep -v "\["

# Hardware spec ranges without citation
grep -n "[0-9]\+[–-][0-9]\+W\|[0-9]\+ watts\|[0-9]\+W\b\|[0-9]\+ GHz\|[0-9]\+ MB RAM" paper.md | grep -v "\["
```

---

## Category 8: Code Block Factual Claims

A factual claim does not become uncitable by being placed inside a code block, bash comment, or YAML value. Price figures (`~$5/month`), version numbers presented as current (`v3.2`), and specification claims inside code comments are all published claims in the final PDF.

**Rule:** Either (a) add a prose sentence with a citation adjacent to the code block, or (b) remove the specific figure from the code and use a placeholder or generic descriptor.

```bash
# Wrong — uncited price in a code comment:
# On a fresh Ubuntu 22.04 VPS (Hetzner CX11 at ~$5/month is well-suited)

# Correct — generic descriptor:
# On a fresh Ubuntu 22.04 VPS (Hetzner CX11 or equivalent budget provider)
```

**Audit command:**
```bash
grep -n "\$[0-9]\|~\\\$\|per month\|/month\|/year" paper.md
# Inspect each match — if inside a code block (``` or indented), verify there is
# a cited prose sentence nearby or remove the specific figure.
```

---

## Category 10: Mathematical Bound Primary Source (Rule L)

When a formula, regret bound, or theorem is cited, the citation must point to the paper that **proved or established** the result — not a paper that uses the result in a different application.

**The error pattern:**
You write a mathematical bound (e.g., the linear UCB O(√T) regret bound) and cite the most recent paper from your literature search that contains that formula. That paper may cite the actual theorem origin, but it is not the primary source. The reviewer who specialises in that area will immediately notice the wrong attribution.

**Classification:**
| Claim type | Correct citation |
|---|---|
| UCB regret bound O(√T) | Auer et al. (2002) or Abbasi-Yadkori et al. (NeurIPS 2011) |
| Transformer attention O(n²) | Vaswani et al. (2017) |
| Graph NP-hardness | Cite the original hardness result |
| Information-theoretic bound | Cite Cover & Thomas or the original derivation |
| A bound from YOUR paper | No citation needed — it is your derivation |

**Detection:**
For every `\begin{equation}` block with a `\cite{}` nearby: ask "Did this paper prove this result, or did it use this result?" If the latter — find and cite the paper that proved it.

**Audit:**
```bash
# Find all equations — check each has the right citation
grep -n "\\\\begin{equation}" main.tex
# For each: read the surrounding text and verify the cited paper is the primary source
```

---

## Category 11: Derived Estimate Attribution (Rule N)

A value derived by applying a formula you wrote in the paper is a *derived estimate* — it is not extracted from any source. Citing a paper as if it states your derived range is misattribution.

**The error pattern:**
You describe a mathematical relationship (e.g., variance falls as σ²/S for shot count S), then compute a range from that relationship (e.g., 30–70% shot reduction), then cite a general survey paper as the source of that range. The survey does not state that range. You derived it.

**Correct treatment:**
```
WRONG: "the total shot reduction falls in the 30–70% range~\cite{cerezo2021vqa}"
       (cerezo2021vqa does not state this range)

RIGHT: "the total shot reduction falls in the 30–70% range---derived from the
        σ²/S scaling applied to typical VQA gradient norm ratios; see [N] for the
        underlying variance framework"
```

**Detection:**
For every percentage range in the paper: ask "Did I read this range in a paper, or did I compute it?" If computed — label it as derived. If read — cite the exact paper and section.

---

## Category 12: BibTeX Author List Completeness (Rule M)

`and others` in a BibTeX author field means the author list was not retrieved — it is a placeholder. IEEE formats this as "et al." in the reference list, which is acceptable in *prose* but not as a BibTeX value where you are required to list all authors.

**Why this matters:** A reviewer who checks a paper and finds only 1 author listed ("Xu, Qing and others") when there are actually 9 authors will flag the bibliography as carelessly assembled.

**Rule:** Every `@article`, `@inproceedings`, and `@misc` entry must list all authors explicitly. For papers with >8 authors, IEEE style allows "First Author et al." in prose citations, but the BibTeX entry must still contain all authors so the bibliography manager can format correctly.

**Retrieval protocol:**
- arXiv paper: `https://arxiv.org/abs/XXXX.XXXXX` → read the full author list from the title page
- Published journal: check the DOI landing page
- Conference proceedings: check the ACM DL or IEEE Xplore entry

**Audit:**
```bash
grep -n "and others" references.bib   # Must return zero before delivery
```

---

## Category 9: BibTeX Venue Consistency

The reference list in `paper.md` and the corresponding entries in `references.bib` must agree on venue type and format. Venue type is a factual claim — presenting a preprint as a peer-reviewed conference paper is academic misrepresentation.

- If paper.md lists a paper as an arXiv preprint → `.bib` entry must use `@misc` or `@article` with `archivePrefix = {arXiv}`
- If paper.md lists a conference venue (NeurIPS, ICLR) → `.bib` entry must use `@inproceedings` with the correct `booktitle`
- The compiled LaTeX PDF derives citation format from `.bib` — a mismatch means the PDF shows a different citation format than paper.md

**Audit command:**
```bash
# Find arXiv IDs listed in paper.md reference section
grep -n "arXiv:" paper.md | tail -30

# Find conference entries in .bib
grep "booktitle\|archivePrefix" references.bib

# Every arXiv ID in paper.md should have a matching archivePrefix entry in .bib
# Every conference in paper.md should have a booktitle entry in .bib
```
