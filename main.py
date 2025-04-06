import streamlit as st

st.set_page_config(page_title="AI for construction projects", page_icon="🏗️")

st.title("AI for construction projects")
st.write("Utilize artificial intelligence to assist with the planning, management, and optimization of construction projects.")

st.markdown("## Виберіть помічника:")

if st.button("📄 Асистент по комплаєнсу iC consulenten"):
    st.switch_page("app_compliance.py")

if st.button("📑 Асистент по закупівлям НЕФКО"):
    st.switch_page("app_procurement.py")