import streamlit as st

st.set_page_config(page_title="AI for construction projects", page_icon="🏗️")

st.title("AI for construction projects")
st.write("Utilize artificial intelligence to assist with the planning, management, and optimization of construction projects.")

st.markdown("## Виберіть помічника:")

if st.button("📄 Асистент по комплаєнсу iC consulenten"):
    st.markdown("[Перейти до Асистента по комплаєнсу](./app_compliance)")

if st.button("📑 Асистент по закупівлям НЕФКО"):
    st.markdown("[Перейти до Асистента по закупівлям](./app_procurement)")
