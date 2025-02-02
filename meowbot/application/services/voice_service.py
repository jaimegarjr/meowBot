import discord
from discord.ext import tasks
from meowbot.application.models.ytdl_source import YTDLSource
from meowbot.utils.logger import logging, setup_logger
from meowbot.application.models.music_queue import MusicQueue
from itertools import islice


class VoiceService:
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="service.voice", level=logging.INFO)
        self.check_leave.start()
        self.music_queue = MusicQueue()

    def is_user_in_voice_channel(self, ctx):
        return ctx.message.author.voice is not None

    def is_bot_in_voice_channel(self, ctx):
        return ctx.voice_client is not None

    async def send_message(self, ctx, content):
        await ctx.send(content)
        self.logger.info(content)

    @tasks.loop(minutes=8)
    async def check_leave(self):
        voice_lists = self.bot.voice_clients
        for vl in voice_lists:
            if vl.is_connected() and not vl.is_playing():
                await vl.disconnect()
                self.logger.info(f"meowBot left {vl.channel}.")

    async def join_voice_channel(self, ctx):
        if not self.is_user_in_voice_channel(ctx):
            await self.send_message(ctx, "You are not in a voice channel!")
            return

        channel = ctx.message.author.voice.channel
        voice_client = ctx.voice_client

        if voice_client:
            await voice_client.move_to(channel)
            await self.send_message(ctx, f"Bot moved to {channel}.")
        else:
            self.check_leave.restart()
            await channel.connect()
            await self.send_message(ctx, f"Joined {channel}! ")

    async def leave_voice_channel(self, ctx):
        if not self.is_bot_in_voice_channel(ctx):
            await self.send_message(ctx, "I'm not in a voice channel!")
            return

        channel = ctx.voice_client.channel
        self.music_queue.clear()
        await ctx.voice_client.disconnect()
        await self.send_message(ctx, f"Bot left {channel}.")

    async def pause_song(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await self.send_message(ctx, "Song has been paused!")

    async def resume_song(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await self.send_message(ctx, "Song has resumed playing!")

    async def stop_song(self, ctx):
        ctx.voice_client.stop()
        await self.send_message(ctx, "Song has stopped playing!")

    async def skip_song(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await self.send_message(ctx, "Song has been skipped!")

    async def get_queue(self, ctx):
        if self.music_queue.is_empty():
            await self.send_message(ctx, "Queue is empty!")
            return

        embed = discord.Embed(
            title="**Current Queue**",
            description="List of songs in queue:",
            color=discord.Colour.teal(),
        )
        length = len(self.music_queue.queue)

        for i, song in enumerate(islice(self.music_queue.queue, 10)):
            embed.add_field(name=f"Song {i+1}: ", value=song.title, inline=True)

        if length > 10:
            embed.set_footer(text=f"...and {length - 10} more songs.")

        await ctx.send(embed=embed)

    async def clear_queue(self, ctx):
        self.music_queue.clear()
        await self.send_message(ctx, "Queue has been cleared!")

    async def play_song(self, ctx, url):
        if not self.is_user_in_voice_channel(ctx):
            await self.send_message(ctx, "You are not in a voice channel!")
            return

        channel = ctx.message.author.voice.channel

        if not self.is_bot_in_voice_channel(ctx):
            await channel.connect()

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                if not player:
                    self.send_message(ctx, "Failed to retrieve audio source.")
                    return
            except Exception as e:
                self.logger.error(f"Error when trying to play {url}: {e}")
                return

        embed = self.add_song_to_queue(ctx, player, url)
        await ctx.channel.send(embed=embed)

    def add_song_to_queue(self, ctx, player, url):
        position = self.music_queue.add_to_queue(player)

        if position == 1 and not ctx.voice_client.is_playing():
            self.start_playback(ctx.voice_client, player)
            embed_title = "**Current Song Playing!**"
            embed_desc = f"Playing: {player.title}"
        else:
            embed_title = "**Song Added to Queue!**"
            embed_desc = f"Added: {player.title}"

        embed = discord.Embed(
            title=embed_title, description=embed_desc, color=discord.Colour.teal()
        )
        embed.add_field(name="```User Input```", value=f"Input: {url}", inline=False)
        if position > 1:
            embed.add_field(
                name="```Position in Queue```", value=f"Position: {position}", inline=True
            )

        return embed

    def start_playback(self, voice_client, player):
        if not player or not isinstance(player, discord.AudioSource):
            self.logger.error("Invalid audio source.")
            return

        def after_playback(error):
            if error:
                self.logger.error(f"Error while playing: {error}")
            else:
                self.logger.info(f"Finished playing: {player.title}")
            self.play_next(voice_client)

        voice_client.play(player, after=after_playback)
        voice_client.source.volume = 0.10
        self.logger.info(f"Now playing: {player.title}")

    def play_next(self, voice_client):
        next_song = self.music_queue.remove_from_queue()

        if not next_song:
            self.logger.info("Queue is empty.")
            if voice_client.is_playing():
                voice_client.stop()
                self.logger.info("Stopped playing.")
            self.check_leave.restart()
            return

        self.start_playback(voice_client, next_song)
        self.logger.info(f"Now playing: {next_song.title}")
