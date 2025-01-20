# imported discord modules
import discord
from discord.ext import commands

# cog for storing creation commands
class Creation(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # command to create a basic text channel
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def create(self, ctx, *, channel_name: str):

        channel = await ctx.guild.create_text_channel(channel_name)
        await channel.send("Text channel {} was created!".format(channel_name))

    # command to create a basic voice channel
    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def voice(self, ctx, *, channel_name: str):

        channel = await ctx.guild.create_voice_channel(channel_name)
        await ctx.send("Voice channel {} was created!".format(channel_name))

    # command to create a private text channel
    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def priv(self, ctx, *, channel_name: str):
        
        # find needed roles and store them in variables for later use
        admin = discord.utils.get(ctx.guild.roles, name="Supreme Piano Ruler")
        mods = discord.utils.get(ctx.guild.roles, name="Black Keys")

        # using a dictionary, permissions can be chosen for the new channel
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
        await channel.send("Private text channel {} was created!".format(channel_name))

    # command to create a private voice channel
    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def priv_voice(self, ctx, *, channel_name: str):

        admin = discord.utils.get(ctx.guild.roles, name="Supreme Piano Ruler")
        mods = discord.utils.get(ctx.guild.roles, name="Black Keys")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await ctx.guild.create_voice_channel(channel_name, overwrites=overwrites)
        await ctx.send("Private voice channel {} was created!".format(channel_name))

    # command to delete a given channel
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx, *, channel_name: str):

        # search through channels on a guild for given channel name
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        await channel.delete()
        await ctx.send("Channel {} was deleted!".format(channel_name))

# setup method to add bot
async def setup(bot):
    await bot.add_cog(Creation(bot))