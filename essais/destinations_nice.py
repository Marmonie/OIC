"""
Nom ......... : S2OIC_Exercice3.1.py
Rôle ........ : code pour une API sur les destinations au départ de l'aéroport de Nice, avec FastAPI.
Auteur ...... : Orianne Delmarre
Version ..... : V0.1 du 05/11/2023
Licence ..... : réalisé dans le cadre du cours 'Outils informatiques collaboratifs' de M Kislin-Duval
    de la Licence 1 informatique de l'IED Paris 8
Version de python3 utilisée : 10.6
"""


import json
from fastapi import FastAPI, HTTPException, Query, Path
from mongita import MongitaClientDisk
from pydantic import BaseModel
from typing import Annotated  # utilisation conseillée pour FastAPI, cf https://fastapi.tiangolo.com/tutorial/query-params-str-validations/


class Destination(BaseModel):
    ville: str
    pays: str
    region: str
    activites: list[str]  # need Python version >= 3.9
    id: int
    temps_vol: int  # minutes
    distance_centreville: int  # km
    compagnies: list[str]


app = FastAPI()

client = MongitaClientDisk()
db = client.db
Destinations = db.Destinations


# Insertion de destinations
with open("destinations.json") as file:
    liste_destinations = json.load(file)

if Destinations.count_documents({}) == 0:  # Pour éviter qu’ils ne se rajoutent à chaque fois
    Destinations.insert_many(liste_destinations)  


@app.get("/")
async def root():
    return {"message": "Bonjour ! Où souhaitez-vous partir, depuis l'aéroport de Nice ?"}


# Recherche de destinations
@app.get("/Destinations")
async def get_destinations(
    offset: Annotated[int, Query(description="nombre de résultats à passer")] = 0, 
    limit: Annotated[int, Query(description= "nombre de résultats maximum à afficher")] = 3 ):
    existing_destinations = Destinations.find({})
    res = [
        {key: destination[key] for key in destination if key != "_id"}  # https://www.mongodb.com/docs/manual/reference/method/db.collection.insertMany/
        for destination in existing_destinations
    ]
    return res[offset:offset+limit]


# Recherche d'une destination par nom
@app.get("/Destinations/{ville}")
async def get_destination_by_name(ville: str):
    if Destinations.count_documents({"ville": ville.capitalize()}) > 0:
        destination = Destinations.find_one({"ville": ville.capitalize()})
        return {key: destination[key] for key in destination if key != "_id"}
    raise HTTPException(status_code=404, detail=f"Aucun vol direct connu vers la ville de {ville}.")


# Recherche de destinations par temps de vol (supérieur ou inférieur)
@app.get("/Destinations/temps_vol/{temps_vol}")
async def get_destination_by_flight_time(
    inf_ou_sup: Annotated[str, Query(
        # donne le choix entre les deux valeurs suivantes (https://fastapi.tiangolo.com/tutorial/schema-extra-example/):
        openapi_examples={
        "sup": {"summary": "temps de vol supérieur à ...", "value":"gt"},
        "inf": {"summary": "temps de vol inférieur à ...", "value":"lt"}
        })],
    temps_vol: int ):
    res = Destinations.find({"temps_vol": {f"${inf_ou_sup}": temps_vol}})
    return [{key: destination[key] for key in destination if key != "_id"} for destination in res]


# # Recherche de destinations par compagnie --> pb: elemMatch pas encore implémenté sur Mongita
# @app.get("/Destinations/compagnie/{compagnie}")
# async def get_destination_by_airline(compagnie: str):
#     res = Destinations.find({"compagnies": {"$elemMatch" : {"$eq": compagnie}}})
#     return [{key: destination[key] for key in destination if key != "_id"} for destination in res]


# Recherche de destinations par activité --> même problème



# Recherche de destinations par région du monde --> pb: il faut mettre à jour le code si l'aéroport rajoute une région
@app.get("/Destinations/region/{region}")
async def get_destination_by_world_region(
    region: Annotated[str, Path(
        # menu déroulant
        openapi_examples={
        "Am_Nord": {"summary":"Amérique du Nord", "value":"Amérique du Nord"},
        "Moyen_Orient": {"summary":"Moyen Orient", "value":"Moyen Orient"},
        "Af_Nord": {"summary":"Afrique du Nord", "value":"Afrique du Nord"},
        "Europe": {"summary":"Europe", "value":"Europe"}
        }, 
        description="Région du monde où vous souhaitez voyager" ) ] ):
    if Destinations.count_documents({"region": region}) > 0:
        res = Destinations.find({"region": region})
        return [{key: destination[key] for key in destination if key != "_id"} for destination in res]
    raise HTTPException(status_code=404, detail=f"Aucun vol direct connu vers la region {region}.")


# Ajout d'une destination
@app.post("/Destinations")
async def post_destination(destination: Destination):
    Destinations.insert_one(destination.dict())  # 'dict is deprecated, use model_dump instead' (d'après pycharm)
    return destination


# Ajout d'une compagnie à une destination avec $push (https://www.mongodb.com/docs/manual/reference/method/db.collection.update/)
@app.put("/Destinations/{ville}/compagnie/{nouvelle_compagnie}")
async def add_airline(
    ville: str, 
    nouvelle_compagnie: Annotated[str, Path(description="la compagnie aérienne à ajouter")]):
    if Destinations.count_documents({"ville": ville.capitalize()}) > 0:
        Destinations.update_one(
           {"ville": ville.capitalize()},
           {"$push": {"compagnies": f"{nouvelle_compagnie}"}}  # https://github.com/scottrogowski/mongita/pull/19
        )
        return f"La compagnie {nouvelle_compagnie} a été ajoutée à la destination {ville}."
    raise HTTPException(status_code=404, detail=f"Aucun vol direct connu vers la ville de {ville}.")


# Ajout d'une activité à une destination
@app.put("/Destinations/{ville}/activite/{nouvelle_activite}")
async def add_activity(
    ville: str, 
    nouvelle_activite: Annotated[str, Path(description="l'activité à ajouter")]):
    if Destinations.count_documents({"ville": ville.capitalize()}) > 0:
        Destinations.update_one(
           {"ville": ville.capitalize()},
           {"$push": {"activites": f"{nouvelle_activite.lower()}"}}
        )
        return f"L'activité {nouvelle_activite} a été ajoutée à la destination {ville}."

    raise HTTPException(status_code=404, detail=f"Aucun vol direct vers {ville} trouvé")


# suppression d'une destination par id (find_one_and_delete() aurait été mieux, mais pas implémenté)
@app.delete("/Destinations/{destination_id}")
async def delete_destination(destination_id: Annotated[int, Path(description="l'identifiant de la destination à supprimer") ] ):
    delete_result = Destinations.delete_one({"id": destination_id})  
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Aucune destination avec cet identifiant {destination_id} n’existe")
    return {"OK": True}
