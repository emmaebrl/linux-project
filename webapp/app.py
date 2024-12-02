import streamlit as st
import pandas as pd
from utils import get_street_data, afficher_infos_voie, get_parking_data, afficher_infos_parking

st.title("Nom de l'application")

# Initialiser les variables dans la session
if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

user_input = st.text_input("Entrez une rue dans la barre de recherche :")

if st.button("Rechercher"):
    if user_input.strip():
        parking_data = pd.DataFrame()
        street_data, suggestion = get_street_data(user_input)
        st.session_state.current_input = user_input
        st.session_state.suggestion = suggestion

        if suggestion:
            st.warning(f"Did you mean: **{suggestion}**?")

        if street_data is not None:
            st.success(f"Informations sur {user_input} :")
            
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            parking_data = get_parking_data(user_input, arrondissement)

            tab1, tab2 = st.tabs(["Caractéristiques", "Parkings à proximité"])
            with tab1:
                afficher_infos_voie(street_data)

            with tab2:
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.write("Aucun parking trouvé à proximité.")
        else:
            st.error(f"Aucune information trouvée pour '{user_input}'.")
    else:
        st.error("Veuillez entrer un nom de rue pour lancer la recherche.")

# Gestion des suggestions
if st.session_state.suggestion:
    if st.button(f"Rechercher la suggestion '{st.session_state.suggestion}'"):
        # Initialiser parking_data
        parking_data = pd.DataFrame()

        street_data, suggestion = get_street_data(st.session_state.suggestion)
        if street_data is not None:
   
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            parking_data = get_parking_data(suggestion, arrondissement)
            st.success(f"Informations sur {st.session_state.suggestion} :")
            tab1, tab2 = st.tabs(["Caractéristiques", "Parkings à proximité"])
            with tab1:
                afficher_infos_voie(street_data)

            with tab2:
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.write("Aucun parking trouvé à proximité.")
        else:
            st.error(f"Aucune information trouvée pour '{st.session_state.suggestion}'.")
