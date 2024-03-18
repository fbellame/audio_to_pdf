from googleapiclient.http import MediaFileUpload
import os
import argparse
import google_drive_service

def get_folder_id_by_name(service, folder_name):
    """
    Searches for a folder by name and returns its ID.

    :param service: Authenticated Google Drive service instance.
    :param folder_name: Name of the folder to find.
    :return: ID of the found folder or None if not found.
    """
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
    folders = response.get('files', [])
    
    if folders:
        return folders[0].get('id')
    else:
        print(f"Folder '{folder_name}' not found.")
        return None

def upload_pdf(service, file_path, folder=None):
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
        folder_id = get_folder_id_by_name(service, folder)
        if folder_id:
            file_metadata['parents'] = [folder_id]
    
    media = MediaFileUpload(file_path,
                            mimetype='application/pdf',
                            resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    print(f"File ID: {file.get('id')} - '{file_path}' has been uploaded to Google Drive")

def main():
    parser = argparse.ArgumentParser(description="Upload a PDF file to Google Drive.")
    parser.add_argument("file_path", help="Path to the PDF file to upload.")
    parser.add_argument("--folder", help="The name of the folder to upload the file to.", default=None)
    
    args = parser.parse_args()
    
    service = google_drive_service.get_service()
    upload_pdf(service, args.file_path, folder=args.folder)

if __name__ == '__main__':
    main()
