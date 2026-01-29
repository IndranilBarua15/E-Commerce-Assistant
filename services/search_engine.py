import json
from langchain_community.utilities import SerpAPIWrapper
from core.config import USE_MOCK_DATA

def get_live_products(query: str):
    """
    Fetches product data. Uses dummy data if USE_MOCK_DATA is True to save credits.
    """
    if USE_MOCK_DATA:
        # FAKE DATA for testing UI
        print(f"DEBUG: Returning MOCK data for {query}")
        return json.dumps({
            "shopping_results": [
                {
                    "title": "Mock Product - ASUS TUF Gaming F15",
                    "price": "₹54,990",
                    "source": "Amazon",
                    "thumbnail": "https://m.media-amazon.com/images/I/81nPkLHN3vL._SX679_.jpg",
                    "link": "https://amzn.in/d/0eS3NNo"
                },
                {
                    "title": "Mock Product - HP Pavilion Gaming",
                    "price": "₹56,000",
                    "source": "Flipkart",
                    "thumbnail": "https://rukminim2.flixcart.com/image/416/416/kulk9zk0/computer/f/t/w/15-ec2075ax-gaming-laptop-hp-original-imag7nyzhxqc7xhh.jpeg?q=70&crop=false",
                    "link": "HP Pavilion Gaming AMD Ryzen 5 Hexa Core AMD R5-5600H - (8 GB/512 GB SSD/Windows 11 Home/4 GB Graphics/NVIDIA GeForce GTX 1650) 15-EC2150AX Gaming Laptop. Here's the link http://dl.flipkart.com/dl/hp-pavilion-gaming-amd-ryzen-5-hexa-core-r5-5600h-8-gb-512-gb-ssd-windows-11-home-4-graphics-nvidia-geforce-gtx-1650-15-ec2150ax-laptop/p/itm9d7271fc0c157?pid=COMG92FX6AVCM4UF&marketplace=FLIPKART&cmpid=product.share.pp&lid=LSTCOMG92FX6AVCM4UFN1OAM9"
                },
                {
                    "title": "Mock Product - Acer Nitro 5",
                    "price": "₹53,500",
                    "source": "Croma",
                    "thumbnail": "https://m.media-amazon.com/images/I/81Icsks9xKL._AC_UY218_.jpg",
                    "link": "https://croma.com"
                }
            ]
        })
    else:
        # REAL API CALL
        search = SerpAPIWrapper(params={
            "engine": "google_shopping",
            "gl": "in", 
            "hl": "en"
        })
        return search.run(query)