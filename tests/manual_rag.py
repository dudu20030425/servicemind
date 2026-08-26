import json

from app.rag.service import answer_with_rag


query = "我的蓝牙耳机只有一边有声音，应该怎么办？"
result = answer_with_rag(query)

print(f"Query: {query}")
print("-" * 60)
print(
    json.dumps(
        result,
        ensure_ascii=False,
        indent=2,
    )
)