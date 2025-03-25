
import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("Prix de Vins par Région - iDealwine (version stable)")

REGIONS = {
    "Bordeaux": "bordeaux",
    "Bourgogne": "bourgogne",
    "Rhône": "rhone"
}

def get_wines_from_region(region_code):
    url = f"https://www.idealwine.com/fr/achat-vin-par-regions.jsp?region={region_code}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        wines = []
        rows = soup.select("div.vin")

        for wine in rows[:10]:  # Limiter à 10 résultats
            title = wine.select_one("span.nom")
            price = wine.select_one("span.prix")
            if title and price:
                wines.append({
                    "vin": title.get_text(strip=True),
                    "prix": price.get_text(strip=True)
                })

        return wines if wines else [{"vin": "Aucun vin trouvé", "prix": "-"}]
    except Exception as e:
        return [{"vin": "Erreur de connexion", "prix": str(e)}]

# Interface utilisateur
region_choice = st.selectbox("Choisis une région :", list(REGIONS.keys()))

if region_choice:
    region_code = REGIONS[region_choice]
    st.write(f"Résultats pour la région : {region_choice}")
    results = get_wines_from_region(region_code)
    for result in results:
        st.write(f"**{result['vin']}** : {result['prix']}")
