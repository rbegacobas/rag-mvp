from qdrant_client import QdrantClient, models
import os

# Carga variables de entorno o ponlas aquí directamente
QDRANT_HOST = os.getenv("QDRANT_HOST", "https://16a613d2-f8f8-48d4-b285-6761c9df96f5.us-east4-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "uxulW5pvvhKW0n-29-JcmRbW5wSecuYqEoV0eQEQqjSHX2g95YfbhQ")
COLLECTION_NAME = "docs"
EMBEDDING_SIZE = 1536

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

# Elimina la colección si existe
try:
    client.delete_collection(collection_name=COLLECTION_NAME)
    print(f"Colección '{COLLECTION_NAME}' eliminada.")
except Exception as e:
    print(f"No se pudo eliminar la colección (puede que no exista): {e}")

# Recrea la colección (sin payload_schema)
client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=models.VectorParams(size=EMBEDDING_SIZE, distance=models.Distance.COSINE)
)
print(f"Colección '{COLLECTION_NAME}' creada.")

# Crea los índices de payload
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="empresa",
    field_schema=models.PayloadSchemaType.KEYWORD
)
print("Índice 'empresa' (keyword) creado.")

client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="activo",
    field_schema=models.PayloadSchemaType.BOOL
)
print("Índice 'activo' (bool) creado.") 