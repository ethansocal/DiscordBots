import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
import asyncio
import random
from discord.ext import tasks
import json
import typing
import wolframalpha
import tweepy

load_dotenv()
TOKEN = os.getenv("POLITICS_BOT_TOKEN")
politicsAndWarToken = os.getenv("API_TOKEN")
wolframAlphaToken = os.getenv("WOLFRAM_ALPHA_TOKEN")
wolframAlphaClient = wolframalpha.Client(wolframAlphaToken)
bot = commands.Bot(command_prefix="!")
twitterAuthorization = tweepy.OAuthHandler("81VqLm1jR02lsVZrmmFULu30F", "ppSsfP1Uwu1QzoMmaa33K4sDgqaMGYAVzzwfBf5MnKU0SDMalH")
twitterAuthorization.set_access_token("1312430026541867011-gzPwohIMeIPJ2KaPDbM5BA8t232MfX", "iCtfFWJqIKK3faTTyE8iVnLITON4GUH3c0J9IR0S9SmTH")
twitterClient = tweepy.API(twitterAuthorization)
try:
    twitterClient.verify_credentials()
    print("Twitter authentication success!")
except:
    print("Error during authentication.")

def isAuthorized(ctx):
    file = open("authorized_users.txt")
    for userid in file.readlines():
        if ctx.author.id == int(userid):
            file.close()
            return True
    file.close()
    return False

@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    print("Availiable Commands\n===================")
    for command in bot.commands:
        print("!"+command.name+": "+command.help)
    #updateNations.start()
    updateResources.start()

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(title="Error", color=0xff0000)
    if isinstance(error, commands.CheckFailure):
        embed.add_field(name="Error Message", value="Missing Permissions!")
    else:
        embed.add_field(name="Error Message", value="Please try again")
        print(error)
    await ctx.send(embed=embed)

@bot.command(help="Get a smart answer from Wolfram Alpha. Get math help, quick answers, and AI answers. You need to be authorized by Ethan to run this command.",brief="Get an answer from Wolfram Alpha.")
@commands.check(isAuthorized)
async def answer(ctx, *, question):
    data = wolframAlphaClient.query(question)
    await ctx.message.reply(next(data.results).text)

@bot.command(brief="Tweet in Ethan's Twitter account!", help="Tweet in Ethan's Twitter account! You need to be authorized by Ethan to run this command.")
@commands.check(isAuthorized)
async def tweet(ctx, *, text):
    try:
        twitterClient.update_status(text)
        await ctx.message.reply("Tweet successfully sent!")
    except tweepy.TweepError:
        await ctx.message.reply("Error sending tweet.")

@bot.command(brief="Authorize another user!", help="Authorize another user to get access to restricted commands! Only Ethan can run this command.")
async def authorize(ctx, user : discord.Member):
    if ctx.author.id == 710657087100944476:
        file = open("authorized_users.txt", "a")
        file.write("\n"+str(user.id))
        file.close()
        await ctx.message.reply("Successfully authorized "+user.name + "#"+user.discriminator+"!")

@bot.command(help="Get the current trade price of a resource.", brief="Get the current trade prices.", aliases=["price","tradeprices"])
async def tradeprice(ctx, resource="all"):
    if resource == "all":
        file = open('resource_cache.json', 'r')
        data = json.loads(file.read())
        file.close()
        embed = discord.Embed(title="Resource Prices",color=0x03b1fc)
        for resourceName in data:
            embed.add_field(name=resourceName.capitalize(), value="{:,}".format(int(data[resourceName])))
        await ctx.message.reply(embed=embed)
        return
    elif not resource.lower() in ['credits','steel','food','gasoline','oil','coal','munitions','uranium','iron', 'lead','bauxite','aluminum']:
        await ctx.message.reply("Incorrect resource. Please try again.")
        return
    data = requests.get(f"https://politicsandwar.com/api/tradeprice/?resource={resource}&key={politicsAndWarToken}")
    data = data.json()
    embed = discord.Embed(title=data["resource"].capitalize(),color=0x03b1fc)
    embed.add_field(name="Average Price", value="```$"+data["avgprice"]+"```",inline=False)
    embed.add_field(name="Highest Buy", value=f"```Date: {data['highestbuy']['date']}\nNation ID: {data['highestbuy']['nationid']}\nAmount: {data['highestbuy']['amount']}\nPrice Per Unit: ${data['highestbuy']['price']}\nTotal Price: {data['highestbuy']['totalvalue']}```")
    embed.add_field(name="Lowest Buy", value=f"```Date: {data['lowestbuy']['date']}\nNation ID: {data['lowestbuy']['nationid']}\nAmount: {data['lowestbuy']['amount']}\nPrice Per Unit: ${data['lowestbuy']['price']}\nTotal Price: {data['lowestbuy']['totalvalue']}```")
    await ctx.message.reply(embed=embed)

@bot.command(help="Put a city ID or name to get the city/cities that correspond.", brief="Get a city by it's ID or name",aliases=["city"])
async def getcity(ctx, *, nameOrID : typing.Union[int, str]):
    if type(nameOrID) == int:
        data  = requests.get(f"http://politicsandwar.com/api/city/id={nameOrID}&key={politicsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get City Results", color=0x00ff00)
        for dataName in data:
            if dataName == "url":
                embed.add_field(name="Link", value=f"[City Link]({data[dataName]})")
            elif dataName != "success" and data["success"] == True:
                embed.add_field(name=dataName, value=data[dataName])
        await ctx.message.reply(embed=embed)
    else:
        loading = await ctx.message.reply("Gathering cities, please wait <a:loading:747680523459231834> ...")
        cities = []
        data  = requests.get(f"http://politicsandwar.com/api/all-cities/key={politicsAndWarToken}")
        data = data.json()
        for thing in data["all_cities"]:
            if thing["city_name"].lower() == nameOrID.lower():
                embed = discord.Embed(title="Get City Results",color=0xff0000)
                for thing2 in thing:
                    embed.add_field(name=thing2, value=thing[thing2])

                cities.append(embed)
        await loading.delete()
        if len(cities) == 1:
            await ctx.message.reply(str(len(cities))+ " city with the name "+nameOrID+" was found.")
            data = requests.get(f'http://politicsandwar.com/api/city/id={cities[0].fields[1].value}&key={politicsAndWarToken}')
            data = data.json()
            embed = discord.Embed(title="Get City Results", color=0xff0000)
            for dataName in data:
                if dataName != "success":
                    embed.add_field(name=dataName, value=data[dataName])
            await ctx.message.reply(embed=embed) 
        else:
            await ctx.message.reply(str(len(cities))+ " cities with the name "+nameOrID+" were found.")
            await asyncio.sleep(3) 
            for city in cities:
                await ctx.message.reply(embed=city)

@bot.command(help="Invite others to play. To use your own referral, put your leader name in quotation marks after !invite", brief="Invite others to play", aliases=["refer","referral"])
async def invite(ctx, *, leaderName="Ethan Henry"):
    leaderNameFormatted = leaderName.replace(" ", "+")
    embed = discord.Embed(title="Invite others to Politics and War!", url="https://politicsandwar.com/register/ref="+leaderNameFormatted)
    embed.set_image(url="https://pbs.twimg.com/profile_images/876630922547740672/dcqCkdZm.jpg")
    await ctx.message.reply(embed=embed)

@bot.command(help="Get a nation by its ID or name.",aliases=["nation","getnation"])
async def who(ctx, *, nameOrID : typing.Union[int, str]):
    if type(nameOrID) == int:
        data  = requests.get(f"http://politicsandwar.com/api/nation/id={nameOrID}&key={politicsAndWarToken}")
        data = data.json()
        embed = discord.Embed(title="Get Nation Results", color=0x00ff00)
        if data["success"] != False:
            embed.add_field(name="Link", value=f"[Nation Link](https://politicsandwar.com/nation/?id={data['nationid']})")
            for dataName in data:
                if dataName != "success" and data["success"] == True and dataName != "flagurl":
                    if data[dataName] != "":
                        embed.add_field(name=dataName, value=str(data[dataName]))
                    else:
                        embed.add_field(name=dataName,value="None")
            embed.set_thumbnail(url=data["flagurl"])
            await ctx.message.reply(embed=embed)
        else:
            await ctx.message.reply("There was an error. Please try again.")
            return
    else:
        loading = await ctx.message.reply("Gathering nations, please wait <a:loading:747680523459231834> ...")
        file = open("nations_cache.txt", "r")
        text = file.readlines()
        file.close()
        
        for nation in text:
            if nation == "":
                await ctx.message.reply("There was an error. Please try again.")
                return
            data1 = nation.split(":")
            if data1[0].lower() == nameOrID.lower():
                data  = requests.get(f"http://politicsandwar.com/api/nation/id={data1[1]}&key={politicsAndWarToken}")
                data = data.json()
                embed = discord.Embed(title="Get Nation Results", color=0x00ff00)
                if data["success"] != False:
                    embed.add_field(name="Link", value=f"[Nation Link](https://politicsandwar.com/nation/?id={data1[1]})")
                    for dataName in data:
                        if dataName != "success" and data["success"] == True and dataName != "flagurl":
                            if data[dataName] != "":
                                embed.add_field(name=dataName, value=data[dataName])
                            else:
                                embed.add_field(name=dataName,value="None")
                    embed.set_thumbnail(url=data["flagurl"])
                    await ctx.message.reply(embed=embed)
                    await loading.delete()
                    return
                else:
                    await loading.delete()
                    await ctx.message.reply("There was an error. Please try again.")
                    return
                break
        await loading.delete()
        await ctx.message.reply("There was an error. Please try again.")
        

@tasks.loop(hours=1)
async def updateNations():
    try:
        print("Updating nations cache...")
        data = requests.get(f"https://politicsandwar.com/api/nations/?key={politicsAndWarToken}")
        data = data.json()
        file = open("nations_cache.txt", "w")
        for thing in data["nations"]:
            file.write(str(thing["nation"]) + ":"+str(thing["nationid"])+"\n")
        print("Done updating nations cache.")
    except:
        print("Error updating nations cache.")
    finally:
       file.close()

@tasks.loop(hours=1)
async def updateResources():
    try:
        print("Updating resources cache...")
        resourceInfo = dict()
        for resource in ['steel','credits','food','gasoline','oil','coal','munitions','uranium','iron', 'lead','bauxite','aluminum']:
            data = requests.get(f"https://politicsandwar.com/api/tradeprice/?resource={resource}&key={politicsAndWarToken}")
            data = data.json()
            resourceInfo[resource] = int(data["avgprice"])
        file = open("resource_cache.json", "w")
        file.write(json.dumps(resourceInfo))
        print("Done updating resources cache.")
    except:
        print("Error updating resources cache.")
    finally:
        file.close()




bot.run(TOKEN)
