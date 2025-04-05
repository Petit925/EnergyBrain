import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по комплаєнту iC consulenten", layout="wide")

st.title("📄 Асистент по комплаєнту iC consulenten")
st.caption("(Compliance Assistant)")

query = st.text_input("📝 Введіть свій запит, щодо проходження комплаєнсу у iC consulenten:")

if query:
    with st.spinner("🔎 Шукаю відповідь..."):
        try:
            results = search_index(query)
            prompt = build_prompt(query, results)
            response = ask_gpt(prompt)
            st.markdown("### 💡 Відповідь:")
            st.success(response)
        except Exception as e:
            st.error(f"Сталася помилка: {e}")
