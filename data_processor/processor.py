# ce script python permet de retourner les informations qu'on veut à l'user

import pandas as pd

staged_file_path = "../../data/staged_data.csv"

print("Reading staged data from", staged_file_path)
data = pd.read_csv(staged_file_path)

print(data.head())