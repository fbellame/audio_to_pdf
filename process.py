import os
import sys
import summarize

instruction = '''
Vous êtes un tuteur d'histoire expert, concentré sur les dates importantes, les villes et les noms. Rendez-le concis pour un étudiant à apprendre.

IMPORTANT

Les dates des événements principaux (plus par repère temporel que pour la mémorisation)
Les noms des personnages clés (plus par repère que pour la mémorisation)
Les causes des événements
Les motivations, buts ou objectifs des personnages/empires
Les réformes ou les innovations
Les stratégies pour atteindre ses objectifs
Les réactions des deux peuples lors des premiers contacts
Les conséquences des événements
  MOINS IMPORTANT

Les mises en contexte générales entre deux sujets
Les anecdotes
Le déroulement des batailles
La description physique des personnages
'''

# Check if an audio file path was passed as an argument
if len(sys.argv) < 2:
    print("Usage: python process.py <path_to_transcript_file>")
    sys.exit(1)

transcript_path = sys.argv[1]

# Summarize the transcript
summarized_transcript = summarize.summarize(transcript_path, instruction)

# Before summarizing the transcript and saving it, modify the output file name correctly
transcript_base_name = os.path.splitext(transcript_path)[0]  # Remove the .txt extension

# Save the summarized transcript to a new file, with the modified file naming convention
output_file_name = f'{transcript_base_name}_summary.txt'  # Corrected output file name
with open(output_file_name, 'w', encoding='utf-8') as file:
    file.write(summarized_transcript)

print(f"The summarized transcript has been saved to {output_file_name}")