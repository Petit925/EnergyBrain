import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по комплаєнсу iC consulenten", page_icon="📄")

st.title("📄 Асистент по комплаєнсу iC consulenten")
st.caption("(Compliance Assistant)")

# Ініціалізація історії чату
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Виведення всієї історії чату
for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat["question"])
    with st.chat_message("assistant"):
        st.success(chat["answer"])

# Поле вводу в самому низу
if prompt := st.chat_input("Введіть запит, щодо проходження комплаєнсу у iC consulenten:"):
    matches = search_index(prompt)
    final_prompt = build_prompt(prompt, matches)
    response = ask_gpt(final_prompt)

    # Додати до історії
    st.session_state.chat_history.append({
        "question": prompt,
        "answer": response
    })

    # Ререндер (автоматичний у chat_input, rerun не потрібен)

# Кнопка для очистки чату
if st.button("🧹 Очистити чат"):
    st.session_state.chat_history = []
    st.rerun()
