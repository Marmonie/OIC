"""
Date : 3 novembre 2023
But : Un premier exemple d’utilisation de FastAPI
"""

from fastapi import FastAPI

app = FastAPI()  # app est l’objet principal de l’application qui orientera toutes les routes de l’API


@app.get("/")  # définition du point d’accès "GET" au niveau de la racine ("/")
async def root():  # création d’une coroutine qui retourne un dict
    return {"message": "Bonjour les Étudiants de la Licence Informatique"}

# le message de retour de la coroutine est automatiquement gérée par FastAPI,
# qui produit une réponse HTTP appropriée au format JSON à partir de son dictionnaire

