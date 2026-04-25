from fastapi import FastAPI, HTTPException
import psycopg

from app.config import settings

app = FastAPI(title="Multi-Agent RAG Assistant")


@app.get("/")
def root() -> dict:
    """Return a simple greeting to confirm the server is running."""
    return {"message": "Multi-Agent RAG Assistant is running."}


@app.get("/health")
def health() -> dict:
    """Verify DB connectivity with SELECT 1."""

    # WHY (KR): v1에서는 connection pool 없이 매 요청마다 짧게 연결합니다.
    # health check 목적은 "DB까지 닿는지" 확인하는 것이므로 SELECT 1만 실행합니다.
    try:
        with psycopg.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            dbname=settings.POSTGRES_DB,
        ) as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "db": "connected"}

    except Exception as e:
        # WHY (KR): DB가 죽어 있으면 앱은 살아 있어도 준비 상태가 아니므로 503을 반환합니다.
        raise HTTPException(status_code=503, detail=f"DB connection failed: {e}")