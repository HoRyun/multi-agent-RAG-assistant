# PRD: Local Multi-Agent RAG Assistant

## 1. One-line Summary

A local, learning-focused multi-agent RAG assistant for development documents.

The system ingests development documents, retrieves relevant context for user questions, generates grounded answers, and later evaluates answer quality with retry logic.

---

## 2. Project Motivation

This project is not only a deliverable.  
It is a training project for building practical judgment, design sense, and AI collaboration skills as a junior backend developer.

Goals:

- Learn the basic flow of LLM-powered applications
- Gain hands-on experience with LangGraph orchestration
- Implement the core RAG flow: chunking, embedding, retrieval, generation
- Practice using AI tools effectively without blindly trusting them
- Build a portfolio project focused on decision-making, not just features

---

## 3. Target User / Persona

Primary user:

- Myself
- Junior backend developer
- Frequently reads official docs and learning materials

Secondary persona:

- Junior developers who want grounded answers based on technical documents
- Users who prefer source-backed AI answers over unsupported responses

---

## 4. Core User Scenario

1. The user ingests official documents or markdown learning materials.
2. The user asks a question.
   - Example: `How should State be designed in LangGraph?`
3. The system retrieves relevant document chunks.
4. The system generates an answer based on the retrieved context.
5. The system evaluates answer quality.
   - v2 or later
6. If quality is low, the system retries.
   - v2 or later
7. The system returns the final answer with source references.

---

## 5. v1 Scope: MVP within 2 Weeks

### Included in v1

- Ingest 2–3 markdown documents
- User question → retrieval → answer generation flow
- FastAPI REST API
  - `POST /ingest`
  - `POST /chat`
- Store vectors using PostgreSQL + pgvector
- Use local LLM through Ollama + Qwen

### Excluded from v1

- Planner agent
- Evaluator agent
- Retry logic
- Frontend UI
- Multi-user support
- Complex authentication
- Production-level deployment

---

## 6. v2 Scope: Agentic Flow Extension

Planned for week 3.

### Planned Features

- Planner node
  - Classify query type
  - Decide whether retrieval is needed
- Evaluator node
  - Evaluate answer quality
  - Check whether the answer is grounded in retrieved context
- Retry logic
  - Retry retrieval or generation when quality is low
- Evaluation logs

---

## 7. v3 Scope: Optional Extensions

Planned for week 4 if time permits.

### Optional Features

- MCP server wrapper
- Simple CLI interface
- Retrospective blog post
- Architecture review document

---

## 8. Tech Stack

### Backend

- FastAPI
- Python 3.12

### Orchestration

- LangGraph

### Vector Database

- PostgreSQL 16
- pgvector

### Local LLM

- Ollama
- Qwen3
  - Qwen3 4B for development and testing
  - Qwen3 8B for final demo

### Container

- Docker
- Docker Compose

---

## 9. Success Criteria

### v1 Success

- [ ] Ingest 2–3 markdown documents
- [ ] Retrieve relevant document chunks for a user question
- [ ] Generate an answer based on retrieved context
- [ ] Return source references with the answer

### v2 Success

- [ ] Planner classifies the query type
- [ ] Evaluator scores answer quality
- [ ] Retry logic runs when quality is low
- [ ] Evaluation results are logged

### Learning Success

- [ ] Record major technical decisions in `docs/decision-log.md`
- [ ] Explain the project structure and major design decisions after 4 weeks
- [ ] Commit only code that I understand

---

## 10. Failure Conditions

The main failure is not lack of features.  
The main failure is implementing code without understanding it.

Avoid:

- Committing AI-generated code without understanding it
- Failing to complete v1 within 2 weeks
- Expanding scope before the core v1/v2 flow is done
- Being unable to explain why the system was designed this way
- Leaving only code without decision records

---

## 11. AI Collaboration Principles

- Treat AI responses as drafts, not final answers.
- Record important technical decisions in `decision-log.md`.
  - Decision
  - Reason
  - Alternatives
  - Rejected alternatives
  - Tradeoffs
- Before implementation, ask:
  - `Is there a simpler alternative for v1?`
- Do not use AI-generated designs directly without review.
- Rewrite important designs in my own words before applying them.
- Cross-check important questions between Claude and Codex.
- If AI gives wrong answers repeatedly, switch to official documentation.

---

## 12. Self-Evaluation Checkpoints

### End of Week 1

- Can I explain LangGraph State in my own words?
- Can I explain how FastAPI connects to the LangGraph flow?

### End of Week 2

- Can I explain the difference between chunking, embedding, and retrieval?
- Can I explain how pgvector stores and searches document vectors?
- Can I explain the v1 API flow from ingestion to answer generation?

### End of Week 3

- Can I explain why an Evaluator is needed?
- Can I explain when retry logic should run?
- Can I explain the Planner → Retriever → Generator → Evaluator flow?

### End of Week 4

- Can I explain why this tech stack was chosen?
- Can I explain which alternatives were rejected and why?
- Can I explain this project clearly in a portfolio context?

---

## 13. Out of Scope

This is a local learning project.  
The following are intentionally excluded:

- Production-level authentication and authorization
- Large-scale distributed processing
- Custom embedding model training
- Advanced frontend UI
- Multi-tenant SaaS architecture
- Complex cloud deployment
- LLM fine-tuning