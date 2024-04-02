from pipeline import pipeline

instruction = '''
Tu es un super rappeur Francais! Utilise ce que je te donne pour créer un rap trop cool
'''

pipeline('./input/farid.m4a', "audio", instruction)