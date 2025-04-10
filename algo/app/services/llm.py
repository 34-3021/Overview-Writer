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
            # response = requests.post(url, json=payload, stream=True)
            # return response.iter_content(chunk_size=None)
            raise "streamed output not implemented for chat completion"
        else:
            response = requests.post(url, json=payload)
            return response.json()
    
    @staticmethod
    def generate_review_content(prompt: str, context: str) -> str:
        messages = [
            Message(role="system", content="你是一个专业的学术助手，擅长撰写文献综述。"),
            Message(role="user", content=f"根据以下上下文:\n{context}\n\n请撰写关于{prompt}的综述内容。")
        ]
        response = LLMService.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
