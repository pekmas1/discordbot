import discord
from discord.ext import commands
import datetime
import os
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

POLL: discord.Poll = None

@bot.command()
async def create_poll(ctx, question: str, *options):
    global POLL
    if len(options) < 2 or len(options) > 20:
        await ctx.send("You need to provide between 2 and 20 options for the poll.")
        return

    # Create the poll
    poll = discord.Poll(
        question=question,
        duration=datetime.timedelta(hours=24),  # Poll duration set to 24 hours
        multiple=False  # Only allow one vote per user
    )

    POLL = poll

    # Add options to the poll
    for option in options:
        poll.add_answer(text=option)

    # Send the poll
    await ctx.send(poll=poll)

@bot.command()
async def end_poll(ctx):
# Your answer starts here
…
…
…
# Your answer ends here


bot.run(os.getenv('DISCORD_TOKEN'))
