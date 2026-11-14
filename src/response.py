###This File is used to handle messages and reply as needed###
import discord
import json
from pathlib import Path
import random
import re
import mention as men

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

def get_greetings(bin):
    return random.choice(responses["Greetings"])

def mention(anything):
    return men.ping(anything, "")


def process_text(text, placeholder: str):
    return re.sub(fr"{placeholder}\((.*?)\)", lambda match: str(globals()[placeholder](match.group(1))), text)

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
            return process_text(response.replace("%!", message.removeprefix(trigger.strip("%!") + " ")), responses["Chelper"][trigger.strip("%!")])
            

    return None

def reload_files():
    global responses
    global Responses_PATH

    try:
        with open(Responses_PATH, "r") as file:
            responses = json.load(file)
        return "Reloaded responses succesfully"
    except Exception as exception:
        print("Could not Load Responses")
        print(exception)
        return f"Could not Load responses {exception}"
