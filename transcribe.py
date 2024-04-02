import whisper
import os

def transcribe(audio_path):
    # Initialize Whisper model
    model = whisper.load_model("large")

    # Perform transcription
    result = model.transcribe(audio_path)

    # Extract the base name of the audio file and change its extension to .txt
    base_name = os.path.basename(audio_path)
    transcript_file_name = os.path.splitext(base_name)[0] + ".txt"

    # Define the path for the output text file, in the same directory as the audio file
    output_file_path = os.path.join(os.path.dirname(audio_path), transcript_file_name)

    # Save the transcript to a text file
    with open(output_file_path, "w") as file:
        file.write(result["text"])

    print(f"Transcript saved to {output_file_path}")

    return output_file_path