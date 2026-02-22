import streamlit as st
import json
from streamlit_lottie import st_lottie

from services.auth import init_users, login
from services.search_engine import get_live_products
from services.history_store import (
    init_db,
    save_search,
    get_history,
    clear_history
)
from services.llm_engine import get_ecommerce_agent
from ui.product_card import render_product_card


# ---------------- Lottie Loader ----------------
def load_lottie(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="ShopSmart AI",
    page_icon="🛍️",
    layout="wide"
)

init_users()
init_db()

user = login()
if not user:
    st.stop()


# ---------------- Sidebar ----------------
with st.sidebar:
    st.header("🛍️ ShopSmart AI")

    query = st.text_input(
        "Product Name",
        value=st.session_state.get("query", "")
    )

    limit = st.selectbox("Results", [10, 15, 20])
    search_btn = st.button("Find Best Deal")

    st.divider()
    st.subheader("🕘 History")

    history = get_history(user)
    for i, q in enumerate(history):
        if st.button(q, key=f"h_{i}"):
            st.session_state["query"] = q
            st.rerun()

    if st.button("🗑 Clear History"):
        clear_history(user)
        st.rerun()


# ---------------- Main ----------------
st.title("🛍️ AI E-Commerce Assistant")

# ================= AI ANIMATION (TOP) =================
if search_btn and query:
    st.subheader("🧠 AI Market Analysis")

    with st.container():
        lottie_ai = load_lottie("assets/ai_analysis.json")
        st_lottie(
            lottie_ai,
            speed=1,
            loop=True,
            height=220
        )
        st.caption(
            "Analyzing live market data, understanding product context, "
            "and preparing intelligent recommendations…"
        )

# ================= SEARCH LOGIC =================
if search_btn and query:

    data = get_live_products(query, limit)
    results = data.get("shopping", [])

    if results:
        def p(x):
            try:
                return float(str(x).replace("₹", "").replace(",", ""))
            except:
                return None

        save_search(
            user,
            query,
            p(results[0].get("price")),
            results[0].get("source")
        )

    # -------- AI Recommendation --------
    st.subheader("🤖 AI Recommendation")

    agent = get_ecommerce_agent()
    ai_text, accessories = agent.run(query, results)
    st.markdown(ai_text)

    # -------- Main Products --------
    st.divider()
    st.subheader("🔍 Live Market Data")

    cols = st.columns(3)
    for i, item in enumerate(results):
        with cols[i % 3]:
            render_product_card(
                title=item.get("title"),
                price=item.get("price"),
                source=item.get("source"),
                image_url=item.get("imageUrl"),
                link=item.get("link")
            )

    # -------- Recommended Add-ons --------
    st.divider()
    st.subheader("🎒 Recommended Add-ons")

    add_cols = st.columns(5)

    for i, acc in enumerate(accessories):
        with add_cols[i]:
            acc_data = get_live_products(acc, limit=1)
            acc_items = acc_data.get("shopping", [])

            if acc_items:
                a = acc_items[0]
                render_product_card(
                    title=a.get("title"),
                    price=a.get("price"),
                    source=a.get("source"),
                    image_url=a.get("imageUrl"),
                    link=a.get("link")
                )
            else:
                st.caption("Not available")
