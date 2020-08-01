# general imported pip modules
import os

# imported discord modules
import discord
from discord.ext import commands
from dotenv import load_dotenv

# load in environment variables
load_dotenv()
logo_url = "https://github.com/JJgar2725/meowBot/blob/master/Files/logo.jpg?raw=true"

# class for storing general commands
class General(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # command to display commands to user
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title="**meowBot >.< General Commands**",
                              description="**Some useful commands to access meowBot:**",
                              color=discord.Colour.red())
        embed.set_thumbnail(url=logo_url)
        embed.add_field(
            name="```m.help (none, music, misc, channels)```", value="Lists commands pertaining to a particular topic.", inline=False)
        embed.add_field(name="```m.intro```",
                        value="Greets the user.", inline=False)
        embed.add_field(name="```m.users```",
                        value="Prints number of users.", inline=False)
        embed.add_field(name="```m.purge (num)```",
                        value="Purges however many messages you provide it prior to sending command.",
                        inline=False)
        await user.send(content=None, embed=embed)

    # command to display commands for playing music
    @help.command()
    async def music(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title="**meowBot >.< Music Commands**",
                              description="**Some useful commands to access meowBot's music functionality:**",
                              color=discord.Colour.red())
        embed.set_thumbnail(url=logo_url)
        embed.add_field(name="```m.join```",
                        value="Adds the bot to a voice channel if user is already in one. Otherwise, nothing will "
                              "happen.",
                        inline=False)
        embed.add_field(name="```m.leave```",
                        value="Takes meowBot out of whatever channel the user is in.",
                        inline=False)
        embed.add_field(name="```m.play (url) | m.play (search term)```",
                        value="Plays a song from youtube given by the user.",
                        inline=False)
        embed.add_field(name="```m.pause```",
                        value="Pauses the current song playing.",
                        inline=False)
        embed.add_field(name="```m.resume```",
                        value="Resumes the current song on queue.",
                        inline=False)
        embed.add_field(name="```m.stop```",
                        value="Completely stops any audio from playing on meowBot.",
                        inline=False)
        await user.send(content=None, embed=embed)

    # command to display channel creation commands
    @help.command()
    async def channels(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title="**meowBot >.< Channel Commands**",
                              description="**NOTE**: You need the *Manage Channels* permission to use these commands.\n"
                              "**Some useful commands to create and delete channels with meowBot:**",
                              color=discord.Colour.red())
        embed.set_thumbnail(url=logo_url)
        embed.add_field(name="```m.create (name)```",
                        value="Creates a basic text channel with the given name.",
                        inline=False)
        embed.add_field(name="```m.create voice (name)```",
                        value="Creates a basic voice channel with the given name.",
                        inline=False)
        embed.add_field(name="```m.create priv (name)```",
                        value="Creates a private text channel with the given name.",
                        inline=False)
        embed.add_field(name="```m.create priv_voice (name)```",
                        value="Creates a private voice channel with the given name.",
                        inline=False)
        embed.add_field(name="```m.delete (name)```",
                        value="Deletes a voice / text channel with the given name.",
                        inline=False)
        await user.send(content=None, embed=embed)

    # command to display misc commands
    @help.command()
    async def misc(self, ctx):
        user = ctx.message.author
        embed = discord.Embed(title="**meowBot >.< Misc Commands**",
                              description="**Some fun and miscellaneous functions that meowBot offers:**",
                              color=discord.Colour.red())
        embed.set_thumbnail(url=logo_url)
        embed.add_field(name="```m.quote```", value="Prints a random quote for you fellas feeling under the weather.",
                        inline=False)
        embed.add_field(name="```m.github```",
                        value="Gives the caller a link to the github repo that meowBot runs off of.",
                        inline=False)
        embed.add_field(name="```m.dadprogjoke```",
                        value="Provides the user with a funny dad programming joke, if you're into that stuff.",
                        inline=False)
        embed.add_field(name="```m.jojo```",
                        value="Plays the infamous Giorno's Theme from Jojo's Bizarre Adventure. Pretty cool, I know.",
                        inline=False)
        await user.send(content=None, embed=embed)

    # command to display an intro message
    @commands.command()
    async def intro(self, ctx):
        await ctx.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")

    # @commands.command()
    # async def roles(self, ctx):
    #     member = ctx.message.author
    #     l = member.roles
    #     l_format = []
    #     # l.pop(0) # removes @everyone
    #     for role in range(0, len(l)):
    #         l_format.append(l[role])
    #         print(l[role])

    #     roles_embed = discord.Embed(title="**Your Roles!**",
    #                                 description=f"""Roles: {l_format}""",
    #                                 colour=discord.Colour.teal())
    #     await ctx.channel.send(content=None, embed=roles_embed)

    # command to display amount of users on server
    @commands.command()
    async def users(self, ctx):
        guild_members = ctx.guild.member_count
        users_embed = discord.Embed(title="**Current User Count on Guild!**",
                                    description=f"""Number of Members: {guild_members}""",
                                    colour=discord.Colour.green())
        await ctx.channel.send(content=None, embed=users_embed)

    # command to purge a specific amount of messages
    @commands.command()
    async def purge(self, ctx, arg):
        await ctx.channel.purge(limit=(int(arg) + 1))


# setup method to add bot
def setup(bot):
    bot.add_cog(General(bot))
