import pytest

from app.rag.embed import EmbeddingError, embed_text

DIM = 768
FAKE_VECTOR = [0.1] * DIM


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


def test_empty_string_raises_embedding_error():
    with pytest.raises(EmbeddingError):
        embed_text("")


def test_whitespace_raises_embedding_error():
    with pytest.raises(EmbeddingError):
        embed_text("   ")


def test_api_embed_success(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"embeddings": [FAKE_VECTOR]}),
    )
    result = embed_text("hello")
    assert result == [float(v) for v in FAKE_VECTOR]
    assert len(result) == DIM


def test_fallback_to_api_embeddings(monkeypatch):
    call_count = {"n": 0}

    def fake_post(url, **_):
        call_count["n"] += 1
        if url.endswith("/api/embed"):
            return MockResponse({})  # embeddings 키 없음 → fallback
        return MockResponse({"embedding": FAKE_VECTOR})

    monkeypatch.setattr("httpx.post", fake_post)
    result = embed_text("hello")
    assert result == [float(v) for v in FAKE_VECTOR]
    assert call_count["n"] == 2


def test_dimension_mismatch_raises(monkeypatch):
    wrong_vector = [0.1] * 10  # DIM=768 이 아님
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"embeddings": [wrong_vector]}),
    )
    with pytest.raises(EmbeddingError, match="차원 불일치"):
        embed_text("hello")


def test_response_not_list_raises(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"embeddings": ["not_a_list"]}),
    )
    with pytest.raises(EmbeddingError, match="list가 아닙니다"):
        embed_text("hello")


def test_non_numeric_in_vector_raises(monkeypatch):
    bad_vector = ["a"] * DIM
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({"embeddings": [bad_vector]}),
    )
    with pytest.raises(EmbeddingError, match="숫자가 아닌 값"):
        embed_text("hello")


def test_both_endpoints_fail_raises(monkeypatch):
    monkeypatch.setattr(
        "httpx.post",
        lambda url, **_: MockResponse({}),  # 두 endpoint 모두 key 없음
    )
    with pytest.raises(EmbeddingError):
        embed_text("hello")


def test_retry_succeeds_on_second_attempt(monkeypatch):
    attempt = {"n": 0}

    def fake_post(url, **_):
        if not url.endswith("/api/embed"):
            return MockResponse({})
        attempt["n"] += 1
        if attempt["n"] == 1:
            return MockResponse({})  # 첫 시도 실패
        return MockResponse({"embeddings": [FAKE_VECTOR]})

    monkeypatch.setattr("httpx.post", fake_post)
    monkeypatch.setattr("time.sleep", lambda _: None)  # sleep 스킵

    result = embed_text("hello")
    assert result == [float(v) for v in FAKE_VECTOR]
    assert attempt["n"] == 2
