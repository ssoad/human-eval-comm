# HumanEvalComm V3: Roadmap to Robustness & Innovation

This document outlines the strategic roadmap for upgrading the **HumanEvalComm V2** framework into a robust, industry-defining benchmark for agentic communication (V3). This roadmap is structured to easily translate into the methodology and future work sections of the main research paper.

---

## Phase 1: Robustness Upgrades
*Focus: Validating the evaluation pipeline and scaling to realistic environments.*

### 1.1 Repo-Level Task Integration (SWE-bench Wrapper)
**Motivation**: Real-world software engineering is rarely limited to single-file Python functions (as in HumanEval). Developers must navigate multi-file codebases, understand inter-dependencies, and resolve GitHub issues.
**Action Items**:
- [ ] Create a `src/datasets/swe_bench_comm.py` wrapper to load SWE-bench-lite issues.
- [ ] Inject artificial ambiguity into GitHub issue descriptions (e.g., removing the file path of the bug or making the requested feature vague).
- [ ] Update `v2_benchmark.py` to allow the SandboxRunner to provide agents with bash/filesystem access.
**Paper Contribution**: Proves the communication framework scales to real-world, repository-level complexity.

### 1.2 Multi-Turn Communication Loop
**Motivation**: The current V2 framework evaluates communication in a single turn (Agent asks $\rightarrow$ Evaluator answers). Real-world requirement gathering is a messy, multi-turn dialogue.
**Action Items**:
- [x] Refactor the 3-round structure in `v2_benchmark.py` into a dynamic `while` loop (capped at `MAX_TURNS`).
- [x] Prompt the LLM-as-a-judge to occasionally provide partial, vague, or incomplete answers.
- [x] Evaluate if the agent persists and asks follow-up questions until the ambiguity is fully resolved.
**Paper Contribution**: Evaluates conversational persistence and the ability of an LLM to navigate layered ambiguity.

### 1.3 Human-in-the-Loop Validation UI
**Motivation**: "LLM-as-a-judge" is standard but prone to bias. To make the benchmark scientifically rigorous, the automated grading of "Good Question Rate" must be validated against human baselines.
**Action Items**:
- [x] Add an `/annotate` route to `flask_leaderboard/app.py`.
- [x] Create an intuitive annotation web interface (`annotate.html`) for human reviewers.
- [x] Develop `compute_human_correlation.py` to calculate Pearson Correlation and Cohen's Kappa between human and LLM grades.
**Paper Contribution**: Provides empirical evidence (high correlation scores) that the V2/V3 automated evaluation metrics are trustworthy and aligned with human judgment.

---

## Phase 2: Innovation & Advanced Capabilities
*Focus: Pushing the boundaries of what "communication" means for AI agents.*

### 2.1 "Negotiation & Pushback" (Unfeasible Requirements)
**Motivation**: The best developers do not blindly write code for bad requirements; they push back. If asked to "sort a 10TB array in memory," an agent should flag the architectural flaw rather than attempting to code it.
**Action Items**:
- [ ] Curate a new dataset: `Benchmark/HumanEvalComm_Unfeasible.jsonl` containing mathematically impossible, highly inefficient, or anti-pattern constraints.
- [ ] Introduce a new metric: **Pushback Rate** (Does the model reject the prompt and explain why?).
**Paper Contribution**: Shifts the paradigm from "Clarification" to "Negotiation," demonstrating advanced reasoning and architectural awareness.

### 2.2 Heterogeneous Agent Collaboration (The "Dev Team")
**Motivation**: Future software development will involve swarms of specialized agents. A Code LLM must know *who* to communicate with.
**Action Items**:
- [ ] Create distinct agent personas: `ProductManager` (handles business logic) and `SeniorReviewer` (handles technical architecture).
- [ ] Implement a routing mechanism in `v2_benchmark.py` where the primary agent must decide which persona to query based on the ambiguity.
**Paper Contribution**: Introduces multi-agent collaboration metrics, evaluating an LLM's ability to navigate organizational roles to gather requirements.

### 2.3 Proactive "Fail-Fast" Metrics
**Motivation**: LLMs waste significant compute generating long blocks of hallucinated code for broken prompts before realizing they should have asked a question. 
**Action Items**:
- [ ] Integrate token and time tracking into the generation phase.
- [ ] Introduce a **Compute-to-Question** metric (or Time-to-Question).
- [ ] Update the `V2Score` to penalize models that waste massive amounts of tokens before initiating communication.
**Paper Contribution**: Introduces efficiency into communication evaluation, rewarding models that recognize flawed requirements early ("failing fast").

---

## How to Use This Roadmap for the Main Paper
- **Introduction / Gap Analysis**: Use Phase 1 to justify moving beyond HumanEval. Use Phase 2 to justify moving beyond simple clarification to negotiation.
- **Methodology**: Detail the SWE-bench wrapper (1.1), the multi-turn loop (1.2), and the Dev Team routing (2.2).
- **Evaluation / Results**: Present the correlation graphs from the Human-in-the-Loop validation (1.3), the Pushback Rates (2.1), and the Compute-to-Question efficiency comparisons (2.3).
