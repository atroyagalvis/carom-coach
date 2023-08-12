import streamlit as st

st.set_page_config(
    page_title="Assistant d'entrainement pour billard français",
    page_icon="👋",
)

st.write("# Assistant d'entrainement pour billard français")

st.sidebar.success("Selectionner un type de suivi")

st.markdown(
    """
    ## Bienvenue, cet outil permet de suivre et tracer votre entrainement et vos progrès
    ### Cet outil vous permet de suivre votre travail de trois manières différentes:
    - Suivi de Matchs, enregistrez le résultat de vos parties, suivez vos moyennes par mode de jeu
    - Suivi de travail générale, enregistrez le temps passé à travailler différents axes de travail (ex: gestuelle, rappels de long, prises d'americaine, etc)
    - Suivi de travail ponctuel, enregistrez votre taux de réussite sur un point particulier.
"""
)