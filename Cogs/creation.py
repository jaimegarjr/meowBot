# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get

# class for storing creation commands
class Creation(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # command to create a basic text channel
    @commands.command()
    async def create_text(self, ctx, new_channel):
        member = ctx.message.author # stores member in a variable
        guild = ctx.guild # stores the guild into a variable

        # checks if the user who invoked the command has permissions, return otherwise
        # manage_channels must be true in order to allow making and managing channels
        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a text channel!")
            return 

        channel = await guild.create_text_channel(new_channel, overwrites=None, category=guild.categories[1], reason=None)
        await channel.send(f"Text channel {new_channel} was created!")

    # command to create a basic voice channel
    @commands.command()
    async def create_voice(self, ctx, new_channel):
        member = ctx.message.author
        guild = ctx.guild

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a voice channel!")
            return 

        # note: ctx.guild.categories will return a list of possible categories that the server has
        # you can then select where the channel will be created in the category list
        channel = await guild.create_voice_channel(new_channel, overwrites=None, category=guild.categories[2], reason=None)
        await ctx.send(f"Voice channel {new_channel} was created!")

    # command to create a private text channel
    @commands.command()
    async def priv_text_channel(self, ctx, new_channel):
        member = ctx.message.author
        guild = ctx.guild

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a private text channel!")
            return 
        
        # use discord.utils.get() for retrieving and storing a role into variables
        # guild.roles is an iterable, and name is an attribute to search for
        admin = get(guild.roles, name="Supreme Piano Ruler") # Your Admin Role
        mods = get(guild.roles, name="Black Keys") # Your Moderator Roles (optional)

        # using a dictionary, permissions can be chosen for the new channel
        # guild.default_role is @everyone, guild.me is the bot itself
        # using admin and mods allows to include them into the new channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_text_channel(new_channel, overwrites=overwrites, category=guild.categories[3], reason=None)
        await channel.send(f"Private text channel {new_channel} was created!")

    # command to create a private voice channel
    @commands.command()
    async def priv_voice_channel(self, ctx, new_channel):
        member = ctx.message.author
        guild = ctx.guild

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a private voice channel!")
            return 
        
        admin = get(guild.roles, name="Supreme Piano Ruler")
        mods = get(guild.roles, name="Black Keys")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }

        channel = await guild.create_voice_channel(new_channel, overwrites=overwrites, category=guild.categories[2], reason=None)
        await ctx.send(f"Private voice channel {new_channel} was created!")

    # command to delete a given channel
    @commands.command()
    async def channel_delete(self, ctx, channel_name):
        member = ctx.message.author
        guild = ctx.guild

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a private voice channel!")
            return 

        # using discord.utils.get() and bot.get_all_channels(), you can specify an attribute
        # to search through an iterable, in this case all the channels on a guild
        channel = get(self.bot.get_all_channels(), name=channel_name)
        await channel.delete()

        await ctx.send(f"Channel {channel_name} was deleted!")

# setup method to add bot
def setup(bot):
    bot.add_cog(Creation(bot))