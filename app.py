import streamlit as st
from main import search_index, build_prompt, ask_gpt

st.set_page_config(page_title="Асистент по комплаєнсу", page_icon="📄")

st.title("📄 Асистент по комплаєнсу iC consulenten")
st.caption("(Compliance Assistant)")
st.markdown("💬 **Введіть свій запит, щодо проходження комплаєнсу у iC consulenten:**")

# Ініціалізація історії чату
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.text_input("🧠 Що вас цікавить?", placeholder="Введіть запит тут...")

if st.button("Запитати") and query:
    with st.spinner("🔍 Шукаю відповідь..."):
        matches = search_index(query)
        prompt = build_prompt(query, matches)
        response = ask_gpt(prompt)

        # Зберігаємо у історію
        st.session_state.chat_history.append({"question": query, "answer": response})

# Відображаємо історію діалогу
for item in st.session_state.chat_history:
    with st.chat_message("🧑‍💼 Користувач"):
        st.markdown(item["question"])
    with st.chat_message("🤖 Асистент"):
        st.success(item["answer"])

