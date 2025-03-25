
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Recherche de prix de vins - iDealwine (version améliorée)")

def get_idealwine_prices(wine_name):
    query = wine_name.replace(" ", "+")
    url = f"https://www.idealwine.com/fr/recherche/vin?searchValue={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        items = soup.select("div.result-item")
        results = []

        for item in items:
            title = item.select_one("div.result-item-title")
            price = item.select_one("div.result-item-price")
            if title and price:
                results.append({
                    "vin": title.get_text(strip=True),
                    "prix": price.get_text(strip=True)
                })

        return results if results else [{"vin": "Aucun vin trouvé", "prix": "-"}]
    except Exception as e:
        return [{"vin": "Erreur de connexion", "prix": str(e)}]

# Interface utilisateur
wine_input = st.text_input("Entrez le nom du vin (ex: Château Margaux)")

if wine_input:
    st.write("Résultats de recherche :")
    results = get_idealwine_prices(wine_input)
    for result in results:
        st.write(f"**{result['vin']}** : {result['prix']}")
