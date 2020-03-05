import json
import discord  # imports discord library
import time  # imports time library
import asyncio  # imports asyncio for logging
import random
from discord.ext import commands

# client_id = 556560880897228803
messages = joined = 0
bot = commands.Bot(command_prefix="meow.")

def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines [0].strip()

client = discord.Client()  # stores the client into variable

token = read_token()

@client.event
async def on_ready():
    print("Bot Online")


# Function to update stats on messages and members joined every 24 hours
async def update_stats():
    await client.wait_until_ready()  # waits until the client starts
    global messages, joined  # creates variables for joined members and messages

    while not client.is_closed():  # while the client is running
        try:
            with open("log.txt", "a") as f:  # opens log.txt file and writes
                # writes info to file
                f.write(f"Time: {int(time.time())}, Messages: {messages}, Members Joined: {joined}\n")

            messages = 0  # sets messages to 0
            joined = 0  # sets joined members to 0

            await asyncio.sleep(86400)  # the amount of time to wait until re logging
        except Exception as e:
            print(e)  # exception to be thrown
            await asyncio.sleep(86400)  # every 24 hours


# New client event
@client.event
async def on_member_join(member):  # Function to welcome new user
    global joined  # global variable joined
    joined += 1  # sets joined to increment every time called
    for channel in member.guild.channels:  # loop into channel
        if str(channel) == "general":  # into channel general
            await client.send(f"Hai! Welcome to the server {member.mention}!")  # sends welcome message


# New client event
@client.event
async def on_message(message):  # Command function
    global messages  # global messages variable
    messages += 1  # increments messages

    id = client.get_guild(556560880897228803)  # the server is found with the client id
    channels = ["bots", "bot-testing", "mod-chat"]  # channels that bot commands are allowed in
    bad_words = ["dumb", "stupid", "loser"]

    for word in bad_words:
        if message.content.count(word) > 0:
            await message.channel.purge(limit=1)
            await message.channel.send("Meow! No bad words. -.-")

    if message.content == "meow.help":
        embed = discord.Embed(title="Help On meowBot >.<", description="Some useful commands to access meowBot:")
        embed.add_field(name="meow.intro", value="Greets the user.")
        embed.add_field(name="meow.users", value="Prints number of users.")
        embed.add_field(name="meow.quote", value="Prints a random quote for you fellas feeling under the weather.")
        embed.add_field(name="meow.purge", value="Purges 5 messages prior to sending command.")
        await message.channel.send(content=None, embed=embed)

        # then it will look at possible commands
    if message.content.find("meow.intro") != -1:  # if meow.intro, it'll introduce itself
        await message.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")

    elif message.content == "meow.users":  # if meow.users, will list amount of users
        await message.channel.send(f"""Number of Members: {id.member_count}""")

    if message.content == "meow.quote":
        await message.channel.send(random.choice(list(open('quotes.txt'))))

    elif message.content == "meow.purge":
        await message.channel.purge(limit=5)
        await message.channel.send("Meow! Your dirty messages are gone :3.")

    if message.content == "meow.dadprogjoke":
        await message.channel.send(random.choice(list(open('jokes.txt'))))


client.loop.create_task(update_stats())  # loop for logging into log.txt
client.run(token)  # where the bot will run (discord server)
