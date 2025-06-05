import os
from qdrant_client import QdrantClient, models
from typing import List, Dict, Optional
import uuid
from app.config import load_dotenv

QDRANT_COLLECTION = "docs"
# IMPORTANTE: Ajusta EMBEDDING_SIZE al tamaño del vector que genera tu modelo de embeddings (ej: 1536 para text-embedding-ada-002 de OpenAI)
EMBEDDING_SIZE = 1536

QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

# Crea la colección si no existe
if QDRANT_COLLECTION not in [c.name for c in client.get_collections().collections]:
    client.recreate_collection(
        collection_name=QDRANT_COLLECTION,
        vectors_config=models.VectorParams(size=EMBEDDING_SIZE, distance=models.Distance.COSINE)
    )

def add_documents(chunks: List[str], embeddings: List[list], metadatas: List[Dict], document_id: Optional[str] = None):
    if document_id is None:
        document_id = str(uuid.uuid4())
    points = []
    for i, (chunk, embedding, meta) in enumerate(zip(chunks, embeddings, metadatas)):
        meta = dict(meta)  # copia para no mutar el original
        meta["activo"] = True
        meta["document_id"] = document_id
        meta["chunk_index"] = i
        chunk_id = str(uuid.uuid4())  # UUID único para cada chunk
        points.append(models.PointStruct(
            id=chunk_id,
            vector=embedding,
            payload={**meta, "text": chunk}
        ))
    client.upsert(collection_name=QDRANT_COLLECTION, points=points)
    print(f"[DEBUG][Qdrant] Se agregaron {len(points)} documentos con document_id={document_id}.")
    return document_id

def query_similar(query_embedding: list, empresa: str, n_results: int = 3):
    search_result = client.search(
        collection_name=QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=n_results,
        query_filter=models.Filter(
            must=[
                models.FieldCondition(key="empresa", match=models.MatchValue(value=empresa)),
                models.FieldCondition(key="activo", match=models.MatchValue(value=True))
            ]
        )
    )
    docs = [hit.payload["text"] for hit in search_result]
    return {"documents": [docs]}

def disable_document(document_id: str):
    # Elimina todos los puntos con ese document_id
    client.delete(
        collection_name=QDRANT_COLLECTION,
        filter=models.Filter(
            must=[models.FieldCondition(key="document_id", match=models.MatchValue(value=document_id))]
        )
    )
    print(f"[DEBUG][Qdrant] Documento {document_id} deshabilitado (chunks eliminados).")

def list_documents(show_all: bool = False):
    # Recupera todos los puntos y agrupa por document_id
    scroll = client.scroll(collection_name=QDRANT_COLLECTION, limit=1000)
    docs = {}
    for point in scroll[0]:
        meta = point.payload
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