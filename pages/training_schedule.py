
import streamlit as st
import pandas as pd
from datetime import date
  
db_filename = 'training_schedule.csv'
try:
    df_sched = pd.read_csv(db_filename)
except FileNotFoundError:
    df_sched = pd.DataFrame({
        'Coef':[],
        'Axe de travail': [],
        'Pourcentage': []
    })

axe = st.selectbox(
    'Axe de travail',
    ('Gestuelle', 'Position aléatoire long', 'Position aléatoire large', 'Rappel long', 'Rappel large', 'Billes en lunette', 'Prises americaine', 'Série'))
coef = st.number_input('Entrez le coefficient à travailler sur cet axe: (ce coefficient sera normalisé sur tous les axes de travail pour arriver à 100%)', 0)

valid = st.button('Valider')
if valid:
    current_axe = df_sched[df_sched['Axe de travail']==axe]
    new_row = {'Coef':coef, 'Axe de travail':axe, 'Pourcentage':coef/df_sched['Coef'].sum()}
    
    if len(current_axe) == 0:
        df_sched.loc[len(df_sched)] = new_row
    else:
        df_sched.loc[df_sched['Axe de travail']==axe,'Coef'] = coef
    df_sched['Pourcentage'] = df_sched['Coef']/df_sched['Coef'].sum()

df_sched = st.data_editor(df_sched, num_rows="dynamic")
if st.button('Sauvegarder') or valid:
    df_sched.to_csv(db_filename,  index=False)
    st.experimental_rerun()