import streamlit as st
import pandas as pd
from datetime import date, datetime

db_filename = 'suivi_point.csv'
try:
    df_point= pd.read_csv(db_filename)
except FileNotFoundError:
    df_point = pd.DataFrame({
        'Nom point': [],
        'Type point': [],
        'Réussites': [],
        'Essais': [],
        'Date': [],
        'Timestamp':[],
        'Commentaire': []    
        })

today = date.today()
timestamp = datetime.now()
st.write("Aujourd'hui on est:", today)

type_point = st.selectbox(
    'Type de point',
    ('Rappel de long', 'Rappel de large', 'Prise americaine', 'Prise ligne', 'Billes en lunette', '3 bandes'))

st.write("Dernier point travaillé:")
last = df_point[df_point['Type point']==type_point].sort_values('Timestamp', ascending=False).head(1)
st.write(last)

new_ex = st.radio(
    "Point",
    ('Existant', 'Nouveau'))

if new_ex == 'Existant':
    exo = st.selectbox(
    'Point',
    df_point['Nom point'].unique())
else:
    exo = st.text_input('Entrez le nom du nouvel exercice', 'Exercice')

attempts = st.slider('Entrez le nombre d\'essais', 0, 50, 10)
success = st.slider('Entrez le nombre de réussites', 0, 50, 1)


comm = st.text_input('Commentaires', 'RAS')

if st.button('Valider'):
    # Insert Dict to the dataframe using DataFrame.append()
    new_row = {
        'Nom point': exo,
        'Type point': type_point,
        'Réussites': success,
        'Essais': attempts,
        'Date': today,
        'Timestamp': timestamp,
        'Commentaire': comm    
        }
    df_point.loc[len(df_point)] = new_row
    df_point.to_csv(db_filename,  index=False)
    st.experimental_rerun()

st.write(df_point)
    