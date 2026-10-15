# Author Biography — Muhammad Faisal Laiq

Canonical author bio for all papers in `papers/`. Reuse verbatim.

- **Approved:** 2026-10-14 (HACOF paper); updated 2026-10-15 (duplicate e-mail removed from the bio).
- **Source of truth in use:** `law-policy-governance-ai-ecosystem/access/main.tex`.
- **Photo:** `law-policy-governance-ai-ecosystem/access/author.jpg`, 600×750 (4:5), sized for IEEE's 1 in × 1.25 in bio box. Copy it into each new paper's folder.

## LaTeX (IEEE Access / IEEEtran journal)

Place after `\bibliography{...}`. In the IEEE Access template, it goes before `\EOD`.

```latex
\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{author.jpg}}]{Muhammad Faisal Laiq}
received the master's degree in telecommunication.

He has served in the government sector since 2006 and is currently Additional Director ICT at a public-sector university and hospital in Pakistan, where he leads digital transformation and ICT infrastructure. He is also an agentic AI engineer and independent researcher. His AI work centers on AI-driven development (AIDD), loop engineering, and hierarchical multi-agent systems (``agentic fleets'') built with Python, FastAPI, Docker, and Kubernetes, in which a chief agent proposes specialized sub-agents but must obtain human approval before creating or activating them. His research includes the paper \emph{Artificial Intelligence in Future Warfare: Ethical Frameworks and the Regulation of Lethal Autonomous Weapons}, and covers AI governance, forward-deployed engineering in the AI industry, biocomputing as an alternative to silicon-based AI, the environmental cost of AI resource consumption, and operating systems for cloud-accessible quantum computers.
\end{IEEEbiography}
```

## Rules

- Contact detail: e-mail only (shmlaiq@gmail.com), shown on page 1 (author block / corresponding-author line), **not** in the bio.
- Location: "Pakistan" only. Do not name the employer.
- Do not add a grade, a bachelor's degree, university names, project details, certifications, a phone number or any address.
- Only the research-interests list may be updated for new papers; any other change needs the author's approval.

## Short version (magazines, e.g. IEEE Software)

Approved 2026-10-15. About 55 words. Use it where word limits rule out the full bio.

```latex
\begin{IEEEbiography}[{\includegraphics[width=1in,height=1.25in,clip,keepaspectratio]{author.jpg}}]{Muhammad Faisal Laiq}
is Additional Director ICT at a public-sector university and hospital in Pakistan, where he leads digital transformation and ICT infrastructure, and an independent researcher in agentic AI. His research interests include AI-driven development, loop engineering, human-approved hierarchical multi-agent systems, and AI governance. He received a master's degree in telecommunication.
\end{IEEEbiography}
```

## Where it is used (2026-10-15)

- Full bio: HACOF (both versions), FDE IEEE Access, Biocomputing, Loop Engineering, OpenClaw (`main.tex`), OS of AI Agents.
- Short bio: FDE IEEE Software.
- No bio, by design: the LAWS paper (blind review; a bio would reveal the author) and the OpenClaw arXiv copy (preprints don't use one).
