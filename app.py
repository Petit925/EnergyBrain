import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Compliance Assistant iC consulenten", layout="centered")

st.title("📄 Асистент по комплаєнту iC consulenten\n(Compliance Assistant)")

query = st.text_input("📝 Введіть свій запит, щодо проходження комплаєну у iC consulenten:")

if query:
    with st.spinner("🔎 Пошук в базі знань..."):
        matches = search_index(query)
        if not matches:
            st.warning("❗️ Нічого не знайдено у векторній базі.")
        else:
            prompt = build_prompt(query, matches)
            response = ask_gpt(prompt)
            st.markdown("### 💬 GPT-відповідь асистента іС:")
            st.write(response)
