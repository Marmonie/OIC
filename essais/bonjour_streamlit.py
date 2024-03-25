"""
Nom ......... : S2OIC_c4demoST.py
Rôle ........ : code pour découvrir streamlit
Auteur ...... : Orianne Delmarre
Version ..... : V0.1 du 14/03/2024
Licence ..... : réalisé dans le cadre du cours 'Outils informatiques collaboratifs' de M Kislin-Duval
    de la Licence 1 informatique de l'IED Paris 8
Version de python3 utilisée : 10.6
"""

import streamlit as st
from PIL import Image

prenom = st.text_input('text_input : Quel est votre prénom ?')
message = st.text_input('Quel est votre message ?')
st.write('write : ', message, " ", prenom)


st.header('header')

if st.button('button : Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

img = Image.open('P7070925.jpg')
st.image(img, caption='image : Marmonie voyage')

# Formulaire st.form
with st.form("form : modif des données exif"):
    # Première ligne
    titres = st.columns([1, 1, 1])
    titres[0].subheader('auteur')
    titres[1].subheader('date')
    titres[2].subheader('lieu')

    # Deuxième ligne
    ligne1 = st.columns([1, 1, 1])
    auteur = ligne1[0].text_input('Qui sera l’auteur de cette photo ?')
    date = ligne1[1].date_input('Quel jour voulez-vous la prendre ?')
    coord_gps = ligne1[2].text_input('Où ça ?')

    st.form_submit_button('form_submit_button : enregistrer la photo avec les nouvelles données')

exif = img.getexif()
print('exif = ', exif)
exif.get_ifd(34665)[36868] = "2023:01:01 00:00:00"
img.save('test.jpg', exif = exif)

print(auteur, date, coord_gps)
