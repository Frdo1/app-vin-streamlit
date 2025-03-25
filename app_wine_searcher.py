
import streamlit as st
import urllib.parse

st.title("Recherche de vins sur Wine-Searcher")

st.write("""
Tape un nom de vin pour accéder directement à sa fiche sur [Wine-Searcher](https://www.wine-searcher.com).
Exemples : `Château Margaux 2015`, `Romanée-Conti 2014`, `Châteauneuf-du-Pape 2016`
""")

# Entrée utilisateur
wine_input = st.text_input("Nom du vin à rechercher", "")

if wine_input:
    # Encodage du nom pour l'URL
    query = urllib.parse.quote_plus(wine_input)
    search_url = f"https://www.wine-searcher.com/find/{query}"

    st.markdown(f"🔍 [Voir les prix de **{wine_input}** sur Wine-Searcher]({search_url})", unsafe_allow_html=True)
    st.markdown(f"🌐 URL directe : `{search_url}`")
