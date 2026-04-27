# LangGraph 개요

LangGraph는 LLM 기반 애플리케이션에서 상태 기반 워크플로우를 그래프 구조로 정의하는 라이브러리다. LangChain 위에 구축되었으며, 복잡한 멀티 에이전트 흐름을 명시적으로 표현할 수 있다.

## 핵심 개념

LangGraph는 세 가지 핵심 요소로 구성된다.

**State**: 그래프 전체에서 공유되는 데이터 구조다. TypedDict나 dataclass로 정의하며, 각 노드가 State를 읽고 업데이트한다.

**Node**: 실제 작업을 수행하는 함수다. LLM 호출, 도구 실행, 데이터 변환 등 어떤 로직도 노드로 만들 수 있다.

**Edge**: 노드 간 실행 순서를 정의한다. 조건부 엣지를 사용하면 State 값에 따라 다른 노드로 분기할 수 있다.

## 기본 사용 예시

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class AgentState(TypedDict):
    messages: list[str]
    next_step: str

def call_llm(state: AgentState) -> AgentState:
    # LLM 호출 로직
    return {"messages": state["messages"] + ["LLM 응답"], "next_step": "end"}

builder = StateGraph(AgentState)
builder.add_node("llm", call_llm)
builder.set_entry_point("llm")
builder.add_edge("llm", END)

graph = builder.compile()
```

## 조건부 분기

LangGraph의 강점 중 하나는 State를 기반으로 한 동적 분기다.

```python
def route(state: AgentState) -> str:
    if state["next_step"] == "tool":
        return "tool_node"
    return END

builder.add_conditional_edges("llm", route)
```

이렇게 하면 LLM 응답에 따라 도구 호출 여부를 동적으로 결정할 수 있다.

## 멀티 에이전트 패턴

LangGraph는 여러 에이전트가 협력하는 패턴을 구현하기에 적합하다. 각 에이전트를 별도의 노드로 정의하고, 슈퍼바이저 노드가 어느 에이전트를 호출할지 결정하는 구조가 일반적이다.

이 패턴은 RAG 파이프라인에서도 유용하다. 검색 에이전트, 리랭킹 에이전트, 생성 에이전트를 각각의 노드로 분리해 관리할 수 있다.
