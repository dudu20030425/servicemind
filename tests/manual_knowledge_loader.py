from app.rag.knowledge_loader import load_documents


documents = load_documents()

print(f"Loaded documents: {len(documents)}")

for document in documents[:3]:
    print("-" * 50)
    print(f"ID: {document['id']}")
    print(f"Category: {document['category']}")
    print(f"Source: {document['source']}")
    print(document["text"])