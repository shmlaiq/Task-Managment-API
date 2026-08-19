# Figures Design for Research Papers

## Core Rule (Rule K)

Every figure in a delivered draft must be a working TikZ/pgfplots diagram inside
main.tex. A `\figplaceholder` shaded box, `[INSERT FIGURE]` text, or any stand-in
is a delivery blocker — not a to-do for "later". Reviewers cannot evaluate a
placeholder. The paper author cannot approve a placeholder.

Create the TikZ figure at the same time you write the section that references it.

---

## Required Preamble (add once per paper)

```latex
\usepackage{tikz}
\usepackage{pgfplots}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,fit,calc,backgrounds}
\pgfplotsset{compat=1.18}
```

Place these after `\usepackage{float}` and before `\begin{document}`.

---

## Color Convention (consistent across all figures)

| Color | Meaning | LaTeX |
|---|---|---|
| `darkblue!80` fill | Top-level / header box | `fill=darkblue!78` |
| `blue!18` fill | Core module boxes | `fill=blue!18` |
| `gray!28` fill | Infrastructure / HAL | `fill=gray!28` |
| `gray!48` fill | Hardware nodes | `fill=gray!48` |
| `orange!14` fill | New / proposed additions | `fill=orange!14` |
| `green!12` fill | Portability / cross-cutting | `fill=green!12` |

`darkblue` must be defined in preamble: `\definecolor{darkblue}{RGB}{0,0,139}`

---

## Figure Type 1 — Taxonomy Tree (3-level hierarchy)

Use for: survey section, Related Work, quantum OS classification.

```latex
\begin{figure}[H]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[
  font=\normalsize,
  rn/.style={rectangle,rounded corners=4pt,draw=darkblue,fill=darkblue!80,
             text=white,minimum width=3.6cm,minimum height=0.7cm,
             align=center,font=\normalsize\bfseries},
  bn/.style={rectangle,rounded corners=3pt,draw=blue!55,fill=blue!20,
             minimum width=2.2cm,minimum height=0.65cm,align=center,
             font=\normalsize\bfseries},
  ln/.style={rectangle,rounded corners=2pt,draw=gray!50,fill=gray!10,
             minimum width=2.0cm,minimum height=0.58cm,align=center},
  ar/.style={-{Stealth[length=4pt]},thick,darkblue!60}
]
% Root node
\node[rn] (root) at (0,0) {Root Category};
% Branch nodes
\node[bn] (b1) at (-3.5,-1.2) {Branch A};
\node[bn] (b2) at (0,-1.2)    {Branch B};
\node[bn] (b3) at (3.5,-1.2)  {Branch C};
% Leaf nodes (2 per branch)
\node[ln] (l1a) at (-4.2,-2.5) {Leaf A1};
\node[ln] (l1b) at (-2.8,-2.5) {Leaf A2};
\node[ln] (l2a) at (-0.6,-2.5) {Leaf B1};
\node[ln] (l2b) at (0.8,-2.5)  {Leaf B2};
\node[ln] (l3a) at (2.8,-2.5)  {Leaf C1};
\node[ln] (l3b) at (4.2,-2.5)  {Leaf C2};
% Edges
\draw[ar] (root)--(b1); \draw[ar] (root)--(b2); \draw[ar] (root)--(b3);
\draw[ar] (b1)--(l1a); \draw[ar] (b1)--(l1b);
\draw[ar] (b2)--(l2a); \draw[ar] (b2)--(l2b);
\draw[ar] (b3)--(l3a); \draw[ar] (b3)--(l3b);
% Optional annotation row below leaves
\node[font=\scriptsize\itshape,gray!65] at (-3.5,-3.1) {Annotation A};
\node[font=\scriptsize\itshape,gray!65] at (0,-3.1)    {Annotation B};
\node[font=\scriptsize\itshape,gray!65] at (3.5,-3.1)  {Annotation C};
\end{tikzpicture}%
}
\caption{Taxonomy of [subject] by [dimension].}
\label{fig:taxonomy}
\end{figure}
```

**Scaling rule:** `\resizebox{\columnwidth}{!}` fits any width naturally. Keep node
`minimum width` values in the 2–4cm range; the resizebox handles the rest.

---

## Figure Type 2 — Architecture Stack (vertical pipeline)

Use for: system architecture sections, Origin Pilot 4-module block diagram.

```latex
\begin{figure}[H]
\centering
\resizebox{0.88\columnwidth}{!}{%
\begin{tikzpicture}[
  font=\normalsize,
  api/.style={rectangle,rounded corners=3pt,draw=darkblue,fill=darkblue!78,
              text=white,minimum width=5.4cm,minimum height=0.65cm,
              align=center,font=\normalsize\bfseries},
  mod/.style={rectangle,rounded corners=3pt,draw=blue!55,fill=blue!18,
              minimum width=2.55cm,minimum height=0.65cm,align=center,
              font=\normalsize\bfseries},
  wide/.style={rectangle,rounded corners=3pt,draw=blue!55,fill=blue!18,
               minimum width=5.4cm,minimum height=0.65cm,align=center,
               font=\normalsize\bfseries},
  hal/.style={rectangle,rounded corners=3pt,draw=gray!58,fill=gray!28,
              minimum width=5.4cm,minimum height=0.65cm,align=center,
              font=\normalsize\bfseries},
  hw/.style={rectangle,rounded corners=3pt,draw=gray!62,fill=gray!48,
             minimum width=1.65cm,minimum height=0.6cm,align=center},
  ar/.style={-{Stealth[length=4pt]},thick,darkblue!55}
]
\node[api]  (api) at (0, 0)      {User API / Interface Layer};
\node[wide] (top) at (0,-0.9)    {Top Module (e.g., Scheduler)};
\node[mod]  (ml)  at (-1.45,-1.8) {Module Left};
\node[mod]  (mr)  at (1.45,-1.8)  {Module Right};
\node[wide] (bot) at (0,-2.7)    {Bottom Module (e.g., Calibration)};
\node[hal]  (hal) at (0,-3.6)    {Hardware Abstraction Layer};
\node[hw]   (h1)  at (-2.1,-4.5) {HW Type 1};
\node[hw]   (h2)  at (0,-4.5)    {HW Type 2};
\node[hw]   (h3)  at (2.1,-4.5)  {HW Type 3};
\draw[ar](api)--(top);
\draw[ar](top)--(ml); \draw[ar](top)--(mr);
\draw[ar](ml)--(bot); \draw[ar](mr)--(bot);
\draw[ar](bot)--(hal);
\draw[ar](hal)--(h1); \draw[ar](hal)--(h2); \draw[ar](hal)--(h3);
\end{tikzpicture}%
}
\caption{[System name] architecture stack.}
\label{fig:architecture}
\end{figure}
```

**Spacing rule:** Vertical gap between node rows = 0.9cm. Horizontal gap between
side-by-side modules = 2.9cm (`±1.45` from center).

---

## Figure Type 3 — Enhanced Architecture (core + flanking dashed additions)

Use for: proposed enhancements, new layers added to existing system.

```latex
\begin{figure}[H]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[
  font=\normalsize,
  core/.style={rectangle,rounded corners=3pt,draw=blue!55,fill=blue!18,
               minimum width=2.8cm,minimum height=0.62cm,align=center},
  newn/.style={rectangle,rounded corners=3pt,draw=orange!60,fill=orange!14,
               minimum width=2.2cm,minimum height=0.58cm,align=center},
  cppl/.style={rectangle,rounded corners=4pt,draw=green!55!black,fill=green!12,
               minimum width=2.8cm,minimum height=0.58cm,align=center,
               font=\normalsize\bfseries},
  lbl/.style={font=\normalsize\bfseries},
  ar/.style={-{Stealth[length=4pt]},thick,darkblue!55},
  dar/.style={-{Stealth[length=3pt]},dashed,thick,orange!65}
]
% ── Core modules (center column) ──────────────────────────────────
\node[core] (m1) at (0, 0.0) {Core Module 1};
\node[core] (m2) at (0,-0.9) {Core Module 2};
\node[core] (m3) at (0,-1.8) {Core Module 3};
\node[core] (m4) at (0,-2.7) {Core Module 4};
\draw[blue!40,thick,rounded corners=5pt] (-1.6,0.4) rectangle (1.6,-3.1);
\node[lbl,blue!60] at (0,0.75) {Existing System Core};

% ── Top addition: portability / cross-cutting (dashed green) ──────
\node[cppl] (cppl) at (0,1.55) {Portability Layer};
\draw[dashed,green!55!black,thick,rounded corners=4pt]
  (-1.6,1.15) rectangle (1.6,2.0);
\node[font=\scriptsize\bfseries,green!45!black] at (0,2.18)
  {Cross-Platform Portability};

% ── Left addition: AI / prediction layer (dashed orange) ──────────
\node[newn] (a1) at (-4.0, 0.0) {AI Component 1};
\node[newn] (a2) at (-4.0,-0.9) {AI Component 2};
\node[newn] (a3) at (-4.0,-1.8) {AI Component 3};
\draw[dashed,orange!65,thick,rounded corners=4pt]
  (-5.2,0.42) rectangle (-2.8,-2.22);
\node[lbl,orange!75] at (-4.0,0.78) {New Left Layer};

% ── Right addition: federation / distribution (dashed orange) ─────
\node[newn] (f1) at (4.0, 0.0) {Fed. Component 1};
\node[newn] (f2) at (4.0,-0.9) {Fed. Component 2};
\node[newn] (f3) at (4.0,-1.8) {Fed. Component 3};
\draw[dashed,orange!65,thick,rounded corners=4pt]
  (2.8,0.42) rectangle (5.2,-2.22);
\node[lbl,orange!75] at (4.0,0.78) {New Right Layer};

% ── Connections ───────────────────────────────────────────────────
\draw[dar] (a1)--(m1); \draw[dar] (a2)--(m2); \draw[dar] (a3)--(m3);
\draw[dar] (f2)--(m2); \draw[dar] (f3)--(m4);
\draw[-{Stealth[length=4pt]},dashed,thick,green!55!black] (cppl)--(m1);
\end{tikzpicture}%
}
\caption{Proposed enhanced architecture: existing core (center) plus three
new layers (dashed borders indicate proposed additions).}
\label{fig:enhanced}
\end{figure}
```

---

## Figure Type 4 — Grouped Bar Chart (platform/system comparison)

Use for: comparative analysis, multi-platform evaluation across N dimensions.

```latex
\begin{figure}[H]
\centering
\begin{tikzpicture}
\begin{axis}[
  ybar=1.2pt,
  bar width=4.5pt,
  width=\columnwidth,
  height=5.0cm,
  ylabel={Score (1--5)},
  ylabel style={font=\scriptsize},
  ymin=0, ymax=5.8,
  ytick={1,2,3,4,5},
  xtick=data,
  % ↓ Edit labels and symbolic coords together
  symbolic x coords={Dim1,Dim2,Dim3,Dim4,Dim5,Dim6},
  xticklabels={Dimension 1,Dimension 2,Dimension 3,
               Dimension 4,Dimension 5,Dimension 6},
  xticklabel style={font=\scriptsize,rotate=28,anchor=north east},
  legend style={font=\scriptsize,at={(0.5,-0.48)},anchor=north,
                legend columns=3,column sep=3pt},
  tick label style={font=\scriptsize},
  grid=major,grid style={line width=0.2pt,draw=gray!25},
  enlarge x limits=0.10,
]
% One \addplot per system — scores in same symbolic coord order
\addplot[fill=darkblue!78,draw=darkblue]
  coordinates {(Dim1,4)(Dim2,4)(Dim3,4)(Dim4,3)(Dim5,3)(Dim6,4)};
\addplot[fill=blue!55,draw=blue!70]
  coordinates {(Dim1,4)(Dim2,3)(Dim3,5)(Dim4,4)(Dim5,5)(Dim6,5)};
\addplot[fill=cyan!60,draw=cyan!75]
  coordinates {(Dim1,3)(Dim2,2)(Dim3,4)(Dim4,2)(Dim5,5)(Dim6,2)};
\addplot[fill=orange!68,draw=orange!80]
  coordinates {(Dim1,4)(Dim2,3)(Dim3,3)(Dim4,3)(Dim5,2)(Dim6,5)};
\addplot[fill=green!52,draw=green!65]
  coordinates {(Dim1,3)(Dim2,2)(Dim3,3)(Dim4,2)(Dim5,3)(Dim6,3)};
\addplot[fill=red!52,draw=red!65]
  coordinates {(Dim1,3)(Dim2,2)(Dim3,3)(Dim4,3)(Dim5,5)(Dim6,2)};
\legend{System A,System B,System C,System D,System E,System F}
\end{axis}
\end{tikzpicture}
\caption{Comparative evaluation across six [systems] on six dimensions
(scores 1--5 from published documentation; no self-reported claims accepted).}
\label{fig:comparison}
\end{figure}
```

**Score sourcing rule:** All scores must come from published documentation or
open-source code. Never assign scores from guesswork. If uncertain, use 2 (partial)
rather than leaving the figure ungrounded.

---

## Figure Type 5 — Heatmap (gap analysis, 7×7 grid)

Use for: gap analysis, feature coverage matrix.

**Color legend:** `red!68` = gap present (1) · `orange!58` = partial (2) ·
`yellow!62` = moderate (3) · `green!42` = addressed (4)

Cell dimensions: `1.0cm × 0.48cm`. Grid: 7 cols × 7 rows = 7.0cm × 3.36cm.
`\resizebox{\columnwidth}{!}` scales to fit any column width.

```latex
\begin{figure}[H]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[font=\tiny]
% ── Replace colors below with your actual gap scores ──────────────
% Row order top→bottom, Column order left→right
% Row 0: scores for columns 0–6
\fill[orange!58](0.0, 0.00) rectangle (1.0,-0.48); % (r0,c0): score 2
\fill[orange!58](1.0, 0.00) rectangle (2.0,-0.48); % (r0,c1): score 2
\fill[red!68]   (2.0, 0.00) rectangle (3.0,-0.48); % (r0,c2): score 1
\fill[orange!58](3.0, 0.00) rectangle (4.0,-0.48); % (r0,c3): score 2
\fill[orange!58](4.0, 0.00) rectangle (5.0,-0.48); % (r0,c4): score 2
\fill[red!68]   (5.0, 0.00) rectangle (6.0,-0.48); % (r0,c5): score 1
\fill[red!68]   (6.0, 0.00) rectangle (7.0,-0.48); % (r0,c6): score 1
% Row 1: (repeat pattern for rows 1–6, one \fill per cell)
% ... (49 total \fill commands for 7×7 grid)
% ── Grid lines ────────────────────────────────────────────────────
\foreach \i in {0,...,7}{
  \draw[white!55!black,line width=0.4pt](\i,0)--(\i,-3.36);}
\foreach \j in {0,...,7}{
  \draw[white!55!black,line width=0.4pt](0,-\j*0.48)--(7,-\j*0.48);}
\draw[black!65,thick](0,0) rectangle (7,-3.36);
% ── Row labels (left of grid) ────────────────────────────────────
\foreach \r/\lbl in {
  0/Gap Label 1,1/Gap Label 2,2/Gap Label 3,3/Gap Label 4,
  4/Gap Label 5,5/Gap Label 6,6/Gap Label 7}{
  \node[anchor=east,font=\tiny\bfseries] at (-0.1,{-\r*0.48-0.24}) {\lbl};
}
% ── Column labels (bottom, rotated 35°) ──────────────────────────
\foreach \c/\lbl in {
  0/Sys A,1/Sys B,2/Sys C,3/Sys D,4/Sys E,5/Sys F,6/Sys G}{
  \node[rotate=35,anchor=north east,font=\tiny\bfseries]
    at ({\c*1.0+0.5},-3.42) {\lbl};
}
% ── Legend (right of grid) ───────────────────────────────────────
\node[fill=red!68,minimum width=0.28cm,minimum height=0.22cm,
      draw=gray!50,inner sep=0] at (7.45,-0.24) {};
\node[anchor=west,font=\tiny] at (7.62,-0.24) {Gap (1)};
\node[fill=orange!58,minimum width=0.28cm,minimum height=0.22cm,
      draw=gray!50,inner sep=0] at (7.45,-0.72) {};
\node[anchor=west,font=\tiny] at (7.62,-0.72) {Partial (2)};
\node[fill=yellow!62,minimum width=0.28cm,minimum height=0.22cm,
      draw=gray!50,inner sep=0] at (7.45,-1.20) {};
\node[anchor=west,font=\tiny] at (7.62,-1.20) {Moderate (3)};
\node[fill=green!42,minimum width=0.28cm,minimum height=0.22cm,
      draw=gray!50,inner sep=0] at (7.45,-1.68) {};
\node[anchor=west,font=\tiny] at (7.62,-1.68) {Addressed (4)};
\end{tikzpicture}%
}
\caption{Gap analysis heatmap: [N] gaps (rows) across [M] platforms (columns).
Color scale: red = gap fully present; green = largely addressed.}
\label{fig:heatmap}
\end{figure}
```

---

## Figure Type 6 — Hybrid Loop / Execution Flow

Use for: variational quantum algorithms, iterative pipelines, feedback loops.

```latex
\begin{figure}[H]
\centering
\resizebox{0.94\columnwidth}{!}{%
\begin{tikzpicture}[
  font=\normalsize,
  proc/.style={rectangle,rounded corners=4pt,draw=darkblue,fill=darkblue!75,
               text=white,minimum width=2.8cm,minimum height=0.75cm,
               align=center,font=\normalsize\bfseries},
  cls/.style={rectangle,rounded corners=4pt,draw=blue!58,fill=blue!14,
              minimum width=2.8cm,minimum height=0.75cm,align=center,
              font=\normalsize\bfseries},
  srv/.style={rectangle,rounded corners=4pt,draw=gray!55,fill=gray!18,
              minimum width=2.6cm,minimum height=0.65cm,align=center},
  ar/.style={-{Stealth[length=5pt]},very thick,darkblue!62},
  lab/.style={font=\small,fill=white,inner sep=1pt,rounded corners=1pt}
]
% Four corners of the loop
\node[proc] (step1) at (0,   1.6) {Step 1 (QPU)\\$U(\boldsymbol{\theta})$};
\node[proc] (step2) at (3.5, 0.0) {Step 2\\Measure};
\node[cls]  (step3) at (0,  -1.8) {Step 3\\Optimize};
\node[cls]  (step4) at (-3.5,0.0) {Step 4\\Update $\boldsymbol{\theta}$};
% Optional: secondary nodes
\node[srv]  (aux1)  at (0,   3.3) {Auxiliary Node 1};
\node[srv]  (aux2)  at (4.8, 2.2) {Auxiliary Node 2};
% Main loop arrows (bend creates the circular appearance)
\draw[ar] (step1) to[bend left=15]
  node[lab,above right=-2pt and 2pt] {output} (step2);
\draw[ar] (step2) to[bend left=15]
  node[lab,below right=-2pt and 2pt] {loss} (step3);
\draw[ar] (step3) to[bend left=15]
  node[lab,below left=-2pt and 2pt]  {gradient} (step4);
\draw[ar] (step4) to[bend left=15]
  node[lab,above left=-2pt and 2pt]  {updated params} (step1);
% Secondary dashed connections
\draw[-{Stealth[length=4pt]},gray!55,thick] (aux1) -- (step1);
\draw[-{Stealth[length=4pt]},gray!55,thick,dashed]
  (step4.north) -- ++(0,0.6) -- (aux1.west);
\draw[-{Stealth[length=4pt]},gray!45,dashed,thick]
  (aux2.south west) -- (step1.east);
\draw[-{Stealth[length=4pt]},gray!45,dashed,thick]
  (aux2.south) -- (step2.north);
\end{tikzpicture}%
}
\caption{[Algorithm name] execution loop. [Step 1] → [Step 2] → [Step 3]
→ [Step 4] forms the main feedback cycle; [Aux 1] synchronizes parameters
across workers.}
\label{fig:loop}
\end{figure}
```

**Bend angle rule:** `to[bend left=15]` at 3.5cm node spacing produces a
natural arc. Increase to 20–25 for tighter node spacing.

---

## Figure Type 7 — Two-Branch Taxonomy Tree

Use for: workload classification, AI-for-X vs X-for-AI, any binary split.

```latex
\begin{figure}[H]
\centering
\resizebox{\columnwidth}{!}{%
\begin{tikzpicture}[
  font=\normalsize,
  root/.style={rectangle,rounded corners=4pt,draw=darkblue,fill=darkblue!80,
               text=white,minimum width=4.0cm,minimum height=0.7cm,
               align=center,font=\normalsize\bfseries},
  br/.style={rectangle,rounded corners=3pt,draw=blue!55,fill=blue!20,
             minimum width=2.6cm,minimum height=0.65cm,align=center,
             font=\normalsize\bfseries},
  lf/.style={rectangle,rounded corners=2pt,draw=gray!50,fill=gray!10,
             minimum width=2.4cm,minimum height=0.6cm,align=center},
  ann/.style={font=\scriptsize,gray!65,align=center},
  ar/.style={-{Stealth[length=4pt]},thick,darkblue!60}
]
\node[root] (root) at (0,0)     {Root: All Workloads};
\node[br]   (left) at (-3.2,-1.3) {Left Branch};
\node[br]   (right) at (3.2,-1.3) {Right Branch};
% Left leaves (3 items)
\node[lf] (l1) at (-4.4,-2.7) {Leaf L1\\{\scriptsize (annotation)}};
\node[lf] (l2) at (-3.2,-2.7) {Leaf L2\\{\scriptsize (annotation)}};
\node[lf] (l3) at (-2.0,-2.7) {Leaf L3\\{\scriptsize (annotation)}};
% Right leaves (3 items)
\node[lf] (r1) at (2.0,-2.7)  {Leaf R1\\{\scriptsize (annotation)}};
\node[lf] (r2) at (3.2,-2.7)  {Leaf R2\\{\scriptsize (annotation)}};
\node[lf] (r3) at (4.4,-2.7)  {Leaf R3\\{\scriptsize (annotation)}};
% Edges
\draw[ar] (root)--(left); \draw[ar] (root)--(right);
\draw[ar] (left)--(l1); \draw[ar] (left)--(l2); \draw[ar] (left)--(l3);
\draw[ar] (right)--(r1); \draw[ar] (right)--(r2); \draw[ar] (right)--(r3);
% OS module / status annotations below leaves
\node[ann] at (-4.4,-3.5) {\textbullet\ Module 1};
\node[ann] at (-3.2,-3.5) {\textbullet\ Module 2};
\node[ann] at (-2.0,-3.5) {\textbullet\ Module 3};
\node[ann] at (2.0,-3.5)  {$\circ$\ Future};
\node[ann] at (3.2,-3.5)  {\textbullet\ Module 4};
\node[ann] at (4.4,-3.5)  {\textbullet\ Module 5};
\node[font=\tiny\itshape,gray!55] at (0,-3.5)
  {\textbullet=supported \quad $\circ$=future};
\end{tikzpicture}%
}
\caption{[Subject] taxonomy for [purpose]: left branch covers [category A]
workloads; right branch covers [category B] workloads. Annotations indicate
OS module support (\textbullet) vs.\ future work ($\circ$).}
\label{fig:taxonomy2}
\end{figure}
```

---

## Figure Design Principles

### 1. Readability at column width (88mm / ~3.5 inches)

- Minimum TikZ `font=\scriptsize` for annotations, `\tiny` for dense grids
- Use `\resizebox{\columnwidth}{!}` — lets you design at comfortable size
- Test: compile and read the PDF at 100% zoom; text must be legible

### 2. Color + accessibility

- All figures use the same color convention table above for consistency
- Design works in grayscale: `darkblue` and `gray` are distinguishable when printed
- Never use red+green as the *only* distinguishing factor (colorblind risk)

### 3. Caption completeness

```
BAD:  "Architecture diagram."
GOOD: "Origin Pilot V4.0 four-module architecture. The Quantum Task Scheduler
       dispatches jobs to either the Resource Manager or Program Compiler;
       both feed the Auto Qubit Calibration module, which interfaces with
       three hardware modalities via the HAL."
```

### 4. Figure placement

- `[H]` (forced here, requires `\usepackage{float}`) — use for figures directly
  referenced in the surrounding paragraph where position matters for narrative
- `[t]` (top of page) — use for overview/key figures in Introduction
- `[!t]` — use only when LaTeX persistently floats a critical figure away

### 5. Figure numbering

- Every figure must have a `\label{fig:X}` immediately after `\caption{}`
- Text reference must precede the figure: "as shown in Fig.~\ref{fig:X}"
- Never reference a figure before its float environment appears in the .tex source

---

## LaTeX File Editing Safety Rules

### sed double-backslash corruption (critical)

**Never use `sed` to insert or modify backslash sequences in `.tex` files.**

The bash shell double-expands backslashes inside `sed` replacement strings:

| sed command | Writes to file | LaTeX result |
|---|---|---|
| `sed 's/foo/\\begin/'` | `\begin` | ✓ correct |
| `sed 's/foo/\\\\begin/'` | `\\begin` | ✗ ERROR: "Undefined control sequence" |

If `sed` was used on a `.tex` file and compilation fails with
"Undefined control sequence" for every `\begin`, `\end`, `\caption`, etc.,
run this repair command:

```bash
sed -i 's/\\\\begin{\([^}]*\)}/\\begin{\1}/g;
        s/\\\\end{\([^}]*\)}/\\end{\1}/g;
        s/\\\\centering/\\centering/g;
        s/\\\\caption/\\caption/g;
        s/\\\\label/\\label/g' main.tex
```

**Always use the `Edit` tool directly for any LaTeX modification.**
The Edit tool writes exact bytes — no shell backslash expansion.

---

## Figure Delivery Checklist

Run before every draft delivery:

```bash
# 1. No placeholders remain
grep -n "figplaceholder\|INSERT.*figure\|figure.*placeholder" main.tex
# Must return zero

# 2. Every figure has both \caption and \label
grep -c "\\\\caption" main.tex
grep -c "\\\\label{fig:" main.tex
# Counts must match

# 3. Every \label{fig:X} has a matching \ref{fig:X} in body
for lbl in $(grep -o '\\label{fig:[^}]*}' main.tex | sed 's/\\label{//;s/}//'); do
  grep -q "\\\\ref{$lbl}" main.tex || echo "UNREFERENCED: $lbl"
done
# Must print nothing

# 4. TikZ packages present in preamble
grep "usepackage{tikz}" main.tex
grep "usepackage{pgfplots}" main.tex
# Must each return one match

# 5. Compile with zero errors
pdflatex -interaction=nonstopmode main.tex 2>&1 | grep "^!" | wc -l
# Must return 0
```
