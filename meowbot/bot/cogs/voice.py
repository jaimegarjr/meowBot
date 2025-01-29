import discord
from discord.ext import commands, tasks
from meowbot.application.models.ytdl_source import YTDLSource
from meowbot.utils.logger import logging, setup_logger
from meowbot.application.models.music_queue import MusicQueue


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = setup_logger(name="cog.voice", level=logging.INFO)
        self.check_leave.start()
        self.music_queue = MusicQueue()

    @commands.hybrid_command(name="join", description="Joins a voice channel")
    async def join(self, ctx):
        try:
            if ctx.message.author.voice is None:
                await ctx.send("You are not in a voice channel!")
                self.logger.error("User is not in a voice channel.")
                return
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

    @commands.hybrid_command(name="leave", description="Leaves a voice channel")
    async def leave(self, ctx):
        if ctx.voice_client:
            channel = ctx.voice_client.channel
            self.music_queue.clear()
            await ctx.voice_client.disconnect()
            self.logger.info(f"Bot left {channel}.")
        else:
            await ctx.send("I'm not in a voice channel!")
            self.logger.error("Bot is not in a voice channel.")

    @tasks.loop(minutes=8)
    async def check_leave(self):
        voice_lists = self.bot.voice_clients
        for x in voice_lists:
            if x.is_connected() and not x.is_playing():
                await x.disconnect()
                self.logger.info(f"meowBot left {x.channel}.")

    @commands.hybrid_command(name="pause", description="Pauses the current song")
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Song has been paused!")
            self.logger.info("Song has been paused.")

    @commands.hybrid_command(name="resume", description="Resumes the current song")
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Song has resumed playing!")
            self.logger.info("Song has resumed playing.")

    @commands.hybrid_command(name="stop", description="Stops the current song")
    async def stop(self, ctx):
        ctx.voice_client.stop()
        await ctx.send("Song has stopped playing!")
        self.logger.info("Song has stopped playing.")

    @commands.hybrid_command(name="play", description="Plays a song from youtube given a URL")
    async def play(self, ctx, *, url):
        if ctx.message.author.voice is None:
            await ctx.send("You are not in a voice channel!")
            self.logger.error("User is not in a voice channel.")
            return

        channel = ctx.message.author.voice.channel

        if not ctx.voice_client:
            await channel.connect()

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                if not player:
                    await ctx.send("Failed to retrieve audio source.")
                    self.logger.error(f"Failed to retrieve audio source for {url}.")
                    return
            except Exception as e:
                self.logger.error(f"Error when trying to play {url}: {e}")
                return
        
        position = self.music_queue.add_to_queue(player)
        if position == 1 and not ctx.voice_client.is_playing():
            self.start_playback(ctx.voice_client, player)
        else:
            self.logger.info(f"Added {player.title} to queue at position {position}.")

        embed = discord.Embed(
            title="**Current Song Playing!**",
            description=f"Playing: {player.title}",
            color=discord.Colour.teal(),
        )
        embed.add_field(name="```User Input```", value=f"Input: {url}", inline=False)
        await ctx.channel.send(embed=embed)
        self.logger.info(f"Playing {player.title} in {channel}.")

    def start_playback(self, voice_client, player):
        if not player or not isinstance(player, discord.AudioSource):
            self.logger.error("Invalid audio source.")
            return
        
        self.logger.info(f"Type of player: {type(player)}")

        def after_playback(error):
            self.logger.info(f"After playback triggered. Error: {error} (Type: {type(error)})")

            if error:
                self.logger.error(f"Error while playing: {error}")
            else:
                self.logger.info(f"Finished playing: {player.title}")
            self.play_next(voice_client)
        
        voice_client.play(
            player,
            after=after_playback
        )
        voice_client.source.volume = 0.10
        self.logger.info(f"Now playing: {player.title}")
    
    def play_next(self, voice_client):
        if not self.music_queue.is_empty():
            next_song = self.music_queue.remove_from_queue()
            if next_song:
                self.start_playback(voice_client, next_song)
                self.logger.info(f"Now playing: {next_song.title}")
            else:
                self.logger.error("Failed to retrieve next song.")
        else:
            self.logger.info("Queue is empty.")
            if voice_client.is_playing():
                voice_client.stop()
                self.logger.info("Stopped playing.")
            self.check_leave.restart()

    @commands.hybrid_command(name="queue", description="Displays the current queue")
    async def queue(self, ctx):
        queue = self.music_queue.queue
        if not queue:
            await ctx.send("Queue is empty!")
            return

        embed = discord.Embed(
            title="**Current Queue**",
            description="List of songs in queue",
            color=discord.Colour.teal(),
        )
        for i, song in enumerate(queue):
            embed.add_field(name=f"Song {i+1}", value=song.title, inline=False)
        await ctx.send(embed=embed)
        self.logger.info("Queue displayed.")
    
    @commands.hybrid_command(name="clear", description="Clears the current queue")
    async def clear(self, ctx):
        self.music_queue.clear()
        await ctx.send("Queue has been cleared!")
        self.logger.info("Queue has been cleared.")
    
    @commands.hybrid_command(name="skip", description="Skips the current song")
    async def skip(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Song has been skipped!")
            self.logger.info("Song has been skipped.")


async def setup(bot):
    await bot.add_cog(Voice(bot))
