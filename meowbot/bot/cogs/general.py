import os
import json
import discord
from discord.ext import commands
from dotenv import load_dotenv
from meowbot.utils import logging, setup_logger

load_dotenv()
logo_url = "https://github.com/JJgar2725/meowBot/blob/master/Files/logo.jpg?raw=true"


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.general", level=logging.INFO)

    @commands.hybrid_group(
        name="help",
        description="Lists commands pertaining to a particular topic",
        invoke_without_command=True,
    )
    async def help(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(
            title="**meowBot >.< General Commands**",
            description="**Some useful commands to access meowBot:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=logo_url)
        embed.add_field(
            name="```m.help (none, music, misc, channels)```",
            value="Lists commands pertaining to a particular topic.",
            inline=False,
        )
        embed.add_field(name="```m.intro```", value="Greets the user.", inline=False)
        embed.add_field(name="```m.users```", value="Prints number of users.", inline=False)
        embed.add_field(
            name="```m.purge (num)```",
            value="Purges however many messages you provide it prior to sending command.",
            inline=False,
        )
        embed.add_field(
            name="```m.invite```",
            value="Provides the user with a link to invite meowBot to different servers!",
            inline=False,
        )
        await user.send(content=None, embed=embed)
        self.logger.info(f"User {user} requested help.")

    @help.command()
    async def music(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(
            title="**meowBot >.< Music Commands**",
            description="**Some useful commands to access meowBot's music functionality:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=logo_url)
        embed.add_field(
            name="```m.join```",
            value="Adds the bot to a voice channel if user is already in one. "
            "Otherwise, nothing will happen.",
            inline=False,
        )
        embed.add_field(
            name="```m.leave```",
            value="Takes meowBot out of whatever channel the user is in.",
            inline=False,
        )
        embed.add_field(
            name="```m.play (url) | m.play (search term)```",
            value="Plays a song from youtube given by the user.",
            inline=False,
        )
        embed.add_field(
            name="```m.pause```",
            value="Pauses the current song playing.",
            inline=False,
        )
        embed.add_field(
            name="```m.resume```",
            value="Resumes the current song on queue.",
            inline=False,
        )
        embed.add_field(
            name="```m.stop```",
            value="Completely stops any audio from playing on meowBot.",
            inline=False,
        )
        await user.send(content=None, embed=embed)
        self.logger.info(f"User {user} requested music help.")

    @help.command()
    async def channels(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(
            title="**meowBot >.< Channel Commands**",
            description="**NOTE**: You need the *Manage Channels* "
            "permission to use these commands.\n"
            "**Some useful commands to create and delete channels with meowBot:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=logo_url)
        embed.add_field(
            name="```m.create (name)```",
            value="Creates a basic text channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create voice (name)```",
            value="Creates a basic voice channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create priv (name)```",
            value="Creates a private text channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.create priv_voice (name)```",
            value="Creates a private voice channel with the given name.",
            inline=False,
        )
        embed.add_field(
            name="```m.delete (name)```",
            value="Deletes a voice / text channel with the given name.",
            inline=False,
        )
        await user.send(content=None, embed=embed)
        self.logger.info(f"User {user} requested channel help.")

    @help.command()
    async def misc(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(
            title="**meowBot >.< Misc Commands**",
            description="**Some fun and miscellaneous functions that meowBot offers:**",
            color=discord.Colour.red(),
        )
        embed.set_thumbnail(url=logo_url)
        embed.add_field(
            name="```m.quote```",
            value="Prints a random quote for you fellas feeling under the weather.",
            inline=False,
        )
        embed.add_field(
            name="```m.github```",
            value="Gives the caller a link to the github repo that meowBot runs off of.",
            inline=False,
        )
        embed.add_field(
            name="```m.dadprogjoke```",
            value="Provides the user with a funny dad programming joke, if you're into that stuff.",
            inline=False,
        )
        embed.add_field(
            name="```m.profile (other users)```",
            value="Sends the user a detailed tag of their profile on Discord.",
            inline=False,
        )
        await user.send(content=None, embed=embed)
        self.logger.info(f"User {user} requested misc help.")

    @commands.hybrid_command(name="intro", description="Greets the user")
    async def intro(self, ctx):
        await ctx.channel.send("Well, hai! :3 I'm jaimegarjr's cat-based discord bot!")
        self.logger.info("User requested intro message.")

    @commands.hybrid_command(name="users", description="Prints number of users")
    async def users(self, ctx):
        guild_members = ctx.guild.member_count
        users_embed = discord.Embed(
            title="**Current User Count on Guild!**",
            description=f"""Number of Members: {guild_members}""",
            colour=discord.Colour.green(),
        )
        await ctx.channel.send(content=None, embed=users_embed)
        self.logger.info(f"User requested user count of guild {ctx.guild}.")

    @commands.hybrid_command(
        name="purge", description="Purges however many messages you provide it"
    )
    async def purge(self, ctx, arg):
        await ctx.channel.purge(limit=(int(arg) + 1))
        self.logger.info(f"User {ctx.author} purged {arg} messages in {ctx.channel}.")

    @commands.hybrid_command(
        name="invite", description="Provides the user with a link to invite meowBot"
    )
    async def invite(self, ctx):
        client_id = os.environ.get("CLIENT_ID")
        permissions = discord.Permissions.none()
        permissions.manage_roles = True
        permissions.manage_channels = True
        permissions.view_channel = True
        permissions.send_messages = True
        permissions.manage_messages = True
        permissions.embed_links = True
        permissions.attach_files = True
        permissions.read_message_history = True
        permissions.use_external_emojis = True
        permissions.add_reactions = True
        permissions.connect = True
        permissions.speak = True
        permissions.ban_members = True
        permissions.kick_members = True
        link = discord.utils.oauth_url(client_id, permissions=permissions, redirect_uri=None)
        await ctx.send(f"<{link}>")
        self.logger.info(f"User {ctx.author} requested invite link.")

    @commands.is_owner()
    @commands.hybrid_command(name="changeprefix", description="Changes the prefix for meowBot")
    async def changeprefix(self, ctx, prefix):
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Prefix changed to '{prefix}'. Enjoy!")
        self.logger.info(f"Prefix changed to '{prefix}' for guild {ctx.guild}.")


async def setup(bot):
    await bot.add_cog(General(bot))
