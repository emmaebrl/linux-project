#dos2unix bin/install.sh a lancer avant
#!/bin/bash
echo "Converting files with Windows line endings to Unix format..."
files_to_convert=$(grep -Ilr $'\r' --exclude-dir={.git,.venv} .)

if [ -n "$files_to_convert" ]; then
    for file in $files_to_convert; do
        echo "Converting $file to Unix format"
        dos2unix "$file"
    done
else
    echo "No files with Windows line endings found."
fi

# Fichier à lancer en premier pour ""installer"" l'application: dépendances, dossiers, docker etc ?? Pas très clair encore pour moi
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
pip install --upgrade pip
pip install -r requirements.txt #installer les dépendances


echo "Creating directories"
mkdir -p data #créer le dossier ou les données d'entrée seront stockées

echo "Creating docker image"
# à voir je pense qu'on attend d'avoir le cours dessus