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
streamlit run webapp/app.py --server.port=5002 &
sleep 2

# Afficher l'adresse IP publique ou locale
IP=$(hostname -I | awk '{print $1}')
echo "Votre application est accessible à : http://$IP:5002"

tail -f /dev/null
#sleep 2
#echo "Votre application est accessible à : http://localhost:8501"
