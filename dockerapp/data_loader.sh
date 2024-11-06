mkdir -p "input"

update=false
if [ "$1" == "overwrite" ]; then
  update=true
fi

if [ -f "input/test.csv" ] && [ "$update" = false ]; then
  echo "Data already exists. Skipping download."
else
  echo "Downloading data from data.gouv.fr"
  curl https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-parcoursup_2020/exports/csv?use_labels=true -o input/test.csv
fi