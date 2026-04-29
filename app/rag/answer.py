from app.rag.generate import generate_answer
from app.rag.prompt import build_rag_prompt
from app.rag.retrieve import retrieve


def answer_question(query: str, top_k: int = 4) -> str:
    """
    질문을 받아 검색 → prompt 조합 → LLM 생성 순서로 답변을 반환한다.

    Args:
        query: 사용자 질문.
        top_k: 검색할 최대 청크 수.

    Returns:
        LLM이 생성한 답변 문자열.
    """
    results = retrieve(query, top_k=top_k)
    prompt = build_rag_prompt(query, results)
    return generate_answer(prompt)
