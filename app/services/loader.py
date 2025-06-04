from pypdf import PdfReader
from typing import List
import re
import unicodedata

def clean_text(text: str) -> str:
    # Normaliza el texto a Unicode NFC
    text = unicodedata.normalize("NFC", text)
    # Elimina caracteres no imprimibles
    text = ''.join(c for c in text if c.isprintable())
    # Reemplaza múltiples espacios por uno solo
    text = re.sub(r'\s+', ' ', text)
    # Elimina espacios al inicio y final
    text = text.strip()
    return text

def extract_text_from_pdf(file_path: str) -> List[str]:
    reader = PdfReader(file_path)
    text = []
    for page in reader.pages:
        raw = page.extract_text() or ""
        cleaned = clean_text(raw)
        if cleaned:
            text.append(cleaned)
    return text 