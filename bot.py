import asyncio  # imports asyncio for logging
import json  # to prevent token regeneration
import random
import time  # imports time library
import os

import discord  # imports discord library
from discord.ext import commands
from discord.utils import get
import youtube_dl

messages = joined = 0
bot = commands.Bot(command_prefix="m.")
bot.remove_command("help")

bot_id = bot.get_guild(556560880897228803)  # the server is found with the client id
with open('config.json', 'r') as inFile:
    token = json.load(inFile)['token']


@bot.event
async def on_ready():
    print("Bot Up and Running!")


# Function to update stats on messages and members joined every 24 hours
async def update_stats():
    await bot.wait_until_ready()  # waits until the client starts
    global messages, joined  # creates variables for joined members and messages

    while not bot.is_closed():  # while the client is running
        try:
            with open("log.txt", "a") as file:  # opens log.txt file and writes
                # writes info to file
                file.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0  # sets messages to 0
            joined = 0  # sets joined members to 0

            await asyncio.sleep(86400)  # the amount of time to wait until re logging
        except Exception as e:
            print(e)  # exception to be thrown
            await asyncio.sleep(86400)  # every 24 hours


# New client event
@bot.event
async def on_member_join(member):  # Function to welcome new user
    for channel in member.guild.channels:  # loop into channel
        if str(channel) == "general":  # into channel general
            await bot_id.send(f"""Hai! Welcome to the server {member.mention}!""")  # sends welcome message


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**meowBot >.< General Commands**",
                          description="**Some useful commands to access meowBot:**",
                          color=discord.Colour.red())
    embed.add_field(name="```m.help```", value="Lists the commands currently available for the user.", inline=False)
    embed.add_field(name="```m.musichelp```", value="Lists the commands to access music functions.", inline=False)
    embed.add_field(name="```m.misc```", value="Lists fun and miscellaneous functions.", inline=False)
    embed.add_field(name="```m.intro```", value="Greets the user.", inline=False)
    embed.add_field(name="```m.users```", value="Prints number of users.", inline=False)
    embed.add_field(name="```m.purge (num)```", value="Purges however many messages you provide it prior to sending command.",
                    inline=False)
    await ctx.channel.send(content=None, embed=embed)


@bot.command()
async def musichelp(ctx):
    embed = discord.Embed(title="**meowBot >.< Music Commands**",
                          description="**Some useful commands to access meowBot's music functionality:**",
                          color=discord.Colour.red())
    embed.add_field(name="```m.join```",
                    value="Adds the bot to a voice channel if user is already in one. Otherwise, nothing will happen.",
                    inline=False)
    embed.add_field(name="```m.leave```",
                    value="Takes meowBot out of whatever channel the user is in.",
                    inline=False)
    embed.add_field(name="```m.play (url)```",
                    value="Plays youtube url given to the bot from the user.",
                    inline=False)
    embed.add_field(name="```m.pause```",
                    value="Pauses the current song playing.",
                    inline=False)
    embed.add_field(name="```m.resume```",
                    value="Resumes the current song on queue.",
                    inline=False)
    embed.add_field(name="```m.stop```",
                    value="Completely stops song in order to pass a new url to the bot.",
                    inline=False)
    await ctx.channel.send(content=None, embed=embed)


@bot.command()
async def misc(ctx):
    embed = discord.Embed(title="**meowBot >.< Misc Commands**",
                          description="**Some fun and miscellaneous functions that meowBot offers:**",
                          color=discord.Colour.red())
    embed.add_field(name="```m.quote```", value="Prints a random quote for you fellas feeling under the weather.",
                    inline=False)
    embed.add_field(name="```m.dadprogjoke```",
                    value="Provides the user with a funny dad programming joke, if you're into that stuff.",
                    inline=False)
    embed.add_field(name="```m.jojo```",
                    value="Plays the infamous Giorno's Theme from Jojo's Bizarre Adventure. Pretty cool, I know.",
                    inline=False)
    await ctx.channel.send(content=None, embed=embed)


@bot.command()
async def intro(ctx):
    await ctx.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")


@bot.command()
async def purge(ctx, arg):
    await ctx.channel.purge(limit=int(arg))
    await ctx.channel.send("Meow! Your dirty messages are gone :3.")


@bot.command()
async def users(ctx):
    bot_id = bot.get_guild(556560880897228803)  # the server is found with the client id
    users_embed = discord.Embed(title="**User Count!**",
                                description=f"""Number of Members: {bot_id.member_count}""",
                                colour=discord.Colour.green())
    await ctx.channel.send(content=None, embed=users_embed)


@bot.command()
async def quote(ctx):
    await ctx.channel.send(random.choice(list(open('quotes.txt'))))


@bot.command()
async def dadprogjoke(ctx):
    await ctx.channel.send(random.choice(list(open('jokes.txt'))))


@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="**Message Deleted**", description="You might wanna check this out!",
                          colour=discord.Colour.blue())
    embed.add_field(name="Attention!", value=f"""Someone deleted a message! Wanna ask why? :(""")
    await message.channel.send(content=None, embed=embed)


@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)

    else:
        voice = await channel.connect()
        print(f"Bot Connected To {channel}!")

    await ctx.send(f"Joined {channel}! ")


@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"Bot Left {channel}!")
        await ctx.send(f"Bot Left {channel}!")
    else:
        print("Bot Made To Leave, But Couldn't")
        await ctx.send("Bot Made To Leave, But Couldn't")


@bot.command()
async def play(ctx, url: str):
    global name
    song = os.path.isfile("song.mp3")
    try:
        if song:
            os.remove("song.mp3")
            print("Removed File!")
    except PermissionError:
        print("Tried Deleting, Song Playing!")
        await ctx.send("ERROR: Music Playing!")
        return

    await ctx.send("Getting Song Ready!")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading Audio Now!")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3") and file != "giorno.mp3":
            name = file
            print(f"Renamed File: {file}")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}!")
    print("Playing!")


@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        print("Song has paused!")
        await ctx.send("Song has paused!")


@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
        print("Song has resumed playing!")
        await ctx.send("Song has resumed playing!")


@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_paused() or voice.is_playing():
        voice.stop()
        print("Song has stopped playing!")
        await ctx.send("Song has stopped playing!")


@bot.command()
async def jojo(ctx):  # FIXME: check if user is in voice chat or not
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice:
        voice.play(discord.FFmpegPCMAudio("giorno.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07
        await ctx.send("JOJO REFERENCE!")
        print("JOJO Playing!")
    else:
        await ctx.send("Join a voice channel first! -.-")


bot.loop.create_task(update_stats())  # loop for logging into log.txt
bot.run(token)  # where the bot will run (discord server)
