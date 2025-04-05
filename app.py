import streamlit as st
from main import load_pdf_text, chunk_text, embed_texts, upload_to_pinecone, search_index, build_prompt, ask_gpt, index

st.set_page_config(page_title="📄 Комплаєнс-асистент", layout="wide")

st.title("📄 Пошук по PDF-документу (Compliance Assistant)")

pdf_file = st.file_uploader("Завантаж PDF", type="pdf")
query = st.text_input("📝 Введіть свій запит:")

if pdf_file and query:
    bytes_data = pdf_file.read()
    text = load_pdf_text(pdf_file)
    pdf_hash = get_pdf_hash(text)

    with st.spinner("Перевірка індексації..."):
        existing = index.query(vector=[0.0]*1536, filter={"pdf_hash": {"$eq": pdf_hash}}, top_k=1)
        if not existing["matches"]:
            chunks = chunk_text(text)
            embeddings = embed_texts(chunks)
            upload_to_pinecone(embeddings, pdf_hash)

    with st.spinner("Генерація відповіді..."):
        matches = search_index(query)
        prompt = build_prompt(query, matches)
        response = ask_gpt(prompt)
        st.success("✅ Відповідь:")
        st.write(response)
