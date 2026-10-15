# Pre-Delivery Audit Commands (19 Checks)

Run **all 19 checks** before delivering any draft. Checks 1–5, 13–14, and 19 are delivery BLOCKERS.

**Every check below is a grep/script against source text (`paper.md`/`main.tex`/`references.bib`) — none of them read the compiled PDF.** That is a real blind spot, not a hypothetical one: on the 2026-08-21 "Prompt to Loop Engineering" paper, `\IEEEtitleabstractindextext` silently dropped the entire Abstract and Index Terms block on compile (title page jumped straight from the author line to "I. Introduction"), and a separate merge duplicated the whole Acknowledgments/AI-disclosure paragraph — both invisible to every check in this file, both only caught because the user asked to visually check the rendered PDF. Check 19 exists specifically so this class of bug is never delivery-blocking-invisible again.

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

# 19. Compiled-PDF visual verification — DELIVERY BLOCKER for any paper with main.tex [BLOCKER]
# Checks 1-18 only grep source text. They cannot catch a LaTeX macro that
# compiles clean (no errors, no warnings) but silently drops its content, or
# a merge that duplicates a whole section's text. Both happened on a real
# paper and passed every other check.
#
# 1. Run the full compile chain and confirm zero errors / zero undefined refs:
pdflatex -interaction=nonstopmode main.tex && bibtex main && \
  pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex
grep -iE "error|undefined" main.log | grep -v "may have changed"   # must be empty
grep -c "??" main.log                                              # must be 0
#
# 2. Read the actual rendered main.pdf (Read tool on the PDF file, or render page
#    images) — do not skip this because the compile log is clean. At minimum verify:
#    - Abstract and Index Terms/Keywords are actually visible on page 1 (not just
#      present in main.tex source — confirm they render)
#    - Acknowledgments / AI-disclosure paragraph appears exactly once, not duplicated
#    - Author block, title, and section headers show the intended colors (Rule Q)
#    - Page count matches what was reported to the user
# Fix: if a macro (e.g., \IEEEtitleabstractindextext) drops its content silently,
# switch to the standard `\begin{abstract}`/`\begin{IEEEkeywords}` environments per
# references/visual-design.md's tested pattern — do not debug the broken macro further,
# just use the documented-working one.
#
# 3. Comment-swallowed prose (added 2026-10-11, HACOF revision of the AI-governance
#    paper). Agents tag citations with trailing `% CLAIM: ...` comments for the
#    Fact-Checker. A scripted string replacement that ends just before such a comment
#    left the NEXT sentence on the same line as the comment, so LaTeX treated it as part
#    of the comment and dropped it. The compile was clean, and only a PDF text search
#    found it. Rules: every `% ...` comment must END its line, and prose always starts
#    on a new line. Also never leave a blank line inside a sentence after a comment
#    (it creates a \par mid-sentence). Detect both mechanically:
#      python3 -c "import re;[print(i,l[:120]) for i,l in enumerate(open('main.tex'),1) if re.search(r'(?<!\\\\)%.*(\\\\cite|\\\\ref|\\\\textbf|---)',l)]"
#      mutool draw -F txt main.pdf > /tmp/pdf.txt   # then grep 3-4 distinctive sentences
#    and strip or relocate CLAIM comments before final delivery if any doubt remains.
#
# 4. Rendering pages when the Read tool cannot open the PDF (pdftoppm missing):
#      mutool draw -r 80 -o /tmp/png/p%d.png main.pdf 1,5,13   # then Read the PNGs
#    Also check: the keywords mdframed box is not split across columns (add
#    `nobreak=true`), and long bibliography URLs do not run into the other column
#    (`\usepackage{xurl}` after `\usepackage{url}`).
#
# 5. Waiting on a slow (e.g. /mnt/d on WSL) background build: NEVER use
#      until ! pgrep -f 'pdflatex|bibtex' ...
#    `pgrep -f` matches the waiting shell's own command line, so the loop never
#    exits (2026-10-12: three such waiters sat for hours). Use exact process names:
#      while pgrep -x pdflatex >/dev/null || pgrep -x bibtex >/dev/null; do sleep 5; done
#    And do not edit main.tex while a build is running — rebuild after the edit.
#
# 6. Author biography and AI disclosure (added 2026-10-15; see SKILL.md
#    "Author Biography Rules"):
#      grep -c "begin{IEEEbiography}" main.tex     # >=1 for journals with bios;
#                                                  # MUST be 0 if \author{} says "Anonymous"
#      ls author.jpg                               # photo is in THIS paper's folder
#      python3 -c "import re;b=re.findall(r'begin\{IEEEbiography\}.*?end\{IEEEbiography\}',open('main.tex').read(),re.S);print([x for x in b if '@' in x] or 'OK: no email in bio')"
#      mutool draw -F txt main.pdf | grep -c "<last sentence of the bio>"   # must be 1
#      grep -n "\[author-email\]\|\[Your" main.tex                         # must be empty
#    Then view the last page as an image to confirm the photo renders.
#    Disclosure: grep the Acknowledgments of main.tex AND paper.md for the
#    wording the author chose. A word hyphenated across a PDF line break
#    ("AI-" / "LLM") makes a PDF text grep return 0 even when the text is
#    correct, so check the source or grep for one half of the word.
#    Pre-existing build blockers: an unused `\usepackage{algorithmic}` or
#    `{algorithm}` fails on Debian TeX Live. If `grep -c "begin{algorithm"` is
#    0, delete those lines; a paper folder without IEEEtran.cls/.bst needs them
#    copied in from a sibling paper.

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
