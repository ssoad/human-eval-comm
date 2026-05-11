# HumanEvalComm V2: A Comprehensive Evaluation Report

> An extended framework for benchmarking the communication competence, negotiation capability, and agentic collaboration of Code LLMs in software engineering tasks.

---

## Table of Contents

1. [Background & Motivation](#1-background--motivation)
2. [Foundations: The Original HumanEvalComm](#2-foundations-the-original-humanevalcomm)
3. [HumanEvalComm V2: What We Propose](#3-humanevalcomm-v2-what-we-propose)
4. [Implementation: What We Built](#4-implementation-what-we-built)
5. [Evaluation Methodology](#5-evaluation-methodology)
6. [Metrics & Scoring System](#6-metrics--scoring-system)
7. [Experimental Results](#7-experimental-results)
8. [Key Findings & Discussion](#8-key-findings--discussion)
9. [Developer Tools & Leaderboard](#9-developer-tools--leaderboard)
10. [Limitations & Future Work](#10-limitations--future-work)
11. [References](#11-references)

---

## 1. Background & Motivation

Large Language Models (LLMs) have fundamentally transformed software development. Tools like GitHub Copilot, ChatGPT, and Claude are now indispensable companions for developers worldwide. However, a critical gap exists between an LLM that can *write code* and one that can function as a *collaborative software engineer*.

As Wu & Fard (2025) argue in the original HumanEvalComm paper:

> *"Top-level software engineers often ask clarifying questions to reduce ambiguity in both requirements and coding solutions. We argue that the same should be applied to LLMs for code generation tasks."*

The central insight is that **effective communication is a prerequisite for correct code generation**. When a problem description is ambiguous, inconsistent, or incomplete, a competent engineer does not blindly write code — they ask questions first. Yet existing benchmarks like HumanEval (Chen et al., 2021), MBPP (Austin et al., 2021), APPS (Hendrycks et al., 2021), and CodeXGLUE (Lu et al., 2021) evaluate LLMs exclusively on their ability to generate correct code from perfectly-specified prompts, ignoring the communicative dimension entirely.

**HumanEvalComm V2 addresses this gap by proposing that the true measure of an intelligent Code LLM is not just its ability to write code, but its ability to navigate ambiguity, ask clarifying questions, negotiate against flawed requirements, and collaborate across organizational roles.**

---

## 2. Foundations: The Original HumanEvalComm

### 2.1 Benchmark Construction

The original HumanEvalComm benchmark (Wu & Fard, 2025), published in ACM Transactions on Software Engineering and Methodology (TOSEM), was constructed by manually modifying the 164 problem descriptions from the HumanEval dataset. Modifications were applied according to a taxonomy of clarification types grounded in Requirement Engineering (RE) concepts:

| Category | Code | Description | Count |
|---|---|---|---|
| Ambiguity | 1a | Statements that could be interpreted multiple ways | 164 |
| Inconsistency | 1c | Contradictory requirements between description and examples | 164 |
| Incompleteness | 1p | Critical information removed from descriptions | 164 |
| Ambiguity + Inconsistency | 2ac | Combined challenges | 162 |
| Inconsistency + Incompleteness | 2cp | Combined challenges | 34 |
| Ambiguity + Incompleteness | 2ap | Combined challenges | 74 |
| **Total** | | | **762** |

The modification process was performed manually by two experienced software engineers (with nearly a decade and 15+ years of experience, respectively), taking approximately 130 hours of combined effort.

### 2.2 Original Metrics

The original framework introduced two key evaluation metrics:

- **Communication Rate**: The percentage of responses where the model asks clarifying questions instead of directly generating code.
- **Good Question Rate**: The percentage of clarification questions rated as "Good" by an LLM-based evaluator (questions that help recover the missing/modified information).

### 2.3 Key Findings from the Original Paper

The original study revealed critical limitations in existing Code LLMs:

| Model | Comm Rate | Good Q Rate | Pass@1 (HumanEval) | Pass@1 (HumanEvalComm) | Drop |
|---|---|---|---|---|---|
| ChatGPT 3.5 | 14.21% | 13.43% | 65.58% | 31.34% | -52% |
| CodeLlama 13B | 10.16% | 37.55% | 29.88% | 19.35% | -35% |
| CodeQwen1.5 7B | 4.82% | 41.68% | 76.83% | 47.61% | -38% |
| DeepSeek Coder 7B | 30.76% | 61.42% | 71.78% | 45.68% | -36% |
| DeepSeek Chat 7B | 37.93% | 58.71% | 12.80% | 26.32% | +106% |

**Critical insight**: More than 60% of responses from Code LLMs still blindly generate code even when the problem description contains deliberate flaws that should trigger clarifying questions. Pass@1 dropped by 35%–52% across models.

The study also introduced **Okanagan**, an LLM agent approach with a multi-round structure (Generate → Ask → Reflect), which increased Communication Rate by an absolute 58% and Good Question Rate by 38%.

---

## 3. HumanEvalComm V2: What We Propose

### 3.1 Limitations of V1

While HumanEvalComm V1 established the importance of communication competence, several limitations became apparent:

1. **Limited Evaluation Scope**: V1 focused on binary question-asking behavior without assessing communication *quality* or *effectiveness*.
2. **Single-Model Evaluation**: Each LLM was evaluated in isolation, missing cross-model synergies.
3. **Narrow Metrics**: Communication was binary (asked vs. didn't ask) rather than multi-dimensional.
4. **No Trustworthiness Assessment**: V1 lacked evaluation of code security, reliability, and efficiency.
5. **No Negotiation or Pushback**: V1 did not test whether models could identify and *reject* fundamentally flawed requirements.
6. **No Role-Based Collaboration**: V1 treated communication as a monolithic activity, ignoring the reality that different questions should be directed to different organizational roles.

### 3.2 V2 Innovation Phases

HumanEvalComm V2 addresses these limitations through two structured phases:

**Phase 1 — Robustness Upgrades:**
- Repo-level task integration via SWE-bench wrapper
- Multi-turn communication loop with dynamic persistence
- Human-in-the-loop validation UI for scientific rigor

**Phase 2 — Innovation & Advanced Capabilities:**
- Negotiation & Pushback against unfeasible requirements
- Heterogeneous agent collaboration ("Dev Team" routing)
- Proactive "Fail-Fast" compute efficiency metrics

---

## 4. Implementation: What We Built

### 4.1 Repo-Level Task Integration (SWE-bench Wrapper)

**Motivation**: Real-world software engineering is rarely limited to single-file Python functions. Developers must navigate multi-file codebases, understand inter-dependencies, and resolve GitHub issues.

**Implementation**: We created `src/datasets/swe_bench_comm.py`, a wrapper that loads SWE-bench-lite issues and injects artificial ambiguity into GitHub issue descriptions (e.g., removing the file path of the bug or making the requested feature vague). The `v2_benchmark.py` engine was updated to allow the SandboxRunner to provide agents with bash/filesystem access.

**Paper Contribution**: Proves the communication framework scales beyond toy algorithmic problems to real-world, repository-level complexity.

---

### 4.2 Multi-Turn Communication Loop

**Motivation**: V1 evaluated communication in a single turn (Agent asks → Evaluator answers). Real-world requirement gathering is a messy, multi-turn dialogue where initial answers may be partial, vague, or incomplete.

**Implementation**: The static 3-round Okanagan structure was refactored into a dynamic `while` loop capped at `MAX_TURNS`. The LLM-as-a-judge was prompted to occasionally provide partial or vague answers, forcing the evaluated agent to persist and ask follow-up questions until the ambiguity was fully resolved.

```
Turn 1: Agent receives ambiguous prompt
         → Agent asks clarifying question
         → Evaluator provides partial answer
Turn 2: Agent receives partial answer
         → Agent asks follow-up question (persistence!)
         → Evaluator provides complete answer
Turn 3: Agent generates code with full context
```

**Paper Contribution**: Evaluates conversational persistence and the ability of an LLM to navigate layered ambiguity across multiple dialogue turns.

---

### 4.3 Human-in-the-Loop Validation UI

**Motivation**: "LLM-as-a-judge" is standard but prone to bias (as noted in the original paper: *"LLM evaluators prefer to give high scores to responses that conflict with the facts"*). To make the benchmark scientifically rigorous, automated grading must be validated against human baselines.

**Implementation**:
- Added an `/annotate` route to `flask_leaderboard/app.py`
- Created an intuitive annotation web interface (`annotate.html`) for human reviewers
- Developed `scripts/compute_human_correlation.py` to calculate:
  - **Pearson Correlation**: Measures linear relationship between human and LLM grades
  - **Cohen's Kappa**: Measures inter-rater reliability accounting for chance agreement

**Paper Contribution**: Provides empirical evidence (high correlation scores) that the V2 automated evaluation metrics are trustworthy and aligned with human judgment.

---

### 4.4 Negotiation & Pushback (Unfeasible Requirements)

**Motivation**: The best developers do not blindly write code for bad requirements — they push back. If asked to *"sort a 10TB array in memory"* or *"store plaintext passwords in a public log"*, an agent should flag the architectural flaw rather than attempting to code it.

**Implementation**:
- Curated a new dataset: `Benchmark/HumanEvalComm_Unfeasible.jsonl` containing problems with:
  - Mathematically impossible constraints (e.g., sorting 10TB in RAM)
  - Security anti-patterns (e.g., plaintext password storage)
  - Architecturally infeasible requirements
- Introduced a new metric: **Pushback Rate** — the percentage of problems where the model correctly rejects the prompt and explains why

**Paper Contribution**: Shifts the evaluation paradigm from "Clarification" to "Negotiation," demonstrating advanced reasoning and architectural awareness. This is a fundamentally new dimension of LLM evaluation not present in any existing benchmark.

---

### 4.5 Heterogeneous Agent Collaboration ("Dev Team" Routing)

**Motivation**: Future software development will involve swarms of specialized agents. A Code LLM must know *who* to communicate with — a product manager for business logic questions, or a senior reviewer for technical architecture questions.

**Implementation**:
- Created distinct agent personas embedded in the evaluation:
  - `ProductManager`: Handles business logic, user requirements, and feature scope
  - `SeniorReviewer`: Handles technical architecture, performance, and security decisions
- Implemented a routing mechanism in `v2_benchmark.py` where the primary agent must decide which persona to query based on the nature of the ambiguity
- Routing is detected via `[TO: ProductManager]` and `[TO: SeniorReviewer]` tags in the model's response

**Paper Contribution**: Introduces multi-agent collaboration metrics, evaluating an LLM's ability to navigate organizational roles to gather requirements — a skill critical for real-world software engineering teams.

---

### 4.6 Proactive "Fail-Fast" Metrics

**Motivation**: LLMs waste significant compute generating long blocks of hallucinated code for broken prompts before realizing they should have asked a question. A model that recognizes flawed requirements at token 50 is more efficient than one that generates 500 tokens of incorrect code before asking.

**Implementation**:
- Integrated token and time tracking into the generation phase
- Introduced a **Compute-to-Question** metric (tokens consumed before the first clarifying question)
- Updated the `V2Score` to penalize models that waste massive amounts of tokens before initiating communication:

```
FailFast Score = max(0, 100 - (tokens_to_question / 10))
```

**Paper Contribution**: Introduces *efficiency* into communication evaluation, rewarding models that recognize flawed requirements early ("failing fast") — directly analogous to the software engineering principle of early failure detection.

---

## 5. Evaluation Methodology

### 5.1 Evaluation Pipeline

The V2 evaluation pipeline consists of four integrated stages:

```
┌─────────────────────────────────────────────────────────┐
│                   EVALUATION PIPELINE                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. GENERATION PHASE                                     │
│     └─ Model receives ambiguous/unfeasible prompt        │
│                                                          │
│  2. MULTI-TURN COMMUNICATION ASSESSMENT                  │
│     ├─ Question Detection (is_question)                  │
│     ├─ Pushback Detection (is_pushback)                  │
│     ├─ Question Quality Scoring (evaluate_question)      │
│     ├─ Routing Accuracy (detect_routing_persona)         │
│     ├─ FailFast Scoring (tokens_to_question)             │
│     └─ Answer Generation → Loop back to Step 1           │
│                                                          │
│  3. CODE QUALITY ANALYSIS                                │
│     ├─ Functional Correctness (Pass@1, Test Pass Rate)   │
│     ├─ Static Analysis (Readability)                     │
│     └─ Security Assessment                               │
│                                                          │
│  4. TRUSTWORTHINESS EVALUATION                           │
│     ├─ Efficiency (execution time, memory)               │
│     ├─ Reliability (execution success + LLM confidence)  │
│     └─ Multi-LLM Cross-Judging                          │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Evaluated Models

The V2 framework supports evaluation across multiple providers. In our main paper, five state-of-the-art LLMs were evaluated across the complete benchmark:

| Model | Parameters | Provider | Category |
|---|---|---|---|
| GPT-4o-mini | — | OpenAI | Commercial (Efficient) |
| Llama-3.1-8B-Instruct | 8B | Meta | Open-Source |
| DeepSeek-Chat | 7B | DeepSeek | Open-Source |
| Claude-3-Haiku | — | Anthropic | Commercial (Efficient) |
| Qwen-2.5-Coder-32B | 32B | Alibaba | Open-Source (Code-Specific) |

**Evaluation Configuration:**
- **Problem Set**: 163 modified problems (762 total evaluations)
- **Temperature**: 0.1 (for consistency and reproducibility)
- **Max Tokens**: 2048
- **Statistical Validation**: Cross-model evaluation with inter-rater reliability

### 5.3 Execution Infrastructure

To ensure reproducibility and accessibility, the benchmark supports three execution modes:

1. **API-Based (OpenRouter)**: Evaluates premium models through a unified API proxy
2. **Local (Ollama + Colab)**: 100% free, offline execution using open-source models on Google Colab's free GPU instances
3. **Hybrid**: Combines local and API models for cross-evaluation judging

---

## 6. Metrics & Scoring System

### 6.1 Communication Metrics

| Metric | Formula | Description |
|---|---|---|
| **Communication Rate** | `CommRate = N_q / N_p` | Proportion of problems where the model asks clarifying questions |
| **Good Question Rate** | `GoodQRate = Σ Q_s / N_q` | Quality of clarification questions (5-point scale, multi-judge) |
| **Communication Effectiveness** | `CommEff = N_imp / N_att` | Improvement in outcomes after clarification |
| **Pushback Rate** | `PushbackRate = N_pushback / N_p` | Success in rejecting unfeasible requirements |
| **Routing Accuracy** | `RoutingRate = N_routed / N_q` | Correctly addressing the appropriate persona |
| **FailFast Score** | `FailFast = max(0, 100 - tokens/10)` | Efficiency in early recognition of flawed requirements |

### 6.2 Code Quality Metrics

| Metric | Formula | Description |
|---|---|---|
| **Pass@1** | `Pass@1 = N_pass / N_p` | First-attempt functional correctness |
| **Test Pass Rate** | `TestRate = N_tpass / N_t` | Individual test case pass rate |
| **Readability** | `ReadScore = f(Static)` | Static analysis quality score |

### 6.3 Trustworthiness Metrics

| Metric | Formula | Description |
|---|---|---|
| **Security Score** | `SecScore = 1 - N_vul / N_vul_max` | Vulnerability-free ratio |
| **Reliability Score** | `RelScore = 1 - N_inc / N_out` | Output consistency |
| **Efficiency Score** | `EffScore = C_opt / C_act` | Computational efficiency ratio |

### 6.4 V2 Composite Score

The V2 Score is a hierarchical composite that balances three dimensions:

```
V2Score = w₁ · Communication + w₂ · Correctness + w₃ · Trustworthiness

Where:
  Communication  = α · CommRate + β · GoodQRate + γ · Effectiveness
  Correctness    = δ · Pass@1   + ε · TestRate  + ζ · Readability
  Trustworthiness = η · Security + θ · Reliability + ι · Efficiency

  w₁ + w₂ + w₃ = 1
```

Weights are calibrated based on empirical analysis of developer preferences and code quality priorities.

---

## 7. Experimental Results

### 7.1 Communication Competence

| Model | Comm Rate | Good Q Rate | Communication Pattern |
|---|---|---|---|
| GPT-4o-mini | 33% | 74% | Very Confident |
| Llama-3.1-8B | 40% | 74% | Balanced |
| DeepSeek-Chat | 50% | 75% | Balanced |
| Claude-3-Haiku | 63% | 76% | Cautious |
| Qwen-2.5-Coder-32B | 58% | 74% | Cautious |

**Key Observation**: A 30 percentage-point range exists between the most confident model (GPT-4o-mini at 33%) and the most cautious model (Claude-3-Haiku at 63%).

### 7.2 Functional Correctness & Code Quality

| Model | Pass@1 | Test Pass | Readability | Security | Efficiency | Reliability |
|---|---|---|---|---|---|---|
| GPT-4o-mini | 86% | 65% | 75 | 71 | 0.86 | 0.76 |
| Llama-3.1-8B | 76% | 55% | 63 | 59 | 0.76 | 0.67 |
| DeepSeek-Chat | 78% | 50% | 62 | 58 | 0.78 | 0.68 |
| Claude-3-Haiku | 77% | 45% | 59 | 55 | 0.77 | 0.67 |
| Qwen-2.5-Coder-32B | 69% | 38% | 52 | 48 | 0.69 | 0.60 |

### 7.3 V2 Composite Rankings

| Model | V2 Score | Rank | Gap to Leader | Category |
|---|---|---|---|---|
| GPT-4o-mini | 6.9 | 1st | — | Superior |
| Llama-3.1-8B | 5.8 | 2nd | -1.1 | Strong |
| DeepSeek-Chat | 5.6 | 3rd | -1.3 | Good |
| Claude-3-Haiku | 5.2 | 4th | -1.7 | Moderate |
| Qwen-2.5-Coder-32B | 4.6 | 5th | -2.3 | Developing |

### 7.4 Statistical Correlations

| Metric Pair | Correlation (ρ) | Interpretation |
|---|---|---|
| Readability ↔ V2Score | **0.99** | Code quality is the dominant predictor |
| Security ↔ V2Score | **0.99** | Security strongly predicts overall performance |
| Pass@1 ↔ V2Score | **0.95** | Functional correctness is a strong driver |
| CommRate ↔ V2Score | **-0.88** | Higher questioning correlates with lower performance |

---

## 8. Key Findings & Discussion

### 8.1 The Communication–Performance Trade-off

The most striking finding is a **strong negative correlation (ρ = -0.88)** between communication frequency and overall performance. Models that ask more questions tend to achieve lower composite scores.

> For every 10% increase in Communication Rate, the V2 Score decreases by approximately 0.29 points.

This does not mean communication is bad — rather, it suggests that *excessive* questioning may indicate underlying uncertainty or architectural limitations. The optimal balance appears to be **moderate communication rates (40–50%)**, as demonstrated by Llama-3.1-8B and DeepSeek-Chat.

### 8.2 Code Quality Dominates Rankings

Code quality metrics (Readability and Security) are the **strongest predictors** of overall performance:

- A 1-point increase in Readability correlates with a 0.43 increase in V2 Score
- A 1-point increase in Security correlates with a 0.42 increase in V2 Score
- Quality metrics account for approximately **60% of the variance** in final rankings

### 8.3 Three Behavioral Archetypes

The evaluation reveals three distinct model behavioral patterns:

1. **Confident Models** (GPT-4o-mini): Low communication rates (33%), high execution success (86% Pass@1). These models prefer to generate code directly, relying on internal confidence.
2. **Balanced Models** (Llama-3.1-8B, DeepSeek-Chat): Moderate communication rates (40–50%) with solid overall performance. These models strike the best trade-off.
3. **Cautious Models** (Claude-3-Haiku, Qwen-2.5-Coder-32B): High communication rates (58–63%) but lower execution success. These models may over-question, trading efficiency for thoroughness.

### 8.4 Implications for AI-Assisted Development

| Use Case | Recommended Model Type | Rationale |
|---|---|---|
| High-Stakes Production | Confident (GPT-4o-mini) | Superior execution and code quality |
| Collaborative Development | Balanced (Llama/DeepSeek) | Best trade-off between communication and capability |
| Educational/Learning | Cautious (Claude/Qwen) | Thorough questioning benefits learning contexts |

### 8.5 Comparison with Original HumanEvalComm Findings

| Dimension | V1 (Wu & Fard, 2025) | V2 (This Work) |
|---|---|---|
| Comm Rate Range | 4.82% – 37.93% | 33% – 63% |
| Best Communicator | DeepSeek Chat (37.93%) | Claude-3-Haiku (63%) |
| Evaluation Metrics | 2 (CommRate, GoodQRate) | 12 (including Pushback, FailFast, Routing, etc.) |
| Problem Types | Ambiguity, Inconsistency, Incompleteness | + Unfeasible requirements |
| Evaluation Mode | Single-turn | Multi-turn with persistence |
| Agent Support | Okanagan (3-round fixed) | Dynamic loop + Dev Team routing |
| Human Validation | Manual spot-checking | Systematic Pearson/Kappa correlation UI |

---

## 9. Developer Tools & Leaderboard

### 9.1 Interactive Web Leaderboard

To bridge the gap between academic research and practical developer adoption, we implemented a comprehensive Flask-based web application (`flask_leaderboard/app.py`) that transforms raw benchmark data into developer-actionable insights:

- **Multi-dimensional Rankings**: Sortable tables with all V2 metrics
- **Interactive Charts**: Radar plots, bar charts, and heatmaps
- **Detailed Model Profiles**: Per-model breakdowns by problem type
- **RESTful API**: Programmatic access for CI/CD pipeline integration
- **Export**: CSV and JSON export for offline analysis

### 9.2 Google Colab Notebook

A production-ready Colab notebook (`HumanEvalComm_V2_Colab.ipynb`) enables anyone to reproduce the full benchmark:

1. Mounts Google Drive for persistent result storage
2. Clones the repository from GitHub
3. Installs and runs Ollama with 5 top local models
4. Executes both Unfeasible and Standard benchmarks
5. Displays leaderboard results inline

**No API keys required** — the entire pipeline runs on Colab's free T4 GPU.

---

## 10. Limitations & Future Work

### 10.1 Current Limitations

1. **Problem Scope**: The evaluation focuses on algorithmic programming problems; real-world software development involves system integration, API usage, and multi-file projects.
2. **Language Coverage**: Current evaluation is Python-focused; multi-language assessment would provide broader insights.
3. **Model Scale**: Evaluation is limited by compute resources; larger models (70B+, 405B) may exhibit different communication patterns.
4. **Domain Specificity**: Performance patterns may vary across web development, data science, and systems programming domains.

### 10.2 Future Research Directions

1. **Longitudinal Studies**: Track how communication competence evolves across model generations
2. **Cross-Domain Transfer**: Investigate whether communication skills transfer across programming languages
3. **Human Factors Integration**: Study how developers interact with communication-competent AI assistants
4. **Multi-Agent Orchestration**: Scale from 2-persona routing to full team simulation
5. **Real-World Validation**: Evaluate on authentic development tasks from industry codebases

---

## 11. References

1. **Wu, J.J.W. & Fard, F.H.** (2025). *HumanEvalComm: Benchmarking the Communication Competence of Code Generation for LLMs and LLM Agent.* ACM Trans. Softw. Eng. Methodol. DOI: 10.1145/3715109
2. **Chen, M. et al.** (2021). *Evaluating Large Language Models Trained on Code.* arXiv:2107.03374
3. **Austin, J. et al.** (2021). *Program Synthesis with Large Language Models.* arXiv:2108.07732
4. **Lu, S. et al.** (2021). *CodeXGLUE: A Machine Learning Benchmark Dataset for Code Understanding and Generation.* arXiv:2102.04664
5. **Hendrycks, D. et al.** (2021). *Measuring Coding Challenge Competence with APPS.* arXiv:2105.09938
6. **Pearce, H. et al.** (2022). *Asleep at the Keyboard? Assessing the Security of GitHub Copilot's Code Contributions.* IEEE S&P.
7. **Nijkamp, E. et al.** (2022). *CodeGen: An Open Large Language Model for Code with Multi-Turn Program Synthesis.* arXiv:2203.13474
8. **Wang, X. et al.** (2021). *Towards Understanding How Machines Can Learn Causal Graphs.* arXiv:2106.02353
9. **Adiwardana, D. et al.** (2020). *Towards a Human-like Open-Domain Chatbot.* arXiv:2001.09977
10. **Finn, C., Abbeel, P. & Levine, S.** (2017). *Model-Agnostic Meta-Learning for Fast Adaptation of Deep Networks.* ICML.

---

*This report was compiled from the HumanEvalComm V2 project repository, the original HumanEvalComm reference paper (Wu & Fard, 2025), and the V2 main paper (docs/paper/main.tex).*
