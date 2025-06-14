import requests
from typing import Dict, Any, List
from config import settings
from fastapi import HTTPException

class AIService:
    @staticmethod
    def chat_completion(messages: List[Dict[str, str]]) -> str:
        try:
            response = requests.post(
                f"{settings.ALGO_BASE_URL}/llm/chat",
                json={
                    "messages": messages
                }
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate chat response: {str(e)}"
            )

    @staticmethod
    def generate_content(prompt: str, context: str = "") -> str:
        try:
            response = requests.post(
                f"{settings.ALGO_BASE_URL}/llm/generate",
                json={
                    "prompt": prompt,
                    "context": context
                }
            )
            print(response.status_code, response.content)
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
            print(response.status_code, response.content)
            response.raise_for_status()
            return response.content.decode()  # 返回第一个查询结果的所有文档
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to query related documents: {str(e)}"
            )
