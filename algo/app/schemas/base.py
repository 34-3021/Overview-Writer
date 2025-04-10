from pydantic import BaseModel
from typing import Optional

class StandardResponse(BaseModel):
    status: str
    message: Optional[str] = None
    data: Optional[dict] = None
