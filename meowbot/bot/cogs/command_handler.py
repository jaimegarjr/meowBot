import importlib
from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services import command_handler_service


class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.command.handler", level=logging.INFO)
        self._init_service()

    def _init_service(self):
        importlib.reload(command_handler_service)
        self.command_handler_service = command_handler_service.CommandHandlerService()

    def cog_reload(self):
        self._init_service()
        self.logger.info("Command handler service reloaded.")

    def cog_unload(self):
        self.logger.info("Command handler cog unloaded.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.logger.error(f"Command was used incorrectly. Error: {error}")
        await ctx.send("Invalid command. Try another!", delete_after=3)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.command_handler_service.serve_on_command_event(ctx)
        self.logger.info(f"{ctx.command.name} was persisted.")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.logger.info(f"{ctx.command.name} was successfully used.")


async def setup(bot):
    await bot.add_cog(CommandHandler(bot))
