import discord
from discord.ext import commands
import math
import dotenv
import os

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Your answer starts here
@bot.command()
async def gcd(ctx, a, b):
    a = int(a)
    b = int(b)
    c = (math.gcd(a, b))
    await ctx.send(f"The GCD of {a} and {b} is: {c}")

# Your answer ends here

bot.run(os.getenv('DISCORD_TOKEN'))
