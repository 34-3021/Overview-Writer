from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate, DocumentInDB
from database import get_db
from security import get_current_user
from models.user import User

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
