# Script Python pour retourner des informations à l'utilisateur
import pandas as pd
import sys
from difflib import get_close_matches


DATA_PATH = "data/staged_data.csv"
data = pd.read_csv(DATA_PATH)

def get_informations(street):
    """Retourne des informations sur une rue, avec suggestions si nécessaire."""
    research = street.strip().upper()
    if research not in data["typo"].values:
        suggestions = get_close_matches(research, data["typo"].unique(), n=1, cutoff=0.7)
        if suggestions:
            return None, None, suggestions[0] 
        else:
            return None, None, None
    filtered_data = data[data["typo"] == research]
    historique = filtered_data['historique'].values[0]
    orig = filtered_data['orig'].values[0]
    return historique, orig, None  

