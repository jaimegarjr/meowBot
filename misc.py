# general imported pip modules
import asyncio 
import random
import time
import os

# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv
import discord.opus

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
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice:
            voice.play(discord.FFmpegPCMAudio("Songs/giorno.mp3"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.10
            await ctx.send("JOJO REFERENCE!")
            print("JOJO Playing!")

        elif voice.is_playing():
            await ctx.send("Bot already playing! Use m.stop to stop the current song and play a new song. -.-")
            return

        else:
            await ctx.send("Join a voice channel first! -.-")
            return