import streamlit as st

def render_sidebar():
    """
    Renders the sidebar and returns the user inputs.
    """
    st.sidebar.header("🛍️ ShopSmart AI")
    
    # Input
    query = st.sidebar.text_input("Product Name", placeholder="e.g. iPhone 15")
    
    # Filters
    budget = st.sidebar.slider("Max Budget (₹)", 1000, 200000, 50000)
    
    search_btn = st.sidebar.button("Find Best Deal", type="primary")
    
    st.sidebar.divider()
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This AI Assistant compares prices across Amazon, Flipkart, "
        "and others to find you the best deal."
    )
    
    return query, search_btn