import discord
from discord.ext import commands
import dotenv
import os
import datetime


dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def poll(ctx, question, *options):
    if len(options) < 2 or len(options) >20:
        await ctx.send("You need to provide between 2 and 20 options for the poll.")
        return
    
    poll = discord.Poll(question=question, duration=datetime.timedelta(hours=1))

    for option in options:
        poll.add_answer(text=option)
    
    await ctx.send(poll=poll)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(os.getenv("DISCORD_TOKEN"))