def chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 100,
    min_chunk_size: int = 50,
) -> list[str]:
    """
    텍스트를 고정 크기 문자 단위 청크로 분리한다.

    Args:
        text: 분리할 원본 텍스트.
        chunk_size: 청크 하나의 최대 문자 수.
        overlap: 인접 청크 간 겹치는 문자 수.
        min_chunk_size: 이 길이 미만인 청크는 결과에서 제외한다.

    Returns:
        strip된 청크 문자열 리스트.

    Raises:
        ValueError: 파라미터가 유효하지 않은 경우.
    """
    if chunk_size <= 0:
        raise ValueError(f"chunk_size({chunk_size})는 0보다 커야 한다.")
    if overlap < 0:
        raise ValueError(f"overlap({overlap})은 0 이상이어야 한다.")
    if overlap >= chunk_size:
        raise ValueError(f"overlap({overlap})은 chunk_size({chunk_size})보다 작아야 한다.")
    if min_chunk_size <= 0:
        raise ValueError(f"min_chunk_size({min_chunk_size})는 0보다 커야 한다.")

    if not text or not text.strip():
        return []

    # WHY (KR): v1에서는 튜닝 복잡도를 줄이기 위해 고정 문자 수 기반 chunking을 사용한다.
    step = chunk_size - overlap
    chunks: list[str] = []
    start = 0

    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        # WHY (KR): 너무 짧은 tail chunk는 검색 품질을 떨어뜨릴 수 있어 v1에서는 제외한다.
        if len(chunk) >= min_chunk_size:
            chunks.append(chunk)
        start += step

    return chunks
