# OpenClaw as an AI Agentic OS

**Author:** Muhammad Faisal Laiq
**Target Venue:** IEEE Access
**Date:** April 2026

---

## Abstract

Contemporary autonomous agent deployments face a fundamental architectural mismatch: Large Language Model (LLM) reasoning capacity has outpaced the infrastructure supporting it. Agents today share no common substrate for scheduling concurrent tasks, managing memory beyond a single context window, controlling tool access permissions, or enforcing security boundaries against adversarial channel inputs. OpenClaw, a self-hosted open-source platform created by Peter Steinberger and sponsored by OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, and Convex, addresses this gap by functioning as an operating system for personal AI employees. This paper provides the first formal academic analysis of OpenClaw through classical OS theory. We map five OS primitives—process management, memory management, device management, scheduling, and access control—onto OpenClaw's corresponding architectural components: the WebSocket Gateway, a three-tier memory hierarchy (MEMORY.md, daily journals, and Quantized Memory Distillation (QMD) vector store), a three-tier tool escalation model (Skills, Model Context Protocol (MCP) servers, and Plugins), the heartbeat and cron scheduling subsystem, and the three-tier security stack (Tool Profiles, Plugin Hooks, and NemoClaw isolation). We derive a formal cost bound showing heartbeat batching reduces daily inference turns by a factor of N over equivalent cron-based scheduling, confirmed at 5× for the default configuration. We analyze the Privacy Router pattern in NemoClaw, which achieves API credential isolation through network namespace separation—a strictly stronger guarantee than application-layer access control. A complete cross-platform installation guide is provided alongside six limitations. OpenClaw satisfies two formal OS-level guarantees—scheduled inference cost reduction by factor N and API credential non-interference—unmatched by any compared framework.

**Index Terms:** AI agents, agentic operating system, agent scheduling, memory management, multi-agent systems, agent security, personal AI employee, Model Context Protocol

---

## I. Introduction

The operating systems field spent three decades solving resource allocation problems that application developers could not solve individually. Process isolation, preemptive scheduling, virtual memory, and access control matrices emerged not from theoretical interest but from operational necessity: when multiple programs shared hardware, uncoordinated access produced corruption, starvation, and privilege escalation. The AI agent field stands at the same inflection point.

Modern large language model (LLM)-based agents require persistent memory that survives context window boundaries, concurrent execution without state corruption, granular tool access permissions, and security enforcement that cannot be bypassed by adversarial content in message channels. Framework-level solutions—LangChain [18], AutoGen [6], MetaGPT [7]—address task composition but leave resource management entirely to the developer. Each framework reinvents scheduling, memory, and access control independently, producing incompatible primitives that cannot share infrastructure across deployments.

OpenClaw, an open-source platform created by Peter Steinberger with sponsorship from OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, and Convex [1], attacks this problem at the infrastructure layer. Rather than providing a programming framework, it acts as a gateway daemon sitting between LLM providers and communication channels—managing agent lifecycle, memory persistence, tool permissions, scheduling, and security in a unified runtime process. The platform carries over 350,000 GitHub stars and operates under the explicit architectural metaphor that the Gateway is a kernel, workspace files are firmware, plugins are device drivers, and sessions are process memory [1]. NVIDIA extended this architecture into NemoClaw, a derivative security isolation layer [2].

No prior academic work has formalized OpenClaw's architecture against classical OS theory, derived formal properties from its scheduling primitives, or analyzed the security guarantees of the NemoClaw Privacy Router. This paper addresses that gap.

The contributions are four:

1. **Formal OS-to-agent primitive mapping.** We construct a rigorous correspondence between five classical OS abstractions and their OpenClaw equivalents, establishing the Agentic OS concept on firm architectural footing.

2. **Five-pillar architecture specification.** We formally specify OpenClaw's process management (WebSocket Gateway), memory management (three-tier hierarchy), tool management (three-tier escalation), scheduling (heartbeat/cron/spawn), and security (Profile/Hook/NemoClaw) subsystems.

3. **Scheduling cost bound.** We prove that heartbeat batching achieves a factor-of-N reduction in daily inference turns compared to N equivalent cron jobs at equal check frequency, and confirm the 5× bound for the documented default configuration.

4. **Privacy Router security analysis.** We show that NemoClaw's API credential isolation through network namespace separation satisfies a formal non-interference property that application-layer tool profiles cannot provide.

The remainder is organized as follows. Section II surveys related work. Section III establishes background. Section IV specifies the five-pillar architecture. Section V provides the installation guide. Section VI analyzes the architecture. Section VII addresses limitations. Section VIII concludes.

---

## II. Related Work

### A. Agent Orchestration Frameworks

LangChain [18], introduced by Harrison Chase in 2022, pioneered the chain abstraction for LLM applications, providing composable primitives for tool use, memory, and retrieval. It operates as a library rather than a runtime—tool permissions, session management, and scheduling remain the developer's responsibility. AutoGen [6] from Microsoft Research enables multi-agent conversations through customizable conversable agents that combine LLM inference, human input, and tool execution. MetaGPT [7] encodes standardized operating procedures into multi-agent workflows, achieving a Pass@1 rate of 85.9% [7] on code generation benchmarks, but its scope is workflow definition rather than runtime resource management. LangGraph extends LangChain with stateful cyclic graphs but similarly provides no OS-level abstractions for concurrent execution or security enforcement. A comprehensive survey of LLM-based autonomous agent architectures [8] categorizes planning, memory, tool use, and multi-agent coordination as four key capability dimensions and identifies runtime resource management as a systematic gap across all current frameworks. Systematic evaluation across eight interactive environments [9] confirms that even frontier LLMs underperform humans on complex tool-use tasks—evidence that model capability alone does not substitute for production-grade tool management infrastructure. OpenClaw differs structurally from all these systems: it provides not a programming model but a managed runtime substrate that handles resource concerns beneath any application logic. No other system in this category manages agent resources at runtime.

### B. OS-Inspired Agent Systems

The closest academic antecedents to OpenClaw's architecture are AIOS [4] and MemGPT [5]. AIOS proposes an operating system kernel for LLM-based agents, isolating scheduling, context management, memory, and access control into a dedicated kernel layer distinct from agent application logic. AIOS demonstrates up to 2.1× throughput improvement [4] over unstructured agent execution by managing concurrent agent requests through an LLM-aware scheduler. MemGPT [5] draws an analogy between virtual memory in operating systems and virtual context windows in LLMs, introducing a two-tier memory model—fast in-context storage and slow external storage—managed through OS-inspired interrupt signals. OpenClaw extends and concretizes both contributions: the Gateway implements the scheduling and process management layer described by AIOS [4], while the MEMORY.md plus QMD vector store architecture operationalizes MemGPT's two-tier memory model [5] in a deployed, production-configurable system. Neither predecessor ships production security.

### C. Tool and Protocol Standards

Toolformer [10] demonstrated that language models can autonomously learn to invoke external APIs through self-supervised training, establishing the theoretical basis for tool-using agents. ReAct [11], published at ICLR 2023, interleaves reasoning traces with tool calls, enabling agents to select tools based on intermediate reasoning and achieving a 34% absolute improvement over imitation learning on interactive decision-making benchmarks [11]. The Model Context Protocol (MCP) [3], released by Anthropic in November 2024, provides a standardized JSON-RPC client-server interface for tool access that any agent runtime can adopt without framework-specific integration. OpenClaw integrates MCP through the mcporter bridge [2], making the protocol's tool inventory available to agents via three transport types: stdio, SSE, and streamable-HTTP. MCP alone does not define execution policy. Toolformer's self-supervised training approach is not reproducible on closed-model deployments, limiting adoption to settings where model weights are accessible. The Agent Client Protocol (ACP) extends this model further, enabling OpenClaw agents to spawn and steer Claude Code sessions as external subagents.

### D. Agent Security and Governance

Liu et al. [15] formally characterized prompt injection attacks against LLM-integrated applications, demonstrating that 31 of 36 tested production applications were susceptible, including systems with millions of users. This threat is the primary adversarial vector for deployed agents receiving messages from untrusted channel participants. MITRE ATLAS [17], the adversarial threat landscape for AI systems, provides a structured taxonomy of attack tactics and techniques specific to machine learning deployments. OpenClaw's security architecture explicitly references MITRE ATLAS [2] as its threat modeling foundation. vLLM [14] addressed memory management for LLM inference serving through PagedAttention, improving throughput by 2–4× [14] over prior systems; this work motivates efficient resource management at the serving layer that complements OpenClaw's agent-layer scheduling. Agent-layer security has no equivalent treatment in this literature. No prior published work has formally analyzed NemoClaw's Privacy Router pattern or its network-isolation-based credential security properties.

---

## III. Background

### A. Classical OS Primitives

An operating system mediates access to shared hardware through five canonical abstractions that have remained stable across five decades of system design.

*Process management* creates isolated execution contexts, tracks per-process state, and arbitrates CPU time through a scheduler that allocates processor slices across runnable processes. Process isolation prevents one process's memory writes from corrupting another's address space.

*Memory management* partitions address space into per-process regions, virtualizes physical memory through paging, and enforces read/write/execute permissions per memory page. Virtual memory extends addressable space beyond physical RAM by migrating cold pages to storage and loading them on demand.

*Device management* abstracts hardware peripherals behind uniform driver interfaces, translating device-specific protocols to a common read/write I/O model. The driver layer allows application software to interact with diverse hardware without knowledge of device-specific details.

*Scheduling* allocates CPU time across runnable processes. Preemptive schedulers interrupt running processes at regular intervals, preventing any single process from monopolizing processor time. Priority-based scheduling allocates more CPU time to higher-priority processes.

*Access control* enforces permissions through a reference monitor that intercepts every resource access and consults a policy matrix—typically user identity × resource × operation—before granting or denying the request.

### B. The Agentic OS Primitive Mapping

LLM-based agents face structurally identical resource management problems in a software substrate. Table I maps each classical OS primitive to its agent-domain equivalent and to the corresponding OpenClaw component.

**Table I: OS Primitive → Agent Equivalent → OpenClaw Component**

| OS Primitive | Agent Domain Equivalent | OpenClaw Component |
|---|---|---|
| Kernel | Central coordination process | WebSocket Gateway daemon |
| Process | Agent session (isolated reasoning context) | Session scopes (per-peer, per-channel-peer) |
| RAM | Active context window (in-flight reasoning) | MEMORY.md (prompt-space storage) |
| Virtual memory | Persistent memory beyond context window | QMD vector store + daily journals |
| Firmware | Identity and behavioral constraints | SOUL/IDENTITY/AGENTS/TOOLS/USER.md |
| Device driver | External tool or service adapter | Plugin (native/bundle) / Skill / MCP |
| Scheduler | Agent invocation controller | Heartbeat + Cron subsystem |
| Access control | Tool and channel permission enforcer | Tool Profiles → Plugin Hooks → NemoClaw |

The mapping is not merely metaphorical. Each OpenClaw component exhibits the same resource management behavior as its OS analog: the Gateway arbitrates concurrent message processing as a scheduler arbitrates CPU slices; MEMORY.md provides fixed-capacity fast storage as RAM does; the QMD vector store extends addressable memory as virtual memory extends physical RAM.

### C. OpenClaw System Overview

OpenClaw was created by Peter Steinberger as a personal learning project and evolved through three prior identities—Warelay, Clawdbot, and Moltbot—before reaching its current form. The platform is implemented in TypeScript under the MIT license and has accumulated over 350,000 GitHub stars with sponsorship from OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, and Convex [1]. NVIDIA developed NemoClaw as a derivative security isolation layer. The design philosophy, documented in VISION.md [1], prioritizes hackability (TypeScript for broad developer familiarity), explicit configuration (terminal-first setup exposing all security choices), and local-first data sovereignty (default loopback binding, credentials stored on operator hardware).

The core architectural unit is a WebSocket gateway daemon that binds to localhost port 18789 by default, connecting LLM provider APIs on one side to 30+ messaging platform integrations on the other, with an embedded Pi agent runtime in RPC mode executing between them. This hub-and-spoke topology is illustrated in Fig. 1.

> **Fig. 1** — Hub-and-spoke system architecture: WebSocket Gateway at center; messaging channels (WhatsApp, Slack, Discord, Telegram, 30+ others) on the left; LLM providers (Anthropic, OpenAI, Gemini, local models) on the right; three-tier security stack (Tool Profiles → Plugin Hooks → NemoClaw) below. Source: `figures/fig1_system_architecture.pdf`

---

## IV. OpenClaw Architecture: Five Pillars

The five-pillar architecture and its OS analog labels are shown in Fig. 2.

> **Fig. 2** — Five-pillar vertical stack: Process Management (WebSocket Gateway), Memory Management (3-tier hierarchy), Tool Management (Skill → MCP → Plugin), Scheduling (Heartbeat + Cron + spawn), Security (Profile → Hook → NemoClaw). OS analog labels shown at right. Source: `figures/fig2_five_pillars.pdf`

### A. Pillar 1: Process Management

OpenClaw's kernel analog is a WebSocket gateway daemon running as a background service—LaunchAgent on macOS, systemd user service on Linux. The gateway coordinates three subordinate subsystems: the Pi agent runtime executing in remote procedure call (RPC) mode with tool and block streaming, the channel multiplexer routing messages across messaging platforms, and the Control UI web dashboard at http://127.0.0.1:18789.

**Session isolation** implements the process isolation analogy. Four session scoping levels provide increasing isolation:

- `main`: all direct messages collapse to one shared session per agent
- `per-peer`: each sender receives an isolated session across all channels
- `per-channel-peer`: each sender receives an isolated session per channel
- `per-account-channel-peer`: full isolation across sender × channel × account triple

Each isolated session maintains its own context window, message history, and tool call state. Session isolation is strict. Identity changes (edits to SOUL.md or IDENTITY.md) take effect in new sessions only; existing sessions retain the prior identity until reset with `/new`.

**Two-layer concurrency** mirrors the OS distinction between per-process FIFO queues and the global CPU scheduler. The analogy holds exactly. The Session Lane enforces sequential message processing per sender, preserving conversation coherence. The Global Lane maintains a configurable pool of parallel session slots, defaulting to four concurrent sessions. Under peak load with N active senders and pool size k, maximum queue depth reaches ⌈N/k⌉ sessions; empirical wait times reach 3–8 seconds at N=5, k=4 [1].

**Control-plane rate limiting** enforces a maximum of three write operations per 60-second window per deviceId+clientIp tuple. Excess requests receive an UNAVAILABLE response with a `retryAfterMs` backoff hint, preventing runaway automation from corrupting gateway configuration.

### B. Pillar 2: Memory Management

OpenClaw implements a three-tier memory hierarchy that maps directly onto the OS hierarchy of fast volatile storage, warm addressable storage, and cold archival storage.

**Tier 1 — MEMORY.md (hot storage).** A curated Markdown file loaded at the start of every agent message. It occupies prompt space and is therefore hard-bounded by the LLM's context window—the agent's RAM analog. Documentation advises keeping this file concise: "it is a curated notebook, not a dump file" [1]. Redundant entries inflate context consumption without contributing reasoning value. Chain-of-thought reasoning [12] depends on access to intermediate step records; MEMORY.md entries that omit reasoning traces can cause the agent to repeat failed approaches across sessions, since the outcome is recorded without the reasoning path that led to it. Users trigger writes through explicit prefixes ("Save in memory:") rather than natural language requests that may only acknowledge intent without triggering a file write.

**Tier 2 — Daily journals (warm storage).** Date-stamped Markdown files (YYYY-MM-DD.md) stored at `~/.openclaw/agents/<agentId>/sessions/`. The current and previous day's journals load automatically at session start. Entries older than yesterday reside on disk, addressable only through the explicit memory search interface—the virtual memory analog, where recent pages stay warm and older pages require a page fault equivalent to retrieve.

**Tier 3 — QMD vector store (cold storage).** The QMD (Quantized Memory Distillation) engine applies the retrieval-augmented generation pattern [16] in a locally quantized form, combining vector similarity matching with keyword-based search across all historical journal entries to surface relevant context without loading full journal histories into the active context window. Cross-agent memory access is supported through `extraCollections` configuration, allowing one agent to query another agent's session transcripts while maintaining independent primary stores. The full three-tier hierarchy is shown in Fig. 4.

> **Fig. 4** — Three-tier memory hierarchy pyramid: MEMORY.md (top, hot/prompt-space), Daily journals (middle, warm/automatic), QMD vector store (bottom, cold/semantic retrieval). Firmware identity files shown as a separate base layer. Source: `figures/fig4_memory_hierarchy.pdf`

**Firmware layer.** Five workspace identity files load on every message regardless of session state: SOUL.md (persona, tone, behavioral boundaries), IDENTITY.md (name, role, display identity), AGENTS.md (operating rules and priorities), TOOLS.md (tool guidance notes), and USER.md (operator information). These files are firmware—not session memory—because their effect persists across session boundaries without explicit recall.

**Context engine and session pruning.** Extended conversations trigger automatic compaction: the context engine summarizes older turns and commits key facts to MEMORY.md before releasing prompt space. This is the agent-domain analog of OS page replacement—when addressable context fills, least-recently-used turns are evicted and their essence committed to slower persistent storage.

### C. Pillar 3: Tool and Capability Management

OpenClaw manages external tool access through a three-tier escalation hierarchy mirroring the OS device driver model.

**Tier 1 — Skills (knowledge layer).** A Skill is a directory containing a SKILL.md file encoding knowledge or behavioral instructions without executable code. Skills teach agents how to handle task categories without providing new runtime capabilities—the firmware layer of device management. The SKILL.md format is cross-platform, functioning identically on OpenClaw and Claude Code. Skills are snapshotted when a session starts; installing a skill requires a gateway restart before it becomes available in new sessions [1].

The escalation rule: use a Skill when the agent needs knowledge. If the agent needs authenticated service access, escalate to MCP. If gateway behavior itself must be modified, escalate to a Plugin.

**Tier 2 — MCP servers (service layer).** MCP [3] exposes structured tool interfaces through JSON-RPC over three transports: stdio (local processes via npm or Python packages), SSE (remote HTTP with Server-Sent Events), and streamable-HTTP (remote streaming). OpenClaw integrates MCP through the mcporter bridge, maintaining decoupling from core stability. A critical failure mode merits explicit attention: when an MCP server fails to start, the agent responds using training knowledge without signaling tool unavailability to the user. The gateway log is the sole diagnostic source—operators without active log monitoring can run with degraded tool access indefinitely without awareness.

**Tier 3 — Plugins (capability layer).** Plugins extend gateway behavior in two formats. Native plugins (TypeScript npm packages) execute in-process with the gateway, providing channel integrations, model provider connections, and voice capabilities. Bundle plugins (.claude-plugin/ directories) are code-free extensions containing Markdown skills, JSON commands, and MCP connectors—no TypeScript required. Plugin installation triggers a built-in dangerous-code scan in partnership with VirusTotal before execution, blocking `critical` findings by default. The `--dangerously-force-unsafe-install` flag provides an escape hatch for false positives but does not bypass plugin hook policy enforcement. This supply chain security mechanism has no direct analog in classical OS device drivers; it is a novel contribution of the agentic context, where plugins arrive from untrusted third-party marketplace sources.

**Self-extension.** OpenClaw agents can autonomously author and install new SKILL.md files through conversation: the agent writes a new skill file to the workspace's skills directory in response to operator instruction, then installs it via ClawHub-compatible commands. This self-extension capability—an agent teaching itself new behavioral patterns—has no equivalent in classical OS device management and no counterpart in any compared system.

### D. Pillar 4: Scheduling and Orchestration

OpenClaw's scheduling subsystem provides both event-driven and time-triggered agent invocation through three complementary mechanisms.

**Heartbeat (periodic batch scheduler).** The heartbeat triggers agent execution at configurable intervals (default: 30 minutes) against a HEARTBEAT.md checklist. When no checklist items require action, the agent replies with `HEARTBEAT_OK`, which the gateway intercepts and suppresses without forwarding to the operator. This suppression mechanism is the key cost-control feature.

Consider N monitoring tasks each requiring periodic checks at interval T. Implementing each as a separate cron job produces N × (24h/T) agent invocations per day. Implementing all N tasks as a single heartbeat checklist produces exactly (24h/T) invocations per day. The cost ratio is N:1.

Formally, let I(T) = ⌊24h/T⌋ denote the daily invocation count for period T. For a cron-based system with N tasks: C_cron = N × I(T). For a heartbeat system batching all N tasks: C_heartbeat = I(T). The scheduling cost bound is:

> **C_cron / C_heartbeat = N**

For the default T = 30 minutes, I(T) = 48. At N = 5 concurrent monitoring tasks, heartbeat scheduling reduces daily inference turns from 240 to 48—a 5× reduction. This bound is O(N) improvement, confirmed at N=5 in the documented default configuration [1]. Figure 5 plots this cost ratio across N=1 to N=5.

> **Fig. 5** — Heartbeat cost comparison: grouped bar chart showing daily inference turns for N=1..5 tasks under cron scheduling (240, 192, 144, 96, 48 turns reversed) versus heartbeat batching (constant 48 turns). Cost ratio line (right axis) rises linearly from 1× to 5× as N increases. Source: `figures/fig5_heartbeat_cost.pdf`

**Cron jobs (exact-time scheduler).** Cron executes agent sessions at precise times using standard cron syntax, with a configurable `maxConcurrentRuns` limit. Cron is appropriate for time-sensitive deliverables where exact execution timing matters and HEARTBEAT_OK suppression would incorrectly mask a genuine scheduled result. Completed cron session transcripts are retained for 24 hours by default before pruning.

**Multi-agent orchestration.** The `sessions_spawn` primitive creates background subagent sessions that execute independently without blocking the orchestrating agent. Spawned agents send results as channel announcements upon completion. The maximum spawn depth is configurable via `agents.defaults.subagents.maxSpawnDepth`, defaulting to support three-tier hierarchies: orchestrator → worker → specialist. The Agent Client Protocol (ACP) extends orchestration to external agents—a command such as `openclaw config set agents.defaults.acp.permissionMode approve-reads` enables an OpenClaw agent to spawn and steer a Claude Code session over ACP, treating the coding environment as a specialized subagent.

**Lobster pipelines.** The Lobster workflow engine provides declarative multi-step automation pipelines, specifying sequences of agent invocations, tool calls, and conditional branches as workflow definitions rather than imperative code.

### E. Pillar 5: Security and Governance

OpenClaw's security architecture is organized as three tiers of increasing strength, each addressing a distinct threat model. The threat taxonomy follows MITRE ATLAS [17], the adversarial ML knowledge base documenting tactics and techniques targeting AI system deployments.

**Tier 1 — Tool Profiles (capability gating).** Tool profiles provide binary access control at the agent level. Four presets exist: `deny` (all tools blocked), `messaging` (communication tools only, no file or execution access), `coding` (file I/O, runtime execution, session management), and `full` (unrestricted). Profiles switch instantly without gateway restart. This is the software-layer boundary—it controls what the agent is permitted to attempt, independent of what it knows. Tool profiles alone do not prevent prompt injection attacks [15]: a compromised agent operating under the `full` profile retains full tool access regardless of how it was compromised.

**Tier 2 — Plugin Hooks (approval workflows).** The `before_tool_call` hook intercepts specific tool invocations before execution and routes an approval request to the operator via WhatsApp or Slack. Each request specifies operation title, description, severity level (info/warning/critical), and a 120-second response window. The hook is fail-closed: timeouts deny the operation, preventing indefinitely-pending approvals from creating execution gaps. Operators choose `allow-once`, `allow-always`, or `deny`. The `allow-always` path adds the operation to a persistent allowlist for future bypass. One critical constraint: MCP tools bypass `before_tool_call` hooks entirely [2]. Operators using MCP servers for sensitive tool access must implement approval at the MCP server level independently.

**Tier 3 — NemoClaw (kernel-level isolation).** NemoClaw combines OpenClaw with NVIDIA's containerized sandbox framework [2], deploying as a four-pod K3s cluster inside a single Docker container.

**Table II: NemoClaw Pod Architecture**

| Pod | Role | Has API Keys | Runs Agent |
|---|---|---|---|
| Gateway | Routing, auth, Control UI | No | No |
| Sandbox | Agent runtime, tools, skills | No | Yes |
| Privacy Router | Credential vault, rate limiting | Yes | No |
| Policy Engine | Kernel-level enforcement | No | No |

Figure 3 shows the four-pod cluster topology and the inference request flow through the Privacy Router.

> **Fig. 3** — NemoClaw four-pod K3s cluster: Gateway (top-left) → Sandbox (top-right) → Privacy Router (bottom-right, key icon) → Policy Engine (bottom-left). Arrows show inference request flow: Sandbox issues to `inference.local`, Privacy Router appends key, forwards to external API, strips auth headers on return. Source: `figures/fig3_nemoclaw.pdf`

The Privacy Router is NemoClaw's core security contribution. The agent issues inference requests to the internal hostname `inference.local`. The Privacy Router intercepts these requests, appends the provider API key, forwards to the external LLM API, receives the response, strips authentication headers, and returns the response to the sandbox. The API key never exists in the sandbox's memory space, environment variables, or network-observable traffic. Complete sandbox compromise through prompt injection cannot exfiltrate credentials because they do not exist in the compromised address space.

Kernel enforcement operates through three Linux security primitives. **Landlock** restricts sandbox filesystem access to permitted paths, blocking reads from `/etc`, `/var/run`, and credential directories through filesystem-level restriction independent of application code. **Seccomp** filters dangerous system calls including `ptrace` and `mount`, preventing sandbox processes from acquiring elevated privileges through kernel interface abuse. **Network namespaces** remove routes to external LLM providers from the sandbox's routing table—the sandbox can reach `inference.local` but routing entries for `api.anthropic.com` or `api.openai.com` do not exist in the sandbox network stack.

The `openclaw security audit` CLI assesses runtime security posture across eight dimensions: inbound access policies (DM/group policy coverage), tool blast radius (elevated tools with open channels), exec approval drift (security posture, interpreter allowlists), network exposure (bind mode and auth configuration), browser control exposure (remote node and CDP endpoint coverage), disk hygiene (permission modes, symlink chains, cloud-synced credential directories), plugin and extension allowlists, and policy misconfigurations. The `--fix` flag auto-remediates narrow findings; `--deep` runs live gateway probes against the running instance.

**Incident response workflow.** A documented three-phase response process covers security incidents: (1) Containment—stop the gateway, set bind mode to loopback, disable risky channel DM policies; (2) Rotation—rotate gateway auth token, update remote client secrets, rotate channel and provider credentials in `auth-profiles.json`; (3) Audit—review gateway logs and session transcripts, inspect recent configuration changes that expanded access, re-run `openclaw security audit --deep`.

---

## V. Installation Manual

This section provides a complete, tested installation guide for OpenClaw across all supported platforms. All commands are current as of OpenClaw with Node.js 24.

### A. Prerequisites

Required across all platforms:

- Node.js 24 (recommended) or Node.js 22.14+ minimum
- An API key from a supported model provider. Several providers offer free tiers suitable for low-volume personal deployments; verify current limits at the provider's API documentation.
- A messaging account on at least one supported channel
- Administrative access for daemon installation

### B. macOS Installation

macOS is the primary supported platform with the full feature set including Voice Wake, Talk Mode overlay, and the native menu bar companion app.

```bash
# Install OpenClaw globally
curl -fsSL https://openclaw.ai/install.sh | bash

# Run the onboarding wizard with daemon setup
openclaw onboard --install-daemon

# Verify installation
openclaw status
openclaw doctor

# Access the Control UI
open http://127.0.0.1:18789
```

The onboarding wizard installs a LaunchAgent at `~/Library/LaunchAgents/ai.openclaw.gateway.plist` that starts the gateway on login and restarts it on crash. All configuration is stored at `~/.openclaw/openclaw.json`.

Connect WhatsApp by running `openclaw channels connect whatsapp`, scanning the QR code in the terminal, and approving the pairing request from the mobile device. QR code pairing uses the Baileys library (WhatsApp Web protocol) and may require re-pairing if the WhatsApp session expires.

The macOS companion app (macOS 15+ Universal Binary) provides a menu bar icon, Voice Wake activation, Talk Mode overlay, and seamless remote gateway switching.

### C. Linux Installation

Linux differs from macOS in one operationally significant way: daemon lifetime. The macOS LaunchAgent runs for the user's login session automatically. The Linux systemd user service also starts on login, but stops when the user logs out — unless linger is enabled. For server deployments where the agent must survive SSH disconnection, run `loginctl enable-linger $USER` immediately after onboarding. Skipping this step is the most common Linux setup error. Tested distributions: Ubuntu 22.04+, Debian 12+, Fedora 38+, Arch Linux.

```bash
# Install Node.js 24 via nvm (recommended approach)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24 && nvm use 24 && nvm alias default 24

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# Run onboarding
openclaw onboard --install-daemon

# Enable linger so the gateway survives SSH disconnection (server deployments)
loginctl enable-linger $USER

# Verify systemd service status
systemctl --user status openclaw-gateway
```

The service file installs at `~/.config/systemd/user/openclaw-gateway.service`. Headless servers cannot run QR-based channel pairing through a graphical browser; use the TUI (`openclaw`) over SSH for initial channel setup. Once pairing completes, close the tunnel — the daemon continues running independently.

Known Linux-specific limitation: Telegram is blocked in some regions. Use a Telegram-compatible proxy or configure an alternative channel such as Discord or WhatsApp.

### D. Windows Installation

Two installation paths are available for Windows deployments.

**Native Windows (PowerShell, run as Administrator):**

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
openclaw onboard --install-daemon
```

**WSL2 + Ubuntu (recommended for full compatibility):**

```bash
# Inside Ubuntu WSL2 terminal
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
```

WSL2 is preferred because several native plugins require POSIX system calls unavailable on Windows. Browser automation and certain MCP server configurations function reliably only under WSL2. The gateway binds to the WSL2 loopback interface; access the Control UI from the Windows host browser using the WSL2 IP address (typically 172.x.x.x:18789).

### E. Raspberry Pi and ARM Hardware

Raspberry Pi deployment provides persistent, low-power OpenClaw operation.

```bash
# Install Node.js 24 ARM64 via NodeSource
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify ARM64 build
node -e "console.log(process.arch)"  # Expected: arm64

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon

# For headless access from another machine, set up SSH tunnel
# On your laptop: ssh -N -L 18789:127.0.0.1:18789 pi@raspberrypi.local
# Then open: http://127.0.0.1:18789
```

**Minimum hardware:** Raspberry Pi 4 with 4 GB RAM. Pi 3 and earlier are insufficient for reliable LLM tool-call processing. Use a Class 10 or UHS-I SD card. Enable swap to handle memory pressure during context-heavy sessions:

```bash
sudo dphys-swapfile swapoff
sudo sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=2048/' /etc/dphys-swapfile
sudo dphys-swapfile setup && sudo dphys-swapfile swapon
```

### F. Cloud VPS Deployment

VPS deployment converts OpenClaw from a local personal tool into a 24/7 AI employee accessible from any device. Three deployment paths accommodate different operational skill levels.

**Path 1 — Managed (no SSH required):**
Alibaba Cloud Simple Application Server provides a preconfigured OpenClaw image starting at $0.99 USD/month [2]. Configuration proceeds through a web console; no terminal access is required. Suitable for operators who need persistent availability without infrastructure management.

**Path 2 — VPS Native (recommended for most deployments):**

```bash
# On a fresh Ubuntu 22.04 VPS (Hetzner CX11 or equivalent budget provider)

# Create a non-root user
adduser openclaw
usermod -aG sudo openclaw
su - openclaw

# Install Node.js 24
curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon

# Harden gateway to loopback-only
openclaw config set gateway.bind loopback
openclaw config set channels.whatsapp.dmPolicy pairing
openclaw gateway restart

# On your local machine — set up SSH tunnel for dashboard access
# Add to ~/.ssh/config:
# Host my-openclaw
#   HostName <vps-ip>
#   User openclaw
#   LocalForward 18789 127.0.0.1:18789
```

Monthly cost breakdown: VPS infrastructure $5–8, model provider $50–100 at moderate volume (or $0 with Gemini free tier) [2]. Total: $5–108/month depending on volume.

**Path 3 — VPS Docker (for existing Docker environments):**

```bash
docker compose exec openclaw-gateway openclaw onboard
# All subsequent commands prefix with:
docker compose exec openclaw-gateway openclaw <command>
```

### G. Remote Access Configuration

The gateway binds to loopback by default. Choose a remote access pattern based on usage frequency: SSH tunneling is right for occasional access from one trusted machine with no additional software installation; Tailscale is the correct choice when multiple devices need persistent access and per-session tunnel management becomes friction. Both patterns are safe. Direct `0.0.0.0` binding without authentication is not.

**SSH tunnel (occasional access, no additional software):**

```bash
# Persistent tunnel via SSH config
# ~/.ssh/config entry:
Host openclaw-remote
  HostName <server-ip>
  User openclaw
  LocalForward 18789 127.0.0.1:18789
  ServerAliveInterval 60
  ServerAliveCountMax 3

# Connect and keep tunnel alive:
ssh -N openclaw-remote &
# Then access http://127.0.0.1:18789 locally
```

**Tailscale (permanent multi-device access via meshnet):**

```bash
# Install Tailscale on both server and client
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Configure OpenClaw to serve over tailnet
openclaw config set gateway.bind tailnet
openclaw config set gateway.auth.allowTailscale true
openclaw gateway restart
```

Never expose port 18789 on `0.0.0.0` without authentication. An unauthenticated public binding grants any reachable party full agent control — the gateway API has no rate limiting on unauthenticated connections, so exposure is not a theoretical risk.

### H. iOS and Android Node Pairing

Mobile nodes extend OpenClaw with device-native capabilities beyond what a server or desktop can provide.

**iOS node pairing:**

```bash
# Step 1: On the host machine
openclaw nodes pair --ios
# A pairing QR code appears in the terminal

# Step 2: On iPhone — open the OpenClaw iOS app
# Tap "Pair with Gateway" and scan the QR code

# Step 3: Verify
openclaw nodes list
# Expected: iOS node appears with CONNECTED status
```

iOS node capabilities: Canvas rendering with A2UI (agent-driven interface), Voice Wake activation, Talk Mode overlay, camera capture, screen recording, and location access.

**Android node pairing:**

```bash
# Step 1: On the host machine
openclaw nodes pair --android
# A pairing code appears in the terminal

# Step 2: On Android — open the OpenClaw Android app
# Enter the pairing code when prompted

# Step 3: Verify
openclaw nodes list
```

Android node capabilities: full chat session interface, voice interaction, Canvas, camera capture, and device command access (SMS send, contacts read, calendar access, notifications, location).

### I. NemoClaw Advanced Isolation Deployment

NemoClaw is appropriate for customer-facing deployments and compliance-audited environments. The monthly cost premium over standard Docker Compose is approximately $10 ($76 vs. $66/month at typical volume) [1].

**Prerequisites:** Docker 24+, at minimum 4 GB RAM, 20 GB free disk space.

```bash
# Install NemoClaw
curl -fsSL https://openclaw.ai/nemoclaw-install.sh | bash
openclaw-nemo onboard

# Verify four-pod cluster health
openclaw-nemo status pods
# Expected output:
# gateway        RUNNING
# sandbox        RUNNING
# privacy-router RUNNING
# policy-engine  RUNNING

# Run full security audit against NemoClaw deployment
openclaw security audit --deep
```

**Known NemoClaw v0.1.0 limitations:** Crashed sandbox pods require manual recovery (no automatic restart policy is implemented in v0.1.0); first-run image caching takes approximately 5 minutes; log output is distributed across four pods and requires external aggregation (Loki, Datadog, or similar) for unified operational visibility.

### J. Post-Installation Security Baseline

Every installation must complete this security checklist before operational use.

```bash
# Apply hardened baseline
openclaw config set gateway.bind loopback
openclaw config set gateway.auth.token $(openssl rand -hex 32)
openclaw config set channels.whatsapp.dmPolicy pairing
openclaw config set tools.exec.security ask
openclaw gateway restart

# Run full security audit with auto-remediation
openclaw security audit --deep --fix

# Confirm zero CRITICAL findings before first use
```

The `openclaw security audit` command checks inbound access policies, tool blast radius, exec approval drift, network exposure, browser control exposure, disk hygiene, plugin allowlists, and policy misconfigurations. CRITICAL findings must be resolved before the system processes real operator data or communicates with external contacts.

---

## VI. Architecture Analysis

### A. Agent Lifecycle Walkthrough

A complete agent invocation traverses five stages, each governed by a distinct gateway subsystem.

**Stage 1 — Intake.** An inbound message arrives at the gateway through one of the channel integrations. The routing subsystem resolves the target agent using a deterministic seven-tier binding priority: (1) exact peer match, (2) parent peer inheritance for thread context, (3) Discord role-based routing, (4) guild or team identifier, (5) account-level default, (6) channel-wide fallback, (7) wildcard catch-all. When multiple bindings match at the same tier, the first binding in configuration order wins.

**Stage 2 — Context assembly.** The target agent's workspace loads. All five identity files (SOUL/IDENTITY/AGENTS/TOOLS/USER.md), the current MEMORY.md, and today's and yesterday's journal files are assembled into the system prompt. The skill library is snapshotted at this point—skills installed after session start are not available until the next session after a gateway restart.

**Stage 3 — Model inference.** The assembled context plus the inbound message is submitted to the configured LLM provider. The model produces a response that may include zero or more tool call requests alongside the reply text.

**Stage 4 — Tool execution.** Each requested tool call is evaluated against the active tool profile and any registered `before_tool_call` hooks. Denied calls return an error response to the model; approved calls execute and return results for incorporation into the next inference turn. MCP tool calls bypass the `before_tool_call` hook and execute directly if the MCP server is reachable—a gap requiring separate mitigation at the MCP server level for sensitive operations.

**Stage 5 — Reply and persist.** The final model response streams to the originating channel in chunks. The full turn is appended to the session transcript at `~/.openclaw/agents/<agentId>/sessions/*.jsonl`. If the model determines a fact warrants persistence, a `memory_write` tool call commits it to MEMORY.md or the daily journal file.

### B. Design Trade-offs

**Local-first vs. cloud scale.** The architecture optimizes for a single operator's digital life rather than multi-tenant scale. Horizontal scaling across multiple gateway instances is not natively supported; multi-user deployments require separate gateway instances per user trust boundary. This is a deliberate choice—WhatsApp's session protocol is stateful and ties to a single device connection, making horizontal scale non-trivial without protocol changes.

**Plugin-first lean core.** VISION.md sets an intentionally high bar for core additions—capabilities packageable as ClawHub skills should not enter the core distribution. This produces a lean, hackable core at the cost of requiring explicit plugin installation for non-baseline workflows. The TypeScript implementation trades performance (compared to Go or Rust) for the broad developer familiarity that enables community contributions.

**Cooperative scheduling.** Neither heartbeat nor cron provides preemption. A long inference turn holds its session slot until the LLM returns; there is no mechanism for the gateway to interrupt a running inference call and reallocate its concurrency slot. At the default Global Lane pool size of four concurrent sessions, one slow inference call increases latency for up to three other simultaneous users. This is acceptable for the intended personal assistant deployment model but becomes a bottleneck at high concurrency.

**MCP via bridge.** The mcporter bridge provides flexibility—any MCP server connects through configuration without modifying OpenClaw core—but introduces the silent failure mode described in Section IV-C. A future protocol-level `tool_unavailable` signal from MCP servers to the agent context would address this operational gap without requiring native MCP runtime integration.

### C. Comparison with Existing Systems

Table III compares OpenClaw against the most closely related agent runtime systems across seven dimensions.

**Table III: Agent Runtime System Comparison**

| Dimension | OpenClaw | AIOS [4] | MemGPT [5] | AutoGen [6] | LangChain [18] |
|---|---|---|---|---|---|
| Memory model | 3-tier (prompt / journal / QMD) | Context management kernel | 2-tier (context / external) | Per-agent state dict | Chain memory objects |
| Scheduling | Heartbeat + cron + spawn | LLM-aware scheduler | Interrupt-driven | Conversation turns | Sequential chain |
| Security tier | 3-tier (Profile/Hook/NemoClaw) | Access control module | Not specified | Not specified | Not specified |
| Multi-agent | sessions_spawn + ACP | Agent scheduler | Not primary focus | Core design | Agent executor |
| Tool protocol | MCP via mcporter + native plugins | Tool service layer | External tools via interrupt | Function calling | Tool wrappers |
| Self-extension | Agent writes own skills | No | No | No | No |
| Deployment | Local-first + VPS + K3s | Research prototype | Research prototype | Application library | Application library |

Two differentiators stand out. First, self-extension: OpenClaw agents can autonomously author and install new SKILL.md files, teaching themselves new behavioral patterns through conversation. No compared system provides this capability. Second, the three-tier security stack: AIOS specifies an access control module but neither MemGPT, AutoGen, nor LangChain define deployment-grade security architectures. NemoClaw's Privacy Router pattern—API credential isolation through network namespace separation—has no equivalent in any compared system.

### D. Theoretical Analysis

**Routing complexity.** The binding resolution algorithm evaluates a deterministic seven-tier priority hierarchy. For a configuration with B total bindings, worst-case routing requires O(B) comparisons per message. Typical deployments use fewer than 10 bindings, making routing O(1) in practice.

**Privacy Router non-interference.** Let S denote the sandbox address space and K the set of all API credential values. The Privacy Router enforces the invariant K ∩ S = ∅ through two mechanisms: (a) the sandbox's network namespace contains no route to external LLM providers, so S cannot reach K-holding endpoints directly; (b) the Privacy Router strips authentication headers from responses before forwarding to the sandbox, so K values never appear in network-observable data within S. This property holds under complete sandbox compromise because the restriction is architectural—missing routing table entries and stripped headers—rather than policy-based logic that compromised software could override. For any adversary A with complete control of S: Pr[A recovers k ∈ K] = 0 under the standard network isolation assumption, since no code path from S to any K-containing storage exists.

**Heartbeat cost bound.** For N monitoring tasks at check interval T, the heartbeat model achieves C_cron / C_heartbeat = N as derived in Section IV-D. The bound is tight: each task that would generate I(T) daily cron invocations instead contributes zero marginal invocations to the heartbeat count. At the documented default of N=5 tasks and T=30 minutes, daily inference turns decrease from 240 to 48—a 5× reduction. The crossover point where dedicated cron scheduling is preferred over heartbeat batching is when task execution timing requires exact-minute precision, since the heartbeat executes at a fixed interval and cannot guarantee sub-interval delivery accuracy.

---

## VII. Limitations

Six specific limitations constrain OpenClaw's applicability for production enterprise deployments at scale.

**1. Personal-assistant trust model.** The security architecture assumes a single trusted operator boundary. OpenClaw's documentation states explicitly that it is "not a hostile multi-tenant security boundary for multiple adversarial users sharing one agent/gateway" [2]. Organizations requiring isolation between mutually untrusting users must deploy separate gateway instances per trust boundary—one per host or OS user. NemoClaw provides credential isolation within a single operator's deployment but does not address inter-user authorization. This is an intentional scope constraint, not an implementation gap.

**2. Cooperative-only scheduling.** Neither heartbeat nor cron jobs are preemptible. A long inference turn blocks its session slot until the LLM returns; there is no interrupt mechanism to reallocate the slot to a higher-priority task. At the default pool size of four concurrent sessions, a single slow inference call delays three other concurrent users for the full inference duration. Classical OS preemptive scheduling has no equivalent in OpenClaw's current design. An interrupt signal analogous to POSIX SIGINT that terminates a running inference turn and frees its slot would address this limitation without requiring architectural changes to the concurrency model.

**3. Prompt-space memory constraints.** MEMORY.md occupies the LLM's context window rather than a separate address space. As MEMORY.md grows, it consumes tokens that would otherwise be available for tool outputs and conversation history. The QMD vector store offloads historical retrieval to cold storage but does not reduce the hot-tier memory footprint. This is qualitatively different from OS RAM, which is bounded by physical hardware capacity but is not shared with the instruction execution pipeline. The compaction mechanism mitigates overflow but does not eliminate the fundamental constraint.

**4. Model-capability dependency.** Orchestration reliability depends on the LLM's willingness to invoke delegation tools. Free-tier models exhibit a documented failure mode: they generate plausible-sounding refusals ("permission denied," "tool limitations") rather than invoking `sessions_spawn` [1]. This is worse than silently ignoring the tool—the agent appears to have attempted delegation when it has not, misleading the operator into believing orchestration succeeded. Reliable multi-agent coordination requires commercial models at Claude Sonnet or GPT-4 class [13], adding $50–100/month to operating costs [1]. The scheduler relies on model judgment rather than a deterministic dispatch mechanism.

**5. MCP silent failure.** MCP server startup failures produce no agent-visible error and no user-visible notification. The agent continues responding with training knowledge, and the operator has no indication that tool access is unavailable unless actively monitoring the gateway log. An extended operational period with silently degraded MCP access is possible without detection. This gap would be resolved by a protocol-level `tool_unavailable` signal that MCP servers could emit on startup failure, placing the unavailability notice in the agent's context rather than only in the gateway log.

**6. NemoClaw alpha stability.** NemoClaw v0.1.0 carries three specific operational limitations. Crashed sandbox pods require manual recovery because no automatic restart policy is implemented. First-run image caching takes approximately 5 minutes, creating a startup delay that is unacceptable for time-critical deployments. Log output is split across four pods, requiring external aggregation for unified operational visibility. Compliance-audited deployments using NemoClaw will require additional operational tooling—log aggregators, pod health monitors, and automatic restart supervisors—beyond the base NemoClaw installation.

---

## VIII. Conclusion

This paper presented the first formal academic analysis of OpenClaw as an AI Agentic Operating System. We mapped five classical OS primitives to their OpenClaw equivalents, specified the five-pillar architecture in formal terms, derived a scheduling cost bound showing heartbeat batching achieves N:1 improvement over equivalent cron scheduling, and demonstrated that NemoClaw's Privacy Router provides a formally verifiable credential isolation guarantee that application-layer tool profiles cannot match.

The comparison with AIOS [4], MemGPT [5], AutoGen [6], and LangChain [18] shows that OpenClaw occupies a structurally distinct position among agent runtime systems: it is the only deployed system providing production-grade three-tier security, a three-tier memory hierarchy with cross-agent QMD retrieval, and agent self-extension through autonomous skill authoring. These properties together constitute a more complete Agentic OS than any comparable system.

Scheduling is the most pressing gap. Head-of-line blocking at four concurrent sessions is not a design choice — it is a missing interrupt mechanism, and adding one does not require touching memory or security architecture.

The MEMORY.md constraint is a different category of problem: it is not a missing feature but an architectural boundary. QMD reduces retrieval load but does not shrink the hot-tier token footprint. The right solution is a fixed-size working memory abstraction that maintains a constant MEMORY.md budget and archives overflow to the vector store automatically — decoupling hot memory management from context window capacity, which is the correct separation of concerns.

NemoClaw v1.0 stability is a binary prerequisite for compliance deployments. Manual pod recovery, five-minute startup delays, and fragmented log output across four pods are not acceptable as permanent conditions. Automatic restart, sub-minute image caching, and unified log aggregation must reach production quality first — the security architecture is sound; it is the operational maturity that requires investment before regulated industries can adopt it without supplementary tooling.

OpenClaw's emergence demonstrates that the AI agent field is converging toward the same infrastructure abstractions that classical operating systems developed for hardware resource management. The five-pillar framework described in this paper—process management, memory management, tool management, scheduling, and security—likely generalizes beyond OpenClaw to any multi-agent personal assistant platform. Near-term, the scheduling gap and NemoClaw stability issues are tractable implementation problems the open-source community can address without architectural changes. The longer horizon is interoperability: future work should examine whether these primitives can be formalized into a vendor-neutral Agentic OS specification that multiple platforms could implement, enabling the cross-platform interoperability that POSIX provided for Unix-family operating systems four decades ago. That specification does not yet exist — writing it is the work.

---

## Acknowledgments

The author thanks the OpenClaw open-source community for building the platform this analysis is grounded in. No external funding was received for this work.

## References

[1] P. Steinberger, "OpenClaw," GitHub, [Online]. Available: https://github.com/openclaw/openclaw. [Accessed: Apr. 2026].

[2] P. Steinberger, "OpenClaw Documentation," [Online]. Available: https://docs.openclaw.ai. [Accessed: Apr. 2026].

[3] Anthropic, "Model Context Protocol," Nov. 2024. [Online]. Available: https://modelcontextprotocol.io. [Accessed: Apr. 2026].

[4] K. Mei, X. Zhu, W. Xu, W. Hua, M. Jin, Z. Li, S. Xu, R. Ye, Y. Ge, and Y. Zhang, "AIOS: LLM Agent Operating System," arXiv:2403.16971, 2024.

[5] C. Packer, S. Wooders, K. Lin, V. Fang, S. G. Patil, I. Stoica, and J. E. Gonzalez, "MemGPT: Towards LLMs as Operating Systems," arXiv:2310.08560, 2023.

[6] Q. Wu, G. Bansal, J. Zhang, et al., "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation," arXiv:2308.08155, 2023.

[7] S. Hong, M. Zhuge, J. Chen, et al., "MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework," arXiv:2308.00352, 2023.

[8] L. Wang, C. Ma, X. Feng, et al., "A Survey on Large Language Model based Autonomous Agents," arXiv:2308.11432, 2023.

[9] X. Liu, H. Yu, H. Zhang, et al., "AgentBench: Evaluating LLMs as Agents," arXiv:2308.03688, 2023.

[10] T. Schick, J. Dwivedi-Yu, R. Dessì, et al., "Toolformer: Language Models Can Teach Themselves to Use Tools," in Proc. NeurIPS, 2023.

[11] S. Yao, J. Zhao, D. Yu, et al., "ReAct: Synergizing Reasoning and Acting in Language Models," in Proc. ICLR, 2023.

[12] J. Wei, X. Wang, D. Schuurmans, et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models," in Proc. NeurIPS, 2022.

[13] OpenAI, "GPT-4 Technical Report," arXiv:2303.08774, 2023.

[14] W. Kwon, Z. Li, S. Zhuang, et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention," in Proc. ACM SIGOPS SOSP, 2023.

[15] Y. Liu, G. Deng, Z. Xu, et al., "Prompt Injection Attack against LLM-Integrated Applications," arXiv:2306.05499, 2023.

[16] P. Lewis, E. Perez, A. Piktus, et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," in Proc. NeurIPS, 2020.

[17] MITRE Corporation, "MITRE ATLAS: Adversarial Threat Landscape for Artificial-Intelligence Systems," [Online]. Available: https://atlas.mitre.org. [Accessed: Apr. 2026].

[18] H. Chase, "LangChain," GitHub, 2022. [Online]. Available: https://github.com/langchain-ai/langchain. [Accessed: Apr. 2026].
