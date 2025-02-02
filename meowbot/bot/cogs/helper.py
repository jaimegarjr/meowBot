from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services.helper_service import HelperService


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.helper_service = HelperService()
        self.logger = setup_logger(name="cog.general", level=logging.INFO)

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
