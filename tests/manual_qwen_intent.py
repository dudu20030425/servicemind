from app.llm.qwen import analyze_intent

result = analyze_intent(
    "我的 ORD10001 到哪里了？"
)

print(result)
print(type(result))