import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import asyncio
import random
from discord.ext import tasks
import json

load_dotenv()
TOKEN = os.getenv("POLITICS_BOT_TOKEN")
PoliticsAndWarToken = os.getenv("API_TOKEN")
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    print("Availiable Commands\n===================")
    for command in bot.commands:
        print(["\u001b[34m","\u001b[31m","\u001b[33m","\u001b[34m","\u001b[35m","\u001b[36m","\u001b[37m"][random.randint(0, 6)]+"!"+command.name+": "+command.help)

    print("\u001b[0m",end="")
    #update.start()
@bot.command(help="Put a city ID or name to get the city/cities that correspond.", brief="Get a city by it's ID or name",aliases=["city"])
async def getcity(ctx, nameOrID):
    try:
        int(nameOrID)
        data  = requests.get(f"http://politicsandwar.com/api/city/id={nameOrID}&key={PoliticsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get City Results", color=0x00ff00)
        for dataName in data:
            if dataName == "url":
                embed.add_field(name="Link", value=f"[City Link]({data[dataName]})")
            elif dataName != "success" and data["success"] == True:
                embed.add_field(name=dataName, value=data[dataName])
        await ctx.send(embed=embed)
    except ValueError:
        loading = await ctx.send("Gathering cities, please wait <a:loading:747680523459231834> ...")
        cities = []
        data  = requests.get(f"http://politicsandwar.com/api/all-cities/key={PoliticsAndWarToken}")
        data = data.json()
        for thing in data["all_cities"]:
            if thing["city_name"].lower() == nameOrID.lower():
                embed = discord.Embed(title="Get City Results",color=0xff0000)
                for thing2 in thing:
                    embed.add_field(name=thing2, value=thing[thing2])

                cities.append(embed)
        await loading.delete()
        if len(cities) == 1:
            await ctx.send(str(len(cities))+ " city with the name "+nameOrID+" was found.")
            data = requests.get(f'http://politicsandwar.com/api/city/id={cities[0].fields[1].value}&key={PoliticsAndWarToken}')
            data = data.json()
            embed = discord.Embed(title="Get City Results", color=0xff0000)
            for dataName in data:
                if dataName != "success":
                    embed.add_field(name=dataName, value=data[dataName])
            await ctx.send(embed=embed) 
        else:
            await ctx.send(str(len(cities))+ " cities with the name "+nameOrID+" were found.")
            await asyncio.sleep(3) 
            for city in cities:
                await ctx.send(embed=city)

@bot.command(help="Invite others to play. To use your own referral, put your leader name in quotation marks after !invite", brief="Invite others to play", aliases=["refer","referral"])
async def invite(ctx, leaderName="Ethan Henry"):
    leaderNameFormatted = leaderName.replace(" ", "+")
    embed = discord.Embed(title="Invite others to Politics and War!", url="https://politicsandwar.com/register/ref="+leaderNameFormatted)
    embed.set_image(url="https://pbs.twimg.com/profile_images/876630922547740672/dcqCkdZm.jpg")
    await ctx.send(embed=embed)

@bot.command(help="Get a nation by its ID or name.",aliases=["nation","getnation"])
async def who(ctx, nameOrID):
    try:
        int(nameOrID)
        data  = requests.get(f"http://politicsandwar.com/api/nation/id={nameOrID}&key={PoliticsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get Nation Results", color=0x00ff00)
        if data["success"] != False:
            embed.add_field(name="Link", value=f"[Nation Link](https://politicsandwar.com/nation/?id={data['nationid']})")
            for dataName in data:
                if dataName != "success" and data["success"] == True:
                    if data[dataName] != "":
                        embed.add_field(name=dataName, value=data[dataName])
                    else:
                        embed.add_field(name=dataName,value="None")
            await ctx.send(embed=embed)
        else:
            await ctx.send("There was an error. Please try again.")
    except ValueError:
        loading = await ctx.send("Gathering nations, please wait <a:loading:747680523459231834> ...")
        file = open("nations_cache.txt", "r")
        text = file.read()
        file.close()
        for nation in text.split("\n"):
            hi = nation.split(":")
            print(nation)
            if hi[1].lower() == nameOrID.lower():
                data2 = requests.get(f"http://politicsandwar.com/api/nation/?id={hi[1]}&key={PoliticsAndWarToken}")
                data2 = data2.json()
                embed = discord.Embed(title="Get Nation Results", color=0x00ff00)
                print(data2)
                for dataName in data2:
                    if dataName != "success" and data2[dataName] == "":
                        embed.add_field(name=dataName, value=data2[dataName])
                embed.add_field(name="Link",value=f"https://politicsandwar.com/nation/?id={hi[1]}")
                await ctx.send(embed=embed)
                break
        await loading.delete()

@tasks.loop(hours=1)
async def update():
    print("Updating nation cache...")
    data = requests.get(f"https://politicsandwar.com/api/nations/?key={PoliticsAndWarToken}")
    data = data.json()
    file = open("nations_cache.txt", "w")
    for thing in data["nations"]:
        file.write(str(thing["nation"]) + ":"+str(thing["nationid"])+"\n")
    file.close()
    print("Done")
"""
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
"""

bot.run(TOKEN)
