# 프로젝트 인수인계 문서 (한국어 요약본)

> 이 문서는 `HANDOFF.md`의 한국어 번역본입니다.
> AI에게 전달할 때는 영어 원본(`HANDOFF.md`)을 사용하고, 
> 본인이 복습·회고할 때는 이 한국어본을 읽으세요.

## 1. 나에 대해
- 신입 백엔드 개발자 (학부 졸업, 반년 공백 후 복귀)
- 환경: Windows + WSL2, VS Code, Docker Desktop
- 로컬 스펙: RAM 64GB, VRAM 12GB

### 과거 프로젝트
1. **RAG 기반 SaaS 문서 관리 플랫폼** - 백엔드 및 클라우드 인프라 엔지니어
   - 로컬 Docker Compose 환경을 SaaS형 운영 환경으로 전환하기 위한 초기 클라우드 아키텍처 설계 및 마이그레이션 주도
   - Lambda + API Gateway 기반 서버리스 접근을 검토했으나, 배포 패키지 크기 제약 / 콜드 스타트 오버헤드 / 15분 실행 시간 제한으로 인해 적합하지 않다고 판단
   - 이후 ECS Fargate로 백엔드를 전환 → 운영 안정성 개선 및 워크로드에 더 적합한 구조 확보
   - VPC 설계, 서브넷 분리, 최소 권한 원칙의 Security Group, NACL, ALB 기반 라우팅 구현
   - ECS 태스크 IP가 동적으로 바뀌는 문제 해결을 위해 ALB 도입 (안정적인 엔드포인트 제공)
   - CI/CD 파이프라인 + Discord 배포 알림
   - 모니터링 이원화 (CloudWatch Logs / EventBridge → Lambda → Discord Webhook)
   - 로컬 데이터/스토리지를 RDS, ElastiCache, S3 같은 AWS 관리형 서비스로 이전 지원
   - **성장하고 싶은 영역**: LLM 내부 구조, RAG 검색 품질 튜닝, 에이전트/오케스트레이션 설계에 대한 더 깊은 실무 경험 (지금까지는 인프라·배포·백엔드 엔지니어링 중심 기여)

2. **실종자 탐색 시스템** (2년 전)
   - Python, OpenCV, YOLO, MySQL
   - 모놀리틱 구조 (DevOps 개념 미적용 시절)

### 현재 목표
- 클라우드 + 백엔드 + DevOps 통합 엔지니어
- AI 도구를 업무에 효과적으로 활용하는 개발자 (AI 연구자 X)
- 학습 중: Terraform, Linux, Kubernetes 예정

## 2. 프로젝트 개요
- **이름**: Local Multi-Agent RAG Assistant
- **기간**: 3~4주
- **진짜 목적**: 판단력, 설계 감각, AI 협업 능력 훈련
- **보완 목표**: 과거 인프라 역할로 못 했던 LLM 내부 로직과 오케스트레이션 경험

## 3. 기술 스택
- FastAPI, Python 3.12
- LangGraph
- PostgreSQL + pgvector  
- Ollama + Qwen3 (4B 개발용, 8B 데모용)
- uv, Docker Compose

## 4. 범위
- **v1 (1~2주차)**: 문서 적재 + 검색 + 답변
- **v2 (3주차)**: Planner + Evaluator + 재시도
- **v3 (4주차)**: MCP 서버, 블로그 글

## 5. AI 소통 규칙 핵심

### 언어 정책
- AI 응답: 한국어
- 문서 (PRD, journal 등): 한국어
- AI 참조용 파일 (CLAUDE.md, 프롬프트): 영어 (토큰 절약)
- 공용 문서 (README, architecture): 영어 본문 + 한국어 주석
- 코드: 영어 주석 기본, 주요 결정은 `# WHY (KR):`로 한국어

### 내게 응답할 때 지켜야 할 것
- 코드 주기 전 "왜 이 구조인지" 설명
- 대안 최소 1개 언급
- 트레이드오프 설명
- 패턴 이름 쓸 때 뜻 같이 설명

### 내 강점 활용
- AWS/Docker/CI-CD 비유로 설명하면 빨리 이해함
- 예: "LangGraph State = AWS Step Functions state"

### 금지
- "best practice이니까" 금지
- 범위 밖 기능 제안 금지
- 오버띵킹 유발하는 긴 설명 금지

## 6. 현재 상태 (Day 0 완료)
- 저장소, 폴더 구조, 문서 전부 완료
- uv 환경 + 의존성 설치 완료

## 7. 다음 할 일 (Day 1)
- Docker Compose 작성 (PostgreSQL + pgvector)
- Ollama 설치 + Qwen3 4B pull
- FastAPI Hello World
- LangGraph Quickstart