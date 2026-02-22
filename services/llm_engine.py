import re
from collections import Counter


class EcommerceAgent:
    def __init__(self):
        pass

    # ---------------------------------------------
    # Extract meaningful keywords from product titles
    # ---------------------------------------------
    def _extract_keywords(self, titles):
        words = []

        for title in titles:
            t = title.lower()
            t = re.sub(r"[^a-z0-9 ]", " ", t)
            words.extend(t.split())

        stopwords = {
            "with", "and", "for", "the", "new", "latest",
            "pack", "combo", "set", "buy", "best", "offer",
            "online", "price", "from", "by", "of", "in",
            "mah", "fast", "charging", "usb"
        }

        return [w for w in words if w not in stopwords and len(w) > 3]

    # ---------------------------------------------
    # FIXED: Derive add-ons WITHOUT category drift
    # ---------------------------------------------
    def _derive_addons(self, query, products):
        titles = [p.get("title", "") for p in products[:10]]

        keywords = self._extract_keywords(titles)
        freq = Counter(keywords)

        # Take only secondary terms (not replacing the base query)
        secondary_terms = [
            w for w, _ in freq.most_common(10)
            if w not in query.lower()
        ]

        addons = []

        for term in secondary_terms:
            addons.append(f"{query} {term}")
            if len(addons) == 5:
                break

        # Fallback if still less than 5
        while len(addons) < 5:
            addons.append(f"{query} accessories")

        return addons

    # ---------------------------------------------
    # Main entry
    # ---------------------------------------------
    def run(self, query, products):
        if not products:
            return "No products found to analyze.", []

        def price(p):
            try:
                return float(str(p.get("price", "")).replace("₹", "").replace(",", ""))
            except:
                return float("inf")

        best = min(products, key=price)

        ai_text = (
            f"Based on the current market data, **{best.get('title')}** "
            f"from **{best.get('source')}** at **₹{best.get('price')}** "
            f"appears to be the most suitable option among the available listings."
        )

        # 🔒 FIXED ADD-ONS
        accessories = self._derive_addons(query, products)

        return ai_text, accessories


def get_ecommerce_agent():
    return EcommerceAgent()
