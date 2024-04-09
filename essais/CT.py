"""
Nom ......... : CT.py
Rôle ........ : programme qui permet de comparer les prix des contrôles techniques proches de chez soi (ou ailleurs)
                    pour un type de véhicule et d'énergie donné, puis affiche deux graphes supplémentaires
                    donnant les prix moyens par type de véhicule ou d'énergie dans la même ville.
Auteur ...... : Orianne Delmarre
Version ..... : V2.1 du 23/10/2023
Licence ..... : réalisé dans le cadre du cours 'Outils informatiques collaboratifs' de M Kislin-Duval
    de la Licence 1 informatique de l'IED Paris 8
Version de python3 utilisée : 10.6
"""

import requests
from math import cos
import plotly.express as px

# Données à modifier à convenance
REF_COORD = {"lon": 2.362551, "lat": 48.945260}  # Coordonnées géographiques autour duquel on affiche les CCT (ici, UP8)
RAYON = "5"  # Rayon (km) autour des coordonnées de référence
VEHICULE = "1"  # 1=Voiture Particulière, 2=4x4, 3=Voiture de collection, 4=Camionnette, 5=Camping-car (<3,5 tonnes)
ENERGIE = "1"  # 1=Essence, 2=Diesel, 3=Gaz, 4=Hybride, 5=Electrique

VEHICULE_DIC = {"1": "Voiture Particulière",
                "2": "4 × 4",
                "3": "Voiture de collection",
                "4": "Camionnette",
                "5": "Camping-car (>3,5t)"}
ENERGIE_DIC = {"1": "Essence",
                "2": "Diesel",
                "3": "Gaz",
                "4": "Hybride",
                "5": "Électrique"}


def calcule_distance(coord_a, coord_b):
    """
    Renvoie la distance entre deux points A et B pour de petites distances
    (source pour la formule : http://villemin.gerard.free.fr/aGeograp/Distance.htm)
    :param coord_a: dictionnaire des coordonnées géographiques du point A, de clés 'lon' et 'lat'
    :param coord_b: dictionnaire des coordonnées géographiques du point B, de clés 'lon' et 'lat'
    :return: la distance en kilomètres, au mètre près (float)
    """
    x = (coord_b["lon"] - coord_a["lon"]) * cos((coord_a["lat"] + coord_b["lat"]) / 2)
    y = coord_b["lat"] - coord_a["lat"]
    z = (x ** 2 + y ** 2) ** 0.5
    return round(1.852 * 60 * z, 3)


def renvoie_distance(dico_cct):
    """
    Renvoie la distance d'un CCT par rapport à des coordonnées de référence
    :param dico_cct: dico des données d'un CCT (inclus au minimum l'entrée "coordgeo")
    :return: la distance en km
    """
    return calcule_distance(dico_cct["coordgeo"], REF_COORD)


def teinter(lum):
    """
    Renvoie un code couleur au format hsl, dans les tons bruns, à la luminosité donnée en argument
    (avec un camaïeu, pas d'erreur d'association possible)
    :param lum: int compris entre 0 et 100 inclus
    :return: str (ex: 'hsl(14, 68, 50)')
    """
    return f"hsl(14, 68, {lum})"


# Partie 1 : affichage d'un diagramme en barre des prix des CCT dans le rayon sélectionné, triés par distance

url_rayon = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/records?" \
            f"where=distance(coordgeo%2C%20geom'POINT({REF_COORD['lon']}%20{REF_COORD['lat']})'%2C%20{RAYON}km)%20" \
            f"and%20cat_energie_id%3D%22{ENERGIE}%22%20and%20cat_vehicule_id%3D%22{VEHICULE}%22&" \
            f"order_by=cct_denomination&limit=100"

r_rayon = requests.get(url_rayon)
print(f"Status code tri distance : {r_rayon.status_code}")
nombre_resultats = r_rayon.json()["total_count"]
print(f"nombre d'entrées : {nombre_resultats}")
if nombre_resultats > 100:
    print("Attention, résultats incomplets. Le nombre de données dépasse la limite de 100.")

res_json = r_rayon.json()["results"]

"""
Données disponibles via l'API :
cct_code_dept, code_postal, cct_code_commune, code_insee_commune
cct_denomination (nom du cct), cct_adresse, cct_tel, cct_url, cct_siret
latitude, longitude, coordgeo {lon, lat}
cat_vehicule_id, cat_vehicule_libelle
cat_energie_id, cat_energie_libelle
prix_visite, date_application_visite, prix_contre_visite_min, prix_contre_visite_max
cct_statut
"""

# Élimination des doublons (seule la première entrée est gardée) et ajout des données lien et distance
donnees_completes = []

for donnee in res_json:
    # sauf liste vide ou élément identique au précédent
    if not donnees_completes or donnee["cct_denomination"] != donnees_completes[-1]["cct_denomination"]:
        cct_nom = donnee["cct_denomination"]
        cct_url = donnee["cct_url"]
        donnee["cct_lien"] = f"<a href='{cct_url}'>{cct_nom}</a>"  # pb : les liens ne fonctionnent pas
        donnee["distance"] = calcule_distance(donnee["coordgeo"], REF_COORD)
        donnees_completes.append(donnee)

print(f"nombre d'entrées après filtrage : {len(donnees_completes)}")

# Tri des données en fonction de leur distance au point de référence
donnees_triees = sorted(donnees_completes, key=renvoie_distance)

# La ville du point de référence a de fortes chances d'être la même que celle du CCT le plus proche
ville = donnees_triees[0]["cct_code_commune"]

# Création du diagramme
fig = px.bar(donnees_triees, x="cct_lien", y=["prix_visite", "prix_contre_visite_max"],
             title=f"Prix des Contrôles Techniques près de {ville} ({VEHICULE_DIC[VEHICULE]} {ENERGIE_DIC[ENERGIE]})",
             hover_data=["cct_adresse", "cct_tel", "distance"],
             labels={"cct_lien": "Nom du centre",
                     "cct_adresse": "adresse", "cct_tel": "tel", "distance": "distance (km)",
                     "variable": "légende", "value": "Prix visite / contre-visite"},
             color_discrete_map={"prix_visite": teinter(35), "prix_contre_visite_max": teinter(55)})

fig.update_layout(font_color=teinter(10), title=dict(font=dict(size=25)))

fig.write_html(f"Prix_CT_{ville}.html", auto_open=True)

# Partie 2 : Comparaisons en fonction des catégories d'énergie et de véhicules utilisés

url_energie = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/" \
              f"records?select=avg(prix_visite)&where=cct_code_commune%3D%22{ville}%22%20" \
              f"and%20cat_vehicule_id%3D%22{VEHICULE}%22&group_by=cat_energie_id&order_by=avg(prix_visite)%20DESC"
url_vehicule = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/controle_techn/" \
               f"records?select=avg(prix_visite)&where=cct_code_commune%3D%22{ville}%22%20" \
               f"and%20cat_energie_id%3D%22{ENERGIE}%22&group_by=cat_vehicule_id&order_by=avg(prix_visite)%20DESC"

stat_dic = {"energie": [url_energie, ENERGIE_DIC],
            "vehicule": [url_vehicule, VEHICULE_DIC]}

for key in stat_dic:
    r_stat = requests.get(stat_dic[key][0])
    print(f"Status code {key} : {r_stat.status_code}")
    res_stat = r_stat.json()["results"]

    fig_stat = px.bar(res_stat, x=f"cat_{key}_id", y="avg(prix_visite)",
                      title=f"Prix Moyen d'un CT à {ville} selon la catégorie d {key}",
                      labels={"avg(prix_visite)": "Prix Moyen", f"cat_{key}_id": f"{key}"},
                      color_discrete_sequence=[teinter(40)]*5)

    fig_stat.update_layout(font_color=teinter(10), font_size=15, title=dict(font_size=25))
    fig_stat.update_xaxes(labelalias=stat_dic[key][1])  # Change les codes énergie/véhicule en leur signification

    fig_stat.write_html(f"Prix_CT_{key}.html", auto_open=True)

