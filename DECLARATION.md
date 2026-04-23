# Project Declaration

This document defines why I am building the Local Multi-Agent RAG Assistant and what kind of growth I want from this project.

The goal is not just to build a working system.  
The real goal is to train judgment, design sense, and AI collaboration skills as a junior developer in the AI era.

---

## 1. Why I Am Building This Project

I am building this project to:

1. Create a personal training ground for future projects
2. Implement a multi-agent RAG system myself
3. Learn how to give better instructions to AI tools
4. Build the habit of critically reviewing AI responses
5. Become a developer who can explain design decisions, not just write code

---

## 2. Desired State After 4 Weeks

### Technical Skills

After 4 weeks, I want to be able to:

- Use vibe coding effectively instead of blindly following AI output
- Write PRD and TRD documents by myself
- Understand and explain LangGraph State-based design
- Explain the RAG flow: chunking, embedding, retrieval, generation
- Explain how FastAPI requests connect to the LangGraph flow
- Explain the role of PostgreSQL + pgvector in a RAG system

### Meta Skills

These are more important than the technical skills.

I want to build the habit of:

- Comparing at least 2 alternatives before making design decisions
- Asking “why?” repeatedly to understand tradeoffs
- Starting with imperfect decisions instead of overthinking forever
- Controlling scope creep
- Not committing code that I cannot explain

---

## 3. What I Delegate to AI vs What I Decide Myself

### Delegated to AI

I use AI as a productivity tool for:

- Boilerplate code generation
- Syntax and library usage
- Common implementation patterns
- Error message interpretation
- Test code drafts
- Documentation drafts
- Refactoring suggestions

### Decided by Me

AI can suggest, but I make the final decision for:

- Major architecture choices
- Tech stack selection
- Feature scope
- Features to remove or postpone
- v1/v2/v3 priorities
- Whether code is ready to commit
- Final wording in project documents

---

## 4. Success Conditions

Success is measured by understanding and explainability, not feature count.

### Product Success

- The system can ingest 2–3 documents and answer questions using retrieval.
- v1 completes the basic RAG flow.
- v2 runs the Planner → Retriever → Generator → Evaluator flow.
- Final answers include source references.

### Learning Success

- I can explain major technical decisions in my own words.
- The project process can be reconstructed from documents.
- I understand the core flow of AI-generated code before committing it.
- Decision reasons are recorded, not just implementation results.

---

## 5. Failure Conditions

I must avoid:

- Committing AI-generated code without understanding it
- Being unable to explain after 4 weeks why the system was designed this way
- Failing to start because of overthinking
- Expanding scope too early
- Touching v2/v3 features before v1 is complete
- Leaving only code without documentation

---

## 6. Personal Rules During This Project

### Rule 1: Keep v1 Small

v1 should stay small.

The most important v1 flow is:

```text
ingest document → retrieve chunks → generate answer → return sources