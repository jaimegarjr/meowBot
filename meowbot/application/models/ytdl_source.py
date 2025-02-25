import asyncio
import discord
import yt_dlp as youtube_dl
from .audio_options import ytdl_opts, ffmpeg_options

youtube_dl.utils.bug_reports_message = lambda: ""
ytdl = youtube_dl.YoutubeDL(ytdl_opts)


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

        if data is None:
            print(f"Error: Could not extract info from {url}")
            return None

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        if not filename:
            print(f"Error: Could not prepare filename for {url}")
            return None

        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
