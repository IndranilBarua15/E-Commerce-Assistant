import streamlit as st

def render_product_card(title, price, source, image_url, link):
    with st.container(border=True):
        col1, col2 = st.columns([1, 2])

        with col1:
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.caption("No image available")

        with col2:
            st.markdown(f"**{title}**")
            st.success(price)
            st.caption(f"Source: {source}")
            if link:
                st.link_button("View Deal", link)
