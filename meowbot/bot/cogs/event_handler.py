import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
from discord.utils import get
from meowbot.utils import logging, setup_logger

load_dotenv()


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.event.handler", level=logging.INFO)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        gen_channel = get(member.guild.channels, name="general")
        log_channel = get(member.guild.channels, name="logs")
        role = get(member.guild.roles, name="White Keys")
        await gen_channel.send(f"""Hai! Welcome to the server {member.mention}!""")

        embed = discord.Embed(
            title="**Member Joined**",
            description="Someone joined the server!",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="Attention!",
            value=f"""MEOW! Member joined: {member.mention}!""",
            inline=False,
        )
        await log_channel.send(content=None, embed=embed)

        await member.add_roles(role)

        embed = discord.Embed(
            title="**Role Assigned**",
            description="A role was given to a member!",
            colour=discord.Colour.blue(),
        )
        embed.add_field(
            name="Attention!",
            value=f"""Member {member.mention} was given the {role} role!""",
            inline=False,
        )
        await log_channel.send(content=None, embed=embed)
        self.logger.info(f"{member} joined the server. Role {role} was assigned.")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        log_channel = get(message.guild.channels, name="logs")
        time = str(message.created_at)
        time = time[:-16]
        embed = discord.Embed(
            title="**Message Deleted**",
            description=None,
            colour=discord.Colour.red(),
        )
        embed.add_field(
            name="Attention!",
            value="""Someone deleted a message! Wanna ask why? :(""",
            inline=False,
        )
        embed.add_field(
            name="Info",
            value=f"""Message ID: {message.id} | Date: {time}""",
            inline=False,
        )
        await log_channel.send(content=None, embed=embed)
        self.logger.info(f"Message {message.id} was deleted at {time}.")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.logger.info(f"Joined server {guild.name}.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.logger.info(f"Left server {guild.name}.")


async def setup(bot):
    await bot.add_cog(EventHandler(bot))
