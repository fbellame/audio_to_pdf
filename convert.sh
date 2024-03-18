#!/bin/bash

# Initialize skip_generated flag
skip_generated=0

# Check for the -skip generated option
if [[ "$1" == "-skip" && "$2" == "generated" ]]; then
    skip_generated=1
    shift 2
fi

# Check if an audio file path was passed as an argument
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 [-skip generated] <path_to_m4a_file> <drive_folder>"
    exit 1
fi

M4A_FILE="$1"
DRIVE_FOLDER="$2"
WAV_FILE="${M4A_FILE%.*}.wav"
TXT_FILE="${M4A_FILE%.*}.txt"
SUMMARY_FILE="${M4A_FILE%.*}_summary.txt"
PDF_FILE="${M4A_FILE%.*}_summary.pdf"

# Convert M4A to WAV using ffmpeg
if [ $skip_generated -eq 0 ] || [ ! -f "$WAV_FILE" ]; then
    echo "Starting conversion from M4A to WAV..."
    ffmpeg -i "$M4A_FILE" "$WAV_FILE"
    if [ $? -ne 0 ]; then
        echo "Conversion failed."
        exit 1
    fi
    echo "Conversion completed successfully."
else
    echo "$WAV_FILE already exists, skipping conversion."
fi

# Transcribe WAV to TXT
if [ $skip_generated -eq 0 ] || [ ! -f "$TXT_FILE" ]; then
    echo "Starting transcription from WAV to TXT..."
    python transcribe_audio.py "$WAV_FILE"
    if [ $? -ne 0 ]; then
        echo "Transcription failed."
        exit 1
    fi
    echo "Transcription completed successfully."
else
    echo "$TXT_FILE already exists, skipping transcription."
fi

# Process TXT to generate SUMMARY_FILE
if [ $skip_generated -eq 0 ] || [ ! -f "$SUMMARY_FILE" ]; then
    echo "Starting summary processing..."
    python process.py "$TXT_FILE"
    if [ $? -ne 0 ]; then
        echo "Summary processing failed."
        exit 1
    fi
    echo "Summary processing completed successfully."
else
    echo "$SUMMARY_FILE already exists, skipping summary processing."
fi

# Generate PDF from SUMMARY_FILE
if [ $skip_generated -eq 0 ] || [ ! -f "$PDF_FILE" ]; then
    echo "Starting PDF generation from summary..."
    python to_pdf.py "$SUMMARY_FILE"
    if [ $? -ne 0 ]; then
        echo "PDF generation failed."
        exit 1
    fi
    echo "PDF generation completed successfully."
else
    echo "$PDF_FILE already exists, skipping PDF generation."
fi

# Upload PDF to Google Drive
echo "Uploading PDF to google drive..."
python upload_pdf.py "$PDF_FILE" --folder "$DRIVE_FOLDER"
if [ $? -ne 0 ]; then
    echo "PDF upload failed."
    exit 1
fi
echo "PDF uploaded to google drive completed successfully."

echo " ---> Audio $M4A_FILE processed with success, generated $PDF_FILE uploaded to Google Drive to $DRIVE_FOLDER !!"
