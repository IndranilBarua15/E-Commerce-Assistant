import streamlit as st
import json
import os
from services.llm_engine import get_ecommerce_agent
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
    # 1. THE AI ANALYSIS (The Brain)
    st.subheader("🤖 AI Recommendation")
    
    with st.spinner("Searching live markets & Analyzing prices..."):
        try:
            # Initialize Agent
            agent = get_ecommerce_agent()
            
            # Run Logic (Get Text + Data)
            ai_response, raw_json_data = agent.run(query)
            
            # Display Clean AI Output
            st.markdown(ai_response)
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            raw_json_data = None

    # 2. THE VISUAL CARDS (The UI)
    st.divider()
    st.subheader("🔍 Live Market Data")
    
    if raw_json_data:
        try:
            # 1. Parse JSON data
            data = json.loads(raw_json_data) if isinstance(raw_json_data, str) else raw_json_data
            
            # 2. Extract results (handles list or dict format)
            if isinstance(data, dict):
                results = data.get("shopping_results", [])
            elif isinstance(data, list):
                results = data
            else:
                results = []

            if results:
                # --- HELPER: CLEAN PRICE AND FIND BEST LINK ---
                def get_numeric_price(p_str):
                    try:
                        # 1. Keep only digits and dots
                        clean_str = ''.join(c for c in str(p_str) if c.isdigit() or c == '.')
                        
                        # 2. Fix the "Extra Zeros" issue (e.g., 59000.000 -> 59000.00)
                        if '.' in clean_str:
                            parts = clean_str.split('.')
                            # Reassemble: Integer part + first 2 decimal digits only
                            clean_str = f"{parts[0]}.{parts[1][:2]}"
                            
                        return float(clean_str)
                    except:
                        return float('inf')

                # Find the actual cheapest item using the clean logic
                cheapest_item = min(results, key=lambda x: get_numeric_price(x.get("price", "999999")))
                
                # --- SAFE LINK LOGIC ---
                # Sometimes APIs return empty links. We fix that here.
                lowest_price_link = cheapest_item.get("link", "")
                if not lowest_price_link or not lowest_price_link.startswith("http"):
                    # Fallback: Create a Google Search link for the product
                    lowest_price_link = f"https://www.google.com/search?q={query.replace(' ', '+')}"

                best_source = cheapest_item.get("source", "Online")
                
                st.info(f"✨ **Best Deal Detected:** All 'View Deal' buttons below open the lowest price on **{best_source}**.")

                # 3. Render Top 3 Cards
                cols = st.columns(3)
                for i, item in enumerate(results[:3]):
                    # Clean up the Display Price (Add ₹ symbol if missing)
                    display_price = item.get("price", "N/A")
                    if display_price != "N/A" and "₹" not in display_price:
                        display_price = f"₹{display_price}"

                    with cols[i]:
                        render_product_card(
                            title=item.get("title", "Unknown Product")[:60] + "...", # Truncate long titles
                            price=display_price,
                            source=item.get("source", "Online"),
                            image_url=item.get("thumbnail", ""),
                            link=lowest_price_link 
                        )
            else:
                st.info("No specific product data found to display.")
                
        except Exception as e:
            st.error(f"Error processing visual data: {e}")