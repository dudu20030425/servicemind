# ServiceMind

ServiceMind is an enterprise AI customer support backend built with FastAPI and Qwen.

The project currently supports LLM chat, intent recognition, and semantic knowledge retrieval for customer service scenarios such as refunds, logistics, product troubleshooting, and after-sales support.

## Current Capabilities

- FastAPI backend service
- Qwen chat API
- Customer-service intent recognition
- JSON knowledge-base loading
- Text chunking with overlap
- Qwen text embedding
- Persistent local vector index
- Cosine-similarity Top-K retrieval
- Retrieval source and score output
- Automated API tests

## RAG Retrieval Pipeline

```text
Knowledge JSON
    -> Document Loader
    -> Text Chunker
    -> Embedding Model
    -> Vector Index
    -> Cosine Similarity Search
    -> Top-K Results
```

The current milestone implements the retrieval layer. Grounded answer generation using the retrieved context will be added next.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/chat` | Qwen-based conversation |
| POST | `/intent` | Customer-service intent recognition |
| POST | `/retrieve` | Semantic Top-K knowledge retrieval |

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Project Structure

```text
app/
├── api/            # FastAPI routes
├── llm/            # Qwen and provider abstraction
├── models/         # Request and response schemas
└── rag/            # Loader, chunker, embedding, and retrieval

data/
├── business_db/    # Mock business data
└── knowledge_base/ # FAQ, policy, and product knowledge

tests/              # Automated and manual tests
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure the Qwen API credentials.

Build the local vector index:

```bash
python -m tests.manual_build_index
```

Start the API service:

```bash
python -m uvicorn app.main:app --reload
```

## Tests

Run the automated test suite:

```bash
python -m pytest -q
```

Current result:

```text
7 passed
```

## Roadmap

- RAG-based grounded answer generation
- Source citation in customer-service answers
- Order lookup and refund eligibility tools
- Agent tool calling
- Conversation memory
- MCP integration
- Retrieval and response evaluation