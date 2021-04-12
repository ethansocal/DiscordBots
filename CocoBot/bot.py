import discord
from discord.ext import commands
import typing
import asyncio
import discord_slash

bot = commands.Bot("c>")
slash = discord_slash.SlashCommand(bot, sync_commands=True)

statuses = ["COCOMELON GETTING BEATEN BY PEWDS"]

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"COCOMELON GETTING BEATEN BY PEWDS"))

@bot.command(name="coco", aliases=["connect", "start", "p", "play"])
async def coco(ctx: commands.Context):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\COCO.mp3"))
        await ctx.send("Playing!")
        while True:
            await asyncio.sleep(240)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\COCO.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")

@slash.slash(name="coco", description="Play Coco (the best song on earth) forever!")
async def coco(ctx):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        await ctx.send("Playing!")
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\COCO.mp3"))
        while True:
            await asyncio.sleep(240)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\COCO.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")

@bot.command(name="stop", aliases=["dc", "disconnect"])
async def stop(ctx: commands.Context):
    voice = ctx.guild.voice_client
    if voice != None:
        await voice.disconnect()
        await ctx.send("Disconnected!")
    else:
        await ctx.send("Please join a voice channel first!")

@slash.slash(name="stop", description="Stop playing PewDiePie music >:(")
async def stop(ctx):
    voice = ctx.guild.voice_client
    if voice != None:
        await voice.disconnect()
        await ctx.send("Disconnected!")
    else:
        await ctx.send("Please join a voice channel first!")


@bot.command(name="lasagna")
async def lasagna(ctx: commands.Context):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna.mp3"))
        await ctx.send("Playing!")
        while True:
            await asyncio.sleep(140)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")

@slash.slash(name="lasagna", description="Diss T-Series because they suck")
async def lasagna(ctx):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        await ctx.send("Playing!")
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna.mp3"))
        while True:
            await asyncio.sleep(140)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")


@bot.command(name="lasagna2")
async def lasagna2(ctx: commands.Context):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna2.mp3"))
        await ctx.send("Playing!")
        while True:
            await asyncio.sleep(140)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna2.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")

@slash.slash(name="lasagna2", description="Who the hell is bob, and why you wanna kiss him")
async def lasagna2(ctx):
    voice = ctx.author.voice
    if voice != None:
        if ctx.guild.voice_client != None:
            await ctx.guild.voice_client.disconnect()
        voice_channel = voice.channel
        vc = await voice_channel.connect()
        await ctx.send("Playing!")
        vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna2.mp3"))
        while True:
            await asyncio.sleep(140)
            vc.play(discord.FFmpegPCMAudio(executable="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\ffmpeg\\bin\\ffmpeg.exe", source="C:\\Users\\ethan\\Documents\\GitHub\\DiscordBots\\CocoBot\\lasagna2.mp3"))
    else:
        await ctx.send("Please join a voice channel first!")

"""
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)
"""
bot.run("ODMwOTc2MjA2ODk4ODU1OTQ3.YHOg5g.THyVh4T8582yezKMBvuq2h5mSW8")