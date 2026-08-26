from app.rag.embedding import embed_texts


texts = [
    "商品应该怎样申请退货？",
    "蓝牙耳机只有一边有声音怎么办？",
]

vectors = embed_texts(texts)

print(f"Vector count: {len(vectors)}")
print(f"Vector dimension: {len(vectors[0])}")
print(f"First five values: {vectors[0][:5]}")