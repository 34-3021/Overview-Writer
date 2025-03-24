from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))  # MIME type
    size = Column(Integer)  # Bytes
    upload_time = Column(DateTime, default=lambda: datetime.utcnow)
    # processed = Column(Boolean, default=False)  # 是否被大模型处理
    storage_path = Column(String(512), unique=True)  # 实际存储路径
    
    owner = relationship("User", back_populates="files")
