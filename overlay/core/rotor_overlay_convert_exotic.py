import os
import sys

def pdf_to_txt(filename):
    from PyPDF2 import PdfReader
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".txt")
    reader = PdfReader(in_path)
    with open(out_path, "w", encoding="utf-8") as out:
        for page in reader.pages:
            out.write(page.extract_text() or "")
            out.write("\n")
    print(f"Converted {filename} to TXT.")

def docx_to_txt(filename):
    from docx import Document
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".txt")
    doc = Document(in_path)
    with open(out_path, "w", encoding="utf-8") as out:
        for para in doc.paragraphs:
            out.write(para.text + "\n")
    print(f"Converted {filename} to TXT.")

def xml_to_txt(filename):
    from lxml import etree
    overlay = os.path.expanduser("~/Soap/overlay")
    in_path = os.path.join(overlay, filename)
    out_path = os.path.join(overlay, filename.rsplit('.',1)[0] + ".txt")
    tree = etree.parse(in_path)
    text = ' '.join(tree.xpath('//text()'))
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(text)
    print(f"Converted {filename} to TXT.")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        mode, filename = sys.argv[1], sys.argv[2]
        if mode == "pdf2txt":
            pdf_to_txt(filename)
        elif mode == "docx2txt":
            docx_to_txt(filename)
        elif mode == "xml2txt":
            xml_to_txt(filename)
        else:
            print("Modes: pdf2txt | docx2txt | xml2txt")
    else:
        print("Usage: python rotor_overlay_convert_exotic.py <mode> <filename>")
