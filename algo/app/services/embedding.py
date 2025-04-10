import requests
from typing import List
from config import settings
from schemas.embedding import EmbeddingResponse

class EmbeddingService:
    @staticmethod
    def get_embeddings(texts: List[str]) -> EmbeddingResponse:
        """获取文本的嵌入向量"""
        response = requests.post(
            settings.embedding_api_base,
            json={
                "input": texts,
                "model": settings.embedding_model
            }
        )
        response.raise_for_status()
        return EmbeddingResponse(**response.json())
    
    @staticmethod
    def embed_documents(documents: List[str]) -> List[List[float]]:
        """批量嵌入文档"""
        response = EmbeddingService.get_embeddings(documents)
        return [data.embedding for data in response.data]
