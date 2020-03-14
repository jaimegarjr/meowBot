# general imported pip modules
import os

# imported discord modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="**meowBot >.< General Commands**",
                            description="**Some useful commands to access meowBot:**",
                            color=discord.Colour.red())
        embed.add_field(name="```m.help```", value="Lists the commands currently available for the user.", inline=False)
        embed.add_field(name="```m.musichelp```", value="Lists the commands to access music functions.", inline=False)
        embed.add_field(name="```m.misc```", value="Lists fun and miscellaneous functions.", inline=False)
        embed.add_field(name="```m.intro```", value="Greets the user.", inline=False)
        embed.add_field(name="```m.users```", value="Prints number of users.", inline=False)
        embed.add_field(name="```m.purge (num)```",
                        value="Purges however many messages you provide it prior to sending command.",
                        inline=False)
        await ctx.channel.send(content=None, embed=embed)


    @commands.command()
    async def musichelp(self, ctx):
        embed = discord.Embed(title="**meowBot >.< Music Commands**",
                            description="**Some useful commands to access meowBot's music functionality:**",
                            color=discord.Colour.red())
        embed.add_field(name="```m.join```",
                        value="Adds the bot to a voice channel if user is already in one. Otherwise, nothing will happen.",
                        inline=False)
        embed.add_field(name="```m.leave```",
                        value="Takes meowBot out of whatever channel the user is in.",
                        inline=False)
        embed.add_field(name="```m.play (url) | m.play search term```",
                        value="Plays youtube url given to the bot from the user.",
                        inline=False)
        embed.add_field(name="```m.pause```",
                        value="Pauses the current song playing.",
                        inline=False)
        embed.add_field(name="```m.resume```",
                        value="Resumes the current song on queue.",
                        inline=False)
        embed.add_field(name="```m.stop```",
                        value="Completely stops song in order to pass a new url to the bot.",
                        inline=False)
        await ctx.channel.send(content=None, embed=embed)


    @commands.command()
    async def misc(self, ctx):
        embed = discord.Embed(title="**meowBot >.< Misc Commands**",
                            description="**Some fun and miscellaneous functions that meowBot offers:**",
                            color=discord.Colour.red())
        embed.add_field(name="```m.quote```", value="Prints a random quote for you fellas feeling under the weather.",
                        inline=False)
        embed.add_field(name="```m.dadprogjoke```",
                        value="Provides the user with a funny dad programming joke, if you're into that stuff.",
                        inline=False)
        embed.add_field(name="```m.jojo```",
                        value="Plays the infamous Giorno's Theme from Jojo's Bizarre Adventure. Pretty cool, I know.",
                        inline=False)
        await ctx.channel.send(content=None, embed=embed)

    @commands.command()
    async def intro(self, ctx):
        await ctx.channel.send("Well, hai! :3 I'm JJ's cat-based discord bot!")

    @commands.command()
    async def users(self, ctx):
        bot_id = self.bot.get_guild(int(os.environ.get("CLIENT_ID")))  # the server is found with the client id
        users_embed = discord.Embed(title="**User Count!**",
                                    description=f"""Number of Members: {bot_id.member_count}""",
                                    colour=discord.Colour.green())
        await ctx.channel.send(content=None, embed=users_embed)

    @commands.command()
    async def purge(self, ctx, arg):
        await ctx.channel.purge(limit=int(arg))
        await ctx.channel.send("Meow! Your dirty messages are gone :3.")

def setup(bot):
    bot.add_cog(General(bot))