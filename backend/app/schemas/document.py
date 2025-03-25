from pydantic import BaseModel
from typing import Any
from datetime import datetime

class DocumentBase(BaseModel):
    title: str
    config: dict = {}

class DocumentCreate(DocumentBase):
    content: dict

class DocumentInDB(DocumentBase):
    id: int
    user_id: int
    content: dict
    created_at: datetime

    class Config:
        from_attributes = True
