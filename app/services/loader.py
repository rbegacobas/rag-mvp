import fitz  # PyMuPDF
from typing import List
import re
import unicodedata

def clean_text(text: str) -> str:
    # Normaliza el texto a Unicode NFC
    text = unicodedata.normalize("NFC", text)
    # Elimina caracteres no imprimibles
    text = ''.join(c for c in text if c.isprintable())
    # Elimina secuencias largas de símbolos repetidos (8 o más)
    text = re.sub(r'([\-_\*=])\1{7,}', ' ', text)
    # Reemplaza múltiples espacios por uno solo
    text = re.sub(r'\s+', ' ', text)
    # Elimina espacios al inicio y final
    text = text.strip()
    return text

def extract_text_from_pdf(file_path: str) -> List[str]:
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        raw = page.get_text()
        cleaned = clean_text(raw)
        if cleaned:
            text.append(cleaned)
    return text 