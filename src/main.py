import discord
from discord.ext import commands
from discord import app_commands

import mention
import response

import time
import random as Rand

import json
import urllib.request

import secrets

KILL_KEY = secrets.token_urlsafe(32)

print(f"Shutdown key: {KILL_KEY}")

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

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.tree.command(name="debug", description="Print text to the bot's terminal")
@app_commands.describe(text="Text to print")
async def debug(interaction: discord.Interaction, text: str):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): {text}", flush=True)
    await interaction.response.send_message("Printed to terminal.", ephemeral=True)

@bot.tree.command(name="kill", description="KILL :D")
@app_commands.describe(key="secret key to kill", reason="The reason why it is being shutdown")
async def kill(interaction: discord.Interaction, key: str, reason):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): recieved secret key {key}", flush=True)
    if key == str(KILL_KEY):
        await interaction.response.send_message(f"Shutting Down, requested by {interaction.user}: ")
        await bot.close()
    else:
        await interaction.response.send_message("Wrong Key")

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

@bot.tree.command(name="sendasbot2", description="Allows you to send messages to specific channels as the bot")
@app_commands.describe(message="message")
async def sendasbot(interaction: discord.Interaction, message: str):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}): message: {message}  ", flush=True)
    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("You arent allowed to use this command", ephemeral=True)
        return
    # if channel.category_id == 1470824953321619588:
    #     await interaction.response.send_message("you really though.", ephemeral=True)
    #     return
    await interaction.response.send_message(message)

@bot.tree.command(name="reload", description="Reload the json file that contains a list of responses instead of having to reload the whole bot")
async def reload(interaction: discord.Interaction):
    print(f"\n[DEBUG] {interaction.user} ({interaction.user.id}) requested reload!", flush=True)
    await interaction.response.send_message(response.reload_files())
    
@bot.tree.command(name="react", description="React to specific messages as a bot")
@app_commands.describe(channel="channel", message="message", emoji="emoji")
async def react(interaction:discord.Interaction,channel: discord.TextChannel, message: str, emoji: str):
    if interaction.user.id not in allowed_users:
        await interaction.response.send_message("You arent allowed to use this command", ephemeral=True)
        return
    try:
        chonky = await channel.fetch_message(int(message))
        await chonky.add_reaction(emoji)
        await interaction.response.send_message("Success", ephemeral=True)
    except:
        await interaction.response.send_message("Fail", ephemeral=True)
        

    
    

#Make sure the bot started
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync()

#List of Users/Bots to ignore
ignorelist=[1560314029300256798]
jades_server_id=1340360658633490453

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.id in ignorelist:
        return
    if message.server.id == jades_server_id:
        evilstuff()
    respondwith = response.check_response(message.content.lower())
    if respondwith == None:
        await bot.process_commands(message)
        return
    try:
        await message.channel.send(respondwith)
    except:
        pass
    
    # Process other events
    await bot.process_commands(message)

#EVILLLLL STUFF TO DO TO JADE
def evilstuff():
    #do so many evil stuff it is evil
    print("im doing evil stuff to your server muahahaaha")
    for i in range(0,5,1):
        print("evil is me")

bot.run(token)