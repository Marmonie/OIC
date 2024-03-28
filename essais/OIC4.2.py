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

CoordGPSNice = {
    'GPSLatitudeRef': 'N', 
    'GPSLatitude': (41.0, 47.0, 2.17),
    'GPSLongitudeRef': 'W', 
    'GPSLongitude': (93.0, 46.0, 42.09)}

# Affichage titre
st.title("Carnet de voyage")

# Affichage image légendée à partir du repo github
# https://pillow.readthedocs.io/en/stable/PIL.html#PIL.UnidentifiedImageError
url_img = ('https://github.com/Marmonie/OIC/blob/main/essais/P7070925.jpg?raw=true')
r_img = requests.get(url_img)
if r_img.status_code == 200:
    img = Image.open(io.BytesIO(r_img.content))

#img = Image.open(r_img.raw)
st.image(img, caption='Marmonie voyage')

exif = img.getexif()
GPS_tag = 0

## Formulaire st.form
with st.form("formulaire auto de modif des données dispo"):
    st.header("Liste des métadonnées disponibles de l'image", divider="blue")
    st.write(":gray[Entrer les nouvelles données dans les boîtes correspondantes]")
    
    for k, v in exif.items():
        label = ExifTags.TAGS.get(k, k)
        ligne = st.columns([1, 1])
        ligne[0].subheader(label)

        # Ajout coord GPS de Nice, https://exiftool.org/TagNames/EXIF.html
        if label == 'GPSInfo':
        #    exif[k] = CoordGPSNice
            GPS_tag = k
            print(GPS_tag)

        # Seuls sont traités les paramètres de type chaînes et entiers
        if type(v) == str:
            exif[k] = ligne[1].text_input(f"{label}, donnée originale : {v}")
        
        elif type(v) == int:
            exif[k] = ligne[1].text_input(f"{k} (nombre entier), donnée originale : {v}")
            # Les entiers sont convertis si possible, sinon on garde la valeur d'origine
            try:
                exif[k] = int(exif[k])
            except:
                exif[k] = v

        
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

# Modif des coord GPS (34853 = GPSInfo)
for k, v in CoordGPSNice.items():
    exif.get_ifd(34853)[k] = v

img.save('test.jpg', exif = exif)

# liste des données exif disponibles (code, libellé et valeur)
#for k, v in exif.items():
#    print('tag', k, 'label', ExifTags.TAGS.get(k, k), 'value', v, 'type', type(v))

# Pour connaître les données exif relatives à la position GPS
#loc = ExifTags.GPSTAGS
#print(loc)
#{0: 'GPSVersionID', 1: 'GPSLatitudeRef', 2: 'GPSLatitude', 3: 'GPSLongitudeRef', 4: 'GPSLongitude', 5: 'GPSAltitudeRef', 6: 'GPSAltitude', 7: 'GPSTimeStamp', 8: 'GPSSatellites', 9: 'GPSStatus', 10: 'GPSMeasureMode', 11: 'GPSDOP', 12: 'GPSSpeedRef', 13: 'GPSSpeed', 14: 'GPSTrackRef', 15: 'GPSTrack', 16: 'GPSImgDirectionRef', 17: 'GPSImgDirection', 18: 'GPSMapDatum', 19: 'GPSDestLatitudeRef', 20: 'GPSDestLatitude', 21: 'GPSDestLongitudeRef', 22: 'GPSDestLongitude', 23: 'GPSDestBearingRef', 24: 'GPSDestBearing', 25: 'GPSDestDistanceRef', 26: 'GPSDestDistance', 27: 'GPSProcessingMethod', 28: 'GPSAreaInformation', 29: 'GPSDateStamp', 30: 'GPSDifferential', 31: 'GPSHPositioningError'}
