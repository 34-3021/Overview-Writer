from pydantic import BaseModel
from typing import Any, Optional, List, Dict
from datetime import datetime

class DocumentSection(BaseModel):
    id: str
    type: str
    content: str
    isAI: Optional[bool] = False

class DocumentContent(BaseModel):
    sections: List[DocumentSection]

class DocumentBase(BaseModel):
    title: str
    config: Dict[str, Any] = {}

class DocumentCreate(DocumentBase):
    content: DocumentContent

class DocumentUpdate(DocumentBase):
    title: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    content: Optional[DocumentContent] = None

class DocumentInDB(DocumentBase):
    id: int
    user_id: int
    content: DocumentContent
    created_at: datetime

    class Config:
        from_attributes = True

class GenerateContentRequest(BaseModel):
    type: str
    prompt: Optional[str] = None
    