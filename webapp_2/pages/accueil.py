import os
import streamlit as st

def main():
    # Déterminer le chemin de l'image
    current_dir = os.path.dirname(__file__)
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    image_path = os.path.join(base_dir, "assets", "paris.jpg")

    # CSS pour limiter la taille de l'image
    st.markdown("""
        <style>
        .header-image {
            max-height: 25vh; /* Limite à 25% de la hauteur de l'écran */
            object-fit: cover; /* Coupe l'image si nécessaire */
            width: 100%; /* Prend la largeur complète */
        }
        </style>
    """, unsafe_allow_html=True)

    # Afficher l'image
    if os.path.exists(image_path):
        st.markdown(f'<img src="file://{image_path}" alt="Paris Explorer" class="header-image">', unsafe_allow_html=True)
    else:
        st.warning("L'image de Paris n'a pas été trouvée.")

    # Titre principal et description
    st.title("Bienvenue sur Paris Explorer 🗼")
    st.markdown("""
    Paris Explorer est votre guide pour découvrir les rues et parkings de Paris. 
    Accédez rapidement aux informations nécessaires pour une navigation fluide dans la Ville Lumière.
    """)

    # Présentation des fonctionnalités
    st.write("### Fonctionnalités disponibles :")
    st.write("- 🌍 **Rechercher une rue** : Obtenez des informations sur les rues parisiennes.")
    st.write("- 🅿️ **Découvrir les parkings** : Trouvez les parkings proches de votre destination.")
    st.write("- ℹ️ **À propos** : Apprenez-en plus sur cette application.")
