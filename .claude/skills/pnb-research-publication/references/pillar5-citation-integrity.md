# Pillar 5 — Fact & Citation Integrity

Every factual claim in the paper must trace to a verifiable source. This pillar
covers the mechanics of citation hygiene — author names, DOIs, URLs, BibTeX
completeness — as distinct from Pillar 1 (which covers hallucinated statistics and
fabricated arXiv IDs) and Pillar 2 (which covers plagiarism from sources).

The detailed hallucination deduction checklist for external event claims,
product attribution, third-party specs, BibTeX venue consistency, Rule L (theorem
primary source), Rule M (author list completeness), and Rule N (derived estimate
attribution) lives in `references/anti-hallucination.md` (Categories 6–12). This
file covers the citation workflow and verification protocol.

---

## Category 1 — Author Name Accuracy

Every "Author et al." or "Author and Author" inline citation must match the BibTeX
`author` field.

**Verification protocol:**
1. For each citation in the body, find its `.bib` key.
2. Read the `author` field in the `.bib` entry.
3. Confirm the first-listed surname matches what is written inline.
4. Check for common failures:
   - Chinese/Korean/Japanese names that Western databases list surname-first vs. given-first
   - Hyphenated surnames partially cited (e.g., "García-López" cited as "García")
   - Co-first-author papers where the wrong author is listed first

```bash
# Extract all inline et-al citations for manual cross-check
grep -o '[A-Z][a-z]\+ et al\.' paper.md | sort -u
# For each name: find its .bib key, verify the first author surname matches
```

**Deduction trigger**: −5 per wrong author name cited inline.

---

## Category 2 — DOI and URL Liveness

Every DOI and URL cited in `references.bib` must resolve at time of writing.

**Verification protocol:**
```bash
# Extract all DOIs from .bib
grep -o 'doi = {[^}]*}' references.bib | sed 's/doi = {//;s/}//'
# For each DOI: confirm https://doi.org/[DOI] resolves to the correct paper

# Extract all URLs from .bib
grep -o 'url = {[^}]*}' references.bib | sed 's/url = {//;s/}//'
# For each URL: confirm the page is accessible and matches the cited work
```

**Common failure modes:**
- arXiv IDs that were later retracted or updated to different version
- GitHub repository URLs for archived or deleted repos
- Vendor documentation URLs reorganized after product updates
- Preprint URLs where the journal version has a different DOI

**Fix**: Add `note = {Accessed: YYYY-MM-DD}` for URL citations. If a URL is dead,
locate the archived version (Wayback Machine) or replace with the canonical DOI.

---

## Category 3 — arXiv ID Verification

Every arXiv ID in `references.bib` must be verified at `https://arxiv.org/abs/ID`.

```bash
# Extract all arXiv IDs
grep -o 'arXiv:[0-9]\{4\}\.[0-9]\{4,5\}' references.bib
# For each ID: confirm the title and authors match what is cited in the paper
```

**Verification steps:**
1. Navigate to `arxiv.org/abs/[ID]`
2. Confirm: title matches, first author matches, year matches
3. If the arXiv paper has been published in a venue: update the `.bib` entry to
   `@inproceedings` or `@article` with the correct venue and DOI

**Deduction trigger**: −10 per unverified arXiv ID (delivery blocker).

---

## Category 4 — Zero Placeholder Citations

No paper may be delivered with:
- `arXiv:XXXX.XXXXX` (placeholder ID)
- `[CITE NEEDED]`
- `[Unverified]`
- `TODO: find citation`
- Empty `url = {}` or `doi = {}` fields that reference a source that does have one

```bash
grep -n "XXXX\|CITE NEEDED\|Unverified\|TODO.*cit" paper.md references.bib
# Must return zero — delivery blocker
```

---

## Category 5 — BibTeX Completeness

### Author Lists
`and others` must never appear in any BibTeX author field.

```bash
grep -n "and others" references.bib   # Must return zero
```

**Fix**: Navigate to `https://arxiv.org/abs/ID` or the publisher's title page. List
every author in `Surname, Given and Surname, Given and ...` format.

### Entry Type Matching
The BibTeX entry type must match how the source appears in the paper body:

| Source type | Correct entry type |
|---|---|
| arXiv preprint (not yet published) | `@misc` with `archivePrefix = {arXiv}` |
| arXiv preprint published at venue | `@inproceedings` or `@article` with venue info |
| Conference paper | `@inproceedings` with correct `booktitle` |
| Journal article | `@article` with `journal`, `volume`, `number` |
| Book chapter | `@inbook` or `@incollection` |
| Technical report | `@techreport` |
| Webpage / official docs | `@misc` with `url` and `note = {Accessed: ...}` |

A type mismatch between `.bib` and `paper.md` is a IEEE style violation — the PDF
will show a different format than the review copy.

---

## Category 6 — Multi-Source Statistics

When a factual statistic appears in more than one source document, cite ALL sources
that directly support it — not only the most convenient one.

**Scenario**: A deployment adoption figure that appears in three survey papers.
Citing only one implies only one source supports it, which is partial attribution
and can be challenged in review.

**Rule**: If two or more sources independently state the same fact, cite both:
`[N, M]` format.

---

## Category 7 — Derived Estimates vs. Source Claims

This overlaps with Rule N in `references/writing-rules.md`. A range you computed by
applying a formula from a source is a **derived value** — the source does not state
your specific range. Citing the source as if it states the range is misattribution.

**Incorrect pattern:**
> "...yields a 30–70% reduction~\cite{someformula2021}"

**Correct pattern:**
> "...yields a 30–70% reduction — derived from the σ²/S scaling applied to our
> experimental gradient norm ratios; see [N] for the underlying framework."

---

## Pre-Delivery Citation Integrity Checklist

Run before every draft delivery:

- [ ] All inline "Author et al." names cross-checked vs. BibTeX `author` fields
- [ ] All DOIs verified live on publisher site
- [ ] All URLs verified accessible
- [ ] All arXiv IDs verified at arxiv.org/abs/[ID]
- [ ] Zero `[CITE NEEDED]`, `[Unverified]`, `XXXX` patterns in paper.md
- [ ] Zero `and others` in references.bib
- [ ] BibTeX entry types match paper.md display format
- [ ] Multi-source statistics cite all supporting sources
- [ ] Derived estimates labeled as derived (not attributed to source)
- [ ] Orphan check: every `.bib` key is cited at least once in main.tex body

For deduction scales for citation integrity failures, see `references/grade-paper.md`
(Category 4 — Fact & Citation Integrity, 15% weight).
