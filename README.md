# Local Multi-Agent RAG Assistant

로컬 환경에서 동작하는 개발 학습용 멀티 에이전트 RAG 시스템.

## 목적
신입 개발자의 LLM 시스템 설계 학습과 AI 협업 훈련을 위한 프로젝트.

## 기술 스택
- Backend: FastAPI, Python 3.12
- Orchestration: LangGraph
- Vector DB: PostgreSQL + pgvector
- LLM: Ollama (Qwen3 4B: 개발/테스트용, Qwen3 8B: 최종 실행/데모용)
- Package Manager: uv

## 프로젝트 상태
🚧 개발 중 (Day 0)

## 문서
- [PRD](./docs/PRD.md)
- [Decision Log](./docs/decision-log.md)
- [Declaration](./DECLARATION.md)

## 개발 환경 설정
(내일 작성 예정)

## Agent Development Journal CLI

작업 기록은 `.dev-journal/traces/{task_id}.json`에 저장되고, export 결과는
`.dev-journal/journals/{task_id}.md`에 저장됩니다.

```bash
uv run dev-journal new day-1 --goal "Agent Development Journal MVP 구현"
uv run dev-journal add-test day-1 --command "uv run pytest" --result "passed" --note "MVP 테스트 통과"
uv run dev-journal add-review day-1 --severity medium --note "README 사용 예시 필요"
uv run dev-journal add-decision day-1 --note "표준 라이브러리 argparse 사용" --reason "MVP에는 Typer 없이 충분함"
uv run dev-journal add-lesson day-1 --note "파일 기반 기록은 작은 CLI에 적합함"
uv run dev-journal export day-1
```

`uv run` 없이 실행하려면 프로젝트 가상환경을 활성화합니다.

```bash
source .venv/bin/activate

dev-journal new day-1 --goal "Agent Development Journal MVP 구현"
dev-journal export day-1
```

또는 가상환경을 활성화하지 않고 직접 실행할 수 있습니다.

```bash
.venv/bin/dev-journal new day-1 --goal "Agent Development Journal MVP 구현"
```
