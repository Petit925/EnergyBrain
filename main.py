import fitz  # PyMuPDF
import tiktoken
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# Завантаження API ключів із secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_ENVIRONMENT = st.secrets["PINECONE_ENVIRONMENT"]
PINECONE_INDEX_NAME = st.secrets["PINECONE_INDEX_NAME"]

# Ініціалізація клієнтів
client = OpenAI(api_key=OPENAI_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)

# Завантаження PDF
def load_pdf_text(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

# Розбиття на чанки
def chunk_text(text, max_tokens=500):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

# Створення ембедінгів
def embed_texts(texts):
    embeddings = []
    for chunk in texts:
        res = client.embeddings.create(
            input=[chunk],
            model="text-embedding-ada-002"
        )
        embeddings.append((chunk, res.data[0].embedding))
    return embeddings

# Завантаження в Pinecone
def upload_to_pinecone(embeddings):
    vectors = [
        {"id": f"chunk-{i}", "values": embedding, "metadata": {"text": chunk}}
        for i, (chunk, embedding) in enumerate(embeddings)
    ]
    index.upsert(vectors=vectors)

# Пошук у векторній базі
def search_index(query, top_k=5):
    res = client.embeddings.create(input=[query], model="text-embedding-ada-002")
    query_embed = res.data[0].embedding
    result = index.query(vector=query_embed, top_k=top_k, include_metadata=True)
    return result['matches']

# Побудова prompt
def build_prompt(query, results):
    context = "\n---\n".join([r["metadata"]["text"] for r in results])
    return f"""
Ти експерт з комплаєнсу. Відповідай коротко, чітко, тільки на основі наданого контексту.

Контекст:
{context}

Запит: {query}
Відповідь:
"""

# Запит до GPT
def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
