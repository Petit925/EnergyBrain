import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Compliance Assistant", layout="centered")

st.title("📄 Пошук по PDF-документу\n(Compliance Assistant)")

query = st.text_input("📝 Введіть свій запит:")

if query:
    with st.spinner("🔎 Пошук в базі знань..."):
        matches = search_index(query)
        if not matches:
            st.warning("❗️ Нічого не знайдено у векторній базі.")
        else:
            prompt = build_prompt(query, matches)
            response = ask_gpt(prompt)
            st.markdown("### 💬 GPT-відповідь:")
            st.write(response)
