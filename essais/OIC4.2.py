"""
Nom ......... : OIC4.2.py
Rôle ........ : exercice 4.2 du cours OIC pour découvrir streamlit
Auteur ...... : Orianne Delmarre
Version ..... : V0.1 du 15/03/2024
Licence ..... : réalisé dans le cadre du cours 'Outils informatiques collaboratifs' de M Kislin-Duval
    de la Licence 1 informatique de l'IED Paris 8
Version de python3 utilisée : 10.6
"""

import streamlit as st
from PIL import Image

img = Image.open('https://github.com/Marmonie/OIC/blob/main/essais/P7070925.JPG')
st.image(img, caption='Marmonie voyage')

exif = img.getexif()
exif.get_ifd(34665)[36868] = "2023:01:01 00:00:00"
img.save('test.jpg', exif = exif)
