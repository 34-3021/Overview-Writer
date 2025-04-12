from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.base import StandardResponse
from services.document import DocumentService
import os
from datetime import datetime
from typing import Dict
from schemas.document import ProcessLocalFileRequest
from pathlib import Path

router = APIRouter()

# @router.post("/process", response_model=StandardResponse)
# async def process_document(
#     file: UploadFile = File(...),
#     collection_name: str = "default"
# ):
#     try:
#         # 保存临时文件
#         temp_dir = "temp_uploads"
#         os.makedirs(temp_dir, exist_ok=True)
#         file_path = os.path.join(temp_dir, f"{datetime.now().timestamp()}_{file.filename}")
        
#         with open(file_path, "wb") as f:
#             content = await file.read()
#             f.write(content)
        
#         # 处理文件
#         result = DocumentService.process_uploaded_file(
#             file_path=file_path,
#             file_type=file.content_type,
#             collection_name=collection_name
#         )
        
#         # 删除临时文件
#         os.remove(file_path)
        
#         return result
        
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-local", response_model=StandardResponse)
async def process_local_file(request: ProcessLocalFileRequest):
    try:
        # 验证文件路径
        file_path = Path("../../uploads") / request.file_path
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # 处理文件
        result = DocumentService.process_uploaded_file(
            file_path=str(file_path),
            file_type=request.file_type,
            collection_name=request.collection_name
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
