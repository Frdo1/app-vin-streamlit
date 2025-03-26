import streamlit as st
from PIL import Image
import pytesseract

# For Streamlit Cloud, set the path to the tesseract binary
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

st.title("📸 OCR d'image (Anglais + Français)")

uploaded_file = st.file_uploader("Téléverse une image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Image importée", use_column_width=True)

    with st.spinner("Extraction du texte en cours..."):
        text = pytesseract.image_to_string(image, lang="eng+fra")
    
    st.subheader("📝 Texte extrait :")
    st.text_area("", text, height=300)
