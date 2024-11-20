import pandas as pd
import json


raw_data_path = "../../data/streets_raw_data.csv"
staged_file_path = "../../data/staged_data.csv"

print("Integrating raw data from", raw_data_path)
data = pd.read_csv(raw_data_path)
data = data[["typo", "orig", "historique", "typvoie","arrdt", "quartier", "longueur", "largeur"]]

# à mettre ici : Les transformations des données pour les rendre utilisables (filtres, concaténations, etc.)

print("Writing integrated data to", staged_file_path)
data.to_csv(staged_file_path, index=False)

print("Integration done!")
