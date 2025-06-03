import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHROMA_DB_DIR = os.getenv('CHROMA_DB_DIR', '/Users/ramon/Documents/rag-mvp/db') 