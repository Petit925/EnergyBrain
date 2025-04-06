import streamlit as st

st.set_page_config(page_title="AI for construction projects", page_icon="🏗")

st.title("AI for construction projects")
st.write("Utilize artificial intelligence to assist with the planning, management, and optimization of construction projects.")

st.markdown("### Виберіть помічника:")

st.page_link("1_compliance_assistant", label="📄 Асистент по комплаєнсу iC consulenten")
st.page_link("2_procurement_assistant", label="📑 Асистент по закупівлям НЕФКО")
