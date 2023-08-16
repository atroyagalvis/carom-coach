
import streamlit as st
import pandas as pd
from datetime import date, datetime

db_filename = 'suivi_entrainement.csv'
sched_filename = 'training_schedule.csv'
base_train_time = 30 # minutes
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
df_sched.index = df_sched['Axe de travail'].values
ideal_time = df_sched['Pourcentage']*df_train['Temps'].sum()
actual_time = df_train[['Axe de travail','Temps']].groupby('Axe de travail').agg(lambda x: x.sum())
actual_time['Temps passé'] = actual_time['Temps']
actual_time = actual_time['Temps passé']
needed = (ideal_time-actual_time).fillna(base_train_time)
#.fillna(1)#.sort_values(ascending=False).rename('Temps recommandé')

df_sched['Temps ideal'] = actual_time
df_sched['Temps passé'] = actual_time
df_sched['Temps recommandé'] = needed
df_sched['Pourcentage Ideal'] = df_sched['Pourcentage']*100
df_sched['Pourcentage passé'] = actual_time/df_train['Temps'].sum()*100

st.write(df_sched[['Pourcentage Ideal','Pourcentage passé', 'Temps recommandé']].sort_values('Temps recommandé',ascending=False))

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
