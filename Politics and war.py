import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import asyncio
import random

load_dotenv()
TOKEN = os.getenv("POLITICS_BOT_TOKEN")
PoliticsAndWarToken = os.getenv("API_TOKEN")
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    
@bot.command(help="Put a city ID or name to get the city/cities that correspond. Use `-M` to get maximum info, and `-N` to not get any info.", brief="Get a city by it's ID or name",aliases=["city"])
async def getcity(ctx, nameOrID, argument=None):
    try:
        int(nameOrID)
        data  = requests.get(f"http://politicsandwar.com/api/city/id={nameOrID}&key={PoliticsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get City Results", color=0x00ff00)
        for dataName in data:
            if dataName != "success":
                embed.add_field(name=dataName, value=data[dataName])
        await ctx.send(embed=embed)
    except ValueError:
        if argument != None and argument != "-M" and argument != "-N":
            print(argument)
            await ctx.send("Invalid argument. Use -N to show no city information, and -M to show maximum information.")
            return
        loading = await ctx.send("Gathering cities, please wait <a:loading:747680523459231834> ...")
        cities = []
        data  = requests.get(f"http://politicsandwar.com/api/all-cities/key={PoliticsAndWarToken}")
        data = data.json()
        for thing in data["all_cities"]:
            if thing["city_name"].lower() == nameOrID.lower():
                
                
                if argument == "-M":
                    embed = discord.Embed(title="Get City Results",color=0x00ff00)
                    data  = requests.get(f'http://politicsandwar.com/api/city/id={thing["city_id"]}&key={PoliticsAndWarToken}')
                    data = data.json()
                    for dataName in data:
                        if dataName != "success":
                            embed.add_field(name=dataName, value=data[dataName])
                    
                elif argument == "-N":
                    pass
                elif argument == None:
                    embed = discord.Embed(title="Get City Results",color=0xff0000)
                    for thing2 in thing:
                        embed.add_field(name=thing2, value=thing[thing2])

                cities.append(embed)
        await loading.delete()
        if len(cities) == 1:
            await ctx.send(str(len(cities))+ " city with the name "+nameOrID+" was found.")
            await asyncio.sleep(3)
            if argument != "-N":
                data = requests.get(f'http://politicsandwar.com/api/city/id={cities[0].fields[1].value}&key={PoliticsAndWarToken}')
                data = data.json()
                embed = discord.Embed(title="Get City Results", color=0x00ff00)
                for dataName in data:
                    if dataName != "success":
                        embed.add_field(name=dataName, value=data[dataName])
                await ctx.send(embed=embed) 
        else:
            await ctx.send(str(len(cities))+ " cities with the name "+nameOrID+" were found.")
            await asyncio.sleep(3) 
            if argument != "-N":
                for city in cities:
                    await ctx.send(embed=city)
        

        
        
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


bot.run(TOKEN)
