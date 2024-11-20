import pandas as pd
import sys
import re
from unidecode import unidecode
from difflib import get_close_matches
import codecs


sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
# Récupérer la recherche de l'utilisateur
research = sys.argv[1].strip().upper()

print("Extracting information about", research)

# Chemin des fichiers de données
staged_file_path = "../data/staged_data.csv"
parking_raw_data_path = "../data/parking_raw_data.csv"

# Lecture des fichiers
print("Reading staged data from", staged_file_path)
staged_data = pd.read_csv(staged_file_path)

print("Reading additional data from", parking_raw_data_path)
parking_raw_data = pd.read_csv(parking_raw_data_path, sep=";")

# Vérification si la colonne "typo" est présente
if "typo" not in staged_data.columns:
    print("Error: Column 'typo' not found in the staged dataset.")
    sys.exit(1)

# Vérification de la correspondance exacte
if research not in staged_data["typo"].values:
    print(f"No exact match found for '{research}'. Looking for close matches...")
    suggestions = get_close_matches(research, staged_data["typo"].unique(), n=3, cutoff=0.6)

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

# Filtrer les données avec la recherche confirmée
filtered_data = staged_data[staged_data["typo"] == research].copy()

if filtered_data.empty:
    print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
    sys.exit(1)

# Filtrer les données avec "insee" commençant par "75"
filtered_data_parking = parking_raw_data[parking_raw_data["insee"].astype(str).str.startswith("75")].copy()

if filtered_data_parking.empty:
    print("No data found with 'insee' starting with '75'. Exiting script.")
    sys.exit(1)

# Normalisation des chaînes
def normalize_string(s):
    if pd.isna(s):
        return ""
    s = unidecode(s)  # Supprime les accents
    s = re.sub(r'[^\w]', '', s)  # Supprime les caractères non alphanumériques
    s = s.lower()  # Convertit en minuscules
    return s

# Normaliser les colonnes
filtered_data["typo_normalized"] = filtered_data["typo"].apply(normalize_string)
filtered_data_parking["adresse_normalized"] = filtered_data_parking["adresse"].apply(normalize_string)

# Sauvegarder filtered_data
filtered_data.to_csv("../data/filtered_data_new.csv", index=False)
print("Filtered data saved to ../data/filtered_data_new.csv")

# Sauvegarder filtered_data_parking
filtered_data_parking.to_csv("../data/filtered_data_parking_new.csv", index=False)
print("Filtered parking data saved to ../data/filtered_data_parking_new.csv")

# Trouver les correspondances
def find_match(adresse, typo_list):
    for typo in typo_list:
        if typo in adresse:  # Vérifie si typo est contenu dans l'adresse
            return typo
    return None

# Appliquer la correspondance
typo_list = filtered_data["typo_normalized"].tolist()
filtered_data_parking["typo_match"] = filtered_data_parking["adresse_normalized"].apply(lambda x: find_match(x, typo_list))

# Vérifiez les correspondances trouvées
print("Matches found:")
print(filtered_data_parking[filtered_data_parking["typo_match"].notna()])

# Effectuer la jointure
merged_data = pd.merge(
    filtered_data,
    filtered_data_parking,
    left_on="typo_normalized",
    right_on="typo_match",
    how="outer"
)

# Sauvegarder merged_data
merged_data.to_csv("../data/merged_data.csv", index=False)
print("Merged data saved to ../data/merged_data.csv")

# Suppression des colonnes inutiles
columns_to_drop = ["info", "id_local"]
merged_data_cleaned = merged_data.drop(columns=columns_to_drop)

# Renommage des colonnes
column_renaming = {
    "id": "ID Parking",
    "nom": "Nom",
    "insee": "Code INSEE",
    "adresse": "Adresse",
    "url": "URL",
    "type_usagers": "Type Usagers",
    "gratuit": "Gratuit",
    "nb_places": "Nombre de Places",
    "nb_pmr": "Places PMR",
    "nb_voitures_electriques": "Places Voitures Électriques",
    "hauteur_max": "Hauteur Max (cm)",
    "tarif_1h": "Tarif 1h (€)",
    "tarif_24h": "Tarif 24h (€)",
    "type_ouvrage": "Type Ouvrage",
    "adresse_normalized": "Adresse Normalisée",
    "typo_match": "Correspondance Typo",
    "typo_normalized": "Typo Normalisée",
    "orig": "Origine",
    "historique": "Historique"
}
merged_data_cleaned.rename(columns=column_renaming, inplace=True)

# Conversion des types
numeric_columns = [
    "Nombre de Places", "Places PMR", "Places Voitures Électriques",
    "Tarif 1h (€)", "Tarif 24h (€)", "Hauteur Max (cm)"
]
merged_data_cleaned[numeric_columns] = merged_data_cleaned[numeric_columns].apply(pd.to_numeric, errors="coerce")

# Remplir les valeurs manquantes
merged_data_cleaned.fillna({"Gratuit": "Non Spécifié"}, inplace=True)
merged_data_cleaned["Nombre de Places"] = merged_data_cleaned["Nombre de Places"].fillna(0).astype(int)


# Création d'une colonne descriptive
merged_data_cleaned["Description"] = (
    "Nom : " + merged_data_cleaned["Nom"].astype(str) + "\n" +
    "Adresse : " + merged_data_cleaned["Adresse"].astype(str) + "\n" +
    "Nombre de Places : " + merged_data_cleaned["Nombre de Places"].fillna(0).astype(int).astype(str) + "\n" +
    "Tarif 1h : " + merged_data_cleaned["Tarif 1h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
    "Tarif 24h : " + merged_data_cleaned["Tarif 24h (€)"].map(lambda x: f"{x:.2f} €" if pd.notna(x) else "Non Disponible") + "\n" +
    "Type Usagers : " + merged_data_cleaned["Type Usagers"].fillna("Non Spécifié").astype(str) + "\n" +
    "Gratuit : " + merged_data_cleaned["Gratuit"].astype(str)
)

# Affichage des résultats
print("------------------RESULTATS------------------")
if not merged_data_cleaned.empty:
    # Affichage des informations historiques et originales
    print(f"Informations about {research} -->")
    print(f"Historical name : {merged_data_cleaned['Historique'].iloc[0]}")
    print(f"Original name : {merged_data_cleaned['Origine'].iloc[0]}")
    
    # Affichage de la description
    print("\nDescription:")
    print(merged_data_cleaned["Description"].iloc[0])
else:
    print("No results found for the given query.")
