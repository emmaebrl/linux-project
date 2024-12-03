import importlib
import streamlit as st

# Configuration globale de la page
st.set_page_config(page_title="Paris Explorer", page_icon="🗼", layout="wide")

# Barre latérale pour la navigation
st.sidebar.title("Navigation 🧭")
st.sidebar.write("Explorez les différentes fonctionnalités :")

# Liste des pages disponibles
pages = {
    "Accueil": "pages.accueil",
    "Recherche de rues": "pages.recherche_rues",
    "À propos": "pages.a_propos",
}

# Sélection de la page
selected_page = st.sidebar.selectbox("Pages disponibles", list(pages.keys()))

# Chargement dynamique de la page sélectionnée
module_name = pages[selected_page]
module = importlib.import_module(module_name)
module.main()
