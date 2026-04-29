from unittest.mock import MagicMock

from app.rag.prompt import build_rag_prompt
from app.rag.retrieve import RetrieveResult


def _make_result(source_path: str, chunk_index: int, content: str, distance: float = 0.1) -> RetrieveResult:
    chunk = MagicMock()
    chunk.source_path = source_path
    chunk.chunk_index = chunk_index
    chunk.content = content
    return RetrieveResult(chunk=chunk, distance=distance)


def test_empty_results_contains_no_context_notice():
    prompt = build_rag_prompt("질문입니다", results=[])
    assert "context 없음" in prompt
    assert "질문입니다" in prompt


def test_query_always_included():
    prompt = build_rag_prompt("RAG란 무엇인가?", results=[])
    assert "RAG란 무엇인가?" in prompt


def test_source_label_format():
    result = _make_result("data/sample/rag.md", 2, "RAG 설명 내용")
    prompt = build_rag_prompt("질문", results=[result])
    assert "data/sample/rag.md#2" in prompt


def test_chunk_content_included():
    result = _make_result("docs/a.md", 0, "청크 본문 텍스트")
    prompt = build_rag_prompt("질문", results=[result])
    assert "청크 본문 텍스트" in prompt


def test_system_instruction_included():
    prompt = build_rag_prompt("질문", results=[])
    assert "모르겠습니다" in prompt or "context에 없는" in prompt


def test_multiple_results_all_included():
    results = [
        _make_result("a.md", 0, "첫 번째 청크"),
        _make_result("b.md", 1, "두 번째 청크"),
    ]
    prompt = build_rag_prompt("질문", results=results)
    assert "첫 번째 청크" in prompt
    assert "두 번째 청크" in prompt
    assert "a.md#0" in prompt
    assert "b.md#1" in prompt
