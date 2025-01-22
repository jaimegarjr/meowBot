import logging
import os
import json
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
from meowbot.utils import setup_logger

intents = discord.Intents.default()
intents.message_content = True

logger = setup_logger(name="meowbot", level=logging.INFO)


def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


description = """
    Hi! I'm meowBot.
    I was created by JJgar2725 (otherwise known as PROFLIT).
    Enjoy my services!
"""

bot = commands.Bot(
    intents=intents,
    command_prefix=get_prefix,
    help_command=None,
    description=description,
)


# bot event to display once up and running
@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game("meow :3 | m.help")
    )
    logger.info("meowBot is purring! :3")


# command to load the cog
@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Cog {extension}.py was loaded!", delete_after=3)


# command to reload the cog
@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")
    await ctx.send(f"Cog {extension}.py was reloaded!", delete_after=3)


# command to unload the cog
@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Cog {extension}.py was unloaded!", delete_after=3)


if __name__ == "__main__":
    logger.info("Starting meowBot...")

    load_dotenv()

    logger.info("Loading cogs...")
    cogs = os.listdir("meowbot/bot/cogs")
    extensions = [ext[:-3] for ext in cogs if ext.endswith(".py")]
    extensions.remove("__init__")

    async def load_extensions():
        for ext in extensions:
            await bot.load_extension("meowbot.bot.cogs." + ext)
        logger.info("Cogs loaded!")

    asyncio.run(load_extensions())
    bot.run(os.environ.get("BOT_TOKEN"))
