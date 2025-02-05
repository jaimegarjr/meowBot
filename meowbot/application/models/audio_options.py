ytdl_opts = {
    "format": "bestaudio[ext=webm]/bestaudio/best",
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
    "geo_bypass": True,
    "noprogress": True,
    "overwrites": True,
    "cachedir": False,
    "external_downloader": "aria2c",
    "external_downloader_args": ["-x", "16", "-k", "1M"],
}

ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 \
      -probesize 32M -analyzeduration 0",
    "options": "-vn -loglevel error -bufsize 64k",
}
