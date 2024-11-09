# ce script récupère la (ou les?) base de données

mkdir -p "../input"
update=false
if [ "$1" == "overwrite" ]; then
  update=true
fi

if [ -f "../input/database.csv" ] && [ "$update" = false ]; then
  echo "Data already exists. Skipping download."
else
  echo "Downloading data from opendata.paris.fr"
 curl -X 'GET' \
  'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/denominations-emprises-voies-actuelles/exports/csv?delimiter=%2C&list_separator=%2C&quote_all=false&with_bom=true' \
  -H 'accept: */*' -o ../input/database.csv
  fi

echo "Data are saved and ready in input/database.csv"