# CLAUDE.md

This file is the entrypoint for Claude Code in this repository.

Do not treat this file as the full project context.
Use it as a routing guide and read the referenced documents when needed.

---

## 1. Mandatory First Step

Before making suggestions, generating code, or changing project structure:

1. Read this file.
2. Read only the referenced documents needed for the current task.
3. Do not load every document unless the task requires broad project context.

---

## 2. Project Snapshot

- Project name: multi-agent-rag-assistant
- Purpose: Local learning-focused multi-agent RAG assistant
- Developer: Junior backend developer learning LLM internals and orchestration design
- Main goal: Build v1 RAG flow while training design judgment and AI collaboration skills
- Default response language to the developer: Korean

---

## 3. Document Routing Guide

Use these documents depending on the task.

### Product scope / feature priority

Read:

- `docs/PRD.md`

Use this when:
- deciding whether a feature belongs in v1, v2, or v3
- checking success criteria
- avoiding scope creep
- designing API behavior

### Project philosophy / learning constraints

Read:

- `DECLARATION.md`

Use this when:
- deciding how much to delegate to AI
- checking whether implementation supports learning
- judging whether code is understandable enough to commit
- balancing speed vs understanding

### Technical decisions already made

Read:

- `docs/decision-log.md`

Use this when:
- questioning the chosen stack
- adding or changing architecture
- comparing alternatives
- proposing a new technical decision

### Open doubts / postponed concerns

Read:

- `docs/doubts.md`

Use this when:
- the developer is uncertain about a previous choice
- a topic feels like it may cause overthinking
- deciding whether to revisit or defer a concern

### Current progress / next task

Read:

- `docs/journal.md`

Use this when:
- continuing from the latest development state
- deciding the next implementation step
- checking what was completed recently

### Full project handoff context

Read:

- `docs/handoff.md`

Use this when:
- starting a new conversation
- recovering context after a long break
- needing the full background of the developer and project

Do not read `docs/handoff.md` for every small coding task.

---

## 4. Working Rules

### Code generation

Before generating code, briefly explain:

1. Why this structure is being used
2. One simpler or alternative approach
3. Tradeoffs
4. Core concept the developer should understand

Keep this explanation short and practical.

### Design decisions

Do not immediately force a recommendation.

First check the developer's criteria.
If the criteria are missing, ask up to 3 clarifying questions.

After recommending, explain:

- why it fits the criteria
- alternatives considered
- when this choice could be wrong

### Scope control

Before adding anything beyond the current task, check `docs/PRD.md`.

Do not implement v2/v3 features before v1 works.

### Communication style

- Respond to the developer in Korean.
- Use infra, Docker, AWS, CI/CD analogies when helpful.
- Explain LLM-related topics more carefully than backend topics.
- Keep explanations short enough to avoid overthinking.

---

## 5. Coding Rules

- Use type hints.
- Write function docstrings.
- Prefer clear and simple code over clever code.
- Keep functions small and explainable.
- If a file grows beyond 300 lines, consider splitting it.
- Use comments only when they explain why, not what.
- For important decisions, use `WHY:` comments.

Example:

```python
# WHY: Keep chunk size fixed in v1 to reduce tuning complexity.
chunk_size = 800