import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import math

bot = commands.Bot(command_prefix="=")
load_dotenv()
TOKEN = os.getenv("MATH_BOT_TOKEN")


@bot.event
async def on_ready():
    print(bot.user.name + " has connected to Discord!")
    print("Availiable Commands\n===================")
    for command in bot.commands:
        print("!"+command.name+": "+command.help)

@bot.command(help="Evaluate a math expression!", brief="Evaluate a math expression")
async def evaluate(ctx, *args):
    print(" ".join(args))

bot.run(TOKEN)