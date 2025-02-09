import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from meowbot.utils import setup_logger, logging


class MeowBot:
    def __init__(self):
        load_dotenv()
        self.bot_token = os.environ.get("BOT_TOKEN")
        self.cogs_path = "meowbot.bot.cogs"

        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.logger = setup_logger(name="meowbot", level=logging.INFO)
        self.bot = commands.Bot(
            intents=self.intents,
            command_prefix="m.",
            help_command=None,
            description=self.description,
        )

        self.setup_events()
        self.setup_dev_commands()

    @property
    def description(self):
        return """
            Hi! I'm meowBot.
            I was created by jaimegarjr.
            Enjoy my services!
        """

    async def setup(self):
        self.logger.info("Setting up meowBot...")
        await self.load_extensions()

    def run(self):
        self.bot.setup_hook = self.setup
        self.bot.run(self.bot_token)

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

    def setup_dev_commands(self):
        @self.bot.command()
        @commands.is_owner()
        async def load(ctx, extension):
            await self.bot.load_extension(f"{self.cogs_path}.{extension}")
            await ctx.send(f"Cog {extension}.py was loaded!", delete_after=3)

        @self.bot.command()
        @commands.is_owner()
        async def reload(ctx, extension):
            await self.bot.unload_extension(f"{self.cogs_path}.{extension}")
            await self.bot.load_extension(f"{self.cogs_path}.{extension}")
            await ctx.send(f"Cog {extension}.py was reloaded!", delete_after=3)

        @self.bot.command()
        @commands.is_owner()
        async def unload(ctx, extension):
            await self.bot.unload_extension(f"{self.cogs_path}.{extension}")
            await ctx.send(f"Cog {extension}.py was unloaded!", delete_after=3)

    async def load_extensions(self):
        os_cogs_path = self.cogs_path.replace(".", "/")
        cogs = [
            f[:-3] for f in os.listdir(os_cogs_path) if f.endswith(".py") and f != "__init__.py"
        ]
        failed_extensions = []
        loaded_extensions = []

        for ext in cogs:
            try:
                if ext == "channels":
                    continue
                await self.bot.load_extension(f"{self.cogs_path}.{ext}")
                loaded_extensions.append(ext)
            except Exception as e:
                failed_extensions.append((ext, str(e)))
                self.logger.error(f"Failed to load extension {ext}: {str(e)}")
                continue

        total = len(cogs)
        success = len(loaded_extensions)
        failed = len(failed_extensions)

        if failed_extensions:
            self.logger.warning(f"Loaded {success}/{total} cogs. {failed} cogs failed to load.")
            for ext, error in failed_extensions:
                self.logger.debug(f"Extension {ext} failed with: {error}")
        else:
            self.logger.info(f"Successfully loaded cogs {loaded_extensions}.")


if __name__ == "__main__":
    bot_instance = MeowBot()
    bot_instance.run()
