from app.llm.provider import generate
from app.rag.retriever import retrieve


def answer_with_rag(
    query: str,
    top_k: int = 3,
    min_score: float = 0.6,
) -> dict:
    if not query.strip():
        raise ValueError("Query cannot be empty")

    results = retrieve(query, top_k=top_k)
    relevant_results = [
        item for item in results
        if item["score"] >= min_score
    ]

    if not relevant_results:
        return {
            "answer": "当前知识库中没有找到足够相关的信息。",
            "provider": None,
            "model": None,
            "sources": [],
        }

    context = "\n\n".join(
        (
            f"[Knowledge {index}]\n"
            f"ID: {item['id']}\n"
            f"Source: {item['source']}\n"
            f"Content:\n{item['text']}"
        )
        for index, item in enumerate(
            relevant_results,
            start=1,
        )
    )

    prompt = (
        "你是企业客服助手。请严格根据下面的知识库内容回答用户问题。\n"
        "不得使用知识库之外的信息，不得编造答案。\n"
        "如果知识库内容不足，请明确说明无法确认。\n"
        "请使用简洁、自然的中文回答。\n\n"
        f"知识库内容：\n{context}\n\n"
        f"用户问题：{query}"
    )

    response = generate(prompt)
    response["sources"] = [
        {
            "id": item["id"],
            "text": item["text"],
            "source": item["source"],
            "score": item["score"],
        }
        for item in relevant_results
    ]

    return response