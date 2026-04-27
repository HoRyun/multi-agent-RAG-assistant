# 작업 일지

## Day 0 - [오늘 날짜]

### 완료한 것
- 저장소 생성
- 폴더 구조 생성
- DECLARATION.md 작성
- CLAUDE.md 작성
- PRD.md 초안 작성
- decision-log.md 초안 작성
- doubts.md 초안 작성

### 오늘 배운 것
- 오버띵킹은 프로젝트의 적이다
- 불완전하게 시작하는 것이 완벽하게 시작하려는 것보다 낫다

### 내일 할 것
- STEP 9부터 시작
- Docker Compose 세팅
- LangGraph Hello World

---

## Day 1 - 2026-04-25

### 완료한 것

- **STEP 9**: Docker Compose 작성 — PostgreSQL 16 + pgvector 컨테이너 정의
- **STEP 10**: pgvector 컨테이너 실행 확인 — `CREATE EXTENSION vector` 성공
- **STEP 11**: FastAPI 앱 초안 — `/health` 엔드포인트 + DB ping 포함
- **STEP 12**: Ollama 설치 — `qwen3:4b`, `nomic-embed-text` pull 완료, embedding dim 768 확인
- **STEP 13**: LangGraph Quickstart — `examples/langgraph_quickstart.py` 작성, State / Node / Edge / compile 흐름 이해

### 현재 구성

| 컴포넌트 | 실행 위치 | 포트 |
|----------|-----------|------|
| PostgreSQL + pgvector | Docker Compose | 5432 |
| FastAPI | WSL uvicorn | 8000 |
| Ollama | WSL host | 11434 |

### Day 2 next step

- DB schema for `documents` / `chunks` tables with `vector(768)`

STEP 14: DB 모델 + 테이블 생성
STEP 15: chunk_text 구현
STEP 16: embed_text 구현
STEP 17: ingest_markdown_dir 구현
STEP 18: DB 저장 + 멱등성 검증
STEP 19: 오늘 결과 검증 + 기록      