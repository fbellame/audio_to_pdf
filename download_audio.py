import io
from googleapiclient.http import MediaIoBaseDownload
import os
from google_drive_service import SCOPES, get_service
import argparse

def main(folder, download_dir):

    service = get_service()

    # Find the ID of the folder named 'folder'
    folder_id = ''

    if folder is None:
        query = "'root' in parents and mimeType = 'application/vnd.google-apps.folder'"
    else:
        query = f"name = '{folder}' and mimeType = 'application/vnd.google-apps.folder'"

    print(f"query='{query}'")

    results = service.files().list(q=query, spaces='drive', fields="nextPageToken, files(id, name)").execute()

    print(f"results={results}")

    for folder in results.get('files', []):
        folder_id = folder['id']
        break

    if not folder_id:
        print(f"{folder} folder not found.")
        return

    print(f"{folder} folder ID: {folder_id}")

    query = f"'{folder_id}' in parents and name contains '.m4a'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    if not items:
        print("No .m4a files found.")
    else:
        for item in items:
            file_id = item['id']
            original_file_name = item['name']
            sanitized_file_name = original_file_name.replace(' ', '_')
            file_path = os.path.join(download_dir, sanitized_file_name)

            # Skip downloading if file already exists
            if os.path.exists(file_path):
                print(f"{sanitized_file_name} already exists in '{download_dir}'. Skipping download.")
                continue

            print(f"Downloading {sanitized_file_name} into folder '{download_dir}'...")

            request = service.files().get_media(fileId=file_id)
            fh = io.FileIO(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)

            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")

            print(f"{sanitized_file_name} has been downloaded.")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Download Audio file to Google Drive.")
    parser.add_argument("--folder", help="The name of the drive folder to download the file from.", default=None)
    parser.add_argument("--download_dir", help="The name of the local folder to download the file to.", default=None)

    args = parser.parse_args()

    print(f"args.folder={args.folder}")
    print(f"args.download_dir={args.download_dir}")

    main(folder = args.folder, download_dir = args.download_dir)
