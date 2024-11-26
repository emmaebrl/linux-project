import os
import requests

DATA_PATH = "data"
STREET_DATA_URL = "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/denominations-emprises-voies-actuelles/exports/csv"
PARKING_DATA_URL = "https://static.data.gouv.fr/resources/base-nationale-des-lieux-de-stationnement/20240109-111856/base-nationale-des-lieux-de-stationnement-outil-de-consolidation-bnls-v2.csv"

def download_file(url, file_path):
    response = requests.get(url)
    with open(file_path, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded: {file_path}")

def load_data():
    os.makedirs(DATA_PATH, exist_ok=True)
    street_file = os.path.join(DATA_PATH, "street_data_raw.csv")
    parking_file = os.path.join(DATA_PATH, "parking_data_raw.csv")
    
    if not os.path.exists(street_file):
        download_file(STREET_DATA_URL, street_file)
    if not os.path.exists(parking_file):
        download_file(PARKING_DATA_URL, parking_file)

if __name__ == "__main__":
    load_data()
