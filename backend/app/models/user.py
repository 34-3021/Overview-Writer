from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

from models.file import File
from models.document import Document

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    files = relationship("File", back_populates="owner", cascade="all, delete")
    documents = relationship("Document", back_populates="owner", cascade="all, delete")
