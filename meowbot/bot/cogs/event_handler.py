import importlib
from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services import event_handler_service


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.event.handler", level=logging.INFO)
        self._init_service()

    def _init_service(self):
        importlib.reload(event_handler_service)
        self.event_handler_service = event_handler_service.EventHandlerService()

    def cog_reload(self):
        self._init_service()
        self.logger.info("Event handler service reloaded.")

    def cog_unload(self):
        self.logger.info("Event handler cog unloaded.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.logger.info(f"{member} joined the server.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        time = str(message.created_at)
        time = time[:-16]
        self.logger.info(f"Message {message.id} was deleted at {time}.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.event_handler_service.serve_on_guild_join_event(guild)
        self.logger.info(f"Joined server {guild.name}.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.logger.info(f"Left server {guild.name}.")


async def setup(bot):
    await bot.add_cog(EventHandler(bot))
