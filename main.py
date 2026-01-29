import streamlit as st
import json
import os
from services.llm_engine import get_ecommerce_agent
from services.search_engine import get_live_products 
from ui.product_card import render_product_card

# Page Config
st.set_page_config(page_title="ShopSmart AI", page_icon="🛍️", layout="wide")

# Sidebar
with st.sidebar:
    st.header("🛍️ ShopSmart AI")
    st.markdown("Compare prices across Amazon, Flipkart, and more.")
    
    # Input
    query = st.text_input("Product Name", placeholder="e.g. Gaming Laptop under 60k")
    search_btn = st.button("Find Best Deal", type="primary")
    
    st.divider()
    
    # LangSmith Check
    if os.environ.get("LANGCHAIN_TRACING_V2") == "true":
        st.success("✅ LangSmith Tracing: Active")
    else:
        st.caption("Tracing Inactive")

# Main Page
st.title("🛍️ AI E-Commerce Assistant")

if search_btn and query:
    agent = get_ecommerce_agent()
    
    # --- BLOCK 1: MAIN PRODUCT ANALYSIS ---
    st.subheader("🤖 AI Recommendation")
    with st.spinner("Analyzing market data & Brainstorming accessories..."):
        try:
            # Unpack the 3 values returned by the updated Agent
            ai_response, raw_json_data, accessories = agent.run(query)
            st.markdown(ai_response)
        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")
            raw_json_data = None
            accessories = []

    # --- BLOCK 2: MAIN PRODUCT CARDS ---
    st.divider()
    st.subheader("🔍 Live Market Data")
    
    if raw_json_data:
        try:
            # Parse Data
            data = json.loads(raw_json_data) if isinstance(raw_json_data, str) else raw_json_data
            if isinstance(data, dict):
                results = data.get("shopping_results", [])
            elif isinstance(data, list):
                results = data
            else:
                results = []

            if results:
                # Helper for Price Cleaning
                def get_numeric_price(p_str):
                    try:
                        clean_str = ''.join(c for c in str(p_str) if c.isdigit() or c == '.')
                        if '.' in clean_str:
                            parts = clean_str.split('.')
                            clean_str = f"{parts[0]}.{parts[1][:2]}"
                        return float(clean_str)
                    except:
                        return float('inf')

                # Find Cheapest (For Info Box)
                cheapest_item = min(results, key=lambda x: get_numeric_price(x.get("price", "999999")))
                best_source = cheapest_item.get("source", "Online")
                st.info(f"✨ **Best Deal Detected:** Lowest price found on **{best_source}**.")

                # Render Main Cards
                cols = st.columns(3)
                for i, item in enumerate(results[:3]):
                    # Link Logic
                    individual_link = item.get("link", "")
                    if not individual_link or not str(individual_link).startswith("http"):
                        search_term = f"{item.get('title', query)} {item.get('source', '')}"
                        individual_link = f"https://www.google.com/search?q={search_term.replace(' ', '+')}"

                    display_price = item.get("price", "N/A")
                    if display_price != "N/A" and "₹" not in display_price:
                        display_price = f"₹{display_price}"

                    with cols[i]:
                        render_product_card(
                            title=item.get("title", "Unknown")[:60] + "...",
                            price=display_price,
                            source=item.get("source", "Online"),
                            image_url=item.get("thumbnail", ""),
                            link=individual_link 
                        )
            else:
                st.info("No main product data found.")
        except Exception as e:
            st.error(f"Error showing main products: {e}")

    # --- BLOCK 3: RELATED PRODUCTS (The New Section) ---
    if accessories:
        st.divider()
        st.subheader("🎒 Essential Add-ons")
        st.caption(f"Based on your search for **{query}**, we also recommend:")
        
        # Create columns dynamically based on how many accessories found
        acc_cols = st.columns(len(accessories))
        
        for i, acc_name in enumerate(accessories):
            with acc_cols[i]:
                st.markdown(f"**Searching for: {acc_name}...**")
                
                try:
                    # 1. Perform a FAST secondary search for this accessory
                    acc_raw = get_live_products(acc_name)
                    acc_data = json.loads(acc_raw) if isinstance(acc_raw, str) else acc_raw
                    
                    # 2. Extract Results
                    acc_results = acc_data.get("shopping_results", []) if isinstance(acc_data, dict) else acc_data
                    
                    if acc_results:
                        top_pick = acc_results[0] # Take the #1 result
                        
                        # 3. Render Card
                        # Logic for link fallback
                        acc_link = top_pick.get("link", "")
                        if not acc_link.startswith("http"):
                             acc_link = f"https://www.google.com/search?q={acc_name.replace(' ', '+')}"
                        
                        acc_price = top_pick.get("price", "N/A")
                        if "₹" not in acc_price: acc_price = f"₹{acc_price}"

                        render_product_card(
                            title=top_pick.get("title", acc_name)[:50] + "...",
                            price=acc_price,
                            source=top_pick.get("source", "Online"),
                            image_url=top_pick.get("thumbnail", ""),
                            link=acc_link
                        )
                    else:
                        st.warning(f"No stock found for {acc_name}")
                        
                except Exception as e:
                    st.caption(f"Could not load {acc_name}")