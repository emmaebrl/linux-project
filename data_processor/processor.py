import pandas as pd
import sys
import re
from unidecode import unidecode
from difflib import get_close_matches
import codecs
from utils import column_renaming

# Activer l'UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)


# Récupérer la recherche de l'utilisateur
research = sys.argv[1].strip().upper()
print("Extracting information about", research)
street_data_staged_path = "../data/street_data_staged.csv"
parking_data_staged_path = "../data/parking_data_staged.csv"

street_data_staged = pd.read_csv(street_data_staged_path)
parking_data_staged = pd.read_csv(parking_data_staged_path, sep=",")


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

print("Exact match found for", research)
filtered_street_data = street_data_staged[street_data_staged["typo"] == research].copy()

if filtered_street_data.empty:
    print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
    sys.exit(1)


def find_match(adresse, typo_list):
    for typo in typo_list:
        if typo in adresse:
            return typo
    return None

# Appliquer la correspondance
typo_list = filtered_street_data["typo_normalized"].tolist()
parking_data_staged["typo_match"] = parking_data_staged["adresse_normalized"].apply(lambda x: find_match(x, typo_list))

merged_data = pd.merge(
    filtered_street_data,
    parking_data_staged,
    left_on="typo_normalized",
    right_on="typo_match",
    how="outer"
)

columns_to_drop = ["info", "id_local"]
merged_data_cleaned = merged_data.drop(columns=columns_to_drop)
merged_data_cleaned.rename(columns=column_renaming, inplace=True)


numeric_columns = [
    "Nombre de Places", "Places PMR", "Places Voitures Électriques",
    "Tarif 1h (€)", "Tarif 24h (€)", "Hauteur Max (cm)"
]
merged_data_cleaned[numeric_columns] = merged_data_cleaned[numeric_columns].apply(pd.to_numeric, errors="coerce")

merged_data_cleaned.fillna({"Gratuit": "Non Spécifié"}, inplace=True)
merged_data_cleaned["Nombre de Places"] = merged_data_cleaned["Nombre de Places"].fillna(0).astype(int)

merged_data_cleaned["Description"] = (
    "Nom : " + merged_data_cleaned["Nom"].astype(str) + "\n" +
    "Adresse : " + merged_data_cleaned["Adresse"].astype(str) + "\n" +
    "Nombre de Places : " + merged_data_cleaned["Nombre de Places"].fillna(0).astype(int).astype(str) + "\n" +
    "Tarif 1h : " + merged_data_cleaned["Tarif 1h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
    "Tarif 24h : " + merged_data_cleaned["Tarif 24h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
    "Type Usagers : " + merged_data_cleaned["Type Usagers"].fillna("Non Spécifié").astype(str) + "\n" +
    "Gratuit : " + merged_data_cleaned["Gratuit"].astype(str)
)



print("------------------RESULTATS------------------")
if not merged_data_cleaned.empty:
    print(f"Informations about {research} -->")
    print(f"Historical name : {merged_data_cleaned['Historique'].iloc[0]}")
    print(f"Original name : {merged_data_cleaned['Origine'].iloc[0]}")
    print(f"Arrondissement : {merged_data_cleaned['Arrondissement'].iloc[0]}")
    print(f"Type de Voie : {merged_data_cleaned['Type de Voie'].iloc[0]}")
    print(f"Quartier : {merged_data_cleaned['Quartier'].iloc[0]}")
    print(f"Longueur : {merged_data_cleaned['Longueur'].iloc[0]}")
    print(f"Largeur : {merged_data_cleaned['Largeur'].iloc[0]}")
    print("\nDescription:")
    print(merged_data_cleaned["Description"].iloc[0])
else:
    print("No results found for the given query.")
