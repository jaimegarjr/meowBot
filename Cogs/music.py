# general imported pip modules
import os

# imported discord modules
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
from dotenv import load_dotenv
load_dotenv()

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        try:
            channel = ctx.message.author.voice.channel
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if voice and voice.is_connected():
                await voice.move_to(channel)

            else:
                voice = await channel.connect()
                print(f"Bot Connected To {channel}!")

        except AttributeError:
            await ctx.send("Join a voice channel first! -.-")
            return

        await ctx.send(f"Joined {channel}! ")

    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.disconnect()
            print(f"Bot Left {channel}!")
            await ctx.send(f"Bot Left {channel}!")
        
        else:
            print("Bot Made To Leave, But Couldn't")
            await ctx.send("Bot Made To Leave, But Couldn't")


    @commands.command()
    async def play(self, ctx, *, url: str):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        channel = ctx.message.author.voice.channel

        if not voice:
            await ctx.send("Join a voice channel first! -.-")

        elif voice.is_playing():
            await ctx.send("Bot already playing! Use m.stop to stop the current song and play a new song. -.-")
            return

        # elif not users.voice and voice.is_connected():
            #     await discord.utils.sleep_until(second=10, result=voice.disconnect())
            #     print(f"Bot Left {channel}!")
            #     await ctx.send(f"Bot Left {channel}!")
        
        else:
            song = os.path.isfile("Songs/song.mp3")
            try:
                if song:
                    os.remove("Songs/song.mp3")
                    print("Removed File!")
                    
            except PermissionError:
                print("Tried Deleting, Song Playing!")
                await ctx.send("ERROR: Music Playing!")
                return

            await ctx.send("Getting Song Ready!")

            ydl_opts = {
                'format': 'bestaudio/best',
                'default_search': "ytsearch",
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                print("Downloading Audio Now!")
                ydl.download([url])

            for file in os.listdir("./"):
                if file.endswith(".mp3") and file != "giorno.mp3":
                    name = file
                    print(f"Renamed File: {file}")
                    os.rename(file, "Songs/song.mp3")

            voice.play(discord.FFmpegPCMAudio("Songs/song.mp3"), after=lambda e: print(f"{name} has finished playing!"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.10

            nname = name.rsplit("-", 2)

            embed = discord.Embed(title="**Current Song Playing!**",
                                description=f"Playing: {nname[0]} - {nname[1]}",
                                color=discord.Colour.purple())
            embed.add_field(name="```Youtube Link```",
                            value=f"URL / Input: {url}",
                            inline=False)
            await ctx.channel.send(content=None, embed=embed)

            print("Playing!")


    @commands.command()
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            print("Song has paused!")
            await ctx.send("Song has paused!")


    @commands.command()
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            print("Song has resumed playing!")
            await ctx.send("Song has resumed playing!")


    @commands.command()
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused() or voice.is_playing():
            voice.stop()
            print("Song has stopped playing!")
            await ctx.send("Song has stopped playing!")

def setup(bot):
    bot.add_cog(Music(bot))