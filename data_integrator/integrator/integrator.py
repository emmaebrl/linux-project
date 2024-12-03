import pandas as pd
import json
import re
from unidecode import unidecode

def normalize_string(s):
    if pd.isna(s):
        return ""
    s = unidecode(s) 
    s = re.sub(r'[^\w]', '', s) 
    s = s.lower()
    s = s.replace("de", "") 
    s = s.replace("av", "avenue")
    s = s.replace("bd", "boulevard")
    s = s.replace("pl", "place")
    return s




# Chemin des fichiers de données
street_data_raw_path = "../../data/street_data_raw.csv"
street_data_staged_path = "../../data/street_data_staged.csv"
parking_data_raw_path = "../../data/parking_data_raw.csv"
parking_data_staged_path = "../../data/parking_data_staged.csv"
toilets_data_raw_path = "../../data/toilets_data_raw.csv"
toilets_data_staged_path = "../../data/toilets_data_staged.csv"
museum_data_raw_path = "../../data/museum_data_raw.json"
museum_data_staged_path = "../../data/museum_data_staged.csv"
sports_data_raw_path = "../../data/sports_data_raw.json"
sports_data_staged_path = "../../data/sports_data_staged.csv"

# Intégration des données sur les rues
print("Integrating Streets raw data from", street_data_raw_path)
street_data = pd.read_csv(street_data_raw_path)
street_data = street_data[["typo", "orig", "historique", "typvoie","arrdt", "quartier", "longueur", "largeur"]]
street_data["typo_normalized"] = street_data["typo"].apply(normalize_string)
print("Writing integrated data to", street_data_staged_path)
street_data.to_csv(street_data_staged_path, index=False)

# Intégration des données sur les parkings
print("Integrating Parking raw data from", parking_data_raw_path)
parking_data = pd.read_csv(parking_data_raw_path, sep=";")
parking_data = parking_data[parking_data["insee"].astype(str).str.startswith("75")].copy()
parking_data["gratuit"] = parking_data["gratuit"].map({1: "Oui", 0: "Non"})
parking_data["Arrondissement"] = parking_data["insee"].astype(str).str[-2:] + "e"
parking_data["adresse_normalized"] = parking_data["adresse"].apply(normalize_string)
parking_data.to_csv(parking_data_staged_path, index=False)
print(f"Filtered parking data saved to {parking_data_staged_path}")

# Intégration des données sur les parkings
print("Integrating toilets raw data from" , toilets_data_raw_path)
toilets_data = pd.read_csv(toilets_data_raw_path, sep = ";")
toilets_data["adresse_normalized"] = toilets_data['ADRESSE'].apply(normalize_string)
# Récupération des 2 coordonées situées dans une seule colonne
toilets_data[['latitude', 'longitude']] = toilets_data['geo_point_2d'].str.split(', ', expand=True).astype(float)
toilets_data.to_csv(toilets_data_staged_path, index = False)
print(f"Filtered toilets data savec to {toilets_data_staged_path}")


# Intégration des données sur les musées
print("Integrating Museum raw data from", museum_data_raw_path)
museum_data = json.load(open(museum_data_raw_path))
museum_data = pd.DataFrame({
    "Xlong": [feature["geometry"]["coordinates"][0] for feature in museum_data["features"]],
    "Ylat": [feature["geometry"]["coordinates"][1] for feature in museum_data["features"]],
    "name": [feature["properties"]["l_ep_min"] for feature in museum_data["features"]],
    "adresse": [feature["properties"]["adresse"] for feature in museum_data["features"]],
    "c_postal": [feature["properties"]["c_postal"] for feature in museum_data["features"]],
})
museum_data["adresse_normalized"] = museum_data["adresse"].apply(normalize_string)
museum_data["c_postal"] = museum_data["c_postal"].astype(str)
museum_data_filtered = museum_data[museum_data["c_postal"].str.startswith("75")].copy()
museum_data.to_csv(museum_data_staged_path, index=False)

# Intégration des données sur les complexes sportifs
print("Integrating Sports raw data from", sports_data_raw_path)
sports_data = json.load(open(sports_data_raw_path))
sports_data_df = pd.DataFrame({
    "Xlong": [feature["geometry"]["coordinates"][0] for feature in sports_data["features"]],
    "Ylat": [feature["geometry"]["coordinates"][1] for feature in sports_data["features"]],
    "name": [feature["properties"]["l_ep_maj"] for feature in sports_data["features"]],
    "adresse": [f"{feature['properties'].get('n_voie', '')} {feature['properties'].get('c_suf1', '')} {feature['properties'].get('c_suf2', '')} {feature['properties'].get('c_suf3', '')} {feature['properties'].get('c_desi', '')} {feature['properties'].get('c_liaison', '')} {feature['properties'].get('l_voie', '')}" for feature in sports_data["features"]],
    "annee_creation": [feature["properties"]["d_annee_cr"] for feature in sports_data["features"]],
    "public": [feature["properties"]["b_public"] for feature in sports_data["features"]]
})

# Normaliser l'adresse
sports_data_df["adresse_normalized"] = sports_data_df["adresse"].apply(normalize_string)
sports_data_df.to_csv(sports_data_staged_path, index=False)


print("Integration done!")