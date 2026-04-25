# CLAUDE.md

This file provides project-specific instructions for Claude Code.

Please read this before making suggestions, generating code, or changing the project structure.

---

## 1. Project Context

- **Name**: multi-agent-rag-assistant
- **Purpose**: A local, learning-focused multi-agent RAG system
- **Developer**: Junior backend developer learning LLM internals and orchestration design
- **Primary Goal**: Build a working local RAG assistant while training decision-making, design sense, and AI collaboration skills

---

## 2. Important: Developer Learning Mode

This project is for learning, not just fast implementation.

Follow these rules carefully.

---

## 3. When Generating Code

Before giving code, explain briefly:

1. Why this structure was chosen
2. At least one simpler or alternative approach, if any
3. Tradeoffs of this code
   - Pros
   - Cons
4. Core concepts I need to understand

Keep the explanation short and practical.

Do not generate large code blocks without explaining the reasoning first.

---

## 4. When Making Design Decisions

Do not immediately recommend a solution.

First, ask for my selection criteria.

If I do not provide criteria, ask up to 3 clarifying questions first.

After giving a recommendation, always explain:

- Why this choice fits the criteria
- What alternatives were considered
- Cases where this choice could be wrong

---

## 5. Things I Tend to Miss

I have experience in infrastructure, CI/CD, Docker, and AWS, but I have less hands-on experience with LLM internals.

When explaining LLM-related topics, provide more detail than usual.

Important areas where I may need extra explanation:

- Chunking
- Embedding
- Retrieval
- Reranking
- Prompt design
- LangGraph State
- Agent orchestration
- Evaluator design
- Retry logic

When using a design pattern name, explain what it means.

Use Korean when explaining concepts to me in chat.

---

## 6. How to Explain Things to Me

Use analogies from infrastructure, DevOps, Docker, CI/CD, or AWS when helpful.

Good examples:

- LangGraph State is similar to state passed between steps in AWS Step Functions.
- A retriever is similar to a search layer between storage and application logic.
- An evaluator is similar to a quality gate in a CI/CD pipeline.
- Docker Compose is a local orchestration tool for development dependencies.

Keep explanations short enough to avoid overthinking.

---

## 7. Prohibited Behavior

Do not:

- Say “this is best practice” without explaining why
- Add features I did not ask for
- Increase complexity without asking for permission first
- Suggest features outside the current project scope
- Touch v2/v3 features before v1 is working
- Generate code that hides important logic from me
- Refactor broadly without explaining the reason

---

## 8. Tech Stack

### Backend

- FastAPI
- Python 3.12

### Orchestration

- LangGraph

### Vector Database

- PostgreSQL
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

## 9. Coding Rules

- Use type hints
- Write function docstrings
- Prefer clear and simple code over clever code
- Keep functions small and explainable
- If a file grows beyond 300 lines, consider splitting it
- Use comments only when they explain why, not what
- For important decisions, leave comments with the `WHY:` prefix

Example:

```python
# WHY: Keep chunk size fixed in v1 to reduce tuning complexity.
chunk_size = 800