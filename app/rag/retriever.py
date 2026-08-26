import math

from app.rag.embedding import embed_text
from app.rag.vector_store import load_index


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    if len(vector_a) != len(vector_b):
        raise ValueError("Vector dimensions do not match")

    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return dot_product / (norm_a * norm_b)


def retrieve(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    if top_k <= 0:
        raise ValueError("top_k must be positive")

    query_vector = embed_text(query)
    index = load_index()
    results = []

    for item in index:
        score = cosine_similarity(
            query_vector,
            item["embedding"],
        )

        result = {
            key: value
            for key, value in item.items()
            if key != "embedding"
        }
        result["score"] = round(score, 4)
        results.append(result)

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True,
    )[:top_k]