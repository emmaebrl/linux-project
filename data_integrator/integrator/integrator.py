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
museum_data_raw_path = "../../data/museum_data_raw.json"
museum_data_staged_path = "../../data/museum_data_staged.csv"

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

# Intégration des données sur les musées
print("Integrating Museum raw data from", museum_data_raw_path)
museum_data = json.load(open(museum_data_raw_path))
museum_data = pd.DataFrame({
    "Xlong": [feature["geometry"]["coordinates"][0] for feature in museum_data["features"]],
    "Ylat": [feature["geometry"]["coordinates"][1] for feature in museum_data["features"]],
    "name": [feature["properties"]["l_ep_min"] for feature in museum_data["features"]],
    "adresse": [feature["properties"]["adresse"] for feature in museum_data["features"]]
})
museum_data["adresse_normalized"] = museum_data["adresse"].apply(normalize_string)
museum_data.to_csv(museum_data_staged_path, index=False)
print("Integration done!")