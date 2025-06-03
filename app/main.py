from fastapi import FastAPI
from app.routes import rag

app = FastAPI()

app.include_router(rag.router) 