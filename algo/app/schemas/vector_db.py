from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class CollectionCreateRequest(BaseModel):
    """创建集合请求"""
    name: str
    metadata: Optional[Dict[str, Any]] = None
    get_or_create: bool = False

class CollectionInfoResponse(BaseModel):
    """集合信息响应"""
    name: str
    id: str
    metadata: Optional[Dict[str, Any]] = None
    tenant: Optional[str] = None
    database: Optional[str] = None
    status: str = "active"

class DocumentAddRequest(BaseModel):
    """添加文档请求"""
    collection_name: str
    documents: List[str]
    ids: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None
    embeddings: Optional[List[List[float]]] = None

class DocumentAddResponse(BaseModel):
    """添加文档响应"""
    status: str
    count: int
    collection: str
    inserted_ids: List[str]

class DocumentUpdateRequest(BaseModel):
    """更新文档请求"""
    collection_name: str
    documents: Optional[List[str]] = None
    ids: List[str]
    metadatas: Optional[List[Dict[str, Any]]] = None
    embeddings: Optional[List[List[float]]] = None

class DocumentDeleteRequest(BaseModel):
    """删除文档请求"""
    collection_name: str
    ids: List[str]

class QueryRequest(BaseModel):
    """查询请求"""
    collection_name: str
    query_texts: List[str]
    n_results: int = 5
    where: Optional[Dict[str, Any]] = None
    where_document: Optional[Dict[str, Any]] = None
    include: Optional[List[str]] = None

class QueryResultItem(BaseModel):
    """单个查询结果项"""
    id: str
    document: str
    metadata: Optional[Dict[str, Any]] = None
    distance: float

class QueryResponse(BaseModel):
    """查询响应"""
    query_texts: List[str]
    results: List[List[QueryResultItem]]

class CollectionStatsResponse(BaseModel):
    """集合统计信息响应"""
    count: int
    size_bytes: int
    status: str

class ListCollectionsResponse(BaseModel):
    """列出所有集合响应"""
    collections: List[CollectionInfoResponse]

class GetDocumentRequest(BaseModel):
    """获取文档请求"""
    collection_name: str
    ids: Optional[List[str]] = None
    where: Optional[Dict[str, Any]] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

class DocumentInfo(BaseModel):
    """文档信息"""
    id: str
    document: str
    metadata: Optional[Dict[str, Any]] = None
    embedding: Optional[List[float]] = None

class GetDocumentResponse(BaseModel):
    """获取文档响应"""
    documents: List[DocumentInfo]
    count: int

class UpdateCollectionRequest(BaseModel):
    """更新集合元数据请求"""
    collection_name: str
    new_name: Optional[str] = None
    new_metadata: Optional[Dict[str, Any]] = None

class DeleteCollectionRequest(BaseModel):
    """删除集合请求"""
    collection_name: str

class DeleteCollectionResponse(BaseModel):
    """删除集合响应"""
    status: str
    deleted_collection: str
