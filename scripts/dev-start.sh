#!/usr/bin/env bash
# scripts/dev-start.sh
#
# WSL2 개발 환경 시작 스크립트.
# 각 서비스의 실행 상태를 확인하고, 꺼져 있으면 시작한다.
#
# 사용법:
#   bash scripts/dev-start.sh
#
# 로그 위치:
#   .logs/ollama.log
#   .logs/fastapi.log

set -uo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$PROJECT_DIR/.logs"
mkdir -p "$LOG_DIR"

# ── 출력 헬퍼 ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

ok()    { echo -e "  ${GREEN}[OK]${NC}     $1"; }
warn()  { echo -e "  ${YELLOW}[START]${NC}  $1"; }
fail()  { echo -e "  ${RED}[FAIL]${NC}   $1"; }
header(){ echo -e "\n${BOLD}$1${NC}"; }

echo -e "${BOLD}=== dev-start: $(date '+%Y-%m-%d %H:%M:%S') ===${NC}"

# ── 1. Docker daemon ───────────────────────────────────────────────────────────
header "1. Docker"
if ! docker info &>/dev/null; then
    warn "Docker daemon이 꺼져 있음 → 시작 중..."
    # WHY: WSL2는 systemd 없이 service 명령으로 docker를 올린다.
    sudo service docker start
    sleep 3
fi

if docker info &>/dev/null; then
    ok "Docker daemon"
else
    fail "Docker daemon 시작 실패 — Docker Desktop 실행 여부를 확인하세요"
    exit 1
fi

# ── 2. PostgreSQL + pgvector ───────────────────────────────────────────────────
header "2. PostgreSQL + pgvector"
cd "$PROJECT_DIR"

POSTGRES_RUNNING=$(docker ps --filter "name=multi-agent-rag-postgres" --filter "status=running" -q)
if [ -z "$POSTGRES_RUNNING" ]; then
    warn "postgres 컨테이너가 꺼져 있음 → docker compose up -d..."
    docker compose up -d postgres
    # healthcheck 통과를 기다린다
    for i in {1..10}; do
        sleep 2
        HEALTH=$(docker inspect --format='{{.State.Health.Status}}' multi-agent-rag-postgres 2>/dev/null)
        [ "$HEALTH" = "healthy" ] && break
    done
fi

HEALTH=$(docker inspect --format='{{.State.Health.Status}}' multi-agent-rag-postgres 2>/dev/null || echo "unknown")
if [ "$HEALTH" = "healthy" ]; then
    ok "PostgreSQL (port 5432, healthcheck: healthy)"
else
    fail "PostgreSQL healthcheck 미통과 (status: $HEALTH)"
fi

# ── 3. Ollama ─────────────────────────────────────────────────────────────────
header "3. Ollama"
if curl -sf http://localhost:11434 &>/dev/null; then
    ok "Ollama (port 11434)"
else
    warn "Ollama가 꺼져 있음 → ollama serve 시작 중..."
    nohup ollama serve > "$LOG_DIR/ollama.log" 2>&1 &
    OLLAMA_PID=$!
    echo "$OLLAMA_PID" > "$LOG_DIR/ollama.pid"

    for i in {1..10}; do
        sleep 1
        curl -sf http://localhost:11434 &>/dev/null && break
    done

    if curl -sf http://localhost:11434 &>/dev/null; then
        ok "Ollama (port 11434, PID $OLLAMA_PID)"
    else
        fail "Ollama 시작 실패 — 로그: $LOG_DIR/ollama.log"
    fi
fi

# ── 4. FastAPI ─────────────────────────────────────────────────────────────────
header "4. FastAPI"
if curl -sf http://localhost:8000/health &>/dev/null; then
    ok "FastAPI (port 8000)"
else
    warn "FastAPI가 꺼져 있음 → uvicorn 시작 중..."
    cd "$PROJECT_DIR"
    # WHY: --reload 없이 기동. 개발 중 파일 변경이 필요하면 직접 uvicorn을 포어그라운드로 실행.
    nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 \
        > "$LOG_DIR/fastapi.log" 2>&1 &
    FASTAPI_PID=$!
    echo "$FASTAPI_PID" > "$LOG_DIR/fastapi.pid"

    for i in {1..10}; do
        sleep 1
        curl -sf http://localhost:8000/health &>/dev/null && break
    done

    if curl -sf http://localhost:8000/health &>/dev/null; then
        ok "FastAPI (port 8000, PID $FASTAPI_PID)"
    else
        fail "FastAPI 시작 실패 — 로그: $LOG_DIR/fastapi.log"
    fi
fi

# ── 요약 ──────────────────────────────────────────────────────────────────────
echo -e "\n${BOLD}=== 완료 ===${NC}"
echo "  Postgres : localhost:5432"
echo "  Ollama   : localhost:11434"
echo "  FastAPI  : localhost:8000"
echo "  로그     : $LOG_DIR/"
