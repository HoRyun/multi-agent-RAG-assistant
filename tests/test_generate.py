import pytest

from app.rag.generate import GenerationError, generate_answer


class MockResponse:
    def __init__(self, json_data: dict, status_code: int = 200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            import httpx
            raise httpx.HTTPStatusError(
                "error", request=None, response=None  # type: ignore[arg-type]
            )

    def json(self):
        return self._json


def test_empty_prompt_raises():
    with pytest.raises(GenerationError, match="비어 있습니다"):
        generate_answer("")


def test_whitespace_prompt_raises():
    with pytest.raises(GenerationError, match="비어 있습니다"):
        generate_answer("   ")


def test_success_returns_response(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"response": "  답변 내용  "}),
    )
    result = generate_answer("프롬프트")
    assert result == "답변 내용"


def test_missing_response_field_raises(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"model": "qwen3:4b"}),
    )
    with pytest.raises(GenerationError, match="response"):
        generate_answer("프롬프트")


def test_http_error_raises(monkeypatch):
    import httpx

    def raise_http_error(url, **_):
        raise httpx.ConnectError("연결 실패")

    monkeypatch.setattr("httpx.post", raise_http_error)
    with pytest.raises(GenerationError, match="Ollama 호출 실패"):
        generate_answer("프롬프트")


def test_http_status_error_raises(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({}, status_code=500),
    )
    with pytest.raises(GenerationError):
        generate_answer("프롬프트")
