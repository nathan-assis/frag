def fixed_size_with_overlap(
    text: str, chunk_size: int = 200, overlap: int = 20
) -> list[str]:
    if not text:
        return []

    chunks = [text[: chunk_size + overlap]]

    for i in range(chunk_size, len(text), chunk_size):
        chunks.append(text[i - overlap : i + chunk_size + overlap])

    return chunks
