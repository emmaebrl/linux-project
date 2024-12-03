import pandas as pd
import sys
from difflib import get_close_matches
import streamlit as st
import folium
from streamlit_folium import folium_static


DATA_PATH = "data/street_data_staged.csv"
DATA_PATH_PARKING = "data/parking_data_staged.csv"
DATA_PATH_MUSEUM = "data/museum_data_staged.csv"

data = pd.read_csv(DATA_PATH)
data_parking = pd.read_csv(DATA_PATH_PARKING)
data_museum = pd.read_csv(DATA_PATH_MUSEUM)

def get_street_data(street):
    """Retourne des informations sur une rue, avec suggestions si nécessaire."""
    research = street.strip().upper()
    if research not in data["typo"].values:
        suggestions = get_close_matches(research, data["typo"].unique(), n=1, cutoff=0.7)
        if suggestions:
            return None, suggestions[0] 
        else:
            return None, None
    data.astype('string').fillna("Information non disponible", inplace=True)
    filtered_data = data[data["typo"] == research]
    return filtered_data, None

def afficher_infos_voie(data):
    st.write(f"- **Nom historique :** {data['historique'].values[0]}")
    st.write(f"- **Nom original :** {data['orig'].values[0]}")
    st.write(f"- **Type de voie :** {data['typvoie'].values[0]}")
    st.write(f"- **Arrondissement :** {data['arrdt'].values[0]}")
    st.write(f"- **Quartier :** {data['quartier'].values[0]}")
    st.write(f"- **Longueur :** {data['longueur'].values[0]}")
    st.write(f"- **Largeur :** {data['largeur'].values[0]}")

def get_parking_data(street):
    """Retourne les parkings à proximité d'une rue."""
    parking_data = data_parking[data_parking['adresse'].str.contains(street, case=False, na=False)]
    return parking_data

def afficher_infos_parking(parking_data):
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

def get_museum_data(street):
    """Retourne les musées à proximité d'une rue."""
    museum_data = data_museum[data_museum["adresse_normalized"].str.contains(street, case=False, na=False)]
    return museum_data

def afficher_infos_museum(museum_data):
    localisation = [museum_data.iloc[0]['Ylat'], museum_data.iloc[0]['Xlong']]
    m = folium.Map(location=localisation, zoom_start=15)
    
    for _, row in museum_data.iterrows():
        # Information affichée dans la pop-up en HTML
        popup_content = f"""
            <b>Name:</b> {row['name']}<br>
            <b>Adresse:</b> {row['adresse']}<br>
            """
        # Forme du Marker
        folium.Marker(
            location=[row['Ylat'], row['Xlong']],
            popup=folium.Popup(popup_content),
            tooltip=row['nom_du_musee']
        ).add_to(m)
    
    folium_static(m)