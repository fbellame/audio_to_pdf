import argparse
from upload_to_drive import upload_pdf

def main():
    parser = argparse.ArgumentParser(description="Upload a PDF file to Google Drive.")
    parser.add_argument("file_path", help="Path to the PDF file to upload.")
    parser.add_argument("--folder", help="The name of the folder to upload the file to.", default=None)
    
    args = parser.parse_args()
    
    upload_pdf(args.file_path, folder=args.folder)

if __name__ == '__main__':
    main()
