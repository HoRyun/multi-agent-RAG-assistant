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

---

## Day 2 - 2026-04-27

### 완료한 것

- **STEP 14**: `rag_chunks` SQLAlchemy 모델 작성 — pgvector `Vector(768)` 컬럼, `source_path + chunk_index` unique constraint 포함, DB 연결은 `POSTGRES_*` 개별 설정으로 구성
- **STEP 15**: `app/rag/chunk.py` 작성 — 고정 문자 수 기반 chunking, chunk_size=800 / overlap=100 / min_chunk_size=50 기본값, 파라미터 검증 포함, 테스트 8개 통과
- **STEP 16**: `app/rag/embed.py` 작성 — `/api/embed` 우선 호출 후 `/api/embeddings` fallback, 빈 텍스트 및 dimension 검증, 명시적 예외 처리, 테스트 9개 통과
- **STEP 17**: `app/rag/ingest.py` 작성 — markdown 파일 읽기 → chunk → embed → DB 저장 파이프라인, sample markdown 3개 추가(`fastapi.md`, `langgraph.md`, `rag.md`)
- **STEP 18**: ingest 검증 — 6 chunks (파일당 2개), chunk_index 순서 확인, 재실행 후 count 동일하여 멱등성 확인

### 오늘 만든 흐름

```text
Markdown file
→ chunk_text()
→ embed_text()
→ RagChunk
→ PostgreSQL + pgvector
```

### 오늘 배운 것

- overlap이 있으면 마지막 chunk가 min_chunk_size 미만이어도 포함될 수 있다. 테스트 기대값을 직접 계산해서 검증해야 한다.
- 외부 API 호출(embedding)과 DB transaction은 분리하는 것이 낫다. embedding이 오래 걸릴 경우 DB connection을 불필요하게 잡지 않기 위해서다.
- `except Exception: pass` 같은 silent catch는 디버깅을 어렵게 만든다. 어떤 예외를 잡고 어떻게 처리할지 명시적으로 정의해야 한다.
- retry 가능한 오류(네트워크 오류)와 retry하면 안 되는 오류(잘못된 입력, dimension mismatch)를 구분하는 것이 중요하다.

### 오늘의 의사결정

1. **DATABASE_URL 대신 POSTGRES_* 개별 설정 사용**
   - 선택: `POSTGRES_HOST`, `POSTGRES_PORT` 등 개별 환경변수로 URL 조합
   - 이유: health check 등 다른 곳에서 이미 개별 값을 재사용 중. 각 값의 출처가 더 명확하다.
   - 단점: URL 문자열 조합 실수 가능성이 있다.
   - 나중에 바꿀 수 있는 경우: 설정 관리 방식을 일원화할 때, 또는 DATABASE_URL이 외부에서 주입되는 환경(Cloud Run 등)으로 이동할 때

2. **v1 chunker는 고정 문자 수 기반으로 유지**
   - 선택: 토큰 수가 아닌 문자 수 기준으로 chunk
   - 이유: 토크나이저 의존성 없이 단순하게 구현 가능. v1에서 chunking 전략을 튜닝하는 것은 과한 투자다.
   - 단점: 토큰 수 기준과 다르게 동작할 수 있어 실제 context window 계산이 부정확해질 수 있다.
   - 나중에 바꿀 수 있는 경우: 검색 품질 문제가 실제로 발생하거나, LLM context 초과 이슈가 생길 때

3. **ingest는 DELETE + INSERT 방식으로 멱등성 보장**
   - 선택: 같은 `source_path`의 기존 rows를 삭제한 뒤 새로 insert
   - 이유: 파일이 변경되어 재실행해도 중복 없이 최신 상태를 유지할 수 있다.
   - 단점: 대용량 파일이라면 삭제 후 재삽입 비용이 크다. upsert가 더 효율적일 수 있다.
   - 나중에 바꿀 수 있는 경우: 파일 수나 chunk 수가 많아져 성능 문제가 생길 때

### 아직 이해하고 넘어가야 할 것

- SQLAlchemy Session과 transaction 범위 — `with session:` 블록이 정확히 어디서 commit/rollback되는지
- pgvector Vector dimension과 embedding model dimension의 관계 — dimension이 다르면 저장이 막히는지 검색이 틀어지는지
- chunk_size / overlap / min_chunk_size가 실제 검색 품질에 어떤 영향을 주는지
- retry 가능한 오류와 retry하면 안 되는 오류를 코드 수준에서 어떻게 분리할지 (`EmbeddingValidationError` 분리 후보)

### 내일 할 것

- `retrieve` 함수 구현 — pgvector similarity search 학습
- 검색 결과를 `source_path`, `chunk_index`, `content` 형태로 반환
- 그 다음 FastAPI `/chat` 또는 LangGraph node 연결 검토

---

## Day 3 - 2026-04-29

### 완료한 것

- **STEP 20**: `app/rag/retrieve.py` 작성 — pgvector `cosine_distance` 연산자로 유사 청크 검색, `RetrieveResult(chunk, distance)` dataclass 반환, `top_k` 파라미터 검증 포함
- **STEP 21**: `tests/test_retrieve.py` 작성 — 7개 단위 테스트 통과 (전체 24개 통과)

### 만든 흐름

```text
query string
→ embed_text()          # 쿼리 벡터 생성
→ cosine_distance()     # pgvector <=> 연산자로 유사도 계산
→ ORDER BY distance     # 가까운 것부터 정렬
→ LIMIT top_k           # 상위 k개 반환
→ list[RetrieveResult]
```

### 오늘 배운 것

- pgvector-python의 SQLAlchemy 통합은 `column.cosine_distance(vector)` 메서드를 직접 지원한다. SQL 직접 작성 없이 ORM 수준에서 벡터 연산이 가능하다.
- `session.query(Model, expr.label("name"))` 패턴으로 모델 인스턴스와 계산값을 동시에 SELECT할 수 있다. 결과 row는 `row[0]`, `row[1]`로 접근한다.
- `SessionLocal` 같은 context manager를 테스트에서 mock할 때는 `__enter__`와 `__exit__`를 각각 MagicMock으로 설정해야 한다. `MagicMock()` 기본 설정만으로는 context manager protocol이 완전하지 않다.
- `monkeypatch.setattr("app.rag.retrieve.embed_text", ...)` 처럼 테스트 대상 모듈의 import 경로로 patch해야 한다. 원본 모듈 경로(`app.rag.embed.embed_text`)로 patch하면 효과가 없다.

### 오늘의 의사결정

1. **cosine distance 선택 (vs L2 distance)**
   - 선택: `cosine_distance` (`<=>` 연산자)
   - 이유: 텍스트 임베딩은 벡터 크기보다 방향이 의미를 나타낸다. 같은 의미의 텍스트라도 길이 차이에 따라 L2 거리가 달라질 수 있다.
   - 단점: dot product 방식(내적)보다 연산 비용이 약간 높다.
   - 나중에 바꿀 수 있는 경우: 검색 품질 실험에서 L2 또는 inner product가 더 좋은 결과를 보일 때

2. **`RetrieveResult` dataclass 도입**
   - 선택: raw `RagChunk` 대신 `(chunk, distance)` 쌍을 묶는 dataclass 반환
   - 이유: distance 값을 함께 반환하면 호출자가 threshold 필터링이나 디버깅에 활용할 수 있다.
   - 단점: 한 단계 더 감싸는 구조라 단순 content 접근 시 `result.chunk.content`로 deeper해진다.

### 아직 이해하고 넘어가야 할 것

- cosine distance 범위(0~2)와 실제 검색 결과 품질의 관계 — 어떤 threshold 이상이면 "관련 없음"으로 봐야 하는지
- `SELECT Model, expr` 시 SQLAlchemy가 어떻게 두 컬럼을 하나의 Row 객체로 묶는지 (ORM 내부 동작)
- pgvector index (ivfflat, hnsw)의 필요성 — 지금은 full scan, 데이터가 많아지면 언제 index가 필요한지

### 다음 할 것

- LangGraph RAG 노드 연결 — retrieve 결과를 LangGraph state에 넣기
- `/chat` API 또는 CLI에서 질문 → 검색 → 답변 흐름 완성