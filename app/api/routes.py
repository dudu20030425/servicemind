from fastapi import APIRouter, HTTPException
from app.llm.provider import generate
from app.llm.provider import (
    LLMServiceError,
    UnsupportedProviderError,
    analyze,
    generate,
)
from app.models.schemas import (
    ChatRequest,
    ChatResponse,
    IntentResponse,
)

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