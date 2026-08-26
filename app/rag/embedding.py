import os

from app.llm.qwen import client


EMBEDDING_MODEL = os.getenv(
    "QWEN_EMBEDDING_MODEL",
    "text-embedding-v4",
)
EMBEDDING_DIMENSION = int(
    os.getenv("QWEN_EMBEDDING_DIMENSION", "1024")
)
BATCH_SIZE = 10


def embed_texts(texts: list[str]) -> list[list[float]]:
    vectors = []

    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start:start + BATCH_SIZE]

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=batch,
            dimensions=EMBEDDING_DIMENSION,
            encoding_format="float",
        )

        data = sorted(
            response.data,
            key=lambda item: item.index,
        )
        vectors.extend(item.embedding for item in data)

    return vectors


def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]