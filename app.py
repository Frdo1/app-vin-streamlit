import streamlit as st
from PIL import Image
import pytesseract

# Chemin Tesseract pour Streamlit Cloud
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.title("📷 OCR avec Appareil Photo (Anglais + Français)")

# Capture d'image via webcam
camera_image = st.camera_input("Prendre une photo")

if camera_image is not None:
    # Lire l'image
    image = Image.open(camera_image)
    st.image(image, caption="Image capturée", use_column_width=True)

    with st.spinner("🧠 OCR en cours..."):
        # OCR avec anglais + français
        text = pytesseract.image_to_string(image, lang="eng+fra")
    
    st.subheader("📝 Texte détecté :")
    st.text_area("", text, height=300)
