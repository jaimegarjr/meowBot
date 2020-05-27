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
            "Here's what I'm built off of. If you'd like to contribute, fork and create a pull request! Github: https://github.com/JJgar2725/meowBot")

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

    # command to play giorno's mp3 file
    @commands.command()
    async def jojo(self, ctx):

        if not ctx.voice_client:
            await ctx.send("Join a voice channel first! -.-")

        elif ctx.voice_client.is_playing():
            await ctx.send("Bot already playing! Use m.stop to stop the current song and play a new song. -.-")

        else:
            ctx.voice_client.play(discord.FFmpegPCMAudio("Songs/giorno.mp3"))
            ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
            ctx.voice_client.source.volume = 0.10
            await ctx.send("JOJO REFERENCE!")
            print("JOJO Playing!")


# setup method to add cog
def setup(bot):
    bot.add_cog(Misc(bot))
