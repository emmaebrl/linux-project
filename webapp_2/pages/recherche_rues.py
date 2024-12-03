import streamlit as st
from utils import get_street_data, afficher_infos_voie, get_parking_data, afficher_infos_parking

def main():
    # Titre principal
    st.title("🔍 Recherche de rues")
    st.markdown("Entrez le nom d'une rue pour obtenir des informations détaillées.")

    # Champ de saisie utilisateur
    user_input = st.text_input("Nom de la rue :", placeholder="Exemple : Champs-Élysées")

    # Recherche
    if st.button("Rechercher"):
        if user_input.strip():
            # Appels des fonctions utilitaires
            street_data, suggestion = get_street_data(user_input)
            parking_data = get_parking_data(user_input)

            # Gestion des suggestions
            if suggestion:
                st.warning(f"💡 **Suggestion** : Essayez plutôt **{suggestion}**.")

            # Résultats
            if street_data is not None:
                st.success(f"✅ Résultats pour **{user_input}** :")
                tab1, tab2 = st.tabs(["📄 Caractéristiques", "🅿️ Parkings à proximité"])
                with tab1:
                    afficher_infos_voie(street_data)
                with tab2:
                    if not parking_data.empty:
                        afficher_infos_parking(parking_data)
                    else:
                        st.info("🛑 Aucun parking trouvé à proximité.")
            else:
                st.error("❌ Aucun résultat trouvé pour cette rue.")
        else:
            st.error("❌ Veuillez entrer une rue valide.")
