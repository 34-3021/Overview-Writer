from datetime import datetime
from pydantic import BaseModel

class FileBase(BaseModel):
    filename: str
    file_type: str
    size: int

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    new_filename: str

class FileInDB(FileBase):
    id: int
    user_id: int
    upload_time: datetime
    processed: bool

    class Config:
        from_attributes = True
