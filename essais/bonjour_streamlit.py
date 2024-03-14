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
prenom = st.text_input('Quel est votre prénom ?')
message = st.text_input('Quel est votre message ?')
st.write(message, " ", prenom)
