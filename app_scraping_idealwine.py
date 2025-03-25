
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Recherche de prix de vins - iDealwine")

def get_idealwine_price(wine_name):
    query = wine_name.replace(" ", "+")
    url = f"https://www.idealwine.com/fr/recherche/vin?searchValue={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        price_div = soup.select_one("div.result-item-price")
        if price_div:
            return price_div.get_text(strip=True)
        else:
            return "Prix non trouvé"
    except:
        return "Erreur de connexion"

# Interface utilisateur
wine_input = st.text_input("Entrez le nom du vin (ex: Château Margaux 2015)")

if wine_input:
    st.write("Recherche en cours...")
    price = get_idealwine_price(wine_input)
    st.success(f"Prix trouvé pour '{wine_input}' : {price}")
