from pydantic import BaseModel
from typing import List, Optional

class EmbeddingRequest(BaseModel):
    input: List[str]
    model: Optional[str] = None

class EmbeddingData(BaseModel):
    object: str = "embedding"
    embedding: List[float]
    index: int

class EmbeddingResponse(BaseModel):
    object: str = "list"
    data: List[EmbeddingData]
    model: str
