from fastapi import APIRouter
from schemas.vector_db import (
    CollectionCreateRequest,
    DocumentAddRequest,
    QueryRequest
)
from services.vector_db import VectorDBService

router = APIRouter()

@router.post("/collections")
async def create_collection(request: CollectionCreateRequest):
    return VectorDBService.create_collection(request.name)

@router.post("/documents")
async def add_documents(request: DocumentAddRequest):
    return VectorDBService.add_documents(
        request.collection_name,
        request.documents,
        request.ids,
        request.metadatas
    )

@router.post("/query")
async def query_documents(request: QueryRequest):
    return VectorDBService.query(
        request.collection_name,
        request.query_texts,
        request.n_results,
        request.where
    )
