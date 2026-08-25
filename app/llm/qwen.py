import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url=os.getenv("QWEN_BASE_URL"),
)

model = os.getenv("QWEN_MODEL", "qwen-plus")


def chat(message: str) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": message}
        ],
    )

    return response.choices[0].message.content

def analyze_intent(message: str) -> dict:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an intent classifier for a customer service system. "
                    "Analyze the user's message and return JSON only. "
                    "The JSON must contain: "
                    "intent, order_id, need_tool. "
                    "intent must be one of: "
                    "order_query, refund_query, product_query, general_chat. "
                    "If there is no order ID, set order_id to null. "
                    "need_tool must be true or false."
                ),
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)