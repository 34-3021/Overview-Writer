from typing import List, Dict
from pathlib import Path
from utils.file_processor import FileProcessor
from services.embedding import EmbeddingService
from models.vector_db import vector_db

class DocumentService:
    @staticmethod
    def process_uploaded_file(file_path: str, file_type: str, collection_name: str) -> Dict:
        """处理上传的文件并存入向量数据库"""
        if file_type == "application/pdf":
            text = FileProcessor.extract_text_from_pdf(file_path)
        elif file_type == "application/zip":
            text = FileProcessor.extract_text_from_latex_zip(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # 分块处理文本
        chunks = DocumentService._chunk_text(text)
        
        # 获取嵌入向量
        # embeddings = EmbeddingService.embed_documents(chunks)
        
        # 存入向量数据库
        try:
            collection = vector_db.get_collection(collection_name)
        except Exception as e:
            print(f"Collection {collection_name} not found, creating new one")
            collection = vector_db.create_collection(collection_name)
            
        ids = [f"{Path(file_path).stem}_{i}" for i in range(len(chunks))]
        collection.add(
            documents=chunks,
            # embeddings=embeddings,
            ids=ids
        )
        
        return {
            "status": "success",
            "chunks": len(chunks),
            "collection": collection_name
        }

    @staticmethod
    def _chunk_text(text: str, chunk_size: int = 1000) -> List[str]:
        """将文本分割成块"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunks.append(' '.join(words[i:i+chunk_size]))
        return chunks
