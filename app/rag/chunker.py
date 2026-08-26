def split_text(
    text: str,
    chunk_size: int = 200,
    overlap: int = 40,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "overlap must satisfy 0 <= overlap < chunk_size"
        )

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def chunk_documents(
    documents: list[dict[str, str]],
    chunk_size: int = 200,
    overlap: int = 40,
) -> list[dict[str, str]]:
    chunks = []

    for document in documents:
        text_chunks = split_text(
            document["text"],
            chunk_size,
            overlap,
        )

        for index, text in enumerate(text_chunks):
            chunks.append(
                {
                    **document,
                    "chunk_id": (
                        f"{document['id']}_chunk_{index}"
                    ),
                    "text": text,
                }
            )

    return chunks