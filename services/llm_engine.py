from google import genai
from services.search_engine import get_live_products
from core.config import GOOGLE_API_KEY

class CustomEcommerceAgent:
    def __init__(self):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model_name = "gemini-3-flash-preview" 

    def run(self, query):
        """
        Returns: 
        1. recommendation_text (str)
        2. main_raw_data (json/str)
        3. accessory_list (list of strings, e.g. ["Laptop Bag", "Wireless Mouse"])
        """
        # 1. Fetch MAIN product data
        try:
            raw_data = get_live_products(query)
        except Exception as e:
            raw_data = f"Error fetching data: {str(e)}"

        # 2. Prompt with Strict Separation for Accessories
        prompt = f"""
        You are an expert Shopping Assistant.
        
        USER REQUEST: {query}
        MARKET DATA: {raw_data}
        
        INSTRUCTIONS:
        1. Analyze the market data and provide a recommendation.
        2. Identify exactly 2 related accessories that go with this product.
           (e.g. if Laptop -> "Laptop Bag", "Wireless Mouse")
        
        STRICT OUTPUT FORMAT:
        Write your recommendation text first.
        Then, end your response with exactly this line:
        ---ACCESSORIES---
        Followed by the 2 accessory names separated by a comma.
        
        Example End of Response:
        ...so option A is the best choice.
        ---ACCESSORIES---
        Laptop Backpack, Wireless Gaming Mouse
        """

        # 3. Call Gemini
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            full_text = response.text
            
            # 4. PARSING LOGIC (Mind Separation)
            # We split the text to separate the "Advice" from the "Data"
            if "---ACCESSORIES---" in full_text:
                parts = full_text.split("---ACCESSORIES---")
                recommendation = parts[0].strip()
                # Create a clean list: ["Backpack", "Mouse"]
                accessories_text = parts[1].strip()
                accessory_list = [item.strip() for item in accessories_text.split(",")]
            else:
                recommendation = full_text
                accessory_list = []
                
        except Exception as e:
            recommendation = f"Gemini Error: {str(e)}"
            accessory_list = []
        
        return recommendation, raw_data, accessory_list

def get_ecommerce_agent():
    return CustomEcommerceAgent()