import requests
from typing import Dict, Any
from config import settings
from fastapi import HTTPException

class AIService:
    @staticmethod
    def generate_content(prompt: str, context: str = "") -> str:
        try:
            response = requests.post(
                f"{settings.ALGO_BASE_URL}/llm/generate",
                json={
                    "prompt": {"prompt": prompt},
                    "context": context
                }
            )
            response.raise_for_status()
            return response.json()["content"]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate content: {str(e)}"
            )

    @staticmethod
    def query_related_documents(query_text: str, collection_name: str = "default", n_results: int = 3) -> list:
        try:
            response = requests.post(
                f"{settings.ALGO_BASE_URL}/vector-db/query",
                json={
                    "collection_name": collection_name,
                    "query_texts": [query_text],
                    "n_results": n_results
                }
            )
            response.raise_for_status()
            return response.json()[collection_name][0]  # 返回第一个查询结果的所有文档
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to query related documents: {str(e)}"
            )
