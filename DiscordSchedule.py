import discord
from discord.ext import tasks
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
mondaySchedule = "Period 0/5:9:45:10:28;Period 1/6:10:34:11:14;Break:11:14:11:21;Period 2/7:11:27:12:07;Period 3/8:12:13:12:53;Lunch:12:53:13:28;PAWS, click on me to get the PAWS schedule:13:34:13:59;Period 4/9:14:05:14:45;School's Over!:14:45:8:45"
mondaySchedule = mondaySchedule.split(";")
normalSchedule = "Period 0/5:8:45:9:38;Period 1/6:9:45:10:34;Break:10:34:10:41;Period 2/7:10:48:11:37;Period 3/8:11:14:12:33;Lunch:12:33:13:08;PAWS, click on me to get the PAWS schedule:13:15:13:40;Period 4/9:13:47:14:35;School's Over!:14:35:8:45, tomorrow"
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

async def alert(message, hourStart="8", minuteStart="45", hourEnd="9", minuteEnd="45", day="Monday"):

    if message == "PAWS, click on me to get the PAWS schedule":
        url = "https://drive.google.com/file/d/1yg_afS4BswjBJY-13YsUEICAQJTOwHh5/view"
    else:
        url = "https://newhart.schoolloop.com/file/1500178971867/1124898729487/4879874549780900083.pdf"
    embed = discord.Embed(title="School Schedule", url=url,color=0x00FF00,description="The class you should be in right now is:")
    embed.set_author(name="School Schedule Bot", url="https://github.com/ethansocal/DiscordBots/blob/main/DiscordSchedule.py", icon_url=client.user.avatar_url)
    embed.add_field(name="Class", value=message, inline=False)
    embed.add_field(name="Start Time", value=hourStart+":"+minuteStart, inline=True)
    embed.add_field(name="End Time", value=hourEnd+":"+minuteEnd, inline=True)
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.name == "school-alerts":
                message = await channel.send(embed=embed)
                
@client.event
async def on_ready():
    await alert("Class Alert")
    print(client.user.name + " has connected to discord!")
    schedule.start()

@client.event
async def on_message(message):
    if message.content.lower() == "!help":
        await message.channel.send("Bot Commands:\n`!support` - Get help or submit an issue\n`!help` - ***INCEPTION***\n`!invite` - Invite me to your server!")
    elif message.content.lower() == "!support":
        await message.channel.send("DM'ed you the links!")
        await message.author.send("https://discord.gg/k5pBHxJvkX")
    elif message.content.lower() == "!invite":
        await message.channel.send("Click on the link to invite School Schedule! https://discord.com/oauth2/authorize?client_id=813832912067362827&permissions=19472&scope=bot")

@client.event
async def on_guild_join(guild):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
    }
    channel = await guild.create_text_channel("school-alerts", overwrites=overwrites)
    await channel.send("Thank you for inviting School Schedule to your server! Please manage the roles in this channel and make sure its name remains `school-events`. I will send a message everytime you need to go to a different class, or if there is an important event you should know about for Newhart.")

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
                    await alert(time[0], time[1], time[2], time[3], time[4], day)
                    break
        elif day != "Sunday" and day != "Saturday":
            for time in normalSchedule:
                if hour == int(time[1]) and minute == int(time[2]):
                    print(time[0])
                    await alert(time[0], time[1], time[2], time[3], time[4], day)
                    break

client.run(TOKEN)