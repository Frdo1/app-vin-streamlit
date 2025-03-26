
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import difflib
import requests

# Définir le chemin de tesseract pour Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.set_page_config(page_title="Wine OCR Search", layout="centered")
st.title("🍷 Scanner de vin avec OCR + Recherche")

# API Snooth (à configurer avec ta clé)
API_KEY = "TA_CLE_API_ICI"

# Capture d'image via webcam
image_data = st.camera_input("📸 Prends une photo de l'étiquette")

# Charger base de données locale
@st.cache_data
def load_data():
    return pd.read_csv("wines.csv")

df = load_data()

def rechercher_localement(texte_ocr, base):
    noms = base["Nom"].tolist()
    correspondance = difflib.get_close_matches(texte_ocr, noms, n=1, cutoff=0.4)
    if correspondance:
        return base[base["Nom"] == correspondance[0]]
    return pd.DataFrame()

def rechercher_sur_snooth(nom_vin, api_key):
    url = "https://api.snooth.com/wines/"
    params = {
        "akey": api_key,
        "q": nom_vin,
        "n": 1
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if "wines" in data and len(data["wines"]) > 0:
            return data["wines"][0]
    return None

if image_data is not None:
    image = Image.open(image_data)
    st.image(image, caption="📷 Image capturée", use_column_width=True)

    with st.spinner("🔍 Lecture de l'étiquette..."):
        texte = pytesseract.image_to_string(image, lang="eng+fra")
    
    st.subheader("📝 Texte extrait :")
    st.text_area("Texte OCR brut", texte, height=200)

    result = rechercher_localement(texte, df)

    if not result.empty:
        st.success("🍇 Vin trouvé dans la base locale !")
        st.dataframe(result)
    else:
        st.info("🔎 Recherche dans la base en ligne...")
        vin_info = rechercher_sur_snooth(texte, API_KEY)

        if vin_info:
            st.success("🌍 Vin trouvé sur Snooth !")
            st.write(f"**Nom** : {vin_info['name']}")
            st.write(f"**Appellation** : {vin_info['region']}")
            st.write(f"**Cépage** : {vin_info.get('varietal', 'Non précisé')}")
            st.write(f"**Prix moyen** : {vin_info.get('price', 'N/A')} USD")
            st.image(vin_info['image'], width=200)
        else:
            st.warning("❌ Aucun résultat trouvé sur Snooth.")
