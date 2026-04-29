"""
RAG 답변 흐름 end-to-end CLI 데모.

사용법:
    uv run python examples/rag_answer_demo.py "RAG는 왜 필요한가?"
"""

import sys

from app.rag.generate import generate_answer
from app.rag.prompt import build_rag_prompt
from app.rag.retrieve import retrieve


def main() -> None:
    if len(sys.argv) < 2:
        print("사용법: uv run python examples/rag_answer_demo.py <질문>")
        sys.exit(1)

    query = sys.argv[1]
    top_k = 4

    print(f"Question:\n{query}\n")

    results = retrieve(query, top_k=top_k)
    prompt = build_rag_prompt(query, results)
    answer = generate_answer(prompt)

    print(f"Answer:\n{answer}\n")

    print("Sources:")
    for r in results:
        label = f"{r.chunk.source_path}#{r.chunk.chunk_index}"
        print(f"  - {label}  distance={r.distance:.4f}")


if __name__ == "__main__":
    main()
