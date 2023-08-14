import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()           
drive = GoogleDrive(gauth) 

#TODO: this is pointing directly to a specific drive account, should be more general if the app is to be used by other users
def upload_files():
	carom_coach_drive_id = '18TdPUHCgpT9azjv1Qb4z4c6bmfd-jlim'
	upload_file_list = ['suivi_match.csv', 'suivi_point.csv', 'training_schedule.csv', 'suivi_entrainement.csv']

	files = drive.ListFile({'q': f"'{carom_coach_drive_id}' in parents and trashed=false"}).GetList()
	existing_titles = [f['title'] for f in files]
	ids = {f['title']: f['id'] for f in files}
	for upload_file in upload_file_list:
		if upload_file in existing_titles:
			gfile = drive.CreateFile({'id': ids[upload_file]})
		else:
			gfile = drive.CreateFile({'parents': [{'id': carom_coach_drive_id}]})
		# Read file and set it as the content of this instance.
		gfile.SetContentFile(upload_file)
		gfile.Upload() # Upload the file.

def get_files():
	carom_coach_drive_id = '18TdPUHCgpT9azjv1Qb4z4c6bmfd-jlim'
	download_file_list = ['suivi_match.csv', 'suivi_point.csv', 'training_schedule.csv', 'suivi_entrainement.csv']

	files = drive.ListFile({'q': f"'{carom_coach_drive_id}' in parents and trashed=false"}).GetList()

	for upload_file in files:
		if upload_file['title'] in download_file_list:
			gfile = drive.CreateFile({'id': upload_file['id']})
			# Read file and set it as the content of this instance.
			gfile.GetContentFile(upload_file['title'])

st.set_page_config(
    page_title="Assistant d'entrainement pour billard français",
    page_icon="icon.png",
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

if st.button('Save '):
    upload_files()
    st.write('All files were saved')
else:
    st.write('Save files to google drive')

if st.button('Load'):
    get_files()
    st.write('All files were recovered from drive')
else:
    st.write('Get updated files from google drive')
