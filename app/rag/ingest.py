from dataclasses import dataclass
from pathlib import Path

from app.db.models import RagChunk
from app.db.session import SessionLocal
from app.rag.chunk import chunk_text
from app.rag.embed import embed_text

# WHY: 절대경로 대신 프로젝트 루트 기준 상대경로를 저장해 환경에 독립적으로 만든다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class IngestResult:
    """ingest_markdown_dir() 실행 결과 요약."""

    inserted_files: int
    skipped_empty_files: int
    failed_files: int
    inserted_chunks: int


def ingest_markdown_dir(directory: Path) -> IngestResult:
    """
    디렉토리 내 모든 .md 파일을 읽어 청킹, 임베딩 후 DB에 저장한다.

    Args:
        directory: .md 파일이 있는 디렉토리 경로.

    Returns:
        처리 결과를 담은 IngestResult.
    """
    inserted_files = 0
    skipped_empty_files = 0
    failed_files = 0
    inserted_chunks = 0

    md_files = sorted(directory.glob("*.md"))

    for file_path in md_files:
        source_path = str(file_path.resolve().relative_to(PROJECT_ROOT))

        text = file_path.read_text(encoding="utf-8")
        chunks = chunk_text(text)

        if not chunks:
            with SessionLocal() as session:
                session.query(RagChunk).filter(
                    RagChunk.source_path == source_path
                ).delete()
                session.commit()
            print(f"[SKIP] {source_path}")
            skipped_empty_files += 1
            continue

        # WHY: embedding은 느리고 실패 가능한 외부 호출이므로 DB transaction 전에 전부 완료한다.
        embeddings: list[list[float]] = []
        embed_failed = False

        for idx, chunk in enumerate(chunks):
            try:
                embeddings.append(embed_text(chunk))
            except Exception as e:
                print(f"[FAIL] {source_path} chunk {idx}: {e}")
                failed_files += 1
                embed_failed = True
                break

        if embed_failed:
            continue

        try:
            with SessionLocal() as session:
                session.query(RagChunk).filter(
                    RagChunk.source_path == source_path
                ).delete()
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                    session.add(
                        RagChunk(
                            source_path=source_path,
                            chunk_index=idx,
                            content=chunk,
                            embedding=embedding,
                        )
                    )
                session.commit()
            print(f"[OK] {source_path}: {len(chunks)} chunks")
            inserted_files += 1
            inserted_chunks += len(chunks)
        except Exception as e:
            print(f"[ROLLBACK] {source_path}: {e}")

    print(
        f"\n[SUMMARY] inserted {inserted_files} files, {inserted_chunks} chunks"
        f" | skipped {skipped_empty_files} | failed {failed_files}"
    )
    return IngestResult(
        inserted_files=inserted_files,
        skipped_empty_files=skipped_empty_files,
        failed_files=failed_files,
        inserted_chunks=inserted_chunks,
    )


if __name__ == "__main__":
    ingest_markdown_dir(Path("data/sample"))
