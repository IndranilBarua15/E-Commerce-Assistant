import streamlit as st
from services.history_store import get_history




def render_sidebar(user):
st.sidebar.header("🛍️ ShopSmart AI")


query = st.sidebar.text_input("Product Name")
limit = st.sidebar.selectbox("Results", [10, 15, 20])
search = st.sidebar.button("Search", type="primary")


st.sidebar.divider()
st.sidebar.subheader("🕘 History")


selected = None
for q in get_history(user):
if st.sidebar.button(q):
selected = q


return selected or query, limit, search