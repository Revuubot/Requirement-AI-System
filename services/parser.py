import fitz  # PyMuPDF
from io import BytesIO
from fastapi import UploadFile


def extract_text_from_pdf_path(file_path: str) -> str:
    """Extracts text from a PDF given a file path"""
    text = ""

    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()

    return text.strip()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extracts text from uploaded PDF bytes"""
    text = ""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    return text.strip()


async def parse_pdf_upload(file: UploadFile) -> str:
    """Reads UploadFile and extracts text"""
    pdf_bytes = await file.read()
    return extract_text_from_pdf_bytes(pdf_bytes)
