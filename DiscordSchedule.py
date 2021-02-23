import discord


TOKEN = 'ODEzODMyOTEyMDY3MzYyODI3.YDVC9g.8jeLDI3q0vehjJrMTz6sl4Q9qJU'
client = discord.Client(intents=discord.Intents.all())
mondaySchedule = "Period 0/5:9:45;Period 1/6:10:34;Break:11:14;Period 2/7:11:27;Period 3/8:12:13;Lunch:12:53;PAWS:13:34;Period 4/9:14:5;School's Over!:14:45"
mondaySchedule = mondaySchedule.split(";")
normalSchedule = "Period 0/5:8:45;Period 1/6:9:45;Break:10:34;Period 2/7:10:48;Period 3/8:11:14;Lunch:12:33;PAWS:13:15;Period 4/9:13:47;School's Over!:14:35"
normalSchedule = normalSchedule.split(";")
dummy1 = []

for dummy3 in mondaySchedule:
    dummy3.split(":")
    dummy1.append(dummy3)
mondaySchedule = dummy1
print(mondaySchedule)
dummy1 = []
for dummy3 in normalSchedule:
    dummy1.append(dummy3.split(":"))
normalSchedule = dummy1
print(normalSchedule)
dummy3 = None
dummy1 = None

@client.event
async def on_ready():
    print(client.user.name+" has connected to discord!")


@tasks.loop
async def schedule():
    print("HI")
