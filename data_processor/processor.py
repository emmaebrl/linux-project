# Script Python pour retourner des informations à l'utilisateur
import pandas as pd
import sys
from difflib import get_close_matches

research = sys.argv[1].strip().upper()

print("Extracting information about", research)
staged_file_path = "../data/staged_data.csv"

print("Reading staged datya from", staged_file_path)
data = pd.read_csv(staged_file_path)

if research not in data["typo"].values:
    print(f"No exact match found for '{research}'. Looking for close matches...")
    suggestions = get_close_matches(research, data["typo"].unique(), n=1, cutoff=0.7)

    if suggestions:
        suggested_value = suggestions[0]
        print(f"Did you mean '{suggested_value}'? (yes/no)")
        user_input = input().strip().lower()

        if user_input == "yes":
            research = suggested_value
        else:
            print("Exiting script. No match found.")
            sys.exit(1)
    else:
        print("No close matches found. Exiting script.")
        sys.exit(1)

data = data[data["typo"] == research]

if data.empty:
    print(f"No data found for '{research}'. This should not happen if a suggestion was accepted.")
    sys.exit(1)

print("------------------RESULTATS------------------")
print(f"Informations about {research} --> \n Historical name : {data['historique'].values[0]} \n Original name : {data['orig'].values[0]}")
