import discord
from discord.ext import tasks
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
mondaySchedule = "Period 0/5:9:45:10:28;Period 1/6:10:34:11:14;Break:11:14:11:21;Period 2/7:11:27:12:07;Period 3/8:12:13:12:53;Lunch:12:53:13:28;PAWS:13:34:13:59;Period 4/9:14:05:14:45;School's Over!:14:45:8:45"
mondaySchedule = mondaySchedule.split(";")
normalSchedule = "Period 0/5:8:45:9:38;Period 1/6:9:45:10:34;Break:10:34:10:41;Period 2/7:10:48:11:37;Period 3/8:11:14:12:33;Lunch:12:33:13:08;PAWS:13:15:13:40;Period 4/9:13:47:14:35;School's Over!:14:35:8:45"
normalSchedule = normalSchedule.split(";")
dummy1 = []

for dummy3 in mondaySchedule:
    dummy3.split(":")
    dummy1.append(dummy3)
mondaySchedule = dummy1
dummy1 = []
for dummy3 in normalSchedule:
    dummy1.append(dummy3.split(":"))
normalSchedule = dummy1
dummy3 = None
dummy1 = None
channelMessages = []

async def alert(message, hourStart="8", minuteStart="45", hourEnd="9", minuteEnd="45"):
    for deletemessage in channelMessages:
        await deletemessage.delete()
    embed = discord.Embed(title="School Schedule", url="https://newhart.schoolloop.com/file/1500178971867/1124898729487/4879874549780900083.pdf",color=0xFF0000,description="The class you should be in right now is:")
    embed.set_author(name="School Schedule Bot", url="https://github.com/ethansocal/DiscordBots/blob/main/DiscordSchedule.py", icon_url=client.user.avatar_url)
    embed.add_field(name="Class", value=message, inline=False)
    embed.add_field(name="Start Time", value=hourStart+":"+minuteStart, inline=True)
    embed.add_field(name="End Time", value=hourEnd+":"+minuteEnd, inline=True)
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == "school-alerts":
                message = await channel.send(embed=embed)
                channelMessages.append(message)
                

@client.event
async def on_ready():
    await alert("Class Alert")
    print(client.user.name + " has connected to discord!")
    schedule.start()

@tasks.loop(seconds=1)
async def schedule():
    now = datetime.now()
    hour = int(now.strftime("%H"))
    minute = int(now.strftime("%M"))
    second = int(now.strftime("%S"))
    day = now.strftime("%A")
    if second == 0:
        if day == "Monday":
            for time in mondaySchedule:
                if hour == int(time[1]) and minute == int(time[2]):
                    print(time[0])
                    await alert(time[0], time[1], time[2], time[3], time[4])
                    break
        elif day != "Sunday" and day != "Saturday":
            for time in normalSchedule:
                if hour == int(time[1]) and minute == int(time[2]):
                    print(time[0])
                    await alert(time[0], time[1], time[2], time[3], time[4])
                    break

client.run(TOKEN)