import httpx

from app.config import settings


class GenerationError(Exception):
    """Raised when LLM generation fails."""


def generate_answer(prompt: str) -> str:
    """
    Ollama /api/generate 엔드포인트를 호출해 답변을 생성한다.

    Args:
        prompt: LLM에 전달할 완성된 prompt 문자열.

    Returns:
        LLM이 생성한 답변 문자열.

    Raises:
        GenerationError: Ollama 호출 실패 또는 응답 파싱 오류 시.
    """
    if not prompt or not prompt.strip():
        raise GenerationError("prompt가 비어 있습니다.")

    try:
        resp = httpx.post(
            f"{settings.OLLAMA_HOST}/api/generate",
            json={
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                # WHY: stream=False로 설정해 응답 전체를 한 번에 받는다.
                #      스트리밍 파싱 없이 단순하게 처리할 수 있다.
                "stream": False,
            },
            timeout=120.0,
        )
        resp.raise_for_status()
        data = resp.json()
    except httpx.HTTPError as exc:
        raise GenerationError(f"Ollama 호출 실패: {exc}") from exc
    except ValueError as exc:
        raise GenerationError(f"응답 JSON 파싱 오류: {exc}") from exc

    answer = data.get("response")
    if not answer:
        raise GenerationError("Ollama 응답에 'response' 필드가 없습니다.")

    return answer.strip()
