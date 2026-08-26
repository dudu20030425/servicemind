# ServiceMind

ServiceMind is an enterprise AI customer support backend built with FastAPI and Qwen.

The project supports LLM chat, intent recognition, semantic knowledge retrieval, grounded RAG responses, Agent-based request routing, order lookup, and MCP-compatible tool access.

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
- Agent routing across chat, RAG, and business tools
- JSON-backed order lookup tool
- MCP server exposing `order_lookup`
- Automated API, Agent, RAG, tool, and MCP tests
- Manual semantic retrieval evaluation

## Agent Workflow

```text
User Request
    -> Customer Service Agent
    -> Intent Routing
        -> Order Query: order_lookup
        -> Knowledge Question: RAG
        -> General Conversation: Qwen Chat
    -> Structured Agent Response
```

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
| POST | `/agent` | Route requests across chat, RAG, and business tools |

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## MCP Server

The MCP server exposes the existing business logic as a standardized tool:

| Tool | Input | Description |
|---|---|---|
| `order_lookup` | `order_id: str` | Look up customer order details by order ID |

Run the MCP server:

```bash
mcp run mcp_server/server.py
```

## Project Structure

```text
app/
  agents/          # Customer-service Agent and routing
  api/             # FastAPI routes
  llm/             # Qwen and provider abstraction
  models/          # Request and response schemas
  rag/             # Loading, embedding, retrieval, and RAG service
  tools/           # Business tools

data/
  business_db/     # Mock order and business data
  knowledge_base/  # FAQ, policy, and product knowledge

mcp_server/        # MCP server and tool exposure
tests/             # Automated tests and manual evaluations
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

Run the complete automated test suite:

```bash
python -m pytest -q
```

Current result:

```text
21 passed
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

- Refund eligibility tool
- Product search and ticket creation tools
- Conversation memory and user context
- MCP-based Agent tool transport
- Automated RAG response evaluation
- API retry, logging, and observability