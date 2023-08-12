import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
db_train = 'suivi_entrainement.csv'
db_point = 'suivi_point.csv'
db_match = 'suivi_match.csv'

df_train = pd.read_csv(db_train)
df_point = pd.read_csv(db_point)
df_match = pd.read_csv(db_match)
st.write('hello')

mode_jeu = st.selectbox(
    'Mode de jeu',
    ('Libre', '1 bande', '3 bandes', 'Cadre 42/2', 'Cadre 47/2', 'Cadre 71/2', 'Cadre 47/1'))

df_stat = df_match[df_match['Mode jeu']==mode_jeu]
df_stat.index = df_stat['Timestamp']
fig = plt.figure()

for g, x in df_stat.groupby('Niveau adversaire'):
    plt.hist(x['Points']/x['Reprises'], label=g, bins=20)
plt.title('Distribution moyenne')
plt.ylabel('Cumul')
plt.xlabel('Moyenne')
plt.legend()
st.pyplot(fig)

fig = plt.figure()
plt.hist(df_stat['Série'].values, bins=20)
plt.title('Distribution séries')
plt.ylabel('Cumul')
plt.xlabel('Série')
st.pyplot(fig)