from pypdf import PdfReader
from typing import List

def extract_text_from_pdf(file_path: str) -> List[str]:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return text 