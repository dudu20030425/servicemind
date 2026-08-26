import json
from pathlib import Path


KNOWLEDGE_DIR = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "knowledge_base"
)


def load_documents(
    directory: Path = KNOWLEDGE_DIR,
) -> list[dict[str, str]]:
    if not directory.exists():
        raise FileNotFoundError(
            f"Knowledge directory not found: {directory}"
        )

    documents = []
    required_fields = {"id", "question", "answer", "category"}

    for path in sorted(directory.glob("*.json")):
        items = json.loads(
            path.read_text(encoding="utf-8-sig")
        )

        for item in items:
            missing = required_fields - item.keys()

            if missing:
                raise ValueError(
                    f"{path.name} missing fields: {missing}"
                )

            documents.append(
                {
                    "id": item["id"],
                    "text": (
                        f"问题：{item['question']}\n"
                        f"答案：{item['answer']}"
                    ),
                    "category": item["category"],
                    "source": path.name,
                }
            )

    return documents