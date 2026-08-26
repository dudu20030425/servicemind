from app.rag.retriever import retrieve


test_cases = [
    {
        "query": "蓝牙耳机右边没有声音，应该怎么处理？",
        "expected_id": "PRODUCT003",
    },
    {
        "query": "订单还没有发货，我现在可以取消吗？",
        "expected_id": "FAQ007",
    },
    {
        "query": "充电器特别烫而且出现异味，还能继续用吗？",
        "expected_id": "PRODUCT005",
    },
    {
        "query": "我想知道自己的包裹运到哪里了。",
        "expected_id": "FAQ002",
    },
    {
        "query": "商品签收九天后发现质量问题，还能申请售后吗？",
        "expected_id": "POLICY006",
    },
    {
        "query": "退款审核已经通过，钱大概几天能退回来？",
        "expected_id": "FAQ004",
    },
    {
        "query": "我买完东西以后要在哪里开电子发票？",
        "expected_id": "FAQ008",
    },
    {
        "query": "提交退货申请时需要上传哪些资料？",
        "expected_id": "POLICY003",
    },
    {
        "query": "商品有质量问题需要退货，寄回去的运费谁出？",
        "expected_id": "POLICY004",
    },
    {
        "query": "新买的智能手环怎样和手机进行配对？",
        "expected_id": "PRODUCT001",
    },
]

hit_at_1 = 0
hit_at_3 = 0

for case in test_cases:
    results = retrieve(case["query"], top_k=3)
    result_ids = [result["id"] for result in results]

    top_1_hit = case["expected_id"] == result_ids[0]
    top_3_hit = case["expected_id"] in result_ids

    hit_at_1 += int(top_1_hit)
    hit_at_3 += int(top_3_hit)

    print("-" * 60)
    print(f"Query: {case['query']}")
    print(f"Expected: {case['expected_id']}")
    print(f"Retrieved: {result_ids}")
    print(f"Hit@1: {top_1_hit}")
    print(f"Hit@3: {top_3_hit}")

total = len(test_cases)

print("=" * 60)
print(f"Hit@1: {hit_at_1}/{total}")
print(f"Hit@3: {hit_at_3}/{total}")
print(f"Hit@1 Accuracy: {hit_at_1 / total:.2%}")
print(f"Hit@3 Accuracy: {hit_at_3 / total:.2%}")