# general imported pip modules
import os

# imported discord modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member): 
        gen_channel = self.bot.get_channel(int(os.environ.get("GENERAL_ID")))
        log_channel = self.bot.get_channel(int(os.environ.get("LOGS_ID")))
        role = discord.utils.get(member.guild.roles, name="White Keys")
        await gen_channel.send(f"""Hai! Welcome to the server {member.mention}!""")

        embed = discord.Embed(title="**Member Joined**", description = "Someone joined the server!", colour=discord.Colour.blue())
        embed.add_field(name="Attention!", value=f"""MEOW! Member joined: {member.mention}!""", inline=False)
        await log_channel.send(content=None, embed=embed)

        await member.add_roles(role)

        embed = discord.Embed(title="**Role Assigned**", description = "A role was given to a member!", colour=discord.Colour.blue())
        embed.add_field(name="Attention!", value=f"""Member {member.mention} was given the {role} role!""", inline=False)
        await log_channel.send(content=None, embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(int(os.environ.get("LOGS_ID")))
        time = str(message.created_at)
        time = time[:-16]
        embed = discord.Embed(title="**Message Deleted**", description="You might wanna check this out!",
                            colour=discord.Colour.red())
        embed.add_field(name="Attention!", value=f"""Someone deleted a message! Wanna ask why? :(""", inline=False)
        embed.add_field(name="Info", value=f"""Message ID: {message.id} | Date: {time}""", inline=False)
        await channel.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))