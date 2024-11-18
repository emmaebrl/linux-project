# Fichier à lancer en premier pour ""installer"" l'application: dépendances, dossiers, docker etc ?? Pas très clair encore pour moi
#!/bin/bash
# Ces commandes permettent de créer un environnement virtuel et d'installer les dépendances du projet.
# Je crois qu'elles seront enlévées une fois qu'on utilisera Docker pour lancer l'application.

VENV_DIR=".venv"

if [ -d "$VENV_DIR" ]; then
    echo "L'environnement virtuel existe déjà. Activation..."
else
    command -v virtualenv >/dev/null 2>&1 || { echo >&2 "virtualenv n'est pas installé. Installation en cours..."; pip install virtualenv; }

    virtualenv $VENV_DIR
fi
source $VENV_DIR/bin/activate

echo "Installation des dépendances..."
pip install -r requirements.txt
echo "Environnement virtuel créé avec succès."


echo "Creating directories"
mkdir -p data #créer le dossier ou les données d'entrée seront stockées

echo "Creating docker image"
# à voir je pense qu'on attend d'avoir le cours dessus