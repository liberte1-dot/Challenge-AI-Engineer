# AI Engineer Roadmap: LLMs & Agents

An 8-week, hands-on program to go from a Python and ML foundation to building, orchestrating and deploying **agentic LLM systems**. This repository documents my progress day by day: code, deliverables and lessons learned.

## Goal

By the end of the program I want to be able to:

- Call LLM APIs reliably (async, retries, structured outputs, tool use).
- Build **RAG** pipelines with hybrid search (dense + BM25) and anti-hallucination guardrails.
- Orchestrate **agents** with LangGraph (ReAct, Plan-and-Execute, multi-agent, human-in-the-loop).
- Fine-tune open-weight models with **LoRA / QLoRA**.
- Deploy everything as a containerized API with streaming, auth, rate limiting and guardrails.

## Program overview

| Week | Theme | Main deliverable |
|---|---|---|
| 1 | LLM fundamentals, tokenization, structured outputs, function calling | Integrated mini-project (`semaine1_demo.py`) |
| 2 | RAG fundamentals and vector databases (Chroma, Qdrant) | Hybrid retriever (dense + BM25 with RRF) |
| 3 | LangChain and LCEL | Unified RAG chain with citations, memory and refusal rules |
| 4 | LangGraph: state graphs, persistence, time-travel | Persistent agent with checkpointing |
| 5 | Agent design patterns and human-in-the-loop | ReAct, Plan-and-Execute, multi-agent team, approval workflow |
| 6 | Frugal fine-tuning (PEFT, LoRA, QLoRA) | 4-bit adapter, evaluation report, merged model |
| 7 | Production deployment (FastAPI, SSE, vLLM, Docker, guardrails) | Secured, containerized API |
| 8 | Capstone portfolio project | Full agentic RAG platform, deployed with Docker |

## Progress

| Week | Status |
|---|---|
| 1. LLM fundamentals | 🔄 In progress (Day 1) |
| 2. RAG and vector databases | ⏳ Upcoming |
| 3. LangChain and LCEL | ⏳ Upcoming |
| 4. LangGraph | ⏳ Upcoming |
| 5. Agent patterns and HITL | ⏳ Upcoming |
| 6. Fine-tuning (QLoRA) | ⏳ Upcoming |
| 7. Production deployment | ⏳ Upcoming |
| 8. Capstone | ⏳ Upcoming |

### Week 1 detail

| Day | Topic | Deliverable | Status |
|---|---|---|---|
| 1 | LLM API basics and request architecture | `llm_client.py` (async client with error handling) | 🔄 In progress |
| 2 | Tokenization and context management | `token_counter.py` | ⏳ |
| 3 | Structured prompt engineering and few-shot | `prompts.py` | ⏳ |
| 4 | Structured outputs (Pydantic, JSON mode) | `structured_parser.py` | ⏳ |
| 5 | Function calling / tool use | `tool_agent.py` | ⏳ |
| 6 | Synthesis mini-project | `semaine1_demo.py` | ⏳ |
| 7 | Review | Consolidated code | ⏳ |

## Repository structure

```
.
├── jour 1/            # Day 1: async LLM client
│   ├── llm_client.py
│   ├── test_appel.py
│   ├── .env.example
│   └── README.md
├── jour 2/            # added as the program progresses
└── README.md
```

Each day lives in its own folder with its own README describing what was built, the errors encountered and what I learned.

## Tech stack

- **Language:** Python
- **LLM provider:** Google Gemini, called through its OpenAI-compatible endpoint with the `openai` library (free tier)
- **Frameworks and libraries (planned over the program):** LangChain, LangGraph, Pydantic, Qdrant, ChromaDB, Hugging Face PEFT / TRL, FastAPI, Docker, vLLM

## Getting started

```bash
git clone <this-repository-url>
cd <repository-folder>

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install openai langchain-openai pydantic python-dotenv

cd "jour 1"
cp .env.example .env               # then put your own API key in .env
python llm_client.py
```

You need your own Gemini API key (free from Google AI Studio). **Never commit your real `.env` file**: only `.env.example` is versioned.

## Target portfolio

The program aims to produce four flagship repositories:

1. **RAG-Engine-Qdrant**: RAG engine with PDF ingestion, adaptive chunking, hybrid Qdrant search and citation-based anti-hallucination rules.
2. **LangGraph-MultiAgent-HITL**: agent orchestration with a ReAct loop, multi-agent network, SQLite persistence and a human-in-the-loop checkpoint.
3. **QLoRA-Domain-Adapter**: 4-bit fine-tuning of an open-weight LLM with PEFT/TRL and adapter merging.
4. **Enterprise-LLM-Platform** (capstone): FastAPI platform with SSE streaming, vLLM, Qdrant and guardrails, containerized with docker-compose.

## Working principles

- One folder and one commit per day, with a clear deliverable.
- No secrets in the repository (`.env` is git-ignored, `.env.example` is the template).
- Understand the idea first, build a minimal version by hand, then use the framework.
- Document errors and fixes, not just successes.

## Notes

This is a learning repository. Code is written for understanding and may be refactored as the program advances.
