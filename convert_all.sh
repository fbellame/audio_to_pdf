#!/bin/bash

DRIVE_FOLDER="audio"
INPUT_FOLDER="input"

# Step 1: Call your Python script to download .m4a files into the "input" folder
python3 download_audio.py --folder "$DRIVE_FOLDER" --download_dir "$INPUT_FOLDER"

# Check if the "input" folder exists and has .m4a files
if [ -d "$INPUT_FOLDER" ] && [ "$(ls -A $INPUT_FOLDER/*.m4a 2> /dev/null)" ]; then
    # Step 2: Iterate over each .m4a file in the "input" folder
    for file in $INPUT_FOLDER/*.m4a; do
        echo "Processing $file..."

        # Step 3: Call your conversion script with the path to the .m4a file
        ./convert.sh -skip generated "$file" "$DRIVE_FOLDER"

        echo "Conversion completed for $file"
    done
else
    echo "No .m4a files found in 'input' folder or 'input' folder does not exist."
fi
