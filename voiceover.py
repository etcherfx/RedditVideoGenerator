import json

import pyttsx3

from setup import configFilePath

with open(configFilePath) as c:
    config = json.load(c)
    voiceoverDir = config["General"]["VoiceoverDirectory"]
c.close()


def create_voice_over(fileName, text):
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    engine = pyttsx3.init()
    engine.save_to_file(text, filePath)
    engine.runAndWait()
    return filePath
