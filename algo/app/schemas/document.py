from pydantic import BaseModel
from typing import Optional
from enum import Enum

class FileType(str, Enum):
    PDF = "application/pdf"
    LATEX_ZIP = "application/zip"

class ProcessLocalFileRequest(BaseModel):
    file_path: str
    file_type: FileType
    collection_name: str = "default"
