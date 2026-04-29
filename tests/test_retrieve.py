import pytest
from unittest.mock import MagicMock

from app.rag.embed import EmbeddingError
from app.rag.retrieve import RetrieveResult, retrieve

DIM = 768
FAKE_VECTOR = [0.1] * DIM


def _make_session_ctx(rows: list) -> MagicMock:
    """SessionLocal() context manager mock을 반환한다."""
    mock_session = MagicMock()
    (
        mock_session.query.return_value
        .order_by.return_value
        .limit.return_value
        .all.return_value
    ) = rows

    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=mock_session)
    ctx.__exit__ = MagicMock(return_value=False)
    return ctx


def test_invalid_top_k_zero_raises():
    with pytest.raises(ValueError, match="top_k"):
        retrieve("hello", top_k=0)


def test_invalid_top_k_negative_raises():
    with pytest.raises(ValueError, match="top_k"):
        retrieve("hello", top_k=-1)


def test_empty_query_raises(monkeypatch):
    def raise_error(text):
        raise EmbeddingError("embedding할 텍스트가 비어 있습니다.")

    monkeypatch.setattr("app.rag.retrieve.embed_text", raise_error)
    with pytest.raises(EmbeddingError):
        retrieve("")


def test_embed_failure_propagates(monkeypatch):
    def raise_error(text):
        raise EmbeddingError("Ollama 호출 실패")

    monkeypatch.setattr("app.rag.retrieve.embed_text", raise_error)
    with pytest.raises(EmbeddingError):
        retrieve("some query")


def test_returns_empty_when_no_chunks(monkeypatch):
    monkeypatch.setattr("app.rag.retrieve.embed_text", lambda _: FAKE_VECTOR)
    monkeypatch.setattr("app.rag.retrieve.SessionLocal", lambda: _make_session_ctx([]))

    results = retrieve("query", top_k=5)
    assert results == []


def test_returns_top_k_results(monkeypatch):
    chunk_a = MagicMock()
    chunk_b = MagicMock()
    mock_rows = [(chunk_a, 0.1), (chunk_b, 0.3)]

    monkeypatch.setattr("app.rag.retrieve.embed_text", lambda _: FAKE_VECTOR)
    monkeypatch.setattr("app.rag.retrieve.SessionLocal", lambda: _make_session_ctx(mock_rows))

    results = retrieve("query", top_k=2)

    assert len(results) == 2
    assert isinstance(results[0], RetrieveResult)
    assert results[0].chunk is chunk_a
    assert results[0].distance == pytest.approx(0.1)
    assert results[1].chunk is chunk_b
    assert results[1].distance == pytest.approx(0.3)


def test_distance_is_float(monkeypatch):
    chunk = MagicMock()
    mock_rows = [(chunk, 0)]  # int 0을 float으로 변환하는지 확인

    monkeypatch.setattr("app.rag.retrieve.embed_text", lambda _: FAKE_VECTOR)
    monkeypatch.setattr("app.rag.retrieve.SessionLocal", lambda: _make_session_ctx(mock_rows))

    results = retrieve("query", top_k=1)
    assert isinstance(results[0].distance, float)
