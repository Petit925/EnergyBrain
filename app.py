import streamlit as st

st.set_page_config(page_title="AI for construction projects", page_icon="🏗")

st.title("AI for construction projects")
st.write("Utilize artificial intelligence to assist with the planning, management, and optimization of construction projects.")

st.markdown("### Виберіть помічника:")

# Посилання на внутрішні сторінки з каталогу `pages/`
st.markdown("[📄 Асистент по комплаєнсу iC consulenten](./1_compliance_assistant)")
st.markdown("[📑 Асистент по закупівлям НЕФКО](./2_procurement_assistant)")

