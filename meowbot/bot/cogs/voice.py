from discord.ext import commands
from meowbot.utils.logger import logging, setup_logger
from meowbot.application.services.voice_service import VoiceService


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.voice", level=logging.INFO)
        self.voice_service = VoiceService(bot)

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
    
    def cog_unload(self):
        self.logger.info("Voice cog unloaded.")


async def setup(bot):
    await bot.add_cog(Voice(bot))
