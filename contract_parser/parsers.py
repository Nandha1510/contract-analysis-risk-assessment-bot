import io
from typing import Union
from pdfplumber import open as pdf_open
import docx


def parse_pdf(file_stream) -> str:
    text_parts = []
    with pdf_open(file_stream) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n".join(text_parts)


def parse_docx(file_stream) -> str:
    # python-docx expects a path or a file-like object
    document = docx.Document(io.BytesIO(file_stream.read()))
    paragraphs = [p.text for p in document.paragraphs]
    return "\n".join(paragraphs)


def parse_txt(file_stream) -> str:
    raw = file_stream.read()
    if isinstance(raw, bytes):
        try:
            raw = raw.decode("utf-8")
        except Exception:
            raw = raw.decode("latin-1", errors="ignore")
    return raw


def parse_file(uploaded_file) -> str:
    # uploaded_file is a Streamlit UploadedFile with .read() and .type
    content_type = uploaded_file.type
    uploaded_file.seek(0)
    if content_type == "application/pdf" or uploaded_file.name.lower().endswith(".pdf"):
        uploaded_file.seek(0)
        return parse_pdf(uploaded_file)
    if content_type in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",) or uploaded_file.name.lower().endswith(".docx"):
        uploaded_file.seek(0)
        return parse_docx(uploaded_file)
    # fallback to text
    uploaded_file.seek(0)
    return parse_txt(uploaded_file)
