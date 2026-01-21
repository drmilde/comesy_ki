### https://www.youtube.com/watch?v=f1j1bR50r1c

import pyttsx3
import ollama
import json
import requests
import re

from audio import record_audio, play_audio
from utils import delete_file
from command_processing import checkCommand

import threading


import requests

def ask(question):
    response = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'system',
            'content': 'Dein Name ist Komesie und du bist ein hilfreicher KI Assistent. Sie sind ein Assistent für Aufgaben zur Beantwortung von Fragen. Verwenden Sie die folgenden Teile des abgerufenen Kontexts, um die Frage zu beantworten.',
        },
        {
            'role': 'user',
            'content': question,
        },
    ])
    return(response['message']['content'])

# pyttx3 engine
# language  : en_US, de_DE, ...
# gender    : VoiceGenderFemale, VoiceGenderMale
def change_voice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))


def sendGetRequest(url:str):
    r = requests.get(url)
    return r.status_code

def setCommand(command:str):
    statusCode = sendGetRequest(f'http://127.0.0.1:9000/command/?value={command}')
    print(statusCode)
    
def setSpeech(speech:str):
    statusCode = sendGetRequest(f'http://127.0.0.1:9000/speech/?value={speech}')
    print(statusCode)
    


### pyttx3 engine
engine = pyttsx3.init()


## configure the system 
engine.setProperty('voice', "com.apple.eloquence.de-DE.Shelley")
change_voice(engine, "de_DE", "VoiceGenderFemale")
engine.setProperty('rate', 185)



## los geht es
engine.say("Willkommen zu KoMeSie")
engine.runAndWait()


def sayit (content):
    global engine
    engine.say(content)
    engine.runAndWait()
    

def main():
    """
    Main function to run the voice assistant.
    """
    chat_history = [
        {"role": "system", "content": """ You are a helpful Assistant called Komesi. 
         You are friendly and fun and you will help the users with their requests.
         Your answers are short and concise. """}
    ]

    while True:
        try:
            # Record audio from the microphone and save it as 'test.wav'
            record_audio("test.wav")

            ## spracherkennung mit whisper.cpp
            url = 'http://127.0.0.1:8080/inference'
            files = {'file': open('test.wav', 'rb')}  # Specify the file you want to upload
            response = requests.post(url, files=files)

            ## normalisieren des Frage
            #print(response.text)
            question = json.loads(response.text)['text'].strip()
            #print (question + "\n")
            question = re.sub("\[.*\]", '', question).strip()
            print (question + "\n")

            
            # This check will avoid empty requests if vad_filter is used in the fastwhisperapi
            if not question:
                #logging.info("No transcription was returned. Starting recording again.")
                continue

            if question:
                print(checkCommand(question))
                setSpeech(question)
                setCommand(checkCommand(question))
            
            #if question:
            #    answer = ask(question)
            #    print (answer + "\n\n")
            #    answer = ask("Bitte fasse die folgende Antwort in einem Satz zusammen: \"" + question + "\"")
            #    print (answer + "\n\n")
            #    sayit(answer)

            # Check if the user wants to exit the program
            #if "goodbye" in answer.lower() or "arrivederci" in answer.lower():
            #    break

            delete_file("test.wav")

        except Exception as e:
            print(e)
            delete_file("test.wav")

if __name__ == "__main__":
    main()


