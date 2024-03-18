from fpdf import FPDF
import sys
import os

class PDF(FPDF):

    def __init__(self, title):
        super().__init__()
        # Add DejaVu Sans font
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', uni=True)
        self.title = title

    def header(self):
        self.set_font('DejaVu', '', 12)
        self.cell(0, 10, self.title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_summary_to_pdf(text, path):
    pdf = PDF(path)
    pdf.add_page()
    pdf.set_font("DejaVu", '', 12)
    pdf.multi_cell(0, 10, text)
    pdf.output(path)

def main(transcript_path, summarized_transcript):
    # [The previous script's content up to saving the summarized transcript]

    # Save the summarized transcript to a PDF file
    base_name = os.path.splitext(transcript_path)[0]  # Remove the .txt extension
    pdf_path = f'{base_name}.pdf'
    save_summary_to_pdf(summarized_transcript, pdf_path)

    print(f"The summarized transcript has been saved as a PDF to {pdf_path}")

# [The rest of the previous script]
    
# Check if an audio file path was passed as an argument
if len(sys.argv) < 2:
    print("Usage: python to_pdf.py <path_to_transcript_file>")
    sys.exit(1)    

transcript_path = sys.argv[1]

# Load the French transcript from a file
with open(transcript_path, 'r', encoding='utf-8') as file:
    summarized_transcript = file.read()

main(transcript_path, summarized_transcript)
