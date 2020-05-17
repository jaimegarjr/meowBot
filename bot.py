# general pip modules
import asyncio
import random
import time
import os

# external modules for discord bot
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv

# initial commands before running bot
load_dotenv()
bot = commands.Bot(command_prefix="m.")
bot.remove_command("help")

# loading environment variables
bot_id = bot.get_guild(os.environ.get("CLIENT_ID"))  # the server is found with the client id
token = os.environ.get("BOT_TOKEN")


@bot.event
async def on_ready():
    status = discord.Game("meow :3 | m.help")
    await bot.change_presence(status=discord.Status.online, activity=status)
    print("Bot Up and Running!")


@bot.command()
@commands.has_role('Supreme Piano Ruler')
async def load(ctx, extension):
    bot.load_extension(f'Cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was loaded!")


@bot.command()
@commands.has_role('Supreme Piano Ruler')
async def reload(ctx, extension):
    bot.unload_extension(f'Cogs.{extension}')
    bot.load_extension(f'Cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was reloaded!")


@bot.command()
@commands.has_role('Supreme Piano Ruler')
async def unload(ctx, extension):
    bot.unload_extension(f'Cogs.{extension}')
    await ctx.send(f"Cog {extension}.py was unloaded!")


extensions = ['Cogs.events', 'Cogs.general', 'Cogs.music', 'Cogs.misc', 'Cogs.errors']

if __name__ == '__main__':
    for ext in extensions:
        bot.load_extension(ext)

bot.run(token)  # where the bot will run (discord server)
