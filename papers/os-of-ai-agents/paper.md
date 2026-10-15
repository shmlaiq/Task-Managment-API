# Toward an Agent Operating System: Scheduling, Memory, and Governance Primitives for Concurrent LLM Agent Deployment

**Muhammad Faisal Laiq**

*IEEE Access — Manuscript Draft*

---

## Abstract

Modern large language model (LLM) agents execute as unmanaged processes: they compete for context capacity without scheduling, retain no persistent state without external scaffolding, and invoke tools with permissions far exceeding task requirements. These deficiencies mirror problems that operating system research solved for conventional software decades ago. This paper proposes an Agentic Operating System (AgentOS), a unified architectural framework that maps classical OS abstractions — scheduler, memory manager, device driver, process manager, and security monitor — onto the specific demands of autonomous LLM agents. Five architectural pillars are specified: (1) an LLM Kernel implementing priority-based scheduling and context window isolation; (2) a Hierarchical Memory Subsystem extending working memory through semantic vector retrieval and append-only state logs; (3) a Tool Integration Layer standardizing peripheral access via open protocol standards; (4) a Multi-Agent Orchestration Layer defining inter-agent messaging semantics and conflict arbitration protocols; and (5) a Security and Governance Layer enforcing least-privilege tool access, PII scrubbing, and interrupt-driven human-in-the-loop checkpoints. Each pillar is formally described, positioned against concurrent systems, and evaluated for design trade-offs. The proposed framework addresses the transition from AI as a stateless inference endpoint to AI as a managed, auditable runtime — a foundational shift required before autonomous agents can be deployed reliably at enterprise scale.

**Index Terms** — agent operating system, LLM scheduling, memory management, multi-agent orchestration, Model Context Protocol, security and governance, human-in-the-loop

---

## I. Introduction

Context windows run out. Agents forget. Two separate agents tasked with the same subtask burn through API budget in parallel, with no coordination layer to deduplicate the work. These are not edge cases — they are the default behavior of every LLM agent deployed today without OS-level infrastructure.

The core problem is architectural. Contemporary agent frameworks, including LangChain [17], AutoGen [4], and MetaGPT [5], treat the language model as a remote API to poll and wrap orchestration logic in application code. This design works for single-task, short-horizon pipelines. It breaks for concurrent, stateful, multi-session deployments. A research assistant agent and a code-review agent sharing the same LLM endpoint receive no scheduling priority — the first to submit wins the available context. Neither agent tracks what it committed to an hour ago without custom memory scaffolding. If a tool call fails midway through a multi-step workflow, the intermediate state is lost.

Operating systems faced identical problems with CPU processes in the early decades of computing. Before OS schedulers, programs ran to completion, monopolizing hardware. Before virtual memory, a single process could exhaust physical RAM and crash the system. Before access control lists, any process could overwrite any file. The solutions — scheduling, virtual memory, permission enforcement — became foundational infrastructure that all software now relies on without thinking about it.

LLM agents need the same infrastructure layer. This paper specifies it.

The proposed Agentic Operating System (AgentOS) defines five architectural pillars, each directly addressing a failure mode observed in current agent deployments:

1. **LLM Kernel**: Priority-based scheduling of agent inference requests, context window isolation between concurrent agents, and a standardized system call interface for tool access.
2. **Hierarchical Memory Subsystem**: A three-tier memory model spanning active context (RAM equivalent), semantic vector stores (disk equivalent), and append-only state logs (database commit journal equivalent).
3. **Tool Integration Layer**: Unified peripheral access via the Model Context Protocol [1], with sandboxed execution environments for agents that run code.
4. **Multi-Agent Orchestration Layer**: Structured inter-agent communication protocols and consensus mechanisms for resolving conflicting agent plans.
5. **Security and Governance Layer**: Least-privilege tool scoping, PII scrubbing buffers, and interrupt-driven checkpoints for human-in-the-loop oversight.

The AgentOS does not replace existing agent frameworks. LangChain [17], AutoGen [4], and MetaGPT [5] remain valid application-layer tools. The AgentOS sits below them — a kernel layer they call into, rather than a competing framework at the same level.

The contributions of this paper are as follows:

- We define five formal architectural pillars for an Agentic Operating System, providing the first unified specification that covers scheduling, memory, tool access, multi-agent orchestration, and governance in a single coherent framework.
- We map classical OS abstractions — scheduler, memory hierarchy, device driver, inter-process communication, and access control — directly onto LLM agent requirements, providing principled grounding for each architectural decision.
- We identify five open research challenges — context window fairness under heterogeneous workloads, semantic deduplication in vector stores, tool driver versioning, multi-agent consensus under factual disagreement, and adversarial prompt injection defense — that no existing system currently resolves.

The rest of this paper is organized as follows. Section II surveys related work across four areas: agent frameworks, memory management, tool integration, and multi-agent evaluation. Section III maps OS abstractions to agent primitives. Sections IV-A through IV-E specify each architectural pillar in detail. Section V analyzes component interactions and design trade-offs. Section VI discusses limitations and open research problems. Section VII concludes.

---

## II. Related Work

### A. LLM Agent Frameworks

The ReAct framework [9] established the reasoning-acting loop as the standard agent execution pattern, interleaving chain-of-thought reasoning steps [10] with environment actions to improve decision quality on multi-step tasks. On HotpotQA question answering, ReAct reduces hallucination by grounding intermediate reasoning steps in retrieved Wikipedia facts, outperforming chain-of-thought-only approaches [9]. ReAct is an agent policy — it specifies how one agent should reason and act. It says nothing about how ten agents should share resources or coordinate outputs.

AutoGen [4] extended the single-agent paradigm to multi-agent collaboration via a conversational message-passing model. Agents exchange natural-language messages in configurable topologies, enabling complex workflows spanning code generation, mathematical reasoning, and web navigation [4]. The critical gap: AutoGen provides no admission control or context window scheduling. All agents make concurrent, unconstrained LLM calls. Under heavy load, this degrades into a race condition for inference capacity.

MetaGPT [5] addressed role specialization by assigning agents to software engineering roles — product manager, architect, engineer, QA — with standardized operating procedures (SOPs) governing each role's inputs and outputs. On HumanEval code generation benchmarks, MetaGPT achieves 85.9% Pass@1 [5], outperforming unstructured multi-agent baselines. Coordination in MetaGPT is role-based and hardcoded; two MetaGPT instances deployed in different workflows cannot exchange messages without reconfiguration. The AgentOS generalizes this to a protocol-based orchestration model that is not tied to specific role definitions.

LangChain [17] is the most widely adopted agent application framework, providing composable chains, tool wrappers, and memory components. Its architecture is modular but operates entirely at the application layer — there is no kernel that manages resource allocation across concurrent LangChain agents. The framework leaves scheduling, memory tiering, and access control as developer concerns.

The AIOS system [2] is the closest prior work to the AgentOS proposed here. Mei et al. [2] implement an LLM kernel that provides agent scheduling, context management, and storage management. Empirical evaluation shows AIOS achieves up to 2.1× faster task execution compared to unmanaged agent baselines [2], demonstrating the practical value of kernel-level resource management. AIOS, however, does not specify a governance layer with HITL interrupt semantics, and its memory architecture does not address semantic deduplication or PII scrubbing.

### B. Memory Management for Language Models

The foundational model for LLM inference is stateless: the language model holds no internal state between API calls. All context must be provided in the prompt. This constraint motivates both context-window optimization and external memory systems.

MemGPT [3] is the primary reference for OS-inspired LLM memory management. Packer et al. [3] map OS virtual memory concepts onto LLM context management: the bounded token window serves as fast-access working storage, while off-context external storage provides the persistent, slow-but-unlimited second tier. MemGPT implements a paging mechanism — moving content between tiers based on recency — and introduces interrupt-based control flow where the LLM can request a context swap. MemGPT's paging policy is recency-only. The AgentOS memory subsystem extends this by incorporating semantic relevance as a second retention signal, preventing the eviction of highly relevant older content when a stream of recent but task-irrelevant tokens would otherwise displace it.

Retrieval-Augmented Generation (RAG) [14] provides the vector retrieval substrate for the AgentOS Tier 2 memory. Lewis et al. [14] demonstrate that augmenting language models with dense vector retrieval over non-parametric knowledge stores improves factual accuracy and reduces hallucination on knowledge-intensive tasks. The AgentOS treats the RAG retrieval mechanism as the warm-memory read path: when an agent needs prior context that is not in its active window, the kernel issues a semantic retrieval call against the Tier 2 vector store.

PagedAttention [15] addresses memory fragmentation at the inference engine level. Kwon et al. [15] draw a direct analogy to OS paging and apply it to KV cache management for LLM inference serving. The result is 2–4× throughput improvement compared to prior serving systems [15]. While PagedAttention operates at the inference engine level (below the AgentOS), its design philosophy — treating LLM memory management as an OS problem — validates the OS-analogy approach at a different layer of the stack.

### C. Tool Integration Standards

Toolformer [8] introduced the concept of self-supervised tool learning, training a language model to autonomously insert API calls into its generation stream across five tool categories: calculator, question-answering system, two search engines, translation, and calendar [8]. Toolformer treats tool integration as a generation problem — the model learns when and how to call tools from minimal demonstrations. The AgentOS treats tool integration as an infrastructure problem: define a standard interface so that any agent can call any tool without knowing its implementation details.

The Model Context Protocol (MCP) [1] is the emerging industry standard for this interface. Released by Anthropic in November 2024 as an open standard based on JSON-RPC 2.0, MCP was subsequently adopted by OpenAI, Google DeepMind, and Microsoft, and donated to the Linux Foundation in December 2025 [1]. MCP defines a server/client model: each tool is exposed as an MCP server; agents connect as MCP clients via a standardized protocol. The AgentOS tool integration layer adopts MCP as its native interface, treating each MCP server as a device driver in the classical OS sense.

### D. Multi-Agent Orchestration and Evaluation

Wang et al. [6] survey the LLM agent landscape and identify multi-agent coordination as one of three core unsolved challenges in autonomous agent deployment, alongside persistent memory and generalized task decomposition. Current orchestration approaches divide into centralized (a manager agent dispatches to workers) and decentralized (peer-to-peer negotiation) paradigms. Neither paradigm addresses what happens when two agents produce conflicting plans for the same shared resource — the conflict resolution case is underspecified in the literature.

AgentBench [7] provides the most rigorous multi-environment evaluation of LLM agents to date. Liu et al. [7] test 29 models across 8 environments including operating system interaction, database manipulation, and web browsing. A consistent finding: agent performance degrades sharply on tasks requiring multi-step planning beyond three to five decision points [7]. This failure mode directly motivates the AgentOS orchestration design, which keeps individual agent steps short and delegates multi-step coordination to the dedicated orchestration layer rather than relying on a single agent's extended context.

---

## III. Background: OS Abstractions as Agent Primitives

A conventional operating system manages four physical resources — CPU time, memory, I/O access, and inter-process communication — via a set of well-understood abstractions. Table I maps each abstraction to its LLM agent equivalent.

**Table I: OS-to-Agent Abstraction Mapping**

| OS Abstraction | Traditional Resource | Agent Equivalent |
|---|---|---|
| Scheduler | CPU cycles | LLM context window tokens and inference capacity |
| Memory manager | RAM / disk | Active context window / vector store |
| Device driver | Hardware peripheral | External tool or API server |
| IPC mechanism | Shared memory / socket | Inter-agent structured message bus |
| Access control | File system permissions | Tool scope and PII visibility boundaries |
| Interrupt handler | Hardware signal | Human-in-the-loop approval checkpoint |
| Process control block | CPU register state | Agent Control Record (ACR) |

The analogy is imperfect in one critical respect. Traditional OS processes hold internal state in CPU registers and process memory; restoring a suspended process restores its exact execution state. LLM inference is stateless at the model level — the model holds no memory between calls. The OS must maintain agent state on behalf of the agent, in the same way a traditional kernel stores process state in a process control block (PCB) when a process is not currently scheduled. The AgentOS maintains an **Agent Control Record (ACR)** — a data structure that persists each agent's current task, context tier pointers, tool permissions, interrupt flags, and conversation history — across LLM inference calls.

Chain-of-thought prompting [10] introduced an important insight for the memory mapping: each reasoning step consumes context window tokens. The LLM can hold only a bounded number of reasoning steps in its active window before earlier steps are displaced. The longer the task, the more urgent the question of what to keep in context and what to page out — which is precisely the virtual memory problem applied to agent working memory.

Transformer-based language models [12] operate on sequences bounded by a fixed context window. GPT-4 [11] and other frontier models support context windows of 32K to 128K tokens — substantially larger than earlier models, but still finite. Brown et al. [13] demonstrated that model capability scales predictably with parameter count and training compute; window size does not scale at the same rate, reinforcing the need for external memory management.

---

## IV. The Proposed AgentOS Architecture

### A. Pillar I: LLM Kernel and Scheduling

The LLM kernel treats the language model as a managed processing unit. Multiple agents submit inference requests to the kernel, which schedules them against available context window capacity and compute throughput.

**Priority Queue Scheduling.** Each agent inference request carries a priority tag drawn from {high, normal, low}. The kernel maintains three priority queues and services the highest-priority non-empty queue first. A research agent with a latency-sensitive pipeline receives high priority; a background audit agent processing historical logs receives low priority. Within a priority tier, requests are served in FIFO order.

**Round-Robin Context Allocation.** For equal-priority agents, the kernel divides available context budget across waiting requests in equal slices, preventing any single agent from monopolizing the window. In a 128K-token context model with ten normal-priority agents, each agent receives approximately 12K tokens of working context per scheduling cycle — sufficient for three to five tool calls worth of reasoning. This prevents the starvation condition where a single verbose agent blocks all others.

**Admission Control.** Before accepting a new agent task, the kernel checks whether total queued token demand across all pending requests exceeds the configured capacity threshold. Requests above the threshold are held in a backpressure buffer; the requesting process receives a BUSY signal with a retry-after interval. This prevents the context window equivalent of memory overcommit.

**Context Isolation via ACR Namespacing.** Each agent's context is prefixed with an ACR header that namespaces its working memory from the global system prompt and from other agents' intermediate reasoning. Agent A cannot read tokens allocated to Agent B's context. The ACR header consumes a fixed number of tokens per agent (configurable, default 512 tokens). Operators reduce this overhead by compressing permission declarations; the trade-off between isolation overhead and effective working context is explicit and tunable.

**System Call Interface.** Agents do not call tools directly. They issue typed system calls to the AgentOS kernel, which validates each call against the agent's permission set before routing it:

```
SYS_TOOL_CALL(agent_id, tool_name, parameters, priority)
SYS_MEM_READ(agent_id, query, top_k)
SYS_MEM_WRITE(agent_id, content, metadata)
SYS_AGENT_SPAWN(parent_id, task, permissions_subset)
SYS_HITL_INTERRUPT(agent_id, action_description, risk_level)
```

This interface separates mechanism from policy. The kernel provides routing and isolation; the agent specifies intent. No agent ever needs to know the network address of a tool server, the schema of a memory index, or the current permission configuration of the system.

### B. Pillar II: Hierarchical Memory Management

Two distinct memory pathologies plague LLM agents in practice: **amnesia** (no recollection of prior sessions) and **confabulation** (plausible but false recollection of prior sessions). The hierarchical memory subsystem addresses both. Three tiers are defined:

**Tier 1 — Active Context (Hot Memory).** The model's context window: 8K–128K tokens depending on the deployed model. This is working memory. Content in Tier 1 is processed directly during inference. The kernel manages Tier 1 allocation across agents (Pillar I). Promotion from Tier 2 to Tier 1 is governed by a relevance gate: a content block is promoted only if its cosine similarity to the current task embedding exceeds a configurable threshold θ_hot.

**Tier 2 — Semantic Vector Store (Warm Memory).** A vector index of prior interaction summaries, retrieved documents, and completed task outcomes. Content in Tier 2 is not in the context window; it is retrieved on demand via approximate nearest-neighbor (ANN) search. This tier functions as the agent's persistent storage — it survives across sessions and is shared across agent instances deployed for the same user or organization. The RAG architecture [14] provides the technical substrate: document chunks are embedded, indexed, and retrieved by semantic similarity to the agent's current query. Tier 2 retrieval adds measurable latency per reasoning step that requires prior context; the AgentOS exposes this as a configurable warm-memory read path that short-horizon tasks can bypass entirely.

**Tier 3 — Append-Only State Log (Cold Memory).** Every agent action — tool call issued, tool result received, decision made, error encountered — is appended to an immutable log keyed by (agent_id, timestamp). This log is not searched at inference time; it is the ground truth audit record. The separation of Tier 3 from Tier 2 is deliberate and critical: the vector store may be pruned, re-embedded, or re-indexed over time, but the state log is never modified. This prevents confabulation: the kernel can always verify a claimed prior action against the append-only log, regardless of what the Tier 2 index contains.

**State Commitment Protocol.** Before any irreversible action — file deletion, API write, financial transaction — the kernel issues a commit checkpoint: the agent's current reasoning chain is hashed and appended to Tier 3, creating a verifiable pre-action record. This mirrors the write-ahead log (WAL) pattern in database systems. If the irreversible action fails or is later disputed, the pre-action state is fully recoverable.

**Paging Policy.** The decision of which content to promote from Tier 2 to Tier 1 combines two signals via a weighted scoring function:

$$\text{retain\_score}(c) = \alpha \cdot \text{recency}(c) + (1-\alpha) \cdot \text{sim}(c,\ \tau)$$

where $c$ is a content block, $\tau$ is the embedding of the current agent task, $\text{recency}(c) \in [0,1]$ is a normalized inverse-age score, $\text{sim}(c, \tau)$ is cosine similarity between the block embedding and the task embedding, and $\alpha \in [0,1]$ controls the recency-relevance balance. The default value $\alpha = 0.6$ reflects a moderate recency bias suitable for general-purpose agentic workloads; operators tune this per deployment profile. Long-horizon planning tasks benefit from lower α (relevance dominates, α ≈ 0.3); conversational tasks benefit from higher α (recency dominates, α ≈ 0.8). Pure recency paging — equivalent to α = 1.0, as implemented in MemGPT [3] — is a special case of this policy, not a distinct design.

### C. Pillar III: Tool Integration Layer

Every tool an agent can invoke — code interpreter, web browser, calendar API, database query interface, file system — is a peripheral in the AgentOS model. The Tool Integration Layer standardizes how agents attach to and call these peripherals, in the same way an OS device driver standardizes how processes access hardware.

**MCP as the Standard Driver Interface.** The AgentOS adopts the Model Context Protocol [1] as the universal tool driver interface. Each tool is exposed as an MCP server. The kernel operates as an MCP client and maintains a **Tool Registry** — a runtime table of available tool servers, their declared capabilities, input schemas, and current health status. When an MCP server connects, it registers its callable tools with the kernel; the kernel updates the Tool Registry. Agents query the Tool Registry to discover available tools; they never hardcode tool addresses or schemas.

**Capability Discovery.** Each MCP server declares its capabilities on connection: a list of named tools, each with a parameter schema (JSON Schema format), a human-readable description, and a risk classification tag drawn from the Risk Taxonomy (Pillar V). The kernel uses the risk classification at call time to determine whether the call requires human approval before execution.

**Sandboxed Execution Environments.** Tools that execute arbitrary code — a Python interpreter, a shell command runner, a package installer — operate inside isolated containers. The kernel routes all SYS_TOOL_CALL requests targeting code-execution tools through a container runtime (Docker or WebAssembly), with the container's filesystem, network access, and process namespace restricted to the minimum required for the declared task. A container tasked with parsing a CSV file receives read access to that specific file path and no network access. This enforcement is unconditional — it cannot be disabled by the agent via prompt or by tool configuration.

The failure mode this design prevents is privilege escalation through tool misuse. Without execution environment enforcement, an agent tasked with editing a Markdown file can — through a misconfigured prompt or an adversarial tool result — escalate to shell access. This is not a hypothetical risk: prompt injection attacks embedded in tool outputs [16] are a documented attack vector in current LLM-integrated applications.

**Tool Driver Versioning.** Each MCP server exposes a semantic version identifier. The kernel maintains a compatibility matrix: if an agent was configured with tool version 1.2, the kernel routes its calls to a 1.2-compatible server even if a newer version is registered. This prevents silent API drift, where a tool updates its response schema without the agent being retrained or reconfigured to expect the new format.

### D. Pillar IV: Multi-Agent Orchestration

Single agents are single-threaded reasoners. A task that requires simultaneous web research, code execution, and document drafting cannot be completed by one agent within a reasonable latency budget. The orchestration layer manages agent teams.

**Agent Spawn and Lifecycle.** A parent agent issues SYS_AGENT_SPAWN to create a child agent with a defined task and a permission set that is a strict subset of the parent's own permission set. The kernel creates an ACR for the child, allocates context budget, and begins scheduling it. The child cannot acquire permissions that the parent does not hold — privilege escalation through spawning is architecturally blocked.

When the child completes its task, it returns a structured result to the kernel, which forwards it to the parent and terminates the child's ACR. The parent can block on the child's completion (synchronous spawn) or continue executing and receive the result via the message bus when the child finishes (asynchronous spawn). The spawn model maps directly to fork/join parallelism in conventional concurrent programming.

**Inter-Agent Communication via Structured Message Bus.** Agents communicate through the kernel's message bus, not through shared context. A message carries: sender_id, receiver_id, message_type ∈ {REQUEST, RESPONSE, BROADCAST, INTERRUPT}, a typed payload (JSON Schema validated), and a monotonically increasing sequence number. The kernel routes messages and guarantees in-order delivery within a session.

Shared context — allowing Agent A to read Agent B's active context window — is explicitly disallowed. Shared context creates two problems: information leakage between agents handling different users' data, and reasoning contamination where Agent B's partial results corrupt Agent A's ongoing chain of thought. The message bus enforces information boundaries while still allowing agents to pass results and requests between each other.

**Consensus and Conflict Resolution.** When two agents produce conflicting outputs — Agent A recommends deploying a code change; Agent B (code reviewer) flags a critical regression — the orchestration layer escalates to a **Judge Agent**. The Judge Agent receives both agents' final outputs and the supporting reasoning chains from their Tier 3 logs, and must produce a binary verdict (APPROVE / REJECT / DEFER) with an explicit textual rationale.

The Judge Agent's scope is constrained. It can issue verdicts on the conflict presented to it. It cannot spawn new agents, modify other agents' permission sets, or access resources beyond the two conflicting agents' outputs. This constraint is intentional: a Judge with broad authority is a single point of failure. If the Judge is misconfigured or adversarially prompted, its restricted scope limits the blast radius.

**Manager Agent Pattern.** For hierarchical workflows, a Manager Agent decomposes a high-level goal into subtasks, spawns Worker agents for each, monitors their progress through status polls on the message bus, and merges their outputs into a final result. This pattern generalizes MetaGPT's role-based SOPs [5] to any workflow topology without requiring predefined roles.

### E. Pillar V: Security and Governance

Security in the AgentOS is not an external filter applied after the fact — it is embedded in the kernel's system call interface. Every agent action passes through a governance check before execution. The check is unconditional and cannot be bypassed by application code.

**Least-Privilege Tool Scoping.** Each agent receives a Permission Set at spawn time, specifying the exact tools it may call and the operations it may perform on each tool. A document summarization agent receives READ permission on the document store and WRITE permission on the output queue. Nothing else. The kernel returns PERMISSION_DENIED on any SYS_TOOL_CALL that references a tool or operation outside the agent's permission set.

Permission sets are hierarchically scoped: a child agent holds at most the permissions its parent holds, never more. This enforces least privilege transitively across the full agent dependency tree. A compromised child agent cannot access resources that its parent could not access.

**PII Scrubbing Buffer.** Before any agent output is forwarded to a cloud LLM endpoint, the kernel passes the content through a PII scrubbing buffer. The buffer applies named entity recognition (NER) to detect and replace identifying entities — names, email addresses, phone numbers, account identifiers, location data — with anonymized tokens. The original content is stored in Tier 3 under encryption; the cloud LLM receives only the scrubbed version.

When the LLM response references an anonymized token, the kernel reverses the substitution before returning the result to the agent. The cloud provider never processes raw PII. This matters because the current default in most agent frameworks is to transmit the entire conversation context — including any PII present in tool results or user inputs — to cloud endpoints without scrubbing.

**Human-in-the-Loop Interrupts.** Some agent actions carry irreversible real-world consequences: spending money, sending communications, deleting data, deploying code, modifying production infrastructure. For these actions, the kernel implements OS-style interrupt handling. A **Risk Taxonomy** classifies actions by consequence severity:

**Table II: AgentOS Risk Taxonomy**

| Risk Level | Example Actions | Default Kernel Policy |
|---|---|---|
| Low | Read file, query database, semantic search | Auto-approve, log |
| Medium | Write file, create calendar event, append data | Auto-approve, log with alert |
| High | Send email, API write, modify shared state | HITL interrupt required |
| Critical | Delete data, execute shell command, deploy to production | HITL interrupt + explicit confirmation text |

When an agent issues a SYS_TOOL_CALL classified as High or Critical, the kernel suspends the agent (preserving its ACR state), sends a structured notification to the designated human approver with a description of the proposed action and its estimated impact, and blocks execution until approval or denial is received. An unanswered interrupt times out to denial. The timeout window is configurable per deployment context.

This mirrors hardware interrupt handling: the processor suspends the current process, services the interrupt, and then resumes — or terminates the process if the interrupt cannot be serviced. The agent resumes execution from the exact state it was suspended in, with the approval result injected into its context as an additional input.

The HITL mechanism has a latency cost proportional to human response time. For interactive deployments, this cost is acceptable and expected. For high-frequency automated pipelines, HITL interrupts at the High risk level may be impractical. The Risk Taxonomy is the operator's lever for managing this trade-off: teams that accept reduced oversight for automation can reclassify High actions to Medium. The downside is explicit and documented, not hidden.

---

## V. Architecture Analysis

### A. Lifecycle of an Agent Request

The five pillars interact through the kernel. A complete end-to-end lifecycle proceeds as follows:

1. A user submits a task to the AgentOS interface. The kernel creates an ACR for the primary agent, assigns it a context budget from the scheduling queue, and loads task-relevant content from Tier 2 via semantic retrieval (SYS_MEM_READ).
2. The agent executes a reasoning step, generating a tool call via SYS_TOOL_CALL.
3. The kernel validates the call against the agent's permission set (Pillar V, Least Privilege). If the tool is outside the permission set: PERMISSION_DENIED, agent receives error.
4. The kernel checks the tool's risk classification (Pillar V, Risk Taxonomy). If High or Critical: HITL interrupt raised, agent suspends, human notified.
5. Upon approval (or auto-approve for Low/Medium), the kernel passes the call through the PII scrubbing buffer and routes it to the appropriate MCP server (Pillar III) inside a sandboxed container if required.
6. The tool result returns to the kernel, is appended to Tier 3 (Pillar II, state commit), and is injected into the agent's active context (Tier 1).
7. If the agent issues SYS_AGENT_SPAWN (Pillar IV), the kernel creates a child ACR with a permission subset and begins scheduling the child in parallel.
8. Child results return via the structured message bus. If child and parent outputs conflict, a Judge Agent is invoked (Pillar IV, consensus).
9. Upon task completion, the kernel writes the final ACR state to Tier 3, releases context budget to the scheduling pool, and returns the result.

### B. Design Trade-offs

Three trade-offs dominate the AgentOS design space:

**Isolation vs. throughput.** Context window namespacing (Pillar I) prevents cross-agent contamination but consumes tokens for ACR headers. In a 128K-token window, a 512-token ACR overhead per agent means ten concurrent agents consume 5K tokens in metadata before any task content. At agent counts above twenty, this overhead is non-trivial. Operators can reduce it by compressing permission declarations; the isolation guarantee cannot be weakened without a redesign.

**Memory freshness vs. retrieval latency.** Tier 2 semantic retrieval (Pillar II) adds latency to any agent reasoning step that requires prior context from outside the active window. Short-horizon tasks that fit entirely within Tier 1 should bypass Tier 2. Long-horizon tasks requiring context from prior sessions cannot operate without it. The AgentOS makes this bypass configurable per task class, rather than forcing all tasks through the retrieval path.

**Oversight vs. automation speed.** HITL interrupts (Pillar V) provide the strongest correctness guarantee for irreversible actions but introduce latency that scales with human response time rather than system speed. For fully automated pipelines, HITL at the High-risk level is impractical. The Risk Taxonomy is the primary operator control for this trade-off. The design does not prescribe a single policy — it provides the mechanism and makes the choice explicit.

### C. Comparison with Existing Systems

Table III compares AgentOS against four concurrent systems across the five architectural pillars.

**Table III: AgentOS vs. Existing Systems**

| System | Scheduling | Memory Mgmt | Tool Interface | Multi-Agent | Governance |
|---|---|---|---|---|---|
| AIOS [2] | Priority queue | Context manager | Custom | Limited | None |
| MemGPT [3] | None | Hierarchical (recency) | Custom | None | None |
| AutoGen [4] | None | Conversation buffer | None | Message-based | None |
| MetaGPT [5] | None | None | None | Role-based SOP | None |
| LangChain [17] | None | Pluggable | Tool wrappers | Chain-based | None |
| **AgentOS** | **Priority + RR** | **3-tier + append log** | **MCP standard** | **Protocol + consensus** | **Full (HITL + least-priv + PII)** |

No existing system addresses all five pillars simultaneously. AIOS [2] is the closest, covering scheduling and context management with demonstrated performance gains [2], but lacks governance and PII handling. MemGPT [3] provides the most sophisticated memory model but operates as a single-agent system with custom tool integrations. AutoGen [4] and MetaGPT [5] address multi-agent coordination at the application layer but provide no kernel-level resource management or security enforcement. LangChain [17] provides tool integration but treats all other concerns as application-layer responsibilities.

The AgentOS closes this gap by integrating all five pillars under a single kernel interface.

### D. Theoretical Analysis

Although no running AgentOS implementation exists at the time of writing, the architectural choices permit formal analysis of three core properties: scheduling complexity, paging policy dominance, and context waste reduction.

**Scheduling Complexity.** The priority queue used by the LLM Kernel (Pillar I) processes agent scheduling decisions in O(log n) per enqueue/dequeue operation, where n is the number of concurrently active agents. The round-robin fallback for equal-priority agents adds O(1) per dispatch step. Combined, the scheduler's per-cycle cost is O(n log n) to re-sort priorities after each completed agent turn — the same asymptotic complexity as process scheduling in Linux's Completely Fair Scheduler [7]. At n = 100 concurrent agents, this represents a negligible overhead relative to the LLM inference latency that dominates each agent turn.

**Paging Policy Dominance.** The retain_score function Pareto-dominates pure recency paging (MemGPT [3], α = 1.0) on tasks where semantic relevance and recency are not perfectly correlated. Formally: let C be the set of content blocks competing for the Tier 1 budget, and let R ⊂ C be the set of blocks that are both recent and relevant, while S ⊂ C \ R are blocks that are relevant but not recent. Under pure recency paging, blocks in S are evicted whenever Tier 1 is full. Under AgentOS paging with α < 1, blocks in S are retained if their sim(c, τ) score is high enough to compensate for their lower recency score. The net effect is that tasks requiring long-horizon context — legal analysis, multi-session research, extended code refactoring — retain task-critical older context that pure recency paging would discard.

**Context Waste Reduction.** In an n-agent system without the ACR namespace prefix, every agent's intermediate reasoning pollutes the shared context. The ACR header confines each agent's working tokens to its allocated slice c_per_agent = ⌊C/n⌋ − c_ACR. Wasted tokens — tokens that belong to Agent A's reasoning but appear in Agent B's context — drop from O(n · context_size) in the unmanaged case to O(c_ACR · n) with ACR namespacing. For a 128K-token context window shared across 10 agents with c_ACR = 512 tokens, the waste bound drops from 128K tokens (worst-case full context leak) to 5,120 tokens — a 25× reduction in maximum inter-agent context contamination (derived: 128,000 / 5,120 = 25).

---

## VI. Limitations and Open Challenges

The AgentOS framework is a conceptual specification. No production implementation exists at the time of writing; the architecture has not been empirically validated on a live workload. Five classes of limitation require honest acknowledgment.

**Implementation gap.** The ACR format, PII scrubbing NER pipeline, Risk Taxonomy enforcement engine, and MCP-based Tool Registry are specified at the interface level. Actual performance figures — scheduling latency under concurrent load, Tier 2 retrieval accuracy versus baseline, HITL interrupt overhead — cannot be reported without a running implementation. The AIOS system [2] provides the closest empirical data point, with measured 2.1× throughput gains from kernel-level scheduling [2], but AIOS does not implement governance or PII scrubbing, so its numbers cannot be extrapolated directly.

**Context window fairness under heterogeneous workloads.** The round-robin allocation policy (Pillar I) treats all agents equally. A legal document analysis agent requires dense context — 50K tokens of case history — to function. An arithmetic calculator agent needs 200 tokens. Allocating equal slices wastes the calculator agent's budget and starves the legal agent. A workload-aware scheduling policy, analogous to the Completely Fair Scheduler (CFS) in Linux, would better serve heterogeneous agent populations. Designing such a scheduler with formal starvation-freedom guarantees for LLM workloads is an open problem.

**Semantic deduplication in the vector store.** The Tier 2 vector store accumulates entries from all agent sessions. Without deduplication, semantically equivalent content — the same background fact retrieved by ten independent agents — occupies redundant index space and pollutes ANN retrieval results by returning near-duplicate candidates. Online semantic deduplication (identifying and merging near-duplicate entries at insertion time) requires approximate set-membership tests over high-dimensional embedding vectors. Exact deduplication is computationally prohibitive at index scale; approximate methods introduce false merge risk. No mature solution exists.

**Multi-agent consensus under factual disagreement.** The Judge Agent mechanism (Pillar IV) assumes that conflict between agents is resolvable given their outputs and reasoning chains. This assumption breaks when the conflict originates from a factual divergence — both agents retrieved different context from Tier 2 and reached internally consistent but mutually incompatible conclusions. The AgentOS specifies a three-step escalation for this case: (1) the kernel issues a targeted re-retrieval from Tier 2 using the conflicting claim from each agent as separate query vectors; (2) if the re-retrieval surfaces a single context block that subsumes both conflicting claims, the Judge Agent issues an APPROVE verdict citing that block as the authoritative source; (3) if re-retrieval does not converge — both queries return semantically distinct, non-overlapping context — the system escalates to HITL, attaching both agents' full reasoning chains and the divergent retrieved blocks to the human operator's review queue. This three-step protocol bounds the escalation cost: re-retrieval is always attempted before human involvement, and HITL is triggered only when the information needed to resolve the conflict is genuinely absent from the system's memory.

**Adversarial prompt injection in tool outputs.** Prompt injection attacks [16] embedded in tool results — content returned by a web browser, database query, or file reader that contains instructions designed to override the agent's system prompt — are a live threat in LLM-integrated applications. The PII scrubbing buffer (Pillar V) defends against data leakage but does not detect adversarial instructions. A separate injection detection layer, operating on tool outputs before they reach the agent's context, is a security requirement for any production deployment. The AgentOS defines the required integration point — tool outputs pass through a sanitization buffer before the SYS_TOOL_CALL response is written into the agent's context — but the detection algorithm (classifier, regex, or LLM-based judgment) is left to the operator to configure per deployment risk profile. Liu et al. [16] demonstrate that injection attacks can cause agents to exfiltrate data, execute unauthorized commands, and impersonate users — none of which the current governance layer prevents at the input filtering stage without a configured detection algorithm in place.

---

## VII. Conclusion

LLM agents deployed without OS-level infrastructure face the same failure modes that unmanaged processes faced before operating systems existed: resource contention, state loss, privilege overreach, and no mechanism for human intervention. Five architectural pillars directly address these failure modes.

The LLM kernel prevents context monopolization by applying priority-based scheduling and per-agent isolation — a well-understood OS technique applied to a novel resource (context window tokens). The hierarchical memory subsystem prevents both amnesia and confabulation by separating the mutable vector index from the immutable state log. The MCP-based tool layer replaces ad hoc tool integrations with a standardized driver interface that enables any agent to use any tool without custom connectors. The orchestration layer supports agent teams without shared-context contamination, and the Judge Agent mechanism provides a defined path for conflict resolution. The governance layer makes least-privilege behavior the architectural default rather than an optional enhancement.

The framework is a specification, not a product. Several challenges — context window fairness scheduling, semantic deduplication, multi-agent consensus under factual disagreement, and adversarial injection defense — remain open. These are the correct problems to work on next. The field needs evaluation benchmarks that test agent schedulers, memory paging policies, and HITL latency trade-offs in the same way AgentBench [7] tests raw task performance.

The transition from AI as a stateless inference tool to AI as a managed, auditable runtime is not optional — it is a prerequisite for enterprise deployment at the reliability, compliance, and safety standards that production environments require. The Agent Operating System is the infrastructure layer that makes this transition possible.

---

## Acknowledgments

The author thanks the open-source communities behind AIOS [2], MemGPT [3], AutoGen [4], and the Model Context Protocol [1] for making their technical designs publicly available. This work received no external funding.

---

## References

[1] Anthropic, "Model Context Protocol," Open Standard, Nov. 2024. [Online]. Available: https://modelcontextprotocol.io. [Accessed: Apr. 8, 2026].

[2] K. Mei, X. Zhu, W. Xu, W. Chen, T. He, G. Yao, J. Guo, and Y. Zhang, "AIOS: LLM Agent Operating System," in *Proc. Conf. Language Modeling (COLM)*, 2025. arXiv:2403.16971.

[3] C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, and J. E. Gonzalez, "MemGPT: Towards LLMs as Operating Systems," arXiv:2310.08560, 2023.

[4] Q. Wu, G. Bansal, J. Zhang, Y. Wu, S. Zhang, E. Zhu, B. Li, L. Jiang, X. Zhang, and C. Wang, "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," arXiv:2308.08155, 2023.

[5] S. Hong, X. Zhuge, J. Chen, X. Cheng, Y. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran, L. Xiao, C. Wu, and J. Schmidhuber, "MetaGPT: Meta Programming for a Multi-Agent Collaborative Framework," arXiv:2308.00352, 2023.

[6] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang, X. Chen, Y. Lin, W. X. Zhao, Z. Wei, and J. Wen, "A Survey on Large Language Model based Autonomous Agents," arXiv:2308.11432, 2023.

[7] X. Liu, H. Yu, H. Zhang, Y. Xu, X. Lei, H. Lai, Y. Gu, H. Ding, K. Men, K. Yang, S. Zhang, X. Deng, A. Zeng, Z. Du, C. Zhang, S. Shen, T. Zhang, Y. Su, H. Sun, M. Sun, H. Dong, and J. Tang, "AgentBench: Evaluating LLMs as Agents," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2024. arXiv:2308.03688.

[8] T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, L. Zettlemoyer, N. Cancedda, and T. Scialom, "Toolformer: Language Models Can Teach Themselves to Use Tools," arXiv:2302.04761, 2023.

[9] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao, "ReAct: Synergizing Reasoning and Acting in Language Models," in *Proc. Int. Conf. Learning Representations (ICLR)*, 2023. arXiv:2210.03629.

[10] J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou, "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2022. arXiv:2201.11903.

[11] OpenAI, "GPT-4 Technical Report," arXiv:2303.08774, 2023.

[12] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention Is All You Need," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2017. arXiv:1706.03762.

[13] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal, A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh, D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler, M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish, A. Radford, I. Sutskever, and D. Amodei, "Language Models are Few-Shot Learners," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2020. arXiv:2005.14165.

[14] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in *Proc. Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2020. arXiv:2005.11401.

[15] W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica, "Efficient Memory Management for Large Language Model Serving with PagedAttention," in *Proc. ACM Symp. Operating Systems Principles (SOSP)*, 2023. arXiv:2309.06180.

[16] Y. Liu, G. Deng, Y. Li, K. Wang, Z. Wang, X. Wang, T. Zhang, Y. Liu, H. Wang, Y. Zheng, and Y. Liu, "Prompt Injection attack against LLM-integrated Applications," arXiv:2306.05499, 2023.

[17] H. Chase, "LangChain," GitHub, Oct. 2022. [Online]. Available: https://github.com/langchain-ai/langchain. [Accessed: Apr. 8, 2026].
