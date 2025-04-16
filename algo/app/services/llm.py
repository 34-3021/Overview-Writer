from typing import List, Dict, Any
import requests
from config import settings
from schemas.llm import Message

class LLMService:
    @staticmethod
    def chat_completion(messages: List[Message], stream: bool = False) -> Any:
        url = settings.llm_api_base
        payload = {
            "model": settings.llm_model,
            "messages": [msg.dict() for msg in messages],
            "stream": stream
        }

        if stream:
            raise NotImplementedError("Streaming not implemented yet.")
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    @staticmethod
    def generate_review_content(prompt: str, context: str) -> str:
        messages = [
            Message(role="system", content="你是一个专业的学术助手，擅长撰写文献综述。"),
            Message(role="user", content=f"根据以下上下文:\n{context}\n\n按照下面的要求，撰写一段综述。请你不要回答无关内容，也不要在回答中包含markdown格式。要求如下：{prompt}")
        ]
        response = LLMService.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
