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
        await log_channel.send(f"""MEOW! Member joined: {member.mention}!""") # FIXME: EMBED THIS
        await member.add_roles(role)
        await log_channel.send(f"""Member {member.mention} was given the {role} role!""") # FIXME: EMBED THIS

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.bot.get_channel(int(os.environ.get("LOGS_ID")))
        embed = discord.Embed(title="**Message Deleted**", description="You might wanna check this out!",
                            colour=discord.Colour.blue())
        embed.add_field(name="Attention!", value=f"""Someone deleted a message! Wanna ask why? :(""")
        await channel.send(content=None, embed=embed)

    @commands.command()
    async def load(self, ctx, extension):
        self.bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Cog {extension} was loaded!")
    
    @commands.command()
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'Cogs.{extension}')
        self.bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f"Cog {extension} was reloaded!")
    
    @commands.command()
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'Cogs.{extension}')
        await ctx.send(f"Cog {extension} was unloaded!")

def setup(bot):
    bot.add_cog(Events(bot))