# Project Context

This project is a local-first multi-agent RAG assistant for software engineering learning.

## Primary Goal
This is not just a demo application.
The main goal is to improve the developer's ability to:
- evaluate AI-generated design decisions
- understand RAG internals
- learn orchestration and state-based workflow design
- build systems with explicit evaluation and retry loops

## Project Priorities
1. Simplicity over cleverness
2. Learnable structure over premature abstraction
3. Explicit state flow over hidden magic
4. Testability over speed of hacking
5. Documented trade-offs over blind adoption of trends

## Technical Constraints
- Python
- FastAPI
- LangGraph
- Ollama
- Qwen-based local model
- PostgreSQL + pgvector
- Local-first development
- Minimal dependencies unless clearly justified

## Coding Guidelines
- Prefer small, testable functions
- Avoid overly abstract class hierarchies
- Use type hints
- Add logs at key state transitions
- Keep node responsibilities narrow
- Every non-trivial design choice should include a brief reason

## Architecture Guidelines
- Separate planner / retriever / generator / evaluator responsibilities
- Keep graph state explicit
- Design for observability
- Suggest simpler alternatives when proposing complex designs
- Point out trade-offs, not just the idealized solution

## Response Expectations for AI Agents
When suggesting code or architecture:
1. Explain why this approach fits the project goals
2. Mention at least one simpler alternative
3. Point out one likely risk
4. Avoid unnecessary complexity
