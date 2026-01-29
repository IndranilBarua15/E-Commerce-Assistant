from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from services.search_engine import get_live_products
from core.config import HUGGINGFACE_TOKEN

class CustomEcommerceAgent:
    def __init__(self):
        # 1. Setup Base Endpoint
        repo_id = "HuggingFaceH4/zephyr-7b-beta"
        
        base_llm = HuggingFaceEndpoint(
            repo_id=repo_id,
            temperature=0.1,
            huggingfacehub_api_token=HUGGINGFACE_TOKEN
        )

        # 2. Wrap in ChatHuggingFace
        self.chat_model = ChatHuggingFace(llm=base_llm)

    def run(self, query):
        """
        Executes the Search -> Analyze -> Answer loop.
        """
        # Step 1: Perform the Search
        try:
            # We fetch the data here to give to the LLM
            raw_data = get_live_products(query)
        except Exception as e:
            raw_data = f"Error fetching data: {str(e)}"

        # Step 2: Define Strict Formatting Rules
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are an expert Shopping Assistant.
                    
                    STRICT FORMATTING RULES:
                    1. Start with a clear recommendation (e.g., "The best option is...").
                    2. Use **Bold** for product names and prices.
                    3. Use Bullet Points (•) to list pros/cons.
                    4. Do NOT write long paragraphs. Keep it readable.
                    5. Compare the options based on Price and Value.
                    """
                ),
                (
                    "user", 
                    """
                    SEARCH QUERY: "{query}"

                    LIVE MARKET DATA FOUND:
                    {product_data}
                    
                    Based on this data, which product should I buy? Compare them clearly.
                    """
                )
            ]
        )

        # Step 3: Run the Chain
        chain = prompt | self.chat_model | StrOutputParser()
        
        response = chain.invoke({
            "query": query,
            "product_data": raw_data
        })
        
        # We return the AI text AND the raw data (so UI can show cards)
        return response, raw_data

def get_ecommerce_agent():
    return CustomEcommerceAgent()