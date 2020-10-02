# external modules for discord bot
from discord.ext import commands

# creates a new dict
commands_tally = {}


# errors cog for displaying to console
class Errors(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # upon error, display to console
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print("Command was used incorrectly. Error:", error)
        await ctx.send("Invalid command. Try another!", delete_after=3)

    # upon command, add to list
    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1

    # on command completion, display to console
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " was used correctly!")


# method to add the cog
def setup(bot):
    bot.add_cog(Errors(bot))
