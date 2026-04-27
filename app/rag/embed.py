import time
from typing import Any

import httpx

from app.config import settings


class EmbeddingError(Exception):
    """Raised when embedding generation fails."""


def embed_text(text: str) -> list[float]:
    """텍스트를 Ollama embedding API로 변환해 벡터를 반환한다."""
    if not text or not text.strip():
        raise EmbeddingError("embedding할 텍스트가 비어 있습니다.")

    last_error: Exception | None = None

    for attempt in range(2):
        try:
            return _call_embed(text)
        except EmbeddingError as exc:
            last_error = exc
            if attempt == 0:
                time.sleep(2)
                continue
            break

    raise EmbeddingError(f"Ollama embedding 호출 실패: {last_error}") from last_error


def _call_embed(text: str) -> list[float]:
    errors: list[str] = []

    # WHY (KR): 현재 Ollama 공식 embedding endpoint는 /api/embed 이므로 먼저 시도한다.
    try:
        resp = httpx.post(
            f"{settings.OLLAMA_HOST}/api/embed",
            json={"model": settings.OLLAMA_EMBEDDING_MODEL, "input": text},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()

        if "embeddings" in data and data["embeddings"]:
            return _validate(data["embeddings"][0])

        errors.append("/api/embed 응답에 embeddings가 없습니다.")
    except httpx.HTTPError as exc:
        errors.append(f"/api/embed HTTP 오류: {exc}")
    except ValueError as exc:
        errors.append(f"/api/embed JSON 파싱 오류: {exc}")
    except EmbeddingError:
        raise

    # WHY (KR): 구버전 Ollama 호환성을 위해 legacy endpoint를 fallback으로 유지한다.
    try:
        resp = httpx.post(
            f"{settings.OLLAMA_HOST}/api/embeddings",
            json={"model": settings.OLLAMA_EMBEDDING_MODEL, "prompt": text},
            timeout=30.0,
        )
        resp.raise_for_status()
        data = resp.json()

        if "embedding" in data:
            return _validate(data["embedding"])

        errors.append("/api/embeddings 응답에 embedding이 없습니다.")
    except httpx.HTTPError as exc:
        errors.append(f"/api/embeddings HTTP 오류: {exc}")
    except ValueError as exc:
        errors.append(f"/api/embeddings JSON 파싱 오류: {exc}")
    except EmbeddingError:
        raise

    raise EmbeddingError(" / ".join(errors))


def _validate(vector: Any) -> list[float]:
    if not isinstance(vector, list):
        raise EmbeddingError("embedding 응답이 list가 아닙니다.")

    if len(vector) != settings.EMBEDDING_DIM:
        raise EmbeddingError(
            f"embedding 차원 불일치: 기대 {settings.EMBEDDING_DIM}, 실제 {len(vector)}"
        )

    if not all(isinstance(v, int | float) for v in vector):
        raise EmbeddingError("embedding vector에 숫자가 아닌 값이 포함되어 있습니다.")

    return [float(v) for v in vector]
