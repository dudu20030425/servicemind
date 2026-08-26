import json
from pathlib import Path

from app.rag.embedding import embed_texts


INDEX_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "vector_store"
    / "index.json"
)


def build_index(
    documents: list[dict[str, str]],
) -> list[dict]:
    vectors = embed_texts(
        [document["text"] for document in documents]
    )

    if len(vectors) != len(documents):
        raise RuntimeError(
            "Embedding count does not match document count"
        )

    return [
        {
            **document,
            "embedding": vector,
        }
        for document, vector in zip(documents, vectors)
    ]


def save_index(
    index: list[dict],
    path: Path = INDEX_PATH,
) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(index, ensure_ascii=False),
        encoding="utf-8",
    )

    return path


def load_index(
    path: Path = INDEX_PATH,
) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(
            f"Vector index not found: {path}"
        )

    return json.loads(
        path.read_text(encoding="utf-8")
    )