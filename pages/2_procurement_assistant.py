import streamlit as st
from main_logic import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по закупівлям НЕФКО", page_icon="📑")
st.title("📑 Ви в асистенті по закупівлям НЕФКО!")
st.caption("(NEFCO Procurement Assistant)")

# Стан чату
if "messages" not in st.session_state:
    st.session_state.messages = []

# Кнопка очищення
if st.button("🧹 Очистити чат"):
    st.session_state.messages = []
    st.experimental_rerun()

# Вивід попередніх повідомлень
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Чат-ввід
query = st.chat_input("Введіть запит, щодо закупівель у проектах НЕФКО:")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)

    with st.chat_message("assistant"):
        try:
            matches = search_index(query, index_name
