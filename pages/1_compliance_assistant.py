import streamlit as st
from main_logic import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по комплаєнсу iC", page_icon="📄")
st.title("📄 Ви в асистенті по комплаєнсу!")
st.caption("(Compliance Assistant)")

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("🧹 Очистити чат"):
    st.session_state.messages = []
    st.rerun()  # ← ось так тепер

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

query = st.chat_input("Введіть запит, щодо проходження комплаєнсу у iC consulenten:")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        try:
            matches = search_index(query, index_name="energybrain-index")
            prompt = build_prompt(query, matches)
            response = ask_gpt(prompt)
            st.markdown(response)
        except Exception as e:
            response = "⚠️ Виникла помилка. Перевір API-ключі та з'єднання з Pinecone/OpenAI."
            st.error(str(e))

    st.session_state.messages.append({"role": "assistant", "content": response})
