import json
import os

PERSONA_PATH = "backend/persona/configs"

def load_personas():

    personas = []

    for file in os.listdir(PERSONA_PATH):

        # .json биш файлуудыг (жнь __pycache__, .DS_Store) алгасана
        if not file.endswith(".json"):
            continue

        path = os.path.join(PERSONA_PATH, file)

        with open(path, "r", encoding="utf-8") as f:

            data = json.load(f)

            personas.append(data)

    return personas