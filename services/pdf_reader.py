from io import BytesIO
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Safely extract text from a PDF byte stream
    without requiring Tesseract or OCR.
    """

    text = ""

    try:
        reader = PdfReader(BytesIO(pdf_bytes))

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

    except Exception as e:
        print("PDF parsing error:", e)
        return ""

    
    text = (
        text.replace("\x00", "")
            .replace("\u200b", "")
            .replace("cid:", "")
            .strip()
    )

    return text
