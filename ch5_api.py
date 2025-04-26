import discord
from discord.ext import commands
import dotenv
import os
from openai import OpenAI
import http.client
import json

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
#---------------------------------------------------------
@bot.command()
async def cg(ctx, text):
    response = client.chat.completions.create(
        model = "gpt-4o-mini-2024-07-18",
        messages=[
            {"role":"system", "content": "You are a grammar corrector. You will be given a text and you will need to correct the grammar. You will also need to explain the correction you made."},
            {"role":"user", "content":text}
        ]
    )
    await ctx.send(response.choices[0].message.content)


@bot.command()
async def hd(ctx,year):
        
    conn = http.client.HTTPSConnection("apigw1.bot.or.th")

    headers = {
        'X-IBM-Client-Id': os.getenv("BOT_CLIENT_ID"),
        'accept': "application/json"
        }

    conn.request("GET", f"/bot/public/financial-institutions-holidays/?year={year}", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data = json.loads(data)["result"]

    result = ""
    for item in data["data"]:
        result += item["Date"] + " " + item["HolidayDescriptionThai"] + "\n"


    await ctx.send(result)

#---------------------------------------------------------
bot.run(os.getenv("DISCORD_TOKEN"))