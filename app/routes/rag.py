from fastapi import APIRouter, UploadFile, File, Form
from app.services import loader, splitter, embedder, vector_store, rag
from typing import List
import os

router = APIRouter()

TEMP_FILE = "temp.pdf"

@router.post("/upload-doc")
def upload_doc(file: UploadFile = File(...), empresa: str = Form(...)):
    with open(TEMP_FILE, "wb") as f:
        f.write(file.file.read())
    pages = loader.extract_text_from_pdf(TEMP_FILE)
    text = "\n".join(pages)
    os.remove(TEMP_FILE)
    return {"text": text, "empresa": empresa}

@router.post("/index")
def index_doc(text: str = Form(...), empresa: str = Form(...)):
    chunks = splitter.chunk_text(text)
    embeddings = embedder.get_embeddings(chunks)
    metadatas = [{"empresa": empresa} for _ in chunks]
    vector_store.add_documents(chunks, embeddings, metadatas)
    return {"status": "indexed", "chunks": len(chunks)}

@router.post("/query")
def query_doc(question: str = Form(...), empresa: str = Form(...)):
    # Embedding de la pregunta
    q_embedding = embedder.get_embeddings([question])[0]
    # Recuperar chunks similares
    results = vector_store.query_similar(q_embedding)
    # Filtrar por empresa
    context_chunks = [doc for doc, meta in zip(results["documents"][0], results["metadatas"][0]) if meta.get("empresa") == empresa]
    if not context_chunks:
        return {"respuesta": "No se encontró contexto para la empresa indicada."}
    prompt = rag.build_prompt(context_chunks, question, empresa)
    respuesta = rag.ask_llm(prompt)
    return {"respuesta": respuesta, "contexto": context_chunks}

# Aquí se agregarán los endpoints: /upload-doc, /index, /query 