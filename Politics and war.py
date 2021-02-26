import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests

load_dotenv()
TOKEN = os.getenv("POLITICS_BOT_TOKEN")
PoliticsAndWarToken = os.getenv("API_TOKEN")
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    
@bot.command()
async def getcity(ctx, name):

    data  = requests.get(f"http://politicsandwar.com/api/city/id={name}&key={PoliticsAndWarToken}")
    data = data.json()
    embed = discord.Embed(title="Get City Results")
    for dataName in data:
        if dataName != "success":
            embed.add_field(name=dataName, value=data[dataName])
    await ctx.send(embed=embed)

bot.run(TOKEN)
