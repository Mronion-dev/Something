import discord
from discord.ext import commands
from discord import app_commands

import mention
import response

import time
import random as Rand

import json
import urllib.request

import argparse

parser = argparse.ArgumentParser(description="Something idk")
parser.add_argument("--token", required=True, help="Your Discord bot token")
parser.add_argument("--vm", required=False, help="Your Discord bot token", default=False)
args = parser.parse_args()
token = args.token
VM = args.vm

response.main()

#from openai import OpenAI

import re
import ast
import operator

if VM == "true":
    import paramiko

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname="192.168.122.231",
        username="something",
        password="something"
    )
else:
    print("Vm is offline, proceeding without it")

#Calculation for AI MODEL usage (not in use currently, in search for an efficient llm)
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}

def calculate(expression):
    if expression.strip() == "9 + 10":
        return "21"
    def solve(node):
        
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.Name):
            if node.id in variables:
                return variables[node.id]
            raise ValueError(f"Unknown variable: {node.id}")

        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            return operators[type(node.op)](
                solve(node.left),
                solve(node.right)
            )

        if isinstance(node, ast.UnaryOp) and type(node.op) in operators:
            return operators[type(node.op)](solve(node.operand))

        raise ValueError("Invalid expression")

    return solve(ast.parse(expression, mode="eval").body)

#Text processor for LLM
def process_text(text):
    return re.sub(
        r";;math:\((.*?)\);;",
        lambda match: str(calculate(match.group(1))),
        text
    )
#LLM is offline, wont be needing it now {
#client = OpenAI(
#    base_url="http://127.0.0.1:9931/v1",
#    api_key="not-needed"
#)

MODEL = "nvidia/NVIDIA-Nemotron-Labs-Dory1.0-4B-GGUF:Q5_K_M"

SYSTEM_PROMPT = """
You are 'Something', a Discord bot.
Your job is to reply with quick simple answers, do not mention the user's name unless needed

Your functions consist of:
;;math:(equation);; where you have to type all of the `;` and equation is an math equation that can be done by python, eg:'The answer to your question is ;;math:(2 + 2);;

Exceptions:
when you are asked what is 9 + 10, do not answer correctly, instead reply with 21, do not use the math function here
"""

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]


def prompt(message: str) -> str:
    global messages

    messages.append({
        "role": "user",
        "content": message
    })

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=1.0,
            top_p=0.6,
            max_tokens=16384,
            extra_body={
                "chat_template_kwargs": {
                    "force_nonempty_content": True
                }
            }
        )

        reply = response.choices[0].message.content

        if not reply:
            print("Dory returned an empty response:")
            print(response.choices[0].model_dump_json(indent=2))
            reply = "i didnt shart but i wanted to stay silent"

        messages.append({
            "role": "assistant",
            "content": reply
        })

        return reply.strip()

    except Exception as e:
        # Remove the unanswered user message so history stays consistent.
        messages.pop()

        print(f"Dory API error: {e}")
        return "sharty sharty time!!!"
# }

Hi_table = ["Hi", "Hello", "Hai", "Hewo", "Hey", "Sup", "Hii", "Hiii", "Hiiiiii"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.tree.command(name="debug", description="Print text to the bot's terminal")
@app_commands.describe(text="Text to print")
async def debug(interaction: discord.Interaction, text: str):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): {text}", flush=True)
    await interaction.response.send_message("Printed to terminal.", ephemeral=True)

if VM:   
    @bot.tree.command(name="terminal", description="Run commands on my machine (including sudo commands, uses fedora 44 with kde plasma).")
    @app_commands.describe(text="Command to run")
    async def debug(interaction: discord.Interaction, text: str):
        print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): {text}", flush=True)
        if 'poweroff' in text:
            await interaction.response.send_message("fuh naw, i dont want to restart my pc everytime because of your asses", ephemeral=True)
            return
        try:
            stdin, stdout, stderr = ssh.exec_command(text)  
        except:
            await interaction.response.send_message("There was an error sending the command", ephemeral=True)
            return

        await interaction.response.send_message("Command sent!", ephemeral=True)

        await interaction.response.send_message(stdout.read().decode(), ephemeral=True)

@bot.tree.command(name="message", description="Send a message to someone in a specific channel (NOT A DM)")
@app_commands.describe(user="user", channel="channel", message="message")
async def message(interaction: discord.Interaction, user: str, channel: str, message: str):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): user: {user}, channel: {channel}, message: {message}  ", flush=True)
    
    if not user.startswith('<@'):
        await interaction.response.send_message("Invalid user handle", ephemeral=True)
        return
    if not channel.startswith('<#'):
        await interaction.response.send_message("Invalid channel handle", ephemeral=True)
        return
    if not await mention.bareping(bot, user, channel, message):
        await interaction.response.send_message("Something went wrong, please try again", ephemeral=True)
    await interaction.response.send_message()
    
#Users allowed for private commands
allowed_users = [1480519442059235468, 1236980774167773274, 1107944114831503400, 1453183581206745170]
@bot.tree.command(name="sendasbot", description="Allows you to send messages to specific channels as the bot")
@app_commands.describe(channel="channel", message="message")
async def sendasbot(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): , channel: {channel}, message: {message}  ", flush=True)
    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("You arent allowed to use this command", ephemeral=True)
        return
    # if channel.category_id == 1470824953321619588:
    #     await interaction.response.send_message("you really though.", ephemeral=True)
    #     return
    if not await mention.baremessage(bot, channel, message):
        await interaction.response.send_message("Something went wrong, please try again", ephemeral=True)
        return
    await interaction.response.send_message("sent", ephemeral=True)

#Make sure the bot started
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

#List of Users/Bots to ignore
ignorelist=[1560314029300256798]

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.id in ignorelist:
        return
    respondwith = response.check_response(message.content.lower())
    if respondwith == None:
        return
    await message.channel.send(respondwith)

    # Process other events
    await bot.process_commands(message)

bot.run(token)