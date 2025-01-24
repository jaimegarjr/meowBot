import discord
from discord.ext import commands
from dotenv import load_dotenv
from meowbot.utils import logging, setup_logger


class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.general", level=logging.INFO)
        self.logo_url = "https://github.com/JJgar2725/meowBot/blob/master/Files/logo.jpg?raw=true"
        load_dotenv()

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
        embed.set_thumbnail(url=self.logo_url)
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
        embed.set_thumbnail(url=self.logo_url)
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
        embed.set_thumbnail(url=self.logo_url)
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
        embed.set_thumbnail(url=self.logo_url)
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


async def setup(bot):
    await bot.add_cog(Helper(bot))
