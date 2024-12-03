source ./loader.conf
echo "Overwrite is set to ${overwrite}."

update=false
if [ ${overwrite} == "true" ]; then
  echo "Overwrite is set to true. So if the data already exists, it will be downloaded again."
  update=true
fi

## RUES

if [ -f "../data/street_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Streets already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata.paris.fr"
 curl -X 'GET' \
  'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/denominations-emprises-voies-actuelles/exports/csv?delimiter=%2C&list_separator=%2C&quote_all=false&with_bom=true' \
  -H 'accept: */*' -o ../data/street_data_raw.csv
fi

echo "Data are saved and ready in data/street_data_raw.csv"

## PARKINGS

if [ -f "../data/parking_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Parking data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from opendata.paris.fr"
 curl 'https://static.data.gouv.fr/resources/base-nationale-des-lieux-de-stationnement/20240109-111856/base-nationale-des-lieux-de-stationnement-outil-de-consolidation-bnls-v2.csv' -o ../data/parking_data_raw.csv
fi

echo "Data are saved and ready in data/parking_data_raw.csv"


## TOILETTES

if [ -f "../data/toilets_data_raw.csv" ] && [ "$update" = false ]; then
  echo "Toilets data already exists. Skipping download because overwrite is set to false."
else
  echo "Downloading data from data.gouv.fr"
 curl 'https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/sanisettesparis/exports/csv?use_labels=true' -o ../data/toilets_data_raw.csv
fi

echo "Data are saved and ready in data/toilets_data_raw.csv"