# MVP RAG Empresarial (Backend)

## Objetivo
Procesar un documento PDF, extraer texto, hacer chunking, generar embeddings, guardar en una base vectorial local y consultar con una pregunta. Sin frontend, solo endpoints simples (FastAPI) para pruebas vía Postman/cURL.

## Estructura del proyecto

```
rag-mvp/
├── app/
│   ├── __init__.py
│   ├── main.py                # FastAPI app con los endpoints
│   ├── config.py              # Carga de variables de entorno
│   ├── routes/
│   │   ├── __init__.py
│   │   └── rag.py             # Endpoints de carga, procesamiento, consulta
│   ├── services/
│   │   ├── __init__.py
│   │   ├── loader.py          # Lectura y extracción de texto de documentos
│   │   ├── splitter.py        # Chunking de texto
│   │   ├── embedder.py        # Embedding vía OpenAI
│   │   ├── vector_store.py    # Inserción y búsqueda en base vectorial (Chroma)
│   │   └── rag.py             # Construcción del prompt y query al LLM
├── .env                       # Clave API de OpenAI
├── requirements.txt
└── README.md
```

## Tecnologías principales
- Python 3.10+
- FastAPI
- Langchain
- OpenAI
- ChromaDB
- PyPDF
- Uvicorn

## Cómo levantar el entorno

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Asegúrate de tener el archivo `.env` con tu API Key de OpenAI:
   ```env
   OPENAI_API_KEY=sk-xxxxxx
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints principales
- `/upload-doc` → Carga y procesa el PDF
- `/index` → Genera embeddings y guarda en Chroma
- `/query` → Consulta con pregunta y empresa

--- 