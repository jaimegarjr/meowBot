import asyncio
import discord
from discord.ext import commands, tasks
import yt_dlp as youtube_dl
from meowbot.utils.logger import logging, setup_logger

queue = asyncio.Queue()
play_next_song = asyncio.Event()

youtube_dl.utils.bug_reports_message = lambda: ""

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "extract_flat": "in_playlist",
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn",
}

ytdl = youtube_dl.YoutubeDL(ydl_opts)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.music", level=logging.INFO)

        self.check_leave.start()

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            if ctx.voice_client is not None:
                await ctx.voice_client.move_to(channel)
                self.logger.info(f"Bot moved to {channel}.")

            else:
                self.check_leave.restart()
                await channel.connect()
                self.logger.info(f"Bot connected to {channel}.")

        except AttributeError:
            await ctx.send("Join a voice channel first! -.-")
            self.logger.error("User did not join a voice channel before attempting to join.")

        await ctx.send(f"Joined {channel}! ")
        self.logger.info(f"Bot joined {channel}.")

    @commands.command()
    async def leave(self, ctx):
        try:
            await ctx.voice_client.disconnect()
            self.logger.info(f"Bot left {ctx.voice_client.channel}.")
        except AttributeError:
            await ctx.send("I'm not in a voice channel! -.-")
            self.logger.error("Bot was not in a voice channel before attempting to leave.")

    @tasks.loop(minutes=8)
    async def check_leave(self):
        voice_lists = self.bot.voice_clients
        for x in voice_lists:
            if x.is_connected() and not x.is_playing():
                await x.disconnect()
                self.logger.info(f"meowBot left {x.channel}.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Song has been paused!")
            self.logger.info("Song has been paused.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Song has resumed playing!")
            self.logger.info("Song has resumed playing.")

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Song has stopped playing!")
        self.logger.info("Song has stopped playing.")

    @commands.command()
    async def play(self, ctx, *, url):
        channel = ctx.message.author.voice.channel

        if not ctx.voice_client or not channel:
            await channel.connect()

        elif ctx.voice_client.is_playing():
            await ctx.send("Bot already playing! -.- New song commencing now.")
            ctx.voice_client.stop()
            self.logger.info("Bot was already playing a song. Stopping to play new song.")

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(
                player,
                after=lambda e: print(f"{player.title} has finished playing!"),
            )
            ctx.voice_client.source.volume = 0.10

        embed = discord.Embed(
            title="**Current Song Playing!**",
            description=f"Playing: {player.title}",
            color=discord.Colour.teal(),
        )
        embed.add_field(name="```User Input```", value=f"Input: {url}", inline=False)
        await ctx.channel.send(content=None, embed=embed)
        self.logger.info(f"Playing {player.title} in {channel}.")


async def setup(bot):
    await bot.add_cog(Music(bot))
