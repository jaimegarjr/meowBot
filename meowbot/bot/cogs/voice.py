import importlib
from discord.ext import commands
from meowbot.utils import logging, setup_logger
from meowbot.application.services import voice_service


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.voice", level=logging.INFO)
        self._init_service()

    def _init_service(self):
        importlib.reload(voice_service)
        self.voice_service = voice_service.VoiceService(self.bot)

    def cog_reload(self):
        self._init_service()
        self.logger.info("Voice service reloaded.")

    def cog_unload(self):
        self.logger.info("Voice cog unloaded.")

    @commands.hybrid_command(name="join", description="Joins a voice channel")
    async def join(self, ctx):
        await self.voice_service.join_voice_channel(ctx)

    @commands.hybrid_command(name="leave", description="Leaves a voice channel")
    async def leave(self, ctx):
        await self.voice_service.leave_voice_channel(ctx)

    @commands.hybrid_command(name="pause", description="Pauses the current song")
    async def pause(self, ctx):
        await self.voice_service.pause_song(ctx)

    @commands.hybrid_command(name="resume", description="Resumes the current song")
    async def resume(self, ctx):
        await self.voice_service.resume_song(ctx)

    @commands.hybrid_command(name="stop", description="Stops the current song")
    async def stop(self, ctx):
        await self.voice_service.stop_song(ctx)

    @commands.hybrid_command(name="play", description="Plays a song from youtube given a URL")
    async def play(self, ctx, *, url):
        await self.voice_service.play_song(ctx, url)

    @commands.hybrid_command(name="queue", description="Displays the current queue")
    async def queue(self, ctx):
        await self.voice_service.get_queue(ctx)

    @commands.hybrid_command(name="clear", description="Clears the current queue")
    async def clear(self, ctx):
        await self.voice_service.clear_queue(ctx)

    @commands.hybrid_command(name="skip", description="Skips the current song")
    async def skip(self, ctx):
        await self.voice_service.skip_song(ctx)


async def setup(bot):
    await bot.add_cog(Voice(bot))
