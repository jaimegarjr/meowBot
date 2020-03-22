# general imported pip modules
import os
import asyncio

# imported discord modules
import discord
from discord.ext import tasks, commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

youtube_dl.utils.bug_reports_message = lambda: ''

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ydl_opts)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            else:
                await channel.connect()
                print(f"Bot Connected To {channel}!")

        except:
            await ctx.send("Join a voice channel first! -.-")
            return

        await ctx.send(f"Joined {channel}! ")

    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, url):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel

        if not voice or not channel:
            await ctx.send("Join a voice channel first! -.-")

        elif voice.is_playing():
            await ctx.send("Bot already playing! -.-")
            return
        
        else:
            async with ctx.typing():
                await ctx.send("Getting Song Ready!")
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=lambda e: print(f"{player.title} has finished playing!"))
                ctx.voice_client.source.volume = 0.10

            embed = discord.Embed(title="**Current Song Playing!**",
                                description=f"Playing: {player.title}",
                                color=discord.Colour.teal())
            embed.add_field(name="```Youtube Link```",
                            value=f"URL: FIX ME",
                            inline=False)
            embed.add_field(name="```User Input```",
                            value=f"Input: {url}",
                            inline=False)
            await ctx.channel.send(content=None, embed=embed)

            print("Playing!")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            print("Song has paused!")
            await ctx.send("Song has paused!")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            print("Song has resumed playing!")
            await ctx.send("Song has resumed playing!")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        print("Song has stopped playing!")
        await ctx.send("Song has stopped playing!")

def setup(bot):
    bot.add_cog(Music(bot))