import streamlit as st
from googleapiclient.http import MediaFileUpload
from google_drive_service import get_service, get_folder_id_by_name
from pipeline import pipeline
import os
import base64

instruction_histoire = '''
Vous êtes un tuteur d'histoire expert, concentré sur les dates importantes, les villes et les noms. Rendez-le concis pour un étudiant à apprendre.

IMPORTANT

Les dates des événements principaux (plus par repère temporel que pour la mémorisation)
Les noms des personnages clés (plus par repère que pour la mémorisation)
Les causes des événements
Les motivations, buts ou objectifs des personnages/empires
Les réformes ou les innovations
Les stratégies pour atteindre ses objectifs
Les réactions des deux peuples lors des premiers contacts
Les conséquences des événements
  MOINS IMPORTANT

Les mises en contexte générales entre deux sujets
Les anecdotes
Le déroulement des batailles
La description physique des personnages
'''

instruction_rap = '''Tu es un super rappeur Francais! Utilise ce que je te donne pour créer un rap trop cool'''

upload_folder = "audio"
temp_folder = "./tmp"

# Function to upload file to Google Drive
def upload_file_to_drive(file_name, file_path):

    service = get_service()

    folder_id = get_folder_id_by_name(service, upload_folder)

    # File metadata and upload
    file_metadata = {'name': file_name, 'parents': [folder_id]}
    media = MediaFileUpload(file_path, mimetype='audio/mp4a-latm')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')


# Streamlit app interface
def main():
    st.title('Audio vers PDF avec un prompt style')

    # Add dropdown for selecting prompt type
    prompt_type = st.selectbox("Choisi le type de prompt:", ["Rap", "Histoire"])    

    instruction = instruction_rap if prompt_type == "Rap" else instruction_histoire
    
    uploaded_file = st.file_uploader("Choisi le fichier audio (format m4a normalement sur ton télephone)", type='m4a')
    if uploaded_file is not None:

        tmp_file = os.path.join(temp_folder, uploaded_file.name)
        # Save uploaded file to temporary directory
        with open(tmp_file, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Upload to Google Drive
        file_id = upload_file_to_drive(tmp_file, tmp_file)
        st.success(f"Le fichier vient d'être sauvegardé dans Google Drive avec l'ID: {file_id}")

        st.success(f"Appel du pipeline de conversion...")
        # Assuming pipeline function now returns the path to the generated PDF
        pdf_file_path = pipeline(tmp_file, upload_folder, instruction)

        st.success('Pipeline exécuté avec succès.')

        # Display the PDF in the app
        if pdf_file_path:
            with open(pdf_file_path, "rb") as pdf_file:
                base64_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)

if __name__ == "__main__":
    main()