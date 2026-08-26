from app.rag.chunker import chunk_documents, split_text
from app.rag.knowledge_loader import load_documents


documents = load_documents()
chunks = chunk_documents(documents)

print(f"Documents: {len(documents)}")
print(f"Chunks: {len(chunks)}")

print("-" * 50)
print(chunks[0])

print("-" * 50)
demo_text = "0123456789" * 3

for index, chunk in enumerate(
    split_text(demo_text, chunk_size=12, overlap=4)
):
    print(f"Demo chunk {index}: {chunk}")