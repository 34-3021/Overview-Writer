from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate, DocumentInDB, DocumentUpdate
from database import get_db
from security import get_current_user
from models.user import User
from typing import List, Dict, Any

router = APIRouter()

@router.post("/", response_model=DocumentInDB)
def create_document(
    document: DocumentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_document = Document(
        **document.dict(),
        user_id=user.id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

@router.get("/", response_model=list[DocumentInDB])
def list_documents(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return db.query(Document).filter(Document.user_id == user.id).all()

@router.delete("/{doc_id}")
def delete_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id
    ).first()
    if not document:
        raise HTTPException(404, "Document not found")
    
    db.delete(document)
    db.commit()
    return {"message": "Document deleted"}

@router.get("/{doc_id}", response_model=DocumentInDB)
def get_document(
    doc_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(404, "Document not found")
    return document

@router.put("/{doc_id}", response_model=DocumentInDB)
def update_document(
    doc_id: int,
    document: DocumentUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    db_document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id
    ).first()
    
    if not db_document:
        raise HTTPException(404, "Document not found")
    
    for field, value in document.dict(exclude_unset=True).items():
        setattr(db_document, field, value)
    
    db.commit()
    db.refresh(db_document)
    return db_document

@router.post("/{doc_id}/generate", response_model=Dict[str, Any])
def generate_content(
    doc_id: int,
    prompt: Dict[str, Any],
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    content_type = prompt.get("type", "paragraph")
    
    if content_type == "heading1":
        return {"content": "Generated Heading 1", "type": "heading1"}
    elif content_type == "heading2":
        return {"content": "Generated Heading 2", "type": "heading2"}
    else:
        return {"content": "This is AI-generated paragraph content.", "type": "paragraph"}