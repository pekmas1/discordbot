import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user.name} is gay!")

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f"Hi {member.name}, Welcome to my dis")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if "hello" in message.content.lower():
        response = "yee"
        await message.channel.send(response)

client.run(TOKEN)   