
import requests
from bs4 import BeautifulSoup
import urllib.parse

def chercher_vin_vivino(nom_vin):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # Encodage du nom pour l'URL de recherche
    query = urllib.parse.quote(nom_vin)
    search_url = f"https://www.vivino.com/search/wines?q={query}"

    search_response = requests.get(search_url, headers=headers)
    if search_response.status_code != 200:
        return None

    soup = BeautifulSoup(search_response.text, "html.parser")
    
    # Recherche du premier résultat de vin
    script_tags = soup.find_all("script", type="application/ld+json")
    for tag in script_tags:
        try:
            import json
            data = json.loads(tag.string)
            if isinstance(data, dict) and data.get("@type") == "Product":
                return {
                    "nom": data.get("name"),
                    "note": data.get("aggregateRating", {}).get("ratingValue"),
                    "prix": data.get("offers", {}).get("price"),
                    "image": data.get("image")
                }
        except Exception:
            continue

    return None
