# Fichier à lancer en premier pour ""installer"" l'application: dépendances, dossiers, docker etc ?? Pas très clair encore pour moi
#!/bin/bash
# Ces commandes permettent de créer un environnement virtuel et d'installer les dépendances du projet.
# Je crois qu'elles seront enlévées une fois qu'on utilisera Docker pour lancer l'application.

# Créer un environnement virtuel et installer les dépendances
echo "Creating virtual environment"

if [ -d .venv ]; then
    echo "Virtual environment already exists"
else
    python3 -m venv .venv #créer un environnement virtuel
fi
source .venv/bin/activate #activer l'environnement virtuel
pip install -r requirements.txt #installer les dépendances


echo "Creating directories"
mkdir -p data #créer le dossier ou les données d'entrée seront stockées

echo "Creating docker image"
# à voir je pense qu'on attend d'avoir le cours dessus
