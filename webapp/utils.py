import pandas as pd
import sys
from difflib import get_close_matches
import streamlit as st
import folium
from streamlit_folium import folium_static


DATA_PATH = "data/street_data_staged.csv"
DATA_PATH_PARKING = "data/parking_data_staged.csv"
DATA_PATH_TOILETS = "data/toilets_data_staged.csv"
DATA_PATH_MUSEUM = "data/museum_data_staged.csv"

data = pd.read_csv(DATA_PATH)
data_parking = pd.read_csv(DATA_PATH_PARKING)
data_museum = pd.read_csv(DATA_PATH_MUSEUM)
data_toilets = pd.read_csv(DATA_PATH_TOILETS)


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

def get_parking_data(street, arrondissement=None):
    """Retourne les parkings à proximité d'une rue, éventuellement filtrés par arrondissement."""
    parking_data = pd.DataFrame()  # Initialize as empty DataFrame
    if arrondissement:
        arrondissements = arrondissement.split(",")
        arrondissements_formatted = []
        for arrondissement in arrondissements:
            if len(arrondissement) == 1:
                arrondissement = "7500" + arrondissement
            elif len(arrondissement) == 2:
                arrondissement = "750" + arrondissement
            arrondissements_formatted.append(arrondissement)
        parking_data = data_parking[data_parking['adresse'].apply(lambda x: any(arr in x for arr in arrondissements_formatted))]
    else:
        parking_data = data_parking[data_parking['adresse'].str.contains(street, case=False, na=False)]
    parking_data = parking_data.dropna(subset=['Ylat', 'Xlong'])
    return parking_data


def afficher_infos_parking(parking_data):
    if parking_data.empty:
        st.write("Aucun parking trouvé à proximité.")
        return
    
    localisation = [parking_data.iloc[0]['Ylat'], parking_data.iloc[0]['Xlong']]
    m = folium.Map(location=localisation, zoom_start=15)
    
    for _, row in parking_data.iterrows():
        if pd.isna(row['Ylat']) or pd.isna(row['Xlong']):
            continue 
        
        popup_content = f"""
            <b>Adresse:</b> {row['adresse']}<br>
            <b>Tarif 1h:</b> {row['tarif_1h']} €<br>
            <b>Hauteur max:</b> {row['hauteur_max']} cm
        """
        folium.Marker(
            location=[row['Ylat'], row['Xlong']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=row['adresse']
        ).add_to(m)
    
    folium_static(m)

def get_toilets_data(street, arrondissement=None):
    """Retourne les toilettes à proximité d'une rue, éventuellement filtrés par arrondissement."""
    toilets_data = pd.DataFrame()  # Initialize as empty DataFrame
    if arrondissement:
        arrondissements = arrondissement.split(",")
        arrondissements_formatted = []
        for arrondissement in arrondissements:
            if len(arrondissement) == 1:
                arrondissement = "7500" + arrondissement
            elif len(arrondissement) == 2:
                arrondissement = "750" + arrondissement
            arrondissements_formatted.append(arrondissement)
        data_toilets['ARRONDISSEMENT'] = data_toilets['ARRONDISSEMENT'].astype(str)

        toilets_data = data_toilets[data_toilets['ARRONDISSEMENT'].apply(lambda x: any(arr in x for arr in arrondissements_formatted))]
    else:
        toilets_data = data_toilets[data_toilets['adresse_normalized'].str.contains(street, case=False, na=False)]
    toilets_data = toilets_data.dropna(subset=['latitude', 'longitude'])
    return toilets_data


def get_museum_data(street, arrondissement=None):
    """Retourne les musées à proximité d'une rue."""
    museum_data = pd.DataFrame()
    if arrondissement:
        arrondissements = arrondissement.split(",")
        arrondissements_formatted = []
        for arrondissement in arrondissements:
            if len(arrondissement) == 1:
                arrondissement = "7500" + arrondissement
            elif len(arrondissement) == 2:
                arrondissement = "750" + arrondissement
            arrondissements_formatted.append(arrondissement)
        data_museum['c_postal'] = data_museum['c_postal'].astype(str)
        museum_data = data_museum[data_museum['c_postal'].apply(lambda x: any(arr in x for arr in arrondissements_formatted))]
    else:
        museum_data = data_museum[data_museum['adresse'].str.contains(street, case=False, na=False)]
    museum_data = museum_data.dropna(subset=['Ylat', 'Xlong'])
    return museum_data

def afficher_infos_toilets(toilets_data):
    if toilets_data.empty:
        st.write("Aucune toilette trouvée à proximité.")
        return
    
    localisation = [toilets_data.iloc[0]['latitude'], toilets_data.iloc[0]['longitude']]
    m = folium.Map(location=localisation, zoom_start=15)
    
    for _, row in toilets_data.iterrows():
        if pd.isna(row['latitude']) or pd.isna(row['longitude']):
            continue 
        
        popup_content = f"""
            <b>Accès PMR:</b> {row['ACCES_PMR']}<br>
            <b>Horaire:</b> {row['HORAIRE']}<br>
        """
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            tooltip=row['ADRESSE']
        ).add_to(m)
    folium_static(m)

        

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
            tooltip=row['name']
        ).add_to(m)
    
    folium_static(m)
