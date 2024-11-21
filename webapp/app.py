import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from utils import get_informations

st.title("Recherche d'informations sur une rue")

if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

# Saisie de l'utilisateur
user_input = st.text_input("Entrez une rue dans la barre de recherche :")

# Bouton de recherche
if st.button("Rechercher"):
    if user_input.strip():  # Vérifie que l'utilisateur a saisi un texte
        historique, orig, typevoie, arrdt, quartier, longueur, largeur, suggestion, parking_data = get_informations(user_input)
        st.session_state.current_input = user_input  # Sauvegarde de l'entrée actuelle
        st.session_state.suggestion = suggestion    # Sauvegarde de la suggestion

        if suggestion:
            st.warning(f"Did you mean: **{suggestion}**?")

        if historique and orig:
            st.success(f"Informations sur {user_input} :")
            
            with st.expander("Voir les caractéristiques"):
                st.write(f"- **Nom historique :** {historique}")
                st.write(f"- **Nom original :** {orig}")
                st.write(f"- **Type de voie :** {typevoie}")
                st.write(f"- **Arrondissement :** {arrdt}")
                st.write(f"- **Quartier :** {quartier}")
                st.write(f"- **Longueur :** {longueur}")
                st.write(f"- **Largeur :** {largeur}")
            
            # Menu déroulant pour la map du Parking
            with st.expander("Parkings à proximité"):
                if not parking_data.empty:
                    localisation = [parking_data.iloc[0]['Ylat'], parking_data.iloc[0]['Xlong']]
                    m = folium.Map(location=localisation, zoom_start=15)
                    
                    for _, row in parking_data.iterrows():
                        # Information affichée dans la pop-up en HTML
                        popup_content = f"""
                            <b>Tarif 1h:</b> {row['tarif_1h']} €<br>
                            <b>Hauteur max:</b> {row['hauteur_max']} cm
                            """
                        # Forme du Marker
                        folium.Marker(
                            location=[row['Ylat'], row['Xlong']],
                            popup=folium.Popup(popup_content),
                            tooltip=row['adresse']
                        ).add_to(m)
                    
                    folium_static(m)
                else:
                    st.write("Aucun parking trouvé à proximité.")
        elif not suggestion:
            st.error("Aucune information trouvée pour cette rue. Veuillez vérifier votre saisie.")
    else:
        st.error("Veuillez entrer un nom de rue pour lancer la recherche.")

# Afficher la suggestion et permettre une recherche
if st.session_state.suggestion:
    if st.button(f"Rechercher la suggestion '{st.session_state.suggestion}'"):
        # Recherche avec la suggestion sauvegardée
        historique, orig, typevoie, arrdt, quartier, longueur, largeur, _, parking_data = get_informations(st.session_state.suggestion)
        if historique and orig:
            st.success(f"Informations sur {st.session_state.suggestion} :")
            
            with st.expander("Voir les caractéristiques"):
                st.write(f"- **Nom historique :** {historique}")
                st.write(f"- **Nom original :** {orig}")
                st.write(f"- **Type de voie :** {typevoie}")
                st.write(f"- **Arrondissement :** {arrdt}")
                st.write(f"- **Quartier :** {quartier}")
                st.write(f"- **Longueur :** {longueur}")
                st.write(f"- **Largeur :** {largeur}")
            
            with st.expander("Parkings à proximité"):
                if not parking_data.empty:
                    map_center = [parking_data.iloc[0]['Ylat'], parking_data.iloc[0]['Xlong']]
                    m = folium.Map(location=map_center, zoom_start=15)
                    
                    for _, row in parking_data.iterrows():
                        popup_content = f"""
                            <b>Tarif 1h:</b> {row['tarif_1h']} €<br>
                            <b>Hauteur max:</b> {row['hauteur_max']} cm
                            """
                        folium.Marker(
                            location=[row['Ylat'], row['Xlong']],
                            popup=folium.Popup(popup_content),
                            tooltip=row['adresse']
                        ).add_to(m)
                    
                    folium_static(m)
                else:
                    st.write("Aucun parking trouvé à proximité.")
        else:
            st.error(f"Aucune information trouvée pour '{st.session_state.suggestion}'.")