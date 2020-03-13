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
import discord.opus

# loading in classes from other files
from intro import Intro
from music import Music
from general import General
from misc import Misc

# initial commands before running bot
load_dotenv()
bot = commands.Bot(command_prefix="m.")
bot.remove_command("help")

# loading environment variables
bot_id = bot.get_guild(os.environ.get("CLIENT_ID"))  # the server is found with the client id
token = os.environ.get("BOT_TOKEN")

# loaded cogs
bot.add_cog(Intro(bot))
bot.add_cog(Music(bot))
bot.add_cog(General(bot))
bot.add_cog(Misc(bot))

@bot.event
async def on_ready():
    status = discord.Game("meow :3 | m.help")
    await bot.change_presence(status=discord.Status.online, activity=status)
    print("Bot Up and Running!")


bot.run(token)  # where the bot will run (discord server)
