# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get

# class for storing creation commands
class Creation(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def create_text(self, ctx, name_of_channel):
        member = ctx.message.author
        guild = ctx.guild
        name = name_of_channel

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a text channel!")
            return 

        channel = await guild.create_text_channel(str(name), overwrites=None, category=guild.categories[1], reason=None)
        await channel.send(f"Text channel {name} was created!")

    @commands.command()
    async def create_voice(self, ctx, name_of_channel):
        member = ctx.message.author
        guild = ctx.guild
        name = name_of_channel

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a voice channel!")
            return 

        # guild.categories[5]
        channel = await guild.create_voice_channel(str(name), overwrites=None, category=guild.categories[2], reason=None)
        await channel.send(f"Voice channel {name} was created!")

    @commands.command()
    async def priv_text_channel(self, ctx, name_of_channel):
        member = ctx.message.author
        guild = ctx.guild
        name = name_of_channel

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a private text channel!")
            return 
        
        admin = get(guild.roles, name="Supreme Piano Ruler") # Your Admin Role
        mods = get(guild.roles, name="Black Keys") # Your Moderator Roles (optional)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }
        
        # guild.categories[5]
        channel = await guild.create_text_channel(str(name), overwrites=overwrites, category=guild.categories[3], reason=None)
        await channel.send(f"Private text channel {name} was created!")

    @commands.command()
    async def priv_voice_channel(self, ctx, name_of_channel):
        member = ctx.message.author
        guild = ctx.guild
        name = name_of_channel

        if member.guild_permissions.manage_channels == False:
            await ctx.send("You don't have the permissions to make a private voice channel!")
            return 
        
        admin = get(guild.roles, name="Supreme Piano Ruler") # Your Admin Role
        mods = get(guild.roles, name="Black Keys") # Your Moderator Roles (optional)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            admin: discord.PermissionOverwrite(read_messages=True),
            mods: discord.PermissionOverwrite(read_messages=True)
        }

        # guild.categories[5]
        channel = await guild.create_voice_channel(str(name), overwrites=overwrites, category=guild.categories[2], reason=None)
        await ctx.send(f"Private voice channel {name} was created!")

# setup method to add bot
def setup(bot):
    bot.add_cog(Creation(bot))