"""
Script de referencia para agregar índices de payload a una colección existente en Qdrant Cloud.

¿CUÁNDO USAR ESTE SCRIPT?
- Si necesitas filtrar por un nuevo campo en tus consultas (por ejemplo, tipo_documento, fecha, usuario, etc.).
- No es necesario borrar la colección ni los datos existentes para agregar un nuevo índice.

¿CÓMO FUNCIONA?
- Solo debes ejecutar la función create_payload_index para el campo que quieras indexar.
- Si necesitas cambiar el tipo de un índice existente, sí deberás borrar y recrear la colección.

EJEMPLO DE USO:
Agrega un índice de tipo 'keyword' para el campo 'tipo_documento'. Puedes modificar el nombre y tipo según tu necesidad.
"""

from qdrant_client import QdrantClient, models
import os

QDRANT_HOST = os.getenv("QDRANT_HOST", "https://16a613d2-f8f8-48d4-b285-6761c9df96f5.us-east4-0.gcp.cloud.qdrant.io:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "uxulW5pvvhKW0n-29-JcmRbW5wSecuYqEoV0eQEQqjSHX2g95YfbhQ")
COLLECTION_NAME = "docs"

client = QdrantClient(
    url=QDRANT_HOST,
    api_key=QDRANT_API_KEY
)

# Ejemplo: crear un índice para el campo 'tipo_documento' (puedes cambiar el nombre y tipo)
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="tipo_documento",
    field_schema=models.PayloadSchemaType.KEYWORD
)
print("Índice 'tipo_documento' (keyword) creado.") 