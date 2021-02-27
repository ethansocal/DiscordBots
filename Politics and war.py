import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import asyncio

load_dotenv()
TOKEN = os.getenv("POLITICS_BOT_TOKEN")
PoliticsAndWarToken = os.getenv("API_TOKEN")
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    
@bot.command(help="Put a city ID or name to get the city/cities that correspond.\nUsage: `!getcity <cityID>` or `!getcity <cityName>`.", brief="Get a city by it's ID or name",aliases)
async def getcity(ctx, nameOrID):
    try:
        int(nameOrID)
        data  = requests.get(f"http://politicsandwar.com/api/city/id={nameOrID}&key={PoliticsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get City Results")
        for dataName in data:
            if dataName != "success":
                embed.add_field(name=dataName, value=data[dataName])
        await ctx.send(embed=embed)
    except ValueError:
        await ctx.send("Gathering cities, please wait <a:loading:747680523459231834> ...")
        cities = []
        data  = requests.get(f"http://politicsandwar.com/api/all-cities/key={PoliticsAndWarToken}")
        data = data.json()
        for thing in data["all_cities"]:
            if thing["city_name"].lower() == nameOrID.lower():
                data  = requests.get(f'http://politicsandwar.com/api/city/id={thing["city_id"]}&key={PoliticsAndWarToken}')
                data = data.json()
                embed = discord.Embed(title="Get City Results")
                for dataName in data:
                    if dataName != "success":
                        embed.add_field(name=dataName, value=data[dataName])
                cities.append(embed)
        if len(cities) == 1:
            await ctx.send(str(len(cities))+ " city with the name "+nameOrID+" was found.")
        else:
            await ctx.send(str(len(cities))+ " cities with the name "+nameOrID+" was found.")
        await asyncio.sleep(3)
        for city in cities:
            await ctx.send(embed=city)
        
        
    


bot.run(TOKEN)
