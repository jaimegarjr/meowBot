import importlib
from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services import helper_service


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.helper", level=logging.INFO)
        self._init_service()

    def _init_service(self):
        importlib.reload(helper_service)
        self.helper_service = helper_service.HelperService()

    def cog_reload(self):
        self._init_service()
        self.logger.info("Helper service reloaded.")

    def cog_unload(self):
        self.logger.info("Helper cog unloaded.")

    @commands.hybrid_group(
        name="help",
        description="Lists commands pertaining to a particular topic",
        invoke_without_command=True,
    )
    async def help(self, ctx):
        user = ctx.message.author
        embed = self.helper_service.serve_help_command_embed()
        await user.send(embed=embed)
        self.logger.info(f"User {user} requested help.")

    @help.command()
    async def music(self, ctx):
        user = ctx.message.author
        embed = self.helper_service.serve_music_command_embed()
        await user.send(embed=embed)
        self.logger.info(f"User {user} requested music help.")

    @help.command()
    async def misc(self, ctx):
        user = ctx.message.author
        embed = self.helper_service.serve_misc_command_embed()
        await user.send(embed=embed)
        self.logger.info(f"User {user} requested misc help.")


async def setup(bot):
    await bot.add_cog(Helper(bot))
