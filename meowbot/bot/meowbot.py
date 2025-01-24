import logging
import os
import json
import asyncio

import discord
from discord.ext import commands
from dotenv import load_dotenv
from meowbot.utils import setup_logger


class MeowBot:
    def __init__(self):
        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.logger = setup_logger(name="meowbot", level=logging.INFO)
        self.bot = commands.Bot(
            intents=self.intents,
            command_prefix=self.get_prefix,
            help_command=None,
            description=self.description,
        )

        self.setup_events()
        self.setup_commands()

    @property
    def description(self):
        return """
            Hi! I'm meowBot.
            I was created by JJgar2725 (otherwise known as PROFLIT).
            Enjoy my services!
        """

    def get_prefix(self, client, message):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        return prefixes.get(str(message.guild.id), "m.")

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(
                status=discord.Status.online, activity=discord.Game("meow :3 | m.help")
            )
            try:
                self.logger.info("Syncing commands...")
                synced = await self.bot.tree.sync()
                self.logger.info(f"Synced {len(synced)} commands.")
            except Exception as e:
                self.logger.error(f"Error syncing commands: {e}")
            self.logger.info("meowBot is purring! :3")

    def setup_commands(self):
        @self.bot.command()
        @commands.is_owner()
        async def load(ctx, extension):
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension}.py was loaded!", delete_after=3)

        @self.bot.command()
        @commands.is_owner()
        async def reload(ctx, extension):
            self.bot.unload_extension(f"cogs.{extension}")
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension}.py was reloaded!", delete_after=3)

        @self.bot.command()
        @commands.is_owner()
        async def unload(ctx, extension):
            self.bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"Cog {extension}.py was unloaded!", delete_after=3)

    async def load_extensions(self):
        cogs_path = "meowbot/bot/cogs"
        cogs = [f[:-3] for f in os.listdir(cogs_path) if f.endswith(".py") and f != "__init__.py"]
        for ext in cogs:
            await self.bot.load_extension(f"meowbot.bot.cogs.{ext}")
        self.logger.info("Cogs loaded!")

    def run(self):
        self.logger.info("Starting meowBot...")
        load_dotenv()
        asyncio.run(self.load_extensions())
        self.bot.run(os.environ.get("BOT_TOKEN"))


if __name__ == "__main__":
    bot_instance = MeowBot()
    bot_instance.run()
