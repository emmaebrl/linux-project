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
        st.markdown(f'<img src="file://{image_path}" alt="À propos" class="header-image">', unsafe_allow_html=True)
    else:
        st.warning("L'image de Paris n'a pas été trouvée.")

    # Contenu principal
    st.title("À propos de Paris Explorer 🗼")
    st.markdown("""
    Paris Explorer est une application dédiée à simplifier la navigation dans Paris et à localiser les parkings à proximité.
    """)

    st.write("### Créateurs :")
    st.write("- 🧑‍💻 Développeur principal : **Votre Nom**")
    st.write("- 📧 Contact : [votre.email@example.com](mailto:votre.email@example.com)")
