import os
import zipfile
from pathlib import Path
from typing import Union, List
import pdfplumber
from bs4 import BeautifulSoup

class FileProcessor:
    @staticmethod
    def extract_text_from_pdf(file_path: Union[str, Path]) -> str:
        """从PDF提取文本"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def extract_text_from_latex_zip(zip_path: Union[str, Path]) -> str:
        """从LaTeX zip包提取文本"""
        text = ""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if file_info.filename.endswith('.tex'):
                    with zip_ref.open(file_info) as f:
                        content = f.read().decode('utf-8')
                        # 移除LaTeX命令
                        text += FileProcessor._clean_latex(content) + "\n"
        return text.strip()

    @staticmethod
    def _clean_latex(text: str) -> str:
        """清理LaTeX命令，保留纯文本"""
        # 简单实现，可根据需要扩展
        lines = []
        for line in text.split('\n'):
            if line.strip().startswith('%') or line.strip().startswith('\\'):
                continue
            lines.append(line)
        return ' '.join(lines)

    @staticmethod
    def extract_text_from_html(html: str) -> str:
        """从HTML提取纯文本"""
        soup = BeautifulSoup(html, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
