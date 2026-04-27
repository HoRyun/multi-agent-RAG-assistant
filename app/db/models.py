from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.config import settings
from app.db.base import Base


class RagChunk(Base):
    """pgvector에 저장되는 청크 단위 텍스트와 임베딩."""

    __tablename__ = "rag_chunks"
    __table_args__ = (
        UniqueConstraint(
            "source_path", "chunk_index", name="uq_rag_chunks_source_chunk"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_path: Mapped[str] = mapped_column(String(512), nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # WHY: Mapped[] 타입 힌트를 쓰지 않는다. Vector는 Python 표준 타입이 아니라
    #      SQLAlchemy의 Mapped 시스템이 처리할 수 없다.
    embedding = mapped_column(Vector(settings.EMBEDDING_DIM), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
