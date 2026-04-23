# Project Handoff Document

This document provides context for continuing a multi-agent RAG assistant project in a new conversation. Please read this first before any work begins.

---

## 1. About Me (개발자 소개)

- 신입 백엔드 개발자, 학부 졸업 후 반년 공백기 이후 복귀 중
- Environment: Windows + WSL2 (Ubuntu), VS Code, Docker Desktop
- Local specs: RAM 64GB, VRAM 12GB

### Past Projects

**1. RAG-based SaaS Document Management Platform** (most recent team project)
- **Role**: Backend & Cloud Infrastructure Engineer (initial cloud architecture design, CI/CD pipeline, migration from local to SaaS-oriented production setup)
- **Stack**: FastAPI, PostgreSQL (pgvector), Redis, Docker, React, AWS
- **AWS Architecture Design & Migration**:
  - Designed the initial cloud architecture and led migration from a local Docker Compose environment to a SaaS-oriented production setup
  - Evaluated a serverless approach using Lambda + API Gateway; found it not suitable due to deployment package size constraints, cold-start overhead, and the 15-minute execution-time limit
  - Later migrated the backend to ECS Fargate, which improved operational stability and better fit the workload
  - Implemented AWS networking and security architecture: VPC design, subnet separation, least-privilege security groups, NACLs, and ALB-based routing
  - Introduced ALB to provide a stable endpoint for ECS tasks with dynamically changing IPs
  - Supported data and storage migration from local resources to managed AWS services (RDS, ElastiCache, S3)
- **CI/CD Pipeline**:
  - Backend: GitHub → GitHub Actions → Docker build → ECR push → ECS task update → Fargate deployment
  - Frontend: GitHub Actions → React build → S3 static hosting deployment
  - Deployment notifications: Discord alerts for build and deployment status
- **Monitoring (dual channel)**:
  - ECS logs: CloudWatch Logs → Lambda → Discord Webhook
  - RDS events: EventBridge → Lambda → Discord Webhook
- **Growth Area**: Would like to deepen hands-on experience in **low-level LLM internals, retrieval-quality tuning for RAG systems, and agent/orchestration design**. My primary contribution so far has been in infrastructure, deployment, and backend engineering.

**2. Missing Person Detection System** (2 years ago)
- Full backend implementation + DB design
- Stack: Python, OpenCV, YOLO, MySQL
- Features: person detection from CCTV, matching with missing persons, tracking
- Structure: monolithic (pre-Docker/CI-CD era of my journey)

### Current Career Direction (현재 목표)

- Grow into a **Cloud + Backend + DevOps combined engineer**
- NOT aiming to be an AI/ML researcher. Goal is to **leverage AI tools effectively to boost productivity**
- Currently learning: Terraform (IaC), Linux, planning Kubernetes

---

## 2. Project Overview

- **Name**: Local Multi-Agent RAG Assistant (tentative)
- **Purpose**: Development learning-focused multi-agent RAG system running locally
- **Duration**: 3-4 weeks
- **Real Goal**: NOT just a deliverable. This is a training ground for **decision-making, design sense, and AI collaboration skills** as a junior developer in the AI era
- **Supplement Goal**: Gain hands-on experience with LLM internals and orchestration design that I missed in my previous RAG project (infra-only role)

---

## 3. Tech Stack (Decided)

- **Backend**: FastAPI, Python 3.12
- **Orchestration**: LangGraph
- **Vector DB**: PostgreSQL 16 + pgvector
- **LLM**: Ollama + Qwen3 (dev/test: 4B, demo: 8B)
- **Package Manager**: uv
- **Container**: Docker + Docker Compose

---

## 4. Scope Plan

### v1 (Week 1-2)
- Ingest 2-3 markdown documents
- User query → search → answer generation flow
- FastAPI REST API (POST /ingest, POST /chat)

### v2 (Week 3)
- Planner node (query type classification)
- Evaluator node (answer quality evaluation)
- Retry logic

### v3 (Week 4, if time permits)
- MCP server wrapper
- Retrospective blog posts

---

## 5. CRITICAL: Communication Rules

**IMPORTANT — Read this section carefully before every response.**

### Language Policy (언어 정책)

- **Your responses to me**: Korean (한국어로 응답)
- **Documents I frequently read** (PRD, decision-log, journal): Korean preferred
- **AI-facing configuration files** (CLAUDE.md, prompt templates): English preferred for token efficiency
- **Shared documents** (README, architecture.md): English body + Korean comments/notes where helpful
- **Code comments and docstrings**: English by default, but use `# WHY (KR): ...` for key decisions in Korean
- When you create markdown templates for me, use **English structure + Korean explanations** so I save tokens but still understand

### When generating code
1. Before the code, explain WHY this structure in 1-3 lines
2. Mention at least 1 alternative if any exists
3. Explain tradeoffs (pros and cons)
4. Point out core concepts I need to understand

### When making design decisions
1. Don't push a recommendation first. Ask about MY selection criteria first
2. If I don't share criteria, ask up to 3 clarifying questions
3. After recommending, explain "cases where this choice could be wrong"

### Things I tend to miss
- Strong in infra/CI-CD/AWS, but **weak in LLM internals**
- Need more detailed explanations for LLM-related decisions
- When using design pattern names, explain the meaning too
- Respond in Korean (한국어)

### Leverage my strengths in explanations
- I grasp things faster when connected to infra/DevOps/networking concepts
- Example: "LangGraph State is similar to AWS Step Functions state" — analogies like this are welcome
- AWS/Docker/CI-CD analogies work great for me

### Prohibited
- No "because it's best practice" without reasoning
- Don't add features I didn't ask for
- Ask permission before proposing anything that increases complexity
- Don't propose features outside v1 scope
- No long explanations that trigger overthinking (I tend to fall into analysis paralysis)

---

## 6. My AI Collaboration Principles (what I commit to)

- Treat AI responses as "drafts," never as final answers
- Record major tech decisions in decision-log.md (reason/alternatives/rejection reasons)
- Before implementing, ask "is there a simpler alternative?" once
- Cross-verify between Claude and Codex regularly
- If AI gives wrong answer twice in a row, switch to official docs

---

## 7. Current Status (Day 0 Complete)

✅ Repository created and first commit pushed
✅ Folder structure created (app/, docs/, tests/, data/)
✅ Documents written: DECLARATION.md, CLAUDE.md, PRD.md, decision-log.md, doubts.md, journal.md
✅ Python environment with uv + dependencies installed (pyproject.toml)
✅ .env.example, .env, .gitignore written
✅ Docker Desktop installation verified

---

## 8. Folder Structure

```
multi-agent-rag-assistant/
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ api/
│  │  ├─ chat.py
│  │  └─ ingest.py
│  ├─ agent/
│  │  ├─ state.py
│  │  ├─ graph.py
│  │  └─ nodes.py
│  ├─ rag/
│  │  ├─ ingest.py
│  │  ├─ embed.py
│  │  └─ retrieve.py
│  ├─ evaluation/
│  │  └─ evaluator.py
│  └─ db/
│     ├─ models.py
│     └─ session.py
├─ docs/
│  ├─ PRD.md
│  ├─ architecture.md
│  ├─ decision-log.md
│  ├─ doubts.md
│  ├─ journal.md
│  └─ HANDOFF.md (this file)
├─ tests/
├─ data/sample/
├─ docker-compose.yml (not yet written)
├─ pyproject.toml
├─ .env.example / .env
├─ README.md
├─ CLAUDE.md
└─ DECLARATION.md
```

---

## 9. Next Tasks (Day 1)

- STEP 9: Write Docker Compose for PostgreSQL + pgvector
- STEP 10: Install Ollama + pull Qwen3 4B model
- STEP 11: FastAPI Hello World + DB connection check
- STEP 12: Follow LangGraph official Quickstart (using Claude Code learning mode)

---

## 10. My Tendencies to Watch

- **Overthinking**: I fall into analysis paralysis, preparing endlessly instead of deciding → prefer short, clear directives
- **Perfectionism**: Training myself to tolerate incomplete states and move forward
- **AI dependence vs autonomy**: Balancing this is the core training goal of this project

---

## First Request

If you've understood the context, just reply **"컨텍스트 확인 완료"**. Then I will request specific tasks one by one.