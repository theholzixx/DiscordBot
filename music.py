from __main__ import bot
from discord.ext import commands
import asyncio
from time import sleep
import youtube_dl
import discord
import validators

ytdl_format_options = {
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
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

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

@bot.command()
async def Play(ctx):
    """Plays a Song(If YT URL is provided)"""
    # Gets voice channel of message author
    urlA = ctx.message.content.split(' ', 2)

    if len(urlA) == 3:
        url = urlA[2]
    else:
        url = None

    voice_channel = ctx.author.voice.channel
    if voice_channel != None:
        vc = ctx.voice_client
        if url != None:
            #hier kommt YT code
            if not validators.url(url):
                await ctx.send("not a valid url")
            else:
                async with ctx.typing():
                    player = await YTDLSource.from_url(url, loop=False)
                    vc.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

                await ctx.send(f'Now playing: {player.title}')
        else:
            vc.play(discord.FFmpegPCMAudio(executable="C:/Program Files/ffmpeg-2022-10-13-git-9e8a327e68-full_build/bin/ffmpeg.exe",
            source="C:/Users/hendr/Nextcloud/Musik/coole musik/Frozen Night - II- The Ethereal Forest/Frozen Night - II- The Ethereal Forest - 03 Chrysalis Metamorphosis.mp3"))
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")
    # Delete command after the audio is done playing.

@bot.command()
async def Stop(ctx):
    """Stops and disconnects the bot from voice"""
    
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I am not connected to any voice channel on this server!")

@Play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()