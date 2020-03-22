# general imported pip modules
import random
import os

# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
load_dotenv()

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx):
        await ctx.channel.send(random.choice(list(open('Files/quotes.txt'))))

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
            

def setup(bot):
    bot.add_cog(Misc(bot))