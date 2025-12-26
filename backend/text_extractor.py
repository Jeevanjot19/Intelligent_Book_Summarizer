# backend/text_extractor.py

from pathlib import Path
import PyPDF2
import pdfplumber
import docx


# -----------------------------
# TXT extraction
# -----------------------------
def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Fallback encoding
        with open(file_path, "r", encoding="latin-1") as f:
            return f.read()


# -----------------------------
# PDF extraction
# -----------------------------
def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file.
    Tries PyPDF2 first, falls back to pdfplumber.
    """
    text = ""

    # Try PyPDF2
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception:
        text = ""

    # Fallback to pdfplumber if PyPDF2 failed
    if not text.strip():
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass

    return text


# -----------------------------
# DOCX extraction
# -----------------------------
def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from a DOCX file.
    """
    document = docx.Document(file_path)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


# -----------------------------
# Unified extractor
# -----------------------------
def extract_text(file_path: str) -> str:
    """
    Detect file type and extract text accordingly.
    """
    file_ext = Path(file_path).suffix.lower()

    if file_ext == ".txt":
        text = extract_text_from_txt(file_path)
    elif file_ext == ".pdf":
        text = extract_text_from_pdf(file_path)
    elif file_ext == ".docx":
        text = extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    # Clean up
    text = text.strip()

    if not text:
        raise ValueError("No extractable text found")

    return text
