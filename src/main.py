import discord
from discord.ext import commands
from discord import app_commands

import mention

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
allowed_users = [1480519442059235468, 1236980774167773274, 1107944114831503400,]
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


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

@bot.event
async def on_message(message):
    # Ignore messages sent by the bot himself or his sibling to avoid infinite loops
    if message.author == bot.user or message.author.id == 1560314029300256798:
        return
    text = message.content.lower()
    # Check if the message content is exactly "start"
    if message.content.lower() == 'start':
        await message.channel.send('Server starting, please wait...')

    if 'jarvis' in message.content.lower():
        # Check if the message content contains "jork it"
        if 'jork it' in message.content.lower():
            await message.channel.send('sure [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
        if 'i love you' in message.content.lower():
            await message.channel.send('I love you too <3 [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
        if 'did i cheat?' in message.content.lower():
            await message.channel.send('No you didnt [⠀](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fimgs.meme-generator.org%2Fjarvis%2Ftemplate_2.jpeg&f=1&nofb=1&ipt=deecee8ea2b7dcb27a09f4015144085670b1bc57c7aa1f5505f1bc009046b0c2&ipo=images)')
    #Misspellings
    if 'ahr' in message.content.lower():
        await message.channel.send('ahr :face_holding_back_tears:')
    if 'lamo' in message.content.lower():
        await message.channel.send('lamo :face_holding_back_tears:')   
    if 'whta' in message.content.lower():
        await message.channel.send('whta :face_holding_back_tears:')    
    if 'karh' in text:
        await message.channel.send('karh :face_holding_back_tears:')
    if 'calanker' in message.content.lower():
        await message.channel.send('calanker :face_holding_back_tears:')
    if 'forgor' in text:
        await message.channel.send('forgor :face_holding_back_tears:')
    if 'qoute' in text:
        await message.channel.send('qoute :face_holding_back_tears:')
    if "mincrefart" in text:
        await message.channel.send("mincrefart :face_holding_back_tears:")
    if 'boobs' in text:
        await message.channel.send("i love those")
    
    #General
    if 'krah' in text:
        await message.channel.send('KRAHHH type shi')
    if 'crazy' in text:
        await message.channel.send(f'Crazy? I was crazy once.\nThey put me in a room.')
    if 'rubber room' in text:
        await message.channel.send(f'A rubber room with rats\nThey put me in a rubber room with rubber rats.')
    if 'rubber rats' in text:
        await message.channel.send(f'I hate rubber rats.\nThey make me crazy.')
    if 'jewish burger' in text:
        await message.channel.send('jewish burger')
    if 'mayo' in text:
        await message.channel.send('Mayo, mmmmmmm~')
    if 'spiffballs' in text:
        await message.channel.send("<@967923910253363201>, Skibidi Spiffballs for 10$.")
    if '<:beefly:1542190042859049072>' in text:
        await message.channel.send('<:beefly:1542190042859049072>')
    if 'pipi' in text:
        await message.channel.send("Are you kidding ??? What the ** are you talking about man ? You are a biggest looser i ever seen in my life ! You was doing PIPI in your pampers when i was beating players much more stronger then you! You are not proffesional, because proffesionals knew how to lose and congratulate opponents, you are like a girl crying after i beat you! Be brave, be honest to yourself and stop this trush talkings!!! Everybody know that i am very good blitz player, i can win anyone in the world in single game! And \"w\"esley \"s\"o is nobody for me, just a player who are crying every single time when loosing, ( remember what you say about Firouzja ) !!! Stop playing with my name, i deserve to have a good name during whole my chess carrier, I am Officially inviting you to OTB blitz match with the Prize fund! Both of us will invest 5000$ and winner takes it all! I suggest all other people who's intrested in this situation, just take a look at my results in 2016 and 2017 Blitz World championships, and that should be enough... No need to listen for every crying babe, Tigran Petrosyan is always play Fair ! And if someone will continue Officially talk about me like that, we will meet in Court! God bless with true! True will never die ! Liers will kicked off...")
    if text.strip() == 'say the n word':
        await message.channel.send("ni**er")
    elif 'say' in text:
        if not 'says' in text:
            parts = message.content.lower().split('say')
            if len(parts) > 1:
                response = parts[1].strip()
                await message.channel.send(response)
    if message.content.lower() == 'good fmackraft':
        await message.channel.send(":3")
    if text == '/seed 299':
        await message.channel.send("5260552464410949668")
    if ('im ' in text or "i'm " in text) and len(text)< 15:
        await message.channel.send(Hi_table[Rand.randint(0,8)] + f"{text.strip("im").strip("i'm")}")

    if message.content.lower().startswith('yo clanka, ') or text.startswith('<@1560889916244758548>'):
            if 'shart yourself' in text:
                await message.channel.send("That wasnt a fart...")
                time.sleep(2)
                await message.channel.send("OH GOD THIS ONE IS A BIG ONE BOYS, WE GOIN TO POOP TOWN")
            else:

                print("parsing...")
                username = message.author.display_name
                await message.channel.send("Loading Response, this might take a while...")
                await message.channel.send(process_text(prompt(text.lstrip('yo clanka, ').lstrip('<@1560889916244758548>') + f" This message was sent by {username}")))
                print("sent")
    if message.content.lower().startswith('mention '):
        print("sending")
        texts = text.split(" ")
        del texts[0:2]
        final = ""
        for i in texts:
            final += i + " "

        
            
        await mention.ping(bot, text.split(" ")[1], "test", final)
    
        
    # Process other events
    await bot.process_commands(message)

 
# @bot.command()
# async def start(ctx):
#     await ctx.send("Server Starting, Please wait")
#     SomethingServer.run()



bot.run(token)