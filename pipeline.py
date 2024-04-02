from transcribe import transcribe
from summarize import summarize
import ffmpeg
from upload_pdf import upload_pdf
from pdf_tool import to_pdf
from upload_to_drive import upload_pdf
from pathlib import Path

def file_exists(file_path, skip_generated):
    """Check if file exists and whether to skip if it does."""
    if file_path.exists() and skip_generated:
        print(f"{file_path} already exists, skipping.")
        return True
    return False

def convert(input_file, output_file):
    # Ensure paths are strings representing absolute paths
    input_path = str(input_file.absolute())
    output_path = str(output_file.absolute())
    
    # Execute conversion
    ffmpeg.input(input_path).output(output_path).run(overwrite_output=True)

def convert_to_wav(m4a_file, skip_generated):

    m4a_file = Path(m4a_file)
    wav_file = m4a_file.with_suffix('.wav')
    if not file_exists(wav_file, skip_generated):
        print(f"Starting conversion from M4A to WAV for {m4a_file}...")

        convert(m4a_file.absolute(), wav_file.absolute())

        print("Conversion completed successfully.")
    return wav_file

def transcribe_audio(wav_file, skip_generated):

    wav_file = Path(wav_file)
    txt_file = wav_file.with_suffix('.txt')
    if not file_exists(txt_file, skip_generated):
        print(f"Starting transcription from WAV to TXT for {wav_file}...")
        txt_file = transcribe(str(wav_file.absolute()))

        print("Transcription completed successfully.")
    return txt_file

def process_text(txt_file, prompt, skip_generated):

    txt_file = Path(txt_file)
    summary_file = txt_file.with_suffix('.txt').with_name(f"{txt_file.stem}_summary.txt")
    if not file_exists(summary_file, skip_generated):
        print("Starting summary processing...")
        summary_file = summarize(txt_file, prompt)

        print("Summary processing completed successfully.")
    return summary_file

def generate_pdf(summary_file, skip_generated):

    summary_file = Path(summary_file)
    pdf_file = summary_file.with_suffix('.pdf')
    if not file_exists(pdf_file, skip_generated):
        print("Starting PDF generation from summary...")
        to_pdf(summary_file)
        print("PDF generation completed successfully.")
    return pdf_file

def upload(pdf_file, drive_folder):
    print("Uploading PDF to Google Drive...")
    upload_pdf(pdf_file, drive_folder)

    print("PDF uploaded to Google Drive successfully.")

def pipeline(m4a_file, drive_folder, prompt):

    wav_file = convert_to_wav(m4a_file, True)
    txt_file = transcribe_audio(wav_file, True)
    summary_file = process_text(txt_file, prompt, True)
    pdf_file = generate_pdf(summary_file, True)
    upload(pdf_file, drive_folder)

    print(f" ---> Audio {m4a_file} processed with success, generated {pdf_file} uploaded to Google Drive to {drive_folder} !!")

    return pdf_file

