import fitz  # для читання PDF
import tiktoken  # для розбиття на чанки
from openai import OpenAI
from pinecone import Pinecone

# Підключення до OpenAI і Pinecone
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
pc = Pinecone(api_key=st.secrets["PINECONE_API_KEY"])
index = pc.Index("energybrain-index")  # твій індекс

# 1. Зчитування тексту з PDF
def load_pdf_text(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])

# 2. Розбиття на чанки (не більше 500 токенів)
def chunk_text(text, max_tokens=500):
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    chunks = [tokens[i:i+max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [tokenizer.decode(chunk) for chunk in chunks]

# 3. Ембедінги та відправка в Pinecone
def embed_and_upload(chunks, prefix="nefco", namespace=None):
    vectors = []
    for i, chunk in enumerate(chunks):
        res = client.embeddings.create(input=[chunk], model="text-embedding-ada-002")
        vectors.append({
            "id": f"{prefix}-chunk-{i}",
            "values": res.data[0].embedding,
            "metadata": {"text": chunk}
        })
    index.upsert(vectors=vectors, namespace=namespace)
    print(f"✅ Завантажено {len(vectors)} чанків у Pinecone.")

# 4. Основна функція
def upload_pdf(pdf_path, prefix="nefco", namespace=None):
    text = load_pdf_text(pdf_path)
    chunks = chunk_text(text)
    embed_and_upload(chunks, prefix, namespace)

# 5. Запуск (сюди встав свій PDF)
if __name__ == "__main__":
    upload_pdf("procurement_manual.pdf", prefix="nefco")