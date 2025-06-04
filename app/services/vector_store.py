from chromadb import PersistentClient
from app.config import CHROMA_DB_DIR
from typing import List, Dict
import os
import uuid

client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection("docs")

def add_documents(chunks: List[str], embeddings: List[list], metadatas: List[Dict], document_id: str = None):
    if document_id is None:
        document_id = str(uuid.uuid4())
    ids = [f"{document_id}_chunk_{i}" for i in range(len(chunks))]
    # Agrega metadatos de soft delete y document_id
    for meta in metadatas:
        meta["activo"] = True
        meta["document_id"] = document_id
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"[DEBUG] Se agregaron {len(chunks)} documentos a ChromaDB con document_id={document_id}.")
    return document_id

def disable_document(document_id: str):
    # Recupera todos los ids de los chunks con ese document_id
    all_data = collection.get(include=["metadatas"])
    ids_to_delete = []
    for idx, meta in enumerate(all_data["metadatas"]):
        if isinstance(meta, dict) and meta.get("document_id") == document_id:
            ids_to_delete.append(all_data["ids"][idx])
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        print(f"[DEBUG] Documento {document_id} deshabilitado (chunks eliminados).")
    else:
        print(f"[DEBUG] No se encontraron chunks para document_id={document_id}.")

def query_similar(query_embedding: list, empresa: str, n_results: int = 3):
    # Usa $and para combinar filtros
    where = {"$and": [{"activo": True}, {"empresa": empresa}]}
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where=where
    )
    return results

def list_documents(show_all: bool = False):
    # Recupera todos los metadatos de los documentos
    all_data = collection.get(include=["metadatas"])
    print("[DEBUG] Estructura de metadatos devuelta por collection.get:", all_data)
    all_metas = all_data['metadatas']
    docs = {}
    for meta in all_metas:
        if not isinstance(meta, dict):
            continue
        doc_id = meta.get("document_id")
        activo = meta.get("activo", True)
        if doc_id and doc_id not in docs:
            if show_all or activo:
                docs[doc_id] = {
                    "empresa": meta.get("empresa"),
                    "activo": activo,
                    "document_id": doc_id
                }
    return list(docs.values()) 