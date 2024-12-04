import streamlit as st
import pandas as pd
from utils import get_street_data, afficher_infos_voie, get_parking_data, afficher_infos_parking, get_toilets_data, afficher_infos_toilets, get_museum_data, afficher_infos_museum

# Adding custom styles
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

# Main title and subtitle
st.markdown('<h1 class="main-title">🌟 AroundMe</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title">Explore Paris streets and nearby amenities</h2>', unsafe_allow_html=True)

# Session state initialization
if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

# Create columns for aligning the search bar and button
col1, col2 = st.columns([4, 1])  # Adjust column proportions
with col1:
    user_input = st.text_input("🔍 Enter a street name:", placeholder="Example: Champs-Élysées")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add spacing for vertical alignment
    search = st.button("Search")

# Search management
if search:
    if user_input.strip():
        parking_data = pd.DataFrame()
        street_data, suggestion = get_street_data(user_input)
        st.session_state.current_input = user_input
        st.session_state.suggestion = suggestion

        if street_data is not None:            
            st.success(f"✅ Results for *{user_input}*:")
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            parking_data = get_parking_data(user_input, arrondissement)
            toilets_data = get_toilets_data(user_input, arrondissement)
            museum_data = get_museum_data(user_input, arrondissement)

            # Display results in tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                "📜 Street Details",
                "🚗 Nearby Parking",
                "🚻 Nearby Toilets",
                "🏛️ Nearby Museums"
            ])

            with tab1:
                st.markdown("### Street Details")
                afficher_infos_voie(street_data)
            with tab2:
                st.markdown("### Nearby Parking")
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.info("🚫 No nearby parking found.")
            with tab3:
                st.markdown("### Nearby Toilets")
                if not toilets_data.empty:
                    afficher_infos_toilets(toilets_data)
                else:
                    st.info("🚫 No nearby toilets found.")
            with tab4:
                st.markdown("### Nearby Museums")
                if not museum_data.empty:
                    afficher_infos_museum(museum_data)
                else:
                    st.info("🚫 No nearby museums found.")
    else:
        st.error("❌ Please enter a street name to start the search.")

# Suggestion management
if st.session_state.suggestion:
    if st.button(f"💡 Suggestion: Try with '{st.session_state.suggestion}'"):
        parking_data = pd.DataFrame()
        street_data, suggestion = get_street_data(st.session_state.suggestion)

        if street_data is not None:
            arrondissement = str(street_data["arrdt"].values[0]).replace("e", "")
            museum_data = get_museum_data(st.session_state.suggestion, arrondissement)
            parking_data = get_parking_data(st.session_state.suggestion, arrondissement)
            toilets_data = get_toilets_data(st.session_state.suggestion, arrondissement)

            st.success(f"✅ Results for *{st.session_state.suggestion}*:")
            tab1, tab2, tab3, tab4 = st.tabs([
                "📜 Street Details",
                "🚗 Nearby Parking",
                "🚻 Nearby Toilets",
                "🏛️ Nearby Museums"
            ])
            with tab1:
                st.markdown("### Street Details")
                afficher_infos_voie(street_data)
            with tab2:
                st.markdown("### Nearby Parking")
                if not parking_data.empty:
                    afficher_infos_parking(parking_data)
                else:
                    st.info("🚫 No nearby parking found.")            
            with tab3:
                st.markdown("### Nearby Toilets")
                if not toilets_data.empty:
                    afficher_infos_toilets(toilets_data)
                else:
                    st.info("🚫 No nearby toilets found.")
            with tab4:
                st.markdown("### Nearby Museums")
                if not museum_data.empty:
                    afficher_infos_museum(museum_data)
                else:
                    st.info("🚫 No nearby museums found.")
                    
# Footer
st.markdown('<div class="footer"><p>Powered by AroundMe - Explore Paris, One Street at a Time</p></div>', unsafe_allow_html=True)