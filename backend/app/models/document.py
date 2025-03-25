from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    config = Column(JSON, default={})  # 可配置项
    content = Column(JSON, nullable=False)  # 结构化内容
    created_at = Column(DateTime, default=datetime.now)
    
    owner = relationship("User", back_populates="documents")
