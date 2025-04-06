from main_logic import load_pdf_text, chunk_text, embed_texts, upload_to_pinecone

# Функція для завантаження одного PDF з тегом-джерелом
def process_pdf_to_pinecone(filepath, source_tag, index_name="energybrain-index"):
    print(f"🔄 Обробка файлу: {filepath}")
    
    # Крок 1: зчитування тексту з PDF
    text = load_pdf_text(filepath)

    # Крок 2: розбиття на chunks
    chunks = chunk_text(text)

    # Крок 3: створення ембедінгів
    embeddings = []
    for chunk in chunks:
        emb = embed_texts([chunk])[0]  # повертає [(chunk, embedding)]
        # Додаємо метадані з тегом-джерелом
        embeddings.append((chunk, emb[1], source_tag))  

    # Крок 4: підготовка та завантаження в Pinecone
    formatted_vectors = [
        {
            "id": f"{source_tag}-chunk-{i}",
            "values": emb,
            "metadata": {"text": text, "source": source_tag}
        }
        for i, (text, emb, source_tag) in enumerate(embeddings)
    ]

    upload_to_pinecone(formatted_vectors, index_name=index_name)
    print(f"✅ Завантажено: {len(formatted_vectors)} chunks з '{filepath}' в індекс '{index_name}'.")

# 🚀 Виконуємо для двох файлів:
process_pdf_to_pinecone("compliance_manual.pdf", source_tag="compliance")
process_pdf_to_pinecone("procurement_manual.pdf", source_tag="procurement")
