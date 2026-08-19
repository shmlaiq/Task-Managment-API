# Mathematical Notation and Proof Writing

## Notation Consistency Rules

Inconsistent notation is one of the most common reasons for reviewer complaints.
Define every symbol once, use it consistently, and never reuse a symbol for two
different meanings.

### Standard notation conventions (CS/AI/ML):

| Symbol Type | Convention | Example |
|---|---|---|
| Scalars | lowercase italic | $n$, $x$, $\lambda$ |
| Vectors | lowercase bold | $\mathbf{x}$, $\mathbf{w}$ |
| Matrices | uppercase bold | $\mathbf{W}$, $\mathbf{X}$ |
| Sets | calligraphic | $\mathcal{D}$, $\mathcal{L}$ |
| Random variables | uppercase italic | $X$, $Y$ |
| Functions | italic or roman | $f(\cdot)$, $\text{softmax}(\cdot)$ |
| Operators | roman (non-italic) | $\mathbb{E}[\cdot]$, $\text{Tr}(\cdot)$ |
| Distributions | italic or calligraphic | $\mathcal{N}(\mu, \sigma^2)$ |

---

## Notation Table (Include When > 5 Symbols)

If your paper uses more than 5 symbols, include a notation table early in Section III:

```latex
\begin{table}[h]
\caption{Notation used in this paper}
\label{tab:notation}
\centering
\begin{tabular}{cl}
\toprule
\textbf{Symbol} & \textbf{Description} \\
\midrule
$n$             & Number of training samples \\
$d$             & Feature dimension \\
$\mathbf{X}$    & Input feature matrix, $\mathbf{X} \in \mathbb{R}^{n \times d}$ \\
$\mathbf{y}$    & Label vector, $\mathbf{y} \in \{0, 1\}^n$ \\
$\mathcal{L}$   & Loss function \\
$\theta$        & Model parameters \\
$\hat{y}$       & Predicted output \\
\bottomrule
\end{tabular}
\end{table}
```

---

## Equation Formatting

### Rules:
1. Number every standalone equation with `\begin{equation}...\end{equation}`
2. Use `\begin{align}` for multi-line derivations
3. Only equations that are referenced later need numbers; use `\begin{equation*}` for unnumbered
4. Punctuate equations as part of the sentence (comma or period after equation)
5. Define every new variable inline immediately after introduction

### Examples:

```latex
% Single equation — numbered
The training objective is defined as:
\begin{equation}
  \mathcal{L}(\theta) = \frac{1}{n} \sum_{i=1}^{n} \ell(f_\theta(\mathbf{x}_i), y_i) 
  + \lambda \|\theta\|_2^2,
  \label{eq:objective}
\end{equation}
where $\ell(\cdot, \cdot)$ denotes the cross-entropy loss and $\lambda > 0$
is the regularization coefficient.

% Multi-line aligned derivation
\begin{align}
  \mathcal{L}_\text{total} &= \mathcal{L}_\text{task} + \alpha \mathcal{L}_\text{reg}
    \label{eq:total} \\
  &= -\mathbb{E}_{(\mathbf{x},y) \sim \mathcal{D}}[\log p_\theta(y|\mathbf{x})]
     + \alpha \text{KL}(q_\phi \| p_\theta).
    \label{eq:expanded}
\end{align}
```

### Common mistakes:
```latex
% WRONG — variable not defined
The loss is L = sum_i CE(f(x_i), y_i).

% WRONG — equation not punctuated
The output is:
\begin{equation}
  \hat{y} = \text{softmax}(Wx + b)
\end{equation}
Our method then...

% CORRECT — defined, punctuated, referenced
The predicted output $\hat{y}$ is computed as:
\begin{equation}
  \hat{y} = \text{softmax}(\mathbf{W}\mathbf{x} + \mathbf{b}),
  \label{eq:output}
\end{equation}
where $\mathbf{W} \in \mathbb{R}^{c \times d}$ is the weight matrix and
$\mathbf{b} \in \mathbb{R}^c$ is the bias term.
```

---

## Theorem, Lemma, Proposition Format

For theory papers or papers with formal results:

```latex
% In preamble:
\usepackage{amsthm}
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{definition}{Definition}
\newtheorem{remark}{Remark}

% In document:
\begin{definition}[Lipschitz Continuity]
A function $f: \mathbb{R}^d \to \mathbb{R}$ is $L$-Lipschitz if for all
$\mathbf{x}, \mathbf{y} \in \mathbb{R}^d$:
\begin{equation}
  |f(\mathbf{x}) - f(\mathbf{y})| \leq L \|\mathbf{x} - \mathbf{y}\|_2.
\end{equation}
\end{definition}

\begin{theorem}[Convergence Rate]
\label{thm:convergence}
Under Assumptions 1–3, the gradient descent update with step size
$\eta = 1/L$ satisfies:
\begin{equation}
  f(\mathbf{x}_t) - f^* \leq \frac{\|\mathbf{x}_0 - \mathbf{x}^*\|_2^2}{2\eta t},
\end{equation}
where $f^* = \min_{\mathbf{x}} f(\mathbf{x})$ and $\mathbf{x}^*$ is the minimizer.
\end{theorem}

\begin{proof}
[Proof here — or:]
The proof follows from standard convex optimization arguments; see Appendix A.
\end{proof}
```

### When to put proofs in the appendix:
- If the proof is longer than 1 column — move to appendix
- If the proof uses lemmas — move lemma + theorem to appendix together
- Main text: state the theorem, cite the proof location: "See Appendix A for the proof."

---

## Algorithm Blocks

Use `algorithm` + `algorithmic` packages:

```latex
\usepackage{algorithm}
\usepackage{algorithmic}  % or \usepackage{algpseudocode} for algorithmicx

\begin{algorithm}
\caption{Your Algorithm Name}
\label{alg:main}
\begin{algorithmic}[1]   % [1] = show line numbers
\REQUIRE Dataset $\mathcal{D}$, learning rate $\eta$, epochs $T$
\ENSURE Trained model parameters $\theta$
\STATE Initialize $\theta$ randomly
\FOR{$t = 1$ to $T$}
    \FOR{each mini-batch $(\mathbf{X}_b, \mathbf{y}_b) \in \mathcal{D}$}
        \STATE Compute $\hat{\mathbf{y}}_b = f_\theta(\mathbf{X}_b)$  \COMMENT{Forward pass}
        \STATE Compute $\mathcal{L} = \frac{1}{|b|}\sum_i \ell(\hat{y}_i, y_i)$
        \STATE $\theta \leftarrow \theta - \eta \nabla_\theta \mathcal{L}$  \COMMENT{Gradient update}
    \ENDFOR
\ENDFOR
\RETURN $\theta$
\end{algorithmic}
\end{algorithm}
```

### Algorithm formatting rules:
- Line numbers mandatory (`[1]` in `\begin{algorithmic}`)
- `\COMMENT{}` for inline explanations
- Input/output explicitly stated with `\REQUIRE` / `\ENSURE`
- Reference algorithm in text: "Algorithm~\ref{alg:main} describes..."
- Time complexity stated after the algorithm block or in caption

---

## Common LaTeX Math Commands

```latex
% Useful shortcuts to define in preamble:
\newcommand{\E}{\mathbb{E}}          % Expectation
\newcommand{\R}{\mathbb{R}}          % Real numbers
\newcommand{\norm}[1]{\|#1\|}        % Norm
\newcommand{\abs}[1]{|#1|}           % Absolute value
\newcommand{\given}{\,|\,}           % Conditional
\DeclareMathOperator*{\argmin}{arg\,min}  % argmin
\DeclareMathOperator*{\argmax}{arg\,max}  % argmax

% Usage:
% $\E_{x \sim p}[f(x)]$
% $\mathbf{W} \in \R^{d \times k}$
% $\norm{\mathbf{x}}_2 \leq 1$
% $\theta^* = \argmin_\theta \mathcal{L}(\theta)$
```

---

## Math Notation Checklist

- [ ] All symbols defined at first use (not just in notation table)
- [ ] Notation table included if > 5 symbols
- [ ] Every standalone equation is numbered
- [ ] Equations punctuated as part of sentence (comma/period)
- [ ] No symbol reused for two different meanings
- [ ] Vectors bold lowercase, matrices bold uppercase (or document the convention used)
- [ ] Theorems/lemmas use `\newtheorem` (not manual bold text)
- [ ] Proofs > 1 column moved to appendix with reference in main text
- [ ] Algorithms include line numbers and `\REQUIRE`/`\ENSURE`
- [ ] All algorithm references use `Algorithm~\ref{alg:X}` (capital A)
