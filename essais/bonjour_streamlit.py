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

prenom = st.text_input('st.text_input : Quel est votre prénom ?')
message = st.text_input('Quel est votre message ?')
st.write('st.write : ', message, " ", prenom)


st.header('st.header')

if st.button('st.button : Say hello'):
     st.write('Why hello there')
else:
     st.write('Goodbye')

img = Image.open('P7070925.JPG')
st.image(img, caption='Marmonie voyage')

exif = img.getexif()
exif.get_ifd(34665)[36868] = "2023:01:01 00:00:00"
img.save('test.jpg', exif = exif)
