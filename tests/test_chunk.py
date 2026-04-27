import pytest

from app.rag.chunk import chunk_text


def test_empty_string_returns_empty_list():
    assert chunk_text("") == []


def test_whitespace_returns_empty_list():
    assert chunk_text("   \n\t   ") == []


def test_short_text_above_min_returns_one_chunk():
    result = chunk_text("hello world", chunk_size=100, overlap=10, min_chunk_size=5)
    assert result == ["hello world"]


def test_raises_when_overlap_equals_chunk_size():
    with pytest.raises(ValueError):
        chunk_text("hello world", chunk_size=100, overlap=100)


def test_raises_when_chunk_size_is_zero():
    with pytest.raises(ValueError):
        chunk_text("hello world", chunk_size=0, overlap=0)


def test_raises_when_overlap_is_negative():
    with pytest.raises(ValueError):
        chunk_text("hello world", chunk_size=100, overlap=-1)


def test_raises_when_min_chunk_size_is_zero():
    with pytest.raises(ValueError):
        chunk_text("hello world", chunk_size=100, overlap=10, min_chunk_size=0)


def test_overlap_is_applied_correctly():
    # chunk_size=5, overlap=2, step=3
    # start=0 → "abcde", start=3 → "defgh", start=6 → "ghij", start=9 → "j"
    # "j"는 길이 1 == min_chunk_size=1 이므로 포함된다.
    result = chunk_text("abcdefghij", chunk_size=5, overlap=2, min_chunk_size=1)
    assert result == ["abcde", "defgh", "ghij", "j"]
