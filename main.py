import fitz  # PyMuPDF
import tiktoken
import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

# Ініціалізація клієнтів
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pc.Index(st.secrets["PINECONE_INDEX_NAME"])

def load_pdf_text(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

def chunk_text(text, max_tokens=500):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

def embed_texts(texts):
    embeddings = []
    for chunk in texts:
        res = client.embeddings.create(input=[chunk], model="text-embedding-ada-002")
        embeddings.append((chunk, res.data[0].embedding))
    return embeddings

def upload_to_pinecone(embeddings):
    vectors = [
        {"id": f"chunk-{i}", "values": embedding, "metadata": {"text": chunk}}
        for i, (chunk, embedding) in enumerate(embeddings)
    ]
    index.upsert(vectors=vectors)

def search_index(query, top_k=5):
    res = client.embeddings.create(input=[query], model="text-embedding-ada-002")
    query_embed = res.data[0].embedding
    result = index.query(vector=query_embed, top_k=top_k, include_metadata=True)
    return result["matches"]

def build_prompt(query, results):
    context = "\n---\n".join([r["metadata"]["text"] for r in results])
    return f"""
Ти експерт з комплаєнсу. Відповідай коротко, чітко, тільки на основі наданого контексту.

Контекст:
{context}

Запит: {query}
Відповідь:
"""

def ask_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
