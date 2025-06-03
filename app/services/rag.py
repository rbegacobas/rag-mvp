from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def build_prompt(context_chunks, question, empresa):
    context = "\n".join(context_chunks)
    prompt = f"Responde la siguiente pregunta sobre la empresa {empresa} usando solo la información proporcionada.\n\nContexto:\n{context}\n\nPregunta: {question}\nRespuesta:"
    return prompt

def ask_llm(prompt, model="gpt-3.5-turbo", temperature=0.2):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature
    )
    return response.choices[0].message.content.strip() 