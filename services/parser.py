import PyPDF2
from io import BytesIO
from fastapi import UploadFile


def extract_text_from_pdf_path(file_path: str) -> str:
    """Extracts text from a PDF given a file path using PyPDF2 (serverless-safe)"""
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

    return text.strip()


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """Extracts text from uploaded PDF bytes using PyPDF2 (serverless-safe)"""
    text = ""
    try:
        reader = PyPDF2.PdfReader(BytesIO(pdf_bytes))
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        return f"Error parsing PDF: {str(e)}"

    return text.strip()


async def parse_pdf_upload(file: UploadFile) -> str:
    """Reads UploadFile and extracts text"""
    pdf_bytes = await file.read()
    return extract_text_from_pdf_bytes(pdf_bytes)
