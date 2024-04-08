"""
Nom ......... : OIC4.2.py
Rôle ........ : exercice 4.2 du cours OIC pour découvrir streamlit
Auteur ...... : Orianne Delmarre
Version ..... : V0.1 du 15/03/2024
Licence ..... : réalisé dans le cadre du cours 'Outils informatiques collaboratifs' de M Kislin-Duval
    de la Licence 1 informatique de l'IED Paris 8
Version de python3 utilisée : 10.6
Usage : Pour exécuter : streamlit run https://github.com/Marmonie/OIC/blob/main/essais/OIC4.2.py
"""

import streamlit as st
# https://pillow.readthedocs.io/en/stable/reference/Image.html
from PIL import Image, ExifTags
import io
import requests
import json
import folium
from streamlit_folium import folium_static

# coordonnées en décimal, pour folium (= degré + min/60 + sec/3600)
coord_Nice = 43.7034, 7.2911

url_img = 'https://github.com/Marmonie/OIC/blob/main/essais/P7070925.jpg?raw=true'
url_voyages = 'https://raw.githubusercontent.com/Marmonie/OIC/main/essais/voyages.json'


def trunc(x):
    """
    Ne conserve que la partie entière d'un nombre décimal
    :param x: nombre décimal (ex: 4.5)
    :return: 4.0
    """
    lst_str = str(x).split('.')
    return float(lst_str[0])


def convert_dec_rat(x):
    """
    Convertit un décimal en format (degrés, minutes, secondes)
    :param x: un nombre décimal
    :return: un tuple de décimaux (deg, min, sec)
    """
    abs_x = abs(x)
    d = trunc(abs_x)
    m = trunc((abs_x - d) * 60)
    s = round((3600 * (abs_x - d - m / 60)), 2)
    return d, m, s


def convert_coord(lat, lon):
    """
    Convertit des coordonnées GPS décimales en format EXIF (rational64u)
    :param lat: latitude (float)
    :param lon: longitude (float)
    :return: coord GPS sous forme ('N/S', (deg, min, sec), 'E/W', (deg, min, sec))
    """
    GPSLatitudeRef = 'N'
    if lat < 0:
        GPSLatitudeRef = 'S'

    GPSLatitude = convert_dec_rat(lat)

    GPSLongitudeRef = 'E'
    if lon < 0:
        GPSLongitudeRef = 'W'

    GPSLongitude = convert_dec_rat(lon)

    return {1: GPSLatitudeRef,
            2: GPSLatitude,
            3: GPSLongitudeRef,
            4: GPSLongitude}


# Affichage titre
st.title("Carnet de voyage")

# Première partie : insertion image légendée à partir du repo github
# https://pillow.readthedocs.io/en/stable/PIL.html#PIL.UnidentifiedImageError
r_img = requests.get(url_img)
if r_img.status_code == 200:
    img = Image.open(io.BytesIO(r_img.content))
    st.image(img, caption='Marmonie voyage')
    # img = Image.open(r_img.raw)
else:
    st.write("Problème lors du chargement de l'image")

# Première partie, suite : création formulaire et modification métadonnées exif
exif = img.getexif()

with st.form("formulaire auto de modif des données dispo"):
    st.header("Liste des métadonnées disponibles de l'image", divider="blue")
    st.write(":gray[Modifier les données souhaitées dans les boîtes correspondantes]")
    
    for k, v in exif.items():
        label = ExifTags.TAGS.get(k, k)
        # Seuls sont traités les paramètres de type chaînes et entiers
        if type(v) in (str, int) and label != "GPSInfo":
            ligne = st.columns([1, 1])
            ligne[0].subheader(label)

            if type(v) == str:
                exif[k] = ligne[1].text_input(f"{label}", value=v)

            elif type(v) == int:
                exif[k] = ligne[1].number_input(f"{label} (nombre entier)", value=v)

    # Deuxième partie : choix nouvelles coordonnées GPS (34853 = GPSInfo) https://exiftool.org/TagNames/EXIF.html
    ligne_gps = st.columns([2, 1, 1])
    ligne_gps[0].subheader("Données GPS")
    img_lat = ligne_gps[1].number_input(f"Latitude (décimal)", min_value=-90.0, max_value=90.0, value=coord_Nice[0])
    img_lon = ligne_gps[2].number_input(f"Longitude (décimal)", min_value=-180.0, max_value=180.0, value=coord_Nice[1])

    # Deuxième partie (suite) : conversion en format rational64u et édition des métadonnées GPS
    coord_exif = convert_coord(img_lat, img_lon)
    for k, v in coord_exif.items():
        exif.get_ifd(34853)[k] = v

    st.form_submit_button('Enregistrer la photo avec les nouvelles données')

"""On pourrait intégrer quelques données supplémentaires (hauteur et largeur image par exemple) en utilisant les IFD"""
# for ifd_id in ExifTags.IFD:
#     try:
#         ifd = exif.get_ifd(ifd_id)
#         for k, v in ifd.items():
#             label = ExifTags.TAGS.get(k, k)
#             print(k, label, v)
#     except KeyError:
#         pass

# Pour consulter les données de localisation
# ifd = exif.get_ifd(ExifTags.IFD.GPSInfo)
# for k, v in ifd.items():
#     label = ExifTags.GPSTAGS.get(k, k)
#     print(k, label, v)

img.save('test.jpg', exif=exif)

# liste des données exif disponibles (code, libellé et valeur)
# for k, v in exif.items():
#    print('tag', k, 'label', ExifTags.TAGS.get(k, k), 'value', v, 'type', type(v))

# Pour connaître les données exif relatives à la position GPS
# loc = ExifTags.GPSTAGS
# print(loc)
# {0: 'GPSVersionID', 1: 'GPSLatitudeRef', 2: 'GPSLatitude', 3: 'GPSLongitudeRef', 4: 'GPSLongitude', 5: 'GPSAltitudeRef', 6: 'GPSAltitude', 7: 'GPSTimeStamp', 8: 'GPSSatellites', 9: 'GPSStatus', 10: 'GPSMeasureMode', 11: 'GPSDOP', 12: 'GPSSpeedRef', 13: 'GPSSpeed', 14: 'GPSTrackRef', 15: 'GPSTrack', 16: 'GPSImgDirectionRef', 17: 'GPSImgDirection', 18: 'GPSMapDatum', 19: 'GPSDestLatitudeRef', 20: 'GPSDestLatitude', 21: 'GPSDestLongitudeRef', 22: 'GPSDestLongitude', 23: 'GPSDestBearingRef', 24: 'GPSDestBearing', 25: 'GPSDestDistanceRef', 26: 'GPSDestDistance', 27: 'GPSProcessingMethod', 28: 'GPSAreaInformation', 29: 'GPSDateStamp', 30: 'GPSDifferential', 31: 'GPSHPositioningError'}

# Troisième partie : affichage des coordonnées GPS saisies dans une carte
st.header("Dernière position connue de Marmonie…")
carte_img = folium.Map(location=(img_lat, img_lon), zoom_start=5)

folium.Marker(
    location=(img_lat, img_lon),
    tooltip='Gla gla',
    icon=folium.Icon(prefix='fa', icon='snowman', color='cadetblue')
).add_to(carte_img)

# Affichage de la carte folium dans l'appli streamlit
folium_static(carte_img)

# Quatrième partie : carte des voyages
st.header("Les Voyages de Marmonie à l'étranger")
r_voyages = requests.get(url_voyages)
if r_voyages.status_code == 200:
    liste_voyages = r_voyages.json()["voyages"]
else:
    st.write("Erreur lors du chargement de la liste de voyages.")

jointures = [[coord_Nice, dest['coord']] for dest in liste_voyages]

# Création d'une carte folium
carte_voyages = folium.Map(location=coord_Nice, zoom_start=2)

# Nice, la référence
folium.Marker(
    location=coord_Nice,
    tooltip='Nissa Bella',
    icon=folium.Icon(icon='home', color='purple')
).add_to(carte_voyages)

# Ajout des coordonnées de mes voyages et quelques infos supplémentaires
for dest in liste_voyages:
    folium.Marker(
        location=dest['coord'],
        tooltip=dest['ville'],
        popup=dest['commentaire'],
        icon=folium.Icon(prefix='fa', icon='paper-plane', color='darkpurple')
    ).add_to(carte_voyages)

# Ajout jointures de Nice vers chaque destination
folium.PolyLine(
    locations=jointures,
    color='purple',
    weight=2,
    opacity=1,
    smooth_factor=0
).add_to(carte_voyages)

# Affichage de la carte folium dans l'appli streamlit
folium_static(carte_voyages)
