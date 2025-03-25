
import streamlit as st
import matplotlib.pyplot as plt

# Titre de la page
st.title("Analyse des Prix de Vins par Région")

# Sélection des régions
regions = st.multiselect("Choisis les régions à analyser :", ["Bordeaux", "Bourgogne", "Rhône"])

# Liste de vins fictifs pour chaque région
sample_wines = {
    "Bordeaux": ["Château Margaux 2015", "Pétrus 2010"],
    "Bourgogne": ["Romanée-Conti 2014", "Chambertin 2016"],
    "Rhône": ["Châteauneuf-du-Pape 2016", "Côte Rôtie 2015"]
}

# Simulation de récupération des prix
price_data = {}
for region in regions:
    price_data[region] = []
    for wine in sample_wines[region]:
        # Prix fictif (simulé, ici entre 100 et 400 €)
        price = 100 + hash(wine) % 300
        price_data[region].append(price)

# Affichage des prix récupérés
st.write("### Prix trouvés :")
for region, prices in price_data.items():
    st.write(f"**{region}** : {prices}")

# Création de l'histogramme
if price_data:
    avg_prices = {region: sum(prices)/len(prices) for region, prices in price_data.items()}
    plt.figure(figsize=(8, 5))
    plt.bar(avg_prices.keys(), avg_prices.values())
    plt.title("Prix moyen par région")
    plt.ylabel("Prix (€)")
    plt.grid(True)
    st.pyplot(plt)
else:
    st.info("Sélectionne au moins une région pour afficher les données.")
