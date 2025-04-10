from fastapi import APIRouter

router = APIRouter()

# Import all routers
from .embedding import router as embedding_router
from .vector_db import router as vector_db_router
from .llm import router as llm_router
from .document import router as document_router

# Include all routers
router.include_router(embedding_router, prefix="/embedding", tags=["Embedding"])
router.include_router(vector_db_router, prefix="/vector-db", tags=["Vector Database"])
router.include_router(llm_router, prefix="/llm", tags=["LLM"])
router.include_router(document_router, prefix="/document", tags=["Document Processing"])

__all__ = ["router"]
