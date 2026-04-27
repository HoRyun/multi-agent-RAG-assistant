# PRD: Local Multi-Agent RAG Assistant

> 이 문서는 `PRD.md`의 한국어 번역본입니다.  
> AI에게 전달할 때는 영어 원본(`PRD.md`)을 사용하고,  
> 본인이 복습·회고할 때는 이 한국어본을 읽으세요.

## 1. 한 줄 요약

개발 문서를 대상으로 동작하는 로컬 환경의 학습용 멀티 에이전트 RAG 어시스턴트.

이 시스템은 개발 문서를 적재하고, 사용자 질문에 필요한 관련 컨텍스트를 검색하며, 근거 기반 답변을 생성한다. 이후 버전에서는 답변 품질을 평가하고, 필요하면 재시도하는 로직까지 포함한다.

---

## 2. 프로젝트 동기

이 프로젝트는 단순한 결과물을 만들기 위한 프로젝트가 아니다.  
신입 백엔드 개발자로서 실전적인 판단력, 설계 감각, AI 협업 능력을 기르기 위한 훈련 프로젝트다.

목표:

- LLM 기반 애플리케이션의 기본 흐름을 학습한다.
- LangGraph 기반 오케스트레이션을 직접 경험한다.
- RAG의 핵심 흐름인 청킹, 임베딩, 검색, 생성을 구현한다.
- AI 도구를 맹목적으로 믿지 않고 효과적으로 활용하는 연습을 한다.
- 단순 기능 구현이 아니라 의사결정 중심의 포트폴리오 프로젝트를 만든다.

---

## 3. 대상 사용자 / 페르소나

주 사용자:

- 나 자신
- 신입 백엔드 개발자
- 공식 문서와 학습 자료를 자주 읽는 개발자

보조 사용자:

- 기술 문서 기반의 근거 있는 답변을 원하는 주니어 개발자
- 출처 없는 AI 답변보다, 근거 문서가 함께 제공되는 답변을 선호하는 사용자

---

## 4. 핵심 사용자 시나리오

1. 사용자가 공식 문서 또는 마크다운 학습 자료를 시스템에 적재한다.
2. 사용자가 질문을 입력한다.
   - 예시: `LangGraph에서 State는 어떻게 설계해야 하는가?`
3. 시스템이 관련 문서 조각을 검색한다.
4. 시스템이 검색된 컨텍스트를 바탕으로 답변을 생성한다.
5. 시스템이 답변 품질을 평가한다.
   - v2 이후
6. 품질이 낮으면 시스템이 재시도한다.
   - v2 이후
7. 시스템이 최종 답변과 출처 정보를 함께 반환한다.

---

## 5. v1 범위: 2주 내 MVP

### v1에 포함

- 마크다운 문서 2~3개 적재
- 사용자 질문 → 검색 → 답변 생성 흐름
- FastAPI REST API
  - `POST /ingest`
  - `POST /chat`
- PostgreSQL + pgvector를 사용한 벡터 저장
- Ollama + Qwen을 통한 로컬 LLM 사용

### v1에서 제외

- Planner agent
- Evaluator agent
- Retry logic
- Frontend UI
- Multi-user support
- Complex authentication
- Production-level deployment

---

## 6. v2 범위: 에이전트 흐름 확장

3주차에 진행할 계획이다.

### 예정 기능

- Planner node
  - 질문 유형 분류
  - 검색이 필요한 질문인지 판단
- Evaluator node
  - 답변 품질 평가
  - 답변이 검색된 컨텍스트에 근거하고 있는지 확인
- Retry logic
  - 품질이 낮을 경우 검색 또는 생성을 재시도
- Evaluation logs

---

## 7. v3 범위: 선택 확장

시간이 허락하면 4주차에 진행한다.

### 선택 기능

- MCP server wrapper
- Simple CLI interface
- Retrospective blog post
- Architecture review document

---

## 8. 기술 스택

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
  - Qwen3 4B: 개발 및 테스트용
  - Qwen3 8B: 최종 데모용

### Container

- Docker
- Docker Compose

---

## 9. 성공 기준

### v1 성공 기준

- [ ] 마크다운 문서 2~3개를 적재할 수 있다.
- [ ] 사용자 질문에 대해 관련 문서 조각을 검색할 수 있다.
- [ ] 검색된 컨텍스트를 기반으로 답변을 생성할 수 있다.
- [ ] 답변과 함께 출처 정보를 반환할 수 있다.

### v2 성공 기준

- [ ] Planner가 질문 유형을 분류한다.
- [ ] Evaluator가 답변 품질을 점수화한다.
- [ ] 품질이 낮을 때 재시도 로직이 실행된다.
- [ ] 평가 결과가 로그로 기록된다.

### 학습 성공 기준

- [ ] 주요 기술 결정을 `docs/decision-log.md`에 기록한다.
- [ ] 4주 후 프로젝트 구조와 주요 설계 결정을 설명할 수 있다.
- [ ] 내가 이해한 코드만 커밋한다.

---

## 10. 실패 조건

주요 실패는 기능이 부족한 것이 아니다.  
주요 실패는 이해하지 못한 채 코드를 구현하는 것이다.

피해야 할 것:

- AI가 생성한 코드를 이해하지 못한 채 커밋하는 것
- v1을 2주 안에 완료하지 못하는 것
- v1/v2 핵심 흐름이 끝나기 전에 범위를 확장하는 것
- 시스템을 왜 이렇게 설계했는지 설명하지 못하는 것
- 의사결정 기록 없이 코드만 남기는 것

---

## 11. AI 협업 원칙

- AI 응답은 최종 답변이 아니라 초안으로 취급한다.
- 중요한 기술 결정은 `decision-log.md`에 기록한다.
  - 결정
  - 이유
  - 대안
  - 거절한 대안
  - 트레이드오프
- 구현 전에 다음 질문을 한다.
  - `v1 기준으로 더 단순한 대안이 있는가?`
- AI가 생성한 설계를 검토 없이 그대로 사용하지 않는다.
- 중요한 설계는 적용하기 전에 내 언어로 다시 정리한다.
- 중요한 질문은 Claude와 Codex에 교차 검증한다.
- AI가 반복해서 틀리면 공식 문서를 확인한다.

---

## 12. 자기 평가 체크포인트

### 1주차 종료 시점

- LangGraph State를 내 언어로 설명할 수 있는가?
- FastAPI가 LangGraph 흐름과 어떻게 연결되는지 설명할 수 있는가?

### 2주차 종료 시점

- 청킹, 임베딩, 검색의 차이를 설명할 수 있는가?
- pgvector가 문서 벡터를 어떻게 저장하고 검색하는지 설명할 수 있는가?
- 문서 적재부터 답변 생성까지 v1 API 흐름을 설명할 수 있는가?

### 3주차 종료 시점

- Evaluator가 왜 필요한지 설명할 수 있는가?
- Retry logic이 언제 실행되어야 하는지 설명할 수 있는가?
- Planner → Retriever → Generator → Evaluator 흐름을 설명할 수 있는가?

### 4주차 종료 시점

- 왜 이 기술 스택을 선택했는지 설명할 수 있는가?
- 어떤 대안을 왜 거절했는지 설명할 수 있는가?
- 이 프로젝트를 포트폴리오 관점에서 명확히 설명할 수 있는가?

---

## 13. 범위 밖

이 프로젝트는 로컬 학습용 프로젝트다.  
다음 항목은 의도적으로 제외한다.

- Production-level authentication and authorization
- Large-scale distributed processing
- Custom embedding model training
- Advanced frontend UI
- Multi-tenant SaaS architecture
- Complex cloud deployment
- LLM fine-tuning