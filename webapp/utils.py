import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from googletrans import Translator
from difflib import get_close_matches

# Constants
DATA_PATHS = {
    "streets": "data/street_data_staged.csv",
    "parking": "data/parking_data_staged.csv",
    "toilets": "data/toilets_data_staged.csv",
    "museums": "data/museum_data_staged.csv",
    "sports": "data/sports_data_staged.csv"
}

# Load datasets
data = pd.read_csv(DATA_PATHS["streets"])
data_parking = pd.read_csv(DATA_PATHS["parking"])
data_toilets = pd.read_csv(DATA_PATHS["toilets"])
data_museums = pd.read_csv(DATA_PATHS["museums"])
data_sports = pd.read_csv(DATA_PATHS["sports"])

# Utility functions
def translate_text(text, dest="en"):
    """Translates a given text to the target language."""
    translator = Translator()
    return translator.translate(text, dest=dest).text

def format_arrondissement(arr):
    """Formats arrondissement codes to match expected formats."""
    if len(arr) == 1:
        return "7500" + arr
    elif len(arr) == 2:
        return "750" + arr
    return arr


# Core functions
def get_street_data(street_name):
    """Returns information about a street, with suggestions if needed."""
    search_term = street_name.strip().upper()
    if search_term not in data["typo"].values:
        suggestions = get_close_matches(search_term, data["typo"].unique(), n=1, cutoff=0.7)
        if suggestions:
            return None, suggestions[0]
        else:
            return None, None
    street_data = data[data["typo"] == search_term]
    street_data["historique"] = street_data["historique"].apply(translate_text)
    street_data["orig"] = street_data["orig"].apply(translate_text)
    return street_data, None

def get_nearby_data(data_source, street_name, arrondissement=None, arr_col=None):
    """Returns nearby data (e.g., parking, toilets, museums) filtered by street and/or arrondissement."""
    if arrondissement:
        arr_list = [format_arrondissement(a.strip()) for a in arrondissement.split(",")]
        data_source = data_source[data_source[arr_col].astype(str).apply(lambda x: any(arr in x for arr in arr_list))]
    else:
        data_source = data_source[data_source["adresse_normalized"].str.contains(street_name, case=False, na=False)]
    return data_source.dropna(subset=['Ylat', 'Xlong'])

def display_map(data_source, lat_col, long_col, popup_generator, section):
    """Displays a Folium map with markers based on data source."""
    if data_source.empty:
        st.info(f"🚫 No nearby {section} found.")
        return None

    center = [data_source.iloc[0][lat_col], data_source.iloc[0][long_col]]
    m = folium.Map(location=center, zoom_start=15)

    for _, row in data_source.iterrows():
        popup = folium.Popup(popup_generator(row), max_width=300)
        folium.Marker(
            location=[row[lat_col], row[long_col]],
            popup=popup,
            tooltip=row["adresse"]
        ).add_to(m)
    
    folium_static(m)

def parking_popup(row):
    """Generates HTML content for parking markers."""
    return f"""
        <b>Address:</b> {row['adresse']}<br>
        <b>Free:</b> {row['gratuit']}<br>
        <b>Rate (1h):</b> {row['tarif_1h']} €<br>
        <b>Rate (2h):</b> {row['tarif_2h']} €<br>
        <b>Rate (3h):</b> {row['tarif_3h']} €<br>
        <b>Rate (4h):</b> {row['tarif_4h']} €<br>
        <b>Max Height:</b> {row['hauteur_max']} cm<br>
    """

def toilet_popup(row):
    """Generates HTML content for toilet markers."""
    return f"""
        <b>Accessibility:</b> {row['ACCES_PMR']}<br>
        <b>Schedule:</b> {row['HORAIRE']}<br>
    """

def museum_popup(row):
    """Generates HTML content for museum markers."""
    return f"""
        <b>Name:</b> {row['name']}<br>
        <b>Address:</b> {row['adresse']}
    """

def sports_popup(row):
    """Generates HTML content for sports facility markers."""
    return f"""
        <b>Name:</b> {row['name']}<br>
    """
# Display functions
def display_street_info(street_data):
    """Displays detailed information about a street."""
    st.write(f"- **Historical Name:** {street_data['historique'].values[0]}")
    st.write(f"- **Original Name:** {street_data['orig'].values[0]}")
    st.write(f"- **District:** {street_data['arrdt'].values[0]}")
    st.write(f"- **Neighborhood:** {street_data['quartier'].values[0]}")

def display_parking_data(street_name, arrondissement=None):
    parking_data = get_nearby_data(data_parking, street_name, arrondissement, arr_col="adresse")
    display_map(parking_data, "Ylat", "Xlong", parking_popup, "parking")

def display_toilet_data(street_name, arrondissement=None):
    toilet_data = get_nearby_data(data_toilets, street_name, arrondissement, arr_col= "ARRONDISSEMENT")
    display_map(toilet_data, "Ylat", "Xlong", toilet_popup, "toilets")

def display_museum_data(street_name, arrondissement=None):
    museum_data = get_nearby_data(data_museums, street_name, arrondissement, arr_col= "c_postal")
    display_map(museum_data, "Ylat", "Xlong", museum_popup, "museums")

def display_sports_data(street_name, arrondissement=None):
    sports_data = get_nearby_data(data_sports, street_name, arrondissement, arr_col= "c_postal")
    display_map(sports_data, "Ylat", "Xlong", sports_popup, "sports")
