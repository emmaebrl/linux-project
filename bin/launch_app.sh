# Fichier à lancer pour faire toutes les étapes de l'application: navigue dans les différents dossiers et lance les scripts run.sh
# Je comprends pas pourquoi le while true est là, je le commente pour l'instant parce que ça fait une boucle infinie

source .venv/bin/activate #activer l'environnement virtuel
echo "Downloading data"
cd data_loader
bash run.sh\
&& echo "Data downloaded" \
&& echo "Integrating data" \
&& cd ../data_integrator\
&& bash run.sh \
&& echo "Data integrated" \
&& cd ..\
&& echo "Running the app" \
&& streamlit run webapp/app.py\