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
load_dotenv()

commands_tally = {

}

class Commands(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(ctx.command.name + " was used incorrectly.")
        print(error)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        if ctx.command is not None:
            if ctx.command.name in commands_tally:
                commands_tally[ctx.command.name] += 1
            else:
                commands_tally[ctx.command.name] = 1
            print(commands_tally)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " was used correctly!")

def setup(bot):
    bot.add_cog(Commands(bot))