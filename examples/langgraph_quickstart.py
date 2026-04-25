"""
LangGraph Quickstart — 학습용 예제

목표: State, Node, Edge, Graph compile 흐름을 이해한다.
     외부 LLM 호출 없이 순수 Python 함수만 사용한다.

실행 방법:
    uv run python examples/langgraph_quickstart.py
"""

from typing import TypedDict

from langgraph.graph import END, StateGraph


# ─────────────────────────────────────────────
# 1. State 정의
#
# WHY: TypedDict로 정의하면 각 Node가 어떤 필드를 읽고 쓰는지 명확해진다.
#      AWS Step Functions의 input/output JSON 스키마와 같은 역할.
#      그래프 전체를 흐르는 공유 데이터 컨테이너다.
# ─────────────────────────────────────────────
class RAGState(TypedDict):
    query: str    # 사용자 질문 — 입력값, 변경되지 않음
    context: str  # retrieve Node가 채운다
    answer: str   # generate Node가 채운다


# ─────────────────────────────────────────────
# 2. Node 정의
#
# Node = State를 받아서 처리 후, 변경할 필드만 dict로 반환하는 함수.
# 반환하지 않은 필드는 이전 값이 유지된다.
# Step Functions의 Task State(Lambda 함수 하나)와 같은 단위.
# ─────────────────────────────────────────────
def retrieve(state: RAGState) -> dict:
    """
    문서 검색 Node.
    실제 구현에서는 pgvector에 쿼리하지만, 여기서는 가짜 결과를 반환한다.
    """
    query = state["query"]
    print(f"\n[Node: retrieve] 실행")
    print(f"  입력 state.query = {query!r}")

    # WHY: v1 학습 단계이므로 실제 DB 호출 없이 하드코딩.
    fake_docs = "LangGraph는 LLM 앱을 상태 기반 그래프로 표현하는 프레임워크입니다."
    print(f"  출력 → context = {fake_docs!r}")
    return {"context": fake_docs}


def generate(state: RAGState) -> dict:
    """
    답변 생성 Node.
    실제 구현에서는 Ollama(qwen3:4b)를 호출하지만, 여기서는 가짜 답변을 반환한다.
    """
    context = state["context"]
    print(f"\n[Node: generate] 실행")
    print(f"  입력 state.context = {context!r}")

    # WHY: Ollama 연동은 다음 STEP에서 추가. 지금은 흐름 이해에 집중.
    fake_answer = "LangGraph는 LLM 앱을 그래프로 표현하는 프레임워크입니다."
    print(f"  출력 → answer = {fake_answer!r}")
    return {"answer": fake_answer}


# ─────────────────────────────────────────────
# 3. Graph 조립 및 compile
#
# Edge = Node 간 전이 규칙. Step Functions의 Next/End 설정과 같다.
# compile() = 설계도(builder)를 실행 가능한 Runnable로 변환한다.
#             이 시점에 Edge 연결 유효성 검사가 수행된다.
# ─────────────────────────────────────────────
def build_graph():
    """그래프를 조립하고 실행 가능한 Runnable로 변환해 반환한다."""
    builder = StateGraph(RAGState)

    # Node 등록
    builder.add_node("retrieve", retrieve)
    builder.add_node("generate", generate)

    # Edge 연결: START → retrieve → generate → END
    builder.set_entry_point("retrieve")
    builder.add_edge("retrieve", "generate")
    builder.add_edge("generate", END)

    print("[Graph] compile — 설계도를 실행 가능한 Runnable로 변환")
    return builder.compile()


# ─────────────────────────────────────────────
# 4. 실행
# ─────────────────────────────────────────────
if __name__ == "__main__":
    graph = build_graph()

    initial_state: RAGState = {
        "query": "LangGraph란 무엇인가?",
        "context": "",
        "answer": "",
    }

    print(f"\n[invoke] 초기 State = {initial_state}")
    result = graph.invoke(initial_state)

    print("\n─────────────────────────────")
    print("최종 State:")
    print(f"  query   = {result['query']!r}")
    print(f"  context = {result['context']!r}")
    print(f"  answer  = {result['answer']!r}")
