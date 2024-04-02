import sys
from pdf_tool import to_pdf

# [The rest of the previous script]
    
# Check if an audio file path was passed as an argument
if len(sys.argv) < 2:
    print("Usage: python to_pdf.py <path_to_transcript_file>")
    sys.exit(1)    

transcript_path = sys.argv[1]


to_pdf(transcript_path)
