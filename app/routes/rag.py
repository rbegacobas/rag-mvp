from fastapi import APIRouter, UploadFile, File, Form, Query
from app.services import loader, splitter, embedder, qdrant_store, rag
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
def index_doc(text: str = Form(...), empresa: str = Form(...), document_id: str = Form(None)):
    chunks = splitter.chunk_text(text)
    embeddings = embedder.get_embeddings(chunks)
    metadatas = [{"empresa": empresa} for _ in chunks]
    doc_id = qdrant_store.add_documents(chunks, embeddings, metadatas, document_id=document_id)
    return {"status": "indexed", "chunks": len(chunks), "document_id": doc_id}

@router.post("/query")
def query_doc(question: str = Form(...), empresa: str = Form(...)):
    # Embedding de la pregunta
    q_embedding = embedder.get_embeddings([question])[0]
    # Recuperar chunks similares SOLO de la empresa y activos
    results = qdrant_store.query_similar(q_embedding, empresa=empresa)
    context_chunks = results["documents"][0]
    if not context_chunks:
        return {"respuesta": "No se encontró contexto para la empresa indicada."}
    prompt = rag.build_prompt(context_chunks, question, empresa)
    respuesta = rag.ask_llm(prompt)
    return {"respuesta": respuesta, "contexto": context_chunks}

@router.post("/disable-doc")
def disable_doc(document_id: str = Form(...)):
    qdrant_store.disable_document(document_id)
    return {"status": "disabled", "document_id": document_id}

@router.get("/list-docs")
def list_docs(all: bool = Query(False, description="Mostrar todos los documentos, activos e inactivos")):
    docs = qdrant_store.list_documents(show_all=all)
    return {"documents": docs}

# Aquí se agregarán los endpoints: /upload-doc, /index, /query 