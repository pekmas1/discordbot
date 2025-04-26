import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # if "hello" in message.content.lower():
    #     response = "Hellow Human"
    #     await message.channel.send(response)

    content = message.content.lower()
    count_vowels = 0
    for ch in content:
        if ch in "aeiou":
            count_vowels += 1

    await message.channel.send(f"Your message contains {count_vowels} vowels!")
client.run(TOKEN)
