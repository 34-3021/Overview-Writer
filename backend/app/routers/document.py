from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from models.document import Document
from schemas.document import DocumentCreate, DocumentInDB, DocumentUpdate, ExportFormat
from database import get_db
from security import get_current_user
from models.user import User
from typing import Dict, Any
import zipfile
from pathlib import Path
import os
from markdown import markdown
from weasyprint import HTML
from service.ai_service import AIService

def markdown_to_pdf(md_file_path, pdf_file_path):
    # Read the markdown file
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    
    # Convert markdown to HTML
    html_text = markdown(md_text)
    
    # Create a full HTML document with CSS styling
    full_html = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                code {{ background: #f5f5f5; padding: 2px 5px; }}
                pre {{ background: #f5f5f5; padding: 10px; overflow: auto; }}
            </style>
        </head>
        <body>{html_text}</body>
    </html>
    """
    
    # Convert HTML to PDF
    HTML(string=full_html).write_pdf(pdf_file_path)

router = APIRouter()

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

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
    
    if prompt["type"] == "chat":
        return {
            "content": AIService.chat_completion(
                messages=[{
                    "role": "user",
                    "content": prompt.get("prompt", "")
                }]
            ),
            "type": "chat"
        }

    # 获取当前文档
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(404, "Document not found")
    
    # 查询相关文献
    related_docs = AIService.query_related_documents(document.title, f"user_{user.id}")
    # context = "\n\n".join(related_docs) if related_docs else ""
    # print(context)
    context = related_docs
    
    print(prompt)
    # 生成内容
    content = AIService.generate_content(
        prompt=prompt.get("prompt", ""),
        context=context
    )
    
    return {
        "content": content,
        "type": prompt.get("type", "paragraph")
    }

@router.post("/{doc_id}/export")
def export_document(
    doc_id: int,
    export_format: ExportFormat,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == doc_id,
        Document.user_id == user.id
    ).first()
    
    if not document:
        raise HTTPException(404, "Document not found")
    
    temp_path = Path(EXPORT_DIR)
    
    if export_format.format == "pdf":
        # 生成PDF文件
        pdf_path = temp_path / f"{document.title}.pdf"
        # 这里需要实现PDF生成逻辑
        generate_pdf(document.content, pdf_path)
        return FileResponse(
            pdf_path,
            filename=f"{document.title}.pdf",
            media_type="application/pdf"
        )
        
    elif export_format.format == "markdown":
        # 生成Markdown文件
        md_path = temp_path / f"{document.title}.md"
        generate_markdown(document.content, md_path)
        return FileResponse(
            md_path,
            filename=f"{document.title}.md",
            media_type="text/markdown"
        )
        
    elif export_format.format == "latex":
        # 生成LaTeX文件并打包为zip
        latex_dir = temp_path / document.title / "latex"
        latex_dir.mkdir(parents=True, exist_ok=True)

        # 生成主tex文件
        main_tex = latex_dir / "main.tex"
        generate_latex(document.content, main_tex)
        
        # 复制模板文件
        copy_template_files(latex_dir)
        
        # 创建zip文件
        zip_path = temp_path / f"{document.title}.zip"
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in latex_dir.glob("**/*"):
                zipf.write(file, file.relative_to(latex_dir))
                
        return FileResponse(
            zip_path,
            filename=f"{document.title}.zip",
            media_type="application/zip"
        )
        
    else:
        raise HTTPException(400, "Unsupported export format")

def generate_markdown(content: dict, output_path: Path):
    """生成Markdown文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        # 遍历文档内容并转换为Markdown格式
        for section in content.get('sections', []):
            if section['type'] == 'heading1':
                f.write(f"# {section['content']}\n\n")
            elif section['type'] == 'heading2':
                f.write(f"## {section['content']}\n\n")
            else:
                f.write(f"{section['content']}\n\n")

def generate_pdf(content: dict, output_path: Path):
    """生成PDF文件：先转为Markdown再用pandoc转PDF"""
    try:
        # 先创建临时Markdown文件
        md_path = output_path.with_suffix('.md')
        generate_markdown(content, md_path)
        markdown_to_pdf(md_path, output_path)
    except Exception as e:
        raise HTTPException(500, f"PDF生成错误: {str(e)}")

def generate_latex(content: dict, output_path: Path):
    """生成完整的LaTeX文档"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{xeCJK}\n")
        f.write("\\setCJKmainfont{SimSun}\n")
        f.write("\\usepackage{geometry}\n")
        f.write("\\geometry{a4paper, margin=1in}\n")
        f.write("\\title{我的文档}\n")
        f.write("\\author{作者}\n")
        f.write("\\begin{document}\n")
        f.write("\\maketitle\n")
        
        for section in content.get('sections', []):
            if section['type'] == 'heading1':
                f.write(f"\\section{{{section['content']}}}\n")
            elif section['type'] == 'heading2':
                f.write(f"\\subsection{{{section['content']}}}\n")
            else:
                # 处理段落和列表
                text = section['content'].replace('\n', '\\\\\n')
                f.write(f"{text}\n\n")
                
        f.write("\\end{document}\n")

def copy_template_files(dest_dir: Path):
    """复制LaTeX模板文件"""
    # 创建必要的目录结构
    (dest_dir / 'figures').mkdir(exist_ok=True)
    
    # 写入模板文件
    template_content = r"""% 模板文件
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{SimSun}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=1in}

\title{文档标题}
\author{作者}

\begin{document}
\maketitle

\section{引言}

这是文档内容。

\end{document}
"""
    with open(dest_dir / 'template.tex', 'w', encoding='utf-8') as f:
        f.write(template_content)