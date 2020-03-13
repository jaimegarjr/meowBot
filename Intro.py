# general imported pip modules
import asyncio 
import random
import time
import os

# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv
import discord.opus

load_dotenv()

class Intro (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # FIXME: NOT WORKING
    # @bot.event
    async def on_member_join(self, member): 
        gen_channel = bot.get_channel(int(os.environ.get("GENERAL_ID")))
        log_channel = bot.get_channel(int(os.environ.get("LOGS_ID")))
        role = discord.utils.get(member.guild.roles, name="White Keys")
        await gen_channel.send(f"""Hai! Welcome to the server {member.mention}!""")
        await log_channel.send(f"""MEOW! Member joined: {member.mention}!""") # FIXME: EMBED THIS
        await member.add_roles(role)
        await log_channel.send(f"""Member {member.mention} was given the {role} role!""") # FIXME: EMBED THIS

    
    @commands.command()
    async def intro(self, ctx):
        await ctx.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")