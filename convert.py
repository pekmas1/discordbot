import discord
from discord.ext import commands
import dotenv
import os
import http.client
import json

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
import http.client

@bot.command()
async def convert(ctx,a ,b ,c ):

    conn = http.client.HTTPSConnection("currency-conversion-and-exchange-rates.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "76762323d1mshcfcf8368bd28e98p1bd87fjsn93f80bf3e5ba",
        'x-rapidapi-host': "currency-conversion-and-exchange-rates.p.rapidapi.com"
        }

    conn.request("GET", f"/convert?from={a}&to={b}&amount={c}", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data = json.loads(data)["result"]

    await ctx.send(f"{c} {a} = {data} {b}")

@bot.command()
async def cconvert(ctx,a ,b ,c ):

    conn = http.client.HTTPSConnection("currency-conversion-and-exchange-rates.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "76762323d1mshcfcf8368bd28e98p1bd87fjsn93f80bf3e5ba",
        'x-rapidapi-host': "currency-conversion-and-exchange-rates.p.rapidapi.com"
        }

    country_currency_mapper = {
        "China": "CNY",
        "Japan": "JPY",
        "Korea": "KRW",
        "Thailand": "THB",
        "USA": "USD",
        "Europe": "EUR",
        "UK": "GBP",
    }
    
    conn.request("GET", f"/convert?from={country_currency_mapper[a]}&to={country_currency_mapper[b]}&amount={c}", headers=headers)

    res = conn.getresponse()
    data = res.read().decode("utf-8")
    data = json.loads(data)["result"]

    await ctx.send(f"{c} {country_currency_mapper[a]} ({a}) = {data} {country_currency_mapper[b]} ({b})")

bot.run(os.getenv("DISCORD_TOKEN"))