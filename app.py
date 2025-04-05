import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по комплаєнсу iC consulenten", page_icon="📄")

st.title("📄 Асистент по комплаєнсу iC consulenten")
st.caption("(Compliance Assistant)")

# Ініціалізація історії чату
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Форма для запиту
with st.form("chat_form"):
    st.markdown("💬 **Введіть свій запит, щодо проходження комплаєнсу у iC consulenten:**")
    query = st.text_input("Що вас цікавить?", label_visibility="collapsed")
    submitted = st.form_submit_button("Запитати")

# Після надсилання запиту
if submitted and query:
    matches = search_index(query)
    prompt = build_prompt(query, matches)
    response = ask_gpt(prompt)

    st.session_state.chat_history.append({
        "question": query,
        "answer": response
    })

    st.rerun()

# Виведення історії чату
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.success(chat["answer"])

# Кнопка очистки чату
if st.button("🧹 Очистити чат"):
    st.session_state.chat_history = []
    st.rerun()
