import pandas as pd
import sys
import re
from unidecode import unidecode
from difflib import get_close_matches
import codecs
from utils import column_renaming


# Activer l'UTF-8 pour l'affichage
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

# Récupérer la recherche de l'utilisateur
if len(sys.argv) < 2:
    print("Error: Please provide a search term as an argument.")
    sys.exit(1)

research = sys.argv[1].strip().upper()
print(f"Extracting information about {research}")

# Chemins des fichiers
street_data_staged_path = "../data/street_data_staged.csv"
parking_data_staged_path = "../data/parking_data_staged.csv"

# Charger les données
try:
    street_data_staged = pd.read_csv(street_data_staged_path)
    parking_data_staged = pd.read_csv(parking_data_staged_path, sep=",")
except FileNotFoundError as e:
    print(f"Error: {e}")
    sys.exit(1)

# Vérification de la correspondance exacte
if research not in street_data_staged["typo"].values:
    print(f"No exact match found for '{research}'. Looking for close matches...")
    suggestions = get_close_matches(research, street_data_staged["typo"].unique(), n=3, cutoff=0.6)

    if suggestions:
        print("Did you mean one of the following?")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"{i}. {suggestion}")

        print("Enter the number of the correct match, or 0 to exit.")
        try:
            choice = int(input("Your choice: ").strip())
            if choice == 0:
                print("Exiting script. No match selected.")
                sys.exit(1)
            elif 1 <= choice <= len(suggestions):
                research = suggestions[choice - 1]
            else:
                print("Invalid choice. Exiting script.")
                sys.exit(1)
        except ValueError:
            print("Invalid input. Please enter a number. Exiting script.")
            sys.exit(1)
    else:
        print("No close matches found. Exiting script.")
        sys.exit(1)

print(f"Exact match found for '{research}'")
filtered_street_data = street_data_staged[street_data_staged["typo"] == research].copy()

if filtered_street_data.empty:
    print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
    sys.exit(1)

# Fonction pour trouver une correspondance dans les adresses
def find_match(adresse, typo_list):
    for typo in typo_list:
        if typo in adresse:
            return typo
    return None

# Trouver les correspondances pour les adresses normalisées
typo_list = filtered_street_data['typo_normalized'].tolist()
parking_data_staged["typo_match"] = parking_data_staged["adresse_normalized"].apply(lambda x: find_match(x, typo_list))

filtered_parking_data = parking_data_staged[parking_data_staged["typo_match"].notna()].copy()

filtered_parking_data.rename(columns=column_renaming, inplace=True)


# Conversion des colonnes numériques
numeric_columns = [
    "Nombre de Places", "Places PMR", "Places Voitures Électriques",
    "Tarif 1h (€)", "Tarif 24h (€)", "Hauteur Max (cm)"
]
filtered_parking_data[numeric_columns] = filtered_parking_data[numeric_columns].apply(pd.to_numeric, errors="coerce")

# Remplir les valeurs manquantes
filtered_parking_data.fillna({"Gratuit": "Non Spécifié"}, inplace=True)
filtered_parking_data["Nombre de Places"] = filtered_parking_data["Nombre de Places"].fillna(0).astype(int)

# Générer une description
if not filtered_parking_data.empty:
    filtered_parking_data["Description"] = (
        "Nom : " + filtered_parking_data["Nom"].astype(str) + "\n" +
        "Adresse : " + filtered_parking_data["Adresse"].astype(str) + "\n" +
        "Nombre de Places : " + filtered_parking_data["Nombre de Places"].astype(str) + "\n" +
        "Tarif 1h : " + filtered_parking_data["Tarif 1h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
        "Tarif 24h : " + filtered_parking_data["Tarif 24h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
        "Type Usagers : " + filtered_parking_data["Type Usagers"].fillna("Non Spécifié").astype(str) + "\n" +
        "Gratuit : " + filtered_parking_data["Gratuit"].astype(str)
)

# Afficher les résultats
print("------------------RESULTATS------------------")
if not filtered_street_data.empty:
    print(f"Informations about {research} --> \n Historical name : {filtered_street_data['historique'].values[0]} \n Original name : {filtered_street_data['orig'].values[0]}")

if not filtered_parking_data.empty:
    print("\nDescription des parkings:")
    for description in filtered_parking_data["Description"]:
        print(description)
else:
    print("No parking data found for the given query.")
