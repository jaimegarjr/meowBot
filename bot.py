# general pip modules
import os
import json
import asyncio

# external modules for discord bot
import discord
from discord.ext import commands
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.message_content = True

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

description = """Hi! I'm meowBot. I was created by JJgar2725 (otherwise known as PROFLIT). Enjoy my services!"""
bot = commands.Bot(intents=intents, command_prefix=get_prefix, help_command=None, description=description)
        
# bot event to display once up and running
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("meow :3 | m.help"))
    print("Bot Up and Running!")

# command to load the cog
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was loaded!", delete_after=3)

# command to reload the cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was reloaded!", delete_after=3)

# command to unload the cog
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was unloaded!", delete_after=3)

if __name__ == '__main__':
    # loads in environment variables
    load_dotenv()

    # makes a list of the cogs
    extensions = [
        'creation', 
        'events', 
        'general',
        'music', 
        'misc', 
        'errors'
    ]

    async def load_extensions():
        # a loop to load each cog in
        for ext in extensions:
            await bot.load_extension('cogs.' + ext)

    asyncio.run(load_extensions())


    # runs the bot
    bot.run(os.environ.get("BOT_TOKEN"))  
