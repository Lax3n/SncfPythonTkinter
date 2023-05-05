"""
Ce code permet de crée la base de donnée (gares_et_ids.txt)
"""

import requests
import APIs

# Définir le nom du fichier où stocker les identifiants
filename = "gares_et_id.txt"
# Ouvrir le fichier en mode écriture
with open(filename, "w", encoding="UTF-8") as file:
    # Définir l'URL de l'API SNCF
    url = "https://api.sncf.com/v1/coverage/sncf/stop_areas"
    # Définir les paramètres de la requête
    for i in range(5):#5 est le nombre de page
        params:dict = {
            "type": "stop_area",  # Type de l'objet recherché (ici, une gare)
            "count": 1000,       # Nombre de gare par page
            "key": APIs.APISNCF,  # Clé API SNCF
            "start_page": i
        }# on envoie la première requête à l'API SNCF et on récupére la réponse
        response = requests.get(url, params=params)
        # Vérifier si la première requête a réussi (code 200 (vu en IIW))
        if response.status_code == 200:
            # Extraire les données de la réponse au format JSON (dictionaire de dictionnaire)
            data = response.json()
            # Ajouter les identifiants de toutes les gares de la première page au fichier
            for stop_area in data["stop_areas"]:
                ID = stop_area['id'].split(":")[-1]
                bewrite = f"{stop_area['name']}|{ID}\n" #on mets tout bien en forme pour que la BDD soit bien lisible par main.py
                bewrite = bewrite.replace(" ", "-")
                bewrite = bewrite.replace("--", "-")
                bewrite = bewrite.replace("---", "-")
                bewrite = bewrite.replace("--", "-")
                file.write(bewrite.lower())
            # Vérifier s'il y a d'autres pages de résultats
        else:

            print(response.status_code)
