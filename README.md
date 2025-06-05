# MVP RAG Empresarial (Backend)

## Objetivo
Procesar documentos PDF, extraer texto, hacer chunking, generar embeddings, guardar en una base vectorial (Qdrant/ChromaDB) y consultar con una pregunta. Sin frontend, solo endpoints simples (FastAPI) para pruebas vía Postman/cURL.

## Estructura del proyecto

```
rag-mvp/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app con los endpoints
│   ├── config.py              # Carga de variables de entorno
│   ├── routes/
│   │   ├── __init__.py
│   │   └── rag.py             # Endpoints de carga, procesamiento, consulta, gestión docs
│   ├── services/
│   │   ├── __init__.py
│   │   ├── loader.py          # Extracción de texto (PyMuPDF)
│   │   ├── splitter.py        # Chunking de texto
│   │   ├── embedder.py        # Embedding vía OpenAI
│   │   ├── vector_store.py    # Inserción y búsqueda en ChromaDB (legacy)
│   │   ├── qdrant_store.py    # Inserción y búsqueda en Qdrant
│   │   └── rag.py             # Construcción del prompt y query al LLM
├── .env                       # Variables de entorno (API keys, Qdrant, etc)
├── requirements.txt
└── README.md
```

## Tecnologías principales
- Python 3.10+
- FastAPI
- Langchain
- OpenAI
- Qdrant (vector store principal)
- ChromaDB (opcional/legacy)
- PyMuPDF (fitz)
- Uvicorn
- python-dotenv

## Cómo levantar el entorno

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Crea el archivo `.env` con tus variables:
   ```env
   OPENAI_API_KEY=sk-xxxxxx
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   # Otros parámetros según tu entorno
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```
4. (Opcional) Levanta Qdrant con Docker:
   ```bash
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
   ```

## Endpoints principales
- `POST /upload-doc` → Carga y procesa el PDF (extrae texto, limpia y almacena metadatos)
- `POST /index` → Genera embeddings y guarda chunks en Qdrant (o ChromaDB)
- `POST /query` → Consulta semántica con pregunta y empresa
- `GET /list-docs` → Lista documentos por empresa y estado (activos/todos)
- `POST /disable-doc` → Deshabilita (soft delete) un documento por ID

## Características avanzadas
- **Extracción de texto profesional:** PyMuPDF para PDFs complejos.
- **Limpieza avanzada:** Elimina ruido visual, líneas de guiones, símbolos repetidos, etc.
- **Gestión de documentos:** Soft delete, filtrado por empresa, UUID por documento y chunk.
- **Persistencia y escalabilidad:** Qdrant como vector store robusto, ChromaDB opcional.
- **Variables de entorno:** Configuración flexible y segura.
- **Código modular y profesional:** Listo para producción y escalabilidad.

## Recomendaciones
- Almacenar los PDFs originales en S3/MinIO para trazabilidad.
- Usar Qdrant Cloud para producción.
- Versionar y auditar los documentos y sus embeddings.
- Proteger los endpoints con autenticación en producción.

--- 