#!/usr/bin/env python3
import os
import docx
import PyPDF2

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_docx(path):
    doc = docx.Document(path)
    return '\n'.join([para.text for para in doc.paragraphs])

def extract_text_from_pdf(path):
    pdf = PyPDF2.PdfReader(open(path, "rb"))
    text = []
    for page in pdf.pages:
        text.append(page.extract_text())
    return "\n".join(text)

def extract_text(path):
    ext = os.path.splitext(path)[-1].lower()
    if ext == ".txt":
        return extract_text_from_txt(path)
    elif ext == ".docx":
        return extract_text_from_docx(path)
    elif ext == ".pdf":
        return extract_text_from_pdf(path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")
