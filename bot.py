import json  # to prevent token regeneration
import discord  # imports discord library
import time  # imports time library
import asyncio  # imports asyncio for logging
import random
from discord.ext import commands

messages = joined = 0
bot = commands.Bot(command_prefix="m.")

client = discord.Client()  # stores the client into variable
client_id = client.get_guild(556560880897228803)  # the server is found with the client id
with open('config.json', 'r') as inFile:
    token = json.load(inFile)['token']


@client.event
async def on_ready():
    print("Bot Up and Running!")


# Function to update stats on messages and members joined every 24 hours
async def update_stats():
    await client.wait_until_ready()  # waits until the client starts
    global messages, joined  # creates variables for joined members and messages

    while not client.is_closed():  # while the client is running
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
@client.event
async def on_member_join(member):  # Function to welcome new user
    for channel in member.guild.channels:  # loop into channel
        if str(channel) == "general":  # into channel general
            await client_id.send(f"""Hai! Welcome to the server {member.mention}!""")  # sends welcome message


# New client event
@client.event
async def on_message(message):  # Command function
    client_id = client.get_guild(556560880897228803)  # the server is found with the client id
    channels = ["bots", "bot-testing", "mod-chat", "logs"]  # channels that bot commands are allowed in
    bad_words = ["dumb", "stupid", "loser", "idiot"]

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Meow! No bad words. -.-")

    if message.content == "m.help":
        embed = discord.Embed(title="**meowBot >.< Commands**",
                              description="**Some useful commands to access meowBot:**",
                              color=discord.Colour.red())
        embed.add_field(name="**m.intro**", value="Greets the user.", inline=False)
        embed.add_field(name="**m.users**", value="Prints number of users.", inline=False)
        embed.add_field(name="**m.quote**", value="Prints a random quote for you fellas feeling under the weather.", inline=False)
        embed.add_field(name="**m.purge**", value="Purges 5 messages prior to sending command.", inline=False)
        await message.channel.send(content=None, embed=embed)

        # then it will look at possible commands
    if message.content.find("m.intro") != -1:  # if meow.intro, it'll introduce itself
        await message.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")

    elif message.content == "m.users":  # if meow.users, will list amount of users
        users_embed = discord.Embed(title="**User Count!**",
                                    description=f"""Number of Members: {client_id.member_count}""",
                                    colour=discord.Colour.green())
        await message.channel.send(content=None, embed=users_embed)

    if message.content == "m.quote":
        await message.channel.send(random.choice(list(open('quotes.txt'))))

    elif message.content == "m.purge":
        await message.channel.purge(limit=5)
        await message.channel.send("Meow! Your dirty messages are gone :3.")

    if message.content == "m.dadprogjoke":
        await message.channel.send(random.choice(list(open('jokes.txt'))))


@client.event
async def on_message_delete(message):
    embed = discord.Embed(title="**Message Deleted**", description="You might wanna check this out!",
                          colour=discord.Colour.blue())
    embed.add_field(name="Attention!", value=f"""Someone deleted a message! Wanna ask why? :(""")
    await message.channel.send(content=None, embed=embed)


client.loop.create_task(update_stats())  # loop for logging into log.txt
client.run(token)  # where the bot will run (discord server)
