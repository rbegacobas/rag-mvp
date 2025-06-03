from openai import OpenAI
from app.config import OPENAI_API_KEY
from typing import List

client = OpenAI(api_key=OPENAI_API_KEY)

def get_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[list]:
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [d.embedding for d in response.data] 