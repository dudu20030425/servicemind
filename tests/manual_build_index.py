from app.rag.chunker import chunk_documents
from app.rag.knowledge_loader import load_documents
from app.rag.vector_store import build_index, save_index


documents = load_documents()
chunks = chunk_documents(documents)

index = build_index(chunks)
index_path = save_index(index)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")
print(f"Indexed vectors: {len(index)}")
print(f"Vector dimension: {len(index[0]['embedding'])}")
print(f"Saved to: {index_path}")