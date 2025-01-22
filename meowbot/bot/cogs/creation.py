# imported discord modules
import discord
from discord.ext import commands
from meowbot.utils import logging, setup_logger


class Creation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.creation", level=logging.INFO)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels=True)
    async def create(self, ctx, *, channel_name: str):
        channel = await ctx.guild.create_text_channel(channel_name)
        await channel.send("Text channel {} was created!".format(channel_name))
        self.logger.info(f"Text channel {channel_name} was created.")

    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def voice(self, ctx, *, channel_name: str):
        await ctx.guild.create_voice_channel(channel_name)
        await ctx.send("Voice channel {} was created!".format(channel_name))
        self.logger.info(f"Voice channel {channel_name} was created.")

    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def priv(self, ctx, *, channel_name: str):
        admin = discord.utils.get(ctx.guild.roles, name="Supreme Piano Ruler")
        mods = discord.utils.get(ctx.guild.roles, name="Black Keys")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True),
        }

        channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
        await channel.send("Private text channel {} was created!".format(channel_name))
        self.logger.info(f"Private text channel {channel_name} was created.")

    @create.command()
    @commands.has_permissions(manage_channels=True)
    async def priv_voice(self, ctx, *, channel_name: str):
        admin = discord.utils.get(ctx.guild.roles, name="Supreme Piano Ruler")
        mods = discord.utils.get(ctx.guild.roles, name="Black Keys")

        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True),
        }

        await ctx.guild.create_voice_channel(channel_name, overwrites=overwrites)
        await ctx.send("Private voice channel {} was created!".format(channel_name))
        self.logger.info(f"Private voice channel {channel_name} was created.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def delete(self, ctx, *, channel_name: str):
        channel = discord.utils.get(ctx.guild.channels, name=channel_name)
        await channel.delete()
        await ctx.send("Channel {} was deleted!".format(channel_name))
        self.logger.info(f"Channel {channel_name} was deleted.")


async def setup(bot):
    await bot.add_cog(Creation(bot))
