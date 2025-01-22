# external modules for discord bot
from discord.ext import commands
from meowbot.utils import logging, setup_logger


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.errors", level=logging.INFO)
        self.commands_tally = {}

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.logger.error(f"Command was used incorrectly. Error: {error}")
        await ctx.send("Invalid command. Try another!", delete_after=3)

    # TODO: can be improved by metric firing on command usage
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in self.commands_tally:
                self.commands_tally[ctx.command.name] += 1
            else:
                self.commands_tally[ctx.command.name] = 1
        self.logger.info(f"{ctx.command.name} was persisted.")

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        self.logger.info(f"{ctx.command.name} was successfully used.")


async def setup(bot):
    await bot.add_cog(Errors(bot))
