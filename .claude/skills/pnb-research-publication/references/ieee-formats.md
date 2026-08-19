# IEEE Formats — Citations, LaTeX Templates, Figures, Tables

## Full LaTeX Template (IEEEtran)

```latex
% ============================================================
% IEEE Conference Paper Template
% ============================================================
\documentclass[conference]{IEEEtran}
% For journal: \documentclass[journal]{IEEEtran}
% For transactions: \documentclass[10pt,journal,compsoc]{IEEEtran}

\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{algorithm}
\usepackage{graphicx}
\usepackage{textcomp}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{url}
\usepackage{hyperref}

\begin{document}

\title{Your Paper Title: Specific and Informative}

% ── Author block variants ────────────────────────────────────────────────────

% VARIANT A — Single author WITH institutional affiliation (most common):
\author{%
  \IEEEauthorblockN{Muhammad Faisal Laiq Siddiqui}%
  \IEEEauthorblockA{Department of Computer Science, University Name\\
    City, Country\\
    Email:~author@university.edu \quad ORCID:~0009-0007-5779-9836}%
}

% VARIANT B — Single author WITHOUT institutional affiliation (no affiliation line):
% Rule: when there is NO institution, do NOT use \IEEEauthorblockA at all —
% it creates an unwanted blank line. Put everything on ONE line in \IEEEauthorblockN
% using \qquad for spacing.
\author{%
  \IEEEauthorblockN{Muhammad Faisal Laiq Siddiqui \qquad
    Email:~shmlaiq@gmail.com \qquad ORCID:~0009-0007-5779-9836}%
}

% VARIANT C — Multiple authors with different institutions:
\author{%
  \IEEEauthorblockN{Author One\textsuperscript{1}, Author Two\textsuperscript{2}}
  \IEEEauthorblockA{\textsuperscript{1}Department, University One, City, Country\\
    email1@uni.edu}
  \IEEEauthorblockA{\textsuperscript{2}Company, City, Country\\
    email2@company.com}
}

% VARIANT D — Blind review (double-blind conferences):
% \author{Anonymous Authors}

% ── Decision rule ────────────────────────────────────────────────────────────
% Has institution? → Variant A (or C for multiple)
%   \IEEEauthorblockN{name}
%   \IEEEauthorblockA{institution \\ city \\ email \quad ORCID}
%
% No institution?  → Variant B — ONE line in \IEEEauthorblockN, NO \IEEEauthorblockA
%   \IEEEauthorblockN{name \qquad Email:~x \qquad ORCID:~x}
%
% \qquad produces ~2em of horizontal space — use it between fields on the same line.
% Never use \IEEEauthorblockA with an empty or placeholder value — it creates a
% visible blank line in the rendered PDF.

\maketitle

\begin{abstract}
Your abstract here (150--250 words). State the problem, your approach,
key results, and significance. No citations, no acronyms undefined, no equations.
\end{abstract}

\begin{IEEEkeywords}
keyword one, keyword two, keyword three, keyword four
\end{IEEEkeywords}

\section{Introduction}
\label{sec:intro}

% ... paper content ...

\section{Related Work}
\label{sec:related}

\section{Proposed Method}
\label{sec:method}

% Equation example:
\begin{equation}
  \mathcal{L} = \mathcal{L}_{ce} + \lambda \mathcal{L}_{reg}
  \label{eq:loss}
\end{equation}

\noindent where $\mathcal{L}_{ce}$ is the cross-entropy loss and $\lambda$ is a
regularization weight.

\section{Experiments}
\label{sec:experiments}

\section{Results}
\label{sec:results}

\section{Discussion}
\label{sec:discussion}

\section{Conclusion}
\label{sec:conclusion}

\section*{Acknowledgment}
% Omit for blind review
This work was supported by [Grant Agency, Grant No. XXX].

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
```

---

## BibTeX Citation Formats (references.bib)

### Journal Article
```bibtex
@article{author2024title,
  author    = {Author, First and Author, Second},
  title     = {Title of the Article},
  journal   = {IEEE Transactions on Neural Networks and Learning Systems},
  volume    = {35},
  number    = {4},
  pages     = {1234--1245},
  year      = {2024},
  doi       = {10.1109/TNNLS.2024.XXXXXXX}
}
```

### Conference Paper
```bibtex
@inproceedings{author2024conf,
  author    = {Author, First and Author, Second},
  title     = {Title of the Conference Paper},
  booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision
               and Pattern Recognition (CVPR)},
  address   = {Seattle, WA, USA},
  month     = {June},
  year      = {2024},
  pages     = {1234--1243},
  doi       = {10.1109/CVPR52733.2024.XXXXXX}
}
```

### Book
```bibtex
@book{author2024book,
  author    = {Author, First},
  title     = {Title of the Book},
  edition   = {3rd},
  address   = {New York, NY, USA},
  publisher = {IEEE Press},
  year      = {2024}
}
```

### arXiv Preprint (only use real, verified IDs)
```bibtex
@misc{author2024arxiv,
  author        = {Author, First and Author, Second},
  title         = {Title of the Preprint},
  year          = {2024},
  eprint        = {2401.12345},
  archivePrefix = {arXiv},
  primaryClass  = {cs.LG}
}
```

### GitHub Repository / Software
```bibtex
@misc{author2024github,
  author  = {Author, First},
  title   = {Repository Name},
  year    = {2024},
  url     = {https://github.com/org/repo},
  note    = {[Accessed: Apr. 4, 2026]}
}
```

### Standard
```bibtex
@techreport{ieee2024standard,
  author      = {{IEEE}},
  title       = {IEEE Standard for XYZ},
  institution = {IEEE},
  number      = {IEEE Std 802.11-2024},
  year        = {2024}
}
```

---

## Inline Citation Format

All inline citations use `[N]` — never `(Author, Year)`:

```latex
% Single citation
The attention mechanism \cite{vaswani2017attention} revolutionized NLP.

% Multiple citations
Several methods address this problem \cite{he2016resnet, vaswani2017attention, devlin2019bert}.

% Citation at end of sentence (before period)
This achieves state-of-the-art results on ImageNet \cite{he2016resnet}.

% Author name in text
Vaswani et al. \cite{vaswani2017attention} proposed the Transformer architecture.
```

---

## Figure Formatting

```latex
\begin{figure}[h]
  \centering
  \includegraphics[width=\columnwidth]{figures/fig1_architecture.pdf}
  \caption{Overview of the proposed architecture. 
           (a) The encoder module. (b) The decoder module.
           Best viewed in color.}
  \label{fig:architecture}
\end{figure}

% Two-column spanning figure:
\begin{figure*}[t]
  \centering
  \includegraphics[width=\textwidth]{figures/fig2_results.pdf}
  \caption{Qualitative results on [Dataset]. Top row: input images.
           Bottom row: our predictions vs. ground truth.}
  \label{fig:qualitative}
\end{figure*}
```

**Figure rules:**
- Reference every figure inline: "as shown in Fig.~\ref{fig:architecture}"
- Caption describes what is shown, not the obvious
- "Best viewed in color" if color is meaningful
- Use vector formats (PDF, SVG) for diagrams; PNG for photos
- Number figures sequentially in order of appearance

---

## Table Formatting

```latex
\begin{table}[h]
\caption{Comparison on CIFAR-10 Test Set}
\label{tab:main_results}
\centering
\begin{tabular}{lccc}
\toprule
\textbf{Method} & \textbf{Acc. (\%)} & \textbf{Params (M)} & \textbf{FLOPs (G)} \\
\midrule
ResNet-50 \cite{he2016resnet}    & 93.6 & 25.6 & 4.1 \\
ViT-B/16 \cite{dosovitskiy2020vit} & 94.2 & 86.4 & 17.6 \\
EfficientNet \cite{tan2019efficientnet} & 94.7 & 5.3 & 0.4 \\
\midrule
\textbf{Ours}    & \textbf{95.4} & \textbf{4.1} & \textbf{0.3} \\
\bottomrule
\end{tabular}
\end{table}
```

**Table rules:**
- Use `booktabs` package (`\toprule`, `\midrule`, `\bottomrule`)
- Bold the best result per column
- Place caption ABOVE table (IEEE standard)
- Reference every table inline: "as shown in Table~\ref{tab:main_results}"

---

## Math and Equations

```latex
% Numbered equation
\begin{equation}
  \hat{y} = \text{softmax}(W_o \cdot \text{MultiHead}(Q, K, V))
  \label{eq:output}
\end{equation}

% Aligned multi-line
\begin{align}
  \mathcal{L} &= \mathcal{L}_{ce} + \lambda \mathcal{L}_{kd} \\
              &= -\sum_i y_i \log \hat{y}_i + \lambda \cdot \text{KL}(p \| q)
  \label{eq:total_loss}
\end{align}

% Inline math
The learning rate $\eta$ was set to $10^{-4}$ with cosine decay.
```

---

## IEEE Venue Abbreviations (commonly needed in citations)

| Full Name | Abbreviation used in bibtex |
|---|---|
| IEEE Conference on Computer Vision and Pattern Recognition | CVPR |
| International Conference on Learning Representations | ICLR |
| Neural Information Processing Systems | NeurIPS |
| International Conference on Machine Learning | ICML |
| IEEE Transactions on Pattern Analysis and Machine Intelligence | IEEE Trans. Pattern Anal. Mach. Intell. |
| IEEE Transactions on Neural Networks and Learning Systems | IEEE Trans. Neural Netw. Learn. Syst. |
| IEEE/ACM Transactions on Networking | IEEE/ACM Trans. Netw. |
| Proceedings of the IEEE | Proc. IEEE |
