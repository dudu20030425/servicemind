# ServiceMind

ServiceMind is an enterprise AI customer support backend built with FastAPI and Qwen.

The project currently supports LLM chat, intent recognition, semantic knowledge retrieval, and grounded RAG responses for customer service scenarios such as refunds, logistics, product troubleshooting, and after-sales support.

## Current Capabilities

- FastAPI backend service
- Qwen chat API
- Customer-service intent recognition
- JSON knowledge-base loading
- Text chunking with overlap
- Qwen text embedding
- Persistent local vector index
- Cosine-similarity Top-K retrieval
- Relevance-threshold filtering
- Knowledge-grounded answer generation
- Evidence text, source, and score output
- Automated API tests
- Manual retrieval evaluation

## RAG Pipeline

```text
Knowledge JSON
    -> Document Loader
    -> Text Chunker
    -> Embedding Model
    -> Vector Index

User Query
    -> Query Embedding
    -> Cosine Similarity Search
    -> Relevance Filtering
    -> Context Construction
    -> Qwen Answer Generation
    -> Answer with Evidence Sources
```

The RAG service only generates an answer when sufficiently relevant knowledge is retrieved. Otherwise, it returns a controlled response without calling the chat model.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Service health check |
| POST | `/chat` | Qwen-based conversation |
| POST | `/intent` | Customer-service intent recognition |
| POST | `/retrieve` | Semantic Top-K knowledge retrieval |
| POST | `/rag` | Grounded answer generation with evidence sources |

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
└── rag/            # Loading, embedding, retrieval, and RAG service

data/
├── business_db/    # Mock business data
└── knowledge_base/ # FAQ, policy, and product knowledge

tests/              # Automated tests, manual checks, and retrieval evaluation
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
9 passed
```

Run the semantic retrieval evaluation:

```bash
python -m tests.manual_retrieval_eval
```

Current retrieval result:

```text
Hit@1: 10/10
Hit@3: 10/10
Hit@1 Accuracy: 100.00%
Hit@3 Accuracy: 100.00%
```

## Roadmap

- Unified chat routing across LLM, RAG, and business tools
- Order lookup and refund eligibility tools
- Agent tool calling
- Conversation memory
- MCP integration
- Automated RAG response evaluation
- API retry and observability