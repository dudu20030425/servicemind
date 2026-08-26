from fastapi import APIRouter, HTTPException
from openai import OpenAIError
from app.llm.provider import (
    LLMServiceError,
    UnsupportedProviderError,
    analyze,
    generate,
)
from app.models.schemas import (
    AgentResponse,
    ChatRequest,
    ChatResponse,
    IntentResponse,
    RagRequest,
    RagResponse,
    RetrieveRequest,
    RetrieveResponse,
)
from app.rag.retriever import retrieve
from app.rag.service import answer_with_rag
from app.agents.customer_service_agent import run_agent

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        result = generate(request.message)

        return ChatResponse(
            answer=result["answer"],
            provider=result["provider"],
            model=result["model"],
        )

    except LLMServiceError:
        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        )

    except UnsupportedProviderError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
        
@router.post("/intent", response_model=IntentResponse)
def intent(request: ChatRequest):
    try:
        result = analyze(request.message)
        return IntentResponse(**result)

    except LLMServiceError:
        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        )

    except UnsupportedProviderError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

@router.post(
    "/retrieve",
    response_model=RetrieveResponse,
)
def retrieve_knowledge(
    request: RetrieveRequest,
):
    try:
        results = retrieve(
            request.query,
            request.top_k,
        )

        return RetrieveResponse(
            query=request.query,
            results=results,
        )

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Embedding service unavailable",
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Vector index not found",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

@router.post(
    "/rag",
    response_model=RagResponse,
)
def rag_answer(request: RagRequest):
    try:
        result = answer_with_rag(
            request.query,
            top_k=request.top_k,
        )

        return RagResponse(
            query=request.query,
            answer=result["answer"],
            provider=result["provider"],
            model=result["model"],
            sources=result["sources"],
        )

    except LLMServiceError:
        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        )

    except UnsupportedProviderError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Embedding service unavailable",
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Vector index not found",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

@router.post(
    "/agent",
    response_model=AgentResponse,
)
def customer_service_agent(request: ChatRequest):
    try:
        result = run_agent(request.message)
        return AgentResponse(**result)

    except LLMServiceError:
        raise HTTPException(
            status_code=502,
            detail="LLM service unavailable",
        )

    except UnsupportedProviderError as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    except OpenAIError:
        raise HTTPException(
            status_code=502,
            detail="Embedding service unavailable",
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=500,
            detail="Required data file not found",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )