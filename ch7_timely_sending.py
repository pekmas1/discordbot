import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from datetime import datetime, time


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = 1276744685838405636

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@tasks.loop(seconds=10)
async def daily_morning():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send("Good Morning :)")

@client.event
async def on_ready():
    daily_morning.start()

@bot.command()
async def add_medicine(ctx, name: str, quantity: int, hour: int, minute: int):
    
client.run(TOKEN)