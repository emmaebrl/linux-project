import streamlit as st
import pandas as pd
from utils import get_street_data, afficher_infos_voie, get_parking_data, afficher_infos_parking

# Ajout des styles personnalisés
st.markdown("""
    <style>
    body {
        background-color: #f4f4f9;
    }
    .main-title {
        font-size: 40px;
        color: #4CAF50;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .sub-title {
        font-size: 24px;
        color: #2196F3;
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
        color: white;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4CAF50;
        color: white;
        text-align: center;
        padding: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal et sous-titre
st.markdown('<h1 class="main-title">🌍 Recherche de rues et parkings 🚗</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title">Trouvez des informations rapidement et efficacement</h2>', unsafe_allow_html=True)

# Initialisation des variables de session
if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

# Création de colonnes pour aligner la barre de recherche et le bouton
col1, col2 = st.columns([4, 1])  # Ajustez les proportions des colonnes
with col1:
    user_input = st.text_input("🔍 Entrez une rue :", placeholder="Exemple : Champs-Élysées")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Ajouter un espace pour aligner verticalement
    rechercher = st.button("Rechercher")

# Gestion de la recherche
if rechercher:
    if user_input.strip():
        parking_data = pd.DataFrame()
        street_data, suggestion = get_street_data(user_input)
        st.session_state.current_input = user_input
        st.session_state.suggestion = suggestion

        if suggestion:
            st.warning(f"💡 **Suggestion :** Essayez avec **{suggestion}**.")

        if street_data is not None:
            st.success(f"✅ Résultats pour **{user_input}** :")
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            parking_data = get_parking_data(user_input, arrondissement)

            # Affichage des résultats dans des onglets
            tab1, tab2 = st.tabs(["📄 Détails sur la rue", "🅿️ Parkings à proximité"])
            with tab1:
                afficher_infos_voie(street_data)
            with tab2:
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.info("🛑 Aucun parking trouvé à proximité.")
        else:
            st.error(f"❌ Aucune information trouvée pour **{user_input}**.")
    else:
        st.error("❌ Veuillez entrer un nom de rue pour lancer la recherche.")

# Gestion des suggestions
if st.session_state.suggestion:
    if st.button(f"🔄 Rechercher la suggestion '{st.session_state.suggestion}'"):
        parking_data = pd.DataFrame()
        street_data, suggestion = get_street_data(st.session_state.suggestion)

        if street_data is not None:
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            parking_data = get_parking_data(st.session_state.suggestion, arrondissement)

            st.success(f"✅ Résultats pour **{st.session_state.suggestion}** :")
            tab1, tab2 = st.tabs(["📄 Détails sur la rue", "🅿️ Parkings à proximité"])
            with tab1:
                afficher_infos_voie(street_data)
            with tab2:
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.info("🛑 Aucun parking trouvé à proximité.")
        else:
            st.error(f"❌ Aucune information trouvée pour **{st.session_state.suggestion}**.")

# Pied de page
st.markdown('<div class="footer"><p>Créé avec ❤️ par Sharon, Emma, Alexis et Lina - 2024</p></div>', unsafe_allow_html=True)
