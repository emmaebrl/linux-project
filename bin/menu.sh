#!/bin/bash

echo "Bienvenue dans l'application Streamlit !"
echo "Choisissez une option :"
echo "1) Lancer l'application en mode terminal (launch.sh)"
echo "2) Lancer l'application avec une interface graphique (launch_app.sh)"
read -p "Votre choix (1 ou 2) : " choix

case $choix in
  1)
    # Demander le nom de la rue
    read -p "Entrez le nom de la rue pour obtenir les informations : " rue
    if [ -z "$rue" ]; then
      echo "Erreur : Vous devez entrer un nom de rue."
      exit 1
    fi
    echo "Vous avez choisi : $rue"
    bash bin/launch.sh "$rue"
    ;;
  2)
    echo "Lancement de l'application graphique..."
    bash bin/launch_app.sh
    ;;
  *)
    echo "Choix invalide. Veuillez relancer le conteneur."
    exit 1
    ;;
esac
