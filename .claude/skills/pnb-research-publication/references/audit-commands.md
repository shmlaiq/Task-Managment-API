# Pre-Delivery Audit Commands (17 Checks)

Run **all 17 checks** before delivering any draft. Checks 1–5 and 13–14 are delivery BLOCKERS.

---

```bash
# 1. Hallucination — placeholder arXiv IDs and unverified claims [BLOCKER]
grep -n "XXXX\|CITE NEEDED\|Unverified" paper.md        # must return zero

# 2. Hallucination / Fact — percentages without citations [BLOCKER]
grep -n "[0-9]\+%" paper.md | grep -v "\["              # must return zero

# 3. Plagiarism — author name check
grep -n "et al\." paper.md   # verify each name matches references.bib

# 4. Anti-AI — banned phrases [BLOCKER]
grep -in "worth noting\|it should be noted\|significantly improves\|state-of-the-art performance\|in recent years.*has\|revolutionized\|proliferation\|leverage" paper.md
# Must return zero matches

# 5. Rule C — incomplete escalation paths [BLOCKER]
grep -in "not fully specified\|not yet specified\|remains unspecified\|left for future work\|\bTBD\b" paper.md
# Must return zero matches

# 6. Citation completeness — every .bib key must appear in main.tex body [BLOCKER]
# Use the Python version — the bash comm version fails on multi-key \cite{a,b,c} calls
python3 -c "
import re
with open('references.bib') as f:
    keys = re.findall(r'@\w+\{(\w+),', f.read())
with open('main.aux') as f:
    cited = re.findall(r'\\\\citation\{([^}]+)\}', f.read())
cited_flat = set()
for c in cited:
    for k in c.split(','):
        cited_flat.add(k.strip())
orphans = [k for k in keys if k not in cited_flat]
print('Orphaned:', orphans or 'NONE')
print(f'Total: {len(keys)} refs, {len(cited_flat)} cited')
"
# Must print "Orphaned: NONE". Requires main.aux — run pdflatex once first.
# NOTE: main.aux is only current after the most recent pdflatex run.

# 7. paper.md ↔ main.tex sync — spot-check 3 key paragraphs
# Pick one sentence from Abstract, one from Architecture, one from Conclusion.
# Verify same content (same facts/numbers) exists in both files.

# 8. Rule I — external event claims (named events without citations)
grep -n "announced at\|introduced at\|presented at\|launched at\|revealed at\|debuted at" paper.md
# Each match must have a [N] citation — if not, it is an uncited event claim

# 9. Rule I — third-party product attribution (named products with feature claims)
grep -in "NVIDIA's\|Google's\|OpenAI's\|Microsoft's\|Meta's\|Anthropic's" paper.md | grep -v "\["
# Any match without [N] after it is an uncited product feature claim — cite or rewrite

# 10. Rule J — abstract acronym check (non-standard acronyms not expanded)
# Read the Abstract section. Verify every non-standard acronym: "Full Name (ABBR)"
# Standard exemptions: AI, ML, OS, API, CPU, GPU, RAM, URL, HTTP
# Non-exempt (must expand): LLM, MCP, RAG, HITL, ACP, VPS, QMD, WSL, K3s, CoT

# 11. Rule J — abstract ending check (must end on significance, not limitations)
# Read the final sentence of the Abstract. Does it state contribution/impact?
# If it describes a constraint, gap, or "future work" — deduction trigger. Rewrite.

# 12. Abstract word count — must not exceed venue limit
awk '/^## Abstract/{p=1} p && /^## /{if(!/^## Abstract/)p=0} p' paper.md | wc -w
# IEEE Access: 250 words. IEEE Transactions: 250 words. Conference: 150 words.

# 13. Acknowledgments section — BLOCKER if missing for IEEE submissions [BLOCKER]
grep -n "Acknowledgments\|Acknowledgements" paper.md
# Must return at least one match

# 14. Figure placeholders — DELIVERY BLOCKER [BLOCKER]
grep -n "figplaceholder\|INSERT.*figure\|figure.*TODO\|placeholder.*figure" main.tex
# Must return zero — fix: replace with TikZ code from references/figures-design.md

# 15. Rule M — truncated BibTeX author lists [BLOCKER]
grep -n "and others" references.bib
# Must return zero — fetch arxiv.org/abs/ID or publisher page and list all authors

# 16. Rule O — abstract-body phrase echo (spot check, 3 phrases)
# Pick 3 distinctive phrases (5+ words) from abstract. For each:
#   grep -n "EXACT_PHRASE" main.tex
# Must return at most ONE hit per phrase (the abstract itself).

# 17. Rule N — derived estimate attribution check
grep -n "[0-9][0-9]*--[0-9][0-9]*\\\\%" main.tex
# For EACH match: (a) verify citation exists, AND (b) that citation actually states
# this range. If derived from a formula — label as derived, not attributed to source.
```

---

---

# 18. Hardware spec citations — Category 7 enforcement [BLOCKER]
# Every watt/GHz/GB/TB figure for a named chip or device requires a citation
grep -n "[0-9]\+-[0-9]\+W\|[0-9]\+ watt\|[0-9]\+W\b\|[0-9]\+ GHz\|[0-9]\+ TFLOP" paper.md | grep -v "\["
# Any match without a nearby [N] = uncited hardware spec = Category 7 violation
# Fix: cite the manufacturer's official product/datasheet page, OR
#      rewrite to qualitative language if no primary datasheet exists.
#
# KNOWN PRIMARY SOURCE GAPS (no official datasheet publicly available):
#   - Huawei Ascend 910C/910B TDP → no Huawei primary datasheet; secondary sources
#     cite ~310W for 910C. If you must mention it: qualitative only.
#   - Any Chinese AI chip with "approximately X watts" and no vendor link → remove number.
#
# CONFIRMED CITABLE NVIDIA SPECS:
#   - H100 SXM5: up to 700W → https://www.nvidia.com/en-us/data-center/h100/
#   - RTX 4090: 450W TDP   → https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/
#   - A100 SXM4: 400W      → https://www.nvidia.com/en-us/data-center/a100/
#   Use separate BibTeX keys per product page — do not cite consumer page for data center card.

---

## Fix Actions

| Check | Typical Fix |
|---|---|
| #1 — placeholders | Complete the citation or remove the claim |
| #2 — uncited % | Add `[N]` citation or express as ratio/multiplier |
| #4 — banned phrase | Replace with specific, concrete alternative |
| #6 — uncited .bib key | Give natural inline citation OR remove from .bib |
| #14 — placeholder figure | Replace with TikZ code using templates in `references/figures-design.md` |
| #15 — truncated authors | Fetch title page; write complete author list |
