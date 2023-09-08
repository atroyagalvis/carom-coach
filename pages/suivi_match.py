"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime

db_filename = 'suivi_match.csv'
try:
    df_match = pd.read_csv(db_filename)
except FileNotFoundError:
    df_match = pd.DataFrame({
        'Mode jeu': [],
        'Adversaire': [],
        'Niveau adversaire': [],
        'Points': [],
        'Reprises': [],
        'Série': [],
        'Format billard': [],
        'Date': [],
        'Timestamp':[],
        'Commentaire': []
    })

today = date.today()
timestamp = datetime.now()
st.write("Aujourd'hui on est:", today)
mode_jeu = st.selectbox(
    'Mode de jeu',
    ('Libre', '1 bande', '3 bandes', 'Cadre 42/2', 'Cadre 47/2', 'Cadre 71/2', 'Cadre 47/1'))

format_billard = st.selectbox(
    'Format Billard',
    ('2.80', '3.10', 'Autre'))

st.write("Moyenne génerale:")
df_mode = df_match[(df_match['Mode jeu']==mode_jeu)&(df_match['Format billard']==float(format_billard))]

avg = df_mode['Points'].sum()/df_mode['Reprises'].sum()
st.write(avg)
nb_last_matchs = st.slider('Moyenne sur combien de matchs?', 0, 50, 10)
st.write(f"Moyenne génerale {nb_last_matchs} derniers matchs:")
df_mode = df_mode.sort_values(['Timestamp'], ascending=False).head(nb_last_matchs)
avg = df_mode['Points'].sum()/df_mode['Reprises'].sum()
st.write(avg)
st.write("Meilleure série")
best_ser = df_match['Série'].max()
st.write(best_ser)


new_adv = st.radio(
    "Adversaire",
    ('Existant', 'Nouveau'))

if new_adv == 'Existant':
    adv = st.selectbox(
    'Adversaire',
    df_match['Adversaire'].unique())
else:
    adv = st.text_input('Entrez le nom du nouvel Adversaire', '')

niv_adv = st.selectbox(
    'Mode de jeu',
    ('R4', 'R3', 'R2', 'R1', 'N3', 'N2', 'N1', 'Master'))


points = st.slider('Entrez le nombre de points', 0, 400, 100)
reprises = st.slider('Entrez le nombre de reprises', 0, 100, 20)
serie = st.slider('Entrez la meilleure série', 0, 400, 0)



comm = st.text_input('Commentaires', 'RAS')

valid = st.button('Valider')
if valid:
    # Insert Dict to the dataframe using DataFrame.append()
    new_row = {
        'Mode jeu': mode_jeu,
        'Adversaire': adv,
        'Niveau adversaire': niv_adv,
        'Points': points,
        'Reprises': reprises,
        'Série': serie,
        'Format billard': format_billard,
        'Date': today,
        'Timestamp':timestamp,
        'Commentaire': comm
    }
    df_match.loc[len(df_match)] = new_row
    
df_match = st.data_editor(df_match, num_rows="dynamic")
if st.button('Sauvegarder') or valid:
    df_match.to_csv(db_filename,  index=False)
    st.experimental_rerun()
