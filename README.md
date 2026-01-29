# 🛍️ ShopSmart AI – E-Commerce Assistant  

An **AI-powered E-Commerce Assistant** that helps users compare product prices across multiple online platforms such as **Amazon, Flipkart, and more**, and intelligently recommends the **best deal** along with **essential add-on products**.

🌐 **Live Streamlit App Demo:**  
👉 https://e-commerce-assistant.streamlit.app/

---

## 🚀 Project Overview  

ShopSmart AI is built to simplify online shopping using **AI-driven analysis** and **real-time market data**.  
It enables users to make smarter purchasing decisions by showing price comparisons, deal insights, and related product recommendations in one place.

With a simple product query like *“Gaming Laptop under 60k”*, users get:
- 🤖 AI-based buying recommendations  
- 🔍 Live product listings from multiple platforms  
- 💰 Automatic best-deal detection  
- 🎒 Suggested essential accessories  

---

## 🎯 Key Features  

- **AI Recommendation Engine**  
  Leverages LangChain-powered LLMs to understand user intent and analyze product data.

- **Live Price Comparison**  
  Fetches real-time shopping results using Google Shopping via SerpAPI.

- **Best Deal Detection**  
  Identifies the lowest available price and its source automatically.

- **Accessory & Add-on Suggestions**  
  Suggests relevant complementary products based on the main search.

- **Clean & Modular Architecture**  
  Well-structured separation between UI, services, and configuration layers.

---

## 🧠 Tech Stack  

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI / LLM:** LangChain, Hugging Face  
- **Search Engine:** SerpAPI (Google Shopping)  
- **Tracing & Monitoring:** LangSmith  
- **Environment Management:** python-dotenv  

---

## 📂 File Structure  

```text
ecommerce_assistant/
│
├── .env                    # Store API Keys here (NEVER push this to GitHub)
├── .gitignore              # Ignore .env and __pycache__
├── requirements.txt        # List of libraries
├── main.py                 # Entry point (Main application)
│
├── core/                   # Configuration & Constants
│   ├── __init__.py
│   └── config.py           # Load env vars, setup API keys
│
├── services/               # Logic Layer
│   ├── __init__.py
│   ├── llm_engine.py       # Hugging Face & LangChain logic
│   └── search_engine.py    # SerpAPI (Google Shopping) logic
│
└── ui/                     # Presentation Layer
    ├── __init__.py
    ├── sidebar.py          # Sidebar components
    └── product_card.py     # Component to display a single product
## ⚙️ How the System Works  

1. **User Input** → Product name entered in the sidebar  
2. **LLM Engine** → Understands user intent and suggests accessories  
3. **Search Engine** → Fetches live shopping data from multiple platforms  
4. **AI Reasoning** → Analyzes prices and identifies the best deal  
5. **UI Layer** → Displays results using reusable product cards  

---

## 👥 Team Details  

**Team Name:** Matrix Hooligans  
**Institution:** Haldia Institute of Technology  

- Arnab Kumar Jana – **Group Captain**  
- Indranil Barua Betal  
- Alok Kumar  
- Ayan Jana  
- Bhavya Verma  

---

## 🌟 Future Enhancements  

- Personalized user accounts  
- Product review sentiment analysis  
- Wishlist and price-drop alerts 
