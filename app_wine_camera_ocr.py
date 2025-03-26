
import streamlit as st
from PIL import Image
import pytesseract
import urllib.parse

st.title("Scanner une bouteille de vin 🍷📸")

st.write("""
Prends une photo de l'étiquette de la bouteille et découvre automatiquement les informations grâce à l'OCR,
puis accède aux prix sur [Wine-Searcher](https://www.wine-searcher.com).
""")

# Étape 1 : Photo depuis la caméra
image_file = st.camera_input("Prends une photo de l'étiquette")

if image_file:
    # Étape 2 : Lire l'image et appliquer OCR
    image = Image.open(image_file)
    st.image(image, caption="Image capturée", use_column_width=True)

    st.write("🔍 Lecture du texte avec OCR...")
    extracted_text = pytesseract.image_to_string(image, lang="eng+fra")

    if extracted_text.strip():
        st.success("Texte détecté :")
        st.code(extracted_text)

        # Étape 3 : Générer le lien vers Wine-Searcher
        query = urllib.parse.quote_plus(extracted_text.strip())
        search_url = f"https://www.wine-searcher.com/find/{query}"
        st.markdown(f"🔗 [Voir sur Wine-Searcher]({search_url})", unsafe_allow_html=True)
    else:
        st.warning("Aucun texte lisible n'a été détecté sur l'image.")
