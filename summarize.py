from openai import OpenAI
import os
import sys

# Load API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Function to split the text into chunks that are smaller than the model's maximum token limit
def split_text(text, max_chunk_size=2000):
    # Split the text by full stops to ensure sentences are not cut in half
    sentences = text.split('. ')
    current_chunk = ""
    chunks = []

    for sentence in sentences:
        if len(current_chunk) + len(sentence.split()) < max_chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + ". "
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

# Function to summarize a chunk of text
def summarize_chunk(chunk, prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",  
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Veuillez résumer cet extrait d'histoire: {chunk}"}
        ],
        temperature=0.3,
        max_tokens=4000,  # Load your OpenAI API key
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    return response.choices[0].message.content.strip()

# Function to summarize the entire transcript
def summarize_transcript(transcript, prompt):
    # Split the transcript into chunks
    chunks = split_text(transcript)
    summaries = []

    # Summarize each chunk
    for chunk in chunks:
        summary = summarize_chunk(chunk, prompt)
        summaries.append(summary)
    
    # Combine the summaries
    return ' '.join(summaries)

def summarize(transcript_path, prompt):
    # Load the French transcript from a file
    with open(transcript_path, 'r', encoding='utf-8') as file:
        french_transcript = file.read()

    # Summarize the transcript
    summarized_transcript = summarize_transcript(french_transcript, prompt)

    # Before summarizing the transcript and saving it, modify the output file name correctly
    transcript_base_name = os.path.splitext(transcript_path)[0]  # Remove the .txt extension

    # Save the summarized transcript to a new file, with the modified file naming convention
    output_file_name = f'{transcript_base_name}_summary.txt'  # Corrected output file name
    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(summarized_transcript)

    print(f"The summarized transcript has been saved to {output_file_name}")

    return output_file_name
