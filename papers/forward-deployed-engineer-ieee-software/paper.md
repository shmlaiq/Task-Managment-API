# Forward Deployed Engineer (FDE) in the AI Ecosystem

**Author:** Muhammad Faisal Laiq — Email: shmlaiq@gmail.com — ORCID: 0009-0007-5779-9836

---

## Abstract

"Forward Deployed Engineer" (FDE) job postings multiplied across AI companies between 2023 and 2025, but the title has no shared definition — teams confuse it with Solutions Architect, Sales Engineer, and plain Software Engineer, then staff and pay it like one of those roles instead of what it actually is. This article proposes a six-dimension way to tell FDE apart from four adjacent roles, a competency profile built from real hiring evidence, and a four-stage engagement lifecycle with the feedback loop most teams don't budget for. It compares how Palantir, OpenAI, Anthropic, and Scale AI run their FDE programs from public sources, and closes with three concrete actions engineering leaders can take this quarter — before the next FDE requisition gets written from a Solutions Architect template.

---

## Three Actionable Insights

- **Stop hiring FDEs against a Solutions Architect job description.** Ambiguity tolerance — not client-facing hours — is the trait that actually separates the two roles. Screen for it directly: give candidates an underspecified problem, not a system-design exercise.
- **Budget every FDE engagement for a return trip to discovery.** Teams that plan Discovery → Prototype → Integration → Handoff as four fixed-length phases consistently blow their timeline, because Integration routinely surfaces constraints Discovery couldn't have found.
- **Write down your handoff plan before the engagement starts, not after.** The single most common FDE program failure isn't a bad deployment — it's a good one nobody owns six months later.

---

## I. Introduction

Job postings for "Forward Deployed Engineer" multiplied across AI-native companies between 2023 and 2025. By the time OpenAI stood up a dedicated FDE function in 2025, forward-deployed and solutions-engineering roles already accounted for 22 of the company's 311 open positions [1]. Palantir popularized the title over a decade earlier — engineers embedded directly with clients, internally called "Delta," building and modifying software against operational needs that shifted week to week; for several years before 2016, Palantir employed more FDEs than conventional software engineers [2]. What changed since 2023 is scale and imitation: OpenAI, Anthropic, and Scale AI have each stood up teams under the same label or a close variant [3]–[5].

No engineering body defines it. A Solutions Architect also goes to the client. So does a Site Reliability Engineer (SRE) doing an onsite incident postmortem. That gloss — "an engineer who goes to the client" — collapses distinctions that matter the moment you try to hire, level, or pay for the role. Recruiters copy Solutions Architect job descriptions and add "willingness to travel." Compensation teams benchmark FDE pay against sales scales never designed for engineers who ship production code. Engineering leaders staff FDE teams with generalist engineers who lack client-facing training, then wonder why every engagement stalls in discovery.

The closest precedent for what happens next is Site Reliability Engineering. SRE existed as an internal Google practice for years — a hybrid discipline everyone recognized but nobody had formally written down — before Google's own account of the practice turned it into a hireable, teachable, industry-wide discipline [6]. FDE is at roughly that pre-codification stage today. This article is an attempt to do that codification step early enough to shape hiring practice, not just describe it after the fact.

Large language model (LLM) deployment inside enterprises makes the stakes concrete: a systematic review of 63 enterprise RAG and LLM adoption studies found fewer than 15% addressed the real-time integration challenges production deployment actually requires [7]. That gap — between what a model demonstrates in a benchmark and what it takes to make it work on one company's real data — is exactly the terrain FDEs are hired to cover, and exactly what a Solutions Architect job description was never built to screen for.

## II. What an FDE Actually Is

An FDE is an engineer with full authority to modify a vendor's product — not merely configure it — embedded inside a specific client's environment to close the gap between a horizontal AI product and that client's operational workflow, under open-ended technical and organizational ambiguity. Three clauses do the real work. *Full authority to modify the product* excludes Solutions Architects, who design against existing extension points rather than change core code. *Embedded inside a specific client's environment* excludes ML Research Engineers, whose audience is the model or the research community, not a paying account. *Open-ended ambiguity* excludes conventional Software Engineers working a backlog a product manager has already scoped for them.

Table I lays out the distinction that actually matters for hiring: ambiguity tolerance, not client-interaction frequency. A Sales Engineer talks to clients constantly too, but under a bounded question — does the product meet the stated requirement, yes or no. An FDE routinely doesn't know, at the start of an engagement, whether the requirement is solvable with the current product at all. That's the job. Hiring bars and comp bands built around "client-facing hours" alone will consistently mis-level this role against Sales Engineering, understating the technical bar it actually requires.

**Table I — FDE vs. Four Adjacent Roles**

| Dimension | FDE | SWE | ML Research Engineer | Solutions Architect |
|---|---|---|---|---|
| Primary output | Working integration in client's stack | Shipped product feature | Model/experiment artifact | Design recommendation |
| Client interaction | Continuous, embedded | Rare, mediated | Minimal | High, pre-sale/advisory |
| Ambiguity tolerance | Very high — undefined problem AND solution | Low — scoped tickets | High on research, low on audience | Moderate — defined ask |
| Travel expectation | High (one company quantifies at 25% [4]) | Low | Low | Moderate |

## III. What Makes a Good FDE

Two competencies dominate, and neither shows up in a standard technical interview. The first is integration engineering against unfamiliar, undocumented client systems under time pressure — legacy databases, internal APIs, formats nobody wrote down — plus the AI-specific version of that skill: debugging why a retrieval-augmented generation (RAG) pipeline degrades silently on one client's real document corpus, or why an agent's behavior, reliable in evaluation, breaks on a query pattern the benchmark never saw [7]–[9]. The second is discovery facilitation — running a working session that extracts a client's actual operational problem when the client hasn't fully articulated it themselves. It's arguably the single most valuable FDE skill, and it's almost never assessed in a hiring loop built for engineers.

Fig. 1 shows why the engagement itself resists the flat, phase-by-phase project plan most teams default to. Discovery narrows scope to something achievable; Prototype routinely reveals the narrowed scope was still wrong, because a client's stated workflow and their actual workflow diverge in ways nobody notices until code runs against real data. That divergence forces a return to Discovery — the dashed loop in the figure — and teams that budget four fixed-length sequential phases consistently underrun their timeline because they never planned for that loop.

[FIGURE 1 — FDE engagement lifecycle: Discovery → Prototype → Integration → Handoff/Scale, with a dashed feedback arrow from Integration back to Discovery, labeled "scope revision when integration surfaces unanticipated constraints." Same TikZ diagram as the companion IEEE Access paper.]

The Handoff/Scale stage has its own quiet failure mode, and it's organizational, not technical: client teams frequently lack the capacity to maintain what the FDE built, leaving the vendor holding informal, unstaffed maintenance responsibility for code nobody budgeted as a long-term product. Anthropic's own FDE role description names this directly — "identify and codify repeatable deployment patterns" is a partial, informal answer to it, not a solved one [4].

## IV. How Four AI Companies Are Doing It

Palantir remains the reference implementation: FDE as a first-class engineering discipline with a documented pipeline into product roles, not a support function bolted onto sales [2], [10]. OpenAI's version is younger and unusually well-documented for its age — Colin Jarvis built the business case in early 2025, the team grew from two FDEs to more than ten across eight cities on three continents, and OpenAI draws the Solutions-Architect boundary explicitly: Solutions Architects advise, FDEs write code directly on customer infrastructure under real ambiguity [2]. Anthropic runs FDE inside its Applied AI team with unusual specificity in its own posting — deliverables named as "MCP servers, sub-agents, and agent skills," travel quantified at 25%, four-plus years of customer-facing experience required [4]. Scale AI's solutions and deployment function grew out of data-labeling and evaluation infrastructure rather than a general-purpose product needing client adaptation — a different starting point than the other three, even where the resulting job title looks the same on a careers page --- a characterization this analysis holds with less confidence than the other three, given limited independent verification of the current posting [5].

The clearest pattern across all four isn't structural convergence so much as a documentation gap: Palantir's decade-plus public track record dwarfs the other three, largely because it has one and they don't yet. That's a disclosure asymmetry, not necessarily a maturity one — this analysis can't tell "less mature" apart from "less publicly documented" from public sources alone. What's consistent regardless: all four give FDEs real product-modification authority inside a client's environment, all four treat that as distinct from conventional sales engineering, and none has published a formal competency framework of the kind this article proposes.

## V. Limitations and What's Next

This framework is descriptive, not causal — it says what FDE work looks like across public job postings, not that any one dimension predicts a good engagement, because no engagement-outcome data was collected to test that. Every claim about the four named companies comes from public, often company-authored material that naturally emphasizes program strengths; take the case comparison with that discount in mind. And role titles at this boundary are multiplying fast — "Applied AI Engineer," "AI Solutions Engineer" — so a taxonomy built from a 2026 snapshot will need revisiting inside two years, not five.

The next real step is a practitioner survey: score actual FDEs and their managers against these dimensions and against concrete engagement outcomes. Nothing in Section III has been tested against outcomes yet — that's the honest gap, and it's the highest-priority one to close.

## VI. Conclusion

The FDE title is doing real organizational work right now without a definition to back it up. Section II's distinction — ambiguity tolerance over client-interaction frequency — is the one hiring managers most often get backwards. Section III's lifecycle model gives engineering leaders a planning tool the flat sequential mental model doesn't provide. None of that requires waiting for a formal academic consensus to start using: the three actions at the top of this article are usable on the next FDE requisition your team writes.

---

## Acknowledgments

This work received no external funding or institutional support. All source material is drawn from publicly accessible company career pages, industry publications, and peer-reviewed literature, as cited throughout.

This article's text was drafted with the assistance of Claude (Anthropic), an artificial intelligence system, under the direction, review, and fact-verification of the author, who is fully accountable for all content, citations, and claims. No AI system is credited as an author.

---

## References

[1] J. Schmidt, "Trading Margin for Moat: Why the Forward Deployed Engineer Is the Hottest Job in Startups," Andreessen Horowitz, Jun. 4, 2025. [Online]. Available: https://a16z.com/services-led-growth/

[2] G. Orosz, "What are Forward Deployed Engineers, and why are they so in demand?," *The Pragmatic Engineer*, Aug. 12, 2025. [Online]. Available: https://newsletter.pragmaticengineer.com/p/forward-deployed-engineers

[3] OpenAI, "Forward Deployed Engineer (FDE), Life Sciences – SF," OpenAI Careers, 2026. [Online]. Available: https://openai.com/careers/forward-deployed-engineer-(fde)-life-sciences-sf-san-francisco/

[4] Anthropic, "Forward Deployed Engineer," Anthropic Careers, 2026. [Online]. Available: https://job-boards.greenhouse.io/anthropic/jobs/5302966008

[5] Scale AI, "Forward Deployed Engineer," Scale AI Careers, 2026. [Online]. Available: https://scale.com/careers/4357818005

[6] B. Beyer, C. Jones, J. Petoff, and N. R. Murphy, Eds., *Site Reliability Engineering: How Google Runs Production Systems*. Sebastopol, CA: O'Reilly Media, 2016.

[7] E. Karakurt and A. Akbulut, "Retrieval-Augmented Generation (RAG) and Large Language Models (LLMs) for Enterprise Knowledge Management and Document Automation: A Systematic Literature Review," *Applied Sciences*, vol. 16, no. 1, art. 368, 2026, doi: 10.3390/app16010368.

[8] M. Mohammadi, Y. Li, J. Lo, and W. Yip, "Evaluation and Benchmarking of LLM Agents: A Survey," arXiv:2507.21504, 2025.

[9] L. Brehme, T. Ströhle, and R. Breu, "Can LLMs Be Trusted for Evaluating RAG Systems? A Survey of Methods and Datasets," in *Proc. IEEE Swiss Conf. Data Science (SDS25)*, 2025, arXiv:2504.20119.

[10] Palantir Technologies, "Forward Deployed Software Engineer," Palantir Careers, 2026. [Online]. Available: https://jobs.lever.co/palantir/dab396d4-2f14-4796-aac0-0d82883dccf0
