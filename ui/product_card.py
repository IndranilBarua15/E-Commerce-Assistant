import streamlit as st

def render_product_card(title, price, source, image_url, link):
    """
    Renders a nice card for a single product.
    """
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.text("No Image")
                
        with col2:
            st.markdown(f"**{title}**")
            st.success(f"{price}")
            st.caption(f"Source: {source}")
            st.link_button("View Deal", link)