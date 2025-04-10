from typing import List, Dict, Any
from models.vector_db import vector_db

class VectorDBService:
    @staticmethod
    def create_collection(collection_name: str) -> Dict[str, Any]:
        collection = vector_db.create_collection(collection_name)
        return {"status": "success", "collection": collection.name}
    
    @staticmethod
    def add_documents(
        collection_name: str,
        documents: List[str],
        ids: List[str],
        metadatas: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        collection = vector_db.get_collection(collection_name)
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )
        return {"status": "success", "count": len(ids)}
    
    @staticmethod
    def query(
        collection_name: str,
        query_texts: List[str],
        n_results: int = 5,
        where: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        collection = vector_db.get_collection(collection_name)
        results = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where
        )
        return {
            "documents": results["documents"],
            "distances": results["distances"],
            "metadatas": results["metadatas"],
            "ids": results["ids"]
        }
