# Script Python pour retourner des informations à l'utilisateur
import pandas as pd
import sys
from difflib import get_close_matches

sys.stdout.reconfigure(encoding='utf-8')

# Récupérer la recherche de l'utilisateur
research = sys.argv[1].strip().upper()

print("Extracting information about", research)

# Chemin du fichier de données
staged_file_path = "../data/staged_data.csv"

# Lecture du fichier
print("Reading staged data from", staged_file_path)
data = pd.read_csv(staged_file_path)

# Vérification si la colonne "typo" est présente
if "typo" not in data.columns:
    print("Error: Column 'typo' not found in the dataset.")
    sys.exit(1)

# Vérification de la correspondance exacte
if research not in data["typo"].values:
    print(f"No exact match found for '{research}'. Looking for close matches...")
    
    # Trouver des correspondances approximatives
    suggestions = get_close_matches(research, data["typo"].unique(), n=3, cutoff=0.6)

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
data = data[data["typo"] == research]

if data.empty:
    print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
    sys.exit(1)

# Affichage des résultats
print("------------------RESULTATS------------------")
data.fillna("L'information n'est pas disponible.", inplace=True)
print(
    f"Informations about {research} --> \n"
    f"Historical name : {data['historique'].values[0]} \n"
    f"Origin of the name : {data['orig'].values[0]}\n"
    f"Type of road : {data['typvoie'].values[0]} \n"
    f"District : {data['arrdt'].values[0]} \n"
    f"Neighborhood : {data['quartier'].values[0]}\n"
    f"Length : {data['longueur'].values[0]} \n"
    f"Width : {data['largeur'].values[0]}"
)
