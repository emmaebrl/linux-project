# Script Python pour retourner des informations à l'utilisateur
import pandas as pd
import sys
from difflib import get_close_matches


DATA_PATH = "data/street_data_staged.csv"
data = pd.read_csv(DATA_PATH)

def get_informations(street):
    """Retourne des informations sur une rue, avec suggestions si nécessaire."""
    research = street.strip().upper()
    if research not in data["typo"].values:
        suggestions = get_close_matches(research, data["typo"].unique(), n=1, cutoff=0.7)
        if suggestions:
            return None, None, None, None, None, None, None, suggestions[0] 
        else:
            return None, None, None, None, None, None, None, None
    data.fillna("Information non disponible", inplace=True)
    filtered_data = data[data["typo"] == research]
    historique = filtered_data['historique'].values[0]
    orig = filtered_data['orig'].values[0]
    typevoie = filtered_data['typvoie'].values[0]
    arrdt = filtered_data['arrdt'].values[0]
    quartier = filtered_data['quartier'].values[0]
    longueur = filtered_data['longueur'].values[0]
    largeur = filtered_data['largeur'].values[0]

    return historique, orig, typevoie, arrdt, quartier, longueur, largeur, None
