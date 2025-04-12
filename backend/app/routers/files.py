from fastapi import APIRouter, Depends, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from models.file import File
from fastapi import File as FastAPIFile
from models.user import User
from schemas.file import FileInDB, FileCreate, FileUpdate
from database import get_db
from security import get_current_user
import requests
from config import settings

router = APIRouter()

UPLOAD_DIR = "../../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=FileInDB)
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 生成唯一文件名
    ext = file.filename.split('.')[-1]
    unique_name = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)
    
    # 保存文件
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # 创建数据库记录
    db_file = File(
        filename=file.filename,
        file_type=file.content_type,
        size=len(contents),
        storage_path=file_path,
        user_id=current_user.id,
        # owner=current_user
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    try:
        response = requests.post(
            f"{settings.ALGO_BASE_URL}/document/process-local",
            json={
                "file_path": unique_name,
                "file_type": file.content_type,
                "collection_name": f"user_{current_user.id}"
            }
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Document processing failed: {str(e)}")

    return db_file

@router.get("/", response_model=List[FileInDB])
def list_files(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(File)\
        .filter(File.user_id == current_user.id)\
        .all()

@router.get("/{file_id}", response_model=FileInDB)
def get_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return file

@router.put("/{file_id}", response_model=FileInDB)
def update_file(
    file_id: int,
    update_data: FileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    db_file.filename = update_data.new_filename
    db.commit()
    db.refresh(db_file)
    return db_file

@router.delete("/{file_id}")
def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_file = db.query(File).filter(
        File.id == file_id,
        File.user_id == current_user.id
    ).first()
    
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # 删除物理文件
    if os.path.exists(db_file.storage_path):
        os.remove(db_file.storage_path)
    
    db.delete(db_file)
    db.commit()
    return {"message": "File deleted"}
