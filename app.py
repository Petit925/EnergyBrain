import streamlit as st

st.set_page_config(page_title="AI for construction projects", page_icon="🏗")

st.title("AI for construction projects")
st.write("Utilize artificial intelligence to assist with the planning, management, and optimization of construction projects.")

st.markdown("### Виберіть помічника:")

# Використання вбудованих page links
st.page_link("pages/1_compliance_assistant.py", label="📄 Асистент по комплаєнсу iC consulenten")
st.page_link("pages/2_procurement_assistant.py", label="📑 Асистент по закупівлям НЕФКО")
