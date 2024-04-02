import sys
from transcribe import transcribe

# Check if an audio file path was passed as an argument
if len(sys.argv) < 2:
    print("Usage: python transcribe_audio.py <path_to_audio_file>")
    sys.exit(1)

audio_path = sys.argv[1]

transcribe(audio_path)

