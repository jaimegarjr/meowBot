import json  # to prevent token regeneration
import discord  # imports discord library
import time  # imports time library
import asyncio  # imports asyncio for logging
import random
from discord.ext import commands

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

# New client event
@bot.event
async def on_message(message):  # Command function
    bad_words = ["dumb", "stupid", "loser", "idiot"]  # file of bad words?
    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Meow! No bad words. -.-")

    await bot.process_commands(message)

@bot.command()
async def hello(ctx):
    await ctx.channel.send("Hello.")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="**meowBot >.< Commands**",
                          description="**Some useful commands to access meowBot:**",
                          color=discord.Colour.red())
    embed.add_field(name="```m.help```", value="Lists the commands currently available for the user.", inline=False)
    embed.add_field(name="```m.intro```", value="Greets the user.", inline=False)
    embed.add_field(name="```m.users```", value="Prints number of users.", inline=False)
    embed.add_field(name="```m.purge```", value="Purges however many messages you provide it prior to sending command.",
                    inline=False)
    embed.add_field(name="```m.quote```", value="Prints a random quote for you fellas feeling under the weather.",
                    inline=False)
    embed.add_field(name="```m.dadprogjoke```",
                    value="Provides the user with a funny dad programming joke, if you're into that stuff.",
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


# @bot.command
# async def join(ctx):
#     global vc
#     endpoint = ["Music Room"]
#     vc = endpoint
#     await vc.connect(timeout=60.0, reconnect=True)
#     print(vc.is_connected())
#
# @bot.command
# async def leave(ctx):
#     endpoint = ["Music Room"]
#     voicec = endpoint
#     await voicec.disconnect(force=False)

bot.loop.create_task(update_stats())  # loop for logging into log.txt
bot.run(token)  # where the bot will run (discord server)
