
import streamlit as st
from PIL import Image
import pytesseract
import pandas as pd
import difflib

# Définir le chemin de tesseract pour Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.set_page_config(page_title="Wine OCR Search", layout="centered")
st.title("🍷 Scanner de vin avec OCR + Recherche")

# Capture d'image via webcam
image_data = st.camera_input("📸 Prends une photo de l'étiquette")

# Charger base de données locale
@st.cache_data
def load_data():
    return pd.read_csv("wines.csv")

df = load_data()

def rechercher_vin(texte_ocr, base):
    noms = base["Nom"].tolist()
    correspondance = difflib.get_close_matches(texte_ocr, noms, n=1, cutoff=0.4)
    if correspondance:
        return base[base["Nom"] == correspondance[0]]
    return pd.DataFrame()

if image_data is not None:
    image = Image.open(image_data)
    st.image(image, caption="📷 Image capturée", use_column_width=True)

    with st.spinner("🔍 Lecture de l'étiquette..."):
        texte = pytesseract.image_to_string(image, lang="eng+fra")
    
    st.subheader("📝 Texte extrait :")
    st.text_area("Texte OCR brut", texte, height=200)

    result = rechercher_vin(texte, df)

    if not result.empty:
        st.success("🍇 Vin trouvé !")
        st.dataframe(result)
    else:
        st.warning("Aucun vin trouvé dans la base.")
