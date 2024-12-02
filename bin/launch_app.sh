# Fichier à lancer pour faire toutes les étapes de l'application: navigue dans les différents dossiers et lance les scripts run.sh
# Je comprends pas pourquoi le while true est là, je le commente pour l'instant parce que ça fait une boucle infinie

#!/bin/bash

echo "Downloading data"
cd data_loader
bash run.sh \
&& echo "Data downloaded" \
&& echo "Integrating data" \
&& cd ../data_integrator \
&& bash run.sh \
&& echo "Data integrated" \
&& cd .. \
&& echo "Running the app"

streamlit run webapp/app.py --server.address=0.0.0.0 --server.port=8501 &

# Attendre un moment pour s'assurer que Streamlit démarre
sleep 2

# Afficher l'URL d'accès
echo "Votre application est accessible à : http://localhost:8501"

# Garder le script actif pour éviter que le conteneur se termine
tail -f /dev/null