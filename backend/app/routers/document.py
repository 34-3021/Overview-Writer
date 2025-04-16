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
        generate_latex(document, latex_dir)
        
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

# def generate_latex(document, output_dir: Path):
#     with open(output_dir / "references.bib", 'w', encoding='utf-8') as f:
#         pass

#     with open(output_dir / "macro.tex", 'w', encoding='utf-8') as f:
#         f.write(r"""\documentclass[a4paper,zihao=-4,UTF8]{ctexart}
# \pagestyle{plain}
# \date{}
# \usepackage[top=1.0in, bottom=1.0in, left=1.25in, right=1.25in]{geometry} 
# \setlength{\baselineskip}{20pt}
# \usepackage{titlesec}
# \usepackage{zhnumber}
# \usepackage{abstract}
# \usepackage{indentfirst}
# \setlength{\parindent}{2em}
# \usepackage{color}   % May be necessary if you want to color links
# \usepackage{hyperref}
# \hypersetup{
#     colorlinks=true, %set true if you want colored links
#     linktoc=all,     %set to all if you want both sections and subsections linked
#     linkcolor=black,  %choose some color if you want links to stand out
# }
# \usepackage{booktabs}
# \usepackage{multirow}
# \usepackage{graphicx}
# \usepackage{enumitem}
# \usepackage{amsmath,amssymb}

# % numbering restarts at each section
# \numberwithin{figure}{section}  
# \numberwithin{table}{section}
# \numberwithin{equation}{section}

# \usepackage{xcolor,colortbl}
# \newcommand{\zw}[1]{\textcolor{cyan}{(Zhuowen: #1)}}
# \usepackage[capitalize]{cleveref}  % Support for easy cross-referencing
# \crefname{figure}{图}{图}
# \crefname{table}{表}{表}
# \crefname{equation}{公式}{公式}


# % set font for English
# \usepackage{fontspec}
# \setmainfont{Times New Roman}
# \setsansfont{Arial}
# \setromanfont{Times New Roman}
# % the following two are to support combined Chinese and English
# \newcommand{\hei}[1]{\heiti\sffamily #1}
# \newcommand{\song}[1]{\songti\rmfamily #1}


# % setup style for table of contents
# \usepackage{titlesec}
# \usepackage{titletoc}
# \usepackage{tocloft}
# \titlecontents{section}[1em]{\zihao{-4}}{\contentslabel{1em}}{\hspace{-1em}}{\titlerule*[0.5pc]{$.$}\contentspage}
# \titlecontents{subsection}[3em]{\zihao{-4}}{\contentslabel{2em}}{\hspace{-2em}}{\titlerule*[0.5pc]{$.$}\contentspage}
# \titlecontents{subsubsection}[5em]{\zihao{-4}}{\contentslabel{3em}}{\hspace{-3em}}{\titlerule*[0.5pc]{$.$}\contentspage}
# \renewcommand{\cfttoctitlefont}{\zihao{2}\heiti}
# \renewcommand{\contentsname}{\hfill 目~录\hfill}   
# \renewcommand{\cftaftertoctitle}{\hfill}

# % update references to Chinese style, font size and type can also be set here
# \usepackage{caption}
# % uncomment this if you want to use "第一章" instead of "第 1 章"
# % \renewcommand\thesection{\zhnum{section}}
# \titleformat{\section}{\centering\hei\zihao{-2}}{第~\thesection~章}{1em}{}[]
# \titleformat{\subsection}{\hei\zihao{-3}}{\arabic{section}.\arabic{subsection}}{1em}{}[]
# \titleformat{\subsubsection}{\hei\zihao{4}}{\arabic{section}.\arabic{subsection}.\arabic{subsubsection}}{1em}{}[]
# \renewcommand{\abstractnamefont}{\hei\zihao{-2}}
# \renewcommand{\abstracttextfont}{}
# % \renewenvironment{abstract}{\begin{center}{\hei\zihao{-2}摘~要}\end{center}\par} \\
# % \newenvironment{abstract-en}{\begin{center}{\hei\zihao{-2}Abstract}\end{center}\par}

# \renewcommand{\figurename}{图}
# \renewcommand{\tablename}{表}
# \renewcommand{\thefigure} {\arabic{section}-\arabic{figure}}
# \renewcommand{\theequation}{\arabic{section}.\arabic{equation}}
# \renewcommand{\thetable} {\arabic{section}-\arabic{table}}
# \captionsetup{labelsep=space} 


# % title text
# \newcommand{\mytitle}{""")
#         f.write(f"{document.title}")
#         f.write(r"""}

# % header
# \usepackage{fancyhdr}
# \pagestyle{fancy}
# \fancyhead[L]{\kaishu\zihao{-5}\mytitle}
# \fancyhead[R]{\kaishu\zihao{-5}\leftmark}
# \renewcommand\headrulewidth{.5pt}
# \renewcommand\footrulewidth{0pt}

# % for hype-reference of "section*" to work properly
# \usepackage{xparse}
# \let\oldsection\section
# \makeatletter
# \newcounter{@secnumdepth}
# \RenewDocumentCommand{\section}{s o m}{%
#   \IfBooleanTF{#1}
#     {\setcounter{@secnumdepth}{\value{secnumdepth}}% Store secnumdepth
#      \setcounter{secnumdepth}{0}% Print only up to \chapter numbers
#      \oldsection{#3}% \section*
#      \setcounter{secnumdepth}{\value{@secnumdepth}}}% Restore secnumdepth
#     {\IfValueTF{#2}% \section
#        {\oldsection[#2]{#3}}% \section[.]{..}
#        {\oldsection{#3}}}% \section{..}
# }
# \makeatother

# % use GB/T 7714—2015 BibTeX Style
# \usepackage{gbt7714}
# \bibliographystyle{gbt7714-numerical}
# """)

#     with open(output_dir / "main.tex", 'w', encoding='utf-8') as f:
#         f.write(r"""%% main.tex
# %% Copyright Zhuowen Yuan
# %
# % This work may be distributed and/or modified under the
# % conditions of the LaTeX Project Public License, either version 1.3
# % of this license or (at your option) any later version.
# % The latest version of this license is in
# %   http://www.latex-project.org/lppl.txt
# % and version 1.3 or later is part of all distributions of LaTeX
# % version 2005/12/01 or later.
# %
# % This work has the LPPL maintenance status `maintained'.
# % 
# % The Current Maintainer of this work is Zhuowen Yuan.
# %
# % This work consists of the files main.tex and macro.tex.

# \input{macro}

# \begin{document}
# \title{\hei\zihao{-2}\mytitle}
# \maketitle
# \thispagestyle{empty}
# \clearpage


# \pagenumbering{Roman}

# % important notes: if you find the ToC overflow one page, 
# % then add the following line before the overflowing section in main text 
# % \addtocontents{toc}{\protect\newpage\protect}
# {\pagestyle{plain}
# \tableofcontents
# \clearpage}


# \pagenumbering{arabic}
# \setcounter{page}{1}
# """)
#         for section in document.content.get('sections', []):
#             if section['type'] == 'heading1':
#                 f.write(f"\\section{{{section['content']}}}\n")
#             elif section['type'] == 'heading2':
#                 f.write(f"\\subsection{{{section['content']}}}\n")
#             else:
#                 f.write(f"{section['content']}\n\n")
#         f.write(r"""
# \clearpage
# \bibliography{references}


# \clearpage
# \section*{致谢}
# I would like to thank xxx for their advice.


# \end{document}
# """)
def generate_latex(document, output_dir: Path):
    with open(output_dir / "macro.tex", 'w', encoding='utf-8') as f:
        f.write(r"""\documentclass{article}
\usepackage{graphicx} % Required for inserting images

\title{""")
        f.write(f"{document.title}")
        f.write(r"""}
                
\begin{document}

\maketitle

""")
        for section in document.content.get('sections', []):
            if section['type'] == 'heading1':
                f.write(f"\\section{{{section['content']}}}\n")
            elif section['type'] == 'heading2':
                f.write(f"\\subsection{{{section['content']}}}\n")
            else:
                f.write(f"{section['content']}\n\n")
        f.write(r"""
\end{document}""")
