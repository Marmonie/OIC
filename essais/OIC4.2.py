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

# Affichage image légendée à partir du repo github
# https://pillow.readthedocs.io/en/stable/PIL.html#PIL.UnidentifiedImageError
url_img = ('https://github.com/Marmonie/OIC/blob/main/essais/P7070925.jpg?raw=true')
r_img = requests.get(url_img)
if r_img.status_code == 200:
    img = Image.open(io.BytesIO(r_img.content))

#img = Image.open(r_img.raw)
st.image(img, caption='Marmonie voyage')

## Formulaire st.form
#with st.form("form : modif des données exif"):
    # Première ligne
#    auteur = st.columns([1, 3])
#    auteur[0].subheader('Auteur')
#    aut = auteur[1].text_input('Qui a pris cette photo ?')

    # Deuxième ligne
#    date = st.columns([2, 3, 3])
#    date[0].subheader('Date')
#    jour = date[1].date_input('jour')
#    heure = date[2].time_input('heure')

    # Troisième ligne
#    loc = st.columns([1, 1, 1, 1])
#    loc[0].subheader('Localisation')
#    lat = loc[1].text_input('latitude')
#    lon = loc[2].text_input('longitude')
#    alt = loc[3].text_input('altitude')

#    st.form_submit_button('Enregistrer la photo avec les nouvelles données')


exif = img.getexif()
# dic_form = {} # finalement inutile, remplacé par 'ligne'
with st.form("formulaire auto de modif des données dispo"):
    for k, v in exif.items():
        label = ExifTags.TAGS.get(k, k)
        ligne = st.columns([1, 1])
        ligne[0].subheader(label)
        if type(v) == str:
            exif[k] = ligne[1].text_input(f"{k}, donnée originale : {v}")
        elif type(v) == int:
            exif[k] = ligne[1].text_input(f"{k} (nombre entier), donnée originale : {v}")

    st.form_submit_button('Enregistrer la photo avec les nouvelles données')



# exif.get_ifd(34665)[36868] = "2023:01:01 00:00:00"
# img.save('test.jpg', exif = exif)

# liste des données exif disponibles (code, libellé et valeur)
for k, v in exif.items():
    print('tag', k, 'label', ExifTags.TAGS.get(k, k), 'value', v, 'type', type(v))
