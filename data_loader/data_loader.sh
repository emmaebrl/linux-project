# ce script récupère la (ou les?) base de données
# on peut lui passer un argument pour écraser les données existantes ou non si déjà présente (overwrite) -> à changer dans le fichier de config loader.conf

source ./loader.conf
echo "Overwrite is set to ${overwrite}."

update=false
if [ ${overwrite} == "true" ]; then
  echo "Overwrite is set to true. So if the data already exists, it will be downloaded again."
  update=true
fi

if [ -f "../data/streets_raw_data.csv" ] && [ "$update" = false ]; then
  echo "Data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata.paris.fr"
 curl -X 'GET' \
  'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/denominations-emprises-voies-actuelles/exports/csv?delimiter=%2C&list_separator=%2C&quote_all=false&with_bom=true' \
  -H 'accept: */*' -o ../data/streets_raw_data.csv
fi
echo "Data are saved and ready in data/streets_raw_data.csv" 