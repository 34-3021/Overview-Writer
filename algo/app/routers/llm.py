from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas.llm import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ContentGenerationRequest,
    ContentGenerationResponse
)
from services.llm import LLMService

router = APIRouter()

@router.post("/chat", response_model=ChatCompletionResponse)
async def chat_completion(request: ChatCompletionRequest):
    return LLMService.chat_completion(request.messages)

@router.post("/chat/stream")
async def chat_completion_stream(request: ChatCompletionRequest):
    generator = LLMService.chat_completion(request.messages, stream=True)
    return StreamingResponse(generator, media_type="text/event-stream")

@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    content = LLMService.generate_review_content(
        prompt=request.prompt.get("prompt", ""),
        context=request.context or ""
    )
    return {
        "content": content,
        "type": request.prompt.get("type", "paragraph")
    }
