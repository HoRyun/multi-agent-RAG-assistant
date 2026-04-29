from app.rag.retrieve import RetrieveResult

_SYSTEM_INSTRUCTION = (
    "아래 context를 바탕으로 질문에 답하라. "
    "context에 없는 내용은 '모르겠습니다'라고 답하라. "
    "추측하거나 context 외 지식을 사용하지 마라."
)


def build_rag_prompt(query: str, results: list[RetrieveResult]) -> str:
    """
    검색 결과와 사용자 질문을 LLM에 전달할 prompt 문자열로 조합한다.

    Args:
        query: 사용자 질문.
        results: retrieve() 반환값. 비어 있으면 context 없음 안내 포함.

    Returns:
        완성된 prompt 문자열.
    """
    lines: list[str] = [_SYSTEM_INSTRUCTION, ""]

    if not results:
        lines.append("[context 없음: 관련 문서를 찾지 못했습니다]")
    else:
        lines.append("=== Context ===")
        for r in results:
            source_label = f"{r.chunk.source_path}#{r.chunk.chunk_index}"
            lines.append(f"[출처: {source_label}]")
            lines.append(r.chunk.content)
            lines.append("")

    lines.append("=== 질문 ===")
    lines.append(query)

    return "\n".join(lines)
