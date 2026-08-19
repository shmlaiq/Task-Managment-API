# Visual Design Standard for IEEE Research Papers

## Mandatory Rule (Rule Q) — Every Paper Must Be Colorful and Attractive

A delivered paper is not complete if it looks like a plain black-and-white draft.
Every paper must apply the full visual design standard below from the first draft.
This is not optional polish — it is a delivery requirement on the same level as
Rule K (no figplaceholders).

**Before delivering any draft, confirm all visual checks pass:**
- [ ] Title is colored (not black default)
- [ ] Author block is styled (color + italic)
- [ ] Abstract has a colored border box
- [ ] Index Terms have a styled box
- [ ] All figures use resource-coded color schemes (not monochrome)
- [ ] Heatmaps use diverging color scale (not all-blue)
- [ ] Section headings are colored (IEEEtran default is blue — verify it renders)

---

## Page 1 Visual Template (IEEE Journal — `[journal]{IEEEtran}`)

This is the exact, tested implementation that produces an attractive first page
without breaking IEEEtran's two-column layout.

### Required Packages

Add to preamble (after `\usepackage{float}`):

```latex
\usepackage{mdframed}
```

### Required Color Definitions

```latex
\definecolor{darkblue}{RGB}{0,0,139}
\definecolor{midgreen}{RGB}{34,139,34}
\definecolor{deepred}{RGB}{180,0,0}
\definecolor{steelblue}{RGB}{52,102,153}
\definecolor{tealcolor}{RGB}{0,110,110}
\definecolor{ambercolor}{RGB}{204,102,0}
\definecolor{slateblue}{RGB}{90,80,160}
```

### Suppress IEEEtran's Plain Abstract/Keywords Labels

IEEEtran hardcodes `\textit{\abstractname}---` and `\textit{\IEEEkeywordsname}---`
in the abstract and keywords environments (line 5277 of IEEEtran.cls). These
cannot be removed by `\renewcommand{\abstractname}{}` alone — the `---` is
hardcoded. Use `\makeatletter` to replace the entire definition:

```latex
\makeatletter
\def\abstract{\normalfont
    \if@twocolumn
      \relax  % suppress hardcoded label — we add our own inside the mdframed box
    \else
      \bgroup\par\addvspace{0.5\baselineskip}\centering\vspace{-1.78ex}%
      \@IEEEabskeysecsize\textbf{\abstractname}%
      \par\addvspace{0.5\baselineskip}\egroup\quotation\@IEEEabskeysecsize
    \fi\@IEEEgobbleleadPARNLSP}
\def\IEEEkeywords{\normalfont
    \if@twocolumn
      \relax  % suppress hardcoded label — we add our own inside the mdframed box
    \else
      \bgroup\par\addvspace{0.5\baselineskip}\centering\@IEEEabskeysecsize%
      \textbf{\IEEEkeywordsname}%
      \par\addvspace{0.5\baselineskip}\egroup\quotation\@IEEEabskeysecsize
    \fi\@IEEEgobbleleadPARNLSP}
\makeatother
```

Place this block in the preamble, BEFORE `\begin{document}`.

### Colored Title

```latex
\title{\textcolor{darkblue}{Your Paper Title Here}}
```

`\textcolor` works correctly inside IEEEtran's `\title{}` in journal mode.

### Styled Author Block (italic, dark purple)

```latex
\author{%
  \IEEEauthorblockN{\textcolor{slateblue}{\itshape Author Name
    \qquad Email:~email@domain.com \qquad
    ORCID:~0000-0000-0000-0000}}%
}
```

`slateblue` is defined as `RGB{90,80,160}` — dark purple. Use this always.
Never use `midgreen` for the author block.

**Rule**: Never use `\IEEEauthorblockA` without a real institution. If no
affiliation: single `\IEEEauthorblockN` line with `\qquad` separators.

### Colored Abstract Box

Place the mdframed box INSIDE the abstract environment. Never put the abstract
environment inside the mdframed box — that breaks IEEEtran's column handling.

```latex
\begin{abstract}
\begin{mdframed}[
  linecolor=darkblue, linewidth=1.8pt,
  backgroundcolor=darkblue!5,
  innerleftmargin=10pt, innerrightmargin=10pt,
  innertopmargin=9pt, innerbottommargin=9pt,
  roundcorner=5pt, skipabove=0pt, skipbelow=0pt
]
\noindent\textbf{\textcolor{darkblue}{Abstract\,---}}~Your abstract text...
\end{mdframed}
\end{abstract}
```

### Styled Index Terms Box

Place the mdframed box INSIDE the IEEEkeywords environment. Never wrap
the IEEEkeywords environment in an outer mdframed — that breaks spacing.

```latex
\begin{IEEEkeywords}
\begin{mdframed}[
  linecolor=darkblue!35, linewidth=0.8pt,
  backgroundcolor=darkblue!3,
  innerleftmargin=8pt, innerrightmargin=8pt,
  innertopmargin=5pt, innerbottommargin=5pt,
  roundcorner=3pt, skipabove=0pt, skipbelow=4pt
]
\noindent\textbf{\textcolor{darkblue}{Index Terms\,---\,}}keyword1,
keyword2, keyword3
\end{mdframed}
\end{IEEEkeywords}
```

---

## What NOT to Do (Learned from Production Failures)

| Mistake | What Happens | Correct Approach |
|---|---|---|
| `\renewcommand{\abstractname}{}` to suppress the label | `---` still appears (hardcoded in IEEEtran cls) | Use `\makeatletter\def\abstract{...}\makeatother` |
| Wrapping `\begin{abstract}` inside `\begin{mdframed}` | Column-spanning breaks; abstract goes to wrong column | Put mdframed INSIDE `\begin{abstract}` |
| Wrapping `\begin{IEEEkeywords}` inside outer `\begin{mdframed}` | Spacing errors, IEEEkeywords placed in wrong context | Put mdframed INSIDE `\begin{IEEEkeywords}` |
| Putting visual elements between `\maketitle` and `\begin{abstract}` | Content goes into left column only, not spanning | Place decorative content INSIDE the abstract/keywords mdframed, or omit |
| Using `\IEEEspecialpapernotice{...}` with large TikZ content | Entire title block pushed to page 2 (blank page 1) | `\IEEEspecialpapernotice` is for short inline notices only |
| `\hrule` inside `\IEEEspecialpapernotice` | Renders in wrong context | Use `\noindent\rule{\linewidth}{1.5pt}` if needed in column body |

---

## Figure Color Conventions (All Papers)

Apply these colors consistently across ALL figures in the paper:

### Resource-Type Color Coding

When a paper analyzes multiple resource or category types, color-code them
consistently so readers can track each type visually across all figures:

```latex
% Electricity / Energy → amber family
fill=ambercolor!18, draw=ambercolor!80

% Water / Freshwater → cyan family
fill=cyan!15, draw=cyan!60

% Materials / Hardware → green family
fill=midgreen!18, draw=midgreen!60

% Labor / Human → violet/slate family
fill=slateblue!15, draw=slateblue!55
```

Use the SAME color for the same concept in every figure. A reader should be
able to look at Fig. 1 and Fig. 3 and immediately know which element is which.

### Heatmap / Intensity Scale

Never use an all-blue (monochrome) scale for heatmaps. Always use a diverging
heat scale that communicates intensity:

```latex
\def\lo{gray!12}            % Low intensity
\def\md{yellow!55!orange!30}% Moderate
\def\hi{orange!68}          % High
\def\vhi{deepred!75}        % Dominant / Critical
```

Add a legend box showing all four levels. Use `text=white` for the Dominant
cells to ensure readability.

### Taxonomy / Tree Diagrams

Color-code each branch distinctly. Example for 4-branch taxonomy:

```latex
% Branch styles — one per intervention domain
b1s: fill=steelblue!22, draw=steelblue, text=steelblue!80!black
b2s: fill=tealcolor!18, draw=tealcolor, text=tealcolor!80!black
b3s: fill=ambercolor!20, draw=ambercolor, text=ambercolor!80!black
b4s: fill=slateblue!15, draw=slateblue, text=slateblue!80!black
```

Use matching arrow colors per branch (`ar1/.style`, `ar2/.style`, etc.)

### Matrix / Grid Figures

- Phase/column headers: solid darkblue fill, white text
- Use bold shading on the DOMINANT cell, lighter on others
- Add white gridlines between cells (`\draw[white, line width=1.2pt]`)
- Outer border: `\draw[darkblue!50, line width=0.8pt]`

---

## Hyperlink Colors

Always set colored hyperlinks in preamble:

```latex
\hypersetup{colorlinks=true,linkcolor=darkblue,citecolor=darkblue,urlcolor=darkblue}
```

This makes inline `[N]` citations appear in darkblue, reinforcing the paper's
color identity throughout the body.

---

## Visual Design Audit Checklist (Run Before Delivery)

- [ ] Title text uses `\textcolor{darkblue}{...}` or equivalent
- [ ] Author block uses `\textcolor{slateblue}{\itshape ...}` (dark purple)
- [ ] Abstract: mdframed INSIDE `\begin{abstract}`, not wrapping it
- [ ] Abstract label: custom bold colored "Abstract---" inside mdframed box
- [ ] IEEEkeywords: mdframed INSIDE `\begin{IEEEkeywords}`, not wrapping it
- [ ] Keywords label: custom bold colored "Index Terms---" inside mdframed box
- [ ] IEEEtran abstract/keywords labels suppressed via `\makeatletter` redefinition
- [ ] All figures use resource-coded colors (not monochrome)
- [ ] Heatmaps use diverging scale (gray→yellow→orange→red)
- [ ] Taxonomy branches color-coded per domain
- [ ] Matrix figures have colored headers and bold dominant cells
- [ ] `\hypersetup{colorlinks=true,...}` set in preamble
- [ ] Compile clean (zero errors, zero warnings) after all visual changes
- [ ] Render page 1 to PNG and visually verify before delivery

---

## Quick Verification After Build

```bash
# Render page 1 to PNG and inspect
python3 - << 'EOF'
import fitz
doc = fitz.open("main.pdf")
page = doc[0]
mat = fitz.Matrix(4.0, 4.0)
pix = page.get_pixmap(matrix=mat, alpha=False)
pix.save("page1_check.png")
print(f"{pix.width}x{pix.height}")
doc.close()
EOF
```

Open `page1_check.png` and verify:
1. Title is visible in darkblue (not black)
2. Author line is in green italic
3. Abstract box has colored border and light blue fill
4. "Abstract—" appears ONCE only (bold colored, inside the box)
5. Index Terms box is styled
6. No blank page before page 1 (no `\IEEEspecialpapernotice` misuse)
