import discord
import json
from pathlib import Path

List_Path = Path(__file__).resolve().parent / "List.json"

users=json.load(open(List_Path, "r"))["Users"]
channels=json.load(open(List_Path, "r"))["Channels"]

def ping(user: str, message:str):
    try:
        if users[user] == "":
            # await bot.get_channel(int(channels[channel].strip("<#").strip(">"))).send("User not found")
            return "User not found"
    except Exception as exception:
        print(f"error: {exception}")
        # await bot.get_channel(int(channels[channel].strip("<#").strip(">"))).send(f"User {user} not found")
        print(Warning("user not found"))
        return "user not found " + str(exception)
        
    # await bot.get_channel(int(channels[channel].strip("<#").strip(">"))).send(f"{users[user]}, you've got mail!")
    # await bot.get_channel(int(channels[channel].strip("<#").strip(">"))).send(message)
    return users[user] + message

async def bareping(bot: discord.client, user: str, channel: str, message: str):
    try:
        await bot.get_channel(int(channel.strip("<#").strip(">"))).send(f"{user}, you've got mail!")
        await bot.get_channel(int(channel.strip("<#").strip(">"))).send(message)
    except:
        return False

async def baremessage(bot: discord.client, channel, message: str):
    try:
        await channel.send(message)
        return True
    except:
        return False