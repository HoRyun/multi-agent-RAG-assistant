from dataclasses import dataclass

from app.db.models import RagChunk
from app.db.session import SessionLocal
from app.rag.embed import embed_text


@dataclass
class RetrieveResult:
    """retrieve() 함수의 결과 단위."""

    chunk: RagChunk
    distance: float


def retrieve(query: str, top_k: int = 5) -> list[RetrieveResult]:
    """
    쿼리 텍스트와 cosine distance가 가장 가까운 청크 top_k개를 반환한다.

    Args:
        query: 검색할 텍스트.
        top_k: 반환할 최대 청크 수.

    Returns:
        distance 오름차순으로 정렬된 RetrieveResult 리스트.

    Raises:
        ValueError: top_k가 0 이하인 경우.
        EmbeddingError: 쿼리 임베딩 생성에 실패한 경우.
    """
    if top_k <= 0:
        raise ValueError(f"top_k({top_k})는 0보다 커야 한다.")

    vector = embed_text(query)

    with SessionLocal() as session:
        rows = (
            session.query(
                RagChunk,
                RagChunk.embedding.cosine_distance(vector).label("distance"),
            )
            .order_by(RagChunk.embedding.cosine_distance(vector))
            .limit(top_k)
            .all()
        )

    return [RetrieveResult(chunk=row[0], distance=float(row[1])) for row in rows]
