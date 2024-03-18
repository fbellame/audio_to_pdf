# Audio Processing and Conversion Pipeline

This repository contains a set of Bash and Python scripts designed to automate the process of downloading audio files, converting them from M4A to WAV format, transcribing the audio to text, summarizing the text, and finally generating a PDF document from the summary. The PDF document is then uploaded to a specified Google Drive folder.

## Prerequisites

Before running the scripts, ensure you have the following installed on your system:
- `ffmpeg`: Used for converting audio files from M4A to WAV format.
- Python 3.x: Required to run the Python scripts for transcription, summarization, PDF generation, and uploading the PDF to Google Drive.
- Required Python packages: Install the necessary Python packages by running:


## Setup

```bash
pip install -r requirements.txt
```

1. **Configure Script Variables**: Before running the script, you may need to adjust the `DRIVE_FOLDER` and `INPUT_FOLDER` variables at the top of the script to match your desired Google Drive folder name and local input directory, respectively.

    ```bash
    DRIVE_FOLDER="audio"
    INPUT_FOLDER="input"
    ```

2. **Ensure Script Executability**: Make sure that the script is executable by running the following command:

    ```bash
    chmod +x convert_all.sh
    ```


## Obtaining Google API Credentials

To enable this script to upload files to Google Drive, you must obtain a `credentials.json` file by creating a project in the Google Developers Console and enabling the Drive API. Follow these steps to generate your credentials:

1. **Create a Project in Google Cloud Platform (GCP)**:
    - Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
    - Click on the project dropdown near the top-left corner and then click on "New Project".
    - Enter a project name and click "Create".

2. **Enable the Drive API**:
    - With your project selected, navigate to the "APIs & Services > Dashboard" panel.
    - Click on "ENABLE APIS AND SERVICES" at the top.
    - Search for "Google Drive API", select it, and click "Enable".

3. **Create Credentials**:
    - In the API & Services Dashboard, navigate to "Credentials" using the left-hand menu.
    - Click on "Create Credentials" at the top of the page and select "OAuth client ID".
    - If prompted, configure the OAuth consent screen by selecting an "External" user type and providing the necessary information. Save and continue.
    - Back in the "Create OAuth client ID" screen, select "Desktop app" as the application type, give it a name, and click "Create".
    - Your credentials (`client_id` and `client_secret`) will be displayed. Click "OK".

4. **Download the Credentials**:
    - In the Credentials page, find the OAuth 2.0 Client IDs section and click on the download button to the right of your newly created OAuth client ID.
    - This will download a JSON file, which you should rename to `credentials.json` and place in the same directory as the script.

### Setting Up Your `credentials.json`

After downloading your `credentials.json`, ensure it is placed in the root directory of your project or in a directory from which your scripts are configured to read the credentials.

### First Run

Upon the first run of the script that requires Google Drive API access, you will be prompted to authenticate via a browser. This process grants the script permission to access your Google Drive based on the scopes defined in your code. Once authenticated, an access token will be stored, which allows future script executions without manual authentication.

For more detailed information on setting up OAuth 2.0 credentials for a desktop application, refer to the official Google Developer documentation: [Using OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app).

## Troubleshooting Google API Credentials

If you encounter issues with `credentials.json` or authentication:
- Ensure the `credentials.json` file is correctly placed and accessible by the script.
- Verify that the Google Drive API is enabled for your project in the Google Cloud Console.
- Check that the OAuth consent screen is correctly configured and published if required.

For any permission or access errors, reviewing the OAuth consent screen and the scope of API access in your Google Cloud Project settings may provide insight into the issue.

## Contributing

We appreciate contributions and suggestions for enhancing the script's functionality or documentation. If you have improvements or fixes, please feel free to fork the repository, commit your changes, and submit


## Usage Instructions

To use the script, simply run it from your terminal:

```bash
./convert_all.sh



