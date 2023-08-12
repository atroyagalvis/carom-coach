
import streamlit as st
import pandas as pd
from datetime import date, datetime

db_filename = 'suivi_entrainement.csv'
sched_filename = 'training_schedule.csv'
work_time_unit = 3 #one percent corresponds to work_time_unit minutes
try:
    df_train = pd.read_csv(db_filename)
except FileNotFoundError:
    df_train = pd.DataFrame({
        'Temps': [],
        'Axe de travail': [],
        'Exercice': [],
        'Date': [],
        'Timestamp': [],
        'Commentaire': []
    })

df_sched = pd.read_csv(sched_filename)
today = date.today()
timestamp = datetime.now()
st.write("Today's date:", today)

st.write("Aujourd'hui tu devrais travailler:")
ideal = df_sched['Pourcentage']
ideal.index = df_sched['Axe de travail'].values
actual = df_train[['Axe de travail','Temps']].groupby('Axe de travail').agg(lambda x: x.sum()/df_train['Temps'].sum())
actual['Pourcentage'] = actual['Temps']
actual = actual['Pourcentage']
diff = work_time_unit*100*(ideal-actual).fillna(1).sort_values(ascending=False).rename('Temps recommandé')
st.write(diff)

temps = st.slider('Entrez le nombre de minutes passés à travailler', 0, 360, 30)
    
axe = st.selectbox(
    'Axe de travail',
    ('Gestuelle', 'Position aléatoire long', 'Position aléatoire large', 'Rappel long', 'Rappel large', 'Billes en lunette', 'Prises americaine', 'Série'))
st.write('Sélection:', axe)

new_ex = st.radio(
    "Exercice",
    ('Existant', 'Nouveau'))

if new_ex == 'Existant':
    exo = st.selectbox(
    'Exercice',
    df_train.Exercice.unique())
else:
    exo = st.text_input('Entrez le nom du nouvel exercice', 'Exercice')
st.write('The exercice is', exo)

comm = st.text_input('Commentaires', 'RAS')

if st.button('Valider'):
    # Insert Dict to the dataframe using DataFrame.append()
    new_row = {'Temps':temps, 
               'Axe de travail':axe, 
               'Exercice':exo, 
               'Date':today,
               'Timestamp':timestamp,
               'Commentaire': comm}
    df_train.loc[len(df_train)] = new_row
    df_train.to_csv(db_filename,  index=False)
    st.experimental_rerun()
st.write(df_train)
