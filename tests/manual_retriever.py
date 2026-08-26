from app.rag.retriever import retrieve


query = "我的蓝牙耳机只有一边有声音，应该怎么办？"
results = retrieve(query, top_k=3)

print(f"Query: {query}")

for rank, result in enumerate(results, start=1):
    print("-" * 60)
    print(f"Rank: {rank}")
    print(f"Score: {result['score']}")
    print(f"ID: {result['id']}")
    print(f"Source: {result['source']}")
    print(result["text"])