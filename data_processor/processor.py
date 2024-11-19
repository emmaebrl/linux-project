# ce script python permet de retourner les informations qu'on veut à l'user
import pandas as pd
import sys
research = sys.argv[1] 

print("Extract information about", research)
staged_file_path = "../data/staged_data.csv"

print("Reading staged data from", staged_file_path)
data = pd.read_csv(staged_file_path)
data = data[data["typo"] == research]

print("------------------RESULTATS------------------")
print(f"Informations about {research} --> \n Historical name : {data['historique'].values[0]} \n Original name : {data['orig'].values[0]}")
