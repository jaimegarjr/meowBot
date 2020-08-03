# general imported pip modules
import random

# imported discord modules
import discord
from discord.ext import commands


# cog for misc commands
class Misc(commands.Cog):
    # constructor
    def __init__(self, bot):
        self.bot = bot

    # command to display a random quote from a file
    @commands.command()
    async def quote(self, ctx):
        await ctx.channel.send(random.choice(list(open('Files/quotes.txt'))))

    # command to display the github page for this project
    @commands.command()
    async def github(self, ctx):
        await ctx.channel.send(
            "Here's what I'm built off of. If you'd like to contribute, fork and create a pull request! Github: "
            "https://github.com/JJgar2725/meowBot")

    # command to display a random joke from jokes.txt
    @commands.command()
    async def dadprogjoke(self, ctx):
        quote = random.choice(list(open('Files/jokes.txt')))
        quoteQ = quote[1:quote.find("A")]
        quoteA = quote[quote.find("A") - 1:-2]

        embed = discord.Embed(title="**Dad-Styled Programming Joke**",
                              description="**Chosen at random!**",
                              color=discord.Colour.light_grey())
        embed.add_field(name="```Question```", value=quoteQ, inline=False)
        embed.add_field(name="```Answer```", value=quoteA, inline=False)
        await ctx.channel.send(content=None, embed=embed)


# setup method to add cog
def setup(bot):
    bot.add_cog(Misc(bot))
