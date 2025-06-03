from chromadb import PersistentClient
from app.config import CHROMA_DB_DIR
from typing import List, Dict
import os

client = PersistentClient(path=CHROMA_DB_DIR)
collection = client.get_or_create_collection("docs")

def add_documents(chunks: List[str], embeddings: List[list], metadatas: List[Dict]):
    ids = [f"doc_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )
    print(f"[DEBUG] Se agregaron {len(chunks)} documentos a ChromaDB.")

def query_similar(query_embedding: list, n_results: int = 3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results 