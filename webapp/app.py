import streamlit as st
import pandas as pd
from utils import get_informations

st.title("Recherche d'informations sur une rue")

# Initialisation des variables de session
if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

# Saisie de l'utilisateur
user_input = st.text_input("Entrez une rue dans la barre de recherche :")

# Bouton de recherche
if st.button("Rechercher"):
    if user_input.strip():  # Vérifie que l'utilisateur a saisi un texte
        historique, orig, typevoie, arrdt, quartier, longueur, largeur, suggestion = get_informations(user_input)
        st.session_state.current_input = user_input  # Sauvegarde de l'entrée actuelle
        st.session_state.suggestion = suggestion    # Sauvegarde de la suggestion

        if suggestion:
            st.warning(f"Did you mean: **{suggestion}**?")

        if historique and orig:
            st.success(f"Informations sur {user_input} :")
            
            # Section Caractéristiques
            with st.expander("Voir les caractéristiques"):
                st.write(f"- **Nom historique :** {historique}")
                st.write(f"- **Nom original :** {orig}")
                st.write(f"- **Type de voie :** {typevoie}")
                st.write(f"- **Arrondissement :** {arrdt}")
                st.write(f"- **Quartier :** {quartier}")
                st.write(f"- **Longueur :** {longueur}")
                st.write(f"- **Largeur :** {largeur}")
            
            # Section Parking
            with st.expander("Parkings à proximité"):
                # Exemple de données fictives pour les parkings
                parkings = [
                    {"Nom": "Parking A", "Adresse": "123 Rue Exemple", "Places": 50},
                    {"Nom": "Parking B", "Adresse": "456 Rue Exemple", "Places": 30},
                ]
                parking_df = pd.DataFrame(parkings)
                st.table(parking_df)
        elif not suggestion:
            st.error("Aucune information trouvée pour cette rue. Veuillez vérifier votre saisie.")
    else:
        st.error("Veuillez entrer un nom de rue pour lancer la recherche.")

# Afficher la suggestion et permettre une recherche
if st.session_state.suggestion:
    if st.button(f"Rechercher la suggestion '{st.session_state.suggestion}'"):
        # Recherche avec la suggestion sauvegardée
        historique, orig, typevoie, arrdt, quartier, longueur, largeur, _ = get_informations(st.session_state.suggestion)
        if historique and orig:
            st.success(f"Informations sur {st.session_state.suggestion} :")
            
            # Section Caractéristiques
            with st.expander("Voir les caractéristiques"):
                st.write(f"- **Nom historique :** {historique}")
                st.write(f"- **Nom original :** {orig}")
                st.write(f"- **Type de voie :** {typevoie}")
                st.write(f"- **Arrondissement :** {arrdt}")
                st.write(f"- **Quartier :** {quartier}")
                st.write(f"- **Longueur :** {longueur}")
                st.write(f"- **Largeur :** {largeur}")
            
            # Section Parking
            with st.expander("Parkings à proximité"):
                # Exemple de données fictives pour les parkings
                parkings = [
                    {"Nom": "Parking C", "Adresse": "789 Rue Exemple", "Places": 40},
                    {"Nom": "Parking D", "Adresse": "321 Rue Exemple", "Places": 20},
                ]
                parking_df = pd.DataFrame(parkings)
                st.table(parking_df)
        else:
            st.error(f"Aucune information trouvée pour '{st.session_state.suggestion}'.")
