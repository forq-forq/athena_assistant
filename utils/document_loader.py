import fitz
import docx
import os

def extract_text_from_pdf(file) -> str:
    doc = fitz.open(stream=file, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file) -> str:
    return file.read().decode("utf-8")

def extract_text_from_md(file) -> str:
    return file.read().decode("utf-8")

def load_file(file) -> tuple[str, str]:
    filename = file.name
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file), filename
    elif extension == ".docx":
        return extract_text_from_docx(file), filename
    elif extension == ".txt":
        return extract_text_from_txt(file), filename
    elif extension == ".md":
        return extract_text_from_md(file), filename
    else:
        raise ValueError(f"Unsupported file type: {extension}")
