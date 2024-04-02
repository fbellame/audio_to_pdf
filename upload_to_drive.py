from googleapiclient.http import MediaFileUpload
import os
import google_drive_service

def upload_pdf(file_path, folder=None):

    service = google_drive_service.get_service()

    """
    Uploads a PDF file to Google Drive, optionally within a specific folder.

    :param service: Authenticated Google Drive service instance.
    :param file_path: Path to the PDF file to upload.
    :param folder: Name of the folder where the file will be uploaded (optional).
    :return: None
    """
    file_metadata = {
        'name': os.path.basename(file_path),
        'mimeType': 'application/pdf'
    }
    
    if folder:
        folder_id = google_drive_service.get_folder_id_by_name(service, folder)
        if folder_id:
            file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path,
                            mimetype='application/pdf',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    print(f"File ID: {file.get('id')} - '{file_path}' has been uploaded to Google Drive")