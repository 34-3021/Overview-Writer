from fastapi import APIRouter
from schemas.embedding import EmbeddingRequest, EmbeddingResponse
from services.embedding import EmbeddingService

router = APIRouter()

@router.post("/", response_model=EmbeddingResponse)
async def get_embeddings(request: EmbeddingRequest):
    return EmbeddingService.get_embeddings(request.input)
