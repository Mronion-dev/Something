###This File is used to handle messages and reply as needed###
import discord
import json
from pathlib import Path
import random
import re
import mention

responses = {}
Responses_PATH = Path(__file__).resolve().parent / "Responses.json"

def main():
    global responses
    global Responses_PATH

    try:
        with open(Responses_PATH, "r") as file:
            responses = json.load(file)
    except Exception as exception:
        print("Could not Load Responses")
        print(exception)
        
def functionas(text: str):
    return mention.ping(text, "")

def process_text(text):
    return re.sub(r"{mention\((.*?)\)}", lambda match: str(functionas(match.group(1))), text)

def check_response(message: str):
    # Check for typos (list of strings)
    for typo in responses["Typos"]:
        if typo in message:
            return typo + " :face_holding_back_tears:"

    # Check Jarvis responses (dictionary)
    if 'jarvis' in message:
        for trigger, response in responses["Jarvis"].items():
            if trigger in message:
                return random.choice(response.split("|"))

    # Check Normal responses (dictionary)
    for trigger, response in responses["Normal"].items():
        if trigger in message:
            return random.choice(response.split("|"))

    # Check action responses (dictionary)
    for trigger, response in responses["Custom"].items():
        if message.startswith(trigger.strip("%!")):
            return process_text(response.replace("%!", message.removeprefix(trigger.strip("%!") + " ")))
            

    return None


